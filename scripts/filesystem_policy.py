"""Filesystem behavior shared by repository tools and their tests."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
import shutil
import tempfile
from os import PathLike
from pathlib import Path


def is_system_temporary_path(path: str | PathLike[str]) -> bool:
    """Return whether a path is inside the platform temporary directory."""
    temporary_root = Path(tempfile.gettempdir()).resolve()
    return Path(path).resolve().is_relative_to(temporary_root)


@contextmanager
def temporary_workspace(
    *, prefix: str | None = None, directory: str | PathLike[str] | None = None,
) -> Iterator[str]:
    """Retain workspaces in system temp; clean ordinary workspaces normally."""
    parent = directory or tempfile.gettempdir()
    if is_system_temporary_path(parent):
        name = tempfile.mkdtemp(prefix=prefix, dir=directory)
        try:
            yield name
        finally:
            clear_directory(Path(name))
        return
    name = tempfile.mkdtemp(prefix=prefix, dir=directory)
    try:
        yield name
    finally:
        remove_directory(Path(name))


def remove_directory(path: Path) -> None:
    """Remove a directory, or clear its files when it is inside system temp."""
    if is_system_temporary_path(path):
        clear_directory(path)
        return
    try:
        shutil.rmtree(path)
    except PermissionError:
        if path.exists():
            clear_directory(path)


def clear_directory(path: Path) -> None:
    """Unlink directory contents recursively while retaining every folder."""
    for child in path.iterdir():
        if child.is_symlink() or child.is_file():
            child.unlink()
        elif child.is_dir():
            clear_directory(child)


def replace_directory_contents(source: Path, target: Path) -> None:
    """Copy a tree over a target using file operations only."""
    if target.exists():
        clear_directory(target)
    else:
        target.mkdir(parents=True)
    shutil.copytree(source, target, dirs_exist_ok=True, symlinks=True)


def logical_path_exists(path: Path) -> bool:
    """Treat cleared retained temp folders as absent."""
    if path.is_symlink() or not path.is_dir() or not is_system_temporary_path(path):
        return path.exists() or path.is_symlink()
    return any(
        (item.is_file() or item.is_symlink()) and item.name != ".DS_Store"
        for item in path.rglob("*")
    )
