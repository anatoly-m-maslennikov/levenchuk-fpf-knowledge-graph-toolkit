import json
import unittest
from pathlib import Path

from scripts.filesystem_policy import temporary_workspace
from scripts.install_fpf_skills.install_fpf_skills_workers.snapshots import same_link
from scripts.install_fpf_skills.tests.helpers import (
    END_USER_SKILLS, SERVICE_SKILLS, make_source, run_installer, run_with_method,
)


class SymlinkInstallTests(unittest.TestCase):
    def test_apply_installs_only_end_user_skills_and_receipt(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary)
            source = make_source(root / "source")
            destination = root / "installed"
            self.assertEqual(run_installer(source, root / "control", destination), 0)
            for name in END_USER_SKILLS:
                self.assertTrue(same_link(destination / name, source / f"{name}.skill"))
            for name in SERVICE_SKILLS:
                self.assertFalse((destination / name).exists())
            receipt = json.loads((destination / ".fpf-skills-install.json").read_text())
            self.assertEqual(receipt["method"], "symlink")
            settings_path = destination / END_USER_SKILLS[0] / ".fpf-runtime.toml"
            settings = settings_path.read_text(encoding="utf-8")
            self.assertIn(f'repository_root = "{source.parent.resolve()}"', settings)
            self.assertTrue((source / "fpf.skill" / ".fpf-runtime.toml").is_file())
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
            self.assertTrue(same_link(
                destination / END_USER_SKILLS[0], source / f"{END_USER_SKILLS[0]}.skill"
            ))
