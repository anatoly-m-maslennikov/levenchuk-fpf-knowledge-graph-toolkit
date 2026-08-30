from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from service.scripts.filesystem_policy import temporary_workspace
from service.tests.install_fpf_skills.helpers import run_with_method


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
SOURCE_SKILLS = REPOSITORY_ROOT / "skills"


def _run(package: Path, root: Path, script: str, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(package / "scripts" / script), *arguments],
        cwd=root, text=True, capture_output=True, check=False,
    )


def install_and_run(test: unittest.TestCase, method: str) -> None:
    with temporary_workspace(prefix=f"fpf-{method}-runtime-") as temporary:
        root = Path(temporary)
        destination = root / "installed"
        arguments = ["--apply", "--destination", str(destination)]
        test.assertEqual(0, run_with_method(
            SOURCE_SKILLS, root / "control", destination, method, arguments,
        ))
        package = destination / "fpf"
        route = _run(package, root, "route_fpf.py", "--check")
        test.assertEqual(0, route.returncode, route.stderr)
        graph = _run(package, root, "read_fpf_graph.py", "--node", "sota-harvest")
        test.assertEqual(0, graph.returncode, graph.stderr)
        test.assertEqual("sota-harvest", json.loads(graph.stdout)["nodes"][0]["id"])
        context = _run(package, root, "prepare_fpf_context.py", "--node", "sota-harvest")
        test.assertEqual(0, context.returncode, context.stderr)
        test.assertEqual("sota-harvest", json.loads(context.stdout)["nodes"][0]["id"])


class InstalledRuntimeTests(unittest.TestCase):

    def test_copy_install_executes_real_package(self) -> None:
        install_and_run(self, "copy")

    def test_symlink_install_executes_real_package(self) -> None:
        install_and_run(self, "symlink")


if __name__ == "__main__":
    unittest.main()
