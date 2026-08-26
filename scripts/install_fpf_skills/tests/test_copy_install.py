import unittest
from pathlib import Path

from scripts.filesystem_policy import temporary_workspace
from scripts.install_fpf_skills.tests.helpers import END_USER_SKILLS, make_source, run_with_method


class CopyInstallTests(unittest.TestCase):
    def test_apply_and_check_copy_install(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary)
            source = make_source(root / "source")
            destination = root / "installed"
            apply = ["--apply", "--destination", str(destination)]
            check = ["--check", "--destination", str(destination)]
            self.assertEqual(run_with_method(source, root / "control", destination, "copy", apply), 0)
            self.assertFalse((destination / END_USER_SKILLS[0]).is_symlink())
            settings = (destination / ".fpf-runtime.toml").read_text(encoding="utf-8")
            self.assertIn(f'repository_root = "{source.parent.resolve()}"', settings)
            self.assertIn('report_style = "plain"', settings)
            self.assertEqual(run_with_method(source, root / "control", destination, "copy", check), 0)

    def test_apply_refreshes_managed_stale_copy(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary)
            source = make_source(root / "source")
            destination = root / "installed"
            apply = ["--apply", "--destination", str(destination)]
            self.assertEqual(run_with_method(source, root / "control", destination, "copy", apply), 0)
            source_file = source / f"{END_USER_SKILLS[0]}.skill" / "SKILL.md"
            source_file.write_text(source_file.read_text() + "changed\n", encoding="utf-8")
            self.assertEqual(run_with_method(source, root / "control", destination, "copy", apply), 0)
            self.assertIn("changed", (destination / END_USER_SKILLS[0] / "SKILL.md").read_text())

    def test_check_rejects_and_apply_repairs_stale_runtime_settings(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary)
            source = make_source(root / "source")
            destination = root / "installed"
            apply = ["--apply", "--destination", str(destination)]
            check = ["--check", "--destination", str(destination)]
            self.assertEqual(run_with_method(source, root / "control", destination, "copy", apply), 0)
            (destination / ".fpf-runtime.toml").write_text("stale\n", encoding="utf-8")
            self.assertEqual(run_with_method(source, root / "control", destination, "copy", check), 1)
            self.assertEqual(run_with_method(source, root / "control", destination, "copy", apply), 0)
            self.assertEqual(run_with_method(source, root / "control", destination, "copy", check), 0)
