"""Regression checks for the bounded fenced-code risk heuristic."""

import re
import time
import unittest
import json
from pathlib import Path

from service.scripts.filesystem_policy import temporary_workspace

from service.scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.eval_risk import (
    _has_fenced_heading_or_id,
    _matches,
    risk_inventory,
)


LEGACY_FENCED = re.compile(
    r"```[\s\S]*?(?:^#|[A-Z](?:\.[A-Za-z0-9-]+)+)[\s\S]*?```",
    re.MULTILINE,
)


class FencedRiskSemanticsTests(unittest.TestCase):
    def test_keeps_legacy_heading_and_identifier_boundaries(self) -> None:
        cases = (
            "plain A.1", "```", "`````", "``````", "```# inline```",
            "```\n# heading\n```", "```text A.1```", "```text AB.1.2```",
            "```text a.1```", "```text A.```", "```text A.-```",
            "# before\n```plain```\nA.1 after", "```plain```\nA.1\n```plain```",
            "~~~\n# heading\n~~~", "```\nplain\n```", "```\n# unclosed",
        )
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(_has_fenced_heading_or_id(text), bool(LEGACY_FENCED.search(text)))


class FencedRiskPerformanceTests(unittest.TestCase):
    def test_large_unclosed_code_with_many_ids_is_bounded(self) -> None:
        text = "```\n" + "A.1 plain words\n" * 5000
        start = time.perf_counter()

        matches = _matches(text, "A.10", "A/page.md", "Page", set(), set())

        self.assertNotIn("fenced-code-heading-or-id", matches)
        self.assertLess(time.perf_counter() - start, 2.0)


def _source_page(root: Path, relative: str, *, mode: str = "canonical-generated", lines: str = "  - 5\n  - 9") -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f'---\nmode: "{mode}"\nsource_lines:\n{lines}\n---\n\nText\n', encoding="utf-8")


class IdlessRiskInventoryTests(unittest.TestCase):
    def test_idless_source_pages_are_counted_and_targeted_by_path(self) -> None:
        with temporary_workspace() as name:
            root = Path(name)
            _source_page(root, "00-readme/01_Entry.md")
            _source_page(root, "00-unprefixed/01_Usage.md")
            _source_page(root, "00_Hubs/Hub.md", mode="index-generated")
            _source_page(root, "00_Index/Index.md", mode="index-generated")
            _source_page(root, "00-readme/Empty.md", lines="  - 0\n  - 0")

            result = risk_inventory(root, {}, {}, set())["unprefixed-h2-routing"]

            self.assertEqual(result["population"], 2)
            self.assertEqual(result["targets"], ["00-readme/01_Entry.md"])
            self.assertEqual(result["status"], "populated")

    def test_only_index_pages_do_not_populate_unprefixed_risk(self) -> None:
        with temporary_workspace() as name:
            root = Path(name)
            _source_page(root, "00_Hubs/Hub.md", mode="index-generated")

            result = risk_inventory(root, {}, {}, set())["unprefixed-h2-routing"]

            self.assertEqual(result["population"], 0)
            self.assertEqual(result["status"], "not present in candidate")


class UnresolvedRiskInventoryTests(unittest.TestCase):
    def test_actual_unresolved_sources_take_precedence_over_body_words(self) -> None:
        with temporary_workspace() as name:
            root = Path(name)
            (root / "A0.md").write_text("unresolved questions in prose", encoding="utf-8")
            (root / "A18.md").write_text("actual C.MM relation", encoding="utf-8")
            report = root / "00_Index" / "FPF - Validation Report.json"
            report.parent.mkdir()
            report.write_text(json.dumps({"unresolved_relations_sample": [{"source": "A18", "target": "C.MM"}]}), encoding="utf-8")

            result = risk_inventory(root, {"A.0": "A0.md", "A.18": "A18.md"}, {}, set())

            self.assertEqual(result["unresolved-placeholder-relation"]["population"], 2)
            self.assertEqual(result["unresolved-placeholder-relation"]["targets"], ["A.18"])


if __name__ == "__main__":
    unittest.main()
