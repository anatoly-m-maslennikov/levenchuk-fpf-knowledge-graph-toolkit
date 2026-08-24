"""Load repository validation contracts from JSON."""

import json
from pathlib import Path


def load_contracts(path: Path) -> dict[str, object]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read validation contracts {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("validation contracts must be a JSON object")
    return data
