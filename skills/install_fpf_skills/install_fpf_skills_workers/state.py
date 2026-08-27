"""Classify existing installer-owned package layouts."""

from __future__ import annotations

import json
from pathlib import Path

from .snapshots import same_link, suite_digest


def load_receipt(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"install receipt is not a real file: {path}")
    try:
        receipt = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read install receipt {path}: {exc}") from exc
    return receipt if isinstance(receipt, dict) else {}


def _symlink_state(targets: dict[str, Path], sources: dict[str, Path]) -> str | None:
    existing = [path for path in targets.values() if path.exists() or path.is_symlink()]
    if not existing:
        return "absent"
    if not all(path.is_symlink() or not (path.exists() or path.is_symlink()) for path in targets.values()):
        return None
    current = sum(same_link(targets[name], sources[name]) for name in targets)
    if current == len(targets):
        return "symlink-current"
    if current == len(existing):
        return "symlink-partial"
    return "symlink-stale"


def classify_install(
    targets: dict[str, Path], sources: dict[str, Path],
    names: list[str], receipt: dict[str, object],
) -> tuple[str, str | None]:
    symlink_state = _symlink_state(targets, sources)
    if symlink_state:
        return symlink_state, None
    existing = [path for path in targets.values() if path.exists() or path.is_symlink()]
    real = {name: path for name, path in targets.items() if path.is_dir() and not path.is_symlink()}
    if len(real) != len(existing) or len(real) != len(targets):
        return "conflict", None
    installed_digest = suite_digest(real, names)
    if installed_digest == suite_digest(sources, names):
        return "copy-current", installed_digest
    if receipt.get("method") == "copy" and receipt.get("source_hash") == installed_digest:
        return "copy-managed-stale", installed_digest
    return "conflict", None


def can_apply(method: str, state: str, receipt: dict[str, object]) -> bool:
    if method == "copy":
        return state in {
            "absent", "copy-current", "copy-managed-stale",
            "symlink-current", "symlink-partial", "symlink-stale",
        }
    if state in {"absent", "symlink-current", "symlink-partial", "symlink-stale"}:
        return True
    return state in {"copy-current", "copy-managed-stale"} and receipt.get("method") == "copy"
