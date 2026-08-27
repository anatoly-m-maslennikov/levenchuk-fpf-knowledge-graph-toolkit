"""Perform one recoverable framework graph replacement transaction."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from service.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.models import (
    FPF_PROFILE,
    GraphProfile,
)
from service.filesystem_policy import (
    is_system_temporary_path,
    logical_path_exists,
    remove_directory,
    replace_directory_contents,
    temporary_workspace,
)
from .source_package import source_identity


BUILDER_MODULE = "service.build_fpf_obsidian_graph"


def remove_generated_tree(path: Path) -> None:
    if path.is_symlink() or (path.exists() and not path.is_dir()):
        path.unlink()
    elif path.exists():
        remove_directory(path)


def _validate_targets(graph: Path, backup: Path, require_existing: bool) -> None:
    if require_existing and (not graph.is_dir() or graph.is_symlink()):
        raise ValueError(f"current generated graph must be a real directory: {graph}")
    if graph.exists() and (not graph.is_dir() or graph.is_symlink()):
        raise ValueError(f"generated graph must be absent or a real directory: {graph}")
    if backup.is_symlink() or (backup.exists() and not backup.is_dir()):
        raise ValueError(f"backup path must be absent or a real directory: {backup}")


def _builder_command(
    builder: Path | None, profile: GraphProfile, source: Path,
    revision: str, generated_on: str, target: Path,
) -> list[str]:
    base = [sys.executable, str(builder)] if builder else [sys.executable, "-m", BUILDER_MODULE]
    profile_args = [] if profile == FPF_PROFILE else ["--profile", profile.key]
    return [
        *base, *profile_args, "--source", str(source),
        "--source-revision", revision, "--generated-on", generated_on,
        "--out", str(target), "--clean",
    ]


def _run_builder(command: list[str]) -> None:
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        raise ValueError(f"graph builder failed: {detail}")


def _read_report(graph: Path, label: str) -> dict[str, object]:
    path = graph / "00_Index" / f"{label} - Validation Report.json"
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"new graph has no readable validation report: {exc}") from exc


def _normalize_report(graph: Path, label: str, output_name: str) -> dict[str, object]:
    report = _read_report(graph, label)
    report["out_dir"] = output_name
    path = graph / "00_Index" / f"{label} - Validation Report.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def _tree_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*") if path.is_file() and path.name != ".DS_Store"
    }


def _restore_atomic(
    graph: Path, backup: Path, previous: Path,
    candidate_installed: bool, current_moved: bool, previous_moved: bool,
) -> None:
    if candidate_installed and (graph.exists() or graph.is_symlink()):
        remove_generated_tree(graph)
    if current_moved and backup.exists():
        backup.rename(graph)
    if previous_moved and previous.exists():
        previous.rename(backup)


def _install_atomic(candidate: Path, graph: Path, backup: Path, temporary: Path) -> bool:
    previous = temporary / "previous-backup"
    had_previous = logical_path_exists(backup)
    had_current = logical_path_exists(graph)
    previous_moved = current_moved = candidate_installed = False
    try:
        if had_previous:
            backup.rename(previous)
            previous_moved = True
        if had_current:
            graph.rename(backup)
            current_moved = True
        candidate.rename(graph)
        candidate_installed = True
        return had_previous
    except Exception:
        _restore_atomic(
            graph, backup, previous,
            candidate_installed, current_moved, previous_moved,
        )
        raise


def _restore_in_place(
    graph: Path, backup: Path, previous: Path,
    current_existed: bool, backup_existed: bool,
) -> None:
    if current_existed:
        replace_directory_contents(backup, graph)
    elif graph.exists():
        remove_directory(graph)
    if backup_existed:
        replace_directory_contents(previous, backup)
    elif backup.exists():
        remove_directory(backup)


def _install_in_place(candidate: Path, graph: Path, backup: Path, temporary: Path) -> bool:
    previous = temporary / "previous-backup"
    backup_existed = logical_path_exists(backup)
    current_existed = logical_path_exists(graph)
    if backup_existed:
        replace_directory_contents(backup, previous)
    if current_existed:
        replace_directory_contents(graph, backup)
    try:
        replace_directory_contents(candidate, graph)
        return backup_existed
    except Exception:
        _restore_in_place(graph, backup, previous, current_existed, backup_existed)
        raise


def _install_candidate(candidate: Path, graph: Path, backup: Path, temporary: Path) -> bool:
    if is_system_temporary_path(graph) or (backup.exists() and not logical_path_exists(backup)):
        return _install_in_place(candidate, graph, backup, temporary)
    try:
        return _install_atomic(candidate, graph, backup, temporary)
    except PermissionError:
        return _install_in_place(candidate, graph, backup, temporary)


def _result(
    converter: str, source: Path, repo: Path, remote: str, revision: str,
    generated_on: str, graph: Path, backup: Path, replaced: bool,
    report: dict[str, object],
) -> dict[str, object]:
    return dict(
        converter=converter, source=str(source), source_repository=str(repo),
        source_remote=remote, source_revision=revision, generated_on=generated_on,
        graph=str(graph), backup=str(backup), replaced_previous_backup=replaced,
        builder_report=report,
    )


def convert_transaction(
    *, profile: GraphProfile, converter_name: str, require_existing: bool,
    revision_scope: str, root: Path, builder: Path | None,
    source: Path, generated_on: str,
) -> dict[str, object]:
    graph = root / profile.default_output
    backup = root / f"{profile.default_output}.bak"
    _validate_targets(graph, backup, require_existing)
    repo, revision, remote = source_identity(
        source, expected_filename=profile.default_source,
        source_label=profile.label, revision_scope=revision_scope,
    )
    runtime = root / ".runtime"
    runtime.mkdir(parents=True, exist_ok=True)
    with temporary_workspace(prefix=f".{converter_name}-", directory=runtime) as name:
        candidate = Path(name) / "candidate"
        command = _builder_command(builder, profile, source, revision, generated_on, candidate)
        _run_builder(command)
        report = _normalize_report(candidate, profile.label, graph.name)
        unchanged = graph.is_dir() and _tree_snapshot(candidate) == _tree_snapshot(graph)
        replaced = False if unchanged else _install_candidate(candidate, graph, backup, Path(name))
    return _result(
        converter_name, source, repo, remote, revision, generated_on,
        graph, backup, replaced, report,
    )
