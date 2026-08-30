"""Move repository-contained control panels into external configuration."""

from __future__ import annotations

import shutil
import tomllib
from pathlib import Path

from .migration import next_archive


def legacy_files(legacy_root: Path) -> list[Path]:
    if not legacy_root.is_dir():
        return []
    current = legacy_root / "settings.toml"
    snapshots = sorted(legacy_root.glob("settings.*.toml"))
    return ([current] if current.is_file() else []) + snapshots


def _declared_version(path: Path, fallback: str) -> str:
    try:
        with path.open("rb") as handle:
            package = tomllib.load(handle).get("package")
    except (OSError, tomllib.TOMLDecodeError):
        return fallback
    version = package.get("version") if isinstance(package, dict) else None
    return version if isinstance(version, str) and version.strip() else fallback


def migrate_legacy_control_panel(
    legacy_root: Path, settings_path: Path, fallback_version: str,
) -> bool:
    """Move one former in-repository control panel without losing history."""
    sources = legacy_files(legacy_root)
    if not sources:
        return False
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    current = legacy_root / "settings.toml"
    if current in sources:
        destination = settings_path
        if settings_path.exists():
            destination = next_archive(
                settings_path, _declared_version(current, fallback_version),
            )
        shutil.move(str(current), str(destination))
    for source in sources:
        if source != current:
            version = source.name.removeprefix("settings.").removesuffix(".toml")
            shutil.move(str(source), str(next_archive(settings_path, version)))
    try:
        legacy_root.rmdir()
    except OSError:
        pass
    return True
