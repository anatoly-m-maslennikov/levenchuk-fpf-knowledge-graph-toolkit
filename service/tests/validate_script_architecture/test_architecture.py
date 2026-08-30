import unittest
from pathlib import Path

from service.scripts.filesystem_policy import temporary_workspace
from service.scripts.validate_script_architecture.validate_script_architecture_workers.ast_rules import check_file
from service.scripts.validate_script_architecture.validate_script_architecture_workers.assets import load_policy
from service.scripts.validate_script_architecture.validate_script_architecture_workers.layout import (
    check_cache_placement,
    check_service_boundary,
)


POLICY_PATH = (
    Path(__file__).resolve().parents[3]
    / "service"
    / "scripts"
    / "validate_script_architecture"
    / "validate_script_architecture_assets"
    / "policy.json"
)


class ArchitectureBoundaryTests(unittest.TestCase):
    def test_service_content_outside_three_boundaries_fails(self) -> None:
        with temporary_workspace() as temporary:
            service = Path(temporary) / "service"
            (service / "scripts").mkdir(parents=True)
            (service / "tests").mkdir()
            (service / "skills").mkdir()
            legacy = service / "legacy_tool"
            legacy.mkdir()
            (legacy / "tool.py").write_text("VALUE = 1\n", encoding="utf-8")
            self.assertTrue(check_service_boundary(service))

    def test_bytecode_outside_runtime_fails(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary)
            misplaced = root / "service" / "__pycache__" / "tool.pyc"
            misplaced.parent.mkdir(parents=True)
            misplaced.write_bytes(b"cache")
            expected = root / ".runtime" / "pycache" / "tool.pyc"
            expected.parent.mkdir(parents=True)
            expected.write_bytes(b"cache")
            self.assertEqual(len(check_cache_placement(root)), 1)


class ArchitectureRuleTests(unittest.TestCase):
    def test_oversized_file_and_function_fail(self) -> None:
        policy = load_policy(POLICY_PATH)
        with temporary_workspace() as temporary:
            root = Path(temporary)
            path = root / "oversized.py"
            body = "def oversized():\n" + "".join("    value = 1\n" for _ in range(41))
            path.write_text(body + "\n" * 170, encoding="utf-8")
            errors, _ = check_file(path, root, policy)
            self.assertTrue(any("Python file exceeds" in item for item in errors))
            self.assertTrue(any("atomic object exceeds" in item for item in errors))

    def test_large_dictionary_literal_fails(self) -> None:
        policy = load_policy(POLICY_PATH)
        with temporary_workspace() as temporary:
            root = Path(temporary)
            path = root / "dictionary.py"
            entries = ", ".join(f"'{index}': {index}" for index in range(9))
            path.write_text(f"VALUES = {{{entries}}}\n", encoding="utf-8")
            errors, _ = check_file(path, root, policy)
            self.assertTrue(any("large dictionary literal" in item for item in errors))
