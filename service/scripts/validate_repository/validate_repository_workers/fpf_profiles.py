"""Validate FPF Help areas, task profiles, and profile evaluation cases."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path


BindingValidator = Callable[[Path, str, object], list[str]]


def _validate_areas(root: Path, manifest: dict[str, object]) -> tuple[list[str], list[str]]:
    areas = manifest.get("areas", [])
    area_ids = [area.get("id") for area in areas if isinstance(area, dict)]
    errors = [] if set(area_ids) == {"framework", "software", "skills"} and len(area_ids) == 3 else [
        "FPF Help areas must be exactly framework, software, and skills"
    ]
    for area in areas if isinstance(areas, list) else []:
        prompts = area.get("help_prompts", {}) if isinstance(area, dict) else {}
        if set(prompts) != {"en", "ru"}:
            errors.append(f"FPF Help area prompts are invalid: {area.get('id')}")
        for relative in prompts.values() if isinstance(prompts, dict) else []:
            if not isinstance(relative, str) or not (root / "skills/fpf.skill" / relative).is_file():
                errors.append(f"FPF Help area prompt is missing: {relative}")
    return errors, area_ids


def _validate_profile(
    root: Path, profile: dict[str, object], area_ids: list[str],
    analytical: set[str], validate_binding: BindingValidator,
) -> list[str]:
    profile_id = str(profile.get("id"))
    errors = [] if profile.get("area") in area_ids else [
        f"FPF task profile area is invalid: {profile_id}"
    ]
    examples = profile.get("examples", [])
    if not isinstance(examples, list) or len(examples) < 2:
        errors.append(f"FPF task profile examples are incomplete: {profile_id}")
    for example in examples if isinstance(examples, list) else []:
        if example.get("expected_node") not in analytical or not example.get("text"):
            errors.append(f"FPF task profile example is invalid: {profile_id}")
    bindings = profile.get("fpf_entrypoints", [])
    if not isinstance(bindings, list) or not bindings:
        errors.append(f"FPF task profile lacks bindings: {profile_id}")
    for binding in bindings if isinstance(bindings, list) else []:
        if isinstance(binding, dict) and binding.get("relation") != "profile_context":
            errors.append(f"FPF task profile binding relation is invalid: {profile_id}")
        errors.extend(validate_binding(root, profile_id, binding))
    return errors


def _validate_cases(
    manifest: dict[str, object], profile_ids: list[object], analytical: set[str],
) -> list[str]:
    cases = manifest.get("evaluation_cases", [])
    case_profiles = [case.get("profile") for case in cases if isinstance(case, dict)] if isinstance(cases, list) else []
    case_ids = [case.get("id") for case in cases if isinstance(case, dict)] if isinstance(cases, list) else []
    errors = [] if sorted(case_profiles) == sorted(profile_ids) else [
        "FPF profile catalog must provide exactly one evaluation case per profile"
    ]
    if len(case_ids) != len(set(case_ids)) or not all(case_ids):
        errors.append("FPF evaluation case IDs must be unique and non-empty")
    for case in cases if isinstance(cases, list) else []:
        if (
            case.get("profile") not in profile_ids
            or case.get("node") not in analytical
            or not case.get("required_facets")
            or not case.get("forbidden_inference")
        ):
            errors.append(f"FPF evaluation case is invalid: {case.get('id')}")
    return errors


def validate_areas_and_profiles(
    root: Path, manifest: dict[str, object], analytical: set[str],
    validate_binding: BindingValidator,
) -> list[str]:
    errors, area_ids = _validate_areas(root, manifest)
    profiles = manifest.get("task_profiles", [])
    profile_ids = [profile.get("id") for profile in profiles if isinstance(profile, dict)]
    if len(profile_ids) < 20 or len(profile_ids) != len(set(profile_ids)):
        errors.append("FPF task profiles must be unique and provide at least twenty profiles")
    for profile in profiles if isinstance(profiles, list) else []:
        if isinstance(profile, dict):
            errors.extend(_validate_profile(root, profile, area_ids, analytical, validate_binding))
    errors.extend(_validate_cases(manifest, profile_ids, analytical))
    return errors
