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
from rag_pdf.llm import create_llm_provider
from rag_pdf.rag.chain import answer_question


def main() -> None:
    if load_dotenv is not None:
        load_dotenv()

    settings = get_settings()
    embedder = create_embedding_provider(settings)
    llm = create_llm_provider(settings)

    question = "Resuma os pontos principais do documento e cite as fontes."
    resp = answer_question(
        question,
        embeddings=embedder,
        llm=llm,
        persist_directory=settings.chroma_persist_dir,
        collection_name=settings.chroma_collection_name,
        k=settings.rag_top_k,
    )

    print(resp.answer)
    print("\n---\nCitations:")
    for c in resp.citations[: settings.rag_top_k]:
        print(f"- source={c.source} page={c.page} chunk={c.chunk_index} distance={c.distance:.4f} id={c.id}")


if __name__ == "__main__":
    main()

