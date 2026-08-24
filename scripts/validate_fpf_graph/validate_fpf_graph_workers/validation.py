"""Coordinate atomic generated-graph checks."""

from __future__ import annotations

from pathlib import Path

from scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.models import FPF_PROFILE, GraphProfile
from .page_checks import check_pages
from .path_scan import compare_paths, scan_graph
from .report_checks import classify_unresolved, expected_values, read_report, validate_report_values
from .source_expectations import expected_markdown_paths


def _failure(message: str) -> dict[str, object]:
    return dict(errors=[message], warnings=[])


def _final_result(
    graph: Path, source: Path, revision: str, markdown: set[str],
    directories: set[str], profile: GraphProfile, identifiers: list[str],
    report: dict[str, object], classified: list[dict[str, object]],
    errors: list[str], warnings: list[str],
) -> dict[str, object]:
    return dict(
        graph=str(graph), source=str(source), source_revision=revision,
        markdown_files=len(markdown), directories=len(directories),
        **{f"{profile.key}_ids": len(identifiers)},
        broken_links=report.get("broken_links_count"),
        unresolved_relations=report.get("unresolved_relations_count"),
        unresolved_relation_classification=classified,
        errors=errors, warnings=warnings,
    )


def validate_generated_graph(
    graph: Path, source: Path, profile: GraphProfile = FPF_PROFILE,
) -> dict[str, object]:
    if not source.is_file():
        return _failure(f"source is not a file: {source}")
    if not graph.is_dir() or graph.is_symlink():
        return _failure(f"graph is not a real directory: {graph}")
    expected, hub_count, page_count = expected_markdown_paths(source, profile)
    report_name = f"{profile.label} - Validation Report.json"
    files, directories, errors, warnings = scan_graph(graph, report_name)
    errors.extend(compare_paths(files, expected, report_name))
    report = read_report(graph, report_name, errors)
    values = expected_values(source, graph, profile, hub_count, page_count, len(expected))
    validate_report_values(report, values, errors)
    classified = classify_unresolved(report, source, errors, warnings)
    markdown = {path for path in files if path.endswith(".md")}
    page_errors, identifiers = check_pages(
        graph, markdown, source, profile,
        str(values["source_revision"]), str(values["source_sha256"]),
    )
    errors.extend(page_errors)
    if len(identifiers) != len(set(identifiers)):
        errors.append(f"generated graph contains duplicate {profile.id_field} values")
    if report.get("ids") != len(identifiers):
        errors.append("validation report ID count does not match generated frontmatter")
    return _final_result(
        graph, source, str(values["source_revision"]), markdown, directories,
        profile, identifiers, report, classified, errors, warnings,
    )
