import subprocess
from pathlib import Path

from scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph import build


SOURCE = "# Part A - Example\n\n## A.1 - First page\n\nA.2 links here.\n\n## A.2 - Second page\n"


def make_graph(root: Path) -> tuple[Path, Path]:
    source_repo = root / "FPF"
    source_repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=source_repo, check=True)
    source = source_repo / "FPF-Spec.md"
    source.write_text(SOURCE, encoding="utf-8")
    subprocess.run(["git", "add", "FPF-Spec.md"], cwd=source_repo, check=True)
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
    graph = root / "FPF-Knowledge-Graph"
    build(source, graph, True, revision, "2026-08-22")
    return source, graph
