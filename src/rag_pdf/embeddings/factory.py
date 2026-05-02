from __future__ import annotations

import os

from rag_pdf.config import Settings

from .openai_embeddings import OpenAIEmbeddingProvider
from .protocol import EmbeddingProvider


def create_embedding_provider(settings: Settings) -> EmbeddingProvider:
    provider = settings.embedding_provider.lower().strip()

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY") or None
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Create a .env file or export OPENAI_API_KEY in your shell."
            )
        return OpenAIEmbeddingProvider(
            model=settings.embedding_model,
            api_key=api_key,
        )

    raise ValueError(f"Unsupported EMBEDDING_PROVIDER: {settings.embedding_provider!r}")
