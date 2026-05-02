from __future__ import annotations

from pathlib import Path

from rag_pdf.ingestion.chunking import ChunkingConfig, chunk_documents
from rag_pdf.ingestion.pdf_loader import LoadedDocument
from rag_pdf.ingestion import chunking as chunking_mod
from rag_pdf.rag.chain import answer_question
from rag_pdf.vectorstore import index_document_chunks_chroma

from tests.conftest import FakeEmbeddingProvider, FakeLLMProvider


def test_rag_cli_like_flow_chunk_index_retrieve_answer(tmp_path: Path, monkeypatch) -> None:
    """
    Simulates the full pipeline without filesystem PDFs:
    LoadedDocument → chunk → Chroma persist → retrieval + LLM.
    Uses word-based chunk fallback to avoid tiktoken downloads in CI/offline runs.
    """
    monkeypatch.setattr(chunking_mod, "_try_get_encoding", lambda _n: None)

    docs = [
        LoadedDocument(
            text="The capital of Atlantis is submerged. Atlantis is mythical.",
            source_path=str(tmp_path / "corpus.pdf"),
            page=1,
        )
    ]
    chunks = chunk_documents(
        docs,
        config=ChunkingConfig(chunk_size_tokens=50, chunk_overlap_tokens=10, encoding_name="x"),
    )

    persist = tmp_path / "chroma_integration"
    collection = "integration"
    emb = FakeEmbeddingProvider(dimension=12, model_name="emb-int")
    llm = FakeLLMProvider()

    index_document_chunks_chroma(
        chunks,
        embeddings=emb,
        persist_directory=persist,
        collection_name=collection,
        batch_size=8,
    )

    resp = answer_question(
        "Is Atlantis real?",
        embeddings=emb,
        llm=llm,
        persist_directory=persist,
        collection_name=collection,
        k=4,
    )

    assert resp.retrieved
    assert resp.citations
    assert isinstance(resp.answer, str)
    assert resp.answer.startswith("Synthetic")
    assert "Atlantis" in (llm.last_user or "")
