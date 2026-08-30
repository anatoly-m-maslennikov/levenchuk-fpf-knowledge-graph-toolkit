"""Coordinate script architecture checks."""

from pathlib import Path

from .assets import load_policy
from .ast_rules import check_file
from .layout import (
    check_cache_placement,
    check_layout,
    check_obsolete_boundaries,
    check_service_boundary,
    check_test_placement,
    check_worker_dag,
    tool_directories,
)
from .managers import check_manager
from .settings import check_settings_authority


POLICY_PATH = Path(__file__).parents[1] / "validate_script_architecture_assets" / "policy.json"


def _architecture_files(service: Path, skills: Path, tests: Path) -> list[Path]:
    service_files = [
        path for path in service.rglob("*.py")
        if not path.is_relative_to(tests / "fpf_skill")
    ]
    return sorted([*service_files, *(skills / "install_fpf_skills").rglob("*.py")])


def validate_architecture(root: Path) -> dict[str, object]:
    try:
        policy = load_policy(POLICY_PATH)
    except ValueError as exc:
        return dict(errors=[str(exc)], warnings=[], files=0, tools=0)
    service = root / "service"
    skills = root / "skills"
    tests = service / "tests"
    end_user_installer = skills / "install_fpf_skills"
    files = _architecture_files(service, skills, tests)
    tools = tool_directories(service / "scripts") + [end_user_installer]
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
    errors.extend(check_test_placement(root, tests))
    errors.extend(check_service_boundary(service))
    errors.extend(check_obsolete_boundaries(root))
    errors.extend(check_cache_placement(root))
    errors.extend(check_settings_authority(files, root))
    legacy = sorted(
        path.relative_to(root).as_posix()
        for boundary in (service, skills)
        for path in boundary.rglob("tool.py")
    )
    errors.extend(f"legacy manager filename remains: {path}" for path in legacy)
    return dict(
        errors=errors, warnings=warnings, files=len(files), tools=len(tools),
        preferred_atomic_lines=policy["preferred_atomic_lines"],
        maximum_atomic_lines=policy["maximum_atomic_lines"],
        maximum_python_file_lines=policy["maximum_python_file_lines"],
    )
