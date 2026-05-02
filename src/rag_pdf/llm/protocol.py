from __future__ import annotations

from typing import Protocol


class LLMProvider(Protocol):
    @property
    def model_name(self) -> str:
        """Stable LLM identifier for logging/debug."""

    def generate(self, *, system_prompt: str, user_prompt: str) -> str:
        """Return the assistant response text."""

