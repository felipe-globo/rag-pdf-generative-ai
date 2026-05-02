from __future__ import annotations

import re


_WHITESPACE_RE = re.compile(r"\s+")
_HYPHEN_LINEBREAK_RE = re.compile(r"(\w)-\s*\n\s*(\w)")


def clean_extracted_text(text: str) -> str:
    """
    Basic cleanup for PDF-extracted text:
    - joins hyphenated line breaks (e.g., 'infor-\\nmação' -> 'informação')
    - normalizes whitespace
    """
    if not text:
        return ""

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = _HYPHEN_LINEBREAK_RE.sub(r"\1\2", text)
    text = _WHITESPACE_RE.sub(" ", text).strip()
    return text

