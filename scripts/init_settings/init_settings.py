#!/usr/bin/env python3
"""Initialize and read the repository's single CAPRMEDIO control panel."""

from __future__ import annotations

import argparse
import shutil
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTROL_ROOT = ROOT / ".caprmedio"
SETTINGS_PATH = CONTROL_ROOT / "settings.toml"
EXAMPLE_PATH = CONTROL_ROOT / "settings.toml.example"
REQUIRED_SECTIONS = {"paths", "skills"}
REQUIRED_PATH_KEYS = {"fpf_original_repo"}
REQUIRED_SKILL_KEYS = {
    "output_language", "output_style", "fpf_terms_explained", "save_report",
    "report_style", "install_method",
}
LEGACY_SKILL_KEYS = REQUIRED_SKILL_KEYS - {"output_language"}
FPF_SOURCE_NAME = "FPF-Spec.md"
NPF_SOURCE_NAME = "Narrativization-and-Narrative-Studies-Principles-Framework.md"


def ensure_settings(settings_path: Path = SETTINGS_PATH, example_path: Path = EXAMPLE_PATH) -> bool:
    """Copy the tracked example when the local settings file is absent."""
    if settings_path.exists():
        if not settings_path.is_file():
            raise ValueError(f"settings path is not a file: {settings_path}")
        return False
    if not example_path.is_file():
        raise ValueError(f"settings example not found: {example_path}")
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(example_path, settings_path)
    return True


def read_control_panel(
    settings_path: Path = SETTINGS_PATH, example_path: Path = EXAMPLE_PATH
) -> tuple[dict[str, dict[str, str]], bool]:
    """Return the one validated repository settings set."""
    created = ensure_settings(settings_path, example_path)
    try:
        with settings_path.open("rb") as handle:
            settings = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ValueError(f"cannot read {settings_path}: {exc}") from exc
    if set(settings) != REQUIRED_SECTIONS:
        raise ValueError("control panel must contain exactly [paths] and [skills]")
    if set(settings["paths"]) != REQUIRED_PATH_KEYS:
        raise ValueError("[paths] must contain exactly fpf_original_repo")
    skill_keys = set(settings["skills"])
    if skill_keys == LEGACY_SKILL_KEYS:
        settings["skills"]["output_language"] = "auto"
    elif skill_keys != REQUIRED_SKILL_KEYS:
        raise ValueError("[skills] must contain exactly the six suite settings")
    return settings, created


def read_fpf_original_repo(
    settings_path: Path = SETTINGS_PATH, example_path: Path = EXAMPLE_PATH
) -> tuple[Path, bool]:
    """Return the configured original FPF repository path."""
    settings, created = read_control_panel(settings_path, example_path)
    configured = settings["paths"]["fpf_original_repo"]
    if not isinstance(configured, str) or not configured.strip():
        raise ValueError("fpf_original_repo must be a non-empty string")
    repository = Path(configured).expanduser()
    if not repository.is_absolute():
        repository = settings_path.parent.parent / repository
    return repository.resolve(), created


def read_skill_settings(
    settings_path: Path = SETTINGS_PATH, example_path: Path = EXAMPLE_PATH
) -> tuple[dict[str, str], bool]:
    settings, created = read_control_panel(settings_path, example_path)
    return settings["skills"], created


def read_fpf_source(
    settings_path: Path = SETTINGS_PATH, example_path: Path = EXAMPLE_PATH
) -> tuple[Path, bool]:
    repository, created = read_fpf_original_repo(settings_path, example_path)
    return repository / FPF_SOURCE_NAME, created


def read_npf_source(
    settings_path: Path = SETTINGS_PATH, example_path: Path = EXAMPLE_PATH
) -> tuple[Path, bool]:
    repository, created = read_fpf_original_repo(settings_path, example_path)
    return repository / NPF_SOURCE_NAME, created


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()
    try:
        repository, created = read_fpf_original_repo()
    except ValueError as exc:
        raise SystemExit(f"ERROR: {exc}") from exc
    action = "created" if created else "kept"
    print(f"{action} control panel {SETTINGS_PATH}")
    print(f"Original FPF repository: {repository}")
    print(f"FPF source: {repository / FPF_SOURCE_NAME}")
    print(f"NPF source: {repository / NPF_SOURCE_NAME}")
    return 0
