from __future__ import annotations

import re
from pathlib import Path

from .models import FPF_PROFILE, GraphProfile, Heading, Page
from .name_rules import clean_title
from .patterns import CODE_FENCE_RE, HEADING_RE, ID_START_RE
from .relations import enrich


def parse_headings(source: Path) -> tuple[list[str], list[Heading]]:
    lines = source.read_text(encoding="utf-8", errors="replace").splitlines()
    headings: list[Heading] = []
    in_code = False
    for n, line in enumerate(lines, 1):
        if CODE_FENCE_RE.match(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = HEADING_RE.match(line)
        if not m:
            continue
        text = m.group(2).strip()
        # The source contains table rows accidentally shaped like H1 headings: "# | ...".
        if text.startswith("|"):
            continue
        headings.append(Heading(len(m.group(1)), text, n))
    return lines, headings


def h1_page_type(title: str, profile: GraphProfile = FPF_PROFILE) -> str:
    low = clean_title(title).lower()
    if low.startswith("part "):
        return f"{profile.key}-part"
    if low.startswith("cluster "):
        return f"{profile.key}-cluster"
    if "table of content" in low:
        return f"{profile.key}-toc"
    if "readme" in low:
        return f"{profile.key}-readme-hub"
    return f"{profile.key}-hub"


def h2_page_type(page: Page, profile: GraphProfile = FPF_PROFILE) -> str:
    if page.framework_id:
        root = page.framework_id.split(".", 1)[0]
        if root in profile.pattern_roots:
            return f"{profile.key}-pattern"
        return f"{profile.key}-section"
    low = page.title.lower()
    if "glossary" in low:
        return f"{profile.key}-glossary"
    if "index" in low:
        return f"{profile.key}-index-section"
    if "readme" in low:
        return f"{profile.key}-readme-section"
    return f"{profile.key}-knowledge-page"


def split_id_title(text: str) -> tuple[str, str]:
    t = clean_title(text).replace("—", "-").replace("–", "-")
    m = ID_START_RE.match(t)
    if not m:
        return "", t
    return m.group("id"), (m.group("title").strip() or m.group("id"))


def next_line(heading: Heading, headings: list[Heading], stop_levels: set[int], line_count: int) -> int:
    later = [h.line for h in headings if h.line > heading.line and h.level in stop_levels]
    return min(later) - 1 if later else line_count


def build_pages(
    lines: list[str],
    headings: list[Heading],
    profile: GraphProfile = FPF_PROFILE,
) -> tuple[list[Page], list[Page]]:
    h1s = [h for h in headings if h.level == 1]
    h2s = [h for h in headings if h.level == 2]
    hubs: list[Page] = []
    pages: list[Page] = []
    for h in h1s:
        end = next_line(h, headings, {1}, len(lines))
        title = clean_title(h.text)
        hubs.append(
            Page(
                "hub",
                h,
                h.line,
                end,
                lines[h.line:end],
                title=title,
                page_type=h1_page_type(title, profile),
            )
        )
    for h in h2s:
        end = next_line(h, headings, {1, 2}, len(lines))
        parent = max((x for x in h1s if x.line < h.line), key=lambda x: x.line, default=None)
        fid, title = split_id_title(h.text)
        page = Page("page", h, h.line, end, lines[h.line:end], parent_hub=clean_title(parent.text) if parent else "", framework_id=fid, title=title)
        page.page_type = h2_page_type(page, profile)
        enrich(page, profile)
        pages.append(page)
    return hubs, pages
