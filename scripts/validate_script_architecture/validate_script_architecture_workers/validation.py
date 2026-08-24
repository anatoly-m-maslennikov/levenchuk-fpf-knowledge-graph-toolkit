"""Coordinate script architecture checks."""

from pathlib import Path

from .assets import load_policy
from .ast_rules import check_file
from .layout import check_layout, check_test_placement, check_worker_dag, tool_directories
from .managers import check_manager
from .settings import check_settings_authority


POLICY_PATH = Path(__file__).parents[1] / "validate_script_architecture_assets" / "policy.json"


def validate_architecture(root: Path) -> dict[str, object]:
    try:
        policy = load_policy(POLICY_PATH)
    except ValueError as exc:
        return dict(errors=[str(exc)], warnings=[], files=0, tools=0)
    scripts = root / "scripts"
    files = sorted(scripts.rglob("*.py"))
    tools = tool_directories(scripts)
    errors: list[str] = []
    warnings: list[str] = []
    for path in files:
        file_errors, file_warnings = check_file(path, root, policy)
        errors.extend(file_errors)
        warnings.extend(file_warnings)
    for tool in tools:
        errors.extend(check_manager(tool, policy))
        errors.extend(check_layout(tool))
        errors.extend(check_worker_dag(tool))
    errors.extend(check_test_placement(scripts))
    errors.extend(check_settings_authority(files, root))
    legacy = sorted(path.relative_to(root).as_posix() for path in scripts.rglob("tool.py"))
    errors.extend(f"legacy manager filename remains: {path}" for path in legacy)
    return dict(
        errors=errors, warnings=warnings, files=len(files), tools=len(tools),
        preferred_atomic_lines=policy["preferred_atomic_lines"],
        maximum_atomic_lines=policy["maximum_atomic_lines"],
        maximum_python_file_lines=policy["maximum_python_file_lines"],
    )
