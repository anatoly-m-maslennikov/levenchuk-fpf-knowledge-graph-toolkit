"""Pure manager for portable end-user FPF skill installation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Harness:
    name: str
    environment_variable: str
    default_home_name: str


def run(harness: Harness, arguments: list[str] | None = None) -> int:
    from .install_fpf_skills_workers.cli import run_installer

    return run_installer(harness, arguments)
