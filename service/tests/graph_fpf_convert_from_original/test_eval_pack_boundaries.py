from __future__ import annotations

import unittest
from pathlib import Path

from service.scripts.filesystem_policy import temporary_workspace
from service.scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.eval_pack import build_eval_pack
from service.tests.graph_fpf_convert_from_original.test_eval_pack import _write_graph


class EvalPackLargeDeltaTests(unittest.TestCase):
    def test_removed_and_large_change_sets_have_accountable_selection(self) -> None:
        with temporary_workspace() as name:
            root = Path(name)
            current = root / "FPF-Knowledge-Graph"
            backup = root / "FPF-Knowledge-Graph.bak"
            backup_pages = {"Z.1": ("Z/removed.md", "Removed")}
            backup_pages.update({
                f"A.{index}": (f"A/old-{index}.md", f"Old {index}")
                for index in range(1, 15)
            })
            current_pages = {
                f"A.{index}": (f"A/new-{index}.md", f"New {index}")
                for index in range(1, 15)
            }
            _write_graph(backup, "old", backup_pages)
            _write_graph(current, "new", current_pages)
            result = build_eval_pack(current, backup)
            removed = next(item for item in result["selected_eval_targets"] if item["fpf_id"] == "Z.1")
            self.assertIsNone(removed["current_path"])
            self.assertTrue(removed["backup_path"].endswith("Z/removed.md"))
            for kind in ("moved", "retitled"):
                self.assertEqual(3, len(result["selection"]["by_kind"][kind]["selected"]))
                self.assertEqual(11, result["selection"]["by_kind"][kind]["omitted"])


class EvalPackIdentityTests(unittest.TestCase):
    def test_duplicate_ids_are_rejected(self) -> None:
        with temporary_workspace() as name:
            root = Path(name)
            current = root / "FPF-Knowledge-Graph"
            backup = root / "FPF-Knowledge-Graph.bak"
            _write_graph(backup, "old", {"A.1": ("A/old.md", "Old")})
            _write_graph(current, "new", {"A.1": ("A/one.md", "One")})
            duplicate = current / "A/two.md"
            duplicate.write_text('---\nfpf_id: "A.1"\ntitle: "Two"\n---\n', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate fpf_id"):
                build_eval_pack(current, backup)
