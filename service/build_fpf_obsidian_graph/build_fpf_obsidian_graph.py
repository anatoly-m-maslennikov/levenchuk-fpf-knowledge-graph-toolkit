"""Pure manager for graph-building work."""

from __future__ import annotations

from pathlib import Path

from .build_fpf_obsidian_graph_workers.graph_io import build_graph
from .build_fpf_obsidian_graph_workers.models import FPF_PROFILE, GraphProfile


def build(
    source: Path,
    out_dir: Path,
    clean: bool,
    source_revision: str,
    generated_on: str,
    profile: GraphProfile = FPF_PROFILE,
) -> dict[str, object]:
    return build_graph(source, out_dir, clean, source_revision, generated_on, profile)
