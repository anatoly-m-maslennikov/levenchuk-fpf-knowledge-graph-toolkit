"""Build bounded, verified FPF pattern context for selected command nodes."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from .graph import node_view, profile_view, selected_nodes, selected_profiles


CORE_SECTIONS = {"problem_frame", "problem", "forces", "solution", "consequences"}
HEADING_RE = re.compile(r"^##\s+.*:[A-Za-z0-9.]+\s+(?:-|—|–)\s+(.+?)\s*$")


def _section_name(label: str) -> str | None:
    plain = re.sub(r"[*_`]", "", label).casefold()
    plain = plain.replace("‑", "-").replace("–", "-").replace("—", "-")
    if "problem frame" in plain:
        return "problem_frame"
    if "problem" in plain or "what goes wrong if missed" in plain:
        return "problem"
    if "forces" in plain:
        return "forces"
    if "solution" in plain:
        return "solution"
    if "consequences" in plain or "trade-offs & mitigations" in plain or "what this buys" in plain:
        return "consequences"
    return None


def _frontmatter(text: str) -> dict[str, object]:
    if not text.startswith("---\n"):
        raise ValueError("FPF page lacks YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("FPF page has unterminated YAML frontmatter")
    value = yaml.safe_load(text[4:end])
    if not isinstance(value, dict):
        raise ValueError("FPF page frontmatter must be a mapping")
    return value


def _section_ranges(lines: list[str]) -> dict[str, tuple[int, int]]:
    headings: list[tuple[str | None, int]] = []
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if match:
            headings.append((_section_name(match.group(1)), index))
    ranges: dict[str, tuple[int, int]] = {}
    for position, (name, start) in enumerate(headings):
        if name is not None:
            end = headings[position + 1][1] if position + 1 < len(headings) else len(lines)
            ranges[name] = (start, end)
    return ranges


def _bounded_section(
    lines: list[str], start: int, end: int, limit: int | None,
) -> dict[str, object]:
    text = "\n".join(lines[start:end]).strip()
    complete = limit is None or len(text) <= limit
    if not complete:
        excerpt = text[:limit].rsplit("\n", 1)[0].rstrip()
        headings = [
            {"line": index + 1, "heading": lines[index]}
            for index in range(start + 1, end) if lines[index].startswith("###")
        ]
    else:
        excerpt, headings = text, []
    return {
        "start_line": start + 1, "end_line": end,
        "complete": complete, "text": excerpt, "remaining_headings": headings,
    }


def hydrate_binding(
    repository_root: Path, binding: dict[str, object], solution_chars: int,
    core_sections: list[str],
) -> dict[str, object]:
    relative = Path(str(binding["repository_path"]))
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"unsafe FPF repository path: {relative}")
    page = repository_root / relative
    text = page.read_text(encoding="utf-8")
    metadata = _frontmatter(text)
    if metadata.get("fpf_id") != binding.get("id"):
        raise ValueError(f"FPF ID mismatch at {relative}")
    lines = text.splitlines()
    ranges = _section_ranges(lines)
    missing = set(core_sections) - set(ranges)
    sections = {
        name: _bounded_section(lines, start, end, solution_chars if name == "solution" else None)
        for name, (start, end) in ranges.items() if name in core_sections
    }
    return {
        "id": binding["id"], "repository_path": relative.as_posix(),
        "title": metadata.get("title"), "status": metadata.get("status"),
        "source_revision": metadata.get("source_revision"), "sections": sections,
        "missing_core_sections": sorted(missing),
    }


def build_context(
    graph: dict[str, object], skill_root: Path, repository_root: Path,
    node_ids: list[str], include_conditionals: set[str] | None = None,
    profile_ids: list[str] | None = None,
) -> dict[str, object]:
    nodes = selected_nodes(graph, node_ids)
    profiles = selected_profiles(graph, profile_ids or [])
    connector = graph.get("connector", {})
    solution_chars = int(connector.get("default_solution_chars", 6000))
    core_sections = list(connector.get("core_sections", CORE_SECTIONS))
    include = include_conditionals or set()
    contracts = list(dict.fromkeys(path for node in nodes for path in node.get("contracts", [])))
    patterns: dict[tuple[str, str], dict[str, object]] = {}
    skipped: list[dict[str, object]] = []
    context_owners = [
        ("node", node["id"], node.get("fpf_entrypoints", [])) for node in nodes
    ] + [
        ("profile", profile["id"], profile.get("fpf_entrypoints", []))
        for profile in profiles
    ]
    for owner_type, owner_id, bindings in context_owners:
        for binding in bindings:
            if binding.get("relation") == "conditional_method" and binding.get("id") not in include:
                skipped.append({owner_type: owner_id, **binding})
                continue
            key = (str(binding["id"]), str(binding["repository_path"]))
            if key not in patterns:
                patterns[key] = hydrate_binding(
                    repository_root, binding, solution_chars, core_sections
                )
                patterns[key]["uses"] = []
            patterns[key]["uses"].append({
                owner_type: owner_id, "relation": binding["relation"],
                **({"when": binding["when"]} if "when" in binding else {}),
            })
    resource_paths = contracts + [str(node["prompt"]) for node in nodes]
    for relative in resource_paths:
        if not (skill_root / relative).is_file():
            raise ValueError(f"missing selected skill resource: {relative}")
    return {
        "schema_version": 2, "nodes": [node_view(node) for node in nodes],
        "task_profiles": [profile_view(profile) for profile in profiles],
        "contracts": contracts, "prompts": [node["prompt"] for node in nodes],
        "patterns": list(patterns.values()), "skipped_conditionals": skipped,
    }
