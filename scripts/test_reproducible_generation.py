#!/usr/bin/env python3
"""Regression check for deterministic FPF graph generation."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "build_fpf_obsidian_graph.py"
SOURCE = "# Part A - Example\n\n## A.1 - First page\n\nA.2 links here.\n\n## A.2 - Second page\n"
REVISION = "test-revision-0001"
GENERATED_ON = "2026-08-02"


def tree_bytes(path: Path) -> dict[str, bytes]:
    return {item.relative_to(path).as_posix(): item.read_bytes() for item in sorted(path.rglob("*")) if item.is_file()}


def build(source: Path, output: Path) -> None:
    result = subprocess.run([sys.executable, str(GENERATOR), "--source", str(source), "--source-revision", REVISION, "--generated-on", GENERATED_ON, "--out", str(output), "--clean"], capture_output=True, text=True)
    if result.returncode:
        raise SystemExit(result.stderr or result.stdout)


def main() -> int:
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        source = root / "FPF-Spec.md"
        source.write_text(SOURCE, encoding="utf-8")
        output = root / "FPF-Knowledge-Graph"
        build(source, output)
        first_tree = tree_bytes(output)
        build(source, output)
        if first_tree != tree_bytes(output):
            raise SystemExit("same explicit inputs did not produce identical trees")
        report = json.loads((output / "00_Index" / "FPF - Validation Report.json").read_text(encoding="utf-8"))
        if report["source_sha256"] != hashlib.sha256(source.read_bytes()).hexdigest():
            raise SystemExit("report SHA-256 does not match exact source bytes")
        for page in output.rglob("*.md"):
            text = page.read_text(encoding="utf-8")
            for key in ("source_revision", "source_sha256", "generated_on"):
                if f'{key}: "{report[key]}"' not in text:
                    raise SystemExit(f"provenance mismatch in {page}")
    print("reproducible generation: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
