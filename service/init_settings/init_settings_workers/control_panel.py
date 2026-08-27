"""Read, normalize, and migrate the repository's FPF control panel."""

from __future__ import annotations

import shutil
import tomllib
from pathlib import Path

from .migration import read_project_version, render_settings, replace_with_versioned_archive


ROOT = Path(__file__).resolve().parents[3]
PROJECT_PATH = ROOT / "pyproject.toml"
CONTROL_ROOT = ROOT / ".caprmedio"
SETTINGS_PATH = CONTROL_ROOT / "settings.toml"
EXAMPLE_PATH = CONTROL_ROOT / "settings.toml.example"
PACKAGE_NAME = "fpf"
REQUIRED_SECTIONS = {"package", "paths", "skills"}
LEGACY_SECTIONS = {"paths", "skills"}
REQUIRED_PACKAGE_KEYS = {"name", "version"}
REQUIRED_PATH_KEYS = {"fpf_original_repo"}
REQUIRED_SKILL_KEYS = {
    "output_language", "output_style", "fpf_terms_explained", "save_report",
    "report_style", "install_method",
}
FPF_SOURCE_NAME = "FPF-Spec.md"
NPF_SOURCE_NAME = "Narrativization-and-Narrative-Studies-Principles-Framework.md"


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


def _package_state(package: object, current_version: str) -> tuple[str, bool]:
    if package is None:
        return current_version, True
    if not isinstance(package, dict) or set(package) != REQUIRED_PACKAGE_KEYS:
        raise ValueError("[package] must contain exactly name and version")
    if package.get("name") != PACKAGE_NAME:
        raise ValueError(f"[package].name must be {PACKAGE_NAME}")
    version = package.get("version")
    if not isinstance(version, str) or not version.strip():
        raise ValueError("[package].version must be a non-empty string")
    return version, version != current_version


def _validated_settings(
    settings: dict[str, object], current_version: str,
    defaults: dict[str, object] | None = None,
) -> tuple[dict[str, dict[str, str]], bool, str]:
    if set(settings) not in (REQUIRED_SECTIONS, LEGACY_SECTIONS):
        raise ValueError("control panel must contain [package], [paths], and [skills]")
    old_version, package_migration = _package_state(settings.get("package"), current_version)
    paths, skills = settings.get("paths"), settings.get("skills")
    if not isinstance(paths, dict) or set(paths) != REQUIRED_PATH_KEYS:
        raise ValueError("[paths] must contain exactly fpf_original_repo")
    if not isinstance(skills, dict):
        raise ValueError("[skills] must be a TOML table")
    if set(skills) - REQUIRED_SKILL_KEYS:
        raise ValueError("[skills] must contain only the six suite settings")
    missing = REQUIRED_SKILL_KEYS - set(skills)
    normalized = {
        "package": {"name": PACKAGE_NAME, "version": current_version},
        "paths": dict(paths), "skills": dict(skills),
    }
    default_skills = defaults.get("skills") if isinstance(defaults, dict) else None
    if missing and (not isinstance(default_skills, dict) or not missing.issubset(default_skills)):
        raise ValueError(f"cannot migrate missing [skills] settings: {', '.join(sorted(missing))}")
    for key in missing:
        normalized["skills"][key] = default_skills[key]
    for section in normalized.values():
        if not all(isinstance(value, str) for value in section.values()):
            raise ValueError("control-panel values must be strings")
    return normalized, package_migration or bool(missing), old_version


def migrate_settings(
    settings_path: Path = SETTINGS_PATH, example_path: Path = EXAMPLE_PATH, *,
    apply: bool = False, current_version: str | None = None,
) -> tuple[dict[str, dict[str, str]], bool, bool]:
    version = current_version or read_skill_version()
    created = ensure_settings(settings_path, example_path)
    defaults, example_stale, _ = _validated_settings(_read_toml(example_path), version)
    if example_stale:
        raise ValueError(f"settings example does not declare current skill version {version}")
    settings, migration_needed, old_version = _validated_settings(
        _read_toml(settings_path), version, defaults,
    )
    if migration_needed and apply:
        replace_with_versioned_archive(settings_path, render_settings(settings), old_version)
    return settings, created, migration_needed


def read_control_panel(
    settings_path: Path = SETTINGS_PATH, example_path: Path = EXAMPLE_PATH,
) -> tuple[dict[str, dict[str, str]], bool]:
    settings, created, _ = migrate_settings(settings_path, example_path)
    return settings, created


def read_fpf_original_repo(
    settings_path: Path = SETTINGS_PATH, example_path: Path = EXAMPLE_PATH,
) -> tuple[Path, bool]:
    settings, created = read_control_panel(settings_path, example_path)
    configured = settings["paths"]["fpf_original_repo"]
    if not configured.strip():
        raise ValueError("fpf_original_repo must be a non-empty string")
    repository = Path(configured).expanduser()
    if not repository.is_absolute():
        repository = settings_path.parent.parent / repository
    return repository.resolve(), created


def read_skill_settings(
    settings_path: Path = SETTINGS_PATH, example_path: Path = EXAMPLE_PATH,
) -> tuple[dict[str, str], bool]:
    settings, created = read_control_panel(settings_path, example_path)
    return settings["skills"], created


def read_fpf_source(
    settings_path: Path = SETTINGS_PATH, example_path: Path = EXAMPLE_PATH,
) -> tuple[Path, bool]:
    repository, created = read_fpf_original_repo(settings_path, example_path)
    return repository / FPF_SOURCE_NAME, created


def read_npf_source(
    settings_path: Path = SETTINGS_PATH, example_path: Path = EXAMPLE_PATH,
) -> tuple[Path, bool]:
    repository, created = read_fpf_original_repo(settings_path, example_path)
    return repository / NPF_SOURCE_NAME, created
