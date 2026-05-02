from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from rag_pdf.ingestion.chunking import ChunkingConfig, chunk_documents
from rag_pdf.ingestion import chunking as chunking_mod
from rag_pdf.ingestion.pdf_loader import LoadedDocument, load_pdf
from rag_pdf.ingestion.text_cleaning import clean_extracted_text


def test_clean_extracted_text_joins_hyphen_linebreak() -> None:
    raw = "exem-\nplo de texto\n\ncom espaços "
    assert clean_extracted_text(raw) == "exemplo de texto com espaços"


def test_chunk_documents_rejects_negative_overlap(monkeypatch) -> None:
    with pytest.raises(ValueError, match="chunk_overlap"):
        monkeypatch.setattr(chunking_mod, "_try_get_encoding", lambda _n: None)
        docs = [LoadedDocument(text="a " * 200, source_path="/x.pdf", page=1)]
        chunk_documents(
            docs,
            config=ChunkingConfig(chunk_size_tokens=10, chunk_overlap_tokens=-1, encoding_name="x"),
        )


def test_chunk_documents_word_fallback_splits(monkeypatch) -> None:
    monkeypatch.setattr(chunking_mod, "_try_get_encoding", lambda _n: None)
    text = " ".join([f"w{i}" for i in range(40)])
    docs = [LoadedDocument(text=text, source_path="/doc.pdf", page=1)]

    chunks = chunk_documents(
        docs,
        config=ChunkingConfig(chunk_size_tokens=10, chunk_overlap_tokens=2, encoding_name="unavailable"),
    )
    assert len(chunks) >= 2
    assert all(c.metadata.get("source") == "/doc.pdf" for c in chunks)
    assert all("tokenizer" in c.metadata for c in chunks)


@patch("rag_pdf.ingestion.pdf_loader.PdfReader")
def test_load_pdf_per_page_collects_nonempty_pages(mock_reader_cls) -> None:
    page1 = MagicMock()
    page1.extract_text.return_value = "Primeira linha,\n segundo."
    page2 = MagicMock()
    page2.extract_text.return_value = ""
    reader = MagicMock()
    reader.pages = [page1, page2]
    mock_reader_cls.return_value = reader

    docs = load_pdf(Path("dummy.pdf"), per_page=True)
    assert len(docs) == 1
    assert docs[0].page == 1
    assert "Primeira linha" in docs[0].text
