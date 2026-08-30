from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from service.scripts.filesystem_policy import temporary_workspace
from service.scripts.validate_repository.validate_repository_workers.skills import (
    validate_reference_contracts,
)


ROOT = Path(__file__).resolve().parents[3]
SKILL_ROOT = ROOT / "skills" / "fpf.skill"
CONTRACTS = json.loads(
    (ROOT / "service/scripts/validate_repository/validate_repository_assets/contracts.json").read_text(
        encoding="utf-8"
    )
)
OLD_CONFIDENCE_BUCKET_HEADINGS = (
    "## High-confidence results (>=95%)",
    "## Open questions (confidence <95%)",
)


class OutputContractTests(unittest.TestCase):
    def test_issue_centered_contract_replaces_confidence_buckets(self) -> None:
        analytical = (SKILL_ROOT / "references/fpf-analysis-contract.md").read_text(encoding="utf-8")
        composition = (SKILL_ROOT / "references/fpf-composition.md").read_text(encoding="utf-8")
        plan = (SKILL_ROOT / "prompts/fpf-plan.md").read_text(encoding="utf-8")

        for text in (analytical, composition, plan):
            for old_heading in OLD_CONFIDENCE_BUCKET_HEADINGS:
                self.assertNotIn(old_heading, text)

        for heading in (
            "## Task, scope, and boundaries",
            "## Issues, weak points, and improvements",
            "## Unresolved evidence gaps",
            "## Skills used",
        ):
            self.assertIn(heading, analytical)
            self.assertIn(heading, composition)

        for requirement in (
            "stable issue ID",
            "issue confidence and its evidence basis",
            "fix confidence and its own evidence basis",
            "relationship: `alternative`, `complementary`, or `required prerequisite`",
            "Every issue must map to one or more fix IDs or an explicit disposition",
            "deduplicated, ordered fix and improvement register",
        ):
            self.assertIn(requirement, analytical)

        for requirement in (
            "Stable consolidated issues",
            "One repair and improvement register",
            "issue confidence, its evidence basis",
            "fix confidence and its own evidence basis",
            "every issue must map to a fix or an explicit disposition",
            "one consolidated register",
        ):
            self.assertIn(requirement, composition)

    def test_plan_has_a_distinct_routing_contract(self) -> None:
        plan = (SKILL_ROOT / "prompts/fpf-plan.md").read_text(encoding="utf-8")
        for heading in (
            "## Task, scope, and boundaries",
            "## Routing decisions and recommendations",
            "## Unresolved evidence gaps",
            "## Skills used",
        ):
            self.assertIn(heading, plan)
        for requirement in (
            "**Routing confidence** and its concrete routing-evidence basis",
            "It is not issue confidence, fix confidence",
            "Section 3 contains only genuine missing evidence or unanswered routing questions",
            "FPF methodology sources:** not applicable",
            "Execution boundary",
        ):
            self.assertIn(requirement, plan)

    def test_repository_validator_rejects_a_confidence_bucket_heading(self) -> None:
        with temporary_workspace(prefix="fpf-output-contract-") as temporary:
            root = Path(temporary)
            target = root / "contract.md"
            target.write_text("## High-confidence results (>=95%)\n", encoding="utf-8")
            contracts = copy.deepcopy(CONTRACTS)
            contracts["reference_fragments"] = {}
            contracts["forbidden_contract_fragments"] = {
                "contract.md": ["## High-confidence results (>=95%)"]
            }
            errors = validate_reference_contracts(root, contracts)
        self.assertEqual(
            ["contract.md retains forbidden contract text: ## High-confidence results (>=95%)"],
            errors,
        )


if __name__ == "__main__":
    unittest.main()
