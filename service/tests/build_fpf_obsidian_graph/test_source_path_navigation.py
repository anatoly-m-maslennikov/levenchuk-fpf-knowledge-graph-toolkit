"""Source-relative publication links must survive graph splitting."""

from __future__ import annotations

import json
from pathlib import Path

from service.scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.graph_io import build_graph
from .test_source_anchor_navigation import generated_page


def verify_source_path_navigation(root: Path) -> None:
    repository = root / "source-publications"
    source = repository / "DPFs" / "Example.md"
    source.parent.mkdir(parents=True)
    (repository / "FPF-Spec.md").write_text("# Core\n", encoding="utf-8")
    (repository / "untracked.md").write_text("Untracked\n", encoding="utf-8")
    (root / "outside.md").write_text("Outside\n", encoding="utf-8")
    source.write_text(
        "# Part A - Example\n\n## A.1 - Source links\n\n"
        "[Core](../FPF-Spec.md#a1), [Core reference][core-ref].\n"
        "[Unknown](../untracked.md), [Outside](../../outside.md).\n"
        "`[Core](../FPF-Spec.md)`\n\n```markdown\n[Core](../FPF-Spec.md)\n```\n"
        "[core-ref]: ../FPF-Spec.md\n", encoding="utf-8",
    )
    metadata = {
        "upstream_repository": "ailev/FPF", "upstream_revision": "a" * 40,
        "tracked_files": [{"path": "FPF-Spec.md"}, {"path": "DPFs/Example.md"}],
    }
    (repository / "source-metadata.json").write_text(json.dumps(metadata), encoding="utf-8")
    output = root / "source-path-navigation"
    build_graph(source, output, True, "b" * 40, "2026-10-25")
    text = generated_page(output, "A.1").read_text(encoding="utf-8")
    pinned = f"https://github.com/ailev/FPF/blob/{'a' * 40}/FPF-Spec.md"
    assert f"[Core]({pinned}#a1)" in text
    assert f"[Core reference]({pinned})" in text
    assert "[Unknown](../untracked.md), [Outside](../../outside.md)" in text
    assert "`[Core](../FPF-Spec.md)`" in text
    assert "```markdown\n[Core](../FPF-Spec.md)\n```" in text
