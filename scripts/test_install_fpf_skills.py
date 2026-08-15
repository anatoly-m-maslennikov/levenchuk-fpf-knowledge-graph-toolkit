#!/usr/bin/env python3
"""Regression tests for safe FPF skill symlink refreshes."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import install_fpf_skills as installer


class InstallFpfSkillsTests(unittest.TestCase):
    def make_source(self, root: Path) -> Path:
        skills = root / "skills"
        for name in installer.SKILL_NAMES:
            package = skills / f"{name}.skill"
            package.mkdir(parents=True)
            (package / "SKILL.md").write_text(f"---\nname: {name}\n---\n", encoding="utf-8")
        references = skills / "fpf-route.skill" / "references"
        references.mkdir()
        (references / "routing.md").write_text("route references\n", encoding="utf-8")
        (skills / "fpf-route.skill" / "fpf-settings.toml").write_text(
            'output_style = "general"\n'
            'fpf_terms_explained = "off"\n'
            'install_method = "copy"\n',
            encoding="utf-8",
        )
        return skills

    def run_with_source(self, source: Path, destination: Path) -> int:
        settings = source / "fpf-route.skill" / "fpf-settings.toml"
        harness = installer.Harness("test", "TEST_FPF_HOME", ".test-fpf")
        with patch.object(installer, "SOURCE_SKILLS", source), patch.object(installer, "SOURCE_SETTINGS", settings):
            return installer.run(
                harness,
                ["--apply", "--method", "symlink", "--destination", str(destination)],
            )

    def test_apply_rewrites_stale_and_broken_package_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = self.make_source(root / "current")
            destination = root / "installed"
            old = root / "old-package"
            old.mkdir()
            (old / "SKILL.md").write_text("old", encoding="utf-8")
            destination.mkdir()
            (destination / "fpf-alignment-audit").symlink_to(old, target_is_directory=True)
            (destination / "fpf-applicability-scan").symlink_to(root / "missing", target_is_directory=True)

            self.assertEqual(self.run_with_source(source, destination), 0)
            self.assertTrue(installer.same_link(destination / "fpf-alignment-audit", source / "fpf-alignment-audit.skill"))
            self.assertTrue(installer.same_link(destination / "fpf-applicability-scan", source / "fpf-applicability-scan.skill"))

    def test_apply_creates_route_wrapper_with_copied_skill_and_linked_references(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = self.make_source(root / "current")
            destination = root / "installed"

            self.assertEqual(self.run_with_source(source, destination), 0)

            wrapper = destination / "fpf-route"
            self.assertTrue(installer.is_route_wrapper(wrapper, source / "fpf-route.skill"))
            self.assertTrue((wrapper / "SKILL.md").is_file())
            self.assertFalse((wrapper / "SKILL.md").is_symlink())
            self.assertEqual(
                (wrapper / "SKILL.md").read_text(encoding="utf-8"),
                (source / "fpf-route.skill" / "SKILL.md").read_text(encoding="utf-8"),
            )
            self.assertTrue(installer.same_link(wrapper / "references", source / "fpf-route.skill" / "references"))
            self.assertTrue((wrapper / "fpf-settings.toml").is_file())
            self.assertFalse((wrapper / "fpf-settings.toml").is_symlink())

    def test_apply_refreshes_stale_route_wrapper_and_keeps_settings_real(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = self.make_source(root / "current")
            destination = root / "installed"
            wrapper = destination / "fpf-route"
            wrapper.mkdir(parents=True)
            (wrapper / "fpf-settings.toml").write_text(
                'output_style = "general"\n'
                'fpf_terms_explained = "off"\n'
                'install_method = "symlink"\n',
                encoding="utf-8",
            )
            for entry in (source / "fpf-route.skill").iterdir():
                if entry.name != "fpf-settings.toml":
                    (wrapper / entry.name).symlink_to(root / "old" / entry.name, target_is_directory=entry.is_dir())

            self.assertEqual(self.run_with_source(source, destination), 0)
            self.assertTrue(installer.is_route_wrapper(wrapper, source / "fpf-route.skill"))
            self.assertTrue((wrapper / "SKILL.md").is_file())
            self.assertFalse((wrapper / "SKILL.md").is_symlink())
            self.assertTrue(installer.same_link(wrapper / "references", source / "fpf-route.skill" / "references"))
            self.assertTrue((wrapper / "fpf-settings.toml").is_file())
            self.assertFalse((wrapper / "fpf-settings.toml").is_symlink())
            settings_text = (wrapper / "fpf-settings.toml").read_text(encoding="utf-8")
            for setting in ("output_style", "fpf_terms_explained", "install_method", "install_source_hash"):
                self.assertIn(f"# {setting}:", settings_text)

    def test_apply_removes_owned_legacy_top_level_settings(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = self.make_source(root / "current")
            destination = root / "installed"
            destination.mkdir()
            legacy = destination / "fpf-settings.toml"
            legacy.write_text(
                'output_style = "general"\n'
                'fpf_terms_explained = "off"\n'
                'install_method = "symlink"\n',
                encoding="utf-8",
            )

            self.assertEqual(self.run_with_source(source, destination), 0)
            self.assertFalse(legacy.exists())

    def test_apply_keeps_unparseable_legacy_top_level_settings(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = self.make_source(root / "current")
            destination = root / "installed"
            destination.mkdir()
            legacy = destination / "fpf-settings.toml"
            legacy.write_text("not installer settings\n", encoding="utf-8")

            self.assertEqual(self.run_with_source(source, destination), 0)
            self.assertEqual(legacy.read_text(encoding="utf-8"), "not installer settings\n")

    def test_unmanaged_real_package_remains_a_conflict(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = self.make_source(root / "current")
            destination = root / "installed"
            unmanaged = destination / "fpf-alignment-audit"
            unmanaged.mkdir(parents=True)
            (unmanaged / "custom.txt").write_text("keep", encoding="utf-8")

            self.assertEqual(self.run_with_source(source, destination), 1)
            self.assertEqual((unmanaged / "custom.txt").read_text(encoding="utf-8"), "keep")

    def test_unmanaged_real_route_skill_remains_a_conflict(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = self.make_source(root / "current")
            destination = root / "installed"
            wrapper = destination / "fpf-route"
            wrapper.mkdir(parents=True)
            (wrapper / "SKILL.md").write_text("custom instructions\n", encoding="utf-8")
            (wrapper / "references").symlink_to(
                source / "fpf-route.skill" / "references", target_is_directory=True
            )
            (wrapper / "fpf-settings.toml").write_text(
                'output_style = "general"\n'
                'fpf_terms_explained = "off"\n'
                'install_method = "symlink"\n',
                encoding="utf-8",
            )

            self.assertEqual(self.run_with_source(source, destination), 1)
            self.assertEqual((wrapper / "SKILL.md").read_text(encoding="utf-8"), "custom instructions\n")


if __name__ == "__main__":
    unittest.main()
