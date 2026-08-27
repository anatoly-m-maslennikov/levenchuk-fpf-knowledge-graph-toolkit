from __future__ import annotations

from collections import defaultdict

from .models import Page
from .name_rules import root_id_folder, safe_name, pad_id_part
from .tree_rules import folder_part_count_for_page


def id_parent(prefix_id: str) -> str:
    parts = prefix_id.split(".")
    return parts[0] if len(parts) == 2 else ".".join(parts[:-1])


def build_id_order_maps(pages: list[Page]) -> tuple[dict[tuple[str, str], int], dict[str, int], set[str]]:
    """Return source-order indexes for every tree entry.

    The order is contextual: inside folder C.2, the C.2 page itself and
    immediate child entries C.2.1, C.2.P, C.2.2 are sorted together by their
    original source line.
    """
    prefix_start: dict[str, int] = {}
    exact_start = {page.framework_id: page.start for page in pages if page.framework_id}
    exact_ids = set(exact_start)
    descendant_prefixes: set[str] = set()

    for page in pages:
        if not page.framework_id:
            continue
        parts = page.framework_id.split(".")
        for depth in range(2, len(parts) + 1):
            prefix_id = ".".join(parts[:depth])
            prefix_start[prefix_id] = min(prefix_start.get(prefix_id, page.start), page.start)
            if prefix_id != page.framework_id and prefix_id in exact_ids:
                descendant_prefixes.add(prefix_id)

    children: dict[str, list[str]] = defaultdict(list)
    for prefix_id in prefix_start:
        children[id_parent(prefix_id)].append(prefix_id)

    entry_order: dict[tuple[str, str], int] = {}
    folder_parents = set(children) | exact_ids
    for parent in folder_parents:
        entries = list(children.get(parent, []))
        if parent in exact_start:
            entries.append(parent)
        entries = sorted(set(entries), key=lambda x: (exact_start.get(x, prefix_start.get(x, 10**12)), x))
        for idx, entry_id in enumerate(entries):
            entry_order[(parent, entry_id)] = idx
    return entry_order, prefix_start, descendant_prefixes


def ordered_id_folder(prefix_id: str, title: str, entry_order: dict[tuple[str, str], int]) -> str:
    """Folder segment ordered by source position while preserving id information."""
    last_part = prefix_id.split(".")[-1]
    source_order = f"{entry_order.get((id_parent(prefix_id), prefix_id), 0):02d}"
    id_label = pad_id_part(last_part)
    prefix = source_order if source_order == id_label else f"{source_order}_{id_label}"
    clean = safe_name(title) if title else ""
    return f"{prefix}_{clean}" if clean else prefix


def prefix_folder_for_page(
    page: Page,
    id_to_title: dict[str, str],
    root_to_part_title: dict[str, str],
    entry_order: dict[tuple[str, str], int],
    descendant_prefixes: set[str],
) -> str:
    """Return source-ordered folder path for a generated FPF page."""
    parts = page.framework_id.split(".")
    if len(parts) < 2:
        return ""
    segments = [root_id_folder(parts[0], root_to_part_title)]
    for depth in range(2, folder_part_count_for_page(page, descendant_prefixes) + 2):
        prefix_id = ".".join(parts[:depth])
        owner_title = id_to_title.get(prefix_id, "")
        segments.append(ordered_id_folder(prefix_id, owner_title, entry_order))
    return "/".join(segments)
