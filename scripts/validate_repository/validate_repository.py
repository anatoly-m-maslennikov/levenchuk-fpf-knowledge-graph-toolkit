"""Pure manager for repository integration validation."""

from pathlib import Path

from .validate_repository_workers.validation import validate_repository_state


ROOT = Path(__file__).resolve().parents[2]


def validate_repository(root: Path = ROOT) -> dict[str, object]:
    return validate_repository_state(root)
