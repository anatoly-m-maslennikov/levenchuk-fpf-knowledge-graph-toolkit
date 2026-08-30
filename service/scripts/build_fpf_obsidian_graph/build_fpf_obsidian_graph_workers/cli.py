from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from service.scripts.init_settings.init_settings import read_fpf_source
from ..build_fpf_obsidian_graph import build
from .models import FPF_PROFILE, PROFILES


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=sorted(PROFILES), default=FPF_PROFILE.key)
    parser.add_argument(
        "--source",
        help="Path to the upstream framework source; overrides the external control panel",
    )
    parser.add_argument("--source-revision", required=True, help="Immutable upstream source revision")
    parser.add_argument("--generated-on", required=True, help="Deterministic generation date (YYYY-MM-DD)")
    parser.add_argument("--out")
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()
    profile = PROFILES[args.profile]
    if args.source:
        source = Path(args.source).expanduser().resolve()
    else:
        try:
            fpf_source, _created = read_fpf_source()
            source = fpf_source.parent / profile.default_source
        except ValueError as exc:
            raise SystemExit(f"ERROR: {exc}") from exc
    out_dir = Path(args.out or profile.default_output).resolve()
    if not source.exists():
        raise SystemExit(f"source not found: {source}")
    try:
        date.fromisoformat(args.generated_on)
    except ValueError as exc:
        raise SystemExit("--generated-on must be a valid YYYY-MM-DD date") from exc
    if not args.source_revision.strip():
        raise SystemExit("--source-revision must not be empty")
    report = build(source, out_dir, args.clean, args.source_revision, args.generated_on, profile)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0
