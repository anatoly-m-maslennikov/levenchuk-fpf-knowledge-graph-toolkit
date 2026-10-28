"""Repairing one source revision retains its actual predecessor graph."""

import json
import unittest
from pathlib import Path

from service.scripts.filesystem_policy import temporary_workspace
from service.scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.revision_backup import revision_backup


class RevisionBackupTests(unittest.TestCase):
    def test_same_revision_keeps_existing_backup(self) -> None:
        with temporary_workspace() as name:
            root = Path(name)
            graph, backup = root / "graph", root / "graph.bak"
            index = graph / "00_Index"
            index.mkdir(parents=True)
            report = index / "FPF - Validation Report.json"
            report.write_text(json.dumps({"source_revision": "current"}), encoding="utf-8")
            self.assertEqual(root / "same-revision-predecessor", revision_backup(graph, backup, root, "FPF", "current"))
            self.assertEqual(backup, revision_backup(graph, backup, root, "FPF", "new"))

    def test_initial_or_unreadable_graph_rotates_normally(self) -> None:
        with temporary_workspace() as name:
            root = Path(name)
            self.assertEqual(root / "graph.bak", revision_backup(root / "graph", root / "graph.bak", root, "FPF", "current"))
