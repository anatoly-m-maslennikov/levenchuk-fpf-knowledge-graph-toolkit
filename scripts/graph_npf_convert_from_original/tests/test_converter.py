#!/usr/bin/env python3
"""Regression checks for canonical NPF graph conversion."""

from __future__ import annotations

import unittest
from pathlib import Path

from scripts.filesystem_policy import temporary_workspace
from scripts.graph_npf_convert_from_original.graph_npf_convert_from_original import convert_npf_graph
from scripts.graph_npf_convert_from_original.tests.helpers import make_source


class GraphNpfConvertFromOriginalTests(unittest.TestCase):
    def test_initial_build_and_refresh_use_npf_names_and_backup(self) -> None:
        with temporary_workspace() as temporary:
            temporary_root = Path(temporary)
            toolkit = temporary_root / "toolkit"
            toolkit.mkdir()
            source = make_source(temporary_root / "FPF")

            first = convert_npf_graph(root=toolkit, source=source, generated_on="2026-08-22")
            graph = toolkit / "NPF-Knowledge-Graph"
            marker = graph / "marker.txt"
            marker.write_text("previous graph", encoding="utf-8")
            second = convert_npf_graph(root=toolkit, source=source, generated_on="2026-08-22")

            self.assertEqual(first["builder_report"]["framework"], "NPF")
            self.assertTrue((graph / "00_Index" / "NPF - Index.md").is_file())
            generated_patterns = [path.read_text(encoding="utf-8") for path in graph.glob("NSTD/*/*.md")]
            self.assertTrue(any('npf_id: "NSTD.1"' in text for text in generated_patterns))
            self.assertTrue((toolkit / "NPF-Knowledge-Graph.bak" / "marker.txt").is_file())
            self.assertFalse(first["replaced_previous_backup"])
            self.assertFalse(second["replaced_previous_backup"])


if __name__ == "__main__":
    unittest.main()
