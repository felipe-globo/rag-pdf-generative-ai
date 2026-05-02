from __future__ import annotations

from pathlib import Path

import pytest

from rag_pdf.ingestion.types import DocumentChunk
from rag_pdf.rag.retriever import retrieve
from rag_pdf.vectorstore import index_document_chunks_chroma
from rag_pdf.vectorstore.chunk_ids import stable_document_id

from tests.conftest import FakeEmbeddingProvider


def test_stable_document_id_is_deterministic() -> None:
    chunk = DocumentChunk(
        "same text",
        {"source": "/a.pdf", "page": 2, "chunk_index": 0},
    )
    a = stable_document_id(chunk, embedding_model="emb-a")
    b = stable_document_id(chunk, embedding_model="emb-a")
    assert a == b
    assert len(a) == 64


def test_stable_document_id_changes_with_model_or_text() -> None:
    c1 = DocumentChunk("t1", {"source": "s", "page": 1, "chunk_index": 0})
    c2 = DocumentChunk("t2", {"source": "s", "page": 1, "chunk_index": 0})
    assert stable_document_id(c1, embedding_model="m") != stable_document_id(c2, embedding_model="m")
    assert stable_document_id(c1, embedding_model="m1") != stable_document_id(c1, embedding_model="m2")


def test_retrieve_rejects_non_positive_k(tmp_path: Path, fake_embeddings: FakeEmbeddingProvider) -> None:
    with pytest.raises(ValueError, match="k"):
        retrieve(
            "q",
            embeddings=fake_embeddings,
            persist_directory=tmp_path,
            collection_name="c",
            k=0,
        )


def test_index_and_retrieve_returns_ranked_documents(tmp_path: Path) -> None:
    emb = FakeEmbeddingProvider(dimension=8, model_name="test-model")
    persist = tmp_path / "chroma"
    coll = "rag_test_coll"

    chunks = [
        DocumentChunk("Purple elephant habitats are imaginary.", {"source": "doc.pdf", "page": 1, "chunk_index": 0}),
        DocumentChunk("Unrelated content about spoons.", {"source": "doc.pdf", "page": 2, "chunk_index": 0}),
    ]
    count, _ = index_document_chunks_chroma(
        chunks,
        embeddings=emb,
        persist_directory=persist,
        collection_name=coll,
        batch_size=2,
    )
    assert count == 2

    results = retrieve(
        "What color is the elephant?",
        embeddings=emb,
        persist_directory=persist,
        collection_name=coll,
        k=2,
    )
    assert len(results) == 2
    assert results[0].distance <= results[1].distance
    assert isinstance(results[0].distance, float)
