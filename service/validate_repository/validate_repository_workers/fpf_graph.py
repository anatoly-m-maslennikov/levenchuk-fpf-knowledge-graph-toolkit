"""Validate the YAML FPF command graph and its cross-graph bindings."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from .fpf_profiles import validate_areas_and_profiles


SHARED_CONTRACT = "references/fpf-analysis-contract.md"
ALLOWED_RELATIONS = {
    "primary_method", "conditional_method", "result_projection",
    "routing_method", "routing_entrypoint", "profile_context",
}


def _missing(text: str, fragments: list[str], label: str) -> list[str]:
    return [f"{label} is missing contract text: {item}" for item in fragments if item not in text]


def _load(root: Path) -> tuple[dict[str, object], list[str]]:
    path = root / "skills/fpf.skill/graph.yaml"
    try:
        manifest = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return {}, [f"cannot read FPF graph manifest: {exc}"]
    if not isinstance(manifest, dict):
        return {}, ["FPF graph manifest must contain one YAML mapping"]
    catalog_relative = manifest.get("profile_catalog")
    if not isinstance(catalog_relative, str):
        return {}, ["FPF graph manifest must declare a profile catalog"]
    catalog_path = Path(catalog_relative)
    if catalog_path.is_absolute() or ".." in catalog_path.parts:
        return {}, ["FPF profile catalog path is unsafe"]
    try:
        catalog = yaml.safe_load((path.parent / catalog_path).read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return {}, [f"cannot read FPF profile catalog: {exc}"]
    if not isinstance(catalog, dict) or catalog.get("schema_version") != 1:
        return {}, ["FPF profile catalog must use schema 1"]
    manifest["task_profiles"] = catalog.get("profiles", [])
    manifest["evaluation_cases"] = catalog.get("evaluation_cases", [])
    fpf_nodes = manifest.get("fpf_nodes", {})
    if not isinstance(fpf_nodes, dict):
        return {}, ["FPF graph node catalog must be a mapping"]
    for collection in (manifest.get("nodes", []), manifest.get("task_profiles", [])):
        for item in collection if isinstance(collection, list) else []:
            if not isinstance(item, dict):
                continue
            resolved = []
            for binding in item.get("fpf_entrypoints", []):
                target = fpf_nodes.get(binding.get("id")) if isinstance(binding, dict) else None
                resolved.append({**target, **binding} if isinstance(target, dict) else binding)
            item["fpf_entrypoints"] = resolved
    return manifest, []


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


def _validate_binding(root: Path, node_id: str, binding: object) -> list[str]:
    if not isinstance(binding, dict):
        return [f"FPF graph binding is not an object: {node_id}"]
    fpf_id = binding.get("id")
    relation = binding.get("relation")
    repository_path = binding.get("repository_path")
    errors = [] if relation in ALLOWED_RELATIONS else [
        f"FPF graph binding relation is invalid: {node_id}:{relation}"
    ]
    if not isinstance(repository_path, str):
        return errors + [f"FPF graph binding path is missing: {node_id}:{fpf_id}"]
    relative = Path(repository_path)
    if relative.is_absolute() or ".." in relative.parts or relative.parts[:1] != ("FPF-Knowledge-Graph",):
        return errors + [f"FPF graph binding path is not repository-relative: {node_id}:{fpf_id}"]
    page = root / relative
    if not page.is_file():
        return errors + [f"FPF graph binding path does not exist: {node_id}:{fpf_id}"]
    declared = re.search(
        r'^fpf_id:\s*["\']?([^"\'\n]+)', page.read_text(encoding="utf-8"), re.MULTILINE
    )
    if not isinstance(fpf_id, str) or declared is None or declared.group(1).strip() != fpf_id:
        errors.append(f"FPF graph binding ID does not match page content: {node_id}:{fpf_id}")
    return errors


def _validate_node(root: Path, node: dict[str, object], analytical: set[str]) -> list[str]:
    node_id = str(node.get("id"))
    expected_prompt = "prompts/help/en/fpf-help.md" if node_id == "help" else f"prompts/fpf-{node_id}.md"
    errors = [] if node.get("prompt") == expected_prompt else [f"FPF graph prompt path mismatch: {node_id}"]
    for language, localized in node.get("localized_prompts", {}).items():
        localized_path = root / "skills/fpf.skill" / localized
        if language not in {"en", "ru"} or not localized_path.is_file():
            errors.append(f"FPF graph localized prompt is invalid: {node_id}:{language}")
    if node_id not in analytical:
        if node.get("contracts") or node.get("fpf_entrypoints"):
            errors.append(f"FPF graph ephemeral node has analytical dependencies: {node_id}")
        return errors
    if node.get("contracts") != [SHARED_CONTRACT]:
        errors.append(f"FPF graph analytical contract mismatch: {node_id}")
    bindings = node.get("fpf_entrypoints")
    if not isinstance(bindings, list) or not bindings:
        return errors + [f"FPF graph node lacks FPF entrypoints: {node_id}"]
    for binding in bindings:
        errors.extend(_validate_binding(root, node_id, binding))
    return errors


def _validate_connector(manifest: dict[str, object]) -> list[str]:
    connector = manifest.get("connector", {})
    expected_paths = {
        "reader": "scripts/read_fpf_graph.py",
        "context_builder": "scripts/prepare_fpf_context.py",
        "prompt_helper": "references/fpf-context-connector.md",
    }
    if not isinstance(connector, dict):
        return ["FPF graph connector contract is invalid"]
    errors = [] if all(connector.get(key) == value for key, value in expected_paths.items()) else [
        "FPF graph connector contract is invalid"
    ]
    expected_sections = {"problem_frame", "problem", "forces", "solution", "consequences"}
    if set(connector.get("core_sections", [])) != expected_sections:
        errors.append("FPF graph connector core sections are invalid")
    if not isinstance(connector.get("default_solution_chars"), int) or connector["default_solution_chars"] < 1000:
        errors.append("FPF graph connector solution limit is invalid")
    return errors


def _validate_header(manifest: dict[str, object], contracts: dict[str, object]) -> list[str]:
    nodes = manifest.get("nodes", [])
    expected = set(contracts["prompt_nodes"])
    node_ids = [node.get("id") for node in nodes if isinstance(node, dict)]
    errors = [] if set(node_ids) == expected and len(node_ids) == len(expected) else [
        "FPF graph nodes do not match the prompt-node contract"
    ]
    analytical = set(contracts["analytical_nodes"])
    persistent = {node.get("id") for node in nodes if isinstance(node, dict) and node.get("persist_report")}
    if persistent != analytical:
        errors.append("FPF graph persistence flags do not match the analytical-node contract")
    expected_values = {
        "fallback_node": "plan", "schema_version": 4,
        "repository_graph_root": "FPF-Knowledge-Graph",
    }
    for key, expected_value in expected_values.items():
        if manifest.get(key) != expected_value:
            errors.append(f"FPF graph {key} is invalid")
    composition = manifest.get("composition", {})
    if not isinstance(composition, dict) or composition.get("operator") != "+" or composition.get("reference") != "references/fpf-composition.md":
        errors.append("FPF graph composition contract is invalid")
    errors.extend(_validate_connector(manifest))
    return errors


def validate_fpf_manifest(root: Path, contracts: dict[str, object]) -> list[str]:
    manifest, errors = _load(root)
    if errors:
        return errors
    errors.extend(_validate_header(manifest, contracts))
    connector = manifest.get("connector", {})
    for relative in (
        connector.get("reader", ""), connector.get("context_builder", ""),
        connector.get("prompt_helper", ""),
    ):
        if not isinstance(relative, str) or not (root / "skills/fpf.skill" / relative).is_file():
            errors.append(f"FPF graph connector resource is missing: {relative}")
    skill_root = root / "skills/fpf.skill"
    for node_id in contracts["prompt_nodes"]:
        relative = "prompts/help/en/fpf-help.md" if node_id == "help" else f"prompts/fpf-{node_id}.md"
        errors.extend(_validate_prompt(skill_root / relative, node_id, contracts))
    analytical = set(contracts["analytical_nodes"])
    for node in manifest.get("nodes", []):
        if isinstance(node, dict):
            errors.extend(_validate_node(root, node, analytical))
    errors.extend(validate_areas_and_profiles(root, manifest, analytical, _validate_binding))
    return errors
