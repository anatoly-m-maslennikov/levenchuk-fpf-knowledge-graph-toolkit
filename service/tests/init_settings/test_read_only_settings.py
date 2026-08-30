import unittest
import os
import subprocess
import sys
from pathlib import Path

from service.scripts.filesystem_policy import temporary_workspace
from service.scripts.init_settings.init_settings import (
    migrate_settings, read_skill_version, settings_paths_for_root,
)


class ReadOnlySettingsTests(unittest.TestCase):
    def test_preflight_uses_example_without_creating_settings(self) -> None:
        with temporary_workspace() as temp:
            root = Path(temp)
            settings = root / "external/settings.toml"
            example = root / "skills/settings.toml.example"
            example.parent.mkdir(parents=True)
            example.write_text(
                f'[package]\nname = "fpf"\nversion = "{read_skill_version()}"\n\n'
                '[paths]\nfpf_original_repo = "original-fpf"\n\n'
                '[skills]\noutput_language = "auto"\noutput_style = "general"\n'
                'fpf_terms_explained = "off"\nsave_report = "on"\n'
                'report_style = "plain"\ninstall_method = "copy"\n',
                encoding="utf-8",
            )

            values, created, pending = migrate_settings(
                settings, example, create_if_missing=False,
            )

            self.assertFalse(settings.exists())
            self.assertFalse(created)
            self.assertTrue(pending)
            self.assertEqual("original-fpf", values["paths"]["fpf_original_repo"])

class PublicCheckReadOnlyTests(unittest.TestCase):
    def test_public_sync_check_does_not_create_external_settings(self) -> None:
        repository = Path(__file__).resolve().parents[3]
        with temporary_workspace(prefix="fpf-read-only-check-") as temp:
            external = Path(temp) / "external"
            environment = dict(os.environ, FPF_TOOLKIT_CONFIG_DIR=str(external))
            result = subprocess.run(
                [sys.executable, "-m", "service.scripts.sync_fpf_skill_settings", "--check"],
                cwd=repository, env=environment, text=True, capture_output=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertFalse(external.exists())

class PortableDefaultsTests(unittest.TestCase):
    def test_external_preferences_do_not_change_portable_prompt_check(self) -> None:
        repository = Path(__file__).resolve().parents[3]
        targets = [
            repository / "skills/fpf.skill/references/fpf-analysis-contract.md",
            repository / "skills/fpf.skill/prompts/fpf-plan.md",
        ]
        before = {path: path.read_bytes() for path in targets}
        with temporary_workspace(prefix="fpf-external-preferences-") as temp:
            external = Path(temp) / "external"
            external.mkdir()
            example = (repository / "skills/settings.toml.example").read_text(encoding="utf-8")
            (external / "settings.toml").write_text(
                example.replace('output_style = "general"', 'output_style = "ste"'),
                encoding="utf-8",
            )
            environment = dict(os.environ, FPF_TOOLKIT_CONFIG_DIR=str(external))
            result = subprocess.run(
                [sys.executable, "-m", "service.scripts.sync_fpf_skill_settings", "--check"],
                cwd=repository, env=environment, text=True, capture_output=True,
                check=False,
            )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(before, {path: path.read_bytes() for path in targets})


class RootScopedSettingsTests(unittest.TestCase):
    def test_distinct_checkouts_receive_distinct_external_settings_paths(self) -> None:
        with temporary_workspace(prefix="fpf-root-settings-") as temporary:
            parent = Path(temporary)
            first = parent / "first"
            second = parent / "second"
            first.mkdir()
            second.mkdir()
            first_settings, first_example = settings_paths_for_root(first)
            second_settings, second_example = settings_paths_for_root(second)
            self.assertNotEqual(first_settings, second_settings)
            self.assertEqual((first / "skills/settings.toml.example").resolve(), first_example)
            self.assertEqual((second / "skills/settings.toml.example").resolve(), second_example)


if __name__ == "__main__":
    unittest.main()
