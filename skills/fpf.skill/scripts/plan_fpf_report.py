#!/usr/bin/env python3
"""Plan plain or CAPRMEDIO FPF report delivery without writing the report."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path


TIMESTAMP_RE = re.compile(r"^\d{8}T\d{6}Z$")


def _slug(task: str) -> str:
    ascii_text = unicodedata.normalize("NFKD", task).encode("ascii", "ignore").decode()
    value = re.sub(r"[^a-z0-9]+", "-", ascii_text.casefold()).strip("-")
    return "-".join(value.split("-")[:10]) or "analysis"


def plain_report_path(workspace: Path, node: str, task: str, timestamp: str) -> Path:
    if not TIMESTAMP_RE.fullmatch(timestamp):
        raise ValueError("timestamp must use YYYYMMDDTHHMMSSZ")
    directory = workspace / "fpf-reports"
    stem = f"{timestamp}-fpf-{node}-{_slug(task)}"
    candidate = directory / f"{stem}.md"
    suffix = 2
    while candidate.exists():
        candidate = directory / f"{stem}-{suffix}.md"
        suffix += 1
    return candidate


def _validated_units(units: object) -> dict[str, dict[str, object]]:
    if not isinstance(units, list):
        raise ValueError("topology must be a JSON list")
    indexed: dict[str, dict[str, object]] = {}
    for unit in units:
        if not isinstance(unit, dict) or not isinstance(unit.get("id"), str):
            raise ValueError("every Scope Unit must have a string id")
        identifier = str(unit["id"])
        if identifier in indexed:
            raise ValueError(f"duplicate Scope Unit id: {identifier}")
        if unit.get("kind") not in {"project", "structural", "bseed"}:
            raise ValueError(f"invalid Scope Unit kind: {identifier}")
        if not isinstance(unit.get("contains"), list) or not isinstance(unit.get("depth"), int):
            raise ValueError(f"Scope Unit lacks explicit scope/depth authority: {identifier}")
        indexed[identifier] = unit
    return indexed


def _unique_deepest(candidates: list[dict[str, object]], label: str) -> dict[str, object]:
    if not candidates:
        raise ValueError(f"no proven {label} contains the complete analysis scope")
    best = max(int(item["depth"]) for item in candidates)
    deepest = [item for item in candidates if item["depth"] == best]
    if len(deepest) != 1:
        raise ValueError(f"incomparable {label} candidates contain the analysis scope")
    return deepest[0]


def select_scope_unit(units: object, scoped_unit_ids: list[str]) -> str:
    indexed = _validated_units(units)
    scoped = set(scoped_unit_ids)
    if not scoped or not scoped.issubset(indexed):
        raise ValueError("analysis scope must map to known Scope Units")
    scoped_kinds = {indexed[item]["kind"] for item in scoped}
    if scoped_kinds == {"bseed"}:
        candidates = [
            unit for unit in indexed.values()
            if unit["kind"] == "bseed"
            and scoped.issubset(set(unit.get("cumulative_contains", [])))
            and isinstance(unit.get("bseed_order"), int)
        ]
        if not candidates:
            raise ValueError("no downstream BSEED Scope Unit has declared cumulative scope")
        order = max(int(item["bseed_order"]) for item in candidates)
        lowest = [item for item in candidates if item["bseed_order"] == order]
        if len(lowest) != 1:
            raise ValueError("BSEED downstream containment is ambiguous")
        return str(lowest[0]["id"])
    if "bseed" in scoped_kinds:
        candidates = [
            unit for unit in indexed.values()
            if unit["kind"] == "project" and scoped.issubset(set(unit["contains"]))
        ]
        return str(_unique_deepest(candidates, "project Scope Unit")["id"])
    candidates = [
        unit for unit in indexed.values()
        if unit["kind"] != "bseed" and scoped.issubset(set(unit["contains"]))
    ]
    return str(_unique_deepest(candidates, "structural Scope Unit")["id"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="style", required=True)
    plain = subcommands.add_parser("plain")
    plain.add_argument("--workspace", type=Path, required=True)
    plain.add_argument("--node", required=True)
    plain.add_argument("--task", required=True)
    plain.add_argument("--timestamp", required=True)
    caprmedio = subcommands.add_parser("caprmedio")
    caprmedio.add_argument("--topology-json", type=Path, required=True)
    caprmedio.add_argument("--scope-unit", action="append", required=True)
    caprmedio.add_argument("--composition", action="store_true")
    args = parser.parse_args()
    if args.style == "plain":
        output = {"style": "plain", "path": str(plain_report_path(
            args.workspace, args.node, args.task, args.timestamp,
        )), "writes": 1}
    else:
        topology = json.loads(args.topology_json.read_text(encoding="utf-8"))
        output = {
            "style": "caprmedio",
            "scope_unit": select_scope_unit(topology, args.scope_unit),
            "atom_type": "Analysis Report", "atoms": 1,
            "composition": bool(args.composition),
        }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
