import unittest
from pathlib import Path

from service.filesystem_policy import temporary_workspace
from service.tests.install_fpf_skills.helpers import END_USER_SKILLS, make_source, run_installer


class InstallConflictTests(unittest.TestCase):
    def test_unmanaged_real_package_is_preserved(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary)
            source = make_source(root / "source")
            destination = root / "installed"
            unmanaged = destination / END_USER_SKILLS[0]
            unmanaged.mkdir(parents=True)
            (unmanaged / "custom.txt").write_text("keep", encoding="utf-8")
            self.assertEqual(run_installer(source, root / "control", destination), 1)
            self.assertEqual((unmanaged / "custom.txt").read_text(), "keep")
