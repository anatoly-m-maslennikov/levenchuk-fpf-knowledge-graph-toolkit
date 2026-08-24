"""Finalize an accepted conversion by removing temporary source and backups."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Callable

from scripts.filesystem_policy import remove_directory
from scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.models import FPF_PROFILE
from .source_package import source_identity
from .source_stage import stage_root
from .suite_runner import run_suite


EVIDENCE_RELATIVE = Path(".runtime") / "fpf-conversion-evaluation.json"
CASES_RELATIVE = (
    Path("scripts") / "graph_fpf_convert_from_original" /
    "graph_fpf_convert_from_original_assets" / "test_cases.json"
)
SuiteRunner = Callable[[Path, Path], dict[str, object]]


def _read_json(path: Path, label: str) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    entries = sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix())
    for path in entries:
        if path.is_symlink():
            raise ValueError(f"accepted graph contains a symlink: {path}")
        if not path.is_file() or path.name == ".DS_Store":
            continue
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(relative + b"\0" + path.read_bytes() + b"\0")
    return digest.hexdigest()


def _verify_evidence(root: Path, evidence_path: Path) -> str:
    evidence = _read_json(evidence_path, "evaluation evidence")
    expected = {
        "schema_version", "evaluator", "verdict", "current_revision",
        "backup_revision", "current_tree_sha256", "backup_tree_sha256",
    }
    if set(evidence) != expected:
        raise ValueError("evaluation evidence fields do not match schema 1")
    if evidence.get("schema_version") != 1:
        raise ValueError("evaluation evidence schema_version must be 1")
    if evidence.get("evaluator") != "graph-fpf-evaluate-conversion-result":
        raise ValueError("evaluation evidence names the wrong evaluator")
    if evidence.get("verdict") != "PASS":
        raise ValueError("evaluation verdict is not PASS")
    revision = evidence.get("current_revision")
    if not isinstance(revision, str) or not revision:
        raise ValueError("evaluation evidence has no current_revision")
    current = _read_json(
        root / FPF_PROFILE.default_output / "00_Index" / "FPF - Validation Report.json",
        "current graph report",
    )
    backup = _read_json(
        root / f"{FPF_PROFILE.default_output}.bak" / "00_Index" /
        "FPF - Validation Report.json", "backup graph report",
    )
    if current.get("source_revision") != revision:
        raise ValueError("evaluation revision does not match the current graph")
    if backup.get("source_revision") != evidence.get("backup_revision"):
        raise ValueError("evaluation backup revision does not match the backup graph")
    current_root = root / FPF_PROFILE.default_output
    backup_root = root / f"{FPF_PROFILE.default_output}.bak"
    if evidence.get("current_tree_sha256") != tree_sha256(current_root):
        raise ValueError("evaluation evidence does not match the current graph bytes")
    if evidence.get("backup_tree_sha256") != tree_sha256(backup_root):
        raise ValueError("evaluation evidence does not match the backup graph bytes")
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


def _cleanup_targets(root: Path) -> list[Path]:
    targets = [stage_root(root)]
    for path in sorted(root.iterdir()):
        if path.name.endswith("-Knowledge-Graph.bak"):
            if path.is_symlink() or not path.is_dir():
                raise ValueError(f"backup cleanup target must be a real directory: {path}")
            targets.append(path)
    return targets


def finalize_accepted(
    root: Path, evidence_path: Path | None = None,
    suite_runner: SuiteRunner = run_suite,
) -> dict[str, object]:
    evidence = evidence_path or root / EVIDENCE_RELATIVE
    revision = _verify_evidence(root, evidence)
    _verify_stage(root, revision)
    suite = suite_runner(root, root / CASES_RELATIVE)
    failures = suite.get("failures")
    if not isinstance(failures, list) or failures:
        raise ValueError(f"final deterministic suite did not pass: {failures}")
    targets = _cleanup_targets(root)
    for target in targets:
        remove_directory(target)
    return dict(
        status="accepted conversion finalized", source_revision=revision,
        deterministic_cases=suite.get("cases"), removed=[str(item) for item in targets],
        evaluation_evidence=str(evidence),
    )
