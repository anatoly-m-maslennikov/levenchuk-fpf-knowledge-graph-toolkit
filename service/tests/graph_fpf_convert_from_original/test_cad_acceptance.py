"""Bind optional CAD projections to the existing conversion acceptance contract."""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from service.scripts.filesystem_policy import logical_path_exists, remove_directory, temporary_workspace
from service.scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.acceptance import finalize_accepted
from service.scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.projection_manifest import projection_manifest
from service.scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.source_stage import stage_root, stage_sources
from service.tests.graph_cad_convert_from_original.helpers import SOURCE, SOURCE_RELATIVE
from service.tests.graph_fpf_convert_from_original.helpers import write_npf_report
from service.tests.graph_fpf_convert_from_original.test_acceptance import _prepared as _without_cad
from service.tests.graph_fpf_convert_from_original.test_source_lifecycle import (
    FPF, _make_original, _prepare_package, _run, _suite_result, _write_evidence, _write_report,
)


def _cad_report(graph: Path, revision: str, digest: str) -> None:
    index = graph / "00_Index"
    index.mkdir(parents=True)
    (index / "CAD - Validation Report.json").write_text(
        json.dumps(dict(source_revision=revision, source_sha256=digest)), encoding="utf-8",
    )


def _bind_manifest(root: Path, evidence: Path) -> None:
    data = json.loads(evidence.read_text(encoding="utf-8"))
    data["projection_manifest"] = projection_manifest(root)
    evidence.write_text(json.dumps(data), encoding="utf-8")


def _prepared(temporary: Path) -> tuple[Path, Path]:
    original = _make_original(temporary / "FPF")
    source = original / SOURCE_RELATIVE
    source.parent.mkdir(parents=True)
    source.write_text(SOURCE, encoding="utf-8")
    _run("git", "add", SOURCE_RELATIVE, cwd=original)
    _run("git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "CAD", cwd=original)
    toolkit = temporary / "toolkit"
    toolkit.mkdir()
    _prepare_package(toolkit, original)
    result = stage_sources(toolkit, original)
    revision = str(result["source_revision"])
    digest = hashlib.sha256((stage_root(toolkit) / FPF).read_bytes()).hexdigest()
    _write_report(toolkit / "FPF-Knowledge-Graph", revision, digest)
    _write_report(toolkit / "FPF-Knowledge-Graph.bak", "previous")
    write_npf_report(toolkit / "NPF-Knowledge-Graph", revision)
    write_npf_report(toolkit / "NPF-Knowledge-Graph.bak", "previous")
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    _cad_report(toolkit / "CAD-Knowledge-Graph", revision, digest)
    evidence = _write_evidence(toolkit, revision, "previous")
    _bind_manifest(toolkit, evidence)
    return toolkit, evidence


def _finalize(toolkit: Path, evidence: Path) -> dict[str, object]:
    return finalize_accepted(toolkit, evidence, lambda root, _: _suite_result(root))


class CadCleanupTests(unittest.TestCase):
    def test_first_generation_accepts_no_cad_backup(self) -> None:
        with temporary_workspace() as name:
            toolkit, evidence = _prepared(Path(name))
            record = projection_manifest(toolkit)["cad"]
            self.assertIsNone(record["backup_revision"])
            self.assertIsNone(record["backup_tree_sha256"])
            result = _finalize(toolkit, evidence)
            self.assertFalse(logical_path_exists(stage_root(toolkit)))
            self.assertTrue((toolkit / "CAD-Knowledge-Graph").is_dir())
            self.assertNotIn(str(toolkit / "CAD-Knowledge-Graph.bak"), result["removed"])

    def test_later_generation_cleans_bound_cad_backup(self) -> None:
        with temporary_workspace() as name:
            toolkit, evidence = _prepared(Path(name))
            backup = toolkit / "CAD-Knowledge-Graph.bak"
            _cad_report(backup, "previous", "old")
            _bind_manifest(toolkit, evidence)
            result = _finalize(toolkit, evidence)
            self.assertFalse(logical_path_exists(backup))
            self.assertIn(str(backup), result["removed"])


class CadEvidenceTests(unittest.TestCase):
    def test_changed_graph_bytes_reject_evidence(self) -> None:
        with temporary_workspace() as name:
            toolkit, evidence = _prepared(Path(name))
            (toolkit / "CAD-Knowledge-Graph" / "tampered.md").write_text("changed", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "projection manifest"):
                _finalize(toolkit, evidence)
            self.assertTrue(stage_root(toolkit).is_dir())

    def test_rebound_stale_revision_and_source_digest_are_rejected(self) -> None:
        for field, value, error in (
            ("source_revision", "stale", "projection revisions"),
            ("source_sha256", "bad", "staged source bytes"),
        ):
            with self.subTest(field=field), temporary_workspace() as name:
                toolkit, evidence = _prepared(Path(name))
                path = toolkit / "CAD-Knowledge-Graph/00_Index/CAD - Validation Report.json"
                report = json.loads(path.read_text(encoding="utf-8"))
                report[field] = value
                path.write_text(json.dumps(report), encoding="utf-8")
                _bind_manifest(toolkit, evidence)
                with self.assertRaisesRegex(ValueError, error):
                    _finalize(toolkit, evidence)
                self.assertTrue(stage_root(toolkit).is_dir())


class CadFilesystemTests(unittest.TestCase):
    def test_symlink_current_and_backup_roots_are_rejected(self) -> None:
        for relative in ("CAD-Knowledge-Graph", "CAD-Knowledge-Graph.bak"):
            with self.subTest(relative=relative), temporary_workspace() as name:
                toolkit, evidence = _without_cad(Path(name))
                if relative.endswith(".bak"):
                    _cad_report(toolkit / "CAD-Knowledge-Graph", "current", "unused")
                path = toolkit / relative
                path.symlink_to(toolkit / "FPF-Knowledge-Graph", target_is_directory=True)
                with self.assertRaisesRegex(ValueError, "real directory"):
                    _finalize(toolkit, evidence)

    def test_missing_required_fpf_and_npf_backups_remain_blocking(self) -> None:
        for relative in ("FPF-Knowledge-Graph.bak", "NPF-Knowledge-Graph.bak"):
            with self.subTest(relative=relative), temporary_workspace() as name:
                toolkit, evidence = _prepared(Path(name))
                remove_directory(toolkit / relative)
                with self.assertRaises(ValueError):
                    _finalize(toolkit, evidence)


if __name__ == "__main__":
    unittest.main()
