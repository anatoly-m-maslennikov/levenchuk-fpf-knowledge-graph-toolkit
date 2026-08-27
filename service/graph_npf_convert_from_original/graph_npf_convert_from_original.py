"""Pure manager for NPF graph conversion."""

from __future__ import annotations

from pathlib import Path

from service.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.models import NPF_PROFILE
from service.graph_fpf_convert_from_original.graph_fpf_convert_from_original import (
    ROOT,
    convert_framework_graph,
)


def convert_npf_graph(
    *, source: Path, generated_on: str, root: Path = ROOT,
) -> dict[str, object]:
    return convert_framework_graph(
        profile=NPF_PROFILE, converter_name="graph-npf-convert-from-original",
        require_existing=False, revision_scope="source-file",
        root=root, source=source, generated_on=generated_on,
    )
