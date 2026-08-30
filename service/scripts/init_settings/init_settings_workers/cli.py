"""Command-line adapter for the FPF control panel initializer."""

from __future__ import annotations

import argparse

from .control_panel import (
    FPF_SOURCE_NAME,
    NPF_SOURCE_NAME,
    SETTINGS_PATH,
    migrate_settings,
    read_fpf_original_repo,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply", action="store_true",
        help="move legacy settings outside the repository and apply version migration",
    )
    args = parser.parse_args()
    try:
        _, created, migration_needed = migrate_settings(apply=args.apply)
        repository, _ = read_fpf_original_repo()
    except ValueError as exc:
        raise SystemExit(f"ERROR: {exc}") from exc
    action = "migrated" if args.apply and migration_needed else "created" if created else "kept"
    print(f"{action} control panel {SETTINGS_PATH}")
    print(f"Original FPF repository: {repository}")
    print(f"FPF source: {repository / FPF_SOURCE_NAME}")
    print(f"NPF source: {repository / NPF_SOURCE_NAME}")
    return 0
