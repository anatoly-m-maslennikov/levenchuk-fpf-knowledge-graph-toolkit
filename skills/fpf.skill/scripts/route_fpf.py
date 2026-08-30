#!/usr/bin/env python3
"""Resolve one $fpf invocation to a lazily loaded prompt node."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).absolute().parent.parent
GRAPH_PATH = SKILL_ROOT / "graph.yaml"
SUPPORTED_LANGUAGES = {"auto", "en", "ru"}
SCRIPT_ROOT = Path(__file__).absolute().parent
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))
previous_bytecode_policy = sys.dont_write_bytecode
sys.dont_write_bytecode = True
from fpf_runtime_cache import configure_runtime_cache
configure_runtime_cache(SKILL_ROOT)
sys.dont_write_bytecode = previous_bytecode_policy

from route_fpf_workers.composition import (
    command_suggestions,
    resolve_composition,
    resolve_meta_plan,
)
from route_fpf_workers.graph import load_graph as read_graph


def normalize(value: str) -> str:
    value = value.casefold().replace("-", " ").replace("_", " ")
    value = re.sub(r"[^\w\s?]", " ", value)
    return " ".join(value.split())


def _tokens(value: str) -> list[str]:
    """Return normalized word tokens without allowing substring matches."""
    return re.findall(r"\w+", value.casefold().replace("-", " ").replace("_", " "))


def _contains_key(text: str, key: str) -> bool:
    """Match complete tokens; Russian stem keywords may match token prefixes."""
    text_tokens = _tokens(text)
    key_tokens = _tokens(key)
    if not key_tokens or len(key_tokens) > len(text_tokens):
        return False
    for start in range(len(text_tokens) - len(key_tokens) + 1):
        candidate = text_tokens[start:start + len(key_tokens)]
        if candidate == key_tokens:
            return True
        if (
            len(key_tokens) == 1
            and len(key_tokens[0]) >= 4
            and re.search(r"[\u0400-\u04ff]", key_tokens[0])
            and candidate[0].startswith(key_tokens[0])
        ):
            return True
    return False


def _command_residual(text: str, alias: str) -> str | None:
    """Return text after an alias matched by normalized token span."""
    transformed = text.casefold().replace("-", " ").replace("_", " ")
    matches = list(re.finditer(r"\w+", transformed))
    alias_tokens = _tokens(alias)
    if not alias_tokens or [item.group(0) for item in matches[:len(alias_tokens)]] != alias_tokens:
        return None
    if len(matches) < len(alias_tokens):
        return None
    return text[matches[len(alias_tokens) - 1].end():].strip()


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
    return read_graph(SKILL_ROOT)


def resolve_task_profile(text: str, graph: dict) -> dict | None:
    """Resolve an orthogonal task profile without deciding analytical intent."""
    normalized_text = normalize(text)
    if not normalized_text:
        return None
    scores: list[tuple[int, dict]] = []
    for profile in graph.get("task_profiles", []):
        score = 0
        for alias in profile.get("aliases", []):
            key = normalize(alias)
            if not key:
                continue
            if normalized_text == key:
                score += 10
            elif _contains_key(text, alias):
                score += 6 if " " in key else 4
        for keyword in profile.get("keywords", []):
            key = normalize(keyword)
            if key and _contains_key(text, keyword):
                score += 3 if " " in key else 1
        scores.append((score, profile))
    best = max((score for score, _ in scores), default=0)
    matches = [profile for score, profile in scores if score == best and score > 0]
    return matches[0] if len(matches) == 1 else None


def attach_task_profile(payload: dict, text: str, graph: dict) -> dict:
    profile = resolve_task_profile(text, graph)
    if profile is not None:
        payload["task_profile"] = {
            key: profile[key]
            for key in ("id", "area", "title", "description", "fpf_entrypoints")
        }
    return payload


def resolve_help_area(
    task: str, graph: dict, language: str, language_selected_by: str,
) -> dict | None:
    normalized_task = normalize(task)
    help_node = next(item for item in graph["nodes"] if item["id"] == "help")
    help_aliases = [help_node["command"], *help_node.get("aliases", [])]
    candidates = sorted(
        (normalize(alias) for alias in help_aliases), key=len, reverse=True
    )
    matched = next(
        (alias for alias in candidates if normalized_task.startswith(alias + " ")), None
    )
    if matched is None:
        return None
    residual = " ".join(normalized_task.split()[len(matched.split()):])
    for area in graph.get("areas", []):
        if residual in {normalize(alias) for alias in area.get("aliases", [])}:
            page = result(
                help_node, "", "exact-help-area", 100, language,
                language_selected_by,
            )
            page["prompt"] = area["help_prompts"][language]
            page["help_area"] = area["id"]
            return page
    page = result(
        help_node, residual, "unknown-help-area", 0, language,
        language_selected_by,
    )
    page["available_help_areas"] = [area["id"] for area in graph.get("areas", [])]
    return page


def validate_graph(graph: dict) -> list[str]:
    errors: list[str] = []
    nodes = graph.get("nodes", [])
    node_ids = [node.get("id") for node in nodes]
    if graph.get("schema_version") != 4:
        errors.append("graph schema_version must be 4")
    graph_root = graph.get("repository_graph_root")
    if graph_root != "FPF-Knowledge-Graph":
        errors.append("repository_graph_root must be FPF-Knowledge-Graph")
    if len(node_ids) != len(set(node_ids)):
        errors.append("node IDs must be unique")
    if graph.get("fallback_node") not in node_ids:
        errors.append("fallback_node must reference a node")
    composition = graph.get("composition", {})
    reference = composition.get("reference", "") if isinstance(composition, dict) else ""
    if not isinstance(composition, dict) or composition.get("operator") != "+" or not (SKILL_ROOT / reference).is_file():
        errors.append("composition must declare + and an existing reference")
    connector = graph.get("connector", {})
    connector_paths = ("reader", "context_builder", "prompt_helper", "report_planner")
    if not isinstance(connector, dict):
        errors.append("connector must be an object")
    else:
        for key in connector_paths:
            relative = connector.get(key, "")
            if not isinstance(relative, str) or not (SKILL_ROOT / relative).is_file():
                errors.append(f"connector {key} does not exist: {relative}")
        expected_sections = {"problem_frame", "problem", "forces", "solution", "consequences"}
        if set(connector.get("core_sections", [])) != expected_sections:
            errors.append("connector core_sections must declare the five pattern sections")
        if not isinstance(connector.get("default_solution_chars"), int) or connector["default_solution_chars"] < 1000:
            errors.append("connector default_solution_chars must be an integer >= 1000")

    areas = graph.get("areas", [])
    area_ids = [area.get("id") for area in areas if isinstance(area, dict)]
    if set(area_ids) != {"framework", "software", "skills"} or len(area_ids) != 3:
        errors.append("help areas must be exactly framework, software, and skills")
    for area in areas if isinstance(areas, list) else []:
        prompts = area.get("help_prompts", {}) if isinstance(area, dict) else {}
        if set(prompts) != {"en", "ru"}:
            errors.append(f"{area.get('id')}: help prompts must declare en and ru")
        for prompt in prompts.values() if isinstance(prompts, dict) else []:
            if not isinstance(prompt, str) or not (SKILL_ROOT / prompt).is_file():
                errors.append(f"{area.get('id')}: help prompt does not exist: {prompt}")

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
        "problem-frame", "structure-recover", "applicability-scan",
        "sota-harvest",
        "options-explore", "evaluation-design",
        "design-challenge",
        "decision-synthesize",
        "quality-improve",
        "alignment-audit",
    }
    if persistent != expected_persistent:
        errors.append("exactly the ten analytical nodes must persist reports")
    shared_contract = "references/fpf-analysis-contract.md"
    allowed_binding_relations = {
        "primary_method", "conditional_method", "result_projection",
        "routing_method", "routing_entrypoint", "profile_context",
    }
    for node in nodes:
        node_id = node.get("id", "<missing>")
        contracts = node.get("contracts", [])
        entrypoints = node.get("fpf_entrypoints", [])
        if node_id in expected_persistent:
            if contracts != [shared_contract]:
                errors.append(f"{node_id}: must declare the shared analytical contract")
            if not isinstance(entrypoints, list) or not entrypoints:
                errors.append(f"{node_id}: must declare at least one FPF entrypoint")
            for binding in entrypoints if isinstance(entrypoints, list) else []:
                if not isinstance(binding, dict):
                    errors.append(f"{node_id}: FPF entrypoint must be an object")
                    continue
                fpf_id = binding.get("id")
                relation = binding.get("relation")
                repository_path = binding.get("repository_path")
                if not isinstance(fpf_id, str) or not fpf_id:
                    errors.append(f"{node_id}: FPF entrypoint ID is missing")
                if relation not in allowed_binding_relations:
                    errors.append(f"{node_id}: invalid FPF entrypoint relation: {relation}")
                if (
                    not isinstance(repository_path, str)
                    or not repository_path.startswith(f"{graph_root}/")
                    or Path(repository_path).is_absolute()
                ):
                    errors.append(f"{node_id}: invalid repository-relative FPF path")
        elif contracts or entrypoints:
            errors.append(f"{node_id}: ephemeral nodes must not load analytical contracts or FPF entrypoints")
    if not (SKILL_ROOT / shared_contract).is_file():
        errors.append("shared analytical contract does not exist")
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

    profiles = graph.get("task_profiles", [])
    profile_ids = [profile.get("id") for profile in profiles if isinstance(profile, dict)]
    if len(profile_ids) < 20 or len(profile_ids) != len(set(profile_ids)):
        errors.append("task profile IDs must be unique and provide at least twenty profiles")
    for profile in profiles if isinstance(profiles, list) else []:
        profile_id = profile.get("id", "<missing>")
        if profile.get("area") not in area_ids:
            errors.append(f"{profile_id}: unknown task-profile area")
        bindings = profile.get("fpf_entrypoints", [])
        if not isinstance(bindings, list) or not bindings:
            errors.append(f"{profile_id}: task profile lacks FPF entrypoints")
        for binding in bindings if isinstance(bindings, list) else []:
            if binding.get("relation") != "profile_context":
                errors.append(f"{profile_id}: invalid task-profile relation")
            repository_path = binding.get("repository_path", "")
            if not isinstance(repository_path, str) or not repository_path.startswith(f"{graph_root}/"):
                errors.append(f"{profile_id}: unresolved task-profile FPF path")
        examples = profile.get("examples", [])
        if not isinstance(examples, list) or len(examples) < 2:
            errors.append(f"{profile_id}: task profile needs two routing examples")
        for example in examples if isinstance(examples, list) else []:
            if example.get("expected_node") not in expected_persistent or not example.get("text"):
                errors.append(f"{profile_id}: invalid generated routing example")

    evaluation_cases = graph.get("evaluation_cases", [])
    case_profiles = [
        case.get("profile") for case in evaluation_cases
        if isinstance(case, dict)
    ] if isinstance(evaluation_cases, list) else []
    case_ids = [
        case.get("id") for case in evaluation_cases
        if isinstance(case, dict)
    ] if isinstance(evaluation_cases, list) else []
    if sorted(case_profiles) != sorted(profile_ids):
        errors.append("profile catalog must declare exactly one evaluation case per profile")
    if len(case_ids) != len(set(case_ids)) or not all(case_ids):
        errors.append("profile evaluation case IDs must be unique and non-empty")
    for case in evaluation_cases if isinstance(evaluation_cases, list) else []:
        if (
            case.get("profile") not in profile_ids
            or case.get("node") not in expected_persistent
            or not case.get("required_facets")
            or not case.get("forbidden_inference")
        ):
            errors.append(f"invalid profile evaluation case: {case.get('id')}")

    help_text = (SKILL_ROOT / "prompts/help/en/fpf-help.md").read_text(encoding="utf-8")
    help_ru_text = (SKILL_ROOT / "prompts/help/ru/fpf-help.md").read_text(encoding="utf-8")
    for area in areas:
        if f"$fpf help {area['id']}" not in help_text:
            errors.append(f"general help omits area: {area['id']}")
        localized_title = area.get("localized_title", {}).get("ru", "")
        if localized_title and localized_title not in help_ru_text:
            errors.append(f"Russian general help omits area: {area['id']}")
    return errors


def resolve(invocation: str, graph: dict, language: str = "auto") -> dict:
    resolved_language, language_selected_by = resolve_language(invocation, language)
    task = strip_invocation(invocation)
    help_area = resolve_help_area(task, graph, resolved_language, language_selected_by)
    if help_area is not None:
        return help_area
    meta_plan = resolve_meta_plan(task, graph)
    if meta_plan is not None:
        meta_plan["language"] = resolved_language
        meta_plan["language_selected_by"] = language_selected_by
        return attach_task_profile(meta_plan, meta_plan.get("task", ""), graph)
    composition = resolve_composition(task, graph)
    if composition is not None:
        composition["language"] = resolved_language
        composition["language_selected_by"] = language_selected_by
        return attach_task_profile(composition, composition.get("task", ""), graph)
    normalized_task = normalize(task)
    nodes = graph["nodes"]

    if not normalized_task:
        node = next(item for item in nodes if item["id"] == "help")
        return result(node, "", "empty-invocation", 0, resolved_language, language_selected_by)

    suggestions = command_suggestions(task, nodes)
    if suggestions:
        fallback = next(item for item in nodes if item["id"] == graph["fallback_node"])
        suggested = result(
            fallback, task, "typo-suggestion-fallback", 0,
            resolved_language, language_selected_by,
        )
        suggested["suggestions"] = suggestions
        suggested["execution_disabled"] = True
        return suggested

    exact_candidates: list[tuple[int, dict, str]] = []
    for node in nodes:
        for alias in [node["command"], *node.get("aliases", [])]:
            normalized_alias = normalize(alias)
            residual = _command_residual(task, alias)
            if residual is not None:
                exact_candidates.append((len(normalized_alias), node, residual))
    if exact_candidates:
        _, node, residual = max(exact_candidates, key=lambda item: item[0])
        return attach_task_profile(
            result(node, residual, "exact-command", 100, resolved_language, language_selected_by),
            residual, graph,
        )

    scores: list[tuple[int, dict]] = []
    for node in nodes:
        if node.get("exact_only"):
            continue
        score = 0
        for keyword in node.get("keywords", []):
            normalized_keyword = normalize(keyword)
            if normalized_keyword and _contains_key(task, keyword):
                score += 3 if " " in normalized_keyword else 1
        scores.append((score, node))

    best_score = max(score for score, _ in scores)
    best_nodes = [node for score, node in scores if score == best_score and score > 0]
    if len(best_nodes) == 1:
        return attach_task_profile(
            result(best_nodes[0], task, "keyword-score", best_score, resolved_language, language_selected_by),
            task, graph,
        )

    fallback = next(item for item in nodes if item["id"] == graph["fallback_node"])
    selected_by = "ambiguous-fallback" if best_nodes else "unmatched-fallback"
    return attach_task_profile(
        result(fallback, task, selected_by, best_score, resolved_language, language_selected_by),
        task, graph,
    )


def result(
    node: dict, task: str, selected_by: str, score: int,
    language: str, language_selected_by: str,
) -> dict:
    return {
        "node": node["id"],
        "command": f"$fpf {node['command']}",
        "prompt": node.get("localized_prompts", {}).get(language, node["prompt"]),
        "persist_report": node["persist_report"],
        "contracts": node.get("contracts", []),
        "fpf_entrypoints": node.get("fpf_entrypoints", []),
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
        bindings = sum(len(node.get("fpf_entrypoints", [])) for node in graph["nodes"])
        print(json.dumps({
            "nodes": len(graph["nodes"]), "edges": len(graph["edges"]),
            "task_profiles": len(graph["task_profiles"]),
            "evaluation_cases": len(graph["evaluation_cases"]),
            "fpf_entrypoints": bindings, "status": "ok",
        }))
        return 0

    invocation = args.text if args.text is not None else " ".join(args.invocation)
    print(json.dumps(resolve(invocation, graph, args.language), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
