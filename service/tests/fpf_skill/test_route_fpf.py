from __future__ import annotations

import unittest
from pathlib import Path

from service.scripts.check_fpf_skill_graph_compatibility.check_fpf_skill_graph_compatibility import methodology_prompts
from service.scripts.validate_repository.validate_repository_workers.fpf_markdown import load_markdown_graph, load_routing_scenarios


ROOT = Path(__file__).resolve().parents[3]
SKILL_ROOT = ROOT / "skills/fpf.skill"


class MarkdownFpfGraphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.graph = load_markdown_graph(ROOT)
        cls.nodes = {node["id"]: node for node in cls.graph["nodes"]}

    def test_runtime_package_is_markdown_only(self) -> None:
        files = [path for path in SKILL_ROOT.rglob("*") if path.is_file() and path.name != ".DS_Store"]
        self.assertTrue(files)
        self.assertTrue(all(path.name == "SKILL.md" or path.suffix == ".md" for path in files))
        self.assertFalse(any("scripts" in path.relative_to(SKILL_ROOT).parts for path in files))
        for suffix in (".py", ".yaml", ".yml", ".json"):
            self.assertFalse(any(path.suffix == suffix for path in files))

    def test_graph_declares_all_nodes_and_persistence_boundaries(self) -> None:
        prompt_ids = {
            path.stem.removeprefix("fpf-")
            for path in (SKILL_ROOT / "prompts").glob("fpf-*.md")
            if path.name != "fpf-runtime.md"
        }
        self.assertEqual(prompt_ids | {"help"}, set(self.nodes))
        self.assertFalse(self.nodes["help"]["persist_report"])
        self.assertFalse(self.nodes["plan"]["persist_report"])
        analytical = {name for name, node in self.nodes.items() if node["persist_report"]}
        self.assertTrue(analytical)
        self.assertTrue(all(self.nodes[name]["fpf_entrypoints"] for name in analytical))

    def test_commands_aliases_prompts_and_edges_are_resolved_from_markdown(self) -> None:
        aliases: dict[str, str] = {}
        for node_id, node in self.nodes.items():
            self.assertTrue((SKILL_ROOT / node["prompt"]).is_file())
            for value in [node["command"], node["localized_command"], *node["aliases"]]:
                key = value.casefold()
                self.assertTrue(key not in aliases or aliases[key] == node_id)
                aliases[key] = node_id
        self.assertEqual("plan", aliases["route"])
        self.assertEqual("help", aliases["помощь"])
        edges = {(edge["from"], edge["to"]) for edge in self.graph["edges"]}
        self.assertIn(("design-challenge", "quality-improve"), edges)
        self.assertIn(("quality-improve", "alignment-audit"), edges)
        for edge in self.graph["edges"]:
            for field in (
                "producer_output", "consumer_input", "required_evidence", "gate_predicate",
            ):
                self.assertTrue(edge[field])
            self.assertRegex(edge["stop_state"], r"^STOP_[A-Z0-9_]+$")

    def test_routing_precedence_covers_composition_and_safe_fallbacks(self) -> None:
        text = (SKILL_ROOT / "references/fpf-command-graph.md").read_text(encoding="utf-8")
        for requirement in (
            "Recognize `plan <command> + ...` before executable composition",
            "Treat spaced ` + ` as composition only when every segment",
            "Prefer the longest complete command or alias",
            "never match substrings",
            "When intent is ambiguous, select `plan`",
        ):
            self.assertIn(requirement, text)

    def test_scenarios_cover_every_analytical_node_and_only_legal_stacks(self) -> None:
        scenarios = load_routing_scenarios(ROOT)
        analytical = {name for name, node in self.nodes.items() if node["persist_report"]}
        covered = {node for scenario in scenarios for node in scenario["expected_sequence"]}
        self.assertEqual(analytical, covered)
        edges = {(edge["from"], edge["to"]) for edge in self.graph["edges"]}
        for scenario in scenarios:
            if scenario["expected_mode"] in {"sequence", "composition", "plan"}:
                sequence = scenario["expected_sequence"]
                self.assertGreaterEqual(len(sequence), 2)
                self.assertTrue(all(pair in edges for pair in zip(sequence, sequence[1:])))

    def test_profiles_and_evaluation_cases_are_complete(self) -> None:
        profiles = self.graph["task_profiles"]
        cases = self.graph["evaluation_cases"]
        self.assertTrue(profiles)
        self.assertEqual(len(profiles), len({item["id"] for item in profiles}))
        self.assertEqual({item["id"] for item in profiles}, {item["profile"] for item in cases})
        self.assertTrue(all(len(item["examples"]) >= 2 for item in profiles))
        self.assertTrue(all(item.get("required_facets") and item.get("forbidden_inference") for item in cases))

    def test_compatibility_scan_covers_every_analytical_prompt_and_plan(self) -> None:
        scanned = {name for name, _path in methodology_prompts()}
        expected = {name for name, node in self.nodes.items() if node["persist_report"]} | {"plan"}
        self.assertEqual(expected, scanned)

    def test_localized_area_help_inventory_is_derived_from_graph(self) -> None:
        analytical = [node for node in self.nodes.values() if node["persist_report"]]
        for language, field in (("en", "command"), ("ru", "localized_command")):
            for area in ("framework", "software", "skills"):
                text = (SKILL_ROOT / f"prompts/help/{language}/fpf-help-{area}.md").read_text(
                    encoding="utf-8"
                )
                self.assertTrue(all(f"`$fpf {node[field]} " in text for node in analytical))


if __name__ == "__main__":
    unittest.main()
