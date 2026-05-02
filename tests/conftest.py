from __future__ import annotations

import hashlib
from typing import Sequence

import pytest


class FakeEmbeddingProvider:
    """Deterministic embeddings (no HTTP). Fixed dimensionality for Chroma."""

    def __init__(self, dimension: int = 8, model_name: str = "test-embed-model"):
        self._dim = dimension
        self._model_name = model_name

    @property
    def model_name(self) -> str:
        return self._model_name

    def _vec(self, text: str, salt: bytes = b"") -> list[float]:
        h = hashlib.sha256(salt + text.encode("utf-8")).digest()
        floats: list[float] = []
        for i in range(0, len(h), 2):
            if len(floats) >= self._dim:
                break
            u16 = int.from_bytes(h[i : i + 2], "big") or 1
            floats.append(float((u16 % 10000) / 10000.0))
        while len(floats) < self._dim:
            floats.append(0.0)
        return floats

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        return [self._vec(t, salt=b"d") for t in texts]


class FakeLLMProvider:
    def __init__(self, model_name: str = "test-llm") -> None:
        self._model_name = model_name
        self.last_system: str | None = None
        self.last_user: str | None = None

    @property
    def model_name(self) -> str:
        return self._model_name

    def generate(self, *, system_prompt: str, user_prompt: str) -> str:
        self.last_system = system_prompt
        self.last_user = user_prompt
        if "Purple elephant" in user_prompt:
            return "Answer: Purple elephant (from context)."
        return "Synthetic answer grounded on provided context."


@pytest.fixture
def fake_embeddings():
    return FakeEmbeddingProvider()
