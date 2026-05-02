from __future__ import annotations

from pathlib import Path
from typing import Iterable

import chromadb
from chromadb.api.models.Collection import Collection

from rag_pdf.ingestion.types import DocumentChunk

from rag_pdf.embeddings.protocol import EmbeddingProvider

from .chunk_ids import stable_document_id
from .metadata import normalize_chroma_metadata


def _ensure_persist_directory(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def _get_collection(*, persist_directory: Path, collection_name: str) -> Collection:
    _ensure_persist_directory(persist_directory)
    client = chromadb.PersistentClient(path=str(persist_directory))
    return client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
    )


def index_document_chunks_chroma(
    chunks: Iterable[DocumentChunk],
    *,
    embeddings: EmbeddingProvider,
    persist_directory: Path,
    collection_name: str,
    batch_size: int = 128,
) -> tuple[int, Collection]:
    """
    End-to-end: embed chunks and upsert into a persisted Chroma collection.

    Returns:
      (indexed_count, collection)
    """
    if batch_size <= 0:
        raise ValueError("batch_size must be > 0")

    chunks_list = list(chunks)
    if not chunks_list:
        coll = _get_collection(persist_directory=persist_directory, collection_name=collection_name)
        return 0, coll

    embedding_model = embeddings.model_name
    collection = _get_collection(persist_directory=persist_directory, collection_name=collection_name)

    total = 0

    for i in range(0, len(chunks_list), batch_size):
        batch = chunks_list[i : i + batch_size]

        ids = [stable_document_id(chunk, embedding_model=embedding_model) for chunk in batch]
        texts = [chunk.text for chunk in batch]
        metadatas = []
        for chunk in batch:
            meta = dict(chunk.metadata)
            meta.setdefault("embedding_model", embedding_model)
            metadatas.append(normalize_chroma_metadata(meta))

        embeddings_batch = embeddings.embed_documents(texts)
        collection.upsert(ids=ids, embeddings=embeddings_batch, documents=texts, metadatas=metadatas)
        total += len(batch)

    return total, collection
