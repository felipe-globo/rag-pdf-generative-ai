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
from rag_pdf.ingestion import chunk_documents, load_pdfs_from_dir
from rag_pdf.ingestion.chunking import ChunkingConfig


def main() -> None:
    if load_dotenv is not None:
        load_dotenv()
    settings = get_settings()

    pdf_dir = Path(settings.pdf_dir)
    docs = load_pdfs_from_dir(pdf_dir)
    print(f"Loaded {len(docs)} document pages from {pdf_dir}")

    cfg = ChunkingConfig(
        chunk_size_tokens=settings.chunk_size_tokens,
        chunk_overlap_tokens=settings.chunk_overlap_tokens,
        encoding_name=settings.encoding_name,
    )
    chunks = chunk_documents(docs, config=cfg)
    print(f"Created {len(chunks)} chunks")

    for c in chunks[:3]:
        src = c.metadata.get("source")
        page = c.metadata.get("page")
        tok = c.metadata.get("token_count")
        preview = c.text[:160].replace("\n", " ")
        print(f"- source={src} page={page} tokens={tok} preview={preview!r}")


if __name__ == "__main__":
    main()

