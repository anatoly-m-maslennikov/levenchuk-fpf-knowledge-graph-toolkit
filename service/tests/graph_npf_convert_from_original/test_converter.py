#!/usr/bin/env python3
"""Regression checks for canonical NPF graph conversion."""

from __future__ import annotations

import unittest
import subprocess
import json
from pathlib import Path

from service.scripts.filesystem_policy import temporary_workspace
from service.scripts.graph_npf_convert_from_original.graph_npf_convert_from_original import convert_npf_graph
from service.scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.source_package_refresh import refresh_source_package
from service.scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.source_stage import stage_sources, staged_source
from service.tests.graph_npf_convert_from_original.helpers import SOURCE_NAME, make_source, run


class NpfSourcePathTests(unittest.TestCase):
    def test_unrecognized_nested_source_is_rejected(self) -> None:
        with temporary_workspace() as temporary:
            temporary_root = Path(temporary)
            toolkit = temporary_root / "toolkit"
            toolkit.mkdir()
            original = temporary_root / "FPF"
            source = make_source(original)
            wrong_source = original / "unrelated" / SOURCE_NAME
            wrong_source.parent.mkdir()
            wrong_source.write_bytes(source.read_bytes())
            run("git", "add", ".", cwd=original)
            run(
                "git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                "commit", "-qm", "unrelated file", cwd=original,
            )

            with self.assertRaisesRegex(ValueError, "configured source must"):
                convert_npf_graph(root=toolkit, source=wrong_source, generated_on="2026-10-25")


class NpfSourceRevisionTests(unittest.TestCase):
    def test_nested_upstream_source_uses_repository_snapshot_revision(self) -> None:
        with temporary_workspace() as temporary:
            temporary_root = Path(temporary)
            toolkit = temporary_root / "toolkit"
            toolkit.mkdir()
            original = temporary_root / "FPF"
            source = make_source(original, nested=True)
            (original / "unrelated.md").write_text("later upstream change\n", encoding="utf-8")
            run("git", "add", "unrelated.md", cwd=original)
            run(
                "git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                "commit", "-qm", "unrelated change", cwd=original,
            )
            revision = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=original, check=True,
                capture_output=True, text=True,
            ).stdout.strip()

            result = convert_npf_graph(root=toolkit, source=source, generated_on="2026-10-25")

            self.assertEqual(result["source_revision"], revision)
            self.assertEqual(result["source_repository"], str(original.resolve()))
            self.assertTrue((toolkit / "NPF-Knowledge-Graph" / "00_Index" / "NPF - Index.md").is_file())


class NpfPackagedSourceTests(unittest.TestCase):
    def test_package_and_stage_support_legacy_and_nested_sources(self) -> None:
        for nested in (False, True):
            with self.subTest(nested=nested), temporary_workspace() as temporary:
                temporary_root = Path(temporary)
                toolkit = temporary_root / "toolkit"
                toolkit.mkdir()
                original = temporary_root / "FPF"
                source = make_source(original, nested=nested)
                source_revision = subprocess.run(
                    ["git", "rev-parse", "HEAD"], cwd=original, check=True,
                    capture_output=True, text=True,
                ).stdout.strip()
                (original / "unrelated.md").write_text("later upstream change\n", encoding="utf-8")
                run("git", "add", "unrelated.md", cwd=original)
                run(
                    "git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                    "commit", "-qm", "unrelated change", cwd=original,
                )
                result = refresh_source_package(toolkit, original)
                metadata = json.loads((Path(result["source_package"]) / "source-metadata.json").read_text(encoding="utf-8"))
                record = next(record for record in metadata["tracked_files"] if record["path"] == source.relative_to(original).as_posix())
                self.assertEqual(record["source_revision"], source_revision)
                self.assertNotEqual(record["source_revision"], result["source_revision"])
                package_source = Path(result["source_package"]) / source.relative_to(original)
                package_result = convert_npf_graph(
                    root=toolkit, source=package_source, generated_on="2026-10-25",
                )
                stage_sources(toolkit, original)
                staged = staged_source(toolkit, SOURCE_NAME)

                staged_result = convert_npf_graph(
                    root=toolkit, source=staged, generated_on="2026-10-25",
                )

                self.assertEqual(staged.relative_to(toolkit / ".runtime" / "original-fpf-sources"), source.relative_to(original))
                self.assertEqual(package_result["source_revision"], result["source_revision"])
                self.assertEqual(package_result["source_revision"], staged_result["source_revision"])
                self.assertEqual(staged_result["builder_report"]["framework"], "NPF")


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
            source.write_text(source.read_text(encoding="utf-8") + "\nNew source revision.\n", encoding="utf-8")
            run("git", "add", ".", cwd=source.parent)
            run(
                "git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                "commit", "-qm", "NPF update", cwd=source.parent,
            )
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
