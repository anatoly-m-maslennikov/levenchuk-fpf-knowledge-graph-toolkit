"""Validate README links and CI branch governance."""

import re
from pathlib import Path
from urllib.parse import unquote


def validate_readme_links(root: Path) -> list[str]:
    text = (root / "Readme.md").read_text(encoding="utf-8")
    errors: list[str] = []
    for raw in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        if raw.startswith(("http://", "https://", "#")):
            continue
        target = unquote(raw).split("#", 1)[0]
        if not (root / target).exists():
            errors.append(f"README link does not exist: {raw}")
    return errors


def _trigger_branches(text: str, trigger: str, next_trigger: str) -> set[str]:
    match = re.search(
        rf"(?ms)^  {re.escape(trigger)}:\n(?P<body>.*?)(?=^  {re.escape(next_trigger)}:)", text
    )
    return set(re.findall(r"^      - (\S+)$", match.group("body"), re.MULTILINE)) if match else set()


def validate_ci(root: Path, required_fragments: list[str]) -> list[str]:
    text = (root / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    errors: list[str] = []
    if _trigger_branches(text, "push", "pull_request") != {"dev", "main"}:
        errors.append("CI push branches must be exactly dev and main")
    if _trigger_branches(text, "pull_request", "workflow_dispatch") != {"main"}:
        errors.append("CI pull-request base must be exactly main")
    if "am/dev" in text:
        errors.append("CI references retired am/dev")
    errors.extend(f"CI owner auto-merge condition missing: {item}" for item in required_fragments if item not in text)
    return errors
