"""Load the script architecture policy asset."""

import json
from pathlib import Path


def load_policy(path: Path) -> dict[str, object]:
    try:
        policy = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read architecture policy {path}: {exc}") from exc
    if not isinstance(policy, dict):
        raise ValueError("architecture policy must be a JSON object")
    return policy
