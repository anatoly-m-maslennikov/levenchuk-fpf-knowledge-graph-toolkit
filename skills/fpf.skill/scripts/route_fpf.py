#!/usr/bin/env python3
"""Resolve one $fpf invocation to a lazily loaded prompt node."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
GRAPH_PATH = SKILL_ROOT / "graph.json"
SUPPORTED_LANGUAGES = {"auto", "en", "ru"}
SCRIPT_ROOT = Path(__file__).resolve().parent
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from route_fpf_workers.composition import resolve_composition


def normalize(value: str) -> str:
    value = value.casefold().replace("-", " ").replace("_", " ")
    value = re.sub(r"[^\w\s?]", " ", value)
    return " ".join(value.split())


def strip_invocation(value: str) -> str:
    return re.sub(r"^\s*(?:\$|/)?fpf\b\s*", "", value, count=1, flags=re.IGNORECASE).strip()


def resolve_language(invocation: str, requested: str = "auto") -> tuple[str, str]:
    if requested not in SUPPORTED_LANGUAGES:
        raise ValueError(f"unsupported output language: {requested}")
    if requested != "auto":
        return requested, "explicit-or-setting"
    cyrillic_count = len(re.findall(r"[\u0400-\u04ff]", strip_invocation(invocation)))
    return ("ru", "auto-cyrillic") if cyrillic_count >= 2 else ("en", "auto-default")


def load_graph() -> dict:
    return json.loads(GRAPH_PATH.read_text(encoding="utf-8"))


def validate_graph(graph: dict) -> list[str]:
    errors: list[str] = []
    nodes = graph.get("nodes", [])
    node_ids = [node.get("id") for node in nodes]
    if graph.get("schema_version") != 2:
        errors.append("graph schema_version must be 2")
    if len(node_ids) != len(set(node_ids)):
        errors.append("node IDs must be unique")
    if graph.get("fallback_node") not in node_ids:
        errors.append("fallback_node must reference a node")
    composition = graph.get("composition", {})
    reference = composition.get("reference", "") if isinstance(composition, dict) else ""
    if not isinstance(composition, dict) or composition.get("operator") != "+" or not (SKILL_ROOT / reference).is_file():
        errors.append("composition must declare + and an existing reference")

    seen_aliases: dict[str, str] = {}
    for node in nodes:
        node_id = node.get("id", "<missing>")
        prompt = node.get("prompt", "")
        if not prompt or not (SKILL_ROOT / prompt).is_file():
            errors.append(f"{node_id}: prompt does not exist: {prompt}")
        localized_prompts = node.get("localized_prompts", {})
        if not isinstance(localized_prompts, dict):
            errors.append(f"{node_id}: localized_prompts must be an object")
        else:
            for language, localized_prompt in localized_prompts.items():
                if language not in SUPPORTED_LANGUAGES - {"auto"}:
                    errors.append(f"{node_id}: unsupported localized prompt language: {language}")
                if not localized_prompt or not (SKILL_ROOT / localized_prompt).is_file():
                    errors.append(f"{node_id}: localized prompt does not exist: {localized_prompt}")
        aliases = [node.get("command", ""), *node.get("aliases", [])]
        localized_commands = node.get("localized_commands", {})
        if not isinstance(localized_commands, dict) or set(localized_commands) != {"ru"}:
            errors.append(f"{node_id}: localized_commands must declare exactly ru")
        elif normalize(localized_commands["ru"]) not in {normalize(alias) for alias in aliases}:
            errors.append(f"{node_id}: Russian localized command must be an exact alias")
        for alias in aliases:
            key = normalize(alias)
            if not key:
                errors.append(f"{node_id}: empty command or alias")
            elif key in seen_aliases:
                errors.append(f"alias {alias!r} is shared by {seen_aliases[key]} and {node_id}")
            else:
                seen_aliases[key] = node_id

    persistent = {node["id"] for node in nodes if node.get("persist_report")}
    expected_persistent = {
        "applicability-scan",
        "sota-harvest",
        "options-explore",
        "design-challenge",
        "decision-synthesize",
        "quality-improve",
        "alignment-audit",
    }
    if persistent != expected_persistent:
        errors.append("exactly the seven analytical nodes must persist reports")
    for ephemeral in ("help", "plan"):
        node = next((item for item in nodes if item.get("id") == ephemeral), None)
        if not node or node.get("persist_report"):
            errors.append(f"{ephemeral} must exist and remain ephemeral")

    for edge in graph.get("edges", []):
        if edge.get("from") not in node_ids or edge.get("to") not in node_ids:
            errors.append(f"edge references an unknown node: {edge}")

    scenarios_path = SKILL_ROOT / "references/routing-scenarios.json"
    try:
        fixture = json.loads(scenarios_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read routing scenarios: {exc}")
    else:
        scenarios = fixture.get("scenarios", [])
        covered: set[str] = set()
        for scenario in scenarios if isinstance(scenarios, list) else []:
            sequence = scenario.get("expected_sequence", []) if isinstance(scenario, dict) else []
            if not isinstance(sequence, list) or set(sequence) - expected_persistent:
                errors.append(f"invalid routing scenario sequence: {scenario}")
            else:
                covered.update(sequence)
        if fixture.get("schema_version") != 2 or not scenarios:
            errors.append("routing scenarios must use schema 2 and a non-empty list")
        if covered != expected_persistent:
            errors.append("routing scenarios must cover all analytical nodes")

    help_text = (SKILL_ROOT / "prompts/help.en.md").read_text(encoding="utf-8")
    help_ru_text = (SKILL_ROOT / "prompts/help.ru.md").read_text(encoding="utf-8")
    for node in nodes:
        if f"$fpf {node['command']}" not in help_text:
            errors.append(f"help page omits $fpf {node['command']}")
        localized_command = node.get("localized_commands", {}).get("ru", "")
        if localized_command and f"$fpf {localized_command}" not in help_ru_text:
            errors.append(f"Russian help page omits $fpf {localized_command}")
    return errors


def resolve(invocation: str, graph: dict, language: str = "auto") -> dict:
    resolved_language, language_selected_by = resolve_language(invocation, language)
    task = strip_invocation(invocation)
    composition = resolve_composition(task, graph)
    if composition is not None:
        composition["language"] = resolved_language
        composition["language_selected_by"] = language_selected_by
        return composition
    normalized_task = normalize(task)
    nodes = graph["nodes"]

    if not normalized_task:
        node = next(item for item in nodes if item["id"] == "help")
        return result(node, "", "empty-invocation", 0, resolved_language, language_selected_by)

    exact_candidates: list[tuple[int, dict, str]] = []
    for node in nodes:
        for alias in [node["command"], *node.get("aliases", [])]:
            normalized_alias = normalize(alias)
            if normalized_task == normalized_alias or normalized_task.startswith(normalized_alias + " "):
                exact_candidates.append((len(normalized_alias), node, normalized_alias))
    if exact_candidates:
        _, node, alias = max(exact_candidates, key=lambda item: item[0])
        residual_words = task.split()
        alias_words = len(alias.split())
        residual = " ".join(residual_words[alias_words:]).strip()
        return result(node, residual, "exact-command", 100, resolved_language, language_selected_by)

    scores: list[tuple[int, dict]] = []
    for node in nodes:
        if node.get("exact_only"):
            continue
        score = 0
        for keyword in node.get("keywords", []):
            normalized_keyword = normalize(keyword)
            if normalized_keyword and normalized_keyword in normalized_task:
                score += 3 if " " in normalized_keyword else 1
        scores.append((score, node))

    best_score = max(score for score, _ in scores)
    best_nodes = [node for score, node in scores if score == best_score and score > 0]
    if len(best_nodes) == 1:
        return result(best_nodes[0], task, "keyword-score", best_score, resolved_language, language_selected_by)

    fallback = next(item for item in nodes if item["id"] == graph["fallback_node"])
    selected_by = "ambiguous-fallback" if best_nodes else "unmatched-fallback"
    return result(fallback, task, selected_by, best_score, resolved_language, language_selected_by)


def result(
    node: dict, task: str, selected_by: str, score: int,
    language: str, language_selected_by: str,
) -> dict:
    return {
        "node": node["id"],
        "command": f"$fpf {node['command']}",
        "prompt": node.get("localized_prompts", {}).get(language, node["prompt"]),
        "persist_report": node["persist_report"],
        "task": task,
        "selected_by": selected_by,
        "score": score,
        "language": language,
        "language_selected_by": language_selected_by,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("invocation", nargs="*", help="FPF invocation to resolve")
    parser.add_argument("--text", help="FPF invocation as one string")
    parser.add_argument(
        "--language", choices=sorted(SUPPORTED_LANGUAGES), default="auto",
        help="output language override; auto detects meaningful Cyrillic text",
    )
    parser.add_argument("--check", action="store_true", help="validate graph and resources")
    args = parser.parse_args()

    graph = load_graph()
    errors = validate_graph(graph)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    if args.check:
        print(json.dumps({"nodes": len(graph["nodes"]), "edges": len(graph["edges"]), "status": "ok"}))
        return 0

    invocation = args.text if args.text is not None else " ".join(args.invocation)
    print(json.dumps(resolve(invocation, graph, args.language), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
