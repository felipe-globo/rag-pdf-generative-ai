from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    pdf_dir: Path = Path(os.getenv("PDF_DIR", "data/pdfs"))

    chroma_persist_dir: Path = Path(os.getenv("CHROMA_PERSIST_DIR", "data/chroma"))
    chroma_collection_name: str = os.getenv("CHROMA_COLLECTION_NAME", "rag_pdf")

    embedding_provider: str = os.getenv("EMBEDDING_PROVIDER", "openai")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    embedding_batch_size: int = int(os.getenv("EMBEDDING_BATCH_SIZE", "128"))

    llm_provider: str = os.getenv("LLM_PROVIDER", "openai")
    llm_model: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    llm_temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.2"))
    llm_max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", "600"))

    rag_top_k: int = int(os.getenv("RAG_TOP_K", "5"))

    chunk_size_tokens: int = int(os.getenv("RAG_CHUNK_SIZE", "500"))
    chunk_overlap_tokens: int = int(os.getenv("RAG_CHUNK_OVERLAP", "50"))
    encoding_name: str = os.getenv("RAG_TOKEN_ENCODING", "cl100k_base")


def get_settings() -> Settings:
    return Settings()

