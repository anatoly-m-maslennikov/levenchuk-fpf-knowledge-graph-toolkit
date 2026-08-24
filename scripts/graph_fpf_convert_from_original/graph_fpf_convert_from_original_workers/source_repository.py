"""Validate and identify a canonical framework source revision."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.models import FPF_PROFILE


CANONICAL_REMOTE_RE = re.compile(r"(?:^|[/:])ailev/FPF(?:\.git)?$")


def git(repo: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *arguments], check=False,
        capture_output=True, text=True,
    )
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        raise ValueError(f"git {' '.join(arguments)} failed in {repo}: {detail}")
    return result.stdout.strip()


def _canonical_remote(repo: Path) -> str:
    lines = git(repo, "remote", "-v").splitlines()
    urls = {line.split()[1] for line in lines if len(line.split()) >= 2}
    canonical = sorted(url for url in urls if CANONICAL_REMOTE_RE.search(url))
    if not canonical:
        raise ValueError("configured source repository has no remote for ailev/FPF")
    return canonical[0]


def _source_revision(repo: Path, relative: str, scope: str) -> str:
    if scope == "repository":
        return git(repo, "rev-parse", "HEAD")
    if scope == "source-file":
        return git(repo, "log", "-1", "--format=%H", "--", relative)
    raise ValueError(f"unsupported revision scope: {scope}")


def canonical_source_revision(
    source: Path, *, expected_filename: str = FPF_PROFILE.default_source,
    source_label: str = FPF_PROFILE.label, revision_scope: str = "repository",
) -> tuple[Path, str, str]:
    if not source.is_file():
        raise ValueError(f"{source_label} source is not a file: {source}")
    repo = Path(git(source.parent, "rev-parse", "--show-toplevel")).resolve()
    expected_source = repo / expected_filename
    if source.resolve() != expected_source.resolve():
        raise ValueError(f"configured source must be the original repository {expected_filename}: {expected_source}")
    remote = _canonical_remote(repo)
    relative = source.resolve().relative_to(repo).as_posix()
    git(repo, "ls-files", "--error-unmatch", relative)
    if git(repo, "status", "--porcelain", "--", relative):
        raise ValueError(f"configured {expected_filename} has local changes; refresh requires the exact committed source")
    revision = _source_revision(repo, relative, revision_scope)
    committed = git(repo, "rev-parse", f"{revision}:{relative}")
    if git(repo, "hash-object", str(source)) != committed:
        raise ValueError(f"configured {expected_filename} bytes do not match the source revision")
    return repo, revision, remote
