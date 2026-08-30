"""Detect deterministic syntax-risk strata for conversion evaluation."""

from __future__ import annotations

import re
from pathlib import Path


STRATA_NAMES = (
    "bracketed-reference-punctuation", "existing-link",
    "markdown-table-generated-links", "fenced-code-heading-or-id",
    "relation-section-variants", "non-ascii-title-or-path",
    "long-or-similar-title", "alphanumeric-or-deep-id",
    "unprefixed-h2-routing", "changed-since-backup",
    "unresolved-placeholder-relation", "top-level-family-root",
)


def _matches(text: str, identifier: str, path: str, title: str, duplicates: set[str], changed: set[str]) -> set[str]:
    matched: set[str] = set()
    lines = text.splitlines()
    if re.search(r"\[[A-Z](?:\.[A-Za-z0-9-]+)+[^\]]*\][,.;:]", text):
        matched.add("bracketed-reference-punctuation")
    if "[[" in text or re.search(r"\[[^\]]+\]\([^)]+\)", text):
        matched.add("existing-link")
    if any(line.lstrip().startswith("|") and "[[" in line for line in lines):
        matched.add("markdown-table-generated-links")
    if re.search(r"```[\s\S]*?(?:^#|[A-Z](?:\.[A-Za-z0-9-]+)+)[\s\S]*?```", text, re.MULTILINE):
        matched.add("fenced-code-heading-or-id")
    if re.search(r"(?im)^(?:##+\s+.*relation|\*\*.*relation.*\*\*|\s*[-*]\s+.*(?:→|->))", text):
        matched.add("relation-section-variants")
    if any(ord(character) > 127 for character in title + path):
        matched.add("non-ascii-title-or-path")
    if len(Path(path).name.encode("utf-8")) > 120 or title.casefold() in duplicates:
        matched.add("long-or-similar-title")
    if re.search(r"[A-Za-z]\d|\d[A-Za-z]", identifier) or identifier.count(".") >= 3:
        matched.add("alphanumeric-or-deep-id")
    if "unprefixed" in path.casefold() or any(part.casefold().startswith(("preface", "readme")) for part in Path(path).parts):
        matched.add("unprefixed-h2-routing")
    if identifier in changed:
        matched.add("changed-since-backup")
    if re.search(r"(?i)unresolved|placeholder|\bTBD\b", text):
        matched.add("unresolved-placeholder-relation")
    return matched


def risk_inventory(
    current: Path, current_ids: dict[str, str], current_titles: dict[str, str],
    changed: set[str],
) -> dict[str, dict[str, object]]:
    title_counts: dict[str, int] = {}
    for title in current_titles.values():
        title_counts[title.casefold()] = title_counts.get(title.casefold(), 0) + 1
    duplicates = {title for title, count in title_counts.items() if count > 1}
    strata: dict[str, list[str]] = {name: [] for name in STRATA_NAMES}
    roots: dict[str, str] = {}
    for identifier in sorted(current_ids):
        roots.setdefault(identifier.split(".", 1)[0], identifier)
        path = current_ids[identifier]
        title = current_titles.get(identifier, "")
        text = (current / path).read_text(encoding="utf-8", errors="replace")
        for name in _matches(text, identifier, path, title, duplicates, changed):
            strata[name].append(identifier)
    strata["top-level-family-root"] = sorted(roots.values())
    return {
        name: {
            "population": len(values), "targets": values[:1],
            "status": "populated" if values else "not present in candidate",
        }
        for name, values in strata.items()
    }
