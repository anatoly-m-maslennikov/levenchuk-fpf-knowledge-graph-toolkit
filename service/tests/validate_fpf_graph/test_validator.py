#!/usr/bin/env python3
"""Regression checks for generated FPF graph structural validation."""

from __future__ import annotations

import unittest
from pathlib import Path

from service.scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.models import Heading, Page
from service.scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.relations import normalize_relation_targets
from service.scripts.filesystem_policy import temporary_workspace
from service.scripts.validate_fpf_graph.validate_fpf_graph import validate_graph
from service.tests.validate_fpf_graph.helpers import make_graph


class RelationNormalizationTests(unittest.TestCase):
    def test_relation_qualifiers_and_ranges_resolve_to_real_ids(self) -> None:
        pages = [
            Page("page", Heading(2, identifier, index), index, index, [], framework_id=identifier)
            for index, identifier in enumerate(("A.2", "A.6.2", "A.6.3", "A.6.4", "C.29"), start=1)
        ]
        pages[0].relations = {
            "related": ["A.2-family", "A.6.2-A.6.4", "C.29-compatible", "F.0.2"]
        }

        normalize_relation_targets(pages)

        self.assertEqual(
            pages[0].relations["related"],
            ["A.2", "A.6.2", "A.6.3", "A.6.4", "C.29", "F.0.2"],
        )


class ValidateGraphTests(unittest.TestCase):
    def test_clean_generated_graph_passes(self) -> None:
        with temporary_workspace() as temporary:
            source, graph = make_graph(Path(temporary))

            result = validate_graph(graph, source)

            self.assertEqual(result["errors"], [])

    def test_os_metadata_is_ignored_but_misplaced_file_fails(self) -> None:
        with temporary_workspace() as temporary:
            source, graph = make_graph(Path(temporary))
            (graph / ".DS_Store").write_bytes(b"junk")
            (graph / "wrong.md").write_text("wrong\n", encoding="utf-8")

            result = validate_graph(graph, source)

            self.assertTrue(any("operating-system metadata" in warning for warning in result["warnings"]))
            self.assertTrue(any("unexpected or misplaced" in error for error in result["errors"]))

    def test_empty_managed_directory_shell_is_noncontent(self) -> None:
        with temporary_workspace() as temporary:
            source, graph = make_graph(Path(temporary))
            (graph / "retired-folder-shell").mkdir()

            result = validate_graph(graph, source)

            self.assertEqual(result["errors"], [])
            self.assertTrue(any("directory shell" in warning for warning in result["warnings"]))


if __name__ == "__main__":
    unittest.main()
