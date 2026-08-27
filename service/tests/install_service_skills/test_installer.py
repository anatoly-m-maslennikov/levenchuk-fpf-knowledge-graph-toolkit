from __future__ import annotations

import json
import unittest
from pathlib import Path
from unittest.mock import patch

from service.filesystem_policy import temporary_workspace
from service.install_service_skills.install_service_skills import run
from service.install_service_skills.install_service_skills_workers import cli


NAMES = ["graph-fpf-convert-from-original", "graph-fpf-evaluate-conversion-result"]


def make_source(root: Path) -> Path:
    for name in NAMES:
        package = root / f"{name}.skill"
        package.mkdir(parents=True)
        (package / "SKILL.md").write_text(f"---\nname: {name}\n---\n", encoding="utf-8")
    return root


def invoke(source: Path, destination: Path, *arguments: str) -> int:
    with patch.object(cli, "SOURCE_SKILLS", source):
        return run([*arguments, "--destination", str(destination)])


class ServiceSymlinkInstallerTests(unittest.TestCase):
    def test_symlink_apply_and_check(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary)
            source = make_source(root / "source")
            destination = root / ".agents/skills"
            self.assertEqual(0, invoke(source, destination, "--apply"))
            self.assertTrue(all((destination / name).is_symlink() for name in NAMES))
            self.assertEqual(0, invoke(source, destination, "--check"))
            receipt = json.loads((destination.parent / ".fpf-service-skills-install.json").read_text())
            self.assertEqual(NAMES, receipt["skills"])


class ServiceCopyInstallerTests(unittest.TestCase):
    def test_copy_method_installs_real_packages(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary)
            source = make_source(root / "source")
            destination = root / ".agents/skills"
            args = ("--method", "copy", "--apply")
            self.assertEqual(0, invoke(source, destination, *args))
            self.assertTrue(all((destination / name).is_dir() for name in NAMES))
            self.assertTrue(all(not (destination / name).is_symlink() for name in NAMES))

    def test_non_service_discovery_entry_blocks_apply(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary)
            source = make_source(root / "source")
            destination = root / ".agents/skills"
            (destination / "fpf").mkdir(parents=True)
            self.assertEqual(1, invoke(source, destination, "--apply"))


if __name__ == "__main__":
    unittest.main()
