from __future__ import annotations

import json
import unittest
from pathlib import Path
from unittest.mock import patch

from service.scripts.filesystem_policy import temporary_workspace
from service.scripts.install_service_skills.install_service_skills import run
from service.scripts.install_service_skills.install_service_skills_workers import cli
from skills.install_fpf_skills.install_fpf_skills_workers.snapshots import symlink_wrapper_current
from service.scripts.validate_repository.validate_repository_workers.skills import _validate_project_discovery


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
            self.assertTrue(all(
                (destination / name).is_symlink()
                or symlink_wrapper_current(destination / name, source / f"{name}.skill")
                for name in NAMES
            ))
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
            self.assertEqual(0, invoke(source, destination, "--check"))

class ServiceCopyValidationTests(unittest.TestCase):
    def test_repository_validation_accepts_receipt_bound_copy_install(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary)
            source = make_source(root / "service/skills")
            destination = root / ".agents/skills"
            self.assertEqual(
                0, invoke(source, destination, "--method", "copy", "--apply")
            )
            self.assertEqual(
                [], _validate_project_discovery(root, {"service_skills": NAMES})
            )


class ServiceMethodTransitionTests(unittest.TestCase):
    def test_copy_to_symlink_transition_works_in_managed_temporary_path(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary)
            source = make_source(root / "source")
            destination = root / ".agents/skills"
            self.assertEqual(
                0, invoke(source, destination, "--method", "copy", "--apply")
            )
            self.assertEqual(0, invoke(source, destination, "--apply"))
            self.assertTrue(all(
                symlink_wrapper_current(destination / name, source / f"{name}.skill")
                for name in NAMES
            ))

    def test_symlink_to_copy_transition_works_in_managed_temporary_path(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary)
            source = make_source(root / "source")
            destination = root / ".agents/skills"
            self.assertEqual(0, invoke(source, destination, "--apply"))
            self.assertEqual(
                0, invoke(source, destination, "--method", "copy", "--apply")
            )
            self.assertTrue(all(
                (destination / name).is_dir() and not (destination / name).is_symlink()
                for name in NAMES
            ))


class ServiceConflictTests(unittest.TestCase):
    def test_non_service_discovery_entry_blocks_apply(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary)
            source = make_source(root / "source")
            destination = root / ".agents/skills"
            (destination / "fpf").mkdir(parents=True)
            self.assertEqual(1, invoke(source, destination, "--apply"))


if __name__ == "__main__":
    unittest.main()
