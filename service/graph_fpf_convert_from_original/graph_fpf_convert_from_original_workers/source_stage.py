"""Stage the repository-owned patched source package inside toolkit runtime."""

from __future__ import annotations

import shutil
from pathlib import Path

from service.filesystem_policy import (
    is_system_temporary_path,
    remove_directory,
    replace_directory_contents,
    temporary_workspace,
)
from .source_package import package_root, validate_source_package_against_repository


STAGE_RELATIVE = Path(".runtime") / "original-fpf-sources"


def stage_root(root: Path) -> Path:
    return root / STAGE_RELATIVE


def _install_stage_atomic(candidate: Path, stage: Path, temporary: Path) -> None:
    previous = temporary / "previous"
    moved = False
    try:
        if stage.exists() or stage.is_symlink():
            if stage.is_symlink() or not stage.is_dir():
                raise ValueError(f"source stage must be absent or a real directory: {stage}")
            stage.rename(previous)
            moved = True
        candidate.rename(stage)
    except Exception:
        if moved and not stage.exists() and previous.exists():
            previous.rename(stage)
        raise
    if previous.exists():
        remove_directory(previous)


def _install_stage_in_place(candidate: Path, stage: Path, temporary: Path) -> None:
    previous = temporary / "previous"
    had_stage = stage.exists()
    if had_stage:
        replace_directory_contents(stage, previous)
    try:
        replace_directory_contents(candidate, stage)
    except Exception:
        if had_stage:
            replace_directory_contents(previous, stage)
        elif stage.exists():
            remove_directory(stage)
        raise


def _install_stage(candidate: Path, stage: Path, temporary: Path) -> None:
    if is_system_temporary_path(stage):
        _install_stage_in_place(candidate, stage, temporary)
        return
    try:
        _install_stage_atomic(candidate, stage, temporary)
    except PermissionError:
        _install_stage_in_place(candidate, stage, temporary)


def stage_sources(root: Path, repository: Path) -> dict[str, object]:
    repository = repository.resolve()
    metadata = validate_source_package_against_repository(root, repository)
    revision = str(metadata["upstream_revision"])
    (root / ".runtime").mkdir(parents=True, exist_ok=True)
    with temporary_workspace(prefix="fpf-source-stage-") as name:
        temporary = Path(name)
        candidate = temporary / "candidate"
        shutil.copytree(package_root(root), candidate)
        tracked = [str(item["path"]) for item in metadata["tracked_files"]]
        markdown = [item for item in tracked if item.lower().endswith(".md")]
        _install_stage(candidate, stage_root(root), temporary)
    return dict(
        status="sources staged", source_revision=revision,
        staged_repository=str(stage_root(root)), tracked_files=len(tracked),
        markdown_sources=markdown,
    )


def staged_source(root: Path, filename: str) -> Path:
    stage = stage_root(root)
    if stage.is_symlink() or not stage.is_dir():
        raise ValueError("source stage is missing; run --stage-sources first")
    source = stage / filename
    if not source.is_file():
        raise ValueError(f"staged source is missing: {filename}")
    return source
