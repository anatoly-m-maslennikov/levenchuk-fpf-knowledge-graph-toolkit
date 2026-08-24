"""Inspect generated graph filesystem structure."""

from __future__ import annotations

import re
import unicodedata
from collections import Counter
from pathlib import Path


BAD_SEGMENT_RE = re.compile(r'[<>:"\\|?*\x00-\x1f]')
DASH_LIKE = {"\u2010", "\u2011", "\u2012", "\u2013", "\u2014", "\u2212"}


def _segment_errors(relative: str, segment: str) -> list[str]:
    errors: list[str] = []
    if segment != segment.strip(" ."):
        errors.append(f"path segment has leading or trailing space/dot: {relative}")
    if BAD_SEGMENT_RE.search(segment):
        errors.append(f"path segment contains a filesystem-unsafe character: {relative}")
    if any(character in DASH_LIKE for character in segment):
        errors.append(f"path segment contains a non-normalized dash: {relative}")
    if unicodedata.normalize("NFC", segment) != segment:
        errors.append(f"path segment is not NFC-normalized: {relative}")
    if len(segment.encode("utf-8")) > 240:
        errors.append(f"path segment exceeds 240 UTF-8 bytes: {relative}")
    return errors


def _inspect_entry(path: Path, graph: Path, report_name: str):
    relative = path.relative_to(graph).as_posix()
    errors: list[str] = []
    for segment in path.relative_to(graph).parts:
        errors.extend(_segment_errors(relative, segment))
    if path.is_symlink():
        return "unsupported", relative, errors + [f"symlink is not allowed in generated graph: {relative}"]
    if path.is_dir():
        return "directory", relative, errors
    if not path.is_file():
        return "unsupported", relative, errors + [f"unsupported filesystem entry: {relative}"]
    if path.name.startswith("."):
        errors.append(f"hidden file in generated graph: {relative}")
    if relative != f"00_Index/{report_name}" and path.suffix != ".md":
        errors.append(f"unexpected generated file type: {relative}")
    return "file", relative, errors


def scan_graph(graph: Path, report_name: str):
    files: set[str] = set()
    directories: set[str] = set()
    errors: list[str] = []
    warnings: list[str] = []
    casefold_paths: Counter[str] = Counter()
    for path in sorted(graph.rglob("*")):
        relative = path.relative_to(graph).as_posix()
        if path.is_file() and path.name == ".DS_Store":
            warnings.append(f"ignored operating-system metadata: {relative}")
            continue
        if path.is_dir() and not any(path.iterdir()):
            warnings.append(f"ignored empty managed-filesystem directory shell: {relative}")
            continue
        kind, relative, entry_errors = _inspect_entry(path, graph, report_name)
        errors.extend(entry_errors)
        if kind == "directory":
            directories.add(relative)
        elif kind == "file":
            files.add(relative)
            casefold_paths[relative.casefold()] += 1
    errors.extend(
        f"case-insensitive path collision: {path}"
        for path, count in sorted(casefold_paths.items()) if count > 1
    )
    return files, directories, errors, warnings


def compare_paths(actual: set[str], expected_markdown: set[str], report_name: str) -> list[str]:
    errors = [
        f"missing generated Markdown path: {path}"
        for path in sorted(expected_markdown - {item for item in actual if item.endswith('.md')})
    ]
    actual_markdown = {path for path in actual if path.endswith(".md")}
    errors.extend(
        f"unexpected or misplaced Markdown path: {path}"
        for path in sorted(actual_markdown - expected_markdown)
    )
    expected_files = expected_markdown | {f"00_Index/{report_name}"}
    errors.extend(
        f"unexpected generated file: {path}"
        for path in sorted(actual - expected_files) if not path.endswith(".md")
    )
    return errors
