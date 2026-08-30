"""Run structural validators for both generated framework graphs."""

from pathlib import Path

from service.scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.models import FPF_PROFILE, NPF_PROFILE
from service.scripts.init_settings.init_settings import (
    read_fpf_source, read_npf_source, settings_paths_for_root,
)
from service.scripts.validate_fpf_graph.validate_fpf_graph import validate_graph


def _validate_one(root: Path, profile, source: Path):
    result = validate_graph(root / profile.default_output, source, profile)
    errors = [f"{profile.label} graph: {message}" for message in result["errors"]]
    return result, errors


def validate_graphs(root: Path):
    settings, example = settings_paths_for_root(root)
    try:
        fpf_source, _ = read_fpf_source(
            settings, example, create_if_missing=False,
        )
        npf_source, _ = read_npf_source(
            settings, example, create_if_missing=False,
        )
    except (OSError, ValueError) as exc:
        return {}, {}, [f"cannot resolve graph sources: {exc}"]
    fpf_result, fpf_errors = _validate_one(root, FPF_PROFILE, fpf_source)
    npf_result, npf_errors = _validate_one(root, NPF_PROFILE, npf_source)
    return fpf_result, npf_result, fpf_errors + npf_errors
