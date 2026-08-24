from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path

from scripts.filesystem_policy import logical_path_exists, temporary_workspace
from scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.acceptance import (
    finalize_accepted,
    tree_sha256,
)
from scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.source_stage import (
    stage_root,
    stage_sources,
)
from scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.source_package import (
    package_destination,
)
from scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.source_package_refresh import refresh_source_package


FPF = "FPF-Spec.md"
NPF = "Narrativization-and-Narrative-Studies-Principles-Framework.md"


def _run(*arguments: str, cwd: Path) -> str:
    result = subprocess.run(arguments, cwd=cwd, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def _make_original(root: Path) -> Path:
    root.mkdir()
    _run("git", "init", "-q", cwd=root)
    _run("git", "remote", "add", "origin", "https://github.com/ailev/FPF.git", cwd=root)
    (root / FPF).write_text("# Part A\n\n## A.1 - FPF\n", encoding="utf-8")
    (root / NPF).write_text("# NPF\n\n## NSTD.1 - Narrative\n", encoding="utf-8")
    (root / "Future-Framework.md").write_text("# Future\n", encoding="utf-8")
    _run("git", "add", ".", cwd=root)
    _run(
        "git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
        "commit", "-qm", "sources", cwd=root,
    )
    return root


def _prepare_package(toolkit: Path, original: Path, *, with_patch: bool = True) -> Path:
    revision = _run("git", "rev-parse", "HEAD", cwd=original)
    package = package_destination(toolkit, revision)
    package.mkdir()
    if with_patch:
        (package / "0001-test-source-patch.patch").write_text(
            """diff --git a/FPF-Spec.md b/FPF-Spec.md
--- a/FPF-Spec.md
+++ b/FPF-Spec.md
@@ -3 +3,2 @@
 ## A.1 - FPF
+<!-- repository patch -->
""",
            encoding="utf-8",
        )
    refresh_source_package(toolkit, original)
    return package


def _write_report(graph: Path, revision: str, digest: str = "unused") -> None:
    index = graph / "00_Index"
    index.mkdir(parents=True)
    (index / "FPF - Validation Report.json").write_text(
        json.dumps({"source_revision": revision, "source_sha256": digest}),
        encoding="utf-8",
    )


def _write_evidence(root: Path, current: str, backup: str, verdict: str = "PASS") -> Path:
    path = root / ".runtime" / "evaluation.json"
    path.write_text(
        json.dumps(dict(
            schema_version=1, evaluator="graph-fpf-evaluate-conversion-result",
            verdict=verdict, current_revision=current, backup_revision=backup,
            current_tree_sha256=tree_sha256(root / "FPF-Knowledge-Graph"),
            backup_tree_sha256=tree_sha256(root / "FPF-Knowledge-Graph.bak"),
        )),
        encoding="utf-8",
    )
    return path


class SourceStagingTests(unittest.TestCase):
    def test_stages_every_tracked_source_file(self) -> None:
        with temporary_workspace() as name:
            temporary = Path(name)
            original = _make_original(temporary / "FPF")
            toolkit = temporary / "toolkit"
            toolkit.mkdir()
            package = _prepare_package(toolkit, original)

            result = stage_sources(toolkit, original)

            stage = stage_root(toolkit)
            self.assertTrue((stage / FPF).is_file())
            self.assertTrue((stage / NPF).is_file())
            self.assertTrue((stage / "Future-Framework.md").is_file())
            self.assertIn("Future-Framework.md", result["markdown_sources"])
            self.assertIn("repository patch", (stage / FPF).read_text(encoding="utf-8"))
            self.assertTrue((stage / "0001-test-source-patch.patch").is_file())
            self.assertTrue((stage / "source-metadata.json").is_file())
            self.assertTrue(package.is_dir())
            self.assertFalse((toolkit / FPF).exists())
            self.assertFalse((toolkit / NPF).exists())

class AcceptedCleanupTests(unittest.TestCase):
    def test_finalization_clears_stage_and_all_graph_backups(self) -> None:
        with temporary_workspace() as name:
            temporary = Path(name)
            original = _make_original(temporary / "FPF")
            toolkit = temporary / "toolkit"
            toolkit.mkdir()
            package = _prepare_package(toolkit, original)
            result = stage_sources(toolkit, original)
            revision = str(result["source_revision"])
            digest = hashlib.sha256((stage_root(toolkit) / FPF).read_bytes()).hexdigest()
            _write_report(toolkit / "FPF-Knowledge-Graph", revision, digest)
            _write_report(toolkit / "FPF-Knowledge-Graph.bak", "previous")
            (toolkit / "NPF-Knowledge-Graph.bak").mkdir()
            (toolkit / "Future-Knowledge-Graph.bak").mkdir()
            evidence = _write_evidence(toolkit, revision, "previous")

            accepted = finalize_accepted(
                toolkit, evidence, lambda _root, _cases: dict(cases=17, failures=[])
            )

            self.assertFalse(logical_path_exists(stage_root(toolkit)))
            self.assertFalse(logical_path_exists(toolkit / "FPF-Knowledge-Graph.bak"))
            self.assertFalse(logical_path_exists(toolkit / "NPF-Knowledge-Graph.bak"))
            self.assertFalse(logical_path_exists(toolkit / "Future-Knowledge-Graph.bak"))
            self.assertTrue((toolkit / "FPF-Knowledge-Graph").is_dir())
            self.assertTrue(package.is_dir())
            self.assertTrue((package / FPF).is_file())
            self.assertEqual(accepted["deterministic_cases"], 17)



class RejectedCleanupTests(unittest.TestCase):
    def test_failed_final_suite_preserves_sources_and_backups(self) -> None:
        with temporary_workspace() as name:
            temporary = Path(name)
            original = _make_original(temporary / "FPF")
            toolkit = temporary / "toolkit"
            toolkit.mkdir()
            _prepare_package(toolkit, original)
            result = stage_sources(toolkit, original)
            revision = str(result["source_revision"])
            digest = hashlib.sha256((stage_root(toolkit) / FPF).read_bytes()).hexdigest()
            _write_report(toolkit / "FPF-Knowledge-Graph", revision, digest)
            _write_report(toolkit / "FPF-Knowledge-Graph.bak", "previous")
            evidence = _write_evidence(toolkit, revision, "previous")

            with self.assertRaisesRegex(ValueError, "did not pass"):
                finalize_accepted(
                    toolkit, evidence,
                    lambda _root, _cases: dict(cases=17, failures=["validator"]),
                )

            self.assertTrue(stage_root(toolkit).is_dir())
            self.assertTrue((toolkit / "FPF-Knowledge-Graph.bak").is_dir())


class NonPassEvaluationTests(unittest.TestCase):
    def test_non_pass_evaluation_preserves_everything(self) -> None:
        with temporary_workspace() as name:
            temporary = Path(name)
            original = _make_original(temporary / "FPF")
            toolkit = temporary / "toolkit"
            toolkit.mkdir()
            _prepare_package(toolkit, original)
            result = stage_sources(toolkit, original)
            revision = str(result["source_revision"])
            digest = hashlib.sha256((stage_root(toolkit) / FPF).read_bytes()).hexdigest()
            _write_report(toolkit / "FPF-Knowledge-Graph", revision, digest)
            _write_report(toolkit / "FPF-Knowledge-Graph.bak", "previous")
            evidence = _write_evidence(toolkit, revision, "previous", verdict="FAIL")

            with self.assertRaisesRegex(ValueError, "verdict is not PASS"):
                finalize_accepted(
                    toolkit, evidence, lambda _root, _cases: dict(cases=17, failures=[])
                )

            self.assertTrue(stage_root(toolkit).is_dir())
            self.assertTrue((toolkit / "FPF-Knowledge-Graph.bak").is_dir())


if __name__ == "__main__":
    unittest.main()
