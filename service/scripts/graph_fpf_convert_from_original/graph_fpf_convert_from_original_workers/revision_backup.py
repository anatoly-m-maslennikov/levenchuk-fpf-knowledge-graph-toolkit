"""Keep the original predecessor while repairing one source revision."""

import json
from pathlib import Path


def revision_backup(graph: Path, backup: Path, temporary: Path, label: str, revision: str) -> Path:
    report = graph / "00_Index" / f"{label} - Validation Report.json"
    try:
        current = json.loads(report.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return backup
    if isinstance(current, dict) and current.get("source_revision") == revision:
        return temporary / "same-revision-predecessor"
    return backup
