"""Finalize an accepted conversion by removing temporary source and backups."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Callable

from service.scripts.filesystem_policy import remove_directory
from service.scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.models import FPF_PROFILE
from .source_package import source_identity
from .source_stage import stage_root
from .eval_pack import build_eval_pack
from .projection_manifest import PROJECTION_PROFILES, projection_manifest, tree_sha256
from service.tests.suite_runner import run_suite, suite_contract


EVIDENCE_RELATIVE = Path(".runtime") / "fpf-conversion-evaluation.json"
CASES_RELATIVE = Path("service") / "tests" / "test_cases.json"
SuiteRunner = Callable[[Path, Path], dict[str, object]]
ISSUE_FAMILIES = (
    "source-identity-safety-authority", "transaction-backup-rollback",
    "completeness-exact-reconstruction", "boundary-source-range-fidelity",
    "normative-markdown-preservation", "linkification-rendering",
    "identity-collision-handling", "folder-topology-reading-order",
    "filesystem-portability-path-hygiene", "provenance-replayability",
    "navigation-indexes-reachability", "relation-extraction-classification",
    "eval-pack-validator-independence", "repository-consumer-compatibility",
)
HISTORICAL_PROBES = (
    "unscoped-root-source", "stale-tree-after-moves",
    "triple-bracket-linkification", "table-pipe-corruption",
    "absolute-path-provenance", "implicit-generation-date",
    "missing-source-hashes", "wrong-semantic-link-target",
)


def _read_json(path: Path, label: str) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def _evidence_fields() -> set[str]:
    return {
        "schema_version", "evaluator", "verdict", "source_revision",
        "projection_manifest",
        "eval_pack_sha256", "issue_family_verdicts",
        "historical_regression_probes", "syntax_risk_strata",
        "semantic_selection", "deterministic_suite_manifest_sha256",
        "deterministic_suite_case_names",
    }


def _verify_evidence_identity(root: Path, evidence: dict[str, object]) -> tuple[str, Path, Path]:
    if set(evidence) != _evidence_fields():
        raise ValueError("evaluation evidence fields do not match schema 3")
    if evidence.get("schema_version") != 3:
        raise ValueError("evaluation evidence schema_version must be 3")
    if evidence.get("evaluator") != "graph-fpf-evaluate-conversion-result":
        raise ValueError("evaluation evidence names the wrong evaluator")
    if evidence.get("verdict") != "PASS":
        raise ValueError("evaluation verdict is not PASS")
    revision = evidence.get("source_revision")
    if not isinstance(revision, str) or not revision:
        raise ValueError("evaluation evidence has no source_revision")
    manifest = projection_manifest(root)
    if evidence.get("projection_manifest") != manifest:
        raise ValueError("evaluation projection manifest does not match graph bytes")
    if any(item.get("current_revision") != revision for item in manifest.values()):
        raise ValueError("projection revisions do not match the evaluated source revision")
    current_root = root / FPF_PROFILE.default_output
    backup_root = root / f"{FPF_PROFILE.default_output}.bak"
    return revision, current_root, backup_root


def _verify_eval_attestation(
    evidence: dict[str, object], current_root: Path, backup_root: Path,
) -> None:
    pack = build_eval_pack(current_root, backup_root)
    if evidence.get("eval_pack_sha256") != pack.get("eval_pack_sha256"):
        raise ValueError("evaluation evidence does not match the eval pack")
    family_verdicts = evidence.get("issue_family_verdicts")
    if family_verdicts != {name: "PASS" for name in ISSUE_FAMILIES}:
        raise ValueError("evaluation evidence does not attest all issue families")
    probes = evidence.get("historical_regression_probes")
    if probes != {name: "PASS" for name in HISTORICAL_PROBES}:
        raise ValueError("evaluation evidence does not attest all historical probes")
    expected_strata = {
        name: "PASS" if details.get("status") == "populated" else "NOT_PRESENT"
        for name, details in pack["syntax_risk_strata"].items()
    }
    if evidence.get("syntax_risk_strata") != expected_strata:
        raise ValueError("evaluation evidence does not cover every syntax-risk stratum")
    selection = pack["selection"]
    expected_selection = {
        key: selection[key] for key in ("policy", "selected_count", "omitted_count")
    }
    if evidence.get("semantic_selection") != expected_selection:
        raise ValueError("evaluation evidence selection does not match the eval pack")


def _verify_suite_attestation(root: Path, evidence: dict[str, object]) -> None:
    contract = suite_contract(root / CASES_RELATIVE)
    if evidence.get("deterministic_suite_manifest_sha256") != contract["manifest_sha256"]:
        raise ValueError("evaluation evidence names a stale deterministic suite manifest")
    if evidence.get("deterministic_suite_case_names") != contract["case_names"]:
        raise ValueError("evaluation evidence omits deterministic suite cases")


def _verify_evidence(root: Path, evidence_path: Path) -> str:
    evidence = _read_json(evidence_path, "evaluation evidence")
    revision, current_root, backup_root = _verify_evidence_identity(root, evidence)
    _verify_eval_attestation(evidence, current_root, backup_root)
    _verify_suite_attestation(root, evidence)
    return revision


def _verify_stage(root: Path, revision: str) -> None:
    stage = stage_root(root)
    source = stage / FPF_PROFILE.default_source
    _, staged_revision, _ = source_identity(
        source, expected_filename=FPF_PROFILE.default_source,
        source_label=FPF_PROFILE.label, revision_scope="repository",
    )
    if staged_revision != revision:
        raise ValueError("staged source revision does not match the evaluation")
    report = _read_json(
        root / FPF_PROFILE.default_output / "00_Index" / "FPF - Validation Report.json",
        "current graph report",
    )
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    if report.get("source_sha256") != digest:
        raise ValueError("staged source bytes do not match the current graph")


def _cleanup_targets(root: Path, evidence: dict[str, object]) -> list[Path]:
    targets = [stage_root(root)]
    manifest = evidence["projection_manifest"]
    for profile in PROJECTION_PROFILES:
        relative = manifest[profile.key]["backup_path"]
        path = root / relative
        if path.is_symlink() or not path.is_dir():
            raise ValueError(f"backup cleanup target must be a real directory: {path}")
        targets.append(path)
    return targets


def finalize_accepted(
    root: Path, evidence_path: Path | None = None,
    suite_runner: SuiteRunner = run_suite,
) -> dict[str, object]:
    evidence = evidence_path or root / EVIDENCE_RELATIVE
    evidence_data = _read_json(evidence, "evaluation evidence")
    revision = _verify_evidence(root, evidence)
    _verify_stage(root, revision)
    suite = suite_runner(root, root / CASES_RELATIVE)
    failures = suite.get("failures")
    if not isinstance(failures, list) or failures:
        raise ValueError(f"final deterministic suite did not pass: {failures}")
    contract = suite_contract(root / CASES_RELATIVE)
    if suite.get("manifest_sha256") != contract["manifest_sha256"]:
        raise ValueError("final deterministic suite used the wrong manifest")
    if suite.get("case_names") != contract["case_names"]:
        raise ValueError("final deterministic suite omitted required cases")
    targets = _cleanup_targets(root, evidence_data)
    for target in targets:
        remove_directory(target)
    return dict(
        status="accepted conversion finalized", source_revision=revision,
        deterministic_cases=suite.get("cases"), removed=[str(item) for item in targets],
        evaluation_evidence=str(evidence),
    )
