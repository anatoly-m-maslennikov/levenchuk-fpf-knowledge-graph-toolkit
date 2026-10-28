"""Bind exactly the graph projections covered by conversion acceptance."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from service.scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.models import (
    CAD_PROFILE, FPF_PROFILE, NPF_PROFILE, GraphProfile,
)


PROJECTION_PROFILES = (FPF_PROFILE, NPF_PROFILE, CAD_PROFILE)


def tree_sha256(root: Path) -> str:
    if root.is_symlink() or not root.is_dir():
        raise ValueError(f"accepted graph must be a real directory: {root}")
    digest = hashlib.sha256()
    entries = sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix())
    for path in entries:
        if path.is_symlink():
            raise ValueError(f"accepted graph contains a symlink: {path}")
        if not path.is_file() or path.name == ".DS_Store":
            continue
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(relative + b"\0" + path.read_bytes() + b"\0")
    return digest.hexdigest()


def _report_revision(path: Path, label: str) -> object:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value.get("source_revision")


def _projection(root: Path, profile: GraphProfile) -> dict[str, object]:
    current = root / profile.default_output
    backup = root / f"{profile.default_output}.bak"
    report = Path("00_Index") / f"{profile.label} - Validation Report.json"
    current_digest = tree_sha256(current)
    initial = profile == CAD_PROFILE and not backup.exists() and not backup.is_symlink()
    backup_digest = None if initial else tree_sha256(backup)
    return {
        "current_path": profile.default_output,
        "backup_path": f"{profile.default_output}.bak",
        "current_revision": _report_revision(current / report, f"current {profile.label} graph report"),
        "backup_revision": None if initial else _report_revision(backup / report, f"backup {profile.label} graph report"),
        "current_tree_sha256": current_digest,
        "backup_tree_sha256": backup_digest,
    }


def projection_manifest(root: Path) -> dict[str, object]:
    result: dict[str, object] = {}
    for profile in PROJECTION_PROFILES:
        current = root / profile.default_output
        backup = root / f"{profile.default_output}.bak"
        if profile == CAD_PROFILE and not any(
            path.exists() or path.is_symlink() for path in (current, backup)
        ):
            continue
        result[profile.key] = _projection(root, profile)
    return result
