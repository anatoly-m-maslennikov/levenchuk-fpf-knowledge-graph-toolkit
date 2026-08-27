import unittest
from pathlib import Path

from service.filesystem_policy import temporary_workspace
from service.init_settings.init_settings import read_skill_version
from service.tests.install_fpf_skills.helpers import END_USER_SKILLS, make_source, run_with_method


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
            settings_path = destination / END_USER_SKILLS[0] / ".fpf-runtime.toml"
            settings = settings_path.read_text(encoding="utf-8")
            self.assertIn(f'skill_version = "{read_skill_version()}"', settings)
            self.assertIn(f'repository_root = "{source.parent.resolve()}"', settings)
            self.assertIn('report_style = "plain"', settings)
            self.assertFalse((destination / ".fpf-runtime.toml").exists())
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


class CopyRuntimeSettingsTests(unittest.TestCase):
    def test_check_rejects_and_apply_repairs_stale_runtime_settings(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary)
            source = make_source(root / "source")
            destination = root / "installed"
            apply = ["--apply", "--destination", str(destination)]
            check = ["--check", "--destination", str(destination)]
            self.assertEqual(run_with_method(source, root / "control", destination, "copy", apply), 0)
            settings_path = destination / END_USER_SKILLS[0] / ".fpf-runtime.toml"
            settings_path.write_text("stale\n", encoding="utf-8")
            self.assertEqual(run_with_method(source, root / "control", destination, "copy", check), 1)
            self.assertEqual(run_with_method(source, root / "control", destination, "copy", apply), 0)
            self.assertEqual(run_with_method(source, root / "control", destination, "copy", check), 0)

    def test_apply_replaces_any_legacy_root_runtime_settings_with_canonical_settings(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary)
            source = make_source(root / "source")
            destination = root / "installed"
            apply = ["--apply", "--destination", str(destination)]
            self.assertEqual(run_with_method(source, root / "control", destination, "copy", apply), 0)
            inside = destination / END_USER_SKILLS[0] / ".fpf-runtime.toml"
            legacy = destination / ".fpf-runtime.toml"
            legacy.write_text(
                'schema_version = 0\nrepository_root = "/obsolete"\n\n'
                '[defaults]\noutput_style = "natural"\n',
                encoding="utf-8",
            )
            self.assertEqual(run_with_method(source, root / "control", destination, "copy", apply), 0)
            self.assertFalse(legacy.exists())
            self.assertTrue(inside.is_file())
            self.assertIn(f'repository_root = "{source.parent.resolve()}"', inside.read_text())
            self.assertIn('output_style = "general"', inside.read_text())
