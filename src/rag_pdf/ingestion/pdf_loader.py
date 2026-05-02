from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional

from pypdf import PdfReader

from .text_cleaning import clean_extracted_text


@dataclass(frozen=True)
class LoadedDocument:
    text: str
    source_path: str
    page: Optional[int] = None

    @property
    def metadata(self) -> dict:
        md = {"source": self.source_path}
        if self.page is not None:
            md["page"] = self.page
        return md


def _iter_pdf_paths(pdf_dir: Path) -> Iterable[Path]:
    if not pdf_dir.exists():
        return []
    if pdf_dir.is_file() and pdf_dir.suffix.lower() == ".pdf":
        return [pdf_dir]
    return sorted(p for p in pdf_dir.rglob("*.pdf") if p.is_file())


def load_pdf(path: Path, *, per_page: bool = True) -> List[LoadedDocument]:
    """
    Load a single PDF and extract text.

    Args:
        path: Path to the PDF.
        per_page: If True, returns one LoadedDocument per page (recommended for traceability).

    Returns:
        List of LoadedDocument with cleaned text and metadata (source, page).
    """
    reader = PdfReader(str(path))
    docs: List[LoadedDocument] = []

    if per_page:
        for idx, page in enumerate(reader.pages, start=1):
            raw = page.extract_text() or ""
            cleaned = clean_extracted_text(raw)
            if cleaned:
                docs.append(LoadedDocument(text=cleaned, source_path=str(path), page=idx))
        return docs

    raw_all = "\n".join((p.extract_text() or "") for p in reader.pages)
    cleaned_all = clean_extracted_text(raw_all)
    if cleaned_all:
        docs.append(LoadedDocument(text=cleaned_all, source_path=str(path), page=None))
    return docs


def load_pdfs_from_dir(pdf_dir: Path) -> List[LoadedDocument]:
    """
    Load all PDFs under a directory (recursively).
    """
    docs: List[LoadedDocument] = []
    for pdf_path in _iter_pdf_paths(pdf_dir):
        docs.extend(load_pdf(pdf_path, per_page=True))
    return docs

