"""Repository-owned maintenance tools with isolated runtime state."""

from __future__ import annotations

import os
import sys
from pathlib import Path


RUNTIME_PYCACHE = Path(__file__).resolve().parents[1] / ".runtime" / "pycache"
os.environ["PYTHONPYCACHEPREFIX"] = str(RUNTIME_PYCACHE)
if sys.pycache_prefix is None:
    sys.pycache_prefix = str(RUNTIME_PYCACHE)
