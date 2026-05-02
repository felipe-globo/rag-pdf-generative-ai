from __future__ import annotations

from typing import Optional, Sequence

from langchain_openai import OpenAIEmbeddings


class OpenAIEmbeddingProvider:
    """
    OpenAI embeddings via LangChain (easy to tune/replace implementation details later).
    """

    def __init__(self, *, model: str, api_key: Optional[str] = None) -> None:
        kwargs: dict = {"model": model}
        if api_key:
            kwargs["api_key"] = api_key

        self._model = model
        self._client = OpenAIEmbeddings(**kwargs)

    @property
    def model_name(self) -> str:
        return self._model

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        return self._client.embed_documents(list(texts))
