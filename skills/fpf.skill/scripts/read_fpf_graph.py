#!/usr/bin/env python3
"""Return only the requested command nodes from the FPF YAML graph."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
previous_bytecode_policy = sys.dont_write_bytecode
sys.dont_write_bytecode = True
from fpf_runtime_cache import configure_runtime_cache
configure_runtime_cache(SKILL_ROOT)
sys.dont_write_bytecode = previous_bytecode_policy

from route_fpf_workers.graph import graph_view, load_graph


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--node", action="append", required=True, help="command node ID; repeatable")
    parser.add_argument("--profile", action="append", default=[], help="task-profile ID; repeatable")
    args = parser.parse_args()
    try:
        output = graph_view(load_graph(SKILL_ROOT), args.node, args.profile)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
