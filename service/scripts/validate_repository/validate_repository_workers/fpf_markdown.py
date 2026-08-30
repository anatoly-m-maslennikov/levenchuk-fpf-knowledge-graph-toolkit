"""Parse the end-user FPF Markdown graph for deterministic maintenance checks."""

from __future__ import annotations

import re
from pathlib import Path


COMMAND_GRAPH = "skills/fpf.skill/references/fpf-command-graph.md"
PROFILE_FILES = {
    "framework": "skills/fpf.skill/profiles/fpf-profiles-framework.md",
    "software": "skills/fpf.skill/profiles/fpf-profiles-software.md",
    "skills": "skills/fpf.skill/profiles/fpf-profiles-skills.md",
}
SCENARIOS = "skills/fpf.skill/references/fpf-routing-scenarios.md"


def _plain(value: str) -> str:
    return value.strip().strip("`")


def _items(value: str) -> list[str]:
    if value.strip() == "—":
        return []
    return [_plain(item) for item in value.split("<br>") if _plain(item)]


def _link(value: str) -> tuple[str, str] | None:
    match = re.fullmatch(r"\[([^]]+)]\(([^)]+)\)", value.strip())
    return (match.group(1), match.group(2)) if match else None


def _table(text: str, heading: str) -> list[dict[str, str]]:
    marker = f"## {heading}\n"
    if marker not in text:
        raise ValueError(f"missing Markdown table heading: {heading}")
    section = text.split(marker, 1)[1]
    section = section.split("\n## ", 1)[0]
    lines = [line for line in section.splitlines() if line.startswith("|")]
    if len(lines) < 2:
        raise ValueError(f"missing Markdown table: {heading}")
    headers = [item.strip() for item in lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in lines[2:]:
        cells = [item.strip() for item in line.strip("|").split("|")]
        if len(cells) != len(headers):
            raise ValueError(f"malformed Markdown table row under {heading}: {line}")
        rows.append(dict(zip(headers, cells)))
    return rows


def _bindings(value: str) -> list[dict[str, str]]:
    results = []
    for item in value.split("<br>"):
        match = re.search(r"`([^`@]+)@([^`]+)`(?: when (.+))?", item.strip())
        if match:
            binding = {"id": match.group(1), "relation": match.group(2)}
            if match.group(3):
                binding["when"] = match.group(3).strip()
            results.append(binding)
    return results


def _parse_commands(skill_root: Path, text: str) -> list[dict[str, object]]:
    nodes = []
    for row in _table(text, "Command nodes"):
        prompt = _link(row["Prompt"])
        if prompt is None:
            raise ValueError(f"invalid command prompt link: {row['ID']}")
        prompt_path = (skill_root / "references" / prompt[1]).resolve()
        try:
            prompt_relative = prompt_path.relative_to(skill_root.resolve()).as_posix()
        except ValueError as exc:
            raise ValueError(f"command prompt escapes skill root: {row['ID']}") from exc
        nodes.append({
            "id": _plain(row["ID"]),
            "command": _plain(row["Command"]),
            "localized_command": _plain(row["Russian command"]),
            "aliases": _items(row["Aliases"]),
            "routing_cues": _items(row["Routing cues"]),
            "prompt": prompt_relative,
            "persist_report": row["Saves report"] == "yes",
            "fpf_entrypoints": _bindings(row["FPF bindings"]),
        })
    return nodes


def _parse_edges(text: str) -> list[dict[str, str]]:
    return [
        {"from": _plain(row["From"]), "to": _plain(row["To"]), "relation": row["Required handoff"]}
        for row in _table(text, "Legal composition handoffs")
    ]


def _parse_profile_section(
    profile_id: str, title: str, area: str, section: str,
) -> tuple[dict[str, object], dict[str, object] | None]:
    description = next((line for line in section.splitlines() if line and not line.startswith("-")), "")
    fields: dict[str, list[str]] = {}
    examples: list[dict[str, str]] = []
    case: dict[str, object] | None = None
    for line in section.splitlines():
        if line.startswith(("- Aliases: ", "- Routing cues: ", "- FPF context: ")):
            label, value = line[2:].split(": ", 1)
            fields[label] = re.findall(r"`([^`]+)`", value)
        elif found := re.fullmatch(r"- Example → `([^`]+)`: (.+)", line):
            examples.append({"expected_node": found.group(1), "text": found.group(2)})
        elif found := re.fullmatch(r"- Evaluation case `([^`]+)` → `([^`]+)`: (.+)", line):
            case = {"id": found.group(1), "node": found.group(2), "task": found.group(3)}
        elif line.startswith("- Required facets: ") and case is not None:
            case["required_facets"] = [item.strip() for item in line.removeprefix("- Required facets: ").split(",")]
        elif line.startswith("- Forbidden inference: ") and case is not None:
            case["forbidden_inference"] = line.removeprefix("- Forbidden inference: ")
    bindings = [
        {"id": value.split("@", 1)[0], "relation": value.split("@", 1)[1]}
        for value in fields.get("FPF context", [])
    ]
    profile = {
        "id": profile_id, "area": area, "title": title, "description": description,
        "aliases": fields.get("Aliases", []), "keywords": fields.get("Routing cues", []),
        "fpf_entrypoints": bindings, "examples": examples,
    }
    if case is not None:
        case["profile"] = profile_id
    return profile, case


def _parse_profiles(path: Path, area: str) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    text = path.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^## `([^`]+)` — (.+)$", text, re.MULTILINE))
    profiles: list[dict[str, object]] = []
    cases: list[dict[str, object]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        profile, case = _parse_profile_section(
            match.group(1), match.group(2), area, text[match.end():end],
        )
        profiles.append(profile)
        if case is not None:
            cases.append(case)
    return profiles, cases


def load_markdown_graph(root: Path) -> dict[str, object]:
    skill_root = root / "skills/fpf.skill"
    text = (root / COMMAND_GRAPH).read_text(encoding="utf-8")
    profiles: list[dict[str, object]] = []
    cases: list[dict[str, object]] = []
    for area, relative in PROFILE_FILES.items():
        area_profiles, area_cases = _parse_profiles(root / relative, area)
        profiles.extend(area_profiles)
        cases.extend(area_cases)
    areas = [
        {"id": area, "profile_file": relative}
        for area, relative in PROFILE_FILES.items()
    ]
    return {
        "schema_version": "markdown-1", "fallback_node": "plan",
        "repository_graph_root": "FPF-Knowledge-Graph",
        "nodes": _parse_commands(skill_root, text), "edges": _parse_edges(text),
        "areas": areas, "task_profiles": profiles, "evaluation_cases": cases,
    }


def load_routing_scenarios(root: Path) -> list[dict[str, object]]:
    text = (root / SCENARIOS).read_text(encoding="utf-8")
    scenarios = []
    marker = "| ID | Expected route | Mode | Route action | Question | Stop condition |"
    if marker not in text:
        raise ValueError("routing scenario table header is missing")
    lines = [line for line in text[text.index(marker):].splitlines() if line.startswith("|")]
    for line in lines[2:]:
        cells = [item.strip() for item in line.strip("|").split("|")]
        if len(cells) != 6:
            raise ValueError(f"malformed routing scenario row: {line}")
        route = [] if cells[1] == "—" else re.findall(r"`([^`]+)`", cells[1])
        scenarios.append({
            "id": _plain(cells[0]), "expected_sequence": route,
            "expected_mode": cells[2], "route_action": cells[3],
            "question": cells[4], "stop_condition": cells[5],
        })
    return scenarios
