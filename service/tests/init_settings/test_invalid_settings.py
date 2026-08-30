import unittest
from pathlib import Path

from service.scripts.filesystem_policy import temporary_workspace
from service.scripts.init_settings.init_settings import read_skill_settings, read_skill_version


SKILLS = '''[skills]
output_language = "auto"
output_style = "general"
fpf_terms_explained = "off"
save_report = "on"
report_style = "plain"
install_method = "copy"
'''
INVALID_VALUES = {
    "output_language": "klingon", "output_style": "verbose",
    "fpf_terms_explained": "sometimes", "save_report": "maybe",
    "report_style": "caprmedio-unsafe", "install_method": "junction",
}


class InvalidSettingsTests(unittest.TestCase):
    def test_rejects_every_invalid_skill_setting_value(self) -> None:
        valid = (
            f'[package]\nname = "fpf"\nversion = "{read_skill_version()}"\n\n'
            '[paths]\nfpf_original_repo = "FPF"\n' + SKILLS
        )
        for key, value in INVALID_VALUES.items():
            with self.subTest(key=key), temporary_workspace() as temporary:
                root = Path(temporary)
                settings = root / "settings.toml"
                example = root / "settings.toml.example"
                marker = next(line for line in valid.splitlines() if line.startswith(f"{key} = "))
                settings.write_text(valid.replace(marker, f'{key} = "{value}"'), encoding="utf-8")
                example.write_text(valid, encoding="utf-8")
                with self.assertRaisesRegex(ValueError, key):
                    read_skill_settings(settings, example)
