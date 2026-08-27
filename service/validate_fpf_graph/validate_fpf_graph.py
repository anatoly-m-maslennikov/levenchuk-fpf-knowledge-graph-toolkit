"""Pure manager for generated framework graph validation."""

from pathlib import Path

from service.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.models import (
    FPF_PROFILE,
    GraphProfile,
)
from .validate_fpf_graph_workers.validation import validate_generated_graph


def validate_graph(
    graph: Path, source: Path, profile: GraphProfile = FPF_PROFILE,
) -> dict[str, object]:
    return validate_generated_graph(graph, source, profile)
