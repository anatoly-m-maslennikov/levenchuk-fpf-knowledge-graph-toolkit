"""Pure manager for the repository's versioned FPF control panel."""

from __future__ import annotations

from .init_settings_workers.control_panel import (
    CONTROL_ROOT,
    EXAMPLE_PATH,
    FPF_SOURCE_NAME,
    NPF_SOURCE_NAME,
    PROJECT_PATH,
    ROOT,
    SETTINGS_PATH,
    ensure_settings,
    migrate_settings,
    read_control_panel,
    read_fpf_original_repo,
    read_fpf_source,
    read_npf_source,
    read_skill_settings,
    read_skill_version,
)


def main() -> int:
    from .init_settings_workers.cli import main as run

    return run()
