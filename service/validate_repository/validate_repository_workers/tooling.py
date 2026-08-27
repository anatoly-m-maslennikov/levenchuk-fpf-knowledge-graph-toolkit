"""Validate tool locations and manager naming."""

from pathlib import Path


def validate_tooling(root: Path, required_files: list[str]) -> list[str]:
    errors = [f"missing tooling file: {relative}" for relative in required_files if not (root / relative).is_file()]
    legacy = sorted(path.relative_to(root).as_posix() for path in (root / "service").rglob("tool.py"))
    if legacy:
        errors.append(f"legacy tool.py managers remain: {legacy}")
    return errors
