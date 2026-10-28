"""Regression checks for CAD graph structural validation."""

from __future__ import annotations

import unittest
from pathlib import Path

from service.scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.models import CAD_PROFILE
from service.scripts.filesystem_policy import temporary_workspace
from service.scripts.validate_fpf_graph.validate_fpf_graph import validate_graph
from service.tests.validate_cad_graph.helpers import make_graph


class ValidateCadGraphTests(unittest.TestCase):
    def test_clean_cad_graph_preserves_reference_addresses(self) -> None:
        with temporary_workspace() as temporary:
            source, graph = make_graph(Path(temporary))
            result = validate_graph(graph, source, CAD_PROFILE)
            self.assertEqual(result["errors"], [])
            self.assertEqual(result["cad_ids"], 4)

    def test_misplaced_cad_page_fails(self) -> None:
        with temporary_workspace() as temporary:
            source, graph = make_graph(Path(temporary))
            (graph / "wrong.md").write_text("wrong\n", encoding="utf-8")
            result = validate_graph(graph, source, CAD_PROFILE)
            self.assertTrue(any("unexpected or misplaced" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
