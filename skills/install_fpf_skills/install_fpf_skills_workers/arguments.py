"""Parse the end-user skill installer's public command line."""

from __future__ import annotations

import argparse
from pathlib import Path

from ..install_fpf_skills import Harness


def arguments(harness: Harness, values: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=f"Install end-user FPF skills for {harness.name}.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="install or update packages")
    mode.add_argument("--check", action="store_true", help="verify without writing")
    parser.add_argument(
        "--overwrite", action="store_true",
        help=(
            "replace matching external preferences from a legacy root .fpf-runtime.toml; "
            "the previous external settings remain archived"
        ),
    )
    parser.add_argument("--destination", type=Path, help="exact harness skills directory")
    return parser.parse_args(values)
