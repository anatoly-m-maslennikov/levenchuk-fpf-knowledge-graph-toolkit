"""Command-line adapter for FPF graph conversion."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from service.scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.models import NPF_PROFILE
from service.scripts.init_settings.init_settings import (
    SETTINGS_PATH,
    read_fpf_original_repo,
    read_fpf_source,
    read_npf_source,
)
from ..graph_fpf_convert_from_original import ROOT, convert_graph
from .acceptance import EVIDENCE_RELATIVE, finalize_accepted
from .source_package import (
    package_root,
    validate_source_package_against_repository,
)
from .source_package_refresh import refresh_source_package
from .source_repository import canonical_source_revision
from .source_stage import stage_sources, staged_source


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument(
        "--check-settings", action="store_true",
        help="verify the configured source without changing the graph",
    )
    actions.add_argument(
        "--refresh-source-package", action="store_true",
        help="copy the read-only upstream revision and apply repository patches",
    )
    actions.add_argument(
        "--stage-sources", action="store_true",
        help="copy the verified patched source package into .runtime",
    )
    actions.add_argument(
        "--finalize-accepted", action="store_true",
        help="rerun tests and remove staged originals plus graph backups",
    )
    parser.add_argument(
        "--evaluation-evidence", type=str,
        help=f"PASS evidence JSON (default: {EVIDENCE_RELATIVE.as_posix()})",
    )
    parser.add_argument(
        "--generated-on", default=date.today().isoformat(),
        help="Generation date in YYYY-MM-DD form (default: today)",
    )
    return parser.parse_args()


def _settings_result(created: bool, source, repo, revision: str, remote: str):
    return dict(
        converter="graph-fpf-convert-from-original",
        settings=str(SETTINGS_PATH),
        settings_created=created, source_repository=str(repo),
        source=str(source), source_remote=remote,
        source_revision=revision, source_package=str(package_root(ROOT)),
        status="settings and revision-named source package valid",
    )


def _external_source(*, validate_package: bool = True, create_if_missing: bool = True):
    configured_repo, created = read_fpf_original_repo(
        create_if_missing=create_if_missing,
    )
    source, _ = read_fpf_source(create_if_missing=create_if_missing)
    repo, revision, remote = canonical_source_revision(source)
    if configured_repo != repo:
        raise ValueError(
            f"fpf_original_repo must point to the repository root: "
            f"configured {configured_repo}, actual {repo}"
        )
    npf_source, _ = read_npf_source(create_if_missing=create_if_missing)
    npf_repo, _, _ = canonical_source_revision(
        npf_source, expected_filename=NPF_PROFILE.default_source,
        source_label=NPF_PROFILE.label, revision_scope="source-file",
    )
    if npf_repo != repo:
        raise ValueError(f"NPF source repository mismatch: {npf_repo}")
    if validate_package:
        metadata = validate_source_package_against_repository(ROOT, repo)
        if metadata["upstream_revision"] != revision:
            raise ValueError("patched source package is not based on the configured upstream HEAD")
    return configured_repo, created, source, repo, revision, remote


def _run(args: argparse.Namespace) -> dict[str, object]:
    date.fromisoformat(args.generated_on)
    if args.finalize_accepted:
        evidence = Path(args.evaluation_evidence) if args.evaluation_evidence else None
        if evidence is not None and not evidence.is_absolute():
            evidence = ROOT / evidence
        return finalize_accepted(ROOT, evidence)
    if args.evaluation_evidence:
        raise ValueError("--evaluation-evidence requires --finalize-accepted")
    if not args.check_settings and not args.refresh_source_package and not args.stage_sources:
        source = staged_source(ROOT, "FPF-Spec.md")
        return convert_graph(source=source, generated_on=args.generated_on)
    configured_repo, created, source, repo, revision, remote = _external_source(
        validate_package=not args.refresh_source_package,
        create_if_missing=not args.check_settings,
    )
    if args.check_settings:
        return _settings_result(created, source, repo, revision, remote)
    if args.refresh_source_package:
        return refresh_source_package(ROOT, configured_repo)
    if args.stage_sources:
        return stage_sources(ROOT, configured_repo)
    raise ValueError("no converter action selected")


def main() -> int:
    try:
        result = _run(_arguments())
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0
