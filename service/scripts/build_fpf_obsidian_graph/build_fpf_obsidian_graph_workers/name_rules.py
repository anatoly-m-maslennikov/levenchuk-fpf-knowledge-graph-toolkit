from __future__ import annotations

import re

from .models import Page
from .patterns import BAD_FILENAME_CHARS, MAX_NAME
from .tree_rules import folder_part_count_for_page


def clean_title(text: str) -> str:
    return text.replace("**", "").replace("__", "").strip()


def safe_name(text: str) -> str:
    s = clean_title(text).replace("\u00a0", " ")
    # Normalize Unicode dash-like characters in filenames. Obsidian can handle
    # them, but git/status output may show bytes such as \342\200\221 for
    # U+2011 non-breaking hyphen, which is hard to read and type.
    s = s.translate(str.maketrans({
        "\u2010": "-",  # hyphen
        "\u2011": "-",  # non-breaking hyphen
        "\u2012": "-",  # figure dash
        "\u2013": "-",  # en dash
        "\u2014": "-",  # em dash
        "\u2212": "-",  # minus sign
    }))
    s = re.sub(r"[`*_]+", "", s)
    s = "".join("-" if c in BAD_FILENAME_CHARS else c for c in s)
    s = re.sub(r"\s+", " ", s).strip(" .")
    return (s[:MAX_NAME].rstrip(" .") or "Untitled")


def root_id_folder(root_id: str, root_to_part_title: dict[str, str]) -> str:
    """Root folder for an FPF letter, named from the actual H1 Part title.

    Example:
    Part A - Kernel Architecture Cluster -> A_Kernel Architecture Cluster
    Part G - Discipline SoTA Patterns Kit -> G_Discipline SoTA Patterns Kit
    """
    root = safe_name(root_id)
    part_title = root_to_part_title.get(root_id, "")
    return f"{root}_{safe_name(part_title)}" if part_title else root


def source_ordered_page_base(
    page: Page,
    entry_order: dict[tuple[str, str], int],
    descendant_prefixes: set[str],
    unprefixed_order: dict[int, int],
) -> str:
    """Filename base prefixed for reading order within its tree folder."""
    if not page.framework_id:
        return f"{unprefixed_order.get(id(page), 0):02d}_{safe_name(page.title)}"

    parts = page.framework_id.split(".")
    folder_count = folder_part_count_for_page(page, descendant_prefixes)
    if folder_count >= len(parts) - 1:
        parent_for_order = page.framework_id  # owner page inside its own folder
    elif len(parts) == 2:
        parent_for_order = parts[0]
    else:
        parent_for_order = ".".join(parts[: folder_count + 1])
    order = entry_order.get((parent_for_order, page.framework_id), 0)
    return f"{order:02d}_{display_id(page.framework_id)} - {safe_name(page.title)}"


def unprefixed_folder(parent_hub: str) -> str:
    """Route unprefixed H2 pages by the parent H1 found from source lines.

    These are not automatically appendices. If they sit under a Part H1, they
    are Part pages without FPF ids, so keep them in that Part's tree and use
    source-order filename prefixes instead of hiding them in _unprefixed/.
    """
    clean = safe_name(parent_hub)
    low = clean.lower()
    if "readme" in low:
        return "00-readme"
    if "preface" in low:
        return "00-preface"
    m = re.match(r"Part ([A-Z])\s*-\s*(.+)$", clean)
    if m:
        return f"{m.group(1)}_{safe_name(m.group(2))}"
    m = re.match(r"Cluster ([A-Z])\b", clean)
    if m:
        return f"{m.group(1)}"
    return "00-unprefixed/" + clean


def pad_id_part(part: str) -> str:
    """Zero-pad numeric FPF id parts for filesystem sorting."""
    return f"{int(part):02d}" if part.isdigit() else safe_name(part)


def display_id(framework_id: str) -> str:
    """Filesystem-facing id with numeric parts padded: A.1.1 -> A.01.01.

    Part-local .0 intro pages keep their canonical short id: A.0, G.0.
    """
    parts = framework_id.split(".")
    if len(parts) == 2 and parts[1].isdigit() and int(parts[1]) == 0:
        return framework_id
    return ".".join(pad_id_part(part) for part in parts)
