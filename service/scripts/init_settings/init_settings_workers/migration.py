"""Render and archive external versioned FPF control panels without losing history."""

from __future__ import annotations

import json
import os
import tempfile
import tomllib
from pathlib import Path


def read_project_version(project_path: Path) -> str:
    try:
        with project_path.open("rb") as handle:
            project = tomllib.load(handle).get("project")
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ValueError(f"cannot read {project_path}: {exc}") from exc
    version = project.get("version") if isinstance(project, dict) else None
    if not isinstance(version, str) or not version.strip():
        raise ValueError(f"[project].version must be a non-empty string: {project_path}")
    return version


def render_settings(settings: dict[str, dict[str, str]]) -> str:
    order = {
        "package": ("name", "version"),
        "paths": ("fpf_original_repo",),
        "skills": (
            "output_language", "output_style", "fpf_terms_explained",
            "save_report", "report_style", "install_method",
        ),
    }
    groups = []
    for section, keys in order.items():
        lines = [f"[{section}]"]
        lines.extend(
            f"{key} = {json.dumps(settings[section][key], ensure_ascii=False)}" for key in keys
        )
        groups.append("\n".join(lines))
    return "\n\n".join(groups) + "\n"


def next_archive(path: Path, version: str) -> Path:
    safe = "".join(character if character.isalnum() or character in ".-_" else "_" for character in version)
    candidate = path.with_name(f"{path.stem}.{safe}{path.suffix}")
    index = 2
    while candidate.exists():
        candidate = path.with_name(f"{path.stem}.{safe}.{index}{path.suffix}")
        index += 1
    return candidate


def replace_with_versioned_archive(path: Path, text: str, old_version: str) -> Path:
    """Never overwrite a historical settings snapshot."""
    archive = next_archive(path, old_version)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
        os.replace(path, archive)
        try:
            os.replace(temporary, path)
        except OSError:
            os.replace(archive, path)
            raise
    finally:
        if temporary.exists():
            temporary.unlink()
    return archive
