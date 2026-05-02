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
from rag_pdf.rag.retriever import retrieve


def main() -> None:
    if load_dotenv is not None:
        load_dotenv()

    settings = get_settings()
    embedder = create_embedding_provider(settings)

    question = "Qual é o tema principal dos documentos?"
    results = retrieve(
        question,
        embeddings=embedder,
        persist_directory=settings.chroma_persist_dir,
        collection_name=settings.chroma_collection_name,
        k=5,
        where=None,
    )

    for i, r in enumerate(results, start=1):
        src = r.metadata.get("source")
        page = r.metadata.get("page")
        preview = r.text[:200].replace("\n", " ")
        print(f"{i}. distance={r.distance:.4f} source={src} page={page} id={r.id}")
        print(f"   {preview}\n")


if __name__ == "__main__":
    main()

