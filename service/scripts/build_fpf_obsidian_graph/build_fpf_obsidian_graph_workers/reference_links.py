"""Carry source-wide Markdown reference links across split page boundaries."""

from __future__ import annotations

import re
from collections.abc import Iterator


DEFINITION_RE = re.compile(r"^\s{0,3}\[([^\]]+)\]:\s*(.+?)\s*$")
REFERENCE_RE = re.compile(r"(?<![!\[])\[([^\[\]\n]+)\](?:[ \t]*\[([^\]\n]*)\])?")
FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})(.*)$")


def unfenced_lines(lines: list[str]) -> Iterator[tuple[str, bool]]:
    fence = ""
    for line in lines:
        match = FENCE_RE.match(line)
        if match:
            marker, suffix = match.groups()
            if not fence:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not suffix.strip():
                fence = ""
            yield line, False
        else:
            yield line, not fence


def reference_label(label: str) -> str:
    return " ".join(label.split()).casefold()


def source_reference_definitions(lines: list[str]) -> dict[str, str]:
    definitions: dict[str, str] = {}
    for line, unfenced in unfenced_lines(lines):
        match = DEFINITION_RE.match(line) if unfenced else None
        if match:
            definitions.setdefault(reference_label(match[1]), match[2])
    return definitions


def expand_reference_links(line: str, definitions: dict[str, str]) -> str:
    if DEFINITION_RE.match(line):
        return line
    def replace(match: re.Match[str]) -> str:
        if match.string[match.end():].startswith("("):
            return match[0]
        label = match[2] or match[1]
        destination = definitions.get(reference_label(label))
        return f"[{match[1]}]({destination})" if destination else match[0]
    pieces = re.split(r"(`+[^`]*`+)", line)
    return "".join(piece if piece.startswith("`") else REFERENCE_RE.sub(replace, piece) for piece in pieces)
