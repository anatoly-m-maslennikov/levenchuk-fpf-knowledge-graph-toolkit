"""Read compatible preferences from a legacy installed runtime panel."""

from __future__ import annotations

from pathlib import Path
import tomllib

from .schema import ALLOWED_SKILL_VALUES, RUNTIME_SKILL_KEYS


def read_legacy_runtime_preferences(path: Path) -> dict[str, str]:
    if not path.is_file() or path.is_symlink():
        return {}
    try:
        with path.open("rb") as stream:
            runtime = tomllib.load(stream)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ValueError(f"cannot read legacy runtime settings {path}: {exc}") from exc
    defaults = runtime.get("defaults")
    if not isinstance(defaults, dict):
        raise ValueError(f"legacy runtime settings must contain [defaults]: {path}")
    preferences = {key: value for key, value in defaults.items() if key in RUNTIME_SKILL_KEYS}
    if any(not isinstance(value, str) for value in preferences.values()):
        raise ValueError(f"legacy runtime preference values must be strings: {path}")
    for key, value in preferences.items():
        if value not in ALLOWED_SKILL_VALUES[key]:
            choices = ", ".join(sorted(ALLOWED_SKILL_VALUES[key]))
            raise ValueError(f"legacy {key} must be one of: {choices}")
    return preferences
