"""Read, normalize, and migrate the external FPF skill control panel."""

from __future__ import annotations

import shutil
import tomllib
import os
from pathlib import Path

from .location_migration import legacy_files, migrate_legacy_control_panel
from .migration import read_project_version, render_settings, replace_with_versioned_archive
from .schema import ALLOWED_SKILL_VALUES, validated_settings


ROOT = Path(__file__).resolve().parents[4]
PROJECT_PATH = ROOT / "pyproject.toml"
CONTROL_ROOT = Path(
    os.environ.get("FPF_TOOLKIT_CONFIG_DIR", ROOT.parent / f".{ROOT.name}")
).expanduser().resolve()
SETTINGS_PATH = CONTROL_ROOT / "settings.toml"
EXAMPLE_PATH = ROOT / "skills" / "settings.toml.example"
LEGACY_CONTROL_ROOTS = (ROOT / "skills", ROOT / ".caprmedio")
FPF_SOURCE_NAME = "FPF-Spec.md"
NPF_SOURCE_NAME = "Narrativization-and-Narrative-Studies-Principles-Framework.md"


def settings_paths_for_root(root: Path) -> tuple[Path, Path]:
    """Return root-specific external settings and tracked defaults paths."""
    resolved = root.resolve()
    if resolved == ROOT.resolve():
        return SETTINGS_PATH, EXAMPLE_PATH
    return (
        resolved.parent / f".{resolved.name}" / "settings.toml",
        resolved / "skills" / "settings.toml.example",
    )


def ensure_settings(settings_path: Path = SETTINGS_PATH, example_path: Path = EXAMPLE_PATH) -> bool:
    if settings_path.exists():
        if not settings_path.is_file():
            raise ValueError(f"settings path is not a file: {settings_path}")
        return False
    if not example_path.is_file():
        raise ValueError(f"settings example not found: {example_path}")
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(example_path, settings_path)
    return True


def _read_toml(path: Path) -> dict[str, object]:
    try:
        with path.open("rb") as handle:
            value = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ValueError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"control panel must be a TOML table: {path}")
    return value


def read_skill_version(project_path: Path = PROJECT_PATH) -> str:
    return read_project_version(project_path)


def _apply_skill_overrides(
    settings: dict[str, dict[str, str]], overrides: dict[str, str],
    defaults: dict[str, object], version: str,
) -> tuple[dict[str, dict[str, str]], bool]:
    unknown = set(overrides) - set(ALLOWED_SKILL_VALUES)
    if unknown:
        raise ValueError(f"cannot override unknown [skills] settings: {', '.join(sorted(unknown))}")
    previous = dict(settings["skills"])
    merged = {
        "package": dict(settings["package"]), "paths": dict(settings["paths"]),
        "skills": {**settings["skills"], **overrides},
    }
    normalized, _, _ = validated_settings(merged, version, defaults)
    return normalized, any(previous[key] != value for key, value in overrides.items())


def _effective_settings(
    settings_path: Path, example_path: Path, version: str, apply: bool,
    create_if_missing: bool,
) -> tuple[Path, bool, bool, bool]:
    default_paths = settings_path == SETTINGS_PATH and example_path == EXAMPLE_PATH
    legacy_pending = default_paths and any(legacy_files(root) for root in LEGACY_CONTROL_ROOTS)
    if legacy_pending and apply:
        for legacy_root in LEGACY_CONTROL_ROOTS:
            migrate_legacy_control_panel(legacy_root, SETTINGS_PATH, version)
    effective = settings_path
    if legacy_pending and not settings_path.is_file():
        effective = next(
            root / "settings.toml" for root in LEGACY_CONTROL_ROOTS
            if (root / "settings.toml").is_file()
        )
    settings_pending = effective == settings_path and not settings_path.is_file()
    if settings_pending and not create_if_missing:
        return example_path, False, legacy_pending, settings_pending
    created = False if effective != settings_path else ensure_settings(settings_path, example_path)
    return effective, created, legacy_pending, settings_pending


def migrate_settings(
    settings_path: Path = SETTINGS_PATH, example_path: Path = EXAMPLE_PATH, *,
    apply: bool = False, current_version: str | None = None,
    create_if_missing: bool = True,
    skill_overrides: dict[str, str] | None = None,
) -> tuple[dict[str, dict[str, str]], bool, bool]:
    version = current_version or read_skill_version()
    effective_path, created, legacy_pending, settings_pending = _effective_settings(
        settings_path, example_path, version, apply, create_if_missing,
    )
    defaults, example_stale, _ = validated_settings(_read_toml(example_path), version)
    if example_stale:
        raise ValueError(f"settings example does not declare current skill version {version}")
    settings, migration_needed, old_version = validated_settings(
        _read_toml(effective_path), version, defaults,
    )
    if skill_overrides:
        settings, overrides_changed = _apply_skill_overrides(
            settings, skill_overrides, defaults, version,
        )
        migration_needed = migration_needed or overrides_changed
    if migration_needed and apply:
        replace_with_versioned_archive(settings_path, render_settings(settings), old_version)
    pending = (legacy_pending and not apply) or (settings_pending and not create_if_missing)
    return settings, created, migration_needed or pending


def read_control_panel(
    settings_path: Path = SETTINGS_PATH, example_path: Path = EXAMPLE_PATH,
    *, create_if_missing: bool = True,
) -> tuple[dict[str, dict[str, str]], bool]:
    settings, created, _ = migrate_settings(
        settings_path, example_path, create_if_missing=create_if_missing,
    )
    return settings, created


def read_fpf_original_repo(
    settings_path: Path = SETTINGS_PATH, example_path: Path = EXAMPLE_PATH,
    *, create_if_missing: bool = True,
) -> tuple[Path, bool]:
    settings, created = read_control_panel(
        settings_path, example_path, create_if_missing=create_if_missing,
    )
    configured = settings["paths"]["fpf_original_repo"]
    if not configured.strip():
        raise ValueError("fpf_original_repo must be a non-empty string")
    repository = Path(configured).expanduser()
    if not repository.is_absolute():
        base = ROOT if settings_path == SETTINGS_PATH else settings_path.parent.parent
        repository = base / repository
    return repository.resolve(), created


def read_skill_settings(
    settings_path: Path = SETTINGS_PATH, example_path: Path = EXAMPLE_PATH,
    *, create_if_missing: bool = True,
) -> tuple[dict[str, str], bool]:
    settings, created = read_control_panel(
        settings_path, example_path, create_if_missing=create_if_missing,
    )
    return settings["skills"], created


def read_fpf_source(
    settings_path: Path = SETTINGS_PATH, example_path: Path = EXAMPLE_PATH,
    *, create_if_missing: bool = True,
) -> tuple[Path, bool]:
    repository, created = read_fpf_original_repo(
        settings_path, example_path, create_if_missing=create_if_missing,
    )
    return repository / FPF_SOURCE_NAME, created


def read_npf_source(
    settings_path: Path = SETTINGS_PATH, example_path: Path = EXAMPLE_PATH,
    *, create_if_missing: bool = True,
) -> tuple[Path, bool]:
    repository, created = read_fpf_original_repo(
        settings_path, example_path, create_if_missing=create_if_missing,
    )
    return repository / NPF_SOURCE_NAME, created
