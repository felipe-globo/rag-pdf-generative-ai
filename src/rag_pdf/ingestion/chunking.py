from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple

import tiktoken

from .pdf_loader import LoadedDocument
from .types import DocumentChunk


@dataclass(frozen=True)
class ChunkingConfig:
    chunk_size_tokens: int = 500
    chunk_overlap_tokens: int = 50
    encoding_name: str = "cl100k_base"


def _chunk_tokens(tokens: List[int], *, size: int, overlap: int) -> Iterable[List[int]]:
    if size <= 0:
        raise ValueError("chunk_size_tokens must be > 0")
    if overlap < 0:
        raise ValueError("chunk_overlap_tokens must be >= 0")
    if overlap >= size:
        raise ValueError("chunk_overlap_tokens must be < chunk_size_tokens")

    start = 0
    while start < len(tokens):
        end = min(start + size, len(tokens))
        yield tokens[start:end]
        if end == len(tokens):
            break
        start = end - overlap


def _try_get_encoding(name: str) -> Optional[tiktoken.Encoding]:
    try:
        return tiktoken.get_encoding(name)
    except Exception:
        # tiktoken may need to download encoding assets on first use.
        # In restricted/offline environments we gracefully fall back to a
        # whitespace-based approximation (see below).
        return None


def _chunk_words(words: List[str], *, size: int, overlap: int) -> Iterable[Tuple[int, int]]:
    if size <= 0:
        raise ValueError("chunk_size_tokens must be > 0")
    if overlap < 0:
        raise ValueError("chunk_overlap_tokens must be >= 0")
    if overlap >= size:
        raise ValueError("chunk_overlap_tokens must be < chunk_size_tokens")

    start = 0
    while start < len(words):
        end = min(start + size, len(words))
        yield start, end
        if end == len(words):
            break
        start = end - overlap


def chunk_documents(
    docs: Iterable[LoadedDocument],
    *,
    config: ChunkingConfig,
) -> List[DocumentChunk]:
    """
    Token-based chunking suitable for embedding models.
    Each output chunk carries the source metadata (and a chunk index).
    """
    enc = _try_get_encoding(config.encoding_name)
    chunks: List[DocumentChunk] = []

    for doc in docs:
        if enc is not None:
            tokens = enc.encode(doc.text)
            for i, token_slice in enumerate(
                _chunk_tokens(tokens, size=config.chunk_size_tokens, overlap=config.chunk_overlap_tokens)
            ):
                text = enc.decode(token_slice).strip()
                if not text:
                    continue
                md = dict(doc.metadata)
                md["chunk_index"] = i
                md["chunk_size_tokens"] = config.chunk_size_tokens
                md["chunk_overlap_tokens"] = config.chunk_overlap_tokens
                md["token_count"] = len(token_slice)
                md["tokenizer"] = f"tiktoken:{config.encoding_name}"
                chunks.append(DocumentChunk(text=text, metadata=md))
        else:
            # Fallback: approximate "token" counts by words.
            words = doc.text.split()
            for i, (a, b) in enumerate(
                _chunk_words(words, size=config.chunk_size_tokens, overlap=config.chunk_overlap_tokens)
            ):
                text = " ".join(words[a:b]).strip()
                if not text:
                    continue
                md = dict(doc.metadata)
                md["chunk_index"] = i
                md["chunk_size_tokens"] = config.chunk_size_tokens
                md["chunk_overlap_tokens"] = config.chunk_overlap_tokens
                md["token_count"] = b - a
                md["tokenizer"] = "whitespace-approx"
                chunks.append(DocumentChunk(text=text, metadata=md))

    return chunks

