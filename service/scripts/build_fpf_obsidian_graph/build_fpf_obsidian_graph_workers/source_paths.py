"""Bind links to other tracked source publications to their upstream snapshot."""

from __future__ import annotations

import json
import posixpath
from pathlib import Path
import re
import subprocess
from urllib.parse import quote, unquote, urlsplit

from service.scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.source_repository import _canonical_remote


INLINE_LINK_RE = re.compile(r"(?<!!)(\[(?:\\.|[^\]\\])*\])\(([^\s)]+)\)")


def source_inventory(source: Path) -> tuple[Path, str, list[str]] | None:
    for root in source.parents:
        metadata = root / "source-metadata.json"
        if metadata.is_file():
            value = json.loads(metadata.read_text(encoding="utf-8"))
            if value.get("upstream_repository") != "ailev/FPF":
                return None
            return root, value["upstream_revision"], [item["path"] for item in value["tracked_files"]]
        if (root / ".git").exists():
            return git_source_inventory(root)
    return None


def git_source_inventory(root: Path) -> tuple[Path, str, list[str]] | None:
    def git(*args: str) -> str:
        result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else ""
    try:
        _canonical_remote(root)
    except ValueError:
        return None
    return root, git("rev-parse", "HEAD"), git("ls-files", "-z").split("\0")


def source_file_targets(source: Path) -> dict[str, str]:
    inventory = source_inventory(source)
    if inventory is None:
        return {}
    root, revision, tracked = inventory
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        return {}
    source_parent = source.parent.resolve().relative_to(root.resolve()).as_posix()
    targets = {}
    for relative in tracked:
        path = root / relative
        if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            continue
        destination = posixpath.relpath(relative, source_parent)
        targets[destination] = f"https://github.com/ailev/FPF/blob/{revision}/{quote(relative, safe='/')}"
    return targets


def rewrite_source_file_links(line: str, targets: dict[str, str]) -> str:
    def replace(match: re.Match[str]) -> str:
        destination = match[2].strip("<>")
        parts = urlsplit(destination)
        if parts.scheme or parts.netloc or not parts.path or parts.path.startswith("/"):
            return match[0]
        target = targets.get(posixpath.normpath(unquote(parts.path)))
        if target is None:
            return match[0]
        target += ("?" + parts.query if parts.query else "") + ("#" + parts.fragment if parts.fragment else "")
        return f"{match[1]}({target})"
    pieces = re.split(r"(`+[^`]*`+)", line)
    return "".join(piece if piece.startswith("`") else INLINE_LINK_RE.sub(replace, piece) for piece in pieces)
