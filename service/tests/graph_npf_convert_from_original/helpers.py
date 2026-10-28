import subprocess
from pathlib import Path


SOURCE_NAME = "Narrativization-and-Narrative-Studies-Principles-Framework.md"


def run(*arguments: str, cwd: Path) -> None:
    subprocess.run(arguments, cwd=cwd, check=True, capture_output=True, text=True)


def make_source(root: Path, *, nested: bool = False) -> Path:
    root.mkdir()
    run("git", "init", "-q", cwd=root)
    run("git", "remote", "add", "origin", "https://github.com/ailev/FPF.git", cwd=root)
    source = root / "DPFs" / SOURCE_NAME if nested else root / SOURCE_NAME
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text(
        "# Narrativization Principles Framework\n\n"
        "## NSTD.1 - Source intake\n\nNSTD.2 follows this pattern.\n\n"
        "## NSTD.2 - Narrative route\n",
        encoding="utf-8",
    )
    (root / "FPF-Spec.md").write_text("# Part A\n\n## A.1 - FPF\n", encoding="utf-8")
    run("git", "add", ".", cwd=root)
    run(
        "git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
        "commit", "-qm", "source", cwd=root,
    )
    return source
