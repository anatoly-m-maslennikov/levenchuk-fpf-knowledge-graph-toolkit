from __future__ import annotations

import unittest
from pathlib import Path

from service.scripts.filesystem_policy import temporary_workspace
from service.tests.install_fpf_skills.helpers import run_with_method


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
SOURCE_SKILLS = REPOSITORY_ROOT / "skills"


def install_and_check(test: unittest.TestCase, method: str) -> None:
    with temporary_workspace(prefix=f"fpf-{method}-runtime-") as temporary:
        root = Path(temporary)
        destination = root / "installed"
        arguments = ["--apply", "--destination", str(destination)]
        test.assertEqual(0, run_with_method(SOURCE_SKILLS, root / "control", destination, method, arguments))
        package = destination / "fpf"
        files = [path for path in package.rglob("*") if path.is_file() and path.name != ".DS_Store"]
        test.assertTrue(files)
        test.assertTrue((package / ".fpf-runtime.toml").is_file())
        source_files = [path for path in files if path.name != ".fpf-runtime.toml"]
        test.assertTrue(all(path.name == "SKILL.md" or path.suffix == ".md" for path in source_files))
        test.assertFalse(any(path.suffix in {".py", ".yaml", ".yml", ".json"} for path in source_files))
        test.assertFalse((package / "scripts").exists())
        runtime = (package / "prompts/fpf-runtime.md").read_text(encoding="utf-8")
        test.assertIn("requires only native skill loading and Markdown/plain-text file access", runtime)
        test.assertIn("Never run Python, uv, a shell command", runtime)
        settings = (package / ".fpf-runtime.toml").read_text(encoding="utf-8")
        test.assertIn(f'repository_root = "{REPOSITORY_ROOT}"', settings)


class InstalledRuntimeTests(unittest.TestCase):
    def test_copy_install_is_zero_executable(self) -> None:
        install_and_check(self, "copy")

    def test_symlink_install_is_zero_executable(self) -> None:
        install_and_check(self, "symlink")


if __name__ == "__main__":
    unittest.main()
