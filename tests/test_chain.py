from __future__ import annotations

from pathlib import Path

from rag_pdf.ingestion.types import DocumentChunk
from rag_pdf.rag.chain import answer_question
from rag_pdf.vectorstore import index_document_chunks_chroma

from tests.conftest import FakeEmbeddingProvider, FakeLLMProvider


def test_answer_question_invokes_llm_with_context_and_question(tmp_path: Path) -> None:
    persist = tmp_path / "chroma_chain"
    collection = "chain_coll"
    emb = FakeEmbeddingProvider(dimension=8, model_name="emb-chain")
    llm = FakeLLMProvider(model_name="llm-chain")

    chunks = [
        DocumentChunk("Purple elephant on page one.", {"source": "manual.pdf", "page": 1, "chunk_index": 0}),
    ]
    index_document_chunks_chroma(
        chunks,
        embeddings=emb,
        persist_directory=persist,
        collection_name=collection,
        batch_size=4,
    )

    resp = answer_question(
        "What animal is purple?",
        embeddings=emb,
        llm=llm,
        persist_directory=persist,
        collection_name=collection,
        k=2,
    )

    assert "Purple elephant" in (llm.last_user or "")
    assert "What animal is purple?" in (llm.last_user or "")
    assert "Answer: Purple elephant" in resp.answer
    assert resp.citations[0].source == "manual.pdf"
    assert len(resp.retrieved) == 1
