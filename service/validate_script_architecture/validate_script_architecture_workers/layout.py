"""Check tool folder, worker DAG, test, and asset placement."""

from __future__ import annotations

import ast
from pathlib import Path

from .ast_rules import parse_python


def tool_directories(boundary: Path) -> list[Path]:
    return sorted(
        path for path in boundary.iterdir()
        if path.name not in {"skills", "tests"}
        and path.is_dir() and (path / "__init__.py").is_file()
    )


def _worker_dependencies(path: Path, modules: set[str]) -> set[str]:
    dependencies: set[str] = set()
    for node in ast.walk(parse_python(path)):
        if not isinstance(node, ast.ImportFrom) or node.level != 1 or not node.module:
            continue
        first = node.module.split(".", 1)[0]
        if first in modules:
            dependencies.add(first)
    return dependencies


def _has_cycle(graph: dict[str, set[str]]) -> bool:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(name: str) -> bool:
        if name in visiting:
            return True
        if name in visited:
            return False
        visiting.add(name)
        cycle = any(visit(dependency) for dependency in graph[name])
        visiting.remove(name)
        visited.add(name)
        return cycle

    return any(visit(name) for name in graph)


def check_worker_dag(tool: Path) -> list[str]:
    workers = tool / f"{tool.name}_workers"
    if not workers.is_dir():
        return []
    modules = {path.stem for path in workers.glob("*.py") if path.name != "__init__.py"}
    graph = {
        path.stem: _worker_dependencies(path, modules)
        for path in workers.glob("*.py") if path.stem in modules
    }
    return [f"worker dependency cycle: {workers}"] if _has_cycle(graph) else []


def check_layout(tool: Path) -> list[str]:
    errors: list[str] = []
    workers = [path.name for path in tool.iterdir() if path.is_dir() and path.name.endswith("_workers")]
    assets = [path.name for path in tool.iterdir() if path.is_dir() and path.name.endswith("_assets")]
    expected_workers = f"{tool.name}_workers"
    expected_assets = f"{tool.name}_assets"
    if any(name != expected_workers for name in workers):
        errors.append(f"misnamed workers directory in {tool}")
    if any(name != expected_assets for name in assets):
        errors.append(f"misnamed assets directory in {tool}")
    for path in tool.iterdir():
        if path.is_file() and path.suffix != ".py" and path.name != ".DS_Store":
            errors.append(f"non-Python tool asset is outside {expected_assets}: {path}")
    return errors


def check_test_placement(root: Path, tests: Path) -> list[str]:
    return [
        f"test file must live under service/tests: {path}"
        for path in root.rglob("test_*.py") if not path.is_relative_to(tests)
    ]


def check_obsolete_boundaries(root: Path) -> list[str]:
    errors: list[str] = []
    for boundary in (root / "scripts", root / "service" / "scripts"):
        if boundary.exists() and any(path.is_file() for path in boundary.rglob("*")):
            errors.append(f"obsolete scripts boundary contains files: {boundary}")
    return errors


def check_cache_placement(root: Path) -> list[str]:
    errors: list[str] = []
    for boundary in (root / "service", root / "skills"):
        for path in boundary.rglob("*.pyc"):
            errors.append(f"Python bytecode cache must live under .runtime: {path}")
    return errors
