"""CLI orchestration for the local live-model FPF skill quality gate."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

from .cases import gate_identity, load_cases
from .codex_runner import run_codex
from .evidence import build_evidence, check_evidence, validate_evaluation, write_json
from .prompts import evaluator_prompt, subject_prompt


ROOT = Path(__file__).resolve().parents[4]
TOOL = Path(__file__).resolve().parents[1]
ASSETS = TOOL / "fpf_skill_quality_gate_assets"
EVIDENCE = ROOT / ".runtime" / "fpf-skill-quality-evaluation.json"


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="validate current local PASS evidence")
    mode.add_argument("--dry-run", action="store_true", help="validate and print the gate plan")
    parser.add_argument("--model", help="explicit Codex model; default uses the Codex CLI default")
    parser.add_argument("--codex", default="codex", help="Codex CLI executable")
    parser.add_argument("--timeout", type=float, default=900, help="seconds allowed per model turn")
    return parser.parse_args()


def _run_deterministic_suite() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "service.tests.run_tests"], cwd=ROOT,
        text=True, capture_output=True, check=False,
    )
    if completed.returncode:
        raise RuntimeError(f"deterministic suite failed:\n{completed.stdout[-6000:]}")


def _run_subjects(
    cases: list[dict[str, object]], run: Path, args: argparse.Namespace,
) -> tuple[dict[str, object], dict[str, Path]]:
    responses: dict[str, object] = {}
    outputs: dict[str, Path] = {}
    schema = ASSETS / "subject-output.schema.json"
    for case in cases:
        case_id = str(case["id"])
        output = run / "subjects" / f"{case_id}.json"
        response = run_codex(
            subject_prompt(ASSETS / "subject-prompt.md", case), schema, output, ROOT,
            executable=args.codex, model=args.model, timeout=args.timeout,
        )
        if response.get("output_contract") != case.get("output_contract"):
            raise RuntimeError(
                f"subject output contract does not match case: {case_id}"
            )
        responses[case_id] = response
        outputs[case_id] = output
    return responses, outputs


def _run_evaluator(
    cases: list[dict[str, object]], responses: dict[str, object], run: Path,
    args: argparse.Namespace,
) -> dict[str, object]:
    return run_codex(
        evaluator_prompt(ASSETS / "evaluator-prompt.md", cases, responses),
        ASSETS / "evaluation-output.schema.json", run / "evaluation.json", ROOT,
        executable=args.codex, model=args.model, timeout=args.timeout,
    )


def _new_run_directory() -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    parent = ROOT / ".runtime" / "fpf-quality-eval"
    candidate = parent / stamp
    index = 2
    while candidate.exists():
        candidate = parent / f"{stamp}-{index}"
        index += 1
    return candidate


def main() -> int:
    args = _arguments()
    try:
        cases = load_cases(ASSETS / "cases.json")
        identity = gate_identity(ROOT, ASSETS)
        if args.check:
            failures = check_evidence(EVIDENCE, identity)
            print("OK: current local FPF quality-gate evidence" if not failures else "STALE: " + "; ".join(failures))
            return 1 if failures else 0
        if args.dry_run:
            print(json.dumps({"cases": [case["id"] for case in cases], "identity": identity}, indent=2))
            return 0
        _run_deterministic_suite()
        run = _new_run_directory()
        responses, outputs = _run_subjects(cases, run, args)
        evaluation = _run_evaluator(cases, responses, run, args)
        failures = validate_evaluation(evaluation, cases)
        if failures:
            print("FAIL: " + "; ".join(failures), file=sys.stderr)
            print(json.dumps({
                "weaknesses": evaluation.get("weaknesses", []),
                "consolidated_fixes": evaluation.get("consolidated_fixes", []),
                "evaluation": str(run / "evaluation.json"),
            }, ensure_ascii=False, indent=2), file=sys.stderr)
            return 1
        evidence = build_evidence(
            identity, evaluation, outputs, run, args.model or "codex-default",
        )
        write_json(EVIDENCE, evidence)
        print(f"PASS: local FPF skill quality gate ({len(cases)} cases); evidence={EVIDENCE}")
        return 0
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
