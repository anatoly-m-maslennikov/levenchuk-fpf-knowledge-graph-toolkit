"""Derive expected graph state from a canonical source."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from service.scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.assign_names import assign_names
from service.scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.models import FPF_PROFILE, GraphProfile
from service.scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.source_parser import build_pages, parse_headings


CATALOG_ROW_RE = re.compile(
    r"^\|\s*([A-Z][A-Z0-9-]*(?:\.[A-Za-z0-9][A-Za-z0-9-]*)+)\s*\|[^|]*\|\s*([^|]+?)\s*\|"
)


def source_revision(source: Path, profile: GraphProfile = FPF_PROFILE) -> str:
    arguments = ["rev-parse", "HEAD"]
    if profile != FPF_PROFILE:
        arguments = ["log", "-1", "--format=%H", "--", source.name]
    result = subprocess.run(
        ["git", "-C", str(source.parent), *arguments], check=False,
        capture_output=True, text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def expected_markdown_paths(
    source: Path, profile: GraphProfile = FPF_PROFILE,
) -> tuple[set[str], int, int]:
    lines, headings = parse_headings(source)
    hubs, pages = build_pages(lines, headings, profile)
    assign_names(hubs, pages, profile)
    index_files = {f"00_Index/{name}.md" for name in profile.index_files}
    paths = index_files | {f"{hub.page_name}.md" for hub in hubs}
    paths |= {f"{page.page_name}.md" for page in pages}
    return paths, len(hubs), len(pages)


def catalog_statuses(source: Path) -> dict[str, str]:
    statuses: dict[str, str] = {}
    with source.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            match = CATALOG_ROW_RE.match(line)
            if match:
                statuses[match.group(1)] = match.group(2).strip().strip("*")
    return statuses
