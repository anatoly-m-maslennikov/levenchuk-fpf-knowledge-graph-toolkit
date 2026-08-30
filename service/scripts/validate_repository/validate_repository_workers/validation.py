"""Coordinate bounded repository integration checks."""

from pathlib import Path

from .assets import load_contracts
from .control_panel import validate_control_panel, validate_repository_hygiene
from .docs_ci import validate_ci, validate_readme_links
from .graphs import validate_graphs
from .skills import validate_reference_contracts, validate_routing_scenarios, validate_skill_packages
from .smoke import validate_help, validate_installer, validate_service_installer
from .tooling import validate_tooling


ASSET = Path(__file__).parents[1] / "validate_repository_assets" / "contracts.json"


def validate_repository_state(root: Path) -> dict[str, object]:
    try:
        contracts = load_contracts(ASSET)
    except ValueError as exc:
        return dict(errors=[str(exc)])
    errors: list[str] = []
    errors.extend(validate_control_panel(root, contracts["settings"]))
    errors.extend(validate_repository_hygiene(root))
    errors.extend(validate_tooling(root, contracts["tool_files"]))
    fpf_result, npf_result, graph_errors = validate_graphs(root)
    errors.extend(graph_errors)
    errors.extend(validate_readme_links(root))
    errors.extend(validate_ci(root, contracts["ci_fragments"]))
    errors.extend(validate_skill_packages(root, contracts))
    errors.extend(validate_reference_contracts(root, contracts))
    errors.extend(validate_routing_scenarios(root, contracts["end_user_skills"]))
    errors.extend(validate_help(root))
    errors.extend(validate_installer(
        root, contracts["end_user_skills"], contracts["service_skills"]
    ))
    errors.extend(validate_service_installer(
        root, contracts["end_user_skills"], contracts["service_skills"]
    ))
    return dict(
        errors=errors, markdown_files=fpf_result.get("markdown_files"),
        fpf_ids=fpf_result.get("fpf_ids"), npf_ids=npf_result.get("npf_ids"),
        skill_packages=len(contracts["end_user_skills"]) + len(contracts["service_skills"]),
    )
