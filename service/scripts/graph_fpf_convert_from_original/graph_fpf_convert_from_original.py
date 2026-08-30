"""Pure manager for transactional framework-to-graph conversion."""

from __future__ import annotations

from pathlib import Path

from service.scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.models import (
    FPF_PROFILE,
    GraphProfile,
)
from .graph_fpf_convert_from_original_workers.transaction import convert_transaction


ROOT = Path(__file__).resolve().parents[3]


def convert_framework_graph(
    *, profile: GraphProfile, converter_name: str, require_existing: bool,
    source: Path, generated_on: str, revision_scope: str = "repository",
    root: Path = ROOT, builder: Path | None = None,
) -> dict[str, object]:
    return convert_transaction(
        profile=profile, converter_name=converter_name,
        require_existing=require_existing, revision_scope=revision_scope,
        root=root, builder=builder, source=source, generated_on=generated_on,
    )


def convert_graph(
    *, source: Path, generated_on: str, root: Path = ROOT,
    builder: Path | None = None,
) -> dict[str, object]:
    return convert_framework_graph(
        profile=FPF_PROFILE, converter_name="graph-fpf-convert-from-original",
        require_existing=True, root=root, builder=builder,
        source=source, generated_on=generated_on,
    )
