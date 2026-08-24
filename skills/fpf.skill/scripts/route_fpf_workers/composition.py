"""Resolve explicit ordered compositions of exact FPF commands."""

from __future__ import annotations

import re


OPERATOR_RE = re.compile(r"\s+\+\s+")


def _normalize(value: str) -> str:
    value = value.casefold().replace("-", " ").replace("_", " ")
    value = re.sub(r"[^\w\s?]", " ", value)
    return " ".join(value.split())


def _match(segment: str, nodes: list[dict]) -> tuple[dict, str] | None:
    normalized = _normalize(segment)
    candidates: list[tuple[int, dict, str]] = []
    for node in nodes:
        for alias in [node["command"], *node.get("aliases", [])]:
            key = _normalize(alias)
            if normalized == key or normalized.startswith(key + " "):
                candidates.append((len(key), node, key))
    if not candidates:
        return None
    _, node, alias = max(candidates, key=lambda item: item[0])
    residual = " ".join(segment.split()[len(alias.split()):]).strip()
    return node, residual


def _node_result(node: dict) -> dict[str, object]:
    return dict(
        node=node["id"], command=f"$fpf {node['command']}",
        prompt=node["prompt"], persist_report=node["persist_report"],
    )


def _invalid(graph: dict, task: str, message: str) -> dict[str, object]:
    fallback = next(item for item in graph["nodes"] if item["id"] == graph["fallback_node"])
    return dict(
        **_node_result(fallback), task=task,
        selected_by="invalid-composition-fallback", score=0,
        composition_error=message,
    )


def _validate_steps(graph: dict, matches: list[tuple[dict, str]], task: str):
    nodes = [item[0] for item in matches]
    if any(not node.get("persist_report") for node in nodes):
        return _invalid(graph, task, "only analytical commands can be composed")
    for index, (_, residual) in enumerate(matches[:-1]):
        if residual:
            return _invalid(
                graph, task,
                f"task text is allowed only after the last command (segment {index + 1})",
            )
    legal = {(edge["from"], edge["to"]) for edge in graph.get("edges", [])}
    pairs = [(left["id"], right["id"]) for left, right in zip(nodes, nodes[1:])]
    invalid = next((pair for pair in pairs if pair not in legal), None)
    if invalid:
        return _invalid(graph, task, f"illegal composition handoff: {invalid[0]} -> {invalid[1]}")
    return None


def resolve_composition(task: str, graph: dict) -> dict[str, object] | None:
    if not OPERATOR_RE.search(task):
        return None
    segments = OPERATOR_RE.split(task)
    if len(segments) < 2 or any(not item.strip() for item in segments):
        return _invalid(graph, task, "composition contains an empty command")
    matches: list[tuple[dict, str]] = []
    for index, segment in enumerate(segments):
        match = _match(segment.strip(), graph["nodes"])
        if match is None:
            return _invalid(graph, task, f"segment {index + 1} is not an exact FPF command or alias")
        matches.append(match)
    error = _validate_steps(graph, matches, task)
    if error:
        return error
    steps = [_node_result(node) for node, _ in matches]
    return dict(
        mode="composition", nodes=steps,
        commands=[item["command"] for item in steps],
        persist_report=True, task=matches[-1][1],
        selected_by="explicit-composition", score=100,
    )
