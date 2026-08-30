from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

from service.scripts.filesystem_policy import temporary_workspace


ROOT = Path(__file__).resolve().parents[3]
PATH = ROOT / "skills/fpf.skill/scripts/plan_fpf_report.py"
SPEC = importlib.util.spec_from_file_location("plan_fpf_report", PATH)
assert SPEC and SPEC.loader
REPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REPORT)


TOPOLOGY = [
    {"id": "project", "kind": "project", "depth": 0, "contains": ["project", "layer", "f1", "f2", "b1", "b2"]},
    {"id": "layer", "kind": "structural", "depth": 1, "contains": ["layer", "f1", "f2"]},
    {"id": "f1", "kind": "structural", "depth": 2, "contains": ["f1"]},
    {"id": "f2", "kind": "structural", "depth": 2, "contains": ["f2"]},
    {"id": "b1", "kind": "bseed", "depth": 1, "contains": ["b1"], "cumulative_contains": ["b1"], "bseed_order": 1},
    {"id": "b2", "kind": "bseed", "depth": 1, "contains": ["b2"], "cumulative_contains": ["b1", "b2"], "bseed_order": 2},
]


class ReportDeliveryTests(unittest.TestCase):
    def test_plain_path_never_overwrites(self) -> None:
        with temporary_workspace(prefix="fpf-report-") as temporary:
            root = Path(temporary)
            first = REPORT.plain_report_path(
                root, "design-challenge", "Review API design", "20260829T010203Z",
            )
            first.parent.mkdir()
            first.write_text("existing", encoding="utf-8")
            second = REPORT.plain_report_path(
                root, "design-challenge", "Review API design", "20260829T010203Z",
            )
            self.assertEqual("20260829T010203Z-fpf-design-challenge-review-api-design-2.md", second.name)

    def test_selects_narrowest_structural_scope_unit(self) -> None:
        self.assertEqual("f1", REPORT.select_scope_unit(TOPOLOGY, ["f1"]))
        self.assertEqual("layer", REPORT.select_scope_unit(TOPOLOGY, ["f1", "f2"]))

    def test_selects_lowest_downstream_bseed_scope_unit(self) -> None:
        self.assertEqual("b2", REPORT.select_scope_unit(TOPOLOGY, ["b1", "b2"]))

    def test_mixed_bseed_and_structural_scope_requires_project_authority(self) -> None:
        self.assertEqual("project", REPORT.select_scope_unit(TOPOLOGY, ["b1", "f1"]))
        without_project_scope = [dict(item) for item in TOPOLOGY]
        without_project_scope[0]["contains"] = ["project", "layer", "f1", "f2"]
        with self.assertRaisesRegex(ValueError, "no proven"):
            REPORT.select_scope_unit(without_project_scope, ["b1", "f1"])


if __name__ == "__main__":
    unittest.main()
