from __future__ import annotations

from .models import Page


def folder_part_count_for_page(page: Page, descendant_prefixes: set[str]) -> int:
    parts = page.framework_id.split(".")
    if len(parts) < 2:
        return 0
    if len(parts) == 2 or page.framework_id in descendant_prefixes:
        return len(parts) - 1
    return len(parts) - 2
