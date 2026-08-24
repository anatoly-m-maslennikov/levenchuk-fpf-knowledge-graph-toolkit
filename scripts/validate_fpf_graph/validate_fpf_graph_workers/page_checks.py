"""Validate generated Markdown frontmatter and source ranges."""

from __future__ import annotations

import re
from pathlib import Path

from scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.models import GraphProfile


def source_line_count(source: Path) -> int:
    with source.open(encoding="utf-8", errors="replace") as handle:
        return sum(1 for _ in handle)


def _matching_value(text: str, key: str) -> str | None:
    match = re.search(rf'^{re.escape(key)}: "([^"]+)"$', text, re.MULTILINE)
    return match.group(1) if match else None


def check_page(
    path: Path, relative: str, profile: GraphProfile,
    revision: str, source_sha: str, line_count: int,
) -> tuple[list[str], str | None]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n"):
        return [f"missing YAML frontmatter: {relative}"], None
    if _matching_value(text, "source_revision") != revision:
        errors.append(f"source revision mismatch: {relative}")
    if _matching_value(text, "source_sha256") != source_sha:
        errors.append(f"source SHA-256 mismatch: {relative}")
    identifier = _matching_value(text, profile.id_field)
    line_match = re.search(r"^source_lines:\n  - (\d+)\n  - (\d+)$", text, re.MULTILINE)
    if line_match:
        start, end = map(int, line_match.groups())
        if not 1 <= start <= end <= line_count:
            errors.append(f"source line range is outside source: {relative}")
    return errors, identifier


def check_pages(
    graph: Path, markdown: set[str], source: Path,
    profile: GraphProfile, revision: str, source_sha: str,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    identifiers: list[str] = []
    line_count = source_line_count(source)
    for relative in sorted(markdown):
        page_errors, identifier = check_page(
            graph / relative, relative, profile, revision, source_sha, line_count
        )
        errors.extend(page_errors)
        if identifier:
            identifiers.append(identifier)
    return errors, identifiers
