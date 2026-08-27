"""Command-line adapter for NPF graph conversion."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date

from service.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.models import NPF_PROFILE
from service.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.source_repository import canonical_source_revision
from service.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.source_package import validate_source_package_against_repository
from service.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.source_stage import staged_source
from service.init_settings.init_settings import read_fpf_original_repo, read_npf_source
from ..graph_npf_convert_from_original import ROOT, convert_npf_graph


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-settings", action="store_true",
        help="verify the configured source without changing the graph",
    )
    parser.add_argument(
        "--generated-on", default=date.today().isoformat(),
        help="Generation date in YYYY-MM-DD form (default: today)",
    )
    return parser.parse_args()


def _run(args: argparse.Namespace) -> dict[str, object]:
    date.fromisoformat(args.generated_on)
    if not args.check_settings:
        staged = staged_source(ROOT, NPF_PROFILE.default_source)
        return convert_npf_graph(source=staged, generated_on=args.generated_on)
    configured_repo, created = read_fpf_original_repo()
    source, _ = read_npf_source()
    repo, revision, remote = canonical_source_revision(
        source, expected_filename=NPF_PROFILE.default_source,
        source_label=NPF_PROFILE.label, revision_scope="source-file",
    )
    if configured_repo != repo:
        raise ValueError(
            f"fpf_original_repo must point to the repository root: "
            f"configured {configured_repo}, actual {repo}"
        )
    package = validate_source_package_against_repository(ROOT, repo)
    return dict(
        converter="graph-npf-convert-from-original",
        settings=str(ROOT / ".caprmedio" / "settings.toml"), settings_created=created,
        source_repository=str(repo), source=str(source), source_remote=remote,
        source_revision=revision, status="settings and source package valid",
    )


def main() -> int:
    try:
        result = _run(_arguments())
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0
