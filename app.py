from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:  # pragma: no cover
    load_dotenv = None

from rag_pdf.config import get_settings
from rag_pdf.utils.env import load_dotenv_fallback
from rag_pdf.embeddings import create_embedding_provider
from rag_pdf.ingestion import chunk_documents, load_pdfs_from_dir
from rag_pdf.ingestion.chunking import ChunkingConfig
from rag_pdf.llm import create_llm_provider
from rag_pdf.rag.chain import answer_question
from rag_pdf.vectorstore import index_document_chunks_chroma


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="RAG over local PDFs (Chroma + OpenAI).")

    p.add_argument("--question", "-q", type=str, default=None, help="Question to ask. If omitted, reads from stdin.")
    p.add_argument("--k", type=int, default=None, help="Top-k chunks to retrieve (overrides RAG_TOP_K).")

    p.add_argument("--pdf-dir", type=str, default=None, help="PDF directory (overrides PDF_DIR).")
    p.add_argument("--persist-dir", type=str, default=None, help="Chroma persist directory (overrides CHROMA_PERSIST_DIR).")
    p.add_argument("--collection", type=str, default=None, help="Chroma collection name (overrides CHROMA_COLLECTION_NAME).")

    p.add_argument("--embed-model", type=str, default=None, help="Embedding model (overrides EMBEDDING_MODEL).")
    p.add_argument("--llm-model", type=str, default=None, help="LLM model (overrides LLM_MODEL).")
    p.add_argument("--temperature", type=float, default=None, help="LLM temperature (overrides LLM_TEMPERATURE).")
    p.add_argument("--max-tokens", type=int, default=None, help="LLM max tokens (overrides LLM_MAX_TOKENS).")

    p.add_argument(
        "--index",
        action="store_true",
        help="Index PDFs from --pdf-dir (or PDF_DIR) into Chroma before answering.",
    )
    p.add_argument(
        "--no-answer",
        action="store_true",
        help="Only index (when --index is set), do not call the LLM.",
    )
    return p.parse_args()


def _read_question_fallback(question: Optional[str]) -> str:
    if question and question.strip():
        return question.strip()
    print("Enter your question, then press Ctrl-D (Unix) / Ctrl-Z (Windows):")
    return sys.stdin.read().strip()


def main() -> None:
    if load_dotenv is not None:
        load_dotenv()
    else:
        load_dotenv_fallback(PROJECT_ROOT / ".env")

    args = _parse_args()
    settings = get_settings()

    pdf_dir = Path(args.pdf_dir) if args.pdf_dir else settings.pdf_dir
    persist_dir = Path(args.persist_dir) if args.persist_dir else settings.chroma_persist_dir
    collection_name = args.collection if args.collection else settings.chroma_collection_name

    if args.embed_model:
        # Create a copy-like override without mutating Settings dataclass instance
        settings = type(settings)(
            pdf_dir=settings.pdf_dir,
            chroma_persist_dir=settings.chroma_persist_dir,
            chroma_collection_name=settings.chroma_collection_name,
            embedding_provider=settings.embedding_provider,
            embedding_model=args.embed_model,
            embedding_batch_size=settings.embedding_batch_size,
            llm_provider=settings.llm_provider,
            llm_model=settings.llm_model,
            llm_temperature=settings.llm_temperature,
            llm_max_tokens=settings.llm_max_tokens,
            rag_top_k=settings.rag_top_k,
            chunk_size_tokens=settings.chunk_size_tokens,
            chunk_overlap_tokens=settings.chunk_overlap_tokens,
            encoding_name=settings.encoding_name,
        )

    if args.llm_model or args.temperature is not None or args.max_tokens is not None:
        settings = type(settings)(
            pdf_dir=settings.pdf_dir,
            chroma_persist_dir=settings.chroma_persist_dir,
            chroma_collection_name=settings.chroma_collection_name,
            embedding_provider=settings.embedding_provider,
            embedding_model=settings.embedding_model,
            embedding_batch_size=settings.embedding_batch_size,
            llm_provider=settings.llm_provider,
            llm_model=args.llm_model or settings.llm_model,
            llm_temperature=args.temperature if args.temperature is not None else settings.llm_temperature,
            llm_max_tokens=args.max_tokens if args.max_tokens is not None else settings.llm_max_tokens,
            rag_top_k=settings.rag_top_k,
            chunk_size_tokens=settings.chunk_size_tokens,
            chunk_overlap_tokens=settings.chunk_overlap_tokens,
            encoding_name=settings.encoding_name,
        )

    embedder = create_embedding_provider(settings)

    if args.index:
        docs = load_pdfs_from_dir(pdf_dir)
        chunks = chunk_documents(
            docs,
            config=ChunkingConfig(
                chunk_size_tokens=settings.chunk_size_tokens,
                chunk_overlap_tokens=settings.chunk_overlap_tokens,
                encoding_name=settings.encoding_name,
            ),
        )
        indexed, _ = index_document_chunks_chroma(
            chunks,
            embeddings=embedder,
            persist_directory=persist_dir,
            collection_name=collection_name,
            batch_size=settings.embedding_batch_size,
        )
        print(f"Indexed {indexed} chunks into Chroma.")
        print(f"persist_dir={persist_dir} collection={collection_name}")
        if args.no_answer:
            return

    question = _read_question_fallback(args.question)
    if not question:
        raise SystemExit("Empty question.")

    llm = create_llm_provider(settings)
    k = args.k if args.k is not None else settings.rag_top_k

    resp = answer_question(
        question,
        embeddings=embedder,
        llm=llm,
        persist_directory=persist_dir,
        collection_name=collection_name,
        k=k,
    )

    print(resp.answer)
    print("\n---\nCitations:")
    for c in resp.citations[:k]:
        print(f"- source={c.source} page={c.page} chunk={c.chunk_index} distance={c.distance:.4f} id={c.id}")


if __name__ == "__main__":
    main()

