from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:  # pragma: no cover
    load_dotenv = None

from rag_pdf.config import get_settings
from rag_pdf.embeddings import create_embedding_provider
from rag_pdf.ingestion import chunk_documents, load_pdfs_from_dir
from rag_pdf.ingestion.chunking import ChunkingConfig
from rag_pdf.vectorstore import index_document_chunks_chroma


def main() -> None:
    if load_dotenv is not None:
        load_dotenv()

    settings = get_settings()

    pdf_dir = Path(settings.pdf_dir)
    docs = load_pdfs_from_dir(pdf_dir)

    chunks = chunk_documents(
        docs,
        config=ChunkingConfig(
            chunk_size_tokens=settings.chunk_size_tokens,
            chunk_overlap_tokens=settings.chunk_overlap_tokens,
            encoding_name=settings.encoding_name,
        ),
    )

    embedder = create_embedding_provider(settings)
    count, _ = index_document_chunks_chroma(
        chunks,
        embeddings=embedder,
        persist_directory=settings.chroma_persist_dir,
        collection_name=settings.chroma_collection_name,
        batch_size=settings.embedding_batch_size,
    )

    print(f"chunks={len(chunks)} indexed={count} chroma_collection={settings.chroma_collection_name}")
    print(f"persist_directory={settings.chroma_persist_dir}")


if __name__ == "__main__":
    main()
