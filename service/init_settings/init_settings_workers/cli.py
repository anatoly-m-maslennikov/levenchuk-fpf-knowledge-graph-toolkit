"""Command-line adapter for the FPF control panel initializer."""

from __future__ import annotations

import argparse

from .control_panel import FPF_SOURCE_NAME, NPF_SOURCE_NAME, SETTINGS_PATH, read_fpf_original_repo


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
