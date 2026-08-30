"""Build a bounded current-versus-backup evaluation pack."""

from __future__ import annotations

import json
import hashlib
import re
from pathlib import Path

from .eval_risk import risk_inventory


REPORT = Path("00_Index") / "FPF - Validation Report.json"
MAX_COMPLETE_CHANGE_KIND = 12


def inventory(root: Path) -> tuple[dict[str, str], dict[str, str], dict[str, object]]:
    identifiers: dict[str, str] = {}
    titles: dict[str, str] = {}
    for path in sorted(root.rglob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")[:6000]
        identifier = re.search(r'^fpf_id: "([^"]+)"$', text, re.MULTILINE)
        title = re.search(r'^title: "([^"]*)"$', text, re.MULTILINE)
        if identifier:
            value = identifier.group(1)
            if value in identifiers:
                raise ValueError(
                    f"duplicate fpf_id {value}: {identifiers[value]} and "
                    f"{path.relative_to(root).as_posix()}"
                )
            identifiers[value] = path.relative_to(root).as_posix()
            titles[value] = title.group(1) if title else ""
    report = json.loads((root / REPORT).read_text(encoding="utf-8"))
    return identifiers, titles, report


def _changes(current_ids, backup_ids, current_titles, backup_titles):
    common = sorted(set(current_ids) & set(backup_ids))
    added = sorted(set(current_ids) - set(backup_ids))
    removed = sorted(set(backup_ids) - set(current_ids))
    moved = sorted(item for item in common if current_ids[item] != backup_ids[item])
    retitled = sorted(item for item in common if current_titles[item] != backup_titles[item])
    return added, removed, moved, retitled


def _targets(selected, current_ids, backup_ids, moved, retitled):
    return [
        dict(
            fpf_id=item,
            current_path=(
                f"FPF-Knowledge-Graph/{current_ids[item]}"
                if item in current_ids else None
            ),
            backup_path=f"FPF-Knowledge-Graph.bak/{backup_ids[item]}" if item in backup_ids else None,
            title_changed=item in retitled, path_changed=item in moved,
            removed=item not in current_ids, added=item not in backup_ids,
        )
        for item in selected
    ]


def _bounded(values: list[str]) -> list[str]:
    if len(values) <= MAX_COMPLETE_CHANGE_KIND:
        return values
    return [values[0], values[len(values) // 2], values[-1]]


def eval_pack_sha256(pack: dict[str, object]) -> str:
    payload = {key: value for key, value in pack.items() if key != "eval_pack_sha256"}
    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _selection(delta: dict[str, list[str]], roots: list[str]) -> tuple[list[str], dict[str, object]]:
    selected_by_kind = {
        "added": _bounded(delta["added"]), "removed": delta["removed"],
        "moved": _bounded(delta["moved"]), "retitled": _bounded(delta["retitled"]),
        "top_level_roots": roots,
    }
    selected = sorted(set(item for values in selected_by_kind.values() for item in values))
    changed = set(sum(delta.values(), []))
    details = {
        "policy": "all changes through 12 per kind; otherwise first-middle-last; all removed IDs and top-level roots",
        "selected_count": len(selected),
        "omitted_count": len(changed - set(selected)),
        "by_kind": {
            kind: {"population": len(delta[kind]), "selected": values, "omitted": len(delta[kind]) - len(values)}
            for kind, values in selected_by_kind.items() if kind in delta
        },
    }
    return selected, details


def build_eval_pack(current: Path, backup: Path) -> dict[str, object]:
    current_ids, current_titles, current_report = inventory(current)
    backup_ids, backup_titles, backup_report = inventory(backup)
    added, removed, moved, retitled = _changes(current_ids, backup_ids, current_titles, backup_titles)
    delta = {"added": added, "removed": removed, "moved": moved, "retitled": retitled}
    roots: dict[str, str] = {}
    for identifier in sorted(current_ids):
        roots.setdefault(identifier.split(".", 1)[0], identifier)
    selected, selection = _selection(delta, list(roots.values()))
    counts = dict(
        backup_ids=len(backup_ids), current_ids=len(current_ids),
        added_ids=len(added), removed_ids=len(removed),
        moved_ids=len(moved), retitled_ids=len(retitled),
    )
    integrity = dict(
        broken_links=current_report.get("broken_links_count"),
        unresolved_relations=current_report.get("unresolved_relations_count"),
        unresolved_relation_sample=current_report.get("unresolved_relations_sample", []),
    )
    pack = dict(
        schema_version=2, purpose="bounded evidence pack for FPF graph conversion result evaluation",
        backup_revision=backup_report.get("source_revision"),
        current_revision=current_report.get("source_revision"), counts=counts,
        delta=delta, selection=selection,
        selected_eval_targets=_targets(selected, current_ids, backup_ids, moved, retitled),
        syntax_risk_strata=risk_inventory(
            current, current_ids, current_titles,
            set(added + moved + retitled),
        ),
        builder_integrity=integrity,
    )
    pack["eval_pack_sha256"] = eval_pack_sha256(pack)
    return pack


def main(root: Path) -> int:
    current = root / "FPF-Knowledge-Graph"
    backup = root / "FPF-Knowledge-Graph.bak"
    if not current.is_dir() or not backup.is_dir():
        raise SystemExit("current graph and FPF-Knowledge-Graph.bak are both required")
    print(json.dumps(build_eval_pack(current, backup), ensure_ascii=False, indent=2))
    return 0
