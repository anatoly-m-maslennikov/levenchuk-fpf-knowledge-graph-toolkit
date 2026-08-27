"""Check that Python tooling has no second settings authority."""

from pathlib import Path


ALLOWED_LEGACY_DETECTORS = {
    "service/validate_repository/validate_repository_workers/control_panel.py",
    "service/validate_repository/validate_repository_workers/smoke.py",
}
SELF = "service/validate_script_architecture/validate_script_architecture_workers/settings.py"


def check_settings_authority(files: list[Path], root: Path) -> list[str]:
    errors: list[str] = []
    for path in files:
        relative = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        if relative == SELF:
            continue
        if "fpf-settings.toml" in text and relative not in ALLOWED_LEGACY_DETECTORS:
            errors.append(f"second settings authority referenced: {relative}")
        if "SOURCE_SETTINGS" in text:
            errors.append(f"skill-local settings constant remains: {relative}")
        if "import tomllib" in text and not relative.startswith("service/init_settings/"):
            errors.append(f"settings parsed outside init_settings: {relative}")
    return errors
