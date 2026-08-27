"""Validate the intentionally thin end-user FPF skill package."""

from pathlib import Path

def validate_fpf_skill_package(
    skill_root: Path, text: str, contracts: dict[str, object]
) -> list[str]:
    errors: list[str] = []
    if len(text.splitlines()) > contracts["fpf_skill_max_lines"]:
        errors.append("fpf SKILL.md exceeds the thin-entry line budget")
    for fragment in contracts["fpf_skill_forbidden_fragments"]:
        if fragment in text:
            errors.append(f"fpf SKILL.md contains runtime behavior: {fragment}")
    unprefixed = sorted(
        path.relative_to(skill_root).as_posix()
        for path in skill_root.rglob("*.md")
        if path.name != "SKILL.md" and not path.name.startswith("fpf-")
    )
    errors.extend(f"FPF Markdown resource lacks fpf- prefix: {path}" for path in unprefixed)
    return errors
