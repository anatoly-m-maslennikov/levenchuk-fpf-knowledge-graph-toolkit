"""Resolve explicit ordered compositions of exact FPF commands."""

from __future__ import annotations

import re
from difflib import SequenceMatcher


OPERATOR_RE = re.compile(r"\s+\+\s+")
MIN_SUGGESTION_RATIO = 0.72
MIN_FIRST_WORD_RATIO = 0.60


def _normalize(value: str) -> str:
    value = value.casefold().replace("-", " ").replace("_", " ")
    value = re.sub(r"[^\w\s?]", " ", value)
    return " ".join(value.split())


def _residual_after_alias(segment: str, alias: str) -> str | None:
    transformed = segment.casefold().replace("-", " ").replace("_", " ")
    matches = list(re.finditer(r"\w+", transformed))
    alias_words = _normalize(alias).split()
    if not alias_words or len(matches) < len(alias_words):
        return None
    if [item.group(0) for item in matches[:len(alias_words)]] != alias_words:
        return None
    return segment[matches[len(alias_words) - 1].end():].strip()


def _match(segment: str, nodes: list[dict]) -> tuple[dict, str] | None:
    normalized = _normalize(segment)
    candidates: list[tuple[int, dict, str]] = []
    for node in nodes:
        for alias in [node["command"], *node.get("aliases", [])]:
            key = _normalize(alias)
            residual = _residual_after_alias(segment, alias)
            if residual is not None:
                candidates.append((len(key), node, residual))
    if not candidates:
        return None
    _, node, residual = max(candidates, key=lambda item: item[0])
    return node, residual


def _node_result(node: dict) -> dict[str, object]:
    return dict(
        node=node["id"], command=f"$fpf {node['command']}",
        prompt=node["prompt"], persist_report=node["persist_report"],
        contracts=node.get("contracts", []),
        fpf_entrypoints=node.get("fpf_entrypoints", []),
    )


def command_suggestions(
    text: str, nodes: list[dict], *, limit: int = 3,
) -> list[dict[str, object]]:
    """Return deterministic command corrections without selecting a node."""
    normalized = _normalize(text)
    words = normalized.split()
    if not words:
        return []

    for node in nodes:
        for alias in [node["command"], *node.get("aliases", [])]:
            key_words = _normalize(alias).split()
            if not key_words or len(words) < len(key_words):
                continue
            if words[:len(key_words)] == key_words and (len(key_words) > 1 or len(words) == 1):
                return []

    best_by_node: dict[str, tuple[float, str]] = {}
    for node in nodes:
        for alias in [node["command"], *node.get("aliases", [])]:
            key = _normalize(alias)
            alias_words = key.split()
            if not alias_words:
                continue
            if len(alias_words) == 1 and len(words) != 1:
                continue
            first_ratio = SequenceMatcher(None, words[0], alias_words[0]).ratio()
            if words[0] != alias_words[0] and first_ratio < MIN_FIRST_WORD_RATIO:
                continue
            if len(alias_words) > 1 and len(words) > 1:
                second_ratio = SequenceMatcher(None, words[1], alias_words[1]).ratio()
                if words[1] != alias_words[1] and second_ratio < MIN_FIRST_WORD_RATIO:
                    continue
            lengths = range(
                max(1, len(alias_words) - 1),
                min(len(words), len(alias_words) + 1) + 1,
            )
            candidates = [" ".join(words[:length]) for length in lengths]
            if not candidates:
                continue
            if key in candidates:
                continue
            ratio = max(SequenceMatcher(None, candidate, key).ratio() for candidate in candidates)
            if ratio < MIN_SUGGESTION_RATIO or normalized == key:
                continue
            previous = best_by_node.get(node["id"])
            if previous is None or ratio > previous[0]:
                best_by_node[node["id"]] = (ratio, key)

    ranked = sorted(
        (
            (ratio, node_id, alias)
            for node_id, (ratio, alias) in best_by_node.items()
        ),
        key=lambda item: (-item[0], item[1]),
    )[:limit]
    nodes_by_id = {node["id"]: node for node in nodes}
    return [
        {
            "node": node_id,
            "command": f"$fpf {nodes_by_id[node_id]['command']}",
            "matched_alias": alias,
            "similarity": round(ratio, 3),
        }
        for ratio, node_id, alias in ranked
    ]


def _invalid(
    graph: dict, task: str, message: str,
    suggestions: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    fallback = next(item for item in graph["nodes"] if item["id"] == graph["fallback_node"])
    invalid = dict(
        **_node_result(fallback), task=task,
        selected_by="invalid-composition-fallback", score=0,
        composition_error=message, execution_disabled=True,
    )
    if suggestions:
        invalid["suggestions"] = suggestions
    return invalid


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
    first_match = _match(segments[0].strip(), graph["nodes"])
    if first_match is None:
        return None
    if first_match[1] and not any(
        _match(segment.strip(), graph["nodes"]) is not None
        for segment in segments[1:]
    ):
        return None
    matches: list[tuple[dict, str]] = []
    for index, segment in enumerate(segments):
        suggestions = command_suggestions(segment.strip(), graph["nodes"])
        if suggestions:
            return _invalid(
                graph, task,
                f"segment {index + 1} is not an exact FPF command or alias",
                suggestions,
            )
        match = _match(segment.strip(), graph["nodes"])
        if match is None:
            return _invalid(
                graph, task,
                f"segment {index + 1} is not an exact FPF command or alias",
            )
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


def resolve_meta_plan(task: str, graph: dict) -> dict[str, object] | None:
    """Resolve ``plan <command> + <command>`` without executing the stack."""
    plan = next(item for item in graph["nodes"] if item["id"] == "plan")
    plan_match = _match(task, [plan])
    if plan_match is None:
        return None
    _, proposed = plan_match
    if not OPERATOR_RE.search(proposed):
        return None

    planned = resolve_composition(proposed, graph)
    if planned is None:
        return None
    if planned.get("mode") != "composition":
        planned["selected_by"] = "invalid-meta-plan"
        planned["meta_plan"] = True
        planned["execution_disabled"] = True
        return planned

    return dict(
        **_node_result(plan), mode="plan",
        task=planned["task"], selected_by="explicit-meta-plan", score=100,
        planned_nodes=planned["nodes"], planned_commands=planned["commands"],
        meta_plan=True, execution_disabled=True,
    )
