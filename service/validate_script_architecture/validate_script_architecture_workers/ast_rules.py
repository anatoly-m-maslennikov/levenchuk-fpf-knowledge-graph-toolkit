"""Check Python file and atomic-object size limits."""

from __future__ import annotations

import ast
from pathlib import Path


ATOMIC_NODES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)


def parse_python(path: Path) -> ast.Module:
    try:
        return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, SyntaxError) as exc:
        raise ValueError(f"cannot parse {path}: {exc}") from exc


def check_file(path: Path, root: Path, policy: dict[str, object]):
    relative = path.relative_to(root).as_posix()
    lines = len(path.read_text(encoding="utf-8").splitlines())
    errors: list[str] = []
    warnings: list[str] = []
    if lines > policy["maximum_python_file_lines"]:
        errors.append(f"Python file exceeds {policy['maximum_python_file_lines']} lines: {relative} ({lines})")
    tree = parse_python(path)
    for node in ast.walk(tree):
        if isinstance(node, ATOMIC_NODES):
            span = (node.end_lineno or node.lineno) - node.lineno + 1
            label = f"{relative}:{node.lineno} {node.name} ({span} lines)"
            if span > policy["maximum_atomic_lines"]:
                errors.append(f"atomic object exceeds {policy['maximum_atomic_lines']} lines: {label}")
            elif span > policy["preferred_atomic_lines"]:
                warnings.append(f"atomic object exceeds preferred {policy['preferred_atomic_lines']} lines: {label}")
        if isinstance(node, ast.Dict) and len(node.keys) >= policy["large_dictionary_entries"]:
            errors.append(f"large dictionary literal must be an asset: {relative}:{node.lineno}")
    return errors, warnings
