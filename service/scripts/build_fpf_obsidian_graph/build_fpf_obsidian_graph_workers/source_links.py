"""Resolve source-local Markdown anchors after splitting a source document."""

from __future__ import annotations

from collections import Counter, defaultdict
from html import unescape
import posixpath
import re
from urllib.parse import quote, unquote

from .models import Heading, Page
from .reference_links import expand_reference_links, unfenced_lines
from .source_paths import rewrite_source_file_links


AnchorTargets = dict[str, tuple[str, str]]
LOCAL_LINK_RE = re.compile(r"(?<!!)(\[(?:\\.|[^\]\\])*\])\(\s*(?:<#([^>]+)>|#([^\s)]+))\s*\)")


def heading_slug(text: str) -> str:
    text = re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", lambda m: m[2] or m[1], text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = unescape(text).lower().strip()
    return re.sub(r"[^\w -]", "", text).replace(" ", "-")


def numbered_slug(text: str, counts: Counter[str]) -> str:
    slug = heading_slug(text)
    count = counts[slug]
    counts[slug] += 1
    return f"{slug}-{count}" if count else slug


def source_anchor_targets(headings: list[Heading], hubs: list[Page], pages: list[Page]) -> AnchorTargets:
    owners = {page.start: page for page in [*hubs, *pages]}
    source_counts: Counter[str] = Counter()
    generated_counts: dict[str, Counter[str]] = defaultdict(Counter)
    targets: AnchorTargets = {}
    owner = None
    for heading in headings:
        anchor = numbered_slug(heading.text, source_counts)
        if heading.line in owners:
            owner = owners[heading.line]
            targets[anchor] = (owner.page_name, "")
            if owner.kind == "hub":
                generated_counts[owner.page_name][heading_slug(owner.title)] += 1
        elif owner is not None:
            fragment = numbered_slug(heading.text, generated_counts[owner.page_name])
            targets[anchor] = (owner.page_name, fragment)
    return targets


def rewrite_local_link(line: str, current_page: str, targets: AnchorTargets) -> str:
    def replace(match: re.Match[str]) -> str:
        anchor = unquote(match[2] or match[3])
        target = targets.get(anchor)
        if target is None:
            return match[0]
        page, fragment = target
        if page == current_page and fragment == anchor:
            return match[0]
        relative = posixpath.relpath(page + ".md", posixpath.dirname(current_page) or ".")
        destination = quote(relative, safe="/")
        if fragment:
            destination += "#" + quote(fragment, safe="-_")
        return f"{match[1]}({destination})"
    pieces = re.split(r"(`+[^`]*`+)", line)
    return "".join(piece if piece.startswith("`") else LOCAL_LINK_RE.sub(replace, piece) for piece in pieces)


def rewrite_source_links(
    lines: list[str], current_page: str, targets: AnchorTargets,
    reference_definitions: dict[str, str] | None = None,
    source_file_links: dict[str, str] | None = None,
) -> list[str]:
    result = []
    for line, unfenced in unfenced_lines(lines):
        expanded = expand_reference_links(line, reference_definitions or {}) if unfenced else line
        expanded = rewrite_source_file_links(expanded, source_file_links or {}) if unfenced else line
        result.append(rewrite_local_link(expanded, current_page, targets) if unfenced else line)
    return result
