"""Validate the portable FPF graph skill and its routing fixtures."""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

from .fpf_graph import validate_fpf_manifest
from .skill_entry import validate_fpf_skill_package

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


def _package_set(root: Path) -> set[str]:
    return {
        path.name for path in root.glob("*.skill")
        if path.is_dir() and (path / "SKILL.md").is_file()
    }


def _validate_named_package(
    path: Path, name: str, contracts: dict[str, object], service_names: list[str],
) -> list[str]:
    if not path.is_file():
        return [f"missing skill package: {name}"]
    errors = _validate_frontmatter(path, name)
    fragments = (
        contracts["service_skill_fragments"][name]
        if name in service_names else contracts["fpf_skill_fragments"]
    )
    text = path.read_text(encoding="utf-8")
    errors.extend(_missing_fragments(text, fragments, name))
    if name == "fpf":
        errors.extend(validate_fpf_skill_package(path.parent, text, contracts))
    return errors


def _validate_package_roots(skills_root: Path, contracts: dict[str, object]) -> list[str]:
    end_user_names = list(contracts["end_user_skills"])
    service_names = list(contracts["service_skills"])
    service_root = skills_root.parent / "service/skills"
    expected_end_user = {f"{name}.skill" for name in end_user_names}
    expected_service = {f"{name}.skill" for name in service_names}
    errors = [] if _package_set(skills_root) == expected_end_user else ["end-user skill package set does not match the contract asset"]
    if _package_set(service_root) != expected_service:
        errors.append("service skill package set does not match the contract asset")

    for name in end_user_names + service_names:
        package_root = service_root if name in service_names else skills_root
        path = package_root / f"{name}.skill" / "SKILL.md"
        errors.extend(_validate_named_package(path, name, contracts, service_names))

    errors.extend(_validate_skill_readmes(skills_root, end_user_names, service_names))
    return errors


def _validate_skill_readmes(
    skills_root: Path, end_user_names: list[str], service_names: list[str],
) -> list[str]:
    readme = (skills_root / "README.md").read_text(encoding="utf-8")
    errors = [
        f"skills README omits {name}.skill"
        for name in end_user_names if f"`{name}.skill`" not in readme
    ]
    service_readme = (skills_root.parent / "service/skills/README.md").read_text(encoding="utf-8")
    errors.extend(f"service README omits {name}.skill" for name in service_names if f"`{name}.skill`" not in service_readme)
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
        expected = (root / "service/skills" / f"{name}.skill").resolve()
        if not link.is_symlink() or link.resolve() != expected:
            errors.append(f"project service skill link is invalid: {name}")
    return errors


def validate_skill_packages(root: Path, contracts: dict[str, object]) -> list[str]:
    errors = _validate_package_roots(root / "skills", contracts)
    errors.extend(_validate_project_discovery(root, contracts))
    errors.extend(validate_fpf_manifest(root, contracts))
    return errors


def validate_reference_contracts(root: Path, contracts: dict[str, object]) -> list[str]:
    errors: list[str] = []
    for relative, fragments in contracts["reference_fragments"].items():
        path = root / relative
        if not path.is_file():
            errors.append(f"missing skill reference: {relative}")
            continue
        errors.extend(_missing_fragments(path.read_text(encoding="utf-8"), fragments, relative))
    return errors


def _validate_scenario(
    scenario: object, routable: set[str], edges: set[tuple[object, object]],
) -> tuple[list[str], str, list[str]]:
    if not isinstance(scenario, dict):
        return ["routing scenario must be an object"], "", []
    scenario_id = str(scenario.get("id", ""))
    sequence = scenario.get("expected_sequence", [])
    if not isinstance(sequence, list) or set(sequence) - routable:
        return [f"invalid routing sequence: {scenario_id}"], scenario_id, []
    errors: list[str] = []
    action = scenario.get("route_action")
    expected_mode = scenario.get("expected_mode")
    if action == "calls" and not sequence:
        errors.append(f"empty call route: {scenario_id}")
    if action in {"stop", "external_action"} and sequence:
        errors.append(f"non-empty stop route: {scenario_id}")
    if expected_mode not in {None, "composition", "plan", "closure", "full"}:
        errors.append(f"invalid expected routing mode: {scenario_id}")
    if expected_mode in {"composition", "plan"}:
        pairs = zip(sequence, sequence[1:])
        if len(sequence) < 2 or any(pair not in edges for pair in pairs):
            errors.append(f"illegal stacked routing sequence: {scenario_id}")
    if expected_mode == "plan" and action != "calls":
        errors.append(f"meta-plan routing scenario must return calls: {scenario_id}")
    return errors, scenario_id, sequence


def validate_routing_scenarios(root: Path, _end_user_names: list[str]) -> list[str]:
    path = root / "skills/fpf.skill/references/routing-scenarios.json"
    try:
        fixture = json.loads(path.read_text(encoding="utf-8"))
        manifest = yaml.safe_load((root / "skills/fpf.skill/graph.yaml").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, yaml.YAMLError) as exc:
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
        scenario_errors, scenario_id, sequence = _validate_scenario(scenario, routable, edges)
        errors.extend(scenario_errors)
        ids.append(scenario_id)
        covered.update(sequence)
    if len(ids) != len(set(ids)) or "" in ids:
        errors.append("routing scenario IDs must be present and unique")
    if covered != routable:
        errors.append("routing scenarios must cover every analytical FPF node")
    return errors
