from __future__ import annotations

from typing import Any, Mapping


def normalize_chroma_metadata(metadata: Mapping[str, Any]) -> dict[str, Any]:
    """
    Chroma metadata values must be str, int, float, bool (JSON-serializable primitives).
    """
    out: dict[str, Any] = {}
    for key, val in metadata.items():
        k = str(key)
        if val is None:
            continue
        if isinstance(val, bool):
            out[k] = val
        elif isinstance(val, (int, float, str)):
            out[k] = val
        else:
            out[k] = str(val)
    return out
