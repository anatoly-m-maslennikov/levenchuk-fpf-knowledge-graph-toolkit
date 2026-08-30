"""Validate semantic verdicts and bind PASS evidence to exact inputs and outputs."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import tempfile

from .cases import load_json, sha256_file


def validate_evaluation(
    evaluation: dict[str, object], cases: list[dict[str, object]],
) -> list[str]:
    expected_cases = {str(case["id"]): case for case in cases}
    failures = _validate_top_level(evaluation)
    failures.extend(_validate_case_results(evaluation, expected_cases))
    failures.extend(_validate_output_contract_checks(evaluation, expected_cases))
    if evaluation.get("verdict") != "PASS":
        failures.append("overall evaluator verdict is not PASS")
    if evaluation.get("verdict") == "PASS" and evaluation.get("weaknesses"):
        failures.append("PASS evaluator result still reports weaknesses")
    if evaluation.get("verdict") == "PASS" and evaluation.get("consolidated_fixes"):
        failures.append("PASS evaluator result still reports fixes")
    return failures


def _validate_top_level(evaluation: dict[str, object]) -> list[str]:
    failures: list[str] = []
    if evaluation.get("verdict") not in {"PASS", "FAIL"}:
        failures.append("evaluator verdict must be PASS or FAIL")
    for field in ("weaknesses", "consolidated_fixes"):
        value = evaluation.get(field)
        if not isinstance(value, list) or any(
            not isinstance(item, str) or not item.strip() for item in value
        ):
            failures.append(f"evaluator {field} must be a list of non-empty strings")
    return failures


def _validate_case_results(
    evaluation: dict[str, object], expected_cases: dict[str, dict[str, object]],
) -> list[str]:
    failures: list[str] = []
    results = evaluation.get("case_results")
    if not isinstance(results, list):
        return ["evaluator omitted case_results"]
    actual_ids = [item.get("case_id") for item in results if isinstance(item, dict)]
    if (
        len(actual_ids) != len(results) or len(results) != len(expected_cases)
        or set(actual_ids) != set(expected_cases)
    ):
        failures.append("evaluator case ids do not exactly match the case pack")
    for result in results:
        failures.extend(_validate_case_result(result, expected_cases))
    return failures


def _validate_case_result(
    result: object, expected_cases: dict[str, dict[str, object]],
) -> list[str]:
    if not isinstance(result, dict):
        return ["evaluator case result must be an object"]
    if result.get("case_id") not in expected_cases:
        return [f"unexpected evaluator case result: {result.get('case_id')!r}"]
    case = expected_cases[str(result["case_id"])]
    criteria = result.get("criteria")
    if not isinstance(criteria, list):
        return [f"{case['id']}: evaluator criteria must be a list"]
    actual_ids = [item.get("criterion_id") for item in criteria if isinstance(item, dict)]
    expected_ids = [str(item["id"]) for item in case["criteria"]]
    failures = []
    if (
        len(actual_ids) != len(criteria) or len(criteria) != len(expected_ids)
        or len(actual_ids) != len(set(actual_ids)) or set(actual_ids) != set(expected_ids)
    ):
        failures.append(f"{case['id']}: criterion ids do not match exactly once")
    if result.get("verdict") not in {"PASS", "FAIL"}:
        failures.append(f"{case['id']}: evaluator verdict must be PASS or FAIL")
    elif result.get("verdict") != "PASS":
        failures.append(f"{case['id']}: evaluator verdict is not PASS")
    criterion_failures = _validate_criteria(str(case["id"]), criteria)
    failures.extend(criterion_failures)
    if result.get("verdict") == "PASS" and criterion_failures:
        failures.append(f"{case['id']}: PASS contradicts one or more criterion results")
    return failures


def _validate_criteria(case_id: str, criteria: list[object]) -> list[str]:
    failures: list[str] = []
    for item in criteria:
        if not isinstance(item, dict):
            failures.append(f"{case_id}: evaluator criterion must be an object")
            continue
        criterion_id = item.get("criterion_id")
        if item.get("verdict") not in {"PASS", "FAIL"}:
            failures.append(f"{case_id}/{criterion_id}: criterion verdict must be PASS or FAIL")
        elif item.get("verdict") != "PASS":
            failures.append(f"{case_id}/{criterion_id}: criterion is not PASS")
        if not isinstance(item.get("evidence"), str) or not str(item["evidence"]).strip():
            failures.append(f"{case_id}/{criterion_id}: criterion evidence is blank")
    return failures


def _validate_output_contract_checks(
    evaluation: dict[str, object], expected_cases: dict[str, dict[str, object]],
) -> list[str]:
    failures: list[str] = []
    contract_checks = evaluation.get("output_contract_checks")
    if not isinstance(contract_checks, list):
        return ["evaluator omitted output_contract_checks"]
    actual_ids = [item.get("case_id") for item in contract_checks if isinstance(item, dict)]
    if (
        len(actual_ids) != len(contract_checks) or len(contract_checks) != len(expected_cases)
        or set(actual_ids) != set(expected_cases)
    ):
        failures.append("evaluator output-contract case ids do not exactly match the case pack")
    for check in contract_checks:
        if not isinstance(check, dict):
            failures.append("evaluator output-contract check must be an object")
            continue
        if check.get("case_id") not in expected_cases:
            failures.append(f"unexpected output-contract check: {check.get('case_id')!r}")
            continue
        case = expected_cases[str(check["case_id"])]
        if check.get("output_contract") != case.get("output_contract"):
            failures.append(f"{case['id']}: evaluator output contract does not match")
        if check.get("verdict") not in {"PASS", "FAIL"}:
            failures.append(f"{case['id']}: output-contract verdict must be PASS or FAIL")
        elif check.get("verdict") != "PASS":
            failures.append(f"{case['id']}: output-contract check is not PASS")
        if not isinstance(check.get("evidence"), str) or not str(check["evidence"]).strip():
            failures.append(f"{case['id']}: output-contract evidence is blank")
    return failures


def build_evidence(
    identity: dict[str, object], evaluation: dict[str, object], outputs: dict[str, Path],
    run_directory: Path, model: str,
) -> dict[str, object]:
    return dict(
        schema_version=1, gate="fpf-skill-quality", verdict="PASS",
        evaluated_at=datetime.now(timezone.utc).isoformat(), model=model,
        identity=identity,
        subject_output_sha256={key: sha256_file(path) for key, path in outputs.items()},
        run_directory=str(run_directory), evaluation=evaluation,
    )


def write_json(path: Path, value: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def check_evidence(path: Path, identity: dict[str, object]) -> list[str]:
    if not path.is_file():
        return ["quality-gate PASS evidence is missing"]
    value = load_json(path)
    if not isinstance(value, dict):
        return ["quality-gate evidence must be a JSON object"]
    failures = []
    if value.get("schema_version") != 1 or value.get("verdict") != "PASS":
        failures.append("quality-gate evidence is not a schema-1 PASS")
    if value.get("identity") != identity:
        failures.append("quality-gate evidence is stale for the skill or eval assets")
    run = Path(str(value.get("run_directory", "")))
    outputs = value.get("subject_output_sha256")
    if not isinstance(outputs, dict):
        failures.append("quality-gate evidence omits subject output digests")
    else:
        for case_id, digest in outputs.items():
            output = run / "subjects" / f"{case_id}.json"
            if not output.is_file() or sha256_file(output) != digest:
                failures.append(f"quality-gate subject output is missing or stale: {case_id}")
    return failures
