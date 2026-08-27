"""Command-line adapter for framework graph validation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from service.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.models import FPF_PROFILE, PROFILES
from service.init_settings.init_settings import read_fpf_source
from ..validate_fpf_graph import validate_graph


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=sorted(PROFILES), default=FPF_PROFILE.key)
    parser.add_argument("--graph")
    parser.add_argument("--source")
    return parser.parse_args()


def _run(args: argparse.Namespace) -> dict[str, object]:
    profile = PROFILES[args.profile]
    if args.source:
        source = Path(args.source).expanduser().resolve()
    else:
        fpf_source, _ = read_fpf_source()
        source = fpf_source.parent / profile.default_source
    graph = Path(args.graph or profile.default_output).expanduser().resolve()
    return validate_graph(graph, source, profile)


def main() -> int:
    try:
        result = _run(_arguments())
    except (OSError, ValueError) as exc:
        result = dict(errors=[str(exc)], warnings=[])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["errors"] else 0
