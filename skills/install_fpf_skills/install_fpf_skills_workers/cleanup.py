"""Identify and quarantine leftovers from older FPF installers."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import shutil

from service.scripts.filesystem_policy import (
    clear_directory,
    is_system_temporary_path,
    logical_path_exists,
)


QUARANTINE_DIRECTORY = ".fpf-skills-quarantine"


def _owned_names(catalog: dict[str, object]) -> list[str]:
    values = (
        list(catalog.get("end_user_skills", []))
        + list(catalog.get("retired_end_user_skills", []))
        + list(catalog.get("retired_global_service_skills", []))
    )
    return sorted(set(values))


def _matches(path: Path, catalog: dict[str, object]) -> bool:
    current = set(catalog["end_user_skills"])
    owned = set(_owned_names(catalog))
    exact = (owned - current) | {f"{name}.skill" for name in owned}
    exact.update(str(name) for name in catalog.get("retired_receipts", []))
    exact.update({str(catalog["settings_name"]), ".DS_Store"})
    transient = tuple(
        f".{name}.{kind}-"
        for name in owned | {f"{value}.skill" for value in owned}
        for kind in ("install", "backup")
    )
    generated = (f".{catalog['receipt_name']}.", f".{catalog['settings_name']}.")
    return path.name in exact or path.name.startswith(transient) or path.name.startswith(generated)


def present_leftovers(destination: Path, catalog: dict[str, object]) -> list[Path]:
    if not destination.is_dir():
        return []
    candidates = (path for path in destination.iterdir() if _matches(path, catalog))
    return sorted((path for path in candidates if logical_path_exists(path)), key=lambda path: path.name)


def _quarantine_root(destination: Path) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    parent = destination.parent / QUARANTINE_DIRECTORY
    candidate = parent / timestamp
    suffix = 2
    while candidate.exists():
        candidate = parent / f"{timestamp}-{suffix}"
        suffix += 1
    return candidate


def _move_intact(source: Path, target: Path) -> None:
    if source.is_dir() and not source.is_symlink() and is_system_temporary_path(source):
        shutil.copytree(source, target, symlinks=True)
        clear_directory(source)
        return
    source.rename(target)


def quarantine_leftovers(
    destination: Path, catalog: dict[str, object],
) -> tuple[Path | None, list[Path]]:
    """Move every named legacy candidate intact, without treating its name as ownership proof."""
    leftovers = present_leftovers(destination, catalog)
    if not leftovers:
        return None, []
    quarantine = _quarantine_root(destination)
    quarantine.mkdir(parents=True)
    moved: list[Path] = []
    for source in leftovers:
        target = quarantine / source.name
        _move_intact(source, target)
        moved.append(target)
    return quarantine, moved
