from __future__ import annotations

import os

from rag_pdf.config import Settings

from .openai_chat import OpenAIChatProvider
from .protocol import LLMProvider


def create_llm_provider(settings: Settings) -> LLMProvider:
    provider = settings.llm_provider.lower().strip()

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY") or None
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Create a .env file or export OPENAI_API_KEY in your shell."
            )
        return OpenAIChatProvider(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
            api_key=api_key,
        )

    raise ValueError(f"Unsupported LLM_PROVIDER: {settings.llm_provider!r}")

