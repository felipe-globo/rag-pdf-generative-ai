from __future__ import annotations

import os
from pathlib import Path
from typing import Optional


def load_dotenv_fallback(path: Optional[Path] = None) -> None:
    """
    Minimal .env loader (KEY=VALUE) used when python-dotenv isn't available.

    - Doesn't override already-set environment variables.
    - Ignores blank lines and comments.
    - Strips optional single/double quotes around values.
    """
    env_path = path or Path(".env")
    if not env_path.exists() or not env_path.is_file():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        os.environ.setdefault(key, value)

