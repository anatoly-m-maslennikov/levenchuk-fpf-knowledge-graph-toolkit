"""Apply graph rendering transformations only outside fenced code blocks."""

from __future__ import annotations

from itertools import groupby

from .markdown import demote_headings, linkify_line, remove_empty_table_columns
from .models import GraphProfile
from .reference_links import unfenced_lines
from .source_links import AnchorTargets, rewrite_source_links


def render_body(
    lines: list[str], current_page: str, id_to_page: dict[str, str], profile: GraphProfile,
    anchor_targets: AnchorTargets | None = None,
    reference_definitions: dict[str, str] | None = None,
    source_file_links: dict[str, str] | None = None,
) -> str:
    result = []
    editable = True
    for editable, group in groupby(unfenced_lines(lines), key=lambda item: item[1]):
        block = [line for line, _ in group]
        if editable:
            block = remove_empty_table_columns(demote_headings(block))
            block = rewrite_source_links(block, current_page, anchor_targets or {}, reference_definitions, source_file_links)
            block = [linkify_line(line, id_to_page, profile) for line in block]
        result.append("\n".join(block))
    if result and editable:
        result[-1] = result[-1].rstrip()
        if not result[-1]:
            result.pop()
    return "\n".join(result) + "\n"
