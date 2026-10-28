"""Validate CAD-Knowledge-Graph against its configured canonical source."""

import json
from pathlib import Path

from service.scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.models import CAD_PROFILE
from service.scripts.init_settings.init_settings import read_cad_source
from service.scripts.validate_fpf_graph.validate_fpf_graph import validate_graph


ROOT = Path(__file__).resolve().parents[3]
GRAPH = ROOT / CAD_PROFILE.default_output


def main() -> int:
    try:
        source, _ = read_cad_source(create_if_missing=False)
        result = validate_graph(GRAPH, source, CAD_PROFILE)
    except (OSError, ValueError) as exc:
        result = dict(errors=[str(exc)], warnings=[])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["errors"] else 0
