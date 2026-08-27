"""Identify and remove only repo-owned leftovers from older FPF installers."""

from __future__ import annotations

from pathlib import Path

from service.filesystem_policy import logical_path_exists
from .filesystem import remove_path


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


def remove_leftovers(destination: Path, catalog: dict[str, object]) -> None:
    for path in present_leftovers(destination, catalog):
        remove_path(path)
