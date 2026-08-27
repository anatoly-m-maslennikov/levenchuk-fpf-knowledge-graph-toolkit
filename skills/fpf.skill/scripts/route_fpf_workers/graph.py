"""Read the YAML command/profile graph and expose minimal selected views."""

from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ModuleNotFoundError as exc:  # pragma: no cover - runtime dependency error
    raise SystemExit(
        "PyYAML is required to read graph.yaml; run through the repository uv project"
    ) from exc


def load_graph(skill_root: Path) -> dict[str, object]:
    graph = yaml.safe_load((skill_root / "graph.yaml").read_text(encoding="utf-8"))
    if not isinstance(graph, dict):
        raise ValueError("graph.yaml must contain one mapping")
    catalog_path = graph.get("profile_catalog")
    if not isinstance(catalog_path, str) or Path(catalog_path).is_absolute() or ".." in Path(catalog_path).parts:
        raise ValueError("graph.yaml must declare one safe profile_catalog path")
    catalog = yaml.safe_load((skill_root / catalog_path).read_text(encoding="utf-8"))
    if not isinstance(catalog, dict) or catalog.get("schema_version") != 1:
        raise ValueError("profile catalog must use schema 1")
    graph["task_profiles"] = catalog.get("profiles", [])
    graph["evaluation_cases"] = catalog.get("evaluation_cases", [])
    _resolve_all_bindings(graph)
    return graph


def _resolve_binding(graph: dict[str, object], binding: dict[str, object]) -> dict[str, object]:
    fpf_id = binding.get("id")
    catalog = graph.get("fpf_nodes", {})
    target = catalog.get(fpf_id) if isinstance(catalog, dict) else None
    if not isinstance(target, dict) or not isinstance(target.get("repository_path"), str):
        raise ValueError(f"unknown FPF graph node reference: {fpf_id}")
    return {**target, **binding}


def _resolve_all_bindings(graph: dict[str, object]) -> None:
    for collection in (graph.get("nodes", []), graph.get("task_profiles", [])):
        for item in collection if isinstance(collection, list) else []:
            if not isinstance(item, dict):
                continue
            bindings = item.get("fpf_entrypoints", [])
            if not isinstance(bindings, list):
                continue
            item["fpf_entrypoints"] = [
                _resolve_binding(graph, binding) if isinstance(binding, dict) else binding
                for binding in bindings
            ]


def selected_nodes(graph: dict[str, object], node_ids: list[str]) -> list[dict[str, object]]:
    by_id = {node["id"]: node for node in graph.get("nodes", []) if isinstance(node, dict)}
    missing = [node_id for node_id in node_ids if node_id not in by_id]
    if missing:
        raise ValueError(f"unknown FPF command node: {missing[0]}")
    return [by_id[node_id] for node_id in node_ids]


def selected_profiles(
    graph: dict[str, object], profile_ids: list[str],
) -> list[dict[str, object]]:
    by_id = {
        profile["id"]: profile
        for profile in graph.get("task_profiles", []) if isinstance(profile, dict)
    }
    missing = [profile_id for profile_id in profile_ids if profile_id not in by_id]
    if missing:
        raise ValueError(f"unknown FPF task profile: {missing[0]}")
    return [by_id[profile_id] for profile_id in profile_ids]


def node_view(node: dict[str, object]) -> dict[str, object]:
    keys = (
        "id", "command", "description", "prompt", "localized_prompts",
        "persist_report", "contracts", "fpf_entrypoints",
    )
    return {key: node[key] for key in keys if key in node}


def profile_view(profile: dict[str, object]) -> dict[str, object]:
    keys = ("id", "area", "title", "description", "fpf_entrypoints")
    return {key: profile[key] for key in keys if key in profile}


def graph_view(
    graph: dict[str, object], node_ids: list[str], profile_ids: list[str] | None = None,
) -> dict[str, object]:
    nodes = selected_nodes(graph, node_ids)
    profiles = selected_profiles(graph, profile_ids or [])
    selected = set(node_ids)
    edges = [
        edge for edge in graph.get("edges", [])
        if edge.get("from") in selected and edge.get("to") in selected
    ]
    return {
        "schema_version": graph.get("schema_version"),
        "repository_graph_root": graph.get("repository_graph_root"),
        "connector": graph.get("connector"),
        "nodes": [node_view(node) for node in nodes],
        "task_profiles": [profile_view(profile) for profile in profiles],
        "edges": edges,
    }
