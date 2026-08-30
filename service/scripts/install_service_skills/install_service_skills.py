"""Pure manager for project-local repository-service skill installation."""

from __future__ import annotations


def run(arguments: list[str] | None = None) -> int:
    from .install_service_skills_workers.cli import run_installer

    return run_installer(arguments)
