"""Validate NPF-Knowledge-Graph against its configured canonical source."""

import json
from pathlib import Path

from service.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.models import NPF_PROFILE
from service.init_settings.init_settings import read_npf_source
from service.validate_fpf_graph.validate_fpf_graph import validate_graph


ROOT = Path(__file__).resolve().parents[2]
GRAPH = ROOT / NPF_PROFILE.default_output


def main() -> int:
    try:
        source, _ = read_npf_source()
        result = validate_graph(GRAPH, source, NPF_PROFILE)
    except (OSError, ValueError) as exc:
        result = dict(errors=[str(exc)], warnings=[])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["errors"] else 0
