from __future__ import annotations

import subprocess
from pathlib import Path


def run(*arguments: str, cwd: Path) -> None:
    subprocess.run(arguments, cwd=cwd, check=True, capture_output=True, text=True)


def make_source(root: Path) -> Path:
    root.mkdir()
    run("git", "init", "-q", cwd=root)
    run("git", "remote", "add", "origin", "https://github.com/ailev/FPF.git", cwd=root)
    source = root / "FPF-Spec.md"
    source.write_text("# Part A - Test\n\n## A.1 - Test pattern\n", encoding="utf-8")
    run("git", "add", "FPF-Spec.md", cwd=root)
    run(
        "git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
        "commit", "-qm", "source", cwd=root,
    )
    return source


def make_builder(path: Path, *, fail: bool = False) -> None:
    if fail:
        path.write_text("#!/usr/bin/env python3\nraise SystemExit(2)\n", encoding="utf-8")
        return
    body = '''#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
parser = argparse.ArgumentParser()
parser.add_argument("--source")
parser.add_argument("--source-revision")
parser.add_argument("--generated-on")
parser.add_argument("--out")
parser.add_argument("--clean", action="store_true")
args = parser.parse_args()
out = Path(args.out)
(out / "00_Index").mkdir(parents=True)
(out / "new.txt").write_text("new", encoding="utf-8")
(out / "00_Index" / "FPF - Validation Report.json").write_text(
    json.dumps({"source_revision": args.source_revision}), encoding="utf-8"
)
'''
    path.write_text(body, encoding="utf-8")


def initialize_graphs(root: Path) -> tuple[Path, Path]:
    graph = root / "FPF-Knowledge-Graph"
    backup = root / "FPF-Knowledge-Graph.bak"
    graph.mkdir()
    backup.mkdir()
    (graph / "current.txt").write_text("current", encoding="utf-8")
    (backup / "older.txt").write_text("older", encoding="utf-8")
    return graph, backup
