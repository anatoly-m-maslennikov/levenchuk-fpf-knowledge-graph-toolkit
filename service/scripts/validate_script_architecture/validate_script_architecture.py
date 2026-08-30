"""Pure manager for the repository script architecture gate."""

from pathlib import Path

from .validate_script_architecture_workers.validation import validate_architecture


ROOT = Path(__file__).resolve().parents[3]


def validate_script_architecture(root: Path = ROOT) -> dict[str, object]:
    return validate_architecture(root)
