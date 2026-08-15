#!/usr/bin/env python3
"""Shared installer for the repository's portable FPF skill packages."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import sys
import tempfile
import uuid
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SKILLS = ROOT / "skills"
SOURCE_SETTINGS = SOURCE_SKILLS / "fpf-route.skill" / "fpf-settings.toml"
SKILL_NAMES = (
    "fpf-alignment-audit",
    "fpf-applicability-scan",
    "fpf-decision-synthesize",
    "fpf-design-challenge",
    "fpf-options-explore",
    "fpf-quality-improve",
    "fpf-route",
    "fpf-sota-harvest",
)
METHODS = ("copy", "symlink")
IGNORED_NAMES = {".DS_Store", "__pycache__"}
REQUIRED_SETTINGS = {"output_style", "fpf_terms_explained", "install_method"}
OPTIONAL_SETTINGS = {"install_source_hash"}
ROUTE_SKILL_NAME = "fpf-route"


@dataclass(frozen=True)
class Harness:
    """One skill-capable harness and its user-level discovery root."""

    name: str
    environment_variable: str
    default_home_name: str


def default_destination(harness: Harness) -> Path:
    """Return the harness's standard user-level skill directory."""
    configured = os.environ.get(harness.environment_variable, "").strip()
    harness_home = Path(configured).expanduser() if configured else Path.home() / harness.default_home_name
    return harness_home / "skills"


def parse_settings(path: Path) -> dict[str, str]:
    """Read the intentionally flat, string-only FPF settings format."""
    values: dict[str, str] = {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise ValueError(f"cannot read settings file {path}: {exc}") from exc

    for line_number, line in enumerate(lines, start=1):
        content = line.split("#", 1)[0].strip()
        if not content:
            continue
        match = re.fullmatch(r'([a-z_]+)\s*=\s*"([a-z0-9_-]+)"', content)
        if match is None:
            raise ValueError(f"invalid setting syntax at {path}:{line_number}")
        key, value = match.groups()
        if key not in REQUIRED_SETTINGS | OPTIONAL_SETTINGS:
            raise ValueError(f"unknown setting {key!r} at {path}:{line_number}")
        if key in values:
            raise ValueError(f"duplicate setting {key!r} in {path}")
        values[key] = value
    return values


def validate_source() -> dict[str, str]:
    """Validate the repository inputs before planning any installation."""
    settings = parse_settings(SOURCE_SETTINGS)
    if set(settings) != REQUIRED_SETTINGS:
        raise ValueError(
            "repository settings must contain exactly output_style, "
            "fpf_terms_explained, and install_method"
        )
    if settings["install_method"] not in METHODS:
        raise ValueError("repository install_method must be copy or symlink")

    actual_packages = {path.name for path in SOURCE_SKILLS.glob("fpf-*.skill") if path.is_dir()}
    expected_packages = {f"{name}.skill" for name in SKILL_NAMES}
    if actual_packages != expected_packages:
        raise ValueError("repository FPF skill package set does not match the installer catalog")

    for name in SKILL_NAMES:
        skill_file = SOURCE_SKILLS / f"{name}.skill" / "SKILL.md"
        try:
            frontmatter = skill_file.read_text(encoding="utf-8")
        except OSError as exc:
            raise ValueError(f"cannot read {skill_file}: {exc}") from exc
        if re.search(rf"(?m)^name:\s*{re.escape(name)}\s*$", frontmatter) is None:
            raise ValueError(f"package name does not match SKILL.md frontmatter: {name}")
    return settings


def ignored(path: Path) -> bool:
    """Return whether a generated filesystem artifact is outside the package."""
    return path.name in IGNORED_NAMES or path.suffix in {".pyc", ".pyo"}


def tree_snapshot(root: Path) -> dict[str, str]:
    """Hash a package tree without following embedded symlinks."""
    if not root.is_dir() or root.is_symlink():
        raise ValueError(f"expected a real package directory: {root}")
    snapshot: dict[str, str] = {}
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        relative = path.relative_to(root)
        if any(part in IGNORED_NAMES for part in relative.parts) or ignored(path):
            continue
        if path.is_symlink():
            raise ValueError(f"embedded symlinks are not supported in a copied package: {path}")
        if path.is_file():
            snapshot[relative.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return snapshot


def suite_digest(package_roots: dict[str, Path]) -> str:
    """Return one stable digest, excluding the harness-local route settings file."""
    digest = hashlib.sha256()
    for name in SKILL_NAMES:
        snapshot = tree_snapshot(package_roots[name])
        for relative, file_hash in sorted(snapshot.items()):
            if name == ROUTE_SKILL_NAME and relative == "fpf-settings.toml":
                continue
            digest.update(name.encode("utf-8"))
            digest.update(b"\0")
            digest.update(relative.encode("utf-8"))
            digest.update(b"\0")
            digest.update(file_hash.encode("ascii"))
            digest.update(b"\0")
    return digest.hexdigest()


def source_roots() -> dict[str, Path]:
    return {name: SOURCE_SKILLS / f"{name}.skill" for name in SKILL_NAMES}


def target_roots(destination: Path) -> dict[str, Path]:
    return {name: destination / name for name in SKILL_NAMES}


def installed_settings_path(destination: Path) -> Path:
    """Return the local settings file embedded in the installed route package."""
    return destination / ROUTE_SKILL_NAME / "fpf-settings.toml"


def is_route_wrapper(target: Path, source: Path) -> bool:
    """Return whether a route wrapper has copied instructions and linked references."""
    if target.is_symlink() or not target.is_dir():
        return False
    expected_names = {path.name for path in source.iterdir() if not ignored(path)}
    if "fpf-settings.toml" not in expected_names:
        return False
    settings = target / "fpf-settings.toml"
    if not settings.is_file() or settings.is_symlink():
        return False
    for source_entry in source.iterdir():
        if ignored(source_entry) or source_entry.name == "fpf-settings.toml":
            continue
        installed_entry = target / source_entry.name
        if source_entry.name == "SKILL.md":
            if (
                not installed_entry.is_file()
                or installed_entry.is_symlink()
                or installed_entry.read_bytes() != source_entry.read_bytes()
            ):
                return False
        elif not same_link(installed_entry, source_entry):
            return False
    return {path.name for path in target.iterdir() if not ignored(path)} == expected_names


def is_replaceable_route_wrapper(target: Path, source: Path) -> bool:
    """Return whether a route wrapper has only local settings and source-entry links.

    The links need not resolve or point at this checkout: those are stale installer
    outputs that can safely be replaced. A real entry or an extra entry remains an
    unmanaged conflict.
    """
    if target.is_symlink() or not target.is_dir():
        return False
    expected_names = {path.name for path in source.iterdir() if not ignored(path)}
    if "fpf-settings.toml" not in expected_names:
        return False
    settings = target / "fpf-settings.toml"
    if not settings.is_file() or settings.is_symlink():
        return False
    if {path.name for path in target.iterdir() if not ignored(path)} != expected_names:
        return False
    return all(
        (target / source_entry.name).is_symlink()
        for source_entry in source.iterdir()
        if not ignored(source_entry) and source_entry.name != "fpf-settings.toml"
    )


def same_link(target: Path, source: Path) -> bool:
    """Return whether target is a symlink to this exact checkout package."""
    if not target.is_symlink():
        return False
    try:
        raw_target = Path(os.readlink(target))
        resolved = raw_target if raw_target.is_absolute() else target.parent / raw_target
        return resolved.resolve() == source.resolve()
    except OSError:
        return False


def classify_install(destination: Path, stored_settings: dict[str, str]) -> tuple[str, str | None]:
    """Classify the current catalog and return its state plus optional digest."""
    sources = source_roots()
    targets = target_roots(destination)
    existing = [path for path in targets.values() if path.exists() or path.is_symlink()]
    if not existing:
        return "absent", None

    if all(
        (not path.exists() and not path.is_symlink())
        or (
            (is_route_wrapper(path, sources[name]) or same_link(path, sources[name]))
            if name == ROUTE_SKILL_NAME
            else same_link(path, sources[name])
        )
        for name, path in targets.items()
    ):
        return "symlink-partial" if len(existing) < len(targets) else "symlink-current", None

    if all(
        (not path.exists() and not path.is_symlink())
        or path.is_symlink()
        or (name == ROUTE_SKILL_NAME and is_replaceable_route_wrapper(path, sources[name]))
        for name, path in targets.items()
    ):
        return "symlink-stale", None

    real_directories = {
        name: path for name, path in targets.items() if path.exists() and path.is_dir() and not path.is_symlink()
    }
    if len(real_directories) == len(existing) == len(targets):
        installed_digest = suite_digest(real_directories)
        current_digest = suite_digest(sources)
        if installed_digest == current_digest:
            return "copy-current", installed_digest
        if stored_settings.get("install_method") == "copy" and stored_settings.get("install_source_hash") == installed_digest:
            return "copy-managed-stale", installed_digest
    return "conflict", None


def load_installed_settings(destination: Path) -> dict[str, str]:
    """Load a persistent harness-local preference when present."""
    path = installed_settings_path(destination)
    if not path.exists() and not path.is_symlink():
        return {}
    if path.is_symlink():
        return {}
    settings = parse_settings(path)
    missing = REQUIRED_SETTINGS - set(settings)
    if missing:
        raise ValueError(f"installed settings are missing: {', '.join(sorted(missing))}")
    if settings["install_method"] not in METHODS:
        raise ValueError("installed install_method must be copy or symlink")
    return settings


def remove_legacy_settings(destination: Path) -> None:
    """Remove only a parseable installer-owned pre-wrapper settings file."""
    legacy_path = destination / "fpf-settings.toml"
    if not legacy_path.is_file() or legacy_path.is_symlink():
        return
    try:
        settings = parse_settings(legacy_path)
    except ValueError:
        return
    if REQUIRED_SETTINGS <= set(settings) and settings.get("install_method") in METHODS:
        legacy_path.unlink()


def render_installed_settings(source: dict[str, str], method: str, source_hash: str) -> str:
    """Render suite settings plus the persistent installation choice."""
    return (
        "# FPF suite settings installed by the repository helper.\n"
        "# output_style: natural = FPF wording; general = ordinary-language synonyms; "
        "ste = simplified technical English without FPF terms.\n"
        f'output_style = "{source["output_style"]}"\n'
        "# fpf_terms_explained: natural only; full = up to 3 lines; short = one brief "
        "clause or sentence; off = no explanations.\n"
        f'fpf_terms_explained = "{source["fpf_terms_explained"]}"\n'
        "# install_method: copy = self-contained folders; symlink = live links to the "
        "repository checkout.\n"
        f'install_method = "{method}"\n'
        "# install_source_hash: installer-managed fingerprint of the installed source; "
        "do not edit.\n"
        f'install_source_hash = "{source_hash}"\n'
    )


def remove_path(path: Path) -> None:
    """Remove one installer-owned temporary or backup path."""
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        shutil.rmtree(path)


def replace_package(source: Path, target: Path, method: str, settings_text: str | None = None) -> None:
    """Atomically replace one known-managed package with a copy or symlink."""
    token = uuid.uuid4().hex
    temporary = target.parent / f".{target.name}.install-{token}"
    backup = target.parent / f".{target.name}.backup-{token}"
    backup_created = False
    replacement_installed = False
    try:
        if method == "copy":
            shutil.copytree(
                source,
                temporary,
                ignore=shutil.ignore_patterns(".DS_Store", "__pycache__", "*.pyc", "*.pyo"),
            )
        else:
            if target.name == ROUTE_SKILL_NAME:
                temporary.mkdir()
                for source_entry in source.iterdir():
                    if ignored(source_entry) or source_entry.name == "fpf-settings.toml":
                        continue
                    if source_entry.name == "SKILL.md":
                        shutil.copy2(source_entry, temporary / source_entry.name)
                    else:
                        (temporary / source_entry.name).symlink_to(
                            source_entry, target_is_directory=source_entry.is_dir()
                        )
            else:
                temporary.symlink_to(source, target_is_directory=True)
        if target.name == ROUTE_SKILL_NAME:
            if settings_text is None:
                raise ValueError("route package replacement requires local settings")
            write_settings(temporary / "fpf-settings.toml", settings_text)

        had_target = target.exists() or target.is_symlink()
        if had_target:
            target.rename(backup)
            backup_created = True
        try:
            temporary.rename(target)
            replacement_installed = True
        except OSError:
            if had_target and backup.exists():
                backup.rename(target)
                backup_created = False
            raise
        if had_target:
            remove_path(backup)
            backup_created = False
    finally:
        if temporary.exists() or temporary.is_symlink():
            remove_path(temporary)
        if backup_created and replacement_installed and (backup.exists() or backup.is_symlink()):
            remove_path(backup)


def write_settings(path: Path, text: str) -> None:
    """Replace the harness-local settings file atomically."""
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent, text=True)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def build_parser(harness: Harness) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=f"Install the repository FPF skills for {harness.name}. Writes require --apply."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="install or update the skill packages")
    mode.add_argument("--check", action="store_true", help="verify the current installation without writing")
    parser.add_argument(
        "--method",
        choices=METHODS,
        help="installation method; otherwise reuse the installed choice, then the repository copy default",
    )
    parser.add_argument(
        "--destination",
        type=Path,
        help=(
            f"exact skills directory; default: ${harness.environment_variable}/skills "
            f"or ~/{harness.default_home_name}/skills"
        ),
    )
    return parser


def run(harness: Harness, arguments: list[str] | None = None) -> int:
    """Run one harness-specific installer adapter."""
    args = build_parser(harness).parse_args(arguments)
    destination = (args.destination or default_destination(harness)).expanduser().resolve()

    try:
        source_settings = validate_source()
        installed_settings = load_installed_settings(destination)
        method = args.method or installed_settings.get("install_method") or source_settings["install_method"]
        if method not in METHODS:
            raise ValueError("resolved install method must be copy or symlink")
        state, _installed_digest = classify_install(destination, installed_settings)
        current_source_hash = suite_digest(source_roots())
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    explicit_switch = bool(
        args.method
        and installed_settings.get("install_method")
        and args.method != installed_settings["install_method"]
    )
    acceptable_states = {
        "copy": {"absent", "copy-current", "copy-managed-stale"},
        "symlink": {"absent", "symlink-current", "symlink-partial", "symlink-stale"},
    }
    switchable_states = {
        "copy": {"symlink-current"},
        "symlink": {"copy-current", "copy-managed-stale"},
    }
    can_apply = state in acceptable_states[method] or (explicit_switch and state in switchable_states[method])
    if not can_apply:
        print(
            f"ERROR: conflicting or unmanaged installation at {destination} "
            f"(state={state}, requested={method}); no files were changed",
            file=sys.stderr,
        )
        return 1

    expected_state = f"{method}-current"
    settings_current = (
        installed_settings.get("output_style") == source_settings["output_style"]
        and installed_settings.get("fpf_terms_explained") == source_settings["fpf_terms_explained"]
        and installed_settings.get("install_method") == method
        and installed_settings.get("install_source_hash") == current_source_hash
    )
    route_layout_current = method != "symlink" or is_route_wrapper(
        target_roots(destination)[ROUTE_SKILL_NAME], source_roots()[ROUTE_SKILL_NAME]
    )
    packages_current = state == expected_state and route_layout_current

    if args.check:
        if packages_current and settings_current:
            print(f"OK: {harness.name}: 8 skills installed by {method} at {destination}")
            return 0
        print(
            f"OUT OF DATE: {harness.name}: state={state}, method={method}, "
            f"settings={'current' if settings_current else 'stale'}",
            file=sys.stderr,
        )
        return 1

    if not args.apply:
        action = "no package changes" if packages_current else f"install/update from state={state}"
        print(f"DRY RUN: {harness.name}: {action}; method={method}; destination={destination}")
        print("Run again with --apply to write. Use --method copy or --method symlink to change the choice.")
        return 0

    try:
        destination.mkdir(parents=True, exist_ok=True)
        sources = source_roots()
        targets = target_roots(destination)
        settings_text = render_installed_settings(source_settings, method, current_source_hash)
        for name in SKILL_NAMES:
            target = targets[name]
            if method == "symlink" and (
                is_route_wrapper(target, sources[name]) if name == ROUTE_SKILL_NAME else same_link(target, sources[name])
            ):
                continue
            if method == "copy" and target.exists() and not target.is_symlink():
                try:
                    if tree_snapshot(target) == tree_snapshot(sources[name]):
                        continue
                except ValueError:
                    pass
            replace_package(sources[name], target, method, settings_text if name == ROUTE_SKILL_NAME else None)
        write_settings(installed_settings_path(destination), settings_text)
        remove_legacy_settings(destination)
    except OSError as exc:
        guidance = ""
        if method == "symlink" and os.name == "nt":
            guidance = " Native Windows may require Developer Mode or elevated symlink rights; use --method copy."
        print(f"ERROR: installation failed: {exc}.{guidance}", file=sys.stderr)
        return 1

    print(f"INSTALLED: {harness.name}: 8 skills by {method} at {destination}")
    print("The chosen method is saved in fpf-route/fpf-settings.toml for later updates.")
    return 0
