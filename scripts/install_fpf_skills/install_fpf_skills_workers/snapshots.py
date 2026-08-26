"""Hash package trees and compare installer symlinks."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


IGNORED_NAMES = {".DS_Store", ".fpf-runtime.toml", "__pycache__"}


def ignored(path: Path) -> bool:
    return path.name in IGNORED_NAMES or path.suffix in {".pyc", ".pyo"}


def tree_snapshot(root: Path) -> dict[str, str]:
    if not root.is_dir() or root.is_symlink():
        raise ValueError(f"expected a real package directory: {root}")
    snapshot: dict[str, str] = {}
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        relative = path.relative_to(root)
        if any(part in IGNORED_NAMES for part in relative.parts) or ignored(path):
            continue
        if path.is_symlink():
            raise ValueError(f"embedded symlinks are not supported in a copied package: {path}")
        if path.is_file():
            snapshot[relative.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return snapshot


def suite_digest(roots: dict[str, Path], names: list[str]) -> str:
    digest = hashlib.sha256()
    for name in names:
        for relative, file_hash in sorted(tree_snapshot(roots[name]).items()):
            for value in (name, relative, file_hash):
                digest.update(value.encode("utf-8"))
                digest.update(b"\0")
    return digest.hexdigest()


def same_link(target: Path, source: Path) -> bool:
    if not target.is_symlink():
        return False
    try:
        raw_target = Path(os.readlink(target))
        resolved = raw_target if raw_target.is_absolute() else target.parent / raw_target
        return resolved.resolve() == source.resolve()
    except OSError:
        return False
