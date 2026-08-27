"""Refresh the repository-owned patched source package from read-only upstream."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from service.filesystem_policy import clear_directory, replace_directory_contents, temporary_workspace

from .source_package import (
    METADATA_NAME,
    PACKAGE_PREFIX,
    SCHEMA_VERSION,
    UPSTREAM_REMOTE,
    _apply_patches,
    _git_bytes,
    _sha256_bytes,
    _sha256_file,
    package_destination,
    validate_source_package,
    validate_source_package_against_repository,
)
from .source_repository import canonical_source_revision, git


def refresh_source_package(root: Path, repository: Path) -> dict[str, object]:
    actual, revision, remote = canonical_source_revision(repository / "FPF-Spec.md")
    if actual != repository.resolve():
        raise ValueError(f"configured source repository mismatch: {actual}")
    if git(repository, "status", "--porcelain", "--untracked-files=no"):
        raise ValueError("configured source repository has tracked local changes")
    tracked = git(repository, "ls-tree", "-r", "--name-only", revision).splitlines()
    destination = package_destination(root, revision)
    existing = _existing_package(root, destination)
    patches = sorted(existing.glob("*.patch"))
    with temporary_workspace(prefix="fpf-source-refresh-") as name:
        candidate = Path(name) / "candidate"
        candidate.mkdir()
        upstream_hashes, source_revisions = _copy_upstream(
            repository, revision, tracked, candidate,
        )
        candidate_patches = _copy_patches(patches, candidate)
        _apply_patches(candidate, candidate_patches)
        metadata = _metadata(
            revision, UPSTREAM_REMOTE, tracked, upstream_hashes, source_revisions,
            candidate, candidate_patches,
        )
        (candidate / METADATA_NAME).write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
        )
        validate_source_package(candidate)
        _install_package(candidate, destination, existing, Path(name))
    validate_source_package_against_repository(root, repository)
    return {
        "status": "revision-named source package refreshed",
        "source_package": str(destination), "source_revision": revision,
        "tracked_files": len(tracked), "patches": [patch.name for patch in patches],
    }


def _existing_package(root: Path, destination: Path) -> Path:
    candidates = sorted(
        path for path in root.glob(f"{PACKAGE_PREFIX}*")
        if path.is_dir() and (path / METADATA_NAME).is_file()
    )
    if destination.is_dir() and destination not in candidates:
        candidates.append(destination)
    if len(candidates) != 1:
        raise ValueError(
            f"refresh requires exactly one existing revision-named source package, found {len(candidates)}"
        )
    return candidates[0]


def _install_package(
    candidate: Path, destination: Path, existing: Path, temporary: Path,
) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    if destination != existing:
        replace_directory_contents(existing, temporary / "retired")
        clear_directory(existing)
    replace_directory_contents(candidate, destination)
    remains = any(
        path.is_file() or path.is_symlink() for path in existing.rglob("*")
    )
    if destination != existing and remains:
        raise ValueError(f"old source package was not cleared: {existing}")


def _copy_upstream(
    repository: Path, revision: str, tracked: list[str], candidate: Path,
) -> tuple[dict[str, str], dict[str, str]]:
    hashes: dict[str, str] = {}
    revisions: dict[str, str] = {}
    for relative in tracked:
        value = _git_bytes(repository, revision, relative)
        hashes[relative] = _sha256_bytes(value)
        target = candidate / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(value)
        revisions[relative] = git(
            repository, "log", "-1", "--format=%H", revision, "--", relative,
        )
    return hashes, revisions


def _copy_patches(patches: list[Path], candidate: Path) -> list[Path]:
    copied = []
    for patch in patches:
        target = candidate / patch.name
        shutil.copy2(patch, target)
        copied.append(target)
    return copied


def _metadata(
    revision: str, remote: str, tracked: list[str], upstream_hashes: dict[str, str],
    source_revisions: dict[str, str], candidate: Path, patches: list[Path],
) -> dict[str, object]:
    return {
        "schema_version": SCHEMA_VERSION, "upstream_repository": "ailev/FPF",
        "upstream_revision": revision, "upstream_remote": remote,
        "tracked_files": [
            {
                "path": relative, "source_revision": source_revisions[relative],
                "upstream_sha256": upstream_hashes[relative],
                "effective_sha256": _sha256_file(candidate / relative),
            }
            for relative in tracked
        ],
        "patches": [
            {"path": patch.name, "sha256": _sha256_file(patch)} for patch in patches
        ],
    }
