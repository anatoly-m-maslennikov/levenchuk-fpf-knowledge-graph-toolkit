"""Run deterministic test commands declared in a JSON asset."""

from __future__ import annotations

import json
import hashlib
import subprocess
import sys
from pathlib import Path


DEFAULT_TIMEOUT_SECONDS = 300.0
REQUIRED_CASE_NAMES = {
    "compile", "settings-unit", "settings-preflight", "converter-transaction",
    "graph-validator", "npf-converter", "npf-validator",
    "reproducible-generation", "installer", "fpf-skill-runtime",
    "service-installer-unit", "suite-contract-unit", "methodology-settings-sync",
    "generated-graph", "generated-npf-graph", "eval-pack",
    "skill-graph-compatibility", "repository-integration", "architecture-unit",
    "architecture", "patch-hygiene",
}


def _load_cases(path: Path) -> list[dict[str, object]]:
    cases = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(cases, list) or not cases:
        raise ValueError(f"test case asset must contain a non-empty list: {path}")
    names = [case.get("name") for case in cases if isinstance(case, dict)]
    if len(names) != len(cases) or not all(isinstance(name, str) and name for name in names):
        raise ValueError("every test case must be an object with a non-empty string name")
    if len(names) != len(set(names)):
        raise ValueError("test case names must be unique")
    missing = sorted(REQUIRED_CASE_NAMES - set(names))
    if missing:
        raise ValueError(f"test case asset omits required cases: {missing}")
    return cases


def suite_contract(path: Path) -> dict[str, object]:
    cases = _load_cases(path)
    return {
        "manifest_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "case_names": [str(case["name"]) for case in cases],
    }


def _command(parts: object) -> list[str]:
    if not isinstance(parts, list) or not all(isinstance(item, str) for item in parts):
        raise ValueError("every test command must be a string list")
    return [item.replace("{python}", sys.executable) for item in parts]


def _run_case(case: dict[str, object], root: Path):
    name = case.get("name")
    if not isinstance(name, str):
        raise ValueError("every test case must have a string name")
    timeout = case.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS)
    if not isinstance(timeout, (int, float)) or timeout <= 0:
        raise ValueError(f"{name}: timeout_seconds must be a positive number")
    try:
        completed = subprocess.run(
            _command(case.get("command")), cwd=root, timeout=float(timeout),
            check=False, capture_output=True, text=True,
        )
    except subprocess.TimeoutExpired as exc:
        return dict(
            name=name, returncode=124, timed_out=True,
            stdout_tail=(exc.stdout or "")[-4000:] if isinstance(exc.stdout, str) else "",
            stderr_tail=(exc.stderr or "")[-4000:] if isinstance(exc.stderr, str) else "",
        )
    item = dict(name=name, returncode=completed.returncode)
    if completed.returncode:
        item["stdout_tail"] = completed.stdout[-4000:]
        item["stderr_tail"] = completed.stderr[-4000:]
    return item


def run_suite(root: Path, cases_path: Path) -> dict[str, object]:
    contract = suite_contract(cases_path)
    results = [_run_case(case, root) for case in _load_cases(cases_path)]
    failures = [item["name"] for item in results if item["returncode"]]
    return dict(
        suite="graph-fpf-convert-from-original", cases=len(results),
        case_names=contract["case_names"],
        manifest_sha256=contract["manifest_sha256"],
        failures=failures, results=results,
    )


def main(root: Path, cases_path: Path) -> int:
    result = run_suite(root, cases_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["failures"] else 0
