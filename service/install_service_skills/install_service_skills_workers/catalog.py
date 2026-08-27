"""Load and validate the repository-service skill catalog."""

from __future__ import annotations

import json
import re
from pathlib import Path


def load_catalog(path: Path) -> dict[str, object]:
    try:
        catalog = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read service-skill catalog {path}: {exc}") from exc
    names = catalog.get("service_skills")
    if not isinstance(names, list) or not names or not all(isinstance(name, str) for name in names):
        raise ValueError("service_skills must be a non-empty string list")
    if not isinstance(catalog.get("receipt_name"), str) or not catalog["receipt_name"]:
        raise ValueError("receipt_name must be a non-empty string")
    if not isinstance(catalog.get("schema_version"), int):
        raise ValueError("schema_version must be an integer")
    return catalog


def source_roots(root: Path, names: list[str]) -> dict[str, Path]:
    return {name: root / f"{name}.skill" for name in names}


def validate_sources(root: Path, names: list[str]) -> dict[str, Path]:
    expected = {f"{name}.skill" for name in names}
    actual = {
        path.name for path in root.glob("*.skill")
        if path.is_dir() and (path / "SKILL.md").is_file()
    }
    if actual != expected:
        raise ValueError("repository service-skill package set does not match its catalog")
    sources = source_roots(root, names)
    for name, package in sources.items():
        text = (package / "SKILL.md").read_text(encoding="utf-8")
        if re.search(rf"(?m)^name:\s*{re.escape(name)}\s*$", text) is None:
            raise ValueError(f"service package name does not match frontmatter: {name}")
    return sources
