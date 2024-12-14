"""Agent-related CLI commands."""

from __future__ import annotations

import asyncio
import shutil
from typing import Any

from llmling.cli.constants import output_format_opt, verbose_opt
from llmling.cli.utils import format_output
from promptantic import ModelGenerator
from pydantic import ValidationError
import typer as t

from llmling_agent import config_resources
from llmling_agent.cli import agent_store, resolve_agent_config
from llmling_agent.models import AgentsManifest


agent_cli = t.Typer(help="Agent management commands", no_args_is_help=True)


@agent_cli.command("init")
def init_agent_config(
    output: str = t.Argument(help="Path to write agent configuration file"),
    interactive: bool = t.Option(
        False,
        "--interactive/--no-interactive",
        help="Use interactive configuration wizard",
    ),
) -> None:
    """Initialize a new agent configuration file.

    Creates a new configuration file at the specified path with agent definitions.
    Use --interactive for a guided setup process.
    """
    if interactive:
        generator = ModelGenerator()
        manifest = generator.populate(AgentsManifest)
        manifest.save(output)
        print(f"\nCreated agent configuration file: {output}")
    else:
        # Copy template file
        shutil.copy2(config_resources.AGENTS_TEMPLATE, output)
        print(f"\nCreated agent configuration file: {output}")
        print("\nTry these commands:")
        print("  llmling-agent list")
        print("  llmling-agent chat url_opener")
        print("  llmling-agent run system_inspector")


@agent_cli.command("add")
def add_agent_file(
    name: str = t.Argument(help="Name for the agent configuration file"),
    path: str = t.Argument(help="Path to agent configuration file"),
    verbose: bool = verbose_opt,
) -> None:
    """Add a new agent configuration file."""
    try:
        agent_store.add_config(name, path)
        t.echo(f"Added agent configuration '{name}' -> {path}")
    except Exception as e:
        t.echo(f"Error adding configuration: {e}", err=True)
        raise t.Exit(1) from e


@agent_cli.command("set")
def set_active_file(
    name: str = t.Argument(help="Name of agent configuration to set as active"),
    verbose: bool = verbose_opt,
) -> None:
    """Set the active agent configuration file."""
    try:
        agent_store.set_active(name)
        t.echo(f"Set '{name}' as active agent configuration")
    except Exception as e:
        t.echo(f"Error setting active configuration: {e}", err=True)
        raise t.Exit(1) from e


@agent_cli.command("run")
def run_agent(
    agent_name: str = t.Argument(help="Agent name(s) to run (can be comma-separated)"),
    prompts: list[str] = t.Argument(  # noqa: B008
        None,
        help="Prompts to send to the agent(s)",
    ),
    config_path: str = t.Option(
        None,
        "-c",
        "--config",
        help="Override agent configuration path",
    ),
    prompt_index: int = t.Option(
        0,
        "--index",
        "-i",
        help="Index of predefined prompt to start with",
    ),
    environment: str = t.Option(
        None,
        "--environment",
        "-e",
        help="Override agent's environment",
    ),
    model: str = t.Option(
        None,
        "--model",
        "-m",
        help="Override agent's model",
    ),
    output_format: str = output_format_opt,
    verbose: bool = verbose_opt,
) -> None:
    """Run one or more agents with the given prompts."""
    from llmling_agent.models import AgentsManifest
    from llmling_agent.runners import AgentOrchestrator, AgentRunConfig

    try:
        # Resolve configuration path
        try:
            config_path = resolve_agent_config(config_path)
        except ValueError as e:
            msg = str(e)
            raise t.BadParameter(msg) from e

        # Load agent definition
        try:
            agent_def = AgentsManifest.from_file(config_path)
        except ValidationError as e:
            t.echo("Agent configuration validation failed:", err=True)
            for error in e.errors():
                location = " -> ".join(str(loc) for loc in error["loc"])
                t.echo(f"  {location}: {error['msg']}", err=True)
            raise t.Exit(1) from e

        # Parse agent names
        agent_names = [name.strip() for name in agent_name.split(",")]

        # Build final prompt list
        final_prompts: list[str] = []

        # Add predefined prompt if available
        if prompt_index is not None:
            for name in agent_names:
                config = agent_def.agents[name]
                if config.user_prompts:
                    try:
                        final_prompts.append(config.user_prompts[prompt_index])
                        break
                    except IndexError:
                        continue

        # Add provided prompts
        if prompts:
            final_prompts.extend(prompts)

        # Create run configuration
        run_config = AgentRunConfig(
            agent_names=agent_names,
            prompts=final_prompts,
            environment=environment,
            model=model,
            output_format=output_format,
        )

        # Create and run orchestrator
        orchestrator = AgentOrchestrator[Any](agent_def, run_config)

        async def run() -> None:
            try:
                results = await orchestrator.run()
                # Format results based on whether we ran single or multiple agents
                if len(agent_names) == 1:
                    # Single agent results is a list of RunResults
                    for result in results:  # type: ignore
                        format_output(result.data, output_format)
                else:
                    # Multiple agent results is a dict of agent -> list[RunResult]
                    formatted: dict[str, list[Any]] = {
                        name: [r.data for r in agent_results]
                        for name, agent_results in results.items()  # type: ignore
                    }
                    format_output(formatted, output_format)
            finally:
                await orchestrator.cleanup()

        asyncio.run(run())

    except t.Exit:
        raise
    except Exception as e:
        t.echo(f"Error: {e}", err=True)
        if verbose:
            import traceback

            t.echo(traceback.format_exc(), err=True)
        raise t.Exit(1) from e


@agent_cli.command("list")
def list_agents(
    config_name: str = t.Option(
        None,
        "-c",
        "--config",
        help="Name of agent configuration to list (defaults to active)",
    ),
    output_format: str = output_format_opt,
    verbose: bool = verbose_opt,
) -> None:
    """List agents from the active (or specified) configuration."""
    from llmling_agent.models import AgentsManifest

    try:
        try:
            config_path = resolve_agent_config(config_name)
        except ValueError as e:
            msg = str(e)
            raise t.BadParameter(msg) from e

        # Load and validate agent definition
        agent_def = AgentsManifest.from_file(config_path)
        # Set the name field from the dict key for each agent
        agents = [
            agent.model_copy(update={"name": name})
            for name, agent in agent_def.agents.items()
        ]
        format_output(agents, output_format)

    except t.Exit:
        raise
    except Exception as e:
        t.echo(f"Error: {e}", err=True)
        if verbose:
            import traceback

            t.echo(traceback.format_exc(), err=True)
        raise t.Exit(1) from e
