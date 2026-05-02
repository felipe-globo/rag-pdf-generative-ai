from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

from rag_pdf.embeddings.protocol import EmbeddingProvider
from rag_pdf.llm.protocol import LLMProvider
from rag_pdf.rag.retriever import RetrievalItem, retrieve


@dataclass(frozen=True)
class Citation:
    source: str
    page: Optional[int]
    chunk_index: Optional[int]
    distance: float
    id: str


@dataclass(frozen=True)
class RAGResponse:
    answer: str
    citations: List[Citation]
    retrieved: List[RetrievalItem]


SYSTEM_PROMPT_TEMPLATE = """\
You are a RAG assistant answering questions using ONLY the provided context.

Rules:
- Use ONLY the context to answer. If the context is insufficient, say you don't have enough information.
- Do not invent facts, numbers, names, or sources.
- Be concise and technical.
- When you use information from a context chunk, cite it inline using: [source: <source>, page: <page>, chunk: <chunk_index>]
  - If page is missing, omit it (still cite source and chunk).
"""


USER_PROMPT_TEMPLATE = """\
## Context
{context}

## Question
{question}

## Instructions
Answer the question using only the context. Include inline citations as specified.
"""


def _format_context(items: List[RetrievalItem]) -> str:
    blocks: List[str] = []
    for i, it in enumerate(items, start=1):
        src = it.metadata.get("source", "")
        page = it.metadata.get("page", None)
        chunk_index = it.metadata.get("chunk_index", None)

        header = f"[{i}] source={src}"
        if page is not None:
            header += f" page={page}"
        if chunk_index is not None:
            header += f" chunk={chunk_index}"
        header += f" distance={it.distance:.6f} id={it.id}"

        blocks.append(header + "\n" + it.text.strip())
    return "\n\n---\n\n".join(blocks)


def _to_citations(items: List[RetrievalItem]) -> List[Citation]:
    out: List[Citation] = []
    for it in items:
        src = str(it.metadata.get("source", ""))
        page_raw = it.metadata.get("page", None)
        chunk_raw = it.metadata.get("chunk_index", None)
        page = int(page_raw) if isinstance(page_raw, (int, float, str)) and str(page_raw).isdigit() else None
        chunk_index = int(chunk_raw) if isinstance(chunk_raw, (int, float, str)) and str(chunk_raw).isdigit() else None
        out.append(
            Citation(
                source=src,
                page=page,
                chunk_index=chunk_index,
                distance=float(it.distance),
                id=str(it.id),
            )
        )
    return out


def answer_question(
    question: str,
    *,
    embeddings: EmbeddingProvider,
    llm: LLMProvider,
    persist_directory: Path,
    collection_name: str,
    k: int = 5,
    where: Optional[Mapping[str, Any]] = None,
    system_prompt: str = SYSTEM_PROMPT_TEMPLATE,
) -> RAGResponse:
    """
    Full RAG step: retrieve context, build prompt, call LLM, return answer + citations.
    """
    retrieved = retrieve(
        question,
        embeddings=embeddings,
        persist_directory=persist_directory,
        collection_name=collection_name,
        k=k,
        where=where,
    )
    context = _format_context(retrieved)
    user_prompt = USER_PROMPT_TEMPLATE.format(context=context, question=question)
    answer = llm.generate(system_prompt=system_prompt, user_prompt=user_prompt)

    return RAGResponse(
        answer=answer,
        citations=_to_citations(retrieved),
        retrieved=retrieved,
    )

