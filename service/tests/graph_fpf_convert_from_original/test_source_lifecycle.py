from __future__ import annotations

import hashlib
import json
import subprocess
import shutil
import unittest
from pathlib import Path

from service.scripts.filesystem_policy import logical_path_exists, temporary_workspace
from service.scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.acceptance import (
    CASES_RELATIVE,
    HISTORICAL_PROBES,
    ISSUE_FAMILIES,
    finalize_accepted,
    tree_sha256,
)
from service.scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.eval_pack import build_eval_pack
from service.tests.suite_runner import suite_contract
from service.scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.source_stage import (
    stage_root,
    stage_sources,
)
from service.scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.source_package import (
    package_destination,
)
from service.scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.source_package_refresh import refresh_source_package


FPF = "FPF-Spec.md"
NPF = "Narrativization-and-Narrative-Studies-Principles-Framework.md"
SUITE_CASES = Path(__file__).resolve().parents[1] / "test_cases.json"


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
    cases = root / CASES_RELATIVE
    cases.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SUITE_CASES, cases)
    contract = suite_contract(cases)
    pack = build_eval_pack(
        root / "FPF-Knowledge-Graph", root / "FPF-Knowledge-Graph.bak",
    )
    selection = pack["selection"]
    path = root / ".runtime" / "evaluation.json"
    path.write_text(
        json.dumps(dict(
            schema_version=2, evaluator="graph-fpf-evaluate-conversion-result",
            verdict=verdict, current_revision=current, backup_revision=backup,
            current_tree_sha256=tree_sha256(root / "FPF-Knowledge-Graph"),
            backup_tree_sha256=tree_sha256(root / "FPF-Knowledge-Graph.bak"),
            eval_pack_sha256=pack["eval_pack_sha256"],
            issue_family_verdicts={name: "PASS" for name in ISSUE_FAMILIES},
            historical_regression_probes={name: "PASS" for name in HISTORICAL_PROBES},
            syntax_risk_strata={
                name: "PASS" if details["status"] == "populated" else "NOT_PRESENT"
                for name, details in pack["syntax_risk_strata"].items()
            },
            semantic_selection={
                key: selection[key] for key in ("policy", "selected_count", "omitted_count")
            },
            deterministic_suite_manifest_sha256=contract["manifest_sha256"],
            deterministic_suite_case_names=contract["case_names"],
        )),
        encoding="utf-8",
    )
    return path


def _suite_result(root: Path, failures: list[str] | None = None) -> dict[str, object]:
    contract = suite_contract(root / CASES_RELATIVE)
    return {
        "cases": len(contract["case_names"]), "failures": failures or [],
        "case_names": contract["case_names"],
        "manifest_sha256": contract["manifest_sha256"],
    }


class SourceRefreshTests(unittest.TestCase):
    def test_refresh_bootstraps_when_no_source_package_exists(self) -> None:
        with temporary_workspace() as name:
            temporary = Path(name)
            original = _make_original(temporary / "FPF")
            toolkit = temporary / "toolkit"
            toolkit.mkdir()

            result = refresh_source_package(toolkit, original)

            package = Path(result["source_package"])
            self.assertTrue((package / FPF).is_file())
            self.assertTrue((package / "source-metadata.json").is_file())
            self.assertEqual([], result["patches"])

    def test_refresh_rejects_corrupt_existing_source_package(self) -> None:
        with temporary_workspace() as name:
            temporary = Path(name)
            original = _make_original(temporary / "FPF")
            toolkit = temporary / "toolkit"
            toolkit.mkdir()
            corrupt = toolkit / ".fpf-original-corrupt"
            corrupt.mkdir()
            (corrupt / "unexpected.txt").write_text("not a patch seed", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "corrupt"):
                refresh_source_package(toolkit, original)

    def test_refresh_rejects_spoofed_non_github_remote(self) -> None:
        with temporary_workspace() as name:
            temporary = Path(name)
            original = _make_original(temporary / "FPF")
            _run("git", "remote", "set-url", "origin", "https://example.invalid/ailev/FPF.git", cwd=original)
            toolkit = temporary / "toolkit"
            toolkit.mkdir()

            with self.assertRaisesRegex(ValueError, "no remote"):
                refresh_source_package(toolkit, original)


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

if __name__ == "__main__":
    unittest.main()
