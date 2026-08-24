"""Run bounded command-line and installer integration smoke checks."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from scripts.filesystem_policy import temporary_workspace

def _run(root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", *arguments], cwd=root,
        check=False, capture_output=True, text=True,
    )


def validate_help(root: Path) -> list[str]:
    errors: list[str] = []
    builder = _run(root, "scripts.build_fpf_obsidian_graph", "--help")
    if builder.returncode or not all(
        item in builder.stdout for item in ("--source SOURCE", "--source-revision", "--generated-on")
    ):
        errors.append("graph builder help contract failed")
    converter = _run(root, "scripts.graph_fpf_convert_from_original", "--help")
    if converter.returncode or "--check-settings" not in converter.stdout:
        errors.append("FPF converter help contract failed")
    for module in ("scripts.install_fpf_skills.for_codex", "scripts.install_fpf_skills.for_claude"):
        result = _run(root, module, "--help")
        if result.returncode or not all(item in result.stdout for item in ("--apply", "--check", "--destination")):
            errors.append(f"installer help contract failed: {module}")
        if "--method" in result.stdout:
            errors.append(f"installer exposes a second settings authority: {module}")
    return errors


def _check_install(destination: Path, names: list[str], services: list[str]) -> list[str]:
    errors: list[str] = []
    for name in names:
        path = destination / name
        if not path.is_dir() or path.is_symlink():
            errors.append(f"copy install is not a real directory: {name}")
    errors.extend(f"project service skill was installed globally: {name}" for name in services if (destination / name).exists())
    if not (destination / ".fpf-skills-install.json").is_file():
        errors.append("installer receipt is missing")
    if list(destination.rglob("fpf-settings.toml")):
        errors.append("installer created a second settings file")
    return errors


def validate_installer(root: Path, names: list[str], services: list[str]) -> list[str]:
    with temporary_workspace(prefix="fpf-installer-validation-") as temporary:
        destination = Path(temporary) / "skills"
        module = "scripts.install_fpf_skills.for_codex"
        apply = _run(root, module, "--destination", str(destination), "--apply")
        if apply.returncode:
            return [f"copy installer smoke failed: {apply.stderr.strip()}"]
        check = _run(root, module, "--destination", str(destination), "--check")
        errors = [] if check.returncode == 0 else [f"copy installer check failed: {check.stderr.strip()}"]
        return errors + _check_install(destination, names, services)
