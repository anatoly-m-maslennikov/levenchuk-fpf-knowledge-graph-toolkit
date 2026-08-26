from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "route_fpf.py"
SPEC = importlib.util.spec_from_file_location("route_fpf", SCRIPT_PATH)
assert SPEC and SPEC.loader
ROUTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ROUTER)


class RouteFpfTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.graph = ROUTER.load_graph()

    def route(self, invocation: str, language: str = "auto") -> dict:
        return ROUTER.resolve(invocation, self.graph, language)

    def test_graph_is_valid(self) -> None:
        self.assertEqual([], ROUTER.validate_graph(self.graph))

    def test_empty_invocation_shows_help(self) -> None:
        route = self.route("$fpf")
        self.assertEqual("help", route["node"])
        self.assertFalse(route["persist_report"])

    def test_help_is_ephemeral(self) -> None:
        route = self.route("$fpf help")
        self.assertEqual("help", route["node"])
        self.assertFalse(route["persist_report"])

    def test_primary_russian_help_command_selects_russian_help_page(self) -> None:
        route = self.route("$fpf справка")
        self.assertEqual("help", route["node"])
        self.assertEqual("ru", route["language"])
        self.assertEqual("prompts/fpf-help.ru.md", route["prompt"])

    def test_old_russian_help_alias_remains_compatible(self) -> None:
        self.assertEqual("help", self.route("$fpf помощь")["node"])

    def test_explicit_russian_language_selects_russian_help_for_english_command(self) -> None:
        route = self.route("$fpf help", "ru")
        self.assertEqual("help", route["node"])
        self.assertEqual("ru", route["language"])
        self.assertEqual("explicit-or-setting", route["language_selected_by"])
        self.assertEqual("prompts/fpf-help.ru.md", route["prompt"])

    def test_every_russian_help_command_is_an_exact_routable_alias(self) -> None:
        help_text = (ROUTER.SKILL_ROOT / "prompts/fpf-help.ru.md").read_text(encoding="utf-8")
        for node in self.graph["nodes"]:
            command = node["localized_commands"]["ru"]
            with self.subTest(command=command):
                route = self.route(f"$fpf {command}")
                self.assertEqual(node["id"], route["node"])
                self.assertEqual("exact-command", route["selected_by"])
                self.assertIn(f"$fpf {command}", help_text)

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

    def test_natural_language_selects_analysis_node(self) -> None:
        route = self.route("$fpf Audit the implemented repairs for regressions")
        self.assertEqual("alignment-audit", route["node"])

    def test_russian_natural_language_routes_every_analytical_node(self) -> None:
        cases = {
            "Какие паттерны FPF применимы к этому вопросу?": "applicability-scan",
            "Построй актуальную карту исследований по этой области.": "sota-harvest",
            "Сгенерируй и сравни альтернативы без выбора победителя.": "options-explore",
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
        for scenario in singles[:7]:
            with self.subTest(scenario=scenario["id"]):
                self.assertEqual(
                    scenario["expected_sequence"][0],
                    self.route(scenario["question"])["node"],
                )

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


if __name__ == "__main__":
    unittest.main()
