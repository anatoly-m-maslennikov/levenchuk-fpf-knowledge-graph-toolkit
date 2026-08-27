import subprocess
from pathlib import Path


SOURCE_NAME = "Narrativization-and-Narrative-Studies-Principles-Framework.md"


def run(*arguments: str, cwd: Path) -> None:
    subprocess.run(arguments, cwd=cwd, check=True, capture_output=True, text=True)


def make_source(root: Path) -> Path:
    root.mkdir()
    run("git", "init", "-q", cwd=root)
    run("git", "remote", "add", "origin", "https://github.com/ailev/FPF.git", cwd=root)
    source = root / SOURCE_NAME
    source.write_text(
        "# Narrativization Principles Framework\n\n"
        "## NSTD.1 - Source intake\n\nNSTD.2 follows this pattern.\n\n"
        "## NSTD.2 - Narrative route\n",
        encoding="utf-8",
    )
    run("git", "add", SOURCE_NAME, cwd=root)
    run(
        "git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
        "commit", "-qm", "source", cwd=root,
    )
    return source
