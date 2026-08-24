"""Check manager naming and zero-I/O boundaries."""

from __future__ import annotations

import ast
from pathlib import Path

from .ast_rules import parse_python


def _imports(tree: ast.Module) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".", 1)[0])
    return names


def _call_name(node: ast.Call) -> str:
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return ""


def check_manager(tool: Path, policy: dict[str, object]) -> list[str]:
    expected = tool / f"{tool.name}.py"
    if not expected.is_file():
        return [f"tool manager must be named {tool.name}.py: {tool}"]
    workers = tool / f"{tool.name}_workers"
    if not workers.is_dir():
        return []
    tree = parse_python(expected)
    relative = expected.as_posix()
    errors = [
        f"manager imports I/O module {name}: {relative}"
        for name in sorted(_imports(tree) & set(policy["manager_forbidden_imports"]))
    ]
    forbidden_calls = set(policy["manager_forbidden_calls"])
    errors.extend(
        f"manager performs I/O call {_call_name(node)}: {relative}:{node.lineno}"
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and _call_name(node) in forbidden_calls
    )
    return errors
