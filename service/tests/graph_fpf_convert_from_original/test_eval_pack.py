from __future__ import annotations

import json
import unittest
from pathlib import Path

from service.scripts.filesystem_policy import temporary_workspace
from service.scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.eval_pack import (
    build_eval_pack,
)


def _write_graph(root: Path, revision: str, pages: dict[str, tuple[str, str]]) -> None:
    index = root / "00_Index"
    index.mkdir(parents=True)
    (index / "FPF - Validation Report.json").write_text(
        json.dumps({"source_revision": revision, "broken_links_count": 0}),
        encoding="utf-8",
    )
    for identifier, (relative, title) in pages.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f'---\nfpf_id: "{identifier}"\ntitle: "{title}"\n---\n',
            encoding="utf-8",
        )


class EvalPackTests(unittest.TestCase):
    def test_compares_current_graph_with_predecessor(self) -> None:
        with temporary_workspace() as name:
            root = Path(name)
            current = root / "FPF-Knowledge-Graph"
            backup = root / "FPF-Knowledge-Graph.bak"
            _write_graph(backup, "old", {"A.1": ("A/old.md", "Old title")})
            _write_graph(
                current,
                "new",
                {"A.1": ("A/new.md", "New title"), "B.1": ("B/new.md", "Added")},
            )

            result = build_eval_pack(current, backup)

            self.assertEqual(result["backup_revision"], "old")
            self.assertEqual(result["current_revision"], "new")
            self.assertEqual(result["delta"]["added"], ["B.1"])
            self.assertEqual(result["counts"]["moved_ids"], 1)
            self.assertEqual(result["counts"]["retitled_ids"], 1)
            self.assertEqual(result["builder_integrity"]["broken_links"], 0)
            self.assertEqual(2, result["schema_version"])
            self.assertEqual(64, len(result["eval_pack_sha256"]))

if __name__ == "__main__":
    unittest.main()
