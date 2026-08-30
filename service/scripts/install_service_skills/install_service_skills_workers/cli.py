"""Command-line adapter for project-local service-skill installation."""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass
from pathlib import Path

from skills.install_fpf_skills.install_fpf_skills_workers.filesystem import replace_package, write_receipt
from service.scripts.filesystem_policy import is_system_temporary_path
from skills.install_fpf_skills.install_fpf_skills_workers.snapshots import suite_digest
from skills.install_fpf_skills.install_fpf_skills_workers.state import can_apply, classify_install, load_receipt
from .catalog import load_catalog, validate_sources


ROOT = Path(__file__).resolve().parents[4]
SOURCE_SKILLS = ROOT / "service/skills"
DEFAULT_DESTINATION = ROOT / ".agents/skills"
CATALOG_PATH = Path(__file__).parents[1] / "install_service_skills_assets/catalog.json"
IGNORED_DESTINATION_ENTRIES = {".DS_Store"}


@dataclass(frozen=True)
class Context:
    method: str
    catalog: dict[str, object]
    names: list[str]
    sources: dict[str, Path]
    targets: dict[str, Path]
    receipt_path: Path
    receipt: dict[str, object]
    state: str
    source_hash: str


def _arguments(arguments: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install repository-service skills into project discovery.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="install or update service skills")
    mode.add_argument("--check", action="store_true", help="verify without writing")
    parser.add_argument("--method", choices=("copy", "symlink"))
    parser.add_argument("--destination", type=Path, help="exact project skills directory")
    return parser.parse_args(arguments)


def _load_context(destination: Path, method: str) -> Context:
    catalog = load_catalog(CATALOG_PATH)
    names = list(catalog["service_skills"])
    sources = validate_sources(SOURCE_SKILLS, names)
    targets = {name: destination / name for name in names}
    receipt_path = destination.parent / str(catalog["receipt_name"])
    receipt = load_receipt(receipt_path)
    state, _ = classify_install(targets, sources, names, receipt)
    return Context(
        method, catalog, names, sources, targets, receipt_path, receipt,
        state, suite_digest(sources, names),
    )


def _unknown_entries(destination: Path, names: list[str]) -> list[str]:
    if not destination.is_dir():
        return []
    allowed = set(names) | IGNORED_DESTINATION_ENTRIES
    return sorted(path.name for path in destination.iterdir() if path.name not in allowed)


def _receipt_current(context: Context) -> bool:
    return context.receipt == {
        "schema_version": context.catalog["schema_version"],
        "method": context.method,
        "source_hash": context.source_hash,
        "skills": context.names,
    }


def _validate_destination(destination: Path, context: Context) -> None:
    unknown = _unknown_entries(destination, context.names)
    if unknown:
        raise ValueError(f"project discovery contains non-service entries: {', '.join(unknown)}")
    if not can_apply(context.method, context.state, context.receipt):
        raise ValueError(f"unmanaged service-skill installation at {destination} (state={context.state})")


def _apply(destination: Path, context: Context) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for name in context.names:
        source = context.sources[name]
        wrapper_symlink = context.method == "symlink" and is_system_temporary_path(
            context.targets[name]
        )
        if context.method == "symlink":
            if not wrapper_symlink:
                try:
                    source = Path(os.path.relpath(source, context.targets[name].parent))
                except ValueError:
                    pass
        replace_package(
            source, context.targets[name], context.method,
            wrapper_symlink=wrapper_symlink,
        )
    write_receipt(context.receipt_path, {
        "schema_version": context.catalog["schema_version"],
        "method": context.method,
        "source_hash": context.source_hash,
        "skills": context.names,
    })


def run_installer(arguments: list[str] | None = None) -> int:
    args = _arguments(arguments)
    destination = (args.destination or DEFAULT_DESTINATION).expanduser().resolve()
    method = args.method
    if method is None and args.check:
        catalog = load_catalog(CATALOG_PATH)
        receipt = load_receipt(destination.parent / str(catalog["receipt_name"]))
        recorded = receipt.get("method")
        method = recorded if recorded in {"copy", "symlink"} else "symlink"
    method = method or "symlink"
    try:
        context = _load_context(destination, method)
        _validate_destination(destination, context)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    current = context.state == f"{context.method}-current" and _receipt_current(context)
    if args.check:
        print(f"{'OK' if current else 'OUT OF DATE'}: service skills: {context.state} at {destination}")
        return 0 if current else 1
    if not args.apply:
        print(f"DRY RUN: service skills: state={context.state}; method={context.method}; destination={destination}")
        return 0
    try:
        _apply(destination, context)
    except OSError as exc:
        print(f"ERROR: service-skill installation failed: {exc}", file=sys.stderr)
        return 1
    print(f"INSTALLED: {len(context.names)} service skills by {context.method} at {destination}")
    return 0
