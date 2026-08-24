from __future__ import annotations

import re
from collections import Counter, defaultdict

from .id_tree import build_id_order_maps, prefix_folder_for_page
from .models import FPF_PROFILE, GraphProfile, Page
from .name_rules import safe_name, source_ordered_page_base, unprefixed_folder
from .patterns import HUBS_DIR


def assign_names(
    hubs: list[Page],
    pages: list[Page],
    profile: GraphProfile = FPF_PROFILE,
) -> tuple[dict[str, str], dict[str, str]]:
    used: Counter[str] = Counter()
    id_to_title = {page.framework_id: page.title for page in pages if page.framework_id}
    entry_order, _prefix_start, descendant_prefixes = build_id_order_maps(pages)
    unprefixed_order = _unprefixed_order(pages)
    root_titles = _root_titles(hubs)
    hub_by_title = _assign_hubs(hubs, profile, used)
    id_to_page = _assign_pages(
        pages, id_to_title, root_titles, entry_order, descendant_prefixes, unprefixed_order, used
    )
    return hub_by_title, id_to_page


def _unprefixed_order(pages: list[Page]) -> dict[int, int]:
    grouped: dict[str, list[Page]] = defaultdict(list)
    for page in pages:
        if not page.framework_id:
            grouped[page.parent_hub].append(page)
    return {
        id(page): index
        for siblings in grouped.values()
        for index, page in enumerate(sorted(siblings, key=lambda item: item.start))
    }


def _root_titles(hubs: list[Page]) -> dict[str, str]:
    titles: dict[str, str] = {}
    for hub in hubs:
        m = re.match(r"Part ([A-Z])\s*-\s*(.+)$", safe_name(hub.title))
        if m:
            titles[m.group(1)] = m.group(2).strip()
    return titles


def _assign_hubs(hubs: list[Page], profile: GraphProfile, used: Counter[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for hub in hubs:
        base = f"{HUBS_DIR}/{profile.label} - {safe_name(hub.title)}"
        used[base] += 1
        hub.page_name = base if used[base] == 1 else f"{base} ({used[base]})"
        result[hub.title] = hub.page_name
    return result


def _assign_pages(
    pages: list[Page], id_to_title: dict[str, str], root_titles: dict[str, str],
    entry_order: dict[tuple[str, str], int], descendant_prefixes: set[str],
    unprefixed_order: dict[int, int], used: Counter[str],
) -> dict[str, str]:
    result: dict[str, str] = {}
    for page in pages:
        folder = (
            prefix_folder_for_page(page, id_to_title, root_titles, entry_order, descendant_prefixes)
            if page.framework_id
            else unprefixed_folder(page.parent_hub)
        )
        base = source_ordered_page_base(page, entry_order, descendant_prefixes, unprefixed_order)
        rel = f"{folder}/{base}" if folder else base
        used[rel] += 1
        page.page_name = rel if used[rel] == 1 else f"{rel} ({used[rel]})"
        if page.framework_id:
            result[page.framework_id] = page.page_name
    return result
