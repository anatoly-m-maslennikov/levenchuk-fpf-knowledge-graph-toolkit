#!/usr/bin/env python3
"""Regression checks for repository-local FPF source settings."""

from __future__ import annotations

import unittest
from pathlib import Path

from scripts.filesystem_policy import temporary_workspace
from scripts.init_settings.init_settings import ensure_settings, read_fpf_source, read_npf_source

SKILLS = '''
[skills]
output_style = "general"
fpf_terms_explained = "off"
save_report = "on"
report_style = "plain"
install_method = "copy"
'''


class SettingsInitializationTests(unittest.TestCase):
    def test_first_run_copies_example_and_resolves_relative_source(self) -> None:
        with temporary_workspace() as temp:
            root = Path(temp)
            settings = root / ".caprmedio/settings.toml"
            example = root / ".caprmedio/settings.toml.example"
            source = root / "original-fpf" / "FPF-Spec.md"
            source.parent.mkdir()
            source.write_text("# FPF\n", encoding="utf-8")
            example.parent.mkdir()
            example.write_text('[paths]\nfpf_original_repo = "original-fpf"\n' + SKILLS, encoding="utf-8")

            resolved, created = read_fpf_source(settings, example)

            self.assertTrue(created)
            self.assertEqual(settings.read_bytes(), example.read_bytes())
            self.assertEqual(resolved, source.resolve())

    def test_existing_settings_are_preserved(self) -> None:
        with temporary_workspace() as temp:
            root = Path(temp)
            settings = root / ".caprmedio/settings.toml"
            example = root / ".caprmedio/settings.toml.example"
            settings.parent.mkdir()
            settings.write_text('[paths]\nfpf_original_repo = "custom"\n' + SKILLS, encoding="utf-8")
            example.write_text('[paths]\nfpf_original_repo = "example"\n' + SKILLS, encoding="utf-8")

            created = ensure_settings(settings, example)

            self.assertFalse(created)
            self.assertEqual(settings.read_text(encoding="utf-8"), '[paths]\nfpf_original_repo = "custom"\n' + SKILLS)



class SettingsResolutionTests(unittest.TestCase):
    def test_npf_source_uses_the_same_original_repository_setting(self) -> None:
        with temporary_workspace() as temp:
            root = Path(temp)
            settings = root / ".caprmedio/settings.toml"
            example = root / ".caprmedio/settings.toml.example"
            settings.parent.mkdir()
            settings.write_text('[paths]\nfpf_original_repo = "original-fpf"\n' + SKILLS, encoding="utf-8")
            example.write_text('[paths]\nfpf_original_repo = "example"\n' + SKILLS, encoding="utf-8")

            resolved, created = read_npf_source(settings, example)

            self.assertFalse(created)
            self.assertEqual(
                resolved,
                (root / "original-fpf" / "Narrativization-and-Narrative-Studies-Principles-Framework.md").resolve(),
            )

    def test_only_control_panel_sections_are_allowed(self) -> None:
        with temporary_workspace() as temp:
            root = Path(temp)
            settings = root / ".caprmedio/settings.toml"
            example = root / ".caprmedio/settings.toml.example"
            settings.parent.mkdir()
            settings.write_text('[paths]\nfpf_original_repo = "FPF"\nextra = "no"\n' + SKILLS, encoding="utf-8")
            example.write_text('[paths]\nfpf_original_repo = "FPF"\n' + SKILLS, encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "exactly fpf_original_repo"):
                read_fpf_source(settings, example)


if __name__ == "__main__":
    unittest.main()
