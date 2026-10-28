"""Regression checks for source-local links in split graph pages."""

from __future__ import annotations

import posixpath
from pathlib import Path
from urllib.parse import quote

from service.scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.graph_io import build_graph
from service.scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.source_links import heading_slug


SOURCE = """[cross-page]: #a2---second-page

# Part A - Examples

## A.1 - First page

[Hub](#part-a---examples), [Second page](#a2---second-page).
[Shared section](#shared-1), [Nested section](#nested), [Own section](#shared).
[Global reference][cross-page], [cross-page][], [cross-page].
[Case reference][ CROSS-PAGE ], [Unknown reference][absent].
| Destination | Note |
| --- | --- |
| [Same label](#a2---second-page) | Kept |
| [Table reference][cross-page] | Kept |
[Unknown](#absent), [External](https://example.com/#shared-1).
`[Inline example](#a2---second-page)`
`[Reference example][cross-page]`

```markdown
[Code example](#a2---second-page)
[Reference example][cross-page]
[fenced-only]: https://example.com/ignored
```

### Shared

Own section body.

## A.2 - Second page

### Shared

Second shared section.

#### Nested

Nested body.
[cross-page]: https://example.com/duplicate-must-not-win
[fenced-only]
"""


def link_destination(source: Path, target: Path, fragment: str = "") -> str:
    relative = posixpath.relpath(target.as_posix(), source.parent.as_posix())
    return quote(relative, safe="/") + ("#" + fragment if fragment else "")


def generated_page(output: Path, identifier: str) -> Path:
    return next(
        path for path in output.rglob("*.md")
        if f'fpf_id: "{identifier}"' in path.read_text(encoding="utf-8")
    )


def verify_source_anchor_navigation(root: Path) -> None:
    source = root / "source-links.md"
    source.write_text(SOURCE, encoding="utf-8")
    output = root / "anchor-navigation"
    build_graph(source, output, True, "test-links", "2026-10-25")
    first, second = (generated_page(output, identifier) for identifier in ("A.1", "A.2"))
    hub = next((output / "00_Hubs").glob("*.md"))
    text = first.read_text(encoding="utf-8")
    assert f"[Hub]({link_destination(first, hub)})" in text
    page_labels = ("Second page", "Same label", "Global reference", "cross-page", "Case reference", "Table reference")
    for label in page_labels:
        assert f"[{label}]({link_destination(first, second)})" in text, label
    for label, fragment in (("Shared section", "shared"), ("Nested section", "nested")):
        assert f"[{label}]({link_destination(first, second, fragment)})" in text, label
    assert "[Own section](#shared)" in text
    assert "[Unknown](#absent)" in text
    assert "[External](https://example.com/#shared-1)" in text
    assert "`[Inline example](#a2---second-page)`" in text
    assert "`[Reference example][cross-page]`" in text
    assert "[Unknown reference][absent]" in text
    assert "```markdown\n[Code example](#a2---second-page)\n[Reference example][cross-page]" in text
    assert "[fenced-only]" in second.read_text(encoding="utf-8")
    assert heading_slug("[A.1](url) and `words` & more") == "a1-and-words--more"
