"""Cleared managed-filesystem directories do not block the next refresh."""

import unittest
from pathlib import Path

from service.scripts.filesystem_policy import temporary_workspace
from service.scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.source_package_refresh import refresh_source_package
from service.tests.graph_fpf_convert_from_original.test_source_lifecycle import _make_original


class EmptySourceShellTests(unittest.TestCase):
    def test_refresh_ignores_retired_empty_package_shell(self) -> None:
        with temporary_workspace() as name:
            root = Path(name)
            original = _make_original(root / "FPF")
            toolkit = root / "toolkit"
            (toolkit / ".fpf-original-retired" / "empty").mkdir(parents=True)
            result = refresh_source_package(toolkit, original)
            self.assertTrue((Path(result["source_package"]) / "source-metadata.json").is_file())
            repeated = refresh_source_package(toolkit, original)
            self.assertEqual(result["source_revision"], repeated["source_revision"])
