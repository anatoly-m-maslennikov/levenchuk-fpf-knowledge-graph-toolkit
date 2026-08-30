"""Maintain and verify the repository-owned patched FPF source package."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from service.scripts.filesystem_policy import temporary_workspace

from .source_repository import canonical_source_revision, git


PACKAGE_PREFIX = ".fpf-original-"
METADATA_NAME = "source-metadata.json"
SCHEMA_VERSION = 1
UPSTREAM_REMOTE = "https://github.com/ailev/FPF.git"


def package_root(root: Path) -> Path:
    candidates = sorted(
        path for path in root.glob(f"{PACKAGE_PREFIX}*")
        if path.is_dir() and (path / METADATA_NAME).is_file()
    )
    if len(candidates) != 1:
        raise ValueError(
            f"expected exactly one revision-named patched source package, found {len(candidates)}"
        )
    return candidates[0]


def package_destination(root: Path, revision: str) -> Path:
    return root / f"{PACKAGE_PREFIX}{revision}"


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _read_metadata(directory: Path) -> dict[str, object]:
    path = directory / METADATA_NAME
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read revision-named source metadata: {exc}") from exc
    required = {
        "schema_version", "upstream_repository", "upstream_revision",
        "upstream_remote", "tracked_files", "patches",
    }
    if not isinstance(value, dict) or set(value) != required:
        raise ValueError("source package metadata fields do not match schema 1")
    if value["schema_version"] != SCHEMA_VERSION:
        raise ValueError("source package metadata schema_version must be 1")
    if value["upstream_repository"] != "ailev/FPF":
        raise ValueError("source package metadata names the wrong upstream repository")
    return value


def _records(value: object, label: str) -> list[dict[str, str]]:
    if not isinstance(value, list):
        raise ValueError(f"source package metadata {label} must be a list")
    records: list[dict[str, str]] = []
    for item in value:
        if not isinstance(item, dict) or not all(isinstance(key, str) and isinstance(val, str) for key, val in item.items()):
            raise ValueError(f"invalid source package metadata {label} record")
        records.append(item)
    return records


def validate_source_package(directory: Path) -> dict[str, object]:
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError(f"revision-named source package is missing: {directory}")
    metadata = _read_metadata(directory)
    files = _records(metadata["tracked_files"], "tracked_files")
    patches = _records(metadata["patches"], "patches")
    expected_paths = {METADATA_NAME}
    for record in files:
        if set(record) != {
            "path", "source_revision", "upstream_sha256", "effective_sha256",
        }:
            raise ValueError("invalid source package file record")
        path = directory / record["path"]
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"source package file is missing: {record['path']}")
        if _sha256_file(path) != record["effective_sha256"]:
            raise ValueError(f"source package file digest mismatch: {record['path']}")
        expected_paths.add(record["path"])
    for record in patches:
        if set(record) != {"path", "sha256"}:
            raise ValueError("invalid patched source patch record")
        path = directory / record["path"]
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"source patch is missing: {record['path']}")
        if _sha256_file(path) != record["sha256"]:
            raise ValueError(f"source patch digest mismatch: {record['path']}")
        expected_paths.add(record["path"])
    actual_paths = {
        path.relative_to(directory).as_posix()
        for path in directory.rglob("*")
        if (path.is_file() or path.is_symlink()) and path.name != ".DS_Store"
    }
    if actual_paths != expected_paths:
        raise ValueError("source package contains unrecorded or missing files")
    revision = metadata["upstream_revision"]
    remote = metadata["upstream_remote"]
    if not isinstance(revision, str) or not revision or not isinstance(remote, str) or not remote:
        raise ValueError("source package metadata has invalid upstream identity")
    return metadata


def _git_bytes(repository: Path, revision: str, relative: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repository), "show", f"{revision}:{relative}"],
        check=False, capture_output=True,
    )
    if result.returncode:
        raise ValueError(result.stderr.decode("utf-8", errors="replace").strip())
    return result.stdout


def _apply_patches(directory: Path, patch_paths: list[Path]) -> None:
    for patch in patch_paths:
        result = subprocess.run(
            ["git", "apply", "--no-index", str(patch.resolve())], cwd=directory,
            check=False, capture_output=True, text=True,
        )
        if result.returncode:
            detail = result.stderr.strip() or result.stdout.strip()
            raise ValueError(f"source patch does not apply cleanly: {patch.name}: {detail}")


def validate_source_package_against_repository(
    root: Path, repository: Path,
) -> dict[str, object]:
    directory = package_root(root)
    metadata = validate_source_package(directory)
    revision = str(metadata["upstream_revision"])
    if directory.name != f"{PACKAGE_PREFIX}{revision}":
        raise ValueError("source package folder does not include its full upstream HEAD")
    _, head, _ = canonical_source_revision(repository / "FPF-Spec.md")
    if revision != head:
        raise ValueError("source package is not based on the configured upstream HEAD")
    tracked = git(repository, "ls-tree", "-r", "--name-only", revision).splitlines()
    records = _records(metadata["tracked_files"], "tracked_files")
    if [record["path"] for record in records] != tracked:
        raise ValueError("source package file set differs from the recorded upstream revision")
    with temporary_workspace(prefix="fpf-source-verify-") as name:
        candidate = Path(name) / "candidate"
        candidate.mkdir()
        for record in records:
            relative = record["path"]
            base = _git_bytes(repository, revision, relative)
            if _sha256_bytes(base) != record["upstream_sha256"]:
                raise ValueError(f"upstream source digest mismatch: {relative}")
            target = candidate / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(base)
        patch_paths = [directory / record["path"] for record in _records(metadata["patches"], "patches")]
        _apply_patches(candidate, patch_paths)
        for record in records:
            if (candidate / record["path"]).read_bytes() != (directory / record["path"]).read_bytes():
                raise ValueError(f"stored effective source differs from patch result: {record['path']}")
    return metadata


def source_identity(
    source: Path, *, expected_filename: str, source_label: str,
    revision_scope: str,
) -> tuple[Path, str, str]:
    if (source.parent / METADATA_NAME).is_file():
        metadata = validate_source_package(source.parent)
        if source.name != expected_filename:
            raise ValueError(f"expected {expected_filename}, got {source.name}")
        revision = str(metadata["upstream_revision"])
        if revision_scope == "source-file":
            records = _records(metadata["tracked_files"], "tracked_files")
            revision = next(
                record["source_revision"] for record in records
                if record["path"] == expected_filename
            )
        return source.parent.resolve(), revision, str(metadata["upstream_remote"])
    return canonical_source_revision(
        source, expected_filename=expected_filename, source_label=source_label,
        revision_scope=revision_scope,
    )
