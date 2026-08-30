from __future__ import annotations

import re
import unittest
from pathlib import Path

from service.scripts.validate_repository.validate_repository_workers.fpf_markdown import load_markdown_graph


ROOT = Path(__file__).resolve().parents[3]
GRAPH_ROOT = ROOT / "FPF-Knowledge-Graph"
SKILL_ROOT = ROOT / "skills/fpf.skill"


def index_paths() -> dict[str, Path]:
    index = GRAPH_ROOT / "00_Index/FPF - Index.md"
    result: dict[str, Path] = {}
    for line in index.read_text(encoding="utf-8").splitlines():
        match = re.match(r"\|\s*([^| ]+)\s*\|\s*\[\[([^]]+)]]\s*\|", line)
        if match:
            result[match.group(1)] = GRAPH_ROOT / f"{match.group(2)}.md"
    return result


class FpfMarkdownContextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.graph = load_markdown_graph(ROOT)
        cls.pages = index_paths()

    def test_every_command_and_profile_binding_resolves_by_stable_id(self) -> None:
        owners = [*self.graph["nodes"], *self.graph["task_profiles"]]
        for owner in owners:
            for binding in owner["fpf_entrypoints"]:
                with self.subTest(owner=owner["id"], identifier=binding["id"]):
                    page = self.pages.get(binding["id"])
                    self.assertIsNotNone(page)
                    self.assertTrue(page.is_file())
                    self.assertIn(f'fpf_id: "{binding["id"]}"', page.read_text(encoding="utf-8"))

    def test_selected_pages_expose_bounded_core_sections(self) -> None:
        for identifier in ("G.2", "B.5.2.1", "E.11.PUA"):
            text = self.pages[identifier].read_text(encoding="utf-8")
            headings = re.findall(r"(?m)^## (.+)$", text)
            self.assertGreaterEqual(len(headings), 3)
            self.assertTrue(any("problem" in heading.casefold() for heading in headings))
            self.assertTrue(any("solution" in heading.casefold() or "implementation" in heading.casefold() for heading in headings))

    def test_conditional_binding_remains_explicit_and_lazy(self) -> None:
        options = next(node for node in self.graph["nodes"] if node["id"] == "options-explore")
        conditional = next(item for item in options["fpf_entrypoints"] if item["relation"] == "conditional_method")
        self.assertEqual("G.9", conditional["id"])
        self.assertIn("alternatives require", conditional["when"])
        connector = (SKILL_ROOT / "references/fpf-context-connector.md").read_text(encoding="utf-8")
        self.assertIn("Load a `conditional_method` only when", connector)

    def test_composition_context_is_loaded_one_node_at_a_time(self) -> None:
        connector = (SKILL_ROOT / "references/fpf-context-connector.md").read_text(encoding="utf-8")
        self.assertIn("current node immediately before it executes", connector)
        self.assertIn("do not preload later-node context", connector)

    def test_context_budget_and_ledger_are_native_and_nonpersistent(self) -> None:
        connector = (SKILL_ROOT / "references/fpf-context-connector.md").read_text(encoding="utf-8")
        for requirement in (
            "Invocation-local context ledger and budget",
            "at most 6 distinct FPF pages",
            "at most 18 distinct FPF pages",
            "STOP_CONTEXT_BUDGET_EXHAUSTED",
            "Never create or consult a persistent context cache",
            "Derive the final `FPF sources consulted` subsection from this ledger",
        ):
            self.assertIn(requirement, connector)


if __name__ == "__main__":
    unittest.main()
