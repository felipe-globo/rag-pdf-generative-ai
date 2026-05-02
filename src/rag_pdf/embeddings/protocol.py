from __future__ import annotations

from typing import Protocol, Sequence


class EmbeddingProvider(Protocol):
    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        """Return embedding vectors aligned with `texts` order."""

    @property
    def model_name(self) -> str:
        """Stable model identifier included in deterministic chunk IDs."""
