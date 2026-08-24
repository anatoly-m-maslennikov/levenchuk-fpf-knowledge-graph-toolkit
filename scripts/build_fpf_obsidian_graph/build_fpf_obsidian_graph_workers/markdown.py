from __future__ import annotations

import re

from .frontmatter import wiki
from .models import FPF_PROFILE, GraphProfile
from .patterns import BACKTICK_ID_RE, HEADING_RE, ID_RE, SINGLE_ROOT_BACKTICK_ID_RE, SINGLE_ROOT_ID_RE


def demote_headings(body: list[str]) -> list[str]:
    result = []
    for line in body:
        m = HEADING_RE.match(line)
        if not m:
            result.append(line)
            continue
        lvl = len(m.group(1))
        text = m.group(2).strip()
        if lvl == 2:
            result.append("# " + text)
        else:
            result.append("#" * max(2, lvl - 1) + " " + text)
    return result


def split_table_row(line: str) -> list[str]:
    text = line.strip()
    if text.startswith("|"):
        text = text[1:]
    if text.endswith("|"):
        text = text[:-1]

    cells: list[str] = []
    buf: list[str] = []
    in_wikilink = False
    i = 0
    while i < len(text):
        if text.startswith("[[", i):
            in_wikilink = True
            buf.append("[[")
            i += 2
            continue
        if in_wikilink and text.startswith("]]", i):
            in_wikilink = False
            buf.append("]]")
            i += 2
            continue
        if text[i] == "|" and not in_wikilink:
            cells.append("".join(buf))
            buf = []
        else:
            buf.append(text[i])
        i += 1
    cells.append("".join(buf))
    return cells


def strip_wikilink_aliases_in_table_line(line: str) -> str:
    if not line.lstrip().startswith("|"):
        return line
    return re.sub(
        r"\[\[([^\]\|#]+(?:#[^\]\|]+)?)\|[^\]]+\]\]",
        lambda match: f"[[{match.group(1)}]]",
        line,
    )


def is_table_separator(line: str) -> bool:
    if "|" not in line:
        return False
    cells = split_table_row(line)
    return len(cells) >= 2 and all(re.fullmatch(r"\s*:?-{3,}:?\s*", cell or "") for cell in cells)


def render_table_row(cells: list[str], is_separator: bool = False) -> str:
    if is_separator:
        rendered = []
        for cell in cells:
            c = cell.strip()
            rendered.append(c if re.fullmatch(r":?-{3,}:?", c) else "---")
        return "| " + " | ".join(rendered) + " |"
    return "| " + " | ".join(cell.strip() for cell in cells) + " |"


def remove_empty_table_columns_from_block(block: list[str]) -> list[str]:
    rows = [split_table_row(line) for line in block]
    separator_rows = {i for i, line in enumerate(block) if is_table_separator(line)}
    width = max((len(row) for row in rows), default=0)
    if width <= 1:
        return block
    for row in rows:
        row.extend([""] * (width - len(row)))

    content_row_indexes = [i for i in range(1, len(rows)) if i not in separator_rows]
    if not content_row_indexes:
        return block
    empty_columns = set()
    for col in range(width):
        if all(rows[row_idx][col].strip() == "" for row_idx in content_row_indexes):
            empty_columns.add(col)
    if not empty_columns:
        return block

    keep = [col for col in range(width) if col not in empty_columns]
    if not keep:
        return block
    cleaned = []
    for idx, row in enumerate(rows):
        kept_cells = [row[col] for col in keep]
        cleaned.append(render_table_row(kept_cells, idx in separator_rows))
    return cleaned


def remove_empty_table_columns(lines: list[str]) -> list[str]:
    """Remove markdown table columns that are empty in every content row."""
    out: list[str] = []
    i = 0
    while i < len(lines):
        if i + 1 < len(lines) and "|" in lines[i] and is_table_separator(lines[i + 1]):
            j = i + 2
            while j < len(lines) and lines[j].strip() and "|" in lines[j]:
                j += 1
            out.extend(remove_empty_table_columns_from_block(lines[i:j]))
            i = j
        else:
            out.append(lines[i])
            i += 1
    return out


def linkify_line(
    line: str,
    id_to_page: dict[str, str],
    profile: GraphProfile = FPF_PROFILE,
) -> str:
    protected: list[str] = []
    in_table = line.lstrip().startswith("|")
    def hold(value: str) -> str:
        protected.append(value)
        return f"@@P{len(protected)-1}@@"
    def protect(match: re.Match[str]) -> str:
        return hold(match.group(0))
    def linked_ref(ref: str) -> str:
        return wiki(id_to_page[ref]) if in_table else wiki(id_to_page[ref], ref)
    line = re.sub(r"\[\[[^\]]+\]\]", protect, line)
    line = re.sub(r"\[[^\]]+\]\([^\)]+\)", protect, line)
    def repl_backtick(match: re.Match[str]) -> str:
        ref = match.group(1)
        return hold(linked_ref(ref)) if ref in id_to_page else match.group(0)
    backtick_id_re = BACKTICK_ID_RE if profile.multi_root_relations else SINGLE_ROOT_BACKTICK_ID_RE
    plain_id_re = ID_RE if profile.multi_root_relations else SINGLE_ROOT_ID_RE
    line = backtick_id_re.sub(repl_backtick, line)

    def repl_plain(match: re.Match[str]) -> str:
        ref = match.group(1)
        if ref not in id_to_page:
            return ref
        prefix = " " if match.start() > 0 and match.string[match.start() - 1] == "[" else ""
        return prefix + linked_ref(ref)

    line = plain_id_re.sub(repl_plain, line)
    for i, value in enumerate(protected):
        line = line.replace(f"@@P{i}@@", value)
    return strip_wikilink_aliases_in_table_line(line)
