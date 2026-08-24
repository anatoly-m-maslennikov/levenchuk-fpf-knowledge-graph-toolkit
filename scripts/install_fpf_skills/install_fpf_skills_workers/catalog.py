"""Load and validate the installable skill catalog."""

from __future__ import annotations

import json
import re
from pathlib import Path


def load_catalog(path: Path) -> dict[str, object]:
    try:
        catalog = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read installer catalog {path}: {exc}") from exc
    skills = catalog.get("end_user_skills")
    if not isinstance(skills, list) or not all(isinstance(name, str) for name in skills):
        raise ValueError("installer catalog end_user_skills must be a string list")
    return catalog


def source_roots(source_skills: Path, names: list[str]) -> dict[str, Path]:
    return {name: source_skills / f"{name}.skill" for name in names}


def target_roots(destination: Path, names: list[str]) -> dict[str, Path]:
    return {name: destination / name for name in names}


def validate_source(source_skills: Path, catalog: dict[str, object]) -> list[str]:
    names = list(catalog["end_user_skills"])
    services = list(catalog.get("project_service_skills", []))
    expected = {f"{name}.skill" for name in names + services}
    actual = {
        path.name for path in source_skills.glob("*.skill")
        if path.is_dir() and (path / "SKILL.md").is_file()
    }
    if actual != expected:
        raise ValueError("repository skill package set does not match the installer catalog")
    for name, package in source_roots(source_skills, names).items():
        try:
            text = (package / "SKILL.md").read_text(encoding="utf-8")
        except OSError as exc:
            raise ValueError(f"cannot read skill package {name}: {exc}") from exc
        if re.search(rf"(?m)^name:\s*{re.escape(name)}\s*$", text) is None:
            raise ValueError(f"package name does not match SKILL.md frontmatter: {name}")
    return names
