from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from service.scripts.filesystem_policy import logical_path_exists, temporary_workspace
from service.scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.acceptance import (
    CASES_RELATIVE, HISTORICAL_PROBES, ISSUE_FAMILIES, finalize_accepted,
)
from service.scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.source_stage import stage_root, stage_sources
from service.tests.graph_fpf_convert_from_original.test_source_lifecycle import (
    FPF, _make_original, _prepare_package, _suite_result, _write_evidence,
    _write_report,
)
from service.tests.suite_runner import suite_contract


def _prepared(temporary: Path, verdict: str = "PASS") -> tuple[Path, Path]:
    original = _make_original(temporary / "FPF")
    toolkit = temporary / "toolkit"
    toolkit.mkdir()
    _prepare_package(toolkit, original)
    result = stage_sources(toolkit, original)
    revision = str(result["source_revision"])
    digest = hashlib.sha256((stage_root(toolkit) / FPF).read_bytes()).hexdigest()
    _write_report(toolkit / "FPF-Knowledge-Graph", revision, digest)
    _write_report(toolkit / "FPF-Knowledge-Graph.bak", "previous")
    return toolkit, _write_evidence(toolkit, revision, "previous", verdict=verdict)


class AcceptedCleanupTests(unittest.TestCase):
    def test_finalization_clears_stage_and_all_graph_backups(self) -> None:
        with temporary_workspace() as name:
            toolkit, evidence = _prepared(Path(name))
            (toolkit / "NPF-Knowledge-Graph.bak").mkdir()
            (toolkit / "Future-Knowledge-Graph.bak").mkdir()
            accepted = finalize_accepted(toolkit, evidence, lambda root, _: _suite_result(root))
            self.assertFalse(logical_path_exists(stage_root(toolkit)))
            self.assertFalse(logical_path_exists(toolkit / "FPF-Knowledge-Graph.bak"))
            self.assertFalse(logical_path_exists(toolkit / "NPF-Knowledge-Graph.bak"))
            self.assertFalse(logical_path_exists(toolkit / "Future-Knowledge-Graph.bak"))
            self.assertEqual(accepted["deterministic_cases"], len(
                suite_contract(toolkit / CASES_RELATIVE)["case_names"]
            ))


class RejectedCleanupTests(unittest.TestCase):
    def test_failed_suite_and_non_pass_evaluation_preserve_inputs(self) -> None:
        with temporary_workspace() as name:
            toolkit, evidence = _prepared(Path(name))
            with self.assertRaisesRegex(ValueError, "did not pass"):
                finalize_accepted(toolkit, evidence, lambda root, _: _suite_result(root, ["validator"]))
            self.assertTrue(stage_root(toolkit).is_dir())
        with temporary_workspace() as name:
            toolkit, evidence = _prepared(Path(name), verdict="FAIL")
            with self.assertRaisesRegex(ValueError, "verdict is not PASS"):
                finalize_accepted(toolkit, evidence, lambda root, _: _suite_result(root))
            self.assertTrue((toolkit / "FPF-Knowledge-Graph.bak").is_dir())


def _mutations():
    return (
        ("schema", lambda data: data.__setitem__("schema_version", 1)),
        ("evaluator", lambda data: data.__setitem__("evaluator", "other")),
        ("revision", lambda data: data.__setitem__("current_revision", "wrong")),
        ("tree", lambda data: data.__setitem__("current_tree_sha256", "0" * 64)),
        ("eval-pack", lambda data: data.__setitem__("eval_pack_sha256", "0" * 64)),
        ("families", lambda data: data["issue_family_verdicts"].pop(ISSUE_FAMILIES[0])),
        ("probes", lambda data: data["historical_regression_probes"].pop(HISTORICAL_PROBES[0])),
        ("strata", lambda data: data["syntax_risk_strata"].clear()),
        ("selection", lambda data: data["semantic_selection"].__setitem__("selected_count", -1)),
        ("suite-digest", lambda data: data.__setitem__("deterministic_suite_manifest_sha256", "0" * 64)),
        ("suite-cases", lambda data: data["deterministic_suite_case_names"].pop()),
    )


class EvidenceTamperTests(unittest.TestCase):
    def test_every_bound_evidence_family_rejects_tampering(self) -> None:
        for label, mutate in _mutations():
            with self.subTest(label=label), temporary_workspace() as name:
                toolkit, evidence = _prepared(Path(name))
                data = json.loads(evidence.read_text(encoding="utf-8"))
                mutate(data)
                evidence.write_text(json.dumps(data), encoding="utf-8")
                with self.assertRaises(ValueError):
                    finalize_accepted(toolkit, evidence, lambda root, _: _suite_result(root))
                self.assertTrue(stage_root(toolkit).is_dir())


class EvidenceFilesystemTamperTests(unittest.TestCase):
    def test_symlink_and_staged_source_tampering_are_rejected(self) -> None:
        with temporary_workspace() as name:
            toolkit, evidence = _prepared(Path(name))
            (toolkit / "FPF-Knowledge-Graph/link").symlink_to("missing")
            with self.assertRaisesRegex(ValueError, "symlink"):
                finalize_accepted(toolkit, evidence, lambda root, _: _suite_result(root))
        with temporary_workspace() as name:
            toolkit, evidence = _prepared(Path(name))
            source = stage_root(toolkit) / FPF
            source.write_text(source.read_text(encoding="utf-8") + "tampered\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "digest mismatch|staged source bytes"):
                finalize_accepted(toolkit, evidence, lambda root, _: _suite_result(root))
