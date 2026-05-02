from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional

import chromadb

from rag_pdf.embeddings.protocol import EmbeddingProvider


@dataclass(frozen=True)
class RetrievalItem:
    text: str
    metadata: Dict[str, Any]
    distance: float
    id: str


def open_chroma_collection(*, persist_directory: Path, collection_name: str):
    """
    Open an existing Chroma persisted collection (or create if missing).
    """
    client = chromadb.PersistentClient(path=str(persist_directory))
    return client.get_or_create_collection(name=collection_name)


def embed_query(question: str, *, embeddings: EmbeddingProvider) -> list[float]:
    """
    Generate a single query embedding using the same provider/model as indexing.
    """
    return embeddings.embed_documents([question])[0]


def retrieve(
    question: str,
    *,
    embeddings: EmbeddingProvider,
    persist_directory: Path,
    collection_name: str,
    k: int = 5,
    where: Optional[Mapping[str, Any]] = None,
) -> List[RetrievalItem]:
    """
    Semantic retrieval over a persisted Chroma collection.

    Args:
        question: user question.
        embeddings: embedding provider used in indexing (same model).
        persist_directory: Chroma persist directory.
        collection_name: Chroma collection name.
        k: number of results.
        where: optional Chroma metadata filter (e.g., {\"source\": \"...\"}).

    Returns:
        List of RetrievalItem with text, metadata, distance, id.
    """
    if k <= 0:
        raise ValueError("k must be > 0")

    collection = open_chroma_collection(persist_directory=persist_directory, collection_name=collection_name)
    q_emb = embed_query(question, embeddings=embeddings)

    query_kwargs: dict = {
        "query_embeddings": [q_emb],
        "n_results": k,
        "include": ["documents", "metadatas", "distances"],
    }
    if where:
        query_kwargs["where"] = dict(where)

    res = collection.query(**query_kwargs)

    documents = (res.get("documents") or [[]])[0]
    metadatas = (res.get("metadatas") or [[]])[0]
    distances = (res.get("distances") or [[]])[0]
    ids = (res.get("ids") or [[]])[0]

    items: List[RetrievalItem] = []
    for doc, meta, dist, _id in zip(documents, metadatas, distances, ids):
        items.append(
            RetrievalItem(
                text=doc or "",
                metadata=dict(meta or {}),
                distance=float(dist),
                id=str(_id),
            )
        )

    return items

