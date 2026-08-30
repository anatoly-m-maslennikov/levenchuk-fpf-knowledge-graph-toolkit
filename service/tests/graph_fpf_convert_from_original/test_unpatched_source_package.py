from __future__ import annotations

import json
import unittest
from pathlib import Path

from service.scripts.filesystem_policy import temporary_workspace
from service.scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.source_stage import (
    stage_root,
    stage_sources,
)
from service.tests.graph_fpf_convert_from_original.test_source_lifecycle import (
    FPF,
    _make_original,
    _prepare_package,
)


class UnpatchedSourcePackageTests(unittest.TestCase):
    def test_refresh_accepts_an_unpatched_full_head(self) -> None:
        with temporary_workspace() as name:
            temporary = Path(name)
            original = _make_original(temporary / "FPF")
            toolkit = temporary / "toolkit"
            toolkit.mkdir()
            package = _prepare_package(toolkit, original, with_patch=False)

            result = stage_sources(toolkit, original)
            metadata = json.loads((package / "source-metadata.json").read_text())

            self.assertEqual(metadata["patches"], [])
            self.assertEqual(result["tracked_files"], 3)
            self.assertEqual((stage_root(toolkit) / FPF).read_bytes(), (original / FPF).read_bytes())


if __name__ == "__main__":
    unittest.main()
