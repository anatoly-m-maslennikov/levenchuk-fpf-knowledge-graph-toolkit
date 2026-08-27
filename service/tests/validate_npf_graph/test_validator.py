#!/usr/bin/env python3
"""Regression checks for NPF graph structural validation."""

from __future__ import annotations

import unittest
from pathlib import Path

from service.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.models import NPF_PROFILE
from service.filesystem_policy import temporary_workspace
from service.validate_fpf_graph.validate_fpf_graph import validate_graph
from service.tests.validate_npf_graph.helpers import make_graph


class ValidateNpfGraphTests(unittest.TestCase):
    def test_clean_npf_graph_passes(self) -> None:
        with temporary_workspace() as temporary:
            source, graph = make_graph(Path(temporary))

            result = validate_graph(graph, source, NPF_PROFILE)

            self.assertEqual(result["errors"], [])
            self.assertEqual(result["npf_ids"], 1)

    def test_misplaced_npf_page_fails(self) -> None:
        with temporary_workspace() as temporary:
            source, graph = make_graph(Path(temporary))
            (graph / "wrong.md").write_text("wrong\n", encoding="utf-8")

            result = validate_graph(graph, source, NPF_PROFILE)

            self.assertTrue(any("unexpected or misplaced" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
