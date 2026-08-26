"""Validate the single CAPRMEDIO control panel and runtime hygiene."""

from __future__ import annotations

from pathlib import Path

from scripts.init_settings.init_settings import (
    FPF_SOURCE_NAME,
    NPF_SOURCE_NAME,
    read_control_panel,
    read_fpf_original_repo,
)
from scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.source_package import (
    validate_source_package_against_repository,
)


def _require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def _validate_settings_values(values: dict[str, str], errors: list[str]) -> None:
    allowed = dict(
        output_language={"auto", "en", "ru"},
        output_style={"natural", "general", "ste"},
        fpf_terms_explained={"full", "short", "off"},
        save_report={"on", "off"}, report_style={"plain", "caprmedio"},
        install_method={"copy", "symlink"},
    )
    for key, choices in allowed.items():
        _require(values.get(key) in choices, f"invalid control-panel value: {key}", errors)


def _validate_uv_project(root: Path, errors: list[str]) -> None:
    try:
        config = (root / "pyproject.toml").read_text(encoding="utf-8")
        python_version = (root / ".python-version").read_text(encoding="utf-8").strip()
    except OSError as exc:
        errors.append(f"cannot read uv project configuration: {exc}")
        return
    fragments = (
        'name = "levenchuk-fpf-knowledge-graph-toolkit"', 'requires-python = ">=3.12"',
        "dependencies = []", "[tool.uv]", "package = false",
        'cache-dir = ".runtime/uv-cache"',
    )
    for fragment in fragments:
        _require(fragment in config, f"uv project configuration changed: {fragment}", errors)
    _require(python_version == "3.12", "uv Python pin changed", errors)
    _require((root / "uv.lock").is_file(), "missing uv.lock", errors)


def validate_control_panel(root: Path, expected: dict[str, str]) -> list[str]:
    errors: list[str] = []
    example = root / ".caprmedio" / "settings.toml.example"
    _require(example.is_file(), "missing .caprmedio/settings.toml.example", errors)
    try:
        panel, _ = read_control_panel()
        repository, _ = read_fpf_original_repo()
        example_panel, _ = read_control_panel(example, example)
        validate_source_package_against_repository(root, repository)
    except (OSError, ValueError) as exc:
        return errors + [f"cannot read CAPRMEDIO control panel: {exc}"]
    _validate_settings_values(panel["skills"], errors)
    _require(example_panel.get("skills") == expected, "control-panel example defaults changed", errors)
    _require((repository / FPF_SOURCE_NAME).is_file(), "configured original FPF source is missing", errors)
    _require((repository / NPF_SOURCE_NAME).is_file(), "configured original NPF source is missing", errors)
    return errors


def validate_repository_hygiene(root: Path) -> list[str]:
    errors: list[str] = []
    _validate_uv_project(root, errors)
    gitignore = (root / ".gitignore").read_text(encoding="utf-8").splitlines()
    for entry in ("/.venv/", "/.runtime/", "/.caprmedio/settings.toml", "/*-Knowledge-Graph.bak/"):
        _require(entry in gitignore, f"missing gitignore entry: {entry}", errors)
    for retired in (
        "settings.toml", "settings.toml.example", "FPF-Spec.md", "FPF-Spec",
        "Narrativization-and-Narrative-Studies-Principles-Framework.md",
    ):
        _require(not (root / retired).exists(), f"retired root artifact remains: {retired}", errors)
    local_settings = list((root / "skills").rglob("fpf-settings.toml"))
    _require(not local_settings, "skill-local settings files remain", errors)
    return errors
