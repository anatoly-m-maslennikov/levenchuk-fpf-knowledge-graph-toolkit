"""Atomically replace skill packages and write installer receipts."""

from __future__ import annotations

import json
import os
import shutil
import tempfile
import uuid
from pathlib import Path

from service.scripts.filesystem_policy import (
    clear_directory,
    is_system_temporary_path,
    remove_directory,
    replace_directory_contents,
)


IGNORED_PACKAGE_NAMES = {".DS_Store", ".fpf-runtime.toml", "__pycache__"}


def remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        remove_directory(path)


def _link_package_entries(source: Path, target: Path) -> None:
    for child in source.iterdir():
        if child.name in IGNORED_PACKAGE_NAMES or child.suffix in {".pyc", ".pyo"}:
            continue
        destination = target / child.name
        if destination.exists() and destination.is_dir() and not destination.is_symlink():
            if not child.is_dir():
                raise OSError(
                    f"cannot replace retained temp package directory with a file link: {destination}"
                )
            clear_directory(destination)
            _link_package_entries(child, destination)
        else:
            destination.symlink_to(child, target_is_directory=child.is_dir())


def _stage_package(
    source: Path, temporary: Path, method: str, wrapper_symlink: bool,
) -> None:
    if method == "copy":
        shutil.copytree(
            source, temporary,
            ignore=shutil.ignore_patterns(
                ".DS_Store", ".fpf-runtime.toml", "__pycache__", "*.pyc", "*.pyo",
            ),
        )
    elif wrapper_symlink:
        temporary.mkdir()
        _link_package_entries(source, temporary)
    else:
        temporary.symlink_to(source, target_is_directory=True)


def _replace_temporary_package(
    source: Path, target: Path, method: str, wrapper_symlink: bool,
) -> None:
    if method == "copy":
        replace_directory_contents(source, target)
        return
    if not wrapper_symlink:
        if target.is_symlink() or target.is_file():
            target.unlink()
        elif target.exists():
            raise OSError(f"cannot replace retained temp directory with symlink: {target}")
        target.symlink_to(source, target_is_directory=True)
        return
    if target.is_symlink() or target.is_file():
        target.unlink()
        target.mkdir(parents=True)
    elif target.exists():
        clear_directory(target)
    else:
        target.mkdir(parents=True)
    _link_package_entries(source, target)


def replace_package(
    source: Path, target: Path, method: str, *, wrapper_symlink: bool = False,
) -> None:
    if is_system_temporary_path(target):
        _replace_temporary_package(source, target, method, wrapper_symlink)
        return
    token = uuid.uuid4().hex
    temporary = target.parent / f".{target.name}.install-{token}"
    backup = target.parent / f".{target.name}.backup-{token}"
    had_target = target.exists() or target.is_symlink()
    backup_created = False
    try:
        _stage_package(source, temporary, method, wrapper_symlink)
        if had_target:
            target.rename(backup)
            backup_created = True
        try:
            temporary.rename(target)
        except OSError:
            if backup_created and backup.exists():
                backup.rename(target)
                backup_created = False
            raise
        if backup_created:
            remove_path(backup)
            backup_created = False
    finally:
        if temporary.exists() or temporary.is_symlink():
            remove_path(temporary)
        if backup_created and (backup.exists() or backup.is_symlink()):
            remove_path(backup)


def write_receipt(path: Path, receipt: dict[str, object]) -> None:
    text = json.dumps(receipt, ensure_ascii=False, indent=2) + "\n"
    write_text(path, text)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()
