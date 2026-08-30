"""Validate generated report provenance and unresolved relations."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import date
from pathlib import Path

from service.scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.models import FPF_PROFILE, GraphProfile
from .source_expectations import catalog_statuses, source_revision


def read_report(graph: Path, report_name: str, errors: list[str]) -> dict[str, object]:
    try:
        return json.loads((graph / "00_Index" / report_name).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read graph validation report: {exc}")
        return {}


def expected_values(
    source: Path, graph: Path, profile: GraphProfile,
    hubs: int, pages: int, markdown_count: int,
) -> dict[str, object]:
    values = dict(
        source=source.name, out_dir=graph.name,
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        source_revision=source_revision(source, profile), hubs=hubs, pages=pages,
        markdown_files=markdown_count,
    )
    if profile != FPF_PROFILE:
        values["framework"] = profile.label
    return values


def validate_report_values(
    report: dict[str, object], expected: dict[str, object], errors: list[str],
) -> None:
    for key, value in expected.items():
        if report.get(key) != value:
            errors.append(
                f"validation report {key} mismatch: expected {value!r}, got {report.get(key)!r}"
            )
    try:
        date.fromisoformat(report.get("generated_on", ""))
    except (TypeError, ValueError):
        errors.append("validation report generated_on is not a valid YYYY-MM-DD date")
    if report.get("broken_links_count") != 0:
        errors.append(f"generated graph has {report.get('broken_links_count')} broken wiki-links")


def _classification(target: str, count: int, status: str | None):
    plural = "s" if count != 1 else ""
    suffix = f"{target} ({count} relation occurrence{plural}"
    if status and status.casefold() != "planned":
        label = "catalog target missing generated pattern body"
        return label, "error", f"{label}: {suffix}; status={status})"
    if status:
        label = "planned catalog target has no generated pattern body"
    elif target.rsplit(".", 1)[-1].isdigit():
        label = "uncataloged numeric relation target has no generated pattern body"
    else:
        label = "non-catalog relation token or legacy alias"
    return label, "warning", f"{label}: {suffix})"


def classify_unresolved(
    report: dict[str, object], source: Path,
    errors: list[str], warnings: list[str],
) -> list[dict[str, object]]:
    count = report.get("unresolved_relations_count")
    sample = report.get("unresolved_relations_sample", [])
    if not isinstance(count, int) or not count:
        return []
    if not isinstance(sample, list) or len(sample) != count:
        errors.append("validation report does not expose every unresolved relation for classification")
        return []
    statuses = catalog_statuses(source)
    targets = Counter(
        item.get("target") for item in sample if isinstance(item, dict) and item.get("target")
    )
    classified: list[dict[str, object]] = []
    for target, occurrences in sorted(targets.items()):
        status = statuses.get(target)
        label, severity, message = _classification(target, occurrences, status)
        (errors if severity == "error" else warnings).append(message)
        classified.append(dict(
            target=target, occurrences=occurrences,
            catalog_status=status, classification=label,
        ))
    return classified
