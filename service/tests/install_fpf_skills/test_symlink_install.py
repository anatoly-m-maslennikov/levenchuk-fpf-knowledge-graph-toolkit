import json
import unittest
from pathlib import Path

from service.scripts.filesystem_policy import temporary_workspace
from skills.install_fpf_skills.install_fpf_skills_workers.snapshots import symlink_wrapper_current
from service.tests.install_fpf_skills.helpers import (
    END_USER_SKILLS, make_source, run_installer, run_with_method,
)


class SymlinkInstallTests(unittest.TestCase):
    def test_apply_installs_only_end_user_skills_and_receipt(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary)
            source = make_source(root / "source")
            destination = root / "installed"
            self.assertEqual(run_installer(source, root / "control", destination), 0)
            for name in END_USER_SKILLS:
                self.assertFalse((destination / name).is_symlink())
                self.assertTrue(symlink_wrapper_current(
                    destination / name, source / f"{name}.skill",
                ))
            receipt = json.loads((destination / ".fpf-skills-install.json").read_text())
            self.assertEqual(receipt["method"], "symlink")
            settings_path = destination / END_USER_SKILLS[0] / ".fpf-runtime.toml"
            settings = settings_path.read_text(encoding="utf-8")
            self.assertIn(f'repository_root = "{source.parent.resolve()}"', settings)
            self.assertFalse((source / "fpf.skill" / ".fpf-runtime.toml").exists())
            self.assertFalse((destination / ".fpf-runtime.toml").exists())
            check = ["--check", "--destination", str(destination)]
            self.assertEqual(
                run_with_method(source, root / "control", destination, "symlink", check), 0
            )

    def test_apply_repairs_stale_and_broken_links(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary)
            source = make_source(root / "source")
            destination = root / "installed"
            destination.mkdir()
            (destination / END_USER_SKILLS[0]).symlink_to(root / "missing")
            self.assertEqual(run_installer(source, root / "control", destination), 0)
            self.assertTrue(symlink_wrapper_current(
                destination / END_USER_SKILLS[0], source / f"{END_USER_SKILLS[0]}.skill"
            ))


class SymlinkTransitionTests(unittest.TestCase):
    def test_copy_to_symlink_transition_works_in_managed_temporary_path(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary)
            source = make_source(root / "source")
            destination = root / "installed"
            apply = ["--apply", "--destination", str(destination)]
            self.assertEqual(0, run_with_method(source, root / "control", destination, "copy", apply))
            self.assertEqual(0, run_with_method(source, root / "control", destination, "symlink", apply))
            self.assertTrue(symlink_wrapper_current(
                destination / END_USER_SKILLS[0], source / f"{END_USER_SKILLS[0]}.skill",
            ))


class LegacyWholeLinkMigrationTests(unittest.TestCase):
    def test_apply_migrates_without_retaining_source_settings(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary)
            source = make_source(root / "source")
            package = source / f"{END_USER_SKILLS[0]}.skill"
            leaked = package / ".fpf-runtime.toml"
            leaked.write_text("legacy leaked settings\n", encoding="utf-8")
            destination = root / "installed"
            destination.mkdir()
            (destination / END_USER_SKILLS[0]).symlink_to(package, target_is_directory=True)

            self.assertEqual(run_installer(source, root / "control", destination), 0)

            target = destination / END_USER_SKILLS[0]
            self.assertFalse(target.is_symlink())
            self.assertTrue(symlink_wrapper_current(target, package))
            self.assertFalse(leaked.exists())
            self.assertTrue((target / ".fpf-runtime.toml").is_file())
