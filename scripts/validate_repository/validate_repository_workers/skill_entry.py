"""Validate the intentionally thin end-user FPF entry skill."""


def validate_thin_fpf_skill(text: str, contracts: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if len(text.splitlines()) > contracts["fpf_skill_max_lines"]:
        errors.append("fpf SKILL.md exceeds the thin-entry line budget")
    for fragment in contracts["fpf_skill_forbidden_fragments"]:
        if fragment in text:
            errors.append(f"fpf SKILL.md contains doer behavior: {fragment}")
    return errors
