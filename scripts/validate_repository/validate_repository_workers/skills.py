"""Validate the portable FPF graph skill and its routing fixtures."""

from __future__ import annotations

import json
import re
from pathlib import Path


def _missing_fragments(text: str, fragments: list[str], label: str) -> list[str]:
    return [f"{label} is missing contract text: {fragment}" for fragment in fragments if fragment not in text]


def _validate_frontmatter(path: Path, expected_name: str) -> list[str]:
    text = path.read_text(encoding="utf-8")
    frontmatter = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not frontmatter:
        return [f"missing skill frontmatter: {path}"]
    name = re.search(r"^name:\s*(\S+)\s*$", frontmatter.group(1), re.MULTILINE)
    description = re.search(r"^description:\s*(.+)$", frontmatter.group(1), re.MULTILINE)
    errors: list[str] = []
    if name is None or name.group(1) != expected_name:
        errors.append(f"skill name mismatch: {expected_name}")
    if description is None or not description.group(1).strip():
        errors.append(f"missing skill description: {expected_name}")
    return errors


def _validate_prompt(path: Path, node: str, contracts: dict[str, object]) -> list[str]:
    if not path.is_file():
        return [f"missing FPF prompt node: {node}"]
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    if node != "help":
        errors.extend(_missing_fragments(text, contracts["common_prompt_fragments"], node))
        specific = "plan_prompt_fragments" if node == "plan" else "analytical_prompt_fragments"
        errors.extend(_missing_fragments(text, contracts[specific], node))
        if text.count("<!-- output-settings:start -->") != 1:
            errors.append(f"missing or duplicate output settings block: {node}")
        if text.count("<!-- output-settings:end -->") != 1:
            errors.append(f"missing or duplicate output settings block end: {node}")
    if re.search(r"</?(?:details|summary)\b", text, re.IGNORECASE):
        errors.append(f"HTML disclosure tag in prompt: {node}")
    if re.match(r"\A---\n", text):
        errors.append(f"prompt node must not declare skill frontmatter: {node}")
    return errors


def _load_manifest(root: Path) -> tuple[dict[str, object], list[str]]:
    path = root / "skills/fpf.skill/graph.json"
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"cannot read FPF graph manifest: {exc}"]
    return manifest, []


def _validate_package_roots(skills_root: Path, contracts: dict[str, object]) -> list[str]:
    names = list(contracts["end_user_skills"]) + list(contracts["service_skills"])
    expected = {f"{name}.skill" for name in names}
    actual = {
        path.name for path in skills_root.glob("*.skill")
        if path.is_dir() and (path / "SKILL.md").is_file()
    }
    errors = [] if actual == expected else ["skill package set does not match the contract asset"]

    for name in names:
        path = skills_root / f"{name}.skill" / "SKILL.md"
        if not path.is_file():
            errors.append(f"missing skill package: {name}")
            continue
        errors.extend(_validate_frontmatter(path, name))
        fragments = (
            contracts["service_skill_fragments"][name] if name in contracts["service_skills"]
            else contracts["fpf_skill_fragments"]
        )
        errors.extend(_missing_fragments(path.read_text(encoding="utf-8"), fragments, name))

    readme = (skills_root / "README.md").read_text(encoding="utf-8")
    errors.extend(f"skills README omits {name}.skill" for name in names if f"`{name}.skill`" not in readme)
    return errors


def _validate_project_discovery(root: Path, contracts: dict[str, object]) -> list[str]:
    discovery = root / ".agents" / "skills"
    service_names = set(contracts["service_skills"])
    actual = {path.name for path in discovery.iterdir()} if discovery.is_dir() else set()
    errors = [] if actual == service_names else [
        "project skill discovery must expose exactly the service skills"
    ]
    for name in sorted(service_names):
        link = discovery / name
        expected = (root / "skills" / f"{name}.skill").resolve()
        if not link.is_symlink() or link.resolve() != expected:
            errors.append(f"project service skill link is invalid: {name}")
    return errors


def _validate_manifest(root: Path, contracts: dict[str, object]) -> list[str]:
    manifest, errors = _load_manifest(root)
    expected_nodes = set(contracts["prompt_nodes"])
    nodes = manifest.get("nodes", []) if isinstance(manifest, dict) else []
    node_ids = [node.get("id") for node in nodes if isinstance(node, dict)]
    if set(node_ids) != expected_nodes or len(node_ids) != len(expected_nodes):
        errors.append("FPF graph nodes do not match the prompt-node contract")
    analytical = set(contracts["analytical_nodes"])
    persistent = {node.get("id") for node in nodes if isinstance(node, dict) and node.get("persist_report")}
    if persistent != analytical:
        errors.append("FPF graph persistence flags do not match the seven analytical nodes")
    if manifest.get("fallback_node") != "plan":
        errors.append("FPF graph fallback node must be plan")
    if manifest.get("schema_version") != 2:
        errors.append("FPF graph schema version must be 2")
    composition = manifest.get("composition", {})
    if not isinstance(composition, dict) or composition.get("operator") != "+":
        errors.append("FPF graph must declare the + composition operator")
    elif composition.get("reference") != "references/composition.md":
        errors.append("FPF graph composition reference is invalid")

    prompts_root = root / "skills/fpf.skill/prompts"
    for node in contracts["prompt_nodes"]:
        errors.extend(_validate_prompt(prompts_root / f"{node}.md", node, contracts))
    for node in nodes:
        if not isinstance(node, dict):
            continue
        expected_prompt = f"prompts/{node.get('id')}.md"
        if node.get("prompt") != expected_prompt:
            errors.append(f"FPF graph prompt path mismatch: {node.get('id')}")

    return errors


def validate_skill_packages(root: Path, contracts: dict[str, object]) -> list[str]:
    errors = _validate_package_roots(root / "skills", contracts)
    errors.extend(_validate_project_discovery(root, contracts))
    errors.extend(_validate_manifest(root, contracts))
    return errors


def validate_reference_contracts(root: Path, contracts: dict[str, object]) -> list[str]:
    errors: list[str] = []
    for relative, fragments in contracts["reference_fragments"].items():
        path = root / "skills" / relative
        if not path.is_file():
            errors.append(f"missing skill reference: {relative}")
            continue
        errors.extend(_missing_fragments(path.read_text(encoding="utf-8"), fragments, relative))
    return errors


def validate_routing_scenarios(root: Path, _end_user_names: list[str]) -> list[str]:
    path = root / "skills/fpf.skill/references/routing-scenarios.json"
    try:
        fixture = json.loads(path.read_text(encoding="utf-8"))
        manifest = json.loads((root / "skills/fpf.skill/graph.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read routing scenarios: {exc}"]
    scenarios = fixture.get("scenarios", [])
    if fixture.get("schema_version") != 2 or not isinstance(scenarios, list) or not scenarios:
        return ["routing scenarios must use schema 2 and a non-empty list"]
    routable = {node["id"] for node in manifest["nodes"] if node.get("persist_report")}
    covered: set[str] = set()
    ids: list[str] = []
    errors: list[str] = []
    edges = {(item.get("from"), item.get("to")) for item in manifest.get("edges", [])}
    for scenario in scenarios:
        if not isinstance(scenario, dict):
            errors.append("routing scenario must be an object")
            continue
        ids.append(str(scenario.get("id", "")))
        sequence = scenario.get("expected_sequence", [])
        action = scenario.get("route_action")
        if not isinstance(sequence, list) or set(sequence) - routable:
            errors.append(f"invalid routing sequence: {scenario.get('id')}")
            continue
        if action == "calls" and not sequence:
            errors.append(f"empty call route: {scenario.get('id')}")
        if action in {"stop", "external_action"} and sequence:
            errors.append(f"non-empty stop route: {scenario.get('id')}")
        if scenario.get("expected_mode") == "composition":
            pairs = zip(sequence, sequence[1:])
            if len(sequence) < 2 or any(pair not in edges for pair in pairs):
                errors.append(f"illegal composed routing sequence: {scenario.get('id')}")
        covered.update(sequence)
    if len(ids) != len(set(ids)) or "" in ids:
        errors.append("routing scenario IDs must be present and unique")
    if covered != routable:
        errors.append("routing scenarios must cover every analytical FPF node")
    return errors
