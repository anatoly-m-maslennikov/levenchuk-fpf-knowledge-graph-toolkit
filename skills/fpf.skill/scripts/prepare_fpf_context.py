#!/usr/bin/env python3
"""Hydrate bounded FPF context for selected analytical command nodes."""

from __future__ import annotations

import argparse
import json
import sys
import tomllib
from pathlib import Path


SKILL_ROOT = Path(__file__).absolute().parent.parent
previous_bytecode_policy = sys.dont_write_bytecode
sys.dont_write_bytecode = True
from fpf_runtime_cache import configure_runtime_cache
configure_runtime_cache(SKILL_ROOT)
sys.dont_write_bytecode = previous_bytecode_policy

from route_fpf_workers.context import build_context
from route_fpf_workers.graph import load_graph


def _installed_repository_root() -> Path:
    path = SKILL_ROOT / ".fpf-runtime.toml"
    try:
        settings = tomllib.loads(path.read_text(encoding="utf-8"))
        root = settings["repository_root"]
    except (OSError, KeyError, tomllib.TOMLDecodeError) as exc:
        raise ValueError("pass --repository-root or reinstall the skill runtime settings") from exc
    return Path(root)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--node", action="append", required=True, help="analytical node ID; repeatable")
    parser.add_argument("--profile", action="append", default=[], help="task-profile ID; repeatable")
    parser.add_argument("--repository-root", type=Path, help="toolkit repository root")
    parser.add_argument(
        "--include-conditional", action="append", default=[],
        help="conditional FPF ID to materialize; repeatable",
    )
    args = parser.parse_args()
    try:
        root = args.repository_root or _installed_repository_root()
        output = build_context(
            load_graph(SKILL_ROOT), SKILL_ROOT, root.resolve(), args.node,
            set(args.include_conditional), args.profile,
        )
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
