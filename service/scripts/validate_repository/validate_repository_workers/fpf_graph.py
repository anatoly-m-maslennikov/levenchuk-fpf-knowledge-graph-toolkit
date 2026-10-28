"""Validate the zero-executable FPF Markdown command graph."""

from __future__ import annotations

import re
from pathlib import Path

from .fpf_markdown import load_markdown_graph
from .fpf_profiles import validate_areas_and_profiles


ALLOWED_RELATIONS = {
    "primary_method", "conditional_method", "result_projection",
    "routing_method", "routing_entrypoint", "profile_context",
}
FORBIDDEN_RUNTIME_TEXT = (
    "scripts/route_fpf.py", "scripts/read_fpf_graph.py", "scripts/prepare_fpf_context.py",
    "scripts/plan_fpf_report.py", "graph.yaml", "profiles.yaml",
    "uv --project", "uv run", "run python",
)
ORCHESTRATION_PROMPTS = {"fpf-manager.md", "fpf-runtime.md", "fpf-warden.md"}


def _missing(text: str, fragments: list[str], label: str) -> list[str]:
    return [f"{label} is missing contract text: {item}" for item in fragments if item not in text]


def _fpf_index(root: Path) -> dict[str, Path]:
    graph_root = root / "FPF-Knowledge-Graph"
    index = graph_root / "00_Index/FPF - Index.md"
    results: dict[str, Path] = {}
    for line in index.read_text(encoding="utf-8").splitlines():
        match = re.match(r"\|\s*([^| ]+)\s*\|\s*\[\[([^]]+)]]\s*\|", line)
        if match:
            results[match.group(1)] = graph_root / f"{match.group(2)}.md"
    return results


def _validate_binding(root: Path, owner: str, binding: object) -> list[str]:
    if not isinstance(binding, dict):
        return [f"FPF Markdown binding is not an object: {owner}"]
    identifier = binding.get("id")
    relation = binding.get("relation")
    errors = [] if relation in ALLOWED_RELATIONS else [
        f"FPF Markdown binding relation is invalid: {owner}:{relation}"
    ]
    page = _fpf_index(root).get(str(identifier))
    if page is None or not page.is_file():
        return errors + [f"FPF Markdown binding ID does not resolve: {owner}:{identifier}"]
    declared = re.search(
        r'^fpf_id:\s*["\']?([^"\'\n]+)', page.read_text(encoding="utf-8"), re.MULTILINE
    )
    if declared is None or declared.group(1).strip() != identifier:
        errors.append(f"FPF Markdown binding ID does not match page content: {owner}:{identifier}")
    if relation == "conditional_method" and not binding.get("when"):
        errors.append(f"conditional FPF binding lacks a condition: {owner}:{identifier}")
    return errors


def _validate_prompt(path: Path, node: str, contracts: dict[str, object]) -> list[str]:
    if not path.is_file():
        return [f"missing FPF prompt node: {node}"]
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    if node == "plan":
        errors.extend(_missing(text, contracts["common_prompt_fragments"], node))
        errors.extend(_missing(text, contracts["plan_prompt_fragments"], node))
        if text.count("<!-- output-settings:start -->") != 1 or text.count("<!-- output-settings:end -->") != 1:
            errors.append("plan must contain exactly one output settings block")
    elif node != "help":
        errors.extend(_missing(text, contracts["analytical_prompt_fragments"], node))
        if "<!-- output-settings:" in text or "## Output and report settings" in text:
            errors.append(f"analytical prompt repeats the shared output contract: {node}")
    if re.search(r"</?(?:details|summary)\b", text, re.IGNORECASE):
        errors.append(f"HTML disclosure tag in prompt: {node}")
    if re.match(r"\A---\n", text):
        errors.append(f"prompt node must not declare skill frontmatter: {node}")
    return errors


def _validate_runtime_package(skill_root: Path) -> list[str]:
    errors: list[str] = []
    for path in skill_root.rglob("*"):
        if not path.is_file() or path.name == ".DS_Store":
            continue
        if path.name != "SKILL.md" and path.suffix != ".md":
            errors.append(f"end-user FPF runtime contains a non-Markdown package file: {path}")
    runtime_files = [
        skill_root / "SKILL.md",
        *(skill_root / "prompts" / name for name in sorted(ORCHESTRATION_PROMPTS)),
    ]
    for path in runtime_files:
        text = path.read_text(encoding="utf-8")
        for fragment in FORBIDDEN_RUNTIME_TEXT:
            if fragment in text:
                errors.append(f"end-user FPF runtime depends on forbidden executable data: {path}:{fragment}")
    runtime = (skill_root / "prompts/fpf-runtime.md").read_text(encoding="utf-8")
    required = [
        "Never run Python, uv, a shell command", "references/fpf-command-graph.md",
        "Markdown/plain-text file access", ".fpf-runtime.toml", "repository_root",
    ]
    errors.extend(_missing(runtime, required, "Markdown runtime"))
    return errors


def _validate_nodes(root: Path, nodes: list[dict[str, object]], contracts: dict[str, object]) -> list[str]:
    errors: list[str] = []
    node_ids = [node["id"] for node in nodes]
    skill_root = root / "skills/fpf.skill"
    prompt_ids = {
        path.stem.removeprefix("fpf-")
        for path in (skill_root / "prompts").glob("fpf-*.md")
        if path.name not in ORCHESTRATION_PROMPTS
    }
    expected = prompt_ids | {"help"}
    if set(node_ids) != expected or len(node_ids) != len(expected):
        errors.append("FPF Markdown nodes do not exactly match their prompt files")
    if not {"help", "plan"}.issubset(node_ids):
        errors.append("FPF Markdown graph lacks Help or Plan")
    analytical = {node["id"] for node in nodes if node["persist_report"]}
    persistent = {node["id"] for node in nodes if node["persist_report"]}
    if persistent & {"help", "plan"} or not persistent:
        errors.append("FPF Markdown persistence flags do not define a valid analytical set")
    aliases: dict[str, str] = {}
    for node in nodes:
        node_id = str(node["id"])
        expected_prompt = "prompts/help/en/fpf-help.md" if node_id == "help" else f"prompts/fpf-{node_id}.md"
        if node["prompt"] != expected_prompt:
            errors.append(f"FPF Markdown prompt path mismatch: {node_id}")
        errors.extend(_validate_prompt(root / "skills/fpf.skill" / expected_prompt, node_id, contracts))
        for value in [node["command"], node["localized_command"], *node["aliases"]]:
            key = str(value).casefold().strip()
            if not key or (key in aliases and aliases[key] != node_id):
                errors.append(f"FPF Markdown alias is empty or duplicated: {node_id}:{value}")
            else:
                aliases[key] = node_id
        bindings = node["fpf_entrypoints"]
        if node_id in analytical and not bindings:
            errors.append(f"FPF Markdown analytical node lacks FPF bindings: {node_id}")
        if node_id not in analytical and bindings:
            errors.append(f"FPF Markdown ephemeral node has FPF bindings: {node_id}")
        for binding in bindings:
            errors.extend(_validate_binding(root, node_id, binding))
    return errors


def _validate_edges(edges: list[dict[str, object]], analytical: set[str]) -> list[str]:
    errors: list[str] = []
    edge_pairs = [(edge["from"], edge["to"]) for edge in edges]
    if len(edge_pairs) != len(set(edge_pairs)):
        errors.append("FPF Markdown composition edges are duplicated")
    for edge in edges:
        handoff_fields = (
            "producer_output", "consumer_input", "required_evidence", "gate_predicate",
        )
        if (
            edge["from"] not in analytical or edge["to"] not in analytical
            or any(not edge.get(field) for field in handoff_fields)
            or not re.fullmatch(r"STOP_[A-Z0-9_]+", str(edge.get("stop_state", "")))
        ):
            errors.append(f"FPF Markdown composition edge is invalid: {edge}")
    return errors


def _validate_help_inventory(skill_root: Path, nodes: list[dict[str, object]]) -> list[str]:
    analytical = [node for node in nodes if node.get("persist_report")]
    errors: list[str] = []
    for language in ("en", "ru"):
        for area in ("framework", "software", "skills"):
            path = skill_root / f"prompts/help/{language}/fpf-help-{area}.md"
            text = path.read_text(encoding="utf-8")
            missing = [
                str(node["id"]) for node in analytical
                if f"`$fpf {node['command']} " not in text
            ]
            if missing:
                errors.append(f"FPF {language} Help inventory is incomplete: {area}:{missing}")
            missing_aliases = [
                str(node["id"]) for node in analytical
                if language == "ru" and f"псевдоним: `{node['localized_command']}`" not in text
            ]
            if missing_aliases:
                errors.append(f"FPF ru Help aliases are incomplete: {area}:{missing_aliases}")
    return errors


def validate_fpf_manifest(root: Path, contracts: dict[str, object]) -> list[str]:
    try:
        manifest = load_markdown_graph(root)
    except (OSError, ValueError) as exc:
        return [f"cannot read FPF Markdown graph: {exc}"]
    analytical = {
        node["id"] for node in manifest["nodes"] if node.get("persist_report")
    }
    errors = _validate_runtime_package(root / "skills/fpf.skill")
    errors.extend(_validate_nodes(root, manifest["nodes"], contracts))
    errors.extend(_validate_edges(manifest["edges"], analytical))
    errors.extend(_validate_help_inventory(root / "skills/fpf.skill", manifest["nodes"]))
    errors.extend(validate_areas_and_profiles(root, manifest, analytical, _validate_binding))
    return errors
