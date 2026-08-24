import subprocess
from pathlib import Path

from scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph import build
from scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.models import NPF_PROFILE


SOURCE_NAME = "Narrativization-and-Narrative-Studies-Principles-Framework.md"
SOURCE = "# Narrativization Principles Framework\n\n## NSTD.1 - Source intake\n"


def make_graph(root: Path) -> tuple[Path, Path]:
    source_repo = root / "FPF"
    source_repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=source_repo, check=True)
    source = source_repo / SOURCE_NAME
    source.write_text(SOURCE, encoding="utf-8")
    subprocess.run(["git", "add", SOURCE_NAME], cwd=source_repo, check=True)
    subprocess.run(
        [
            "git", "-c", "user.name=Test", "-c",
            "user.email=test@example.invalid", "commit", "-qm", "source",
        ],
        cwd=source_repo, check=True,
    )
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=source_repo,
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    graph = root / NPF_PROFILE.default_output
    build(source, graph, True, revision, "2026-08-22", NPF_PROFILE)
    return source, graph
