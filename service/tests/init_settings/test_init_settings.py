#!/usr/bin/env python3
"""Regression checks for repository-local FPF source settings."""

from __future__ import annotations

import unittest
from pathlib import Path

from service.scripts.filesystem_policy import temporary_workspace
from service.scripts.init_settings.init_settings import (
    ensure_settings,
    migrate_settings,
    read_fpf_source,
    read_npf_source,
    read_skill_version,
)

SKILLS = '''
[skills]
output_language = "auto"
output_style = "general"
fpf_terms_explained = "off"
save_report = "on"
report_style = "plain"
install_method = "copy"
'''
CURRENT_VERSION = read_skill_version()
PACKAGE = f'''[package]
name = "fpf"
version = "{CURRENT_VERSION}"

'''


class SettingsInitializationTests(unittest.TestCase):
    def test_first_run_copies_example_and_resolves_relative_source(self) -> None:
        with temporary_workspace() as temp:
            root = Path(temp)
            settings = root / "skills/settings.toml"
            example = root / "skills/settings.toml.example"
            source = root / "original-fpf" / "FPF-Spec.md"
            source.parent.mkdir()
            source.write_text("# FPF\n", encoding="utf-8")
            example.parent.mkdir()
            example.write_text(PACKAGE + '[paths]\nfpf_original_repo = "original-fpf"\n' + SKILLS, encoding="utf-8")

            resolved, created = read_fpf_source(settings, example)

            self.assertTrue(created)
            self.assertEqual(settings.read_bytes(), example.read_bytes())
            self.assertEqual(resolved, source.resolve())


class ExistingSettingsTests(unittest.TestCase):
    def test_existing_settings_are_preserved(self) -> None:
        with temporary_workspace() as temp:
            root = Path(temp)
            settings = root / "skills/settings.toml"
            example = root / "skills/settings.toml.example"
            settings.parent.mkdir()
            settings.write_text('[paths]\nfpf_original_repo = "custom"\n' + SKILLS, encoding="utf-8")
            example.write_text(PACKAGE + '[paths]\nfpf_original_repo = "example"\n' + SKILLS, encoding="utf-8")

            created = ensure_settings(settings, example)

            self.assertFalse(created)
            self.assertEqual(settings.read_text(encoding="utf-8"), '[paths]\nfpf_original_repo = "custom"\n' + SKILLS)

class LegacySettingsCompatibilityTests(unittest.TestCase):
    def test_legacy_five_setting_panel_defaults_output_language_to_auto(self) -> None:
        with temporary_workspace() as temp:
            root = Path(temp)
            settings = root / "skills/settings.toml"
            example = root / "skills/settings.toml.example"
            settings.parent.mkdir()
            legacy = SKILLS.replace('output_language = "auto"\n', "")
            settings.write_text('[paths]\nfpf_original_repo = "FPF"\n' + legacy, encoding="utf-8")
            example.write_text(PACKAGE + '[paths]\nfpf_original_repo = "FPF"\n' + SKILLS, encoding="utf-8")

            from service.scripts.init_settings.init_settings import read_skill_settings

            values, created = read_skill_settings(settings, example)

            self.assertFalse(created)
            self.assertEqual("auto", values["output_language"])


class SettingsSchemaMigrationTests(unittest.TestCase):
    def test_apply_migrates_the_file_and_preserves_existing_values(self) -> None:
        with temporary_workspace() as temp:
            root = Path(temp)
            settings = root / "skills/settings.toml"
            example = root / "skills/settings.toml.example"
            settings.parent.mkdir()
            legacy = SKILLS.replace('output_language = "auto"\n', "").replace(
                'output_style = "general"', 'output_style = "ste"'
            )
            settings.write_text('[paths]\nfpf_original_repo = "custom-fpf"\n' + legacy, encoding="utf-8")
            example.write_text(PACKAGE + '[paths]\nfpf_original_repo = "example"\n' + SKILLS, encoding="utf-8")

            values, created, migration_needed = migrate_settings(settings, example, apply=True)

            self.assertFalse(created)
            self.assertTrue(migration_needed)
            self.assertEqual("custom-fpf", values["paths"]["fpf_original_repo"])
            self.assertEqual("ste", values["skills"]["output_style"])
            self.assertEqual("auto", values["skills"]["output_language"])
            migrated = settings.read_text(encoding="utf-8")
            self.assertIn('fpf_original_repo = "custom-fpf"', migrated)
            self.assertIn('output_style = "ste"', migrated)
            self.assertIn('output_language = "auto"', migrated)
            self.assertIn(f'version = "{CURRENT_VERSION}"', migrated)
            archive = settings.with_name(f"settings.{CURRENT_VERSION}.toml")
            self.assertTrue(archive.is_file())
            self.assertNotIn('output_language = "auto"', archive.read_text(encoding="utf-8"))


class SettingsSnapshotCollisionTests(unittest.TestCase):
    def test_migration_never_overwrites_an_existing_version_snapshot(self) -> None:
        with temporary_workspace() as temp:
            root = Path(temp)
            settings = root / "skills/settings.toml"
            example = root / "skills/settings.toml.example"
            settings.parent.mkdir()
            legacy = '[paths]\nfpf_original_repo = "old"\n' + SKILLS.replace(
                'output_language = "auto"\n', ""
            )
            settings.write_text(legacy, encoding="utf-8")
            example.write_text(PACKAGE + '[paths]\nfpf_original_repo = "example"\n' + SKILLS, encoding="utf-8")
            first = settings.with_name(f"settings.{CURRENT_VERSION}.toml")
            first.write_text("never overwrite\n", encoding="utf-8")

            migrate_settings(settings, example, apply=True)

            self.assertEqual("never overwrite\n", first.read_text(encoding="utf-8"))
            self.assertEqual(
                legacy,
                settings.with_name(f"settings.{CURRENT_VERSION}.2.toml").read_text(encoding="utf-8"),
            )


class SettingsVersionUpdateTests(unittest.TestCase):
    def test_version_update_archives_under_the_declared_old_version(self) -> None:
        with temporary_workspace() as temp:
            root = Path(temp)
            settings = root / "skills/settings.toml"
            example = root / "skills/settings.toml.example"
            settings.parent.mkdir()
            old_version = "0.0.9"
            old_package = PACKAGE.replace(CURRENT_VERSION, old_version)
            old_text = old_package + '[paths]\nfpf_original_repo = "kept"\n' + SKILLS
            settings.write_text(old_text, encoding="utf-8")
            example.write_text(PACKAGE + '[paths]\nfpf_original_repo = "example"\n' + SKILLS, encoding="utf-8")

            values, _, migration_needed = migrate_settings(settings, example, apply=True)

            self.assertTrue(migration_needed)
            self.assertEqual(CURRENT_VERSION, values["package"]["version"])
            self.assertEqual(
                old_text,
                settings.with_name("settings.0.0.9.toml").read_text(encoding="utf-8"),
            )
            self.assertIn(f'version = "{CURRENT_VERSION}"', settings.read_text(encoding="utf-8"))


class SettingsResolutionTests(unittest.TestCase):
    def test_npf_source_uses_the_same_original_repository_setting(self) -> None:
        with temporary_workspace() as temp:
            root = Path(temp)
            settings = root / "skills/settings.toml"
            example = root / "skills/settings.toml.example"
            settings.parent.mkdir()
            settings.write_text('[paths]\nfpf_original_repo = "original-fpf"\n' + SKILLS, encoding="utf-8")
            example.write_text(PACKAGE + '[paths]\nfpf_original_repo = "example"\n' + SKILLS, encoding="utf-8")

            resolved, created = read_npf_source(settings, example)

            self.assertFalse(created)
            self.assertEqual(
                resolved,
                (root / "original-fpf" / "Narrativization-and-Narrative-Studies-Principles-Framework.md").resolve(),
            )

    def test_only_control_panel_sections_are_allowed(self) -> None:
        with temporary_workspace() as temp:
            root = Path(temp)
            settings = root / "skills/settings.toml"
            example = root / "skills/settings.toml.example"
            settings.parent.mkdir()
            settings.write_text('[paths]\nfpf_original_repo = "FPF"\nextra = "no"\n' + SKILLS, encoding="utf-8")
            example.write_text(PACKAGE + '[paths]\nfpf_original_repo = "FPF"\n' + SKILLS, encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "exactly fpf_original_repo"):
                read_fpf_source(settings, example)


if __name__ == "__main__":
    unittest.main()
