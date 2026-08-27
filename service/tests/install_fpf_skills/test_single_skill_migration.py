import json
import unittest
from pathlib import Path

from service.filesystem_policy import logical_path_exists, temporary_workspace
from skills.install_fpf_skills.install_fpf_skills_workers import cli
from skills.install_fpf_skills.install_fpf_skills_workers.snapshots import suite_digest
from service.tests.install_fpf_skills.helpers import make_source, run_with_method


RETIRED = list(cli.load_catalog(cli.CATALOG_PATH)["retired_end_user_skills"])


def make_legacy_copy(destination: Path) -> dict[str, Path]:
    roots: dict[str, Path] = {}
    for name in RETIRED:
        package = destination / name
        package.mkdir(parents=True)
        (package / "SKILL.md").write_text(f"legacy {name}\n", encoding="utf-8")
        roots[name] = package
    receipt = {
        "schema_version": 1,
        "method": "copy",
        "source_hash": suite_digest(roots, RETIRED),
        "skills": RETIRED,
    }
    (destination / ".fpf-skills-install.json").write_text(
        json.dumps(receipt), encoding="utf-8"
    )
    return roots


class SingleSkillMigrationTests(unittest.TestCase):
    def test_managed_legacy_copy_is_replaced_by_one_fpf_package(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary)
            source = make_source(root / "source")
            destination = root / "installed"
            make_legacy_copy(destination)
            apply = ["--apply", "--destination", str(destination)]
            self.assertEqual(run_with_method(source, root / "control", destination, "copy", apply), 0)
            self.assertTrue((destination / "fpf" / "SKILL.md").is_file())
            self.assertFalse(any(
                any((destination / name).rglob("*")) for name in RETIRED
            ))
            receipt = json.loads((destination / ".fpf-skills-install.json").read_text())
            self.assertEqual(["fpf"], receipt["skills"])
            self.assertEqual(4, receipt["schema_version"])

    def test_modified_legacy_copy_is_removed_as_repo_owned_leftover(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary)
            source = make_source(root / "source")
            destination = root / "installed"
            roots = make_legacy_copy(destination)
            (roots[RETIRED[0]] / "custom.md").write_text("keep\n", encoding="utf-8")
            apply = ["--apply", "--destination", str(destination)]
            self.assertEqual(run_with_method(source, root / "control", destination, "copy", apply), 0)
            self.assertFalse(logical_path_exists(roots[RETIRED[0]]))
            self.assertTrue((destination / "fpf" / "SKILL.md").is_file())


class LegacyLeftoverCleanupTests(unittest.TestCase):
    def test_apply_removes_every_known_repo_owned_legacy_shape(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary)
            source = make_source(root / "source")
            destination = root / "installed"
            leftovers = [
                destination / "graph-fpf-convert-from-original",
                destination / "fpf-route.skill",
                destination / ".fpf.backup-deadbeef",
            ]
            for path in leftovers:
                path.mkdir(parents=True)
                (path / "old.txt").write_text("obsolete\n", encoding="utf-8")
            files = [
                destination / ".fpf-service-skills-install.json",
                destination / ".DS_Store",
                destination / "..fpf-runtime.toml.crashed",
            ]
            for path in files:
                path.write_text("obsolete\n", encoding="utf-8")

            apply = ["--apply", "--destination", str(destination)]
            self.assertEqual(run_with_method(source, root / "control", destination, "copy", apply), 0)
            self.assertFalse(any(logical_path_exists(path) for path in leftovers + files))
            self.assertTrue((destination / "fpf" / ".fpf-runtime.toml").is_file())


if __name__ == "__main__":
    unittest.main()
