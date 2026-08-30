from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SKILL_ROOT = ROOT / "skills/fpf.skill"


class ReportDeliveryContractTests(unittest.TestCase):
    def test_plain_delivery_is_collision_safe_without_a_runtime_helper(self) -> None:
        text = (SKILL_ROOT / "references/fpf-report-persistence.md").read_text(encoding="utf-8")
        self.assertIn("Never overwrite", text)
        self.assertIn("append `-2`, then `-3`, and so on", text)
        self.assertIn("UTF-8", text)
        self.assertNotIn("plan_fpf_report", text)

    def test_caprmedio_delivery_keeps_scope_and_bseed_rules(self) -> None:
        text = (SKILL_ROOT / "references/fpf-caprmedio-report-adapter.md").read_text(encoding="utf-8")
        for requirement in ("narrowest structural Scope Unit", "BSEED special case", "project-native Atom creation operation", "stop unsaved"):
            self.assertIn(requirement, text)

    def test_persistence_is_loaded_only_after_saving_is_enabled(self) -> None:
        runtime = (SKILL_ROOT / "prompts/fpf-runtime.md").read_text(encoding="utf-8")
        self.assertIn("Load `references/fpf-report-persistence.md` only after report saving resolves to on", runtime)
        self.assertIn("load the CAPRMEDIO adapter only when report style is `caprmedio`", runtime)


if __name__ == "__main__":
    unittest.main()
