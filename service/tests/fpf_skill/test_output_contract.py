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
        self.assertIn("# Proposed plan", plan)
        for requirement in (
            "Reply `do` to execute this plan.",
            "one ordered list",
            "complete validated result of step 1",
            "no copy-ready invocation",
            "commands_executed` contains only `$fpf plan`",
            "methodology sources are empty",
        ):
            self.assertIn(requirement, plan)
        for obsolete in (
            "## Task, scope, and boundaries",
            "## Routing decisions and recommendations",
        ):
            self.assertNotIn(obsolete, plan)

    def test_approved_plan_is_resumable_and_questions_are_blocking_only(self) -> None:
        manager = (SKILL_ROOT / "prompts/fpf-manager.md").read_text(encoding="utf-8")
        runtime = (SKILL_ROOT / "prompts/fpf-runtime.md").read_text(encoding="utf-8")
        execution = (SKILL_ROOT / "references/fpf-plan-execution.md").read_text(
            encoding="utf-8"
        )
        for requirement in (
            "most recent validated, released, unexecuted FPF Plan",
            "Exact `do` approves that Plan once",
            "Pass the preceding immutable set's complete candidate",
            "two or three mutually exclusive variants",
            "automatically continue",
            "without another `do`",
        ):
            self.assertIn(requirement, manager + execution)
        self.assertIn("QUESTION_READY", runtime)
        self.assertIn("defaults to 95%", execution)
        self.assertIn("0% through 100%", execution)
        self.assertIn("active blocking-decision threshold", execution)
        self.assertIn("operator may explicitly change it", execution)
        self.assertIn("never weakens an exact `STOP_*` gate", execution)
        self.assertIn("lower-confidence analytical finding is never a blocking question", runtime)

    def test_new_requests_are_plan_first_and_direct_execution_is_explicit(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        manager = (SKILL_ROOT / "prompts/fpf-manager.md").read_text(encoding="utf-8")
        runtime = (SKILL_ROOT / "prompts/fpf-runtime.md").read_text(encoding="utf-8")
        graph = (SKILL_ROOT / "references/fpf-command-graph.md").read_text(encoding="utf-8")
        for requirement in (
            "A new invocation produces a Plan by default",
            "Direct execution is allowed only when the operator explicitly asks",
        ):
            self.assertIn(requirement, skill)
        for requirement in (
            "Every new non-Help invocation is `plan-first` by default",
            "`direct-without-plan`",
            "A bare command, `+` stack, `do it`, `run`, `now`, urgency, or prior preference is not a bypass",
            "authority parsing, not analytical routing",
        ):
            self.assertIn(requirement, manager)
        self.assertIn("Under `plan-first`, always select `plan`", runtime)
        self.assertIn("Before exact `do`, an explicit stack only constrains the Plan", runtime)
        self.assertIn("A valid requested stack is normalized to canonical commands and returned as a Plan", graph)

    def test_analysis_finalizer_accepts_h1_or_h2_without_relaxing_names(self) -> None:
        text = (SKILL_ROOT / "references/fpf-analysis-output.md").read_text(encoding="utf-8")
        self.assertIn("may be Markdown `#` or `##`", text)
        self.assertIn("one consistent top level", text)
        self.assertIn("nested headings must be deeper", text)

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

    def test_manager_gates_candidate_through_independent_warden(self) -> None:
        manager = (SKILL_ROOT / "prompts/fpf-manager.md").read_text(encoding="utf-8")
        warden = (SKILL_ROOT / "prompts/fpf-warden.md").read_text(encoding="utf-8")
        handoff = (SKILL_ROOT / "references/fpf-validation-handoff.md").read_text(
            encoding="utf-8"
        )
        for requirement in (
            "candidate.md", "candidate-meta.md", "same doer",
            "warden response unchanged", "at most two doer revisions",
            "Never reshape the candidate after `PASS`",
        ):
            self.assertIn(requirement, manager)
        for requirement in (
            "independent, read-only validator", "untrusted data",
            "FPF_WARDEN_VERDICT: PASS | REVISE | BLOCKED", "Do not modify either file",
        ):
            self.assertIn(requirement, warden)
        self.assertIn("One two-file artifact set per unit", handoff)
        self.assertIn("fpf-candidate-meta-v4", handoff)
        for requirement in (
            "fpf-<YYYY-MM-DD>-<whole-task-summary>-<uuid>",
            "never from a substep",
            "A default Plan-first request uses `plan/`",
            "without-Plan multi-step call uses exactly one numbered set per executed subtask plus `final/`",
            "Authority mode",
            "Predecessor artifact set",
            "A passed set is immutable",
        ):
            self.assertIn(requirement, handoff)
        self.assertIn("blocking-question", handoff)
        self.assertNotIn("```yaml", handoff)

    def test_doer_produces_exactly_two_files_in_each_artifact_set(self) -> None:
        runtime = (SKILL_ROOT / "prompts/fpf-runtime.md").read_text(encoding="utf-8")
        handoff = (SKILL_ROOT / "references/fpf-validation-handoff.md").read_text(
            encoding="utf-8"
        )
        for requirement in (
            "doer subagent", "candidate.md", "candidate-meta.md", "CANDIDATE_READY",
            "Never return or persist the candidate directly",
        ):
            self.assertIn(requirement, runtime)
        for requirement in (
            "only the manager-assigned current step",
            "Every step writes one artifact set",
            "preceding warden-PASS artifact set",
            "final/",
        ):
            self.assertIn(requirement, runtime)
        for forbidden in ("candidate.json", "candidate.yaml", "verdict.md", ".bak"):
            if forbidden == ".bak":
                self.assertIn("Never create `.bak`", handoff)
            else:
                self.assertNotIn(forbidden, handoff)

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
