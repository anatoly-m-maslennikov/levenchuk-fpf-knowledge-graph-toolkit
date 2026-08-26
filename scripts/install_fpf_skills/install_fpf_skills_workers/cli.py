"""Command-line adapter for end-user FPF skill installation."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from scripts.filesystem_policy import logical_path_exists
from scripts.init_settings.init_settings import EXAMPLE_PATH, SETTINGS_PATH, read_skill_settings
from ..install_fpf_skills import Harness
from .catalog import load_catalog, source_roots, target_roots, validate_source
from .filesystem import remove_path, replace_package, write_receipt, write_text
from .runtime_settings import render_runtime_settings, runtime_settings_current
from .snapshots import same_link, suite_digest, tree_snapshot
from .state import can_apply, classify_install, load_receipt


ROOT = Path(__file__).resolve().parents[3]
SOURCE_SKILLS = ROOT / "skills"
CATALOG_PATH = Path(__file__).parents[1] / "install_fpf_skills_assets" / "catalog.json"
METHODS = {"copy", "symlink"}


def default_destination(harness: Harness) -> Path:
    configured = os.environ.get(harness.environment_variable, "").strip()
    home = Path(configured).expanduser() if configured else Path.home() / harness.default_home_name
    return home / "skills"


def _arguments(harness: Harness, arguments: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=f"Install end-user FPF skills for {harness.name}.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="install or update packages")
    mode.add_argument("--check", action="store_true", help="verify without writing")
    parser.add_argument("--destination", type=Path, help="exact harness skills directory")
    return parser.parse_args(arguments)


def _receipt_current(
    receipt: dict[str, object], method: str, source_hash: str, names: list[str], schema_version: int,
) -> bool:
    return (
        receipt.get("schema_version") == schema_version
        and receipt.get("method") == method
        and receipt.get("source_hash") == source_hash
        and receipt.get("skills") == names
    )


def _target_current(source: Path, target: Path, method: str) -> bool:
    if method == "symlink":
        return same_link(target, source)
    if not target.is_dir() or target.is_symlink():
        return False
    try:
        return tree_snapshot(target) == tree_snapshot(source)
    except ValueError:
        return False


def _install_packages(
    sources: dict[str, Path], targets: dict[str, Path], names: list[str], method: str,
) -> None:
    for name in names:
        if not _target_current(sources[name], targets[name], method):
            replace_package(sources[name], targets[name], method)


def _retired_targets(destination: Path, catalog: dict[str, object]) -> dict[str, Path]:
    names = list(catalog.get("retired_end_user_skills", []))
    return target_roots(destination, names)


def _retired_present(targets: dict[str, Path]) -> list[str]:
    return [name for name, path in targets.items() if logical_path_exists(path)]


def _retired_removable(targets: dict[str, Path], receipt: dict[str, object]) -> bool:
    present = _retired_present(targets)
    if not present:
        return True
    receipt_names = receipt.get("skills")
    if not isinstance(receipt_names, list) or not set(present).issubset(set(receipt_names)):
        return False
    method = receipt.get("method")
    if method == "symlink":
        return all(targets[name].is_symlink() for name in present)
    if method != "copy" or set(present) != set(receipt_names):
        return False
    real = {name: targets[name] for name in receipt_names if targets[name].is_dir() and not targets[name].is_symlink()}
    return len(real) == len(receipt_names) and suite_digest(real, receipt_names) == receipt.get("source_hash")


def _remove_retired(targets: dict[str, Path]) -> None:
    for name in _retired_present(targets):
        remove_path(targets[name])


def _load_context(destination: Path):
    settings, _ = read_skill_settings(SETTINGS_PATH, EXAMPLE_PATH)
    method = settings["install_method"]
    if method not in METHODS:
        raise ValueError("[skills].install_method must be copy or symlink")
    catalog = load_catalog(CATALOG_PATH)
    names = validate_source(SOURCE_SKILLS, catalog)
    sources = source_roots(SOURCE_SKILLS, names)
    targets = target_roots(destination, names)
    receipt_path = destination / str(catalog["receipt_name"])
    runtime_settings_path = destination / str(catalog["settings_name"])
    runtime_settings = render_runtime_settings(SOURCE_SKILLS.parent, settings)
    receipt = load_receipt(receipt_path)
    state, _ = classify_install(targets, sources, names, receipt)
    source_hash = suite_digest(sources, names)
    retired = _retired_targets(destination, catalog)
    return (
        method, catalog, names, sources, targets, retired, receipt_path, receipt,
        state, source_hash, runtime_settings_path, runtime_settings,
    )


def _validate_targets(
    destination: Path, method: str, state: str, receipt: dict[str, object], retired: dict[str, Path],
) -> list[str]:
    if not can_apply(method, state, receipt):
        raise ValueError(f"unmanaged installation at {destination} (state={state})")
    present = _retired_present(retired)
    if present and not _retired_removable(retired, receipt):
        names = ", ".join(present)
        raise ValueError(f"retired FPF packages contain unmanaged changes at {destination}: {names}")
    return present


def _apply_install(destination: Path, context: tuple) -> None:
    (
        method, catalog, names, sources, targets, retired, receipt_path, _, _,
        source_hash, runtime_settings_path, runtime_settings,
    ) = context
    destination.mkdir(parents=True, exist_ok=True)
    _remove_retired(retired)
    _install_packages(sources, targets, names, method)
    write_text(runtime_settings_path, runtime_settings)
    write_receipt(
        receipt_path,
        dict(
            schema_version=catalog["schema_version"], method=method,
            source_hash=source_hash, skills=names,
        ),
    )


def run_installer(harness: Harness, arguments: list[str] | None = None) -> int:
    args = _arguments(harness, arguments)
    destination = (args.destination or default_destination(harness)).expanduser().resolve()
    try:
        context = _load_context(destination)
        (
            method, catalog, names, sources, targets, retired, receipt_path, receipt,
            state, source_hash, runtime_settings_path, runtime_settings,
        ) = context
        retired_present = _validate_targets(destination, method, state, receipt, retired)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    current = (
        not retired_present
        and state == f"{method}-current"
        and _receipt_current(receipt, method, source_hash, names, int(catalog["schema_version"]))
        and runtime_settings_current(runtime_settings_path, runtime_settings)
    )
    if args.check:
        print(f"{'OK' if current else 'OUT OF DATE'}: {harness.name}: {state} at {destination}")
        return 0 if current else 1
    if not args.apply:
        print(
            f"DRY RUN: {harness.name}: state={state}; method={method}; "
            f"retired={len(retired_present)}; destination={destination}"
        )
        return 0
    try:
        _apply_install(destination, context)
    except OSError as exc:
        guidance = " Use copy mode in .caprmedio/settings.toml." if method == "symlink" and os.name == "nt" else ""
        print(f"ERROR: installation failed: {exc}.{guidance}", file=sys.stderr)
        return 1
    print(f"INSTALLED: {harness.name}: {len(names)} end-user skills by {method} at {destination}")
    return 0
