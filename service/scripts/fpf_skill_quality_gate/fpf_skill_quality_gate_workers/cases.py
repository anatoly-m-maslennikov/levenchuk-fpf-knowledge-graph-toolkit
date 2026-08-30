"""Load and identify the complete live semantic evaluation surface."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from service.scripts.validate_repository.validate_repository_workers.fpf_markdown import (
    load_markdown_graph,
)


ASSET_NAMES = (
    "cases.json", "subject-prompt.md", "evaluator-prompt.md",
    "subject-output.schema.json", "evaluation-output.schema.json",
)


OUTPUT_CONTRACTS = {"help", "plan", "analysis"}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read JSON asset {path}: {exc}") from exc


def load_cases(path: Path) -> list[dict[str, object]]:
    value = load_json(path)
    if not isinstance(value, list) or not value:
        raise ValueError("quality-gate cases must be a non-empty JSON list")
    ids = [case.get("id") for case in value if isinstance(case, dict)]
    if len(ids) != len(value) or not all(isinstance(item, str) and item for item in ids):
        raise ValueError("every quality-gate case must have a non-empty string id")
    if len(ids) != len(set(ids)):
        raise ValueError("quality-gate case ids must be unique")
    for case in value:
        output_contract = case.get("output_contract")
        if output_contract not in OUTPUT_CONTRACTS:
            raise ValueError(
                f"quality-gate case has invalid output contract: {case['id']}"
            )
        criteria = case.get("criteria")
        if not isinstance(criteria, list) or not criteria:
            raise ValueError(f"quality-gate case has no criteria: {case['id']}")
        criterion_ids = [item.get("id") for item in criteria if isinstance(item, dict)]
        if len(criterion_ids) != len(criteria) or len(criterion_ids) != len(set(criterion_ids)):
            raise ValueError(f"quality-gate criterion ids are invalid: {case['id']}")
    return value


def load_profile_cases(root: Path) -> list[dict[str, object]]:
    graph = load_markdown_graph(root)
    nodes = {str(node["id"]): node for node in graph["nodes"]}
    profiles = {str(profile["id"]): profile for profile in graph["task_profiles"]}
    results: list[dict[str, object]] = []
    for source in graph["evaluation_cases"]:
        profile_id = str(source["profile"])
        profile = profiles[profile_id]
        node_id = str(source["node"])
        facets = ", ".join(str(item) for item in source["required_facets"])
        results.append({
            "id": f"profile-{profile_id.replace('.', '-')}",
            "area": profile["area"], "output_contract": "analysis",
            "invocation": (
                f"$fpf {nodes[node_id]['command']} {source['task']} Do not save a report."
            ),
            "criteria": [
                {"id": "profile-selection", "requirement": f"Selects task profile {profile_id} without changing the explicit {node_id} analytical intent."},
                {"id": "required-facets", "requirement": f"Materially addresses all profile case facets: {facets}."},
                {"id": "forbidden-inference", "requirement": f"Does not make this forbidden inference: {source['forbidden_inference']}"},
                {"id": "bounded-grounding", "requirement": "Uses only the selected node and profile FPF bindings and returns the complete analytical output contract without saving."},
            ],
        })
    return results


def skill_tree_sha256(skill_root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(skill_root.rglob("*"), key=lambda item: item.relative_to(skill_root).as_posix()):
        relative = path.relative_to(skill_root)
        if path.is_dir() or "__pycache__" in relative.parts:
            continue
        if path.name == ".fpf-runtime.toml" or path.suffix in {".pyc", ".pyo"}:
            continue
        digest.update(relative.as_posix().encode("utf-8") + b"\0")
        digest.update(path.read_bytes() + b"\0")
    return digest.hexdigest()


def gate_identity(root: Path, assets: Path) -> dict[str, object]:
    return {
        "skill_tree_sha256": skill_tree_sha256(root / "skills" / "fpf.skill"),
        "assets": {name: sha256_file(assets / name) for name in ASSET_NAMES},
    }
