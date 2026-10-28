"""Canonical nested CAD source fixtures."""

import subprocess
from pathlib import Path


SOURCE_NAME = "CONTROL-ARCHITECTURE-DESIGN-PRINCIPLES-FRAMEWORK.md"
SOURCE_RELATIVE = "DPFs/Engineering DPF Suite/" + SOURCE_NAME
SOURCE = (
    "# Control Architecture Design Principles Framework\n\n"
    "# Architectural Reference\n\n"
    "## CAD.Reference:1 - Purpose\n\nCAD.1 explains the design.\n\n"
    "## CAD.Reference:2 - Objects\n\nCAD.2 follows.\n\n"
    "# A. Design a planning-and-feedback architecture\n\n"
    "## CAD.1 - Decomposition\n\n> **Status:** Stable\n\n"
    "### Relations\n\n- Builds on: CAD.2\n\n"
    "## CAD.2 - Interface\n\n> **Status:** Stable\n\n"
    "### CAD.2:4 - Solution\n\nPreserve the exchange.\n"
)


def run(*arguments: str, cwd: Path) -> str:
    return subprocess.run(
        arguments, cwd=cwd, check=True, capture_output=True, text=True,
    ).stdout.strip()


def make_source(root: Path) -> Path:
    root.mkdir()
    run("git", "init", "-q", cwd=root)
    run("git", "remote", "add", "origin", "https://github.com/ailev/FPF.git", cwd=root)
    source = root / SOURCE_RELATIVE
    source.parent.mkdir(parents=True)
    source.write_text(SOURCE, encoding="utf-8")
    run("git", "add", SOURCE_RELATIVE, cwd=root)
    run(
        "git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
        "commit", "-qm", "source", cwd=root,
    )
    return source
