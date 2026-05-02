from __future__ import annotations

from typing import Optional

from langchain_openai import ChatOpenAI


class OpenAIChatProvider:
    def __init__(
        self,
        *,
        model: str,
        temperature: float = 0.2,
        max_tokens: int = 600,
        api_key: Optional[str] = None,
    ) -> None:
        kwargs: dict = {
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if api_key:
            kwargs["api_key"] = api_key

        self._model = model
        self._client = ChatOpenAI(**kwargs)

    @property
    def model_name(self) -> str:
        return self._model

    def generate(self, *, system_prompt: str, user_prompt: str) -> str:
        msg = self._client.invoke(
            [
                ("system", system_prompt),
                ("human", user_prompt),
            ]
        )
        # LangChain message objects expose `content`
        return str(getattr(msg, "content", msg))

