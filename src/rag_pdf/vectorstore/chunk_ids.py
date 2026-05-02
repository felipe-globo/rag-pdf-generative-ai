from __future__ import annotations

import hashlib

from rag_pdf.ingestion.types import DocumentChunk


def stable_document_id(chunk: DocumentChunk, *, embedding_model: str) -> str:
    """
    Deterministic, stable IDs for vector upserts.

    Why include `embedding_model`?
      - Embedding dimension/type changes when the model changes; keeping separate IDs avoids
        mixing incompatible vectors under the same id.

    Why include chunk text?
      - Same (source/page/chunk_index) can yield different embeddings if OCR/chunking changes.
        Hashing content makes upserts behave like "overwrite when content changes".

    Chroma-compatible id: hexadecimal sha256 is safe (alphanumeric-only).
    """
    source = str(chunk.metadata.get("source", ""))
    page = str(chunk.metadata.get("page", ""))
    chunk_index = str(chunk.metadata.get("chunk_index", ""))

    payload = "|".join([embedding_model, source, page, chunk_index, chunk.text])
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
