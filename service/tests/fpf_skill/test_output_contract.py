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
        analytical = (SKILL_ROOT / "references/fpf-analysis-output.md").read_text(encoding="utf-8")
        composition = (SKILL_ROOT / "references/fpf-composition.md").read_text(encoding="utf-8")
        plan = (SKILL_ROOT / "references/fpf-plan-output.md").read_text(encoding="utf-8")

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

        for requirement in (
            "stable issue ID",
            "issue confidence and evidence basis",
            "independent fix confidence and evidence basis",
            "relationship: `alternative`, `complementary`, or `required prerequisite`",
            "mapped fix IDs or an explicit no-fix disposition",
            "exactly one `### Fix and improvement register`",
            "A persistence failure changes the report outcome",
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
        for requirement in (
            "### Composition receipt", "one result for every typed edge",
            "context-ledger read/used/deferred counts", "One consolidated registry pair",
            "Do not list a consumer that stopped at its incoming handoff",
        ):
            self.assertIn(requirement, analytical)

    def test_plan_has_a_distinct_routing_contract(self) -> None:
        plan = (SKILL_ROOT / "references/fpf-plan-output.md").read_text(encoding="utf-8")
        for heading in (
            "## Task, scope, and boundaries",
            "## Routing decisions and recommendations",
            "## Unresolved evidence gaps",
            "## Skills used",
        ):
            self.assertIn(heading, plan)
        for requirement in (
            "**Routing confidence** with concrete routing evidence",
            "List only missing evidence or unanswered routing questions",
            "**FPF methodology sources:** not applicable",
            "explicit statement that no proposed analytical node executed",
            "include one copy-ready composition",
            "List exactly `$fpf plan`",
            "For every handoff, include a separate record",
            "Never label this field only `Handoff confidence`",
        ):
            self.assertIn(requirement, plan)

    def test_runtime_owns_one_shared_output_finalizer_per_result_kind(self) -> None:
        marker = "Apply that contract's final conformance gate after this prompt"
        prompts = (
            "problem-frame", "structure-recover", "applicability-scan", "sota-harvest",
            "options-explore", "evaluation-design", "design-challenge", "decision-synthesize",
            "quality-improve", "alignment-audit",
        )
        for name in prompts:
            text = (SKILL_ROOT / f"prompts/fpf-{name}.md").read_text(encoding="utf-8")
            self.assertNotIn(marker, text, name)
            for heading in OLD_CONFIDENCE_BUCKET_HEADINGS:
                self.assertNotIn(heading, text, name)
        runtime = (SKILL_ROOT / "prompts/fpf-runtime.md").read_text(encoding="utf-8")
        self.assertIn("references/fpf-plan-output.md` last", runtime)
        self.assertIn("references/fpf-analysis-output.md` last", runtime)

    def test_russian_area_help_preserves_canonical_command_ids(self) -> None:
        commands = (
            "problem frame", "structure recover", "applicability scan", "sota harvest",
            "options explore", "evaluation design", "design challenge", "decision synthesize",
            "quality improve", "alignment audit",
        )
        for area in ("framework", "software", "skills"):
            text = (SKILL_ROOT / f"prompts/help/ru/fpf-help-{area}.md").read_text(encoding="utf-8")
            for command in commands:
                self.assertIn(f"`$fpf {command} ", text, (area, command))
            self.assertIn("псевдоним", text)

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
