"""Regression checks for transactional CAD graph conversion."""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

from service.scripts.filesystem_policy import logical_path_exists, temporary_workspace
from service.scripts.graph_cad_convert_from_original.graph_cad_convert_from_original import convert_cad_graph
from service.tests.graph_cad_convert_from_original.helpers import make_source, run


def _advance_revision(source: Path) -> None:
    source.write_text(source.read_text(encoding="utf-8") + "\nRevised source.\n", encoding="utf-8")
    repository = source.parents[2]
    run("git", "add", ".", cwd=repository)
    run(
        "git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
        "commit", "-qm", "revise source", cwd=repository,
    )


class GraphCadConvertFromOriginalTests(unittest.TestCase):
    def test_initial_build_and_refresh_preserve_cad_ids_and_backup(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary)
            toolkit = root / "toolkit"
            toolkit.mkdir()
            source = make_source(root / "FPF")
            first = convert_cad_graph(root=toolkit, source=source, generated_on="2026-10-25")
            graph = toolkit / "CAD-Knowledge-Graph"
            (graph / "marker.txt").write_text("previous graph", encoding="utf-8")
            _advance_revision(source)
            convert_cad_graph(root=toolkit, source=source, generated_on="2026-10-25")
            notes = "\n".join(path.read_text(encoding="utf-8") for path in graph.rglob("*.md"))
            self.assertEqual(first["builder_report"]["framework"], "CAD")
            self.assertTrue((graph / "00_Index" / "CAD - Index.md").is_file())
            for identifier in ("CAD.1", "CAD.2", "CAD.Reference:1", "CAD.Reference:2"):
                self.assertIn(f'cad_id: "{identifier}"', notes)
            self.assertTrue((toolkit / "CAD-Knowledge-Graph.bak" / "marker.txt").is_file())

    def test_builder_failure_preserves_current_graph_and_backup(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary)
            source = make_source(root / "FPF")
            for name in ("CAD-Knowledge-Graph", "CAD-Knowledge-Graph.bak"):
                (root / name).mkdir()
                (root / name / "marker.txt").write_text(name, encoding="utf-8")
            target = "service.scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.transaction._run_builder"
            with patch(target, side_effect=ValueError("builder failed")):
                with self.assertRaisesRegex(ValueError, "builder failed"):
                    convert_cad_graph(root=root, source=source, generated_on="2026-10-25")
            for name in ("CAD-Knowledge-Graph", "CAD-Knowledge-Graph.bak"):
                self.assertEqual((root / name / "marker.txt").read_text(encoding="utf-8"), name)


class SameRevisionCadRepairTests(unittest.TestCase):
    def test_repair_keeps_absent_or_existing_predecessor_backup(self) -> None:
        for with_backup in (False, True):
            with self.subTest(with_backup=with_backup), temporary_workspace() as temporary:
                root = Path(temporary)
                source = make_source(root / "FPF")
                convert_cad_graph(root=root, source=source, generated_on="2026-10-25")
                graph = root / "CAD-Knowledge-Graph"
                backup = root / "CAD-Knowledge-Graph.bak"
                if with_backup:
                    backup.mkdir()
                    (backup / "predecessor.txt").write_text("previous revision", encoding="utf-8")
                (graph / "repair-marker.txt").write_text("repair me", encoding="utf-8")
                convert_cad_graph(root=root, source=source, generated_on="2026-10-25")
                self.assertFalse((graph / "repair-marker.txt").exists())
                self.assertEqual(logical_path_exists(backup), with_backup)
                if with_backup:
                    self.assertEqual((backup / "predecessor.txt").read_text(encoding="utf-8"), "previous revision")
                    self.assertFalse((backup / "repair-marker.txt").exists())


if __name__ == "__main__":
    unittest.main()
