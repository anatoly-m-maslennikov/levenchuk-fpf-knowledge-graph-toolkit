"""Command-line adapter for CAD graph conversion."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date

from service.scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.models import CAD_PROFILE
from service.scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.source_repository import canonical_source_revision
from service.scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.source_package import validate_source_package_against_repository
from service.scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original_workers.source_stage import staged_source
from service.scripts.init_settings.init_settings import SETTINGS_PATH, read_cad_source, read_fpf_original_repo
from ..graph_cad_convert_from_original import ROOT, convert_cad_graph


SOURCE_RELATIVE = "DPFs/Engineering DPF Suite/" + CAD_PROFILE.default_source


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
        staged = staged_source(ROOT, SOURCE_RELATIVE)
        return convert_cad_graph(source=staged, generated_on=args.generated_on)
    configured_repo, created = read_fpf_original_repo(create_if_missing=False)
    source, _ = read_cad_source(create_if_missing=False)
    repo, revision, remote = canonical_source_revision(
        source, expected_filename=CAD_PROFILE.default_source,
        source_label=CAD_PROFILE.label, revision_scope="repository",
    )
    if configured_repo != repo:
        raise ValueError(
            f"fpf_original_repo must point to the repository root: "
            f"configured {configured_repo}, actual {repo}"
        )
    validate_source_package_against_repository(ROOT, repo)
    return dict(
        converter="graph-cad-convert-from-original",
        settings=str(SETTINGS_PATH), settings_created=created,
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
