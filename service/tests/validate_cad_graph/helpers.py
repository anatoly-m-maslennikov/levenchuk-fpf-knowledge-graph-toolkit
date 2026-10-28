"""Build a CAD graph with canonical provenance for validation tests."""

from pathlib import Path

from service.scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph import build
from service.scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.models import CAD_PROFILE
from service.tests.graph_cad_convert_from_original.helpers import make_source, run


def make_graph(root: Path) -> tuple[Path, Path]:
    source = make_source(root / "FPF")
    revision = run("git", "rev-parse", "HEAD", cwd=source.parents[2])
    graph = root / CAD_PROFILE.default_output
    build(source, graph, True, revision, "2026-10-25", CAD_PROFILE)
    return source, graph
