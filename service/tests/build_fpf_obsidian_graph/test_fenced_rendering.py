"""Fenced source examples must survive every rendering transformation intact."""

from __future__ import annotations

from pathlib import Path

from service.scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.graph_io import build_graph
from .test_source_anchor_navigation import generated_page


BACKTICKS = """```markdown
## A.99 - A code heading
| ID | Empty |
| --- | --- |
| A.2 | |
[A.2][known]
[A.2](#a2---second-page)
```
"""
TILDES = """~~~mermaid
RA[A.2]
  A.2 --> A.1
~~~
"""
WIDE_FENCE = """````markdown
```shorter-is-not-a-close
## A.98 - Still a code heading
~~~
A.2
````  
"""


def verify_fenced_rendering(root: Path) -> None:
    source = root / "fenced-rendering.md"
    source.write_text(
        "[known]: #a2---second-page\n\n# Part A - Examples\n\n## A.1 - First page\n\nOutside A.2.\n\n"
        + BACKTICKS + TILDES + WIDE_FENCE
        + "\n## A.2 - Second page\n\n" + WIDE_FENCE,
        encoding="utf-8",
    )
    output = root / "fenced-rendering"
    report = build_graph(source, output, True, "test-fences", "2026-10-25")
    first = generated_page(output, "A.1").read_text(encoding="utf-8")
    second = generated_page(output, "A.2").read_text(encoding="utf-8")
    for original in (BACKTICKS, TILDES, WIDE_FENCE):
        assert original in first
    assert second.endswith(WIDE_FENCE)
    assert report["ids"] == 2
    assert "|A.2]]" in first
