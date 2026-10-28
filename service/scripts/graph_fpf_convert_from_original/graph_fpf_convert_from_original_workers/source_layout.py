"""Resolve framework publications in legacy and current upstream layouts."""

from pathlib import Path


def resolve_framework_source(directory: Path, filename: str) -> Path:
    relative = Path(filename)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"framework source must be a relative publication path: {filename}")
    candidates = [directory / relative]
    if len(relative.parts) == 1:
        candidates.extend((
            directory / "DPFs" / relative,
            directory / "DPFs" / "Engineering DPF Suite" / relative,
        ))
    return next((path for path in candidates if path.is_file()), candidates[0])
