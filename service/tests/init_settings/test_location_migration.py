import unittest
from pathlib import Path

from service.scripts.filesystem_policy import temporary_workspace
from service.scripts.init_settings.init_settings_workers.location_migration import (
    migrate_legacy_control_panel,
)


class SettingsLocationMigrationTests(unittest.TestCase):
    def test_moves_current_settings_to_external_control_directory(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary)
            legacy = root / ".caprmedio"
            legacy.mkdir()
            source = legacy / "settings.toml"
            source.write_text('[package]\nname = "fpf"\nversion = "0.1.1"\n', encoding="utf-8")
            target = root / "external" / "settings.toml"

            self.assertTrue(migrate_legacy_control_panel(legacy, target, "0.1.2"))

            self.assertFalse(source.exists())
            self.assertEqual(target.read_text(encoding="utf-8"), '[package]\nname = "fpf"\nversion = "0.1.1"\n')


class SettingsLocationCollisionTests(unittest.TestCase):
    def test_never_overwrites_current_or_historical_settings(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary)
            legacy = root / ".caprmedio"
            external = root / "external"
            legacy.mkdir()
            external.mkdir()
            (legacy / "settings.toml").write_text(
                '[package]\nname = "fpf"\nversion = "0.1.1"\n', encoding="utf-8",
            )
            (legacy / "settings.0.1.1.toml").write_text("older\n", encoding="utf-8")
            target = external / "settings.toml"
            target.write_text("current\n", encoding="utf-8")
            (external / "settings.0.1.1.toml").write_text("keep\n", encoding="utf-8")

            migrate_legacy_control_panel(legacy, target, "0.1.2")

            self.assertEqual(target.read_text(encoding="utf-8"), "current\n")
            self.assertEqual((external / "settings.0.1.1.toml").read_text(), "keep\n")
            self.assertIn("version", (external / "settings.0.1.1.2.toml").read_text())
            self.assertEqual((external / "settings.0.1.1.3.toml").read_text(), "older\n")


if __name__ == "__main__":
    unittest.main()
