"""Repository-service tooling and skill sources."""

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.pycache_prefix = str(ROOT / ".runtime" / "pycache")
cached = globals().get("__cached__")
if cached and ".runtime" not in Path(cached).parts:
    try:
        Path(cached).unlink(missing_ok=True)
    except OSError:
        pass
