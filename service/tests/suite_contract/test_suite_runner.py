from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

from service.scripts.filesystem_policy import temporary_workspace
from service.tests.suite_runner import REQUIRED_CASE_NAMES, _load_cases, _run_case


def _case(name: str) -> dict[str, object]:
    return {"name": name, "command": [sys.executable, "-c", "pass"]}


class SuiteContractTests(unittest.TestCase):
    def _write(self, root: Path, cases: list[dict[str, object]]) -> Path:
        path = root / "cases.json"
        path.write_text(json.dumps(cases), encoding="utf-8")
        return path

    def test_rejects_empty_duplicate_and_missing_case_manifests(self) -> None:
        with temporary_workspace(prefix="fpf-suite-contract-") as temporary:
            root = Path(temporary)
            with self.assertRaisesRegex(ValueError, "non-empty"):
                _load_cases(self._write(root, []))
            duplicate = [_case(name) for name in sorted(REQUIRED_CASE_NAMES)]
            duplicate.append(_case(duplicate[0]["name"]))
            with self.assertRaisesRegex(ValueError, "unique"):
                _load_cases(self._write(root, duplicate))
            missing = [_case(name) for name in sorted(REQUIRED_CASE_NAMES)[1:]]
            with self.assertRaisesRegex(ValueError, "omits required"):
                _load_cases(self._write(root, missing))

    def test_timeout_is_a_failure(self) -> None:
        with temporary_workspace(prefix="fpf-suite-timeout-") as temporary:
            result = _run_case(
                {
                    "name": "hang", "timeout_seconds": 0.05,
                    "command": [sys.executable, "-c", "import time; time.sleep(2)"],
                },
                Path(temporary),
            )
            self.assertEqual(124, result["returncode"])
            self.assertTrue(result["timed_out"])


if __name__ == "__main__":
    unittest.main()
