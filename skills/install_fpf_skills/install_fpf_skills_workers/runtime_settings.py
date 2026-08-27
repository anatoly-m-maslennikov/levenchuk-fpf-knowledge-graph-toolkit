"""Render installer-managed machine-local FPF runtime settings."""

from __future__ import annotations

import json
from pathlib import Path


RUNTIME_KEYS = (
    "output_language", "output_style", "fpf_terms_explained",
    "save_report", "report_style",
)


def render_runtime_settings(
    repository_root: Path, settings: dict[str, str], skill_version: str,
) -> str:
    lines = [
        "schema_version = 1",
        f"skill_version = {json.dumps(skill_version, ensure_ascii=False)}",
        f"repository_root = {json.dumps(str(repository_root.resolve()), ensure_ascii=False)}",
        "",
        "[defaults]",
    ]
    lines.extend(
        f"{key} = {json.dumps(settings[key], ensure_ascii=False)}" for key in RUNTIME_KEYS
    )
    return "\n".join(lines) + "\n"


def runtime_settings_current(path: Path, expected: str) -> bool:
    try:
        return path.is_file() and not path.is_symlink() and path.read_text(encoding="utf-8") == expected
    except OSError:
        return False
