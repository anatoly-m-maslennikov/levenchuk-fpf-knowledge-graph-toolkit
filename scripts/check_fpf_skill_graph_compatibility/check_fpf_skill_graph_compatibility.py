"""Check methodology skills for stale hard-coded graph dependencies."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GRAPH = ROOT / "FPF-Knowledge-Graph"
SKILLS = ROOT / "skills"
METHODOLOGY_PROMPTS = (
    "alignment-audit", "applicability-scan", "decision-synthesize",
    "design-challenge", "options-explore", "quality-improve", "plan", "sota-harvest",
)
ID_RE = re.compile(r"(?<![\w/`|#])([A-Z](?:\.[A-Za-z0-9][A-Za-z0-9-]*)+)(?![\w/`-])")
GRAPH_PATH_RE = re.compile(r"`(FPF-Knowledge-Graph/[^`]+\.md)`")
REVISION_RE = re.compile(r"\b[0-9a-f]{40}\b")


def graph_ids() -> set[str]:
    identifiers: set[str] = set()
    for path in GRAPH.rglob("*.md"):
        text = path.read_text(encoding="utf-8", errors="replace")
        match = re.search(r'^fpf_id: "([^"]+)"$', text, re.MULTILINE)
        if match:
            identifiers.add(match.group(1))
    return identifiers


def _skill_result(name: str, identifiers: set[str]) -> tuple[dict[str, object], list[str]]:
    path = SKILLS / "fpf.skill" / "prompts" / f"{name}.md"
    if not path.is_file():
        return dict(prompt=name), [f"missing methodology prompt: {path.relative_to(ROOT)}"]
    text = path.read_text(encoding="utf-8")
    hardcoded_ids = sorted({item for item in ID_RE.findall(text) if not item.startswith("U.")})
    unresolved = sorted(set(hardcoded_ids) - identifiers)
    mentions = sorted(set(GRAPH_PATH_RE.findall(text)))
    templates = [item for item in mentions if "<" in item or ">" in item]
    graph_paths = [item for item in mentions if item not in templates]
    missing = sorted(item for item in graph_paths if not (ROOT / item).is_file())
    revisions = sorted(set(REVISION_RE.findall(text)))
    errors = []
    if unresolved:
        errors.append(f"{name} has unresolved hard-coded FPF IDs: {unresolved}")
    if missing:
        errors.append(f"{name} has missing hard-coded graph paths: {missing}")
    if revisions:
        errors.append(f"{name} hard-codes source revisions: {revisions}")
    result = dict(
        prompt=name, hardcoded_fpf_ids=hardcoded_ids,
        hardcoded_graph_paths=graph_paths, graph_path_templates=templates,
        hardcoded_source_revisions=revisions,
    )
    return result, errors


def main() -> int:
    identifiers = graph_ids()
    results: list[dict[str, object]] = []
    errors: list[str] = []
    for name in METHODOLOGY_PROMPTS:
        result, skill_errors = _skill_result(name, identifiers)
        results.append(result)
        errors.extend(skill_errors)
    output = dict(
        graph_ids=len(identifiers), methodology_prompts=len(results),
        update_required=bool(errors), errors=errors, prompts=results,
    )
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 1 if errors else 0
