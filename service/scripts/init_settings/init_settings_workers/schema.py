"""Validate and normalize the versioned external settings schema."""

from __future__ import annotations


PACKAGE_NAME = "fpf"
REQUIRED_SECTIONS = {"package", "paths", "skills"}
LEGACY_SECTIONS = {"paths", "skills"}
REQUIRED_PACKAGE_KEYS = {"name", "version"}
REQUIRED_PATH_KEYS = {"fpf_original_repo"}
RUNTIME_SKILL_KEYS = (
    "output_language", "output_style", "fpf_terms_explained", "save_report", "report_style",
)
REQUIRED_SKILL_KEYS = set(RUNTIME_SKILL_KEYS) | {"install_method"}
ALLOWED_SKILL_VALUES = {
    "output_language": {"auto", "en", "ru"},
    "output_style": {"natural", "general", "ste"},
    "fpf_terms_explained": {"full", "short", "off"},
    "save_report": {"on", "off"}, "report_style": {"plain", "caprmedio"},
    "install_method": {"copy", "symlink"},
}


def _package_state(package: object, current_version: str) -> tuple[str, bool]:
    if package is None:
        return current_version, True
    if not isinstance(package, dict) or set(package) != REQUIRED_PACKAGE_KEYS:
        raise ValueError("[package] must contain exactly name and version")
    if package.get("name") != PACKAGE_NAME:
        raise ValueError(f"[package].name must be {PACKAGE_NAME}")
    version = package.get("version")
    if not isinstance(version, str) or not version.strip():
        raise ValueError("[package].version must be a non-empty string")
    return version, version != current_version


def validated_settings(
    settings: dict[str, object], current_version: str,
    defaults: dict[str, object] | None = None,
) -> tuple[dict[str, dict[str, str]], bool, str]:
    if set(settings) not in (REQUIRED_SECTIONS, LEGACY_SECTIONS):
        raise ValueError("control panel must contain [package], [paths], and [skills]")
    old_version, package_migration = _package_state(settings.get("package"), current_version)
    paths, skills = settings.get("paths"), settings.get("skills")
    if not isinstance(paths, dict) or set(paths) != REQUIRED_PATH_KEYS:
        raise ValueError("[paths] must contain exactly fpf_original_repo")
    if not isinstance(skills, dict) or set(skills) - REQUIRED_SKILL_KEYS:
        raise ValueError("[skills] must contain only the six suite settings")
    missing = REQUIRED_SKILL_KEYS - set(skills)
    default_skills = defaults.get("skills") if isinstance(defaults, dict) else None
    if missing and (not isinstance(default_skills, dict) or not missing.issubset(default_skills)):
        raise ValueError(f"cannot migrate missing [skills] settings: {', '.join(sorted(missing))}")
    normalized = {
        "package": {"name": PACKAGE_NAME, "version": current_version},
        "paths": dict(paths), "skills": {**skills, **{key: default_skills[key] for key in missing}},
    }
    if any(not all(isinstance(value, str) for value in section.values()) for section in normalized.values()):
        raise ValueError("control-panel values must be strings")
    for key, choices in ALLOWED_SKILL_VALUES.items():
        if normalized["skills"].get(key) not in choices:
            raise ValueError(f"{key} must be one of: {', '.join(sorted(choices))}")
    return normalized, package_migration or bool(missing), old_version
