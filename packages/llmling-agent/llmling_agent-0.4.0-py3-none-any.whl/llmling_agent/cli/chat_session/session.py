from __future__ import annotations

import logging
import traceback
from typing import TYPE_CHECKING

import httpx
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown

from llmling_agent.chat_session import ChatSessionManager
from llmling_agent.chat_session.models import ChatMessage
from llmling_agent.cli.chat_session import utils
from llmling_agent.cli.chat_session.base import CommandContext
from llmling_agent.cli.chat_session.config import HISTORY_DIR, SessionState
from llmling_agent.cli.chat_session.status import StatusBar


if TYPE_CHECKING:
    from llmling_agent import LLMlingAgent
    from llmling_agent.chat_session.base import AgentChatSession
    from llmling_agent.cli.chat_session.base import Command


logger = logging.getLogger(__name__)


class InteractiveSession:
    """Interactive chat session using prompt_toolkit."""

    def __init__(
        self,
        agent: LLMlingAgent[str],
        *,
        debug: bool = False,
    ) -> None:
        """Initialize interactive session."""
        self.agent = agent
        self.debug = debug
        self.console = Console()

        # Internal state
        self._session_manager = ChatSessionManager()
        self._chat_session: AgentChatSession | None = None
        self._state = SessionState()
        self._commands: dict[str, Command] = {}
        self.status_bar = StatusBar(self.console)

        # Setup components
        self._setup_history()
        self._setup_prompt()
        self._register_commands()

    @property
    def chat_session(self) -> AgentChatSession:
        """Get current chat session."""
        if self._chat_session is None:
            msg = "Chat session not initialized"
            raise RuntimeError(msg)
        return self._chat_session

    def _setup_history(self) -> None:
        """Setup command history."""
        HISTORY_DIR.mkdir(parents=True, exist_ok=True)
        history_file = HISTORY_DIR / f"{self.agent.name}.history"
        self._history = FileHistory(str(history_file))

    def _setup_prompt(self) -> None:
        """Setup prompt toolkit session."""
        auto = AutoSuggestFromHistory()
        self._prompt = PromptSession[str](
            "You: ", history=self._history, auto_suggest=auto
        )

    async def _handle_message(self, message: str) -> None:
        """Handle chat message."""
        try:
            # Create user message
            user_message = ChatMessage(content=message, role="user")
            self._state.update_tokens(user_message)
            self.console.print("\nAssistant:", style="bold blue")

            with Live("", console=self.console) as live:
                response_parts = []
                try:
                    response = await self.chat_session.send_message(message, stream=True)
                    async for chunk in response:
                        response_parts.append(chunk.content)
                        md = Markdown("".join(response_parts))
                        live.update(md)
                        # Update tokens for assistant message
                        self._state.update_tokens(chunk)
                except (httpx.ReadError, GeneratorExit):
                    # Handle streaming interruptions gracefully
                    if response_parts:
                        # If we got partial response, show it
                        self.console.print("\nConnection interrupted. Partial response:")
                        self.console.print(Markdown("".join(response_parts)))
                    else:
                        raise  # Re-raise if we got nothing

            # Update message count after complete response
            self._state.message_count += 2
            self.status_bar.render(self._state)

        except Exception as e:  # noqa: BLE001
            error_msg = utils.format_error(e)
            self.console.print(f"\n[red bold]Error:[/] {error_msg}")
            if self.debug:
                md = Markdown(f"```python\n{traceback.format_exc()}\n```")
                self.console.print("\n[dim]Debug traceback:[/]", md)
            # Ensure status bar is still shown even after error
            self.status_bar.render(self._state)

    async def start(self) -> None:
        """Start interactive session."""
        try:
            self._chat_session = await self._session_manager.create_session(self.agent)
            self._state.current_model = self._chat_session._model
            await self._show_welcome()

            while True:
                try:
                    user_input = await self._prompt.prompt_async()
                    if not user_input:
                        continue

                    if user_input.startswith("/"):
                        await self._handle_command(user_input[1:])
                    else:
                        await self._handle_message(user_input)

                except KeyboardInterrupt:
                    self.console.print("\nUse /exit to quit")
                    continue
                except EOFError:
                    break
                except Exception as e:  # noqa: BLE001
                    error_msg = utils.format_error(e)
                    self.console.print(f"\n[red bold]Error:[/] {error_msg}")
                    if self.debug:
                        md = Markdown(f"```python\n{traceback.format_exc()}\n```")
                        self.console.print("\n[dim]Debug traceback:[/]", md)
                    continue

        except Exception as e:  # noqa: BLE001
            self.console.print(f"\n[red bold]Fatal Error:[/] {utils.format_error(e)}")
            if self.debug:
                md = Markdown(f"```python\n{traceback.format_exc()}\n```")
                self.console.print("\n[dim]Debug traceback:[/]", md)
        finally:
            await self._cleanup()
            await self._show_summary()

    def _register_commands(self) -> None:
        """Register available commands."""
        from .commands.builtin import get_builtin_commands

        for command in get_builtin_commands():
            self._commands[command.name] = command

    async def _handle_command(self, input_: str) -> None:
        """Handle command input."""
        cmd, *args = input_.split(maxsplit=1)
        arg = args[0] if args else ""
        command = self._commands.get(cmd)
        if not command:
            self.console.print(f"Unknown command: {cmd}", style="red")
            return

        try:
            context = CommandContext(
                console=self.console,
                session=self.chat_session,
                state=self._state,
                args=arg,
            )
            await command.execute(context)
            self._state.last_command = cmd
        except EOFError:
            raise  # Re-raise EOFError to be caught by main loop
        except Exception as e:  # noqa: BLE001
            self.console.print(f"Error executing command: {e}", style="red")
            if self.debug:
                self.console.print(traceback.format_exc())

    async def _show_welcome(self) -> None:
        """Show welcome message."""
        self.console.print(f"\nStarted chat with {self.agent.name}")
        self.console.print("Type /help for commands or /exit to quit\n")

        # Show initial state
        tools = self.chat_session.get_tool_states()
        enabled = sum(1 for enabled in tools.values() if enabled)
        text = f"Available tools: {len(tools)} ({enabled} enabled)"
        self.console.print(text, style="dim")

        # Show initial status
        self.status_bar.render(self._state)

    async def _cleanup(self) -> None:
        """Cleanup resources."""
        if self._chat_session:
            # Any cleanup needed for chat session
            pass

    async def _show_summary(self) -> None:
        """Show session summary."""
        if self._state.message_count > 0:
            self.console.print("\nSession Summary:")
            self.console.print(f"Messages: {self._state.message_count}")
            token_info = (
                f"Total tokens: {self._state.total_tokens:,} "
                f"(Prompt: {self._state.prompt_tokens:,}, "
                f"Completion: {self._state.completion_tokens:,})"
            )
            self.console.print(token_info)


# Helper function for CLI
async def start_interactive_session(
    agent: LLMlingAgent[str],
    *,
    debug: bool = False,
) -> None:
    """Start an interactive chat session."""
    session = InteractiveSession(agent, debug=debug)
    await session.start()
