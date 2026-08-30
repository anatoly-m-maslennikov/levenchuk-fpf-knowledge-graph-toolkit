"""Validate Markdown Help areas, task profiles, and profile evaluation cases."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path


BindingValidator = Callable[[Path, str, object], list[str]]


def _validate_areas(root: Path, areas: list[object]) -> tuple[list[str], list[object]]:
    errors: list[str] = []
    area_ids = [area.get("id") for area in areas if isinstance(area, dict)]
    if set(area_ids) != {"framework", "software", "skills"} or len(area_ids) != 3:
        errors.append("FPF profile areas must be exactly framework, software, and skills")
    for area in areas:
        relative = area.get("profile_file") if isinstance(area, dict) else None
        if not isinstance(relative, str) or not (root / relative).is_file():
            errors.append(f"FPF Markdown profile file is missing: {relative}")

    return errors, area_ids


def _validate_profiles(
    root: Path, profiles: list[object], area_ids: list[object], analytical: set[str],
    validate_binding: BindingValidator,
) -> tuple[list[str], list[object]]:
    errors: list[str] = []
    profile_ids = [profile.get("id") for profile in profiles if isinstance(profile, dict)]
    if not profile_ids or len(profile_ids) != len(set(profile_ids)):
        errors.append("FPF Markdown task profiles must be present and unique")
    for profile in profiles:
        if not isinstance(profile, dict):
            errors.append("FPF Markdown task profile is not an object")
            continue
        profile_id = str(profile.get("id"))
        if profile.get("area") not in area_ids or not profile_id.startswith(f"{profile.get('area')}."):
            errors.append(f"FPF Markdown task profile area is invalid: {profile_id}")
        if not profile.get("aliases") or not profile.get("keywords") or len(profile.get("examples", [])) < 2:
            errors.append(f"FPF Markdown task profile routing evidence is incomplete: {profile_id}")
        for example in profile.get("examples", []):
            if example.get("expected_node") not in analytical or not example.get("text"):
                errors.append(f"FPF Markdown task profile example is invalid: {profile_id}")
        bindings = profile.get("fpf_entrypoints", [])
        if not bindings:
            errors.append(f"FPF Markdown task profile lacks FPF context: {profile_id}")
        for binding in bindings:
            if binding.get("relation") != "profile_context":
                errors.append(f"FPF Markdown task profile relation is invalid: {profile_id}")
            errors.extend(validate_binding(root, profile_id, binding))

    return errors, profile_ids


def _validate_cases(cases: list[object], profile_ids: list[object], analytical: set[str]) -> list[str]:
    errors: list[str] = []
    case_profiles = [case.get("profile") for case in cases if isinstance(case, dict)]
    case_ids = [case.get("id") for case in cases if isinstance(case, dict)]
    if sorted(case_profiles) != sorted(profile_ids):
        errors.append("FPF Markdown profiles must provide exactly one evaluation case each")
    if len(case_ids) != len(set(case_ids)) or not all(case_ids):
        errors.append("FPF Markdown evaluation case IDs must be unique")
    for case in cases:
        if (
            not isinstance(case, dict) or case.get("node") not in analytical
            or not case.get("task") or not case.get("required_facets")
            or not case.get("forbidden_inference")
        ):
            errors.append(f"FPF Markdown evaluation case is invalid: {case.get('id') if isinstance(case, dict) else case}")
    return errors


def validate_areas_and_profiles(
    root: Path, manifest: dict[str, object], analytical: set[str],
    validate_binding: BindingValidator,
) -> list[str]:
    errors, area_ids = _validate_areas(root, manifest.get("areas", []))
    profile_errors, profile_ids = _validate_profiles(
        root, manifest.get("task_profiles", []), area_ids, analytical, validate_binding,
    )
    errors.extend(profile_errors)
    errors.extend(_validate_cases(manifest.get("evaluation_cases", []), profile_ids, analytical))
    return errors
