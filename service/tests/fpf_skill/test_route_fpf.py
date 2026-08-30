from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
SCRIPT_PATH = REPOSITORY_ROOT / "skills" / "fpf.skill" / "scripts" / "route_fpf.py"
SPEC = importlib.util.spec_from_file_location("route_fpf", SCRIPT_PATH)
assert SPEC and SPEC.loader
ROUTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ROUTER)
from route_fpf_workers.context import build_context


class RouteFpfTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.graph = ROUTER.load_graph()

    def route(self, invocation: str, language: str = "auto") -> dict:
        return ROUTER.resolve(invocation, self.graph, language)

    def test_graph_is_valid(self) -> None:
        self.assertEqual([], ROUTER.validate_graph(self.graph))

    def test_compatibility_scan_covers_every_analytical_prompt(self) -> None:
        from service.scripts.check_fpf_skill_graph_compatibility.check_fpf_skill_graph_compatibility import methodology_prompts

        scanned = {name for name, _path in methodology_prompts()}
        expected = {
            node["id"] for node in self.graph["nodes"]
            if node["persist_report"]
        } | {"plan"}
        self.assertEqual(expected, scanned)

    def test_yaml_graph_declares_shared_contracts_and_resolvable_fpf_bindings(self) -> None:
        self.assertEqual("graph.yaml", ROUTER.GRAPH_PATH.name)
        self.assertEqual(4, self.graph["schema_version"])
        repository_root = REPOSITORY_ROOT
        analytical = [node for node in self.graph["nodes"] if node["persist_report"]]
        self.assertEqual(10, len(analytical))
        for node in analytical:
            with self.subTest(node=node["id"]):
                self.assertEqual(
                    ["references/fpf-analysis-contract.md"], node["contracts"]
                )
                self.assertTrue(node["fpf_entrypoints"])
                for binding in node["fpf_entrypoints"]:
                    page = repository_root / binding["repository_path"]
                    self.assertTrue(page.is_file(), page)
                    self.assertIn(
                        f'fpf_id: "{binding["id"]}"',
                        page.read_text(encoding="utf-8"),
                    )

    def test_empty_invocation_shows_help(self) -> None:
        route = self.route("$fpf")
        self.assertEqual("help", route["node"])
        self.assertFalse(route["persist_report"])

    def test_help_is_ephemeral(self) -> None:
        route = self.route("$fpf help")
        self.assertEqual("help", route["node"])
        self.assertFalse(route["persist_report"])

    def test_area_help_selects_only_requested_area_page(self) -> None:
        route = self.route("$fpf help software")
        self.assertEqual("help", route["node"])
        self.assertEqual("software", route["help_area"])
        self.assertEqual("prompts/help/en/fpf-help-software.md", route["prompt"])
        self.assertFalse(route["persist_report"])

    def test_russian_area_help_selects_russian_page(self) -> None:
        route = self.route("$fpf справка ПО")
        self.assertEqual("software", route["help_area"])
        self.assertEqual("ru", route["language"])
        self.assertEqual("prompts/help/ru/fpf-help-software.md", route["prompt"])

    def test_primary_russian_help_command_selects_russian_help_page(self) -> None:
        route = self.route("$fpf справка")
        self.assertEqual("help", route["node"])
        self.assertEqual("ru", route["language"])
        self.assertEqual("prompts/help/ru/fpf-help.md", route["prompt"])

    def test_old_russian_help_alias_remains_compatible(self) -> None:
        self.assertEqual("help", self.route("$fpf помощь")["node"])

    def test_explicit_russian_language_selects_russian_help_for_english_command(self) -> None:
        route = self.route("$fpf help", "ru")
        self.assertEqual("help", route["node"])
        self.assertEqual("ru", route["language"])
        self.assertEqual("explicit-or-setting", route["language_selected_by"])
        self.assertEqual("prompts/help/ru/fpf-help.md", route["prompt"])

    def test_every_russian_command_is_an_exact_routable_alias(self) -> None:
        for node in self.graph["nodes"]:
            command = node["localized_commands"]["ru"]
            with self.subTest(command=command):
                route = self.route(f"$fpf {command}")
                self.assertEqual(node["id"], route["node"])
                self.assertEqual("exact-command", route["selected_by"])

    def test_plan_replaces_route_and_is_ephemeral(self) -> None:
        route = self.route("$fpf plan compare approaches")
        self.assertEqual("plan", route["node"])
        self.assertEqual("compare approaches", route["task"])
        self.assertFalse(route["persist_report"])

    def test_old_route_alias_resolves_to_plan(self) -> None:
        self.assertEqual("plan", self.route("/fpf route this question")["node"])

    def test_design_challenge_direct_command(self) -> None:
        route = self.route("$fpf design challenge Review this proposal")
        self.assertEqual("design-challenge", route["node"])
        self.assertEqual("Review this proposal", route["task"])
        self.assertTrue(route["persist_report"])
        self.assertEqual(
            ["references/fpf-analysis-contract.md"], route["contracts"]
        )
        self.assertEqual("E.11.PUA", route["fpf_entrypoints"][0]["id"])

    def test_normalized_alias_preserves_original_residual_span(self) -> None:
        route = self.route("$fpf as-is map architecture dependencies")
        self.assertEqual("structure-recover", route["node"])
        self.assertEqual("architecture dependencies", route["task"])

    def test_natural_language_selects_analysis_node(self) -> None:
        route = self.route("$fpf Audit the implemented repairs for regressions")
        self.assertEqual("alignment-audit", route["node"])

    def test_russian_natural_language_routes_every_analytical_node(self) -> None:
        cases = {
            "Сформулируй рамку проблемы и постановку задачи.": "problem-frame",
            "Восстанови текущую структуру и зависимости без редизайна.": "structure-recover",
            "Какие паттерны FPF применимы к этому вопросу?": "applicability-scan",
            "Построй актуальную карту исследований по этой области.": "sota-harvest",
            "Сгенерируй и сравни альтернативы без выбора победителя.": "options-explore",
            "Спроектируй план тестирования и критерии успеха.": "evaluation-design",
            "Проведи стресс-тест архитектуры до реализации.": "design-challenge",
            "Выбери среди уже оценённых альтернатив и оформи ADR.": "decision-synthesize",
            "Улучши версионированный артефакт и повторно оцени качество.": "quality-improve",
            "Проведи аудит реализованной работы на регрессии.": "alignment-audit",
        }
        for task, expected in cases.items():
            with self.subTest(task=task):
                route = self.route(f"$fpf {task}")
                self.assertEqual(expected, route["node"])
                self.assertEqual("ru", route["language"])

    def test_single_node_routing_scenarios_select_the_expected_prompt(self) -> None:
        scenarios_path = ROUTER.SKILL_ROOT / "references/routing-scenarios.json"
        scenarios = json.loads(scenarios_path.read_text())["scenarios"]
        singles = [
            item for item in scenarios
            if item["route_action"] == "calls" and len(item["expected_sequence"]) == 1
        ]
        for scenario in singles:
            with self.subTest(scenario=scenario["id"]):
                self.assertEqual(
                    scenario["expected_sequence"][0],
                    self.route(scenario["question"])["node"],
                )

    def test_profile_examples_generate_routing_cases(self) -> None:
        for profile in self.graph["task_profiles"]:
            for example in profile["examples"]:
                with self.subTest(profile=profile["id"], task=example["text"]):
                    route = self.route(example["text"])
                    self.assertEqual(example["expected_node"], route["node"])
                    self.assertEqual(profile["id"], route["task_profile"]["id"])

    def test_same_profile_does_not_override_analytical_intent(self) -> None:
        recovered = self.route("$fpf structure recover Map the current DDD bounded contexts")
        challenged = self.route("$fpf design challenge Challenge the proposed DDD context split")
        self.assertEqual("structure-recover", recovered["node"])
        self.assertEqual("design-challenge", challenged["node"])
        self.assertEqual(
            recovered["task_profile"]["id"], challenged["task_profile"]["id"]
        )

    def test_every_profile_evaluation_case_executes_routing_and_context(self) -> None:
        profiles = {item["id"] for item in self.graph["task_profiles"]}
        nodes = {item["id"] for item in self.graph["nodes"] if item["persist_report"]}
        self.assertEqual(profiles, {case["profile"] for case in self.graph["evaluation_cases"]})
        for case in self.graph["evaluation_cases"]:
            with self.subTest(case=case["id"]):
                self.assertIn(case["profile"], profiles)
                self.assertIn(case["node"], nodes)
                self.assertTrue(case["required_facets"])
                self.assertTrue(case["forbidden_inference"])
                command = next(
                    node["command"] for node in self.graph["nodes"]
                    if node["id"] == case["node"]
                )
                route = self.route(f"$fpf {command} {case['task']}")
                self.assertEqual(case["node"], route["node"])
                self.assertEqual(case["profile"], route["task_profile"]["id"])
                context = build_context(
                    self.graph, ROUTER.SKILL_ROOT, REPOSITORY_ROOT,
                    [case["node"]], profile_ids=[case["profile"]],
                )
                self.assertEqual(case["node"], context["nodes"][0]["id"])
                self.assertEqual(case["profile"], context["task_profiles"][0]["id"])
                self.assertTrue(context["patterns"])

    def test_meta_plan_routing_scenario_is_non_executing(self) -> None:
        scenarios_path = ROUTER.SKILL_ROOT / "references/routing-scenarios.json"
        scenarios = json.loads(scenarios_path.read_text())["scenarios"]
        scenario = next(item for item in scenarios if item.get("expected_mode") == "plan")
        route = self.route(scenario["question"])
        self.assertEqual("plan", route["mode"])
        self.assertEqual(scenario["expected_sequence"], [
            item["node"] for item in route["planned_nodes"]
        ])
        self.assertTrue(route["execution_disabled"])
        self.assertFalse(route["persist_report"])

    def test_ambiguous_natural_language_falls_back_to_plan(self) -> None:
        route = self.route("$fpf review the implemented design")
        self.assertEqual("plan", route["node"])
        self.assertEqual("ambiguous-fallback", route["selected_by"])

    def test_explicit_composition_resolves_ordered_analytical_nodes(self) -> None:
        route = self.route(
            "$fpf design challenge + quality improve + alignment audit Improve this design"
        )
        self.assertEqual("composition", route["mode"])
        self.assertEqual(
            ["design-challenge", "quality-improve", "alignment-audit"],
            [item["node"] for item in route["nodes"]],
        )
        self.assertEqual("Improve this design", route["task"])
        self.assertTrue(route["persist_report"])
        self.assertTrue(all(item["contracts"] for item in route["nodes"]))
        self.assertTrue(all(item["fpf_entrypoints"] for item in route["nodes"]))

    def test_plan_prefix_validates_composition_without_execution(self) -> None:
        route = self.route(
            "$fpf plan sota harvest + options explore + design challenge Assess this proposal"
        )
        self.assertEqual("plan", route["node"])
        self.assertEqual("plan", route["mode"])
        self.assertEqual("explicit-meta-plan", route["selected_by"])
        self.assertEqual(
            ["sota-harvest", "options-explore", "design-challenge"],
            [item["node"] for item in route["planned_nodes"]],
        )
        self.assertEqual("Assess this proposal", route["task"])
        self.assertTrue(route["execution_disabled"])
        self.assertFalse(route["persist_report"])

    def test_russian_plan_prefix_validates_composition_without_execution(self) -> None:
        route = self.route(
            "$fpf план обзор исследований + исследовать варианты + проверка дизайна "
            "Оцени это предложение"
        )
        self.assertEqual("plan", route["node"])
        self.assertEqual("ru", route["language"])
        self.assertEqual(
            ["sota-harvest", "options-explore", "design-challenge"],
            [item["node"] for item in route["planned_nodes"]],
        )
        self.assertTrue(route["execution_disabled"])

    def test_plan_prefix_reports_illegal_handoff_without_execution(self) -> None:
        route = self.route("$fpf plan alignment audit + design challenge Review this")
        self.assertEqual("plan", route["node"])
        self.assertEqual("invalid-meta-plan", route["selected_by"])
        self.assertIn("illegal composition handoff", route["composition_error"])
        self.assertTrue(route["execution_disabled"])
        self.assertFalse(route["persist_report"])

    def test_direct_command_typo_suggests_but_never_executes(self) -> None:
        route = self.route("$fpf sota harvers Map the current field")
        self.assertEqual("plan", route["node"])
        self.assertEqual("typo-suggestion-fallback", route["selected_by"])
        self.assertEqual("sota-harvest", route["suggestions"][0]["node"])
        self.assertEqual("$fpf sota harvest", route["suggestions"][0]["command"])
        self.assertTrue(route["execution_disabled"])
        self.assertFalse(route["persist_report"])

    def test_russian_command_typo_suggests_but_never_executes(self) -> None:
        route = self.route("$fpf проверка дезайна Проверь предложение")
        self.assertEqual("plan", route["node"])
        self.assertEqual("design-challenge", route["suggestions"][0]["node"])
        self.assertEqual("проверка дизайна", route["suggestions"][0]["matched_alias"])
        self.assertEqual("ru", route["language"])
        self.assertTrue(route["execution_disabled"])

    def test_exact_short_alias_with_task_still_executes_normally(self) -> None:
        route = self.route("$fpf sota Map the current field")
        self.assertEqual("sota-harvest", route["node"])
        self.assertEqual("exact-command", route["selected_by"])
        self.assertEqual("Map the current field", route["task"])
        self.assertNotIn("suggestions", route)

    def test_meta_plan_typo_returns_suggestion_without_execution(self) -> None:
        route = self.route(
            "$fpf plan sota harvers + options explore + design challenge Assess this"
        )
        self.assertEqual("plan", route["node"])
        self.assertEqual("invalid-meta-plan", route["selected_by"])
        self.assertEqual("sota-harvest", route["suggestions"][0]["node"])
        self.assertTrue(route["execution_disabled"])
        self.assertFalse(route["persist_report"])

    def test_help_typo_suggests_help_without_opening_it(self) -> None:
        route = self.route("$fpf hepl")
        self.assertEqual("plan", route["node"])
        self.assertEqual("help", route["suggestions"][0]["node"])
        self.assertTrue(route["execution_disabled"])

    def test_unrelated_natural_language_does_not_gain_a_typo_suggestion(self) -> None:
        route = self.route("$fpf review the implemented design")
        self.assertEqual("ambiguous-fallback", route["selected_by"])
        self.assertNotIn("suggestions", route)

    def test_composition_accepts_exact_aliases(self) -> None:
        route = self.route("$fpf challenge + improve Strengthen this proposal")
        self.assertEqual(["design-challenge", "quality-improve"], [
            item["node"] for item in route["nodes"]
        ])

    def test_composition_accepts_russian_aliases_and_preserves_task(self) -> None:
        route = self.route(
            "$fpf проверка дизайна + улучшение качества + аудит согласованности "
            "Усиль предложение и проверь исправления"
        )
        self.assertEqual(
            ["design-challenge", "quality-improve", "alignment-audit"],
            [item["node"] for item in route["nodes"]],
        )
        self.assertEqual("Усиль предложение и проверь исправления", route["task"])
        self.assertEqual("ru", route["language"])

    def test_illegal_composition_falls_back_to_plan_with_reason(self) -> None:
        route = self.route("$fpf alignment audit + design challenge Review this")
        self.assertEqual("plan", route["node"])
        self.assertEqual("invalid-composition-fallback", route["selected_by"])
        self.assertIn("illegal composition handoff", route["composition_error"])

    def test_task_text_before_last_composed_command_is_rejected(self) -> None:
        route = self.route("$fpf design challenge this proposal + quality improve")
        self.assertEqual("plan", route["node"])
        self.assertIn("only after the last command", route["composition_error"])

    def test_plus_without_spaces_remains_ordinary_task_text(self) -> None:
        route = self.route("$fpf plan Compare A+B")
        self.assertEqual("plan", route["node"])
        self.assertEqual("Compare A+B", route["task"])

    def test_literal_spaced_plus_in_direct_task_is_not_a_composition(self) -> None:
        route = self.route(
            "$fpf design challenge Evaluate speed + safety tradeoffs"
        )
        self.assertEqual("design-challenge", route["node"])
        self.assertNotIn("mode", route)
        self.assertEqual("Evaluate speed + safety tradeoffs", route["task"])

    def test_literal_spaced_plus_in_plan_task_is_not_a_composition(self) -> None:
        route = self.route("$fpf plan Compare speed + safety")
        self.assertEqual("plan", route["node"])
        self.assertNotIn("mode", route)
        self.assertEqual("Compare speed + safety", route["task"])

    def test_profile_keywords_do_not_match_inside_other_words(self) -> None:
        route = self.route("$fpf plan Review capital allocation")
        self.assertNotIn("task_profile", route)


if __name__ == "__main__":
    unittest.main()
