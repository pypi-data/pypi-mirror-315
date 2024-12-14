"""Package resources for LLMling configuration."""

from __future__ import annotations

import importlib.resources
from typing import Final

OPEN_BROWSER: Final[str] = str(
    importlib.resources.files("llmling_agent.config_resources") / "open_browser.yml"
)
SUMMARIZE_README: Final[str] = str(
    importlib.resources.files("llmling_agent.config_resources") / "summarize_readme.yml"
)


__all__ = ["OPEN_BROWSER", "SUMMARIZE_README"]
