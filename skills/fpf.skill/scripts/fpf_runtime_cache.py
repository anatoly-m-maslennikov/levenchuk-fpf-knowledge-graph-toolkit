"""Route installed-skill bytecode into the toolkit runtime directory."""

import sys
import tomllib
from pathlib import Path


def _repository_root(skill_root: Path) -> Path:
    try:
        settings = tomllib.loads(
            (skill_root / ".fpf-runtime.toml").read_text(encoding="utf-8")
        )
        return Path(settings["repository_root"])
    except (OSError, KeyError, tomllib.TOMLDecodeError):
        local_root = skill_root.parents[1]
        return local_root if (local_root / "pyproject.toml").is_file() else Path.cwd()


def configure_runtime_cache(skill_root: Path) -> None:
    sys.pycache_prefix = str(_repository_root(skill_root) / ".runtime" / "pycache")
