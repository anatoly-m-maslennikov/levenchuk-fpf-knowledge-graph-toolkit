from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
SCRIPT_ROOT = REPOSITORY_ROOT / "skills" / "fpf.skill" / "scripts"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from route_fpf_workers.context import build_context
from route_fpf_workers.graph import graph_view, load_graph


class FpfContextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill_root = SCRIPT_ROOT.parent
        cls.repository_root = REPOSITORY_ROOT
        cls.graph = load_graph(cls.skill_root)

    def test_yaml_reader_returns_only_requested_node_runtime_fields(self) -> None:
        view = graph_view(self.graph, ["sota-harvest"])
        self.assertEqual(["sota-harvest"], [node["id"] for node in view["nodes"]])
        self.assertNotIn("aliases", view["nodes"][0])
        self.assertNotIn("keywords", view["nodes"][0])
        self.assertEqual([], view["edges"])
        self.assertEqual([], view["task_profiles"])

    def test_yaml_reader_returns_only_requested_task_profile(self) -> None:
        view = graph_view(
            self.graph, ["structure-recover"], ["software.ddd-bounded-contexts"]
        )
        self.assertEqual(
            ["software.ddd-bounded-contexts"],
            [profile["id"] for profile in view["task_profiles"]],
        )
        self.assertNotIn("keywords", view["task_profiles"][0])
        self.assertNotIn("examples", view["task_profiles"][0])

    def test_context_hydrates_verified_core_sections(self) -> None:
        bundle = build_context(
            self.graph, self.skill_root, self.repository_root, ["sota-harvest"]
        )
        self.assertEqual(["references/fpf-analysis-contract.md"], bundle["contracts"])
        pattern = bundle["patterns"][0]
        self.assertEqual("G.2", pattern["id"])
        self.assertEqual(
            {"problem_frame", "problem", "forces", "solution", "consequences"},
            set(pattern["sections"]),
        )
        self.assertIn("Problem frame", pattern["sections"]["problem_frame"]["text"])
        self.assertGreater(pattern["sections"]["solution"]["start_line"], 1)

    def test_conditional_method_is_lazy_until_explicitly_included(self) -> None:
        initial = build_context(
            self.graph, self.skill_root, self.repository_root, ["options-explore"]
        )
        self.assertEqual(["B.5.2.1"], [item["id"] for item in initial["patterns"]])
        self.assertEqual("G.9", initial["skipped_conditionals"][0]["id"])
        expanded = build_context(
            self.graph, self.skill_root, self.repository_root, ["options-explore"], {"G.9"}
        )
        self.assertEqual({"B.5.2.1", "G.9"}, {item["id"] for item in expanded["patterns"]})
        parity = next(item for item in expanded["patterns"] if item["id"] == "G.9")
        self.assertEqual([], parity["missing_core_sections"])

    def test_composition_deduplicates_shared_pattern_pages(self) -> None:
        bundle = build_context(
            self.graph, self.skill_root, self.repository_root,
            ["design-challenge", "alignment-audit"],
        )
        self.assertEqual(1, len(bundle["contracts"]))
        self.assertEqual(1, len(bundle["patterns"]))
        self.assertEqual(
            {"design-challenge", "alignment-audit"},
            {use["node"] for use in bundle["patterns"][0]["uses"]},
        )

    def test_task_profile_hydrates_only_its_bounded_fpf_context(self) -> None:
        bundle = build_context(
            self.graph, self.skill_root, self.repository_root,
            ["structure-recover"], profile_ids=["software.ddd-bounded-contexts"],
        )
        self.assertEqual(
            ["software.ddd-bounded-contexts"],
            [profile["id"] for profile in bundle["task_profiles"]],
        )
        self.assertEqual(
            {"A.22", "C.33", "A.1.1", "F.9"},
            {pattern["id"] for pattern in bundle["patterns"]},
        )
        ddd = next(pattern for pattern in bundle["patterns"] if pattern["id"] == "A.1.1")
        self.assertEqual(
            ["software.ddd-bounded-contexts"],
            [use["profile"] for use in ddd["uses"]],
        )


if __name__ == "__main__":
    unittest.main()
