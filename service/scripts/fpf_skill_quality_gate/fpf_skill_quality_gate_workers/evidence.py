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
    failures = _validate_case_results(evaluation, expected_cases)
    failures.extend(_validate_output_contract_checks(evaluation, expected_cases))
    if evaluation.get("verdict") != "PASS":
        failures.append("overall evaluator verdict is not PASS")
    if evaluation.get("verdict") == "PASS" and evaluation.get("weaknesses"):
        failures.append("PASS evaluator result still reports weaknesses")
    if evaluation.get("verdict") == "PASS" and evaluation.get("consolidated_fixes"):
        failures.append("PASS evaluator result still reports fixes")
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
    if not isinstance(result, dict) or result.get("case_id") not in expected_cases:
        return []
    case = expected_cases[str(result["case_id"])]
    criteria = result.get("criteria")
    actual = {str(item.get("criterion_id")) for item in criteria or [] if isinstance(item, dict)}
    expected = {str(item["id"]) for item in case["criteria"]}
    failures = [] if actual == expected else [f"{case['id']}: criterion ids do not exactly match"]
    if result.get("verdict") != "PASS":
        failures.append(f"{case['id']}: evaluator verdict is not PASS")
    failures.extend(
        f"{case['id']}/{item.get('criterion_id')}: criterion is not PASS"
        for item in criteria or [] if isinstance(item, dict) and item.get("verdict") != "PASS"
    )
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
        if not isinstance(check, dict) or check.get("case_id") not in expected_cases:
            continue
        case = expected_cases[str(check["case_id"])]
        if check.get("output_contract") != case.get("output_contract"):
            failures.append(f"{case['id']}: evaluator output contract does not match")
        if check.get("verdict") != "PASS":
            failures.append(f"{case['id']}: output-contract check is not PASS")
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
