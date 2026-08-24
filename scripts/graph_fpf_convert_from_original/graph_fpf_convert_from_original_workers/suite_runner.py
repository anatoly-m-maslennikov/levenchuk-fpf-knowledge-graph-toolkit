"""Run deterministic test commands declared in a JSON asset."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def _load_cases(path: Path) -> list[dict[str, object]]:
    cases = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(cases, list):
        raise ValueError(f"test case asset must contain a list: {path}")
    return cases


def _command(parts: object) -> list[str]:
    if not isinstance(parts, list) or not all(isinstance(item, str) for item in parts):
        raise ValueError("every test command must be a string list")
    return [item.replace("{python}", sys.executable) for item in parts]


def _run_case(case: dict[str, object], root: Path, environment: dict[str, str]):
    name = case.get("name")
    if not isinstance(name, str):
        raise ValueError("every test case must have a string name")
    completed = subprocess.run(
        _command(case.get("command")), cwd=root, env=environment,
        check=False, capture_output=True, text=True,
    )
    item = dict(name=name, returncode=completed.returncode)
    if completed.returncode:
        item["stdout_tail"] = completed.stdout[-4000:]
        item["stderr_tail"] = completed.stderr[-4000:]
    return item


def run_suite(root: Path, cases_path: Path) -> dict[str, object]:
    environment = os.environ.copy()
    environment["PYTHONPYCACHEPREFIX"] = str(root / ".runtime" / "pycache")
    results = [_run_case(case, root, environment) for case in _load_cases(cases_path)]
    failures = [item["name"] for item in results if item["returncode"]]
    return dict(
        suite="graph-fpf-convert-from-original", cases=len(results),
        failures=failures, results=results,
    )


def main(root: Path, cases_path: Path) -> int:
    result = run_suite(root, cases_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["failures"] else 0
