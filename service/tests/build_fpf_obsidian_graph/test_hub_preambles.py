"""Keep publication introductions and notices without copying child bodies."""

from __future__ import annotations

from pathlib import Path

from service.scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.graph_io import build_graph
from .test_source_anchor_navigation import generated_page, link_destination


NOTICE = "Copyright 2026 Anatoly Levenchuk. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)."
CODE = "```markdown\n## A.99 - Fenced false child\nA.1\n```\n"
SOURCE = (
    "# Publication\n\n**Edition:** 23 October 2026.\n\nBounded publication introduction.\n\n"
    "[Child](#a1---child), [Notice terms](#terms).\n\n" + CODE
    + "\n## A.1 - Child\n\nUNIQUE-CHILD-BODY.\n\n"
    "# License\n\n" + NOTICE + "\n\n### Terms\n\nAttribution is required.\n\n"
    "# Final notice\n\nNo further pattern follows this notice.\n"
)


def hub_page(output: Path, title: str) -> Path:
    return next(
        path for path in (output / "00_Hubs").glob("*.md")
        if f'title: "{title}"' in path.read_text(encoding="utf-8")
    )


def verify_hub_preambles(root: Path) -> None:
    source = root / "hub-preambles.md"
    source.write_text(SOURCE, encoding="utf-8")
    output = root / "hub-preambles"
    report = build_graph(source, output, True, "test-preambles", "2026-10-25")
    publication, license_page, final = (hub_page(output, name) for name in ("Publication", "License", "Final notice"))
    text = publication.read_text(encoding="utf-8")
    assert "**Edition:** 23 October 2026." in text
    assert "Bounded publication introduction." in text
    assert CODE in text
    assert "UNIQUE-CHILD-BODY" not in text
    assert f"[Child]({link_destination(publication, generated_page(output, 'A.1'))})" in text
    assert f"[Notice terms]({link_destination(publication, license_page, 'terms')})" in text
    assert NOTICE in license_page.read_text(encoding="utf-8")
    assert "Attribution is required." in license_page.read_text(encoding="utf-8")
    assert "No further pattern follows this notice." in final.read_text(encoding="utf-8")
    assert NOTICE not in final.read_text(encoding="utf-8")
    assert report["ids"] == 1
