"""Render subject and evaluator prompts from tracked assets."""

from __future__ import annotations

import json
from pathlib import Path


def subject_prompt(template: Path, case: dict[str, object]) -> str:
    text = template.read_text(encoding="utf-8")
    return text.replace("{{CASE_JSON}}", json.dumps(case, ensure_ascii=False, indent=2))


def evaluator_prompt(
    template: Path, cases: list[dict[str, object]], responses: dict[str, object],
) -> str:
    text = template.read_text(encoding="utf-8")
    payload = {"cases": cases, "subject_responses": responses}
    return text.replace("{{EVALUATION_PAYLOAD_JSON}}", json.dumps(payload, ensure_ascii=False, indent=2))
