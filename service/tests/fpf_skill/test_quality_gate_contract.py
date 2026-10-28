import copy
import json
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

from service.scripts.filesystem_policy import temporary_workspace
from service.scripts.validate_repository.validate_repository_workers.fpf_markdown import (
    load_markdown_graph,
)
from service.scripts.fpf_skill_quality_gate.fpf_skill_quality_gate_workers.cases import (
    gate_identity,
    load_cases,
    load_profile_cases,
)
from service.scripts.fpf_skill_quality_gate.fpf_skill_quality_gate_workers.evidence import (
    build_evidence,
    check_evidence,
    validate_evaluation,
    write_json,
)
from service.scripts.fpf_skill_quality_gate.fpf_skill_quality_gate_workers.codex_runner import (
    run_codex,
)


ROOT = Path(__file__).resolve().parents[3]
ASSETS = ROOT / "service/scripts/fpf_skill_quality_gate/fpf_skill_quality_gate_assets"


def passing_evaluation(cases: list[dict[str, object]]) -> dict[str, object]:
    return {
        "verdict": "PASS", "weaknesses": [], "consolidated_fixes": [],
        "case_results": [
            {
                "case_id": case["id"], "verdict": "PASS",
                "criteria": [
                    {"criterion_id": criterion["id"], "verdict": "PASS", "evidence": "x"}
                    for criterion in case["criteria"]
                ],
            }
            for case in cases
        ],
        "output_contract_checks": [
            {
                "case_id": case["id"],
                "output_contract": case["output_contract"],
                "verdict": "PASS",
                "evidence": "x",
            }
            for case in cases
        ],
    }


class QualityGateContractTests(unittest.TestCase):
    def test_case_pack_is_bounded_and_covers_all_three_areas(self) -> None:
        cases = load_cases(ASSETS / "cases.json")
        self.assertGreaterEqual(len(cases), 10)
        self.assertLessEqual(len(cases), 15)
        self.assertEqual({"general", "framework", "software", "skills"}, {case["area"] for case in cases})
        self.assertEqual(
            {"help", "plan", "analysis"},
            {case["output_contract"] for case in cases},
        )
        case_ids = {case["id"] for case in cases}
        for required in (
            "plan-typo-correction-no-execution", "approved-plan-do-continuation",
            "ambiguous-substring-safe-fallback",
            "literal-plus-single-analysis", "russian-design-challenge-analysis",
            "composition-stops-with-typed-handoff", "plain-persistence-readonly-stop",
            "sota-harvest-fixture-analysis", "evaluation-design-direct-analysis",
            "decision-synthesize-direct-analysis",
        ):
            self.assertIn(required, case_ids)
        continuation = next(case for case in cases if case["id"] == "approved-plan-do-continuation")
        default_plan = next(case for case in cases if case["id"] == "plan-composed-research")
        self.assertNotIn("$fpf plan ", default_plan["invocation"])
        self.assertIn("sota harvest + design challenge + quality improve", default_plan["invocation"])
        for case in cases:
            if case["output_contract"] == "analysis" and case["id"] != "approved-plan-do-continuation":
                invocation = str(case["invocation"]).casefold()
                self.assertTrue(
                    "without a plan" in invocation or "без плана" in invocation,
                    case["id"],
                )
        self.assertEqual("do", continuation["invocation"])
        self.assertEqual("PASS", continuation["prior_validated_plan"]["warden_verdict"])
        self.assertEqual(90, continuation["prior_validated_plan"]["decision_threshold_percent"])
        self.assertIn(
            "Reply `do` to execute this plan.",
            continuation["prior_validated_plan"]["plan_markdown"],
        )
        self.assertIn(
            "blocking threshold: 90% (operator override)",
            continuation["prior_validated_plan"]["plan_markdown"],
        )

    def test_release_pack_executes_every_analytical_command(self) -> None:
        cases = {case["id"]: case for case in load_cases(ASSETS / "cases.json")}
        coverage = {
            "problem-frame": ("literal-plus-single-analysis", "$fpf problem frame"),
            "structure-recover": ("approved-plan-do-continuation", "$fpf structure recover"),
            "applicability-scan": ("framework-skill-analysis", "$fpf applicability scan"),
            "sota-harvest": ("sota-harvest-fixture-analysis", "$fpf sota harvest"),
            "options-explore": ("framework-skill-analysis", "+ options explore"),
            "evaluation-design": ("evaluation-design-direct-analysis", "$fpf evaluation design"),
            "design-challenge": ("russian-design-challenge-analysis", "$fpf проверка дизайна"),
            "decision-synthesize": ("decision-synthesize-direct-analysis", "$fpf decision synthesize"),
            "quality-improve": ("software-review-convergence", "+ quality improve"),
            "alignment-audit": ("software-review-convergence", "+ alignment audit"),
        }
        graph = load_markdown_graph(ROOT)
        analytical_ids = {
            str(node["id"])
            for node in graph["nodes"]
            if str(node["id"]) not in {"help", "plan"}
        }
        self.assertEqual(analytical_ids, set(coverage))
        for command_id, (case_id, marker) in coverage.items():
            case = cases[case_id]
            self.assertEqual("analysis", case["output_contract"], command_id)
            source = str(case["invocation"])
            prior_plan = case.get("prior_validated_plan")
            if isinstance(prior_plan, dict):
                source += "\n" + str(prior_plan.get("plan_markdown", ""))
            self.assertIn(marker, source, command_id)

        fixture = ASSETS / "sota-evidence-fixture.md"
        self.assertTrue(fixture.is_file())
        self.assertIn(
            fixture.relative_to(ROOT).as_posix(),
            str(cases["sota-harvest-fixture-analysis"]["invocation"]),
        )

    def test_exact_complete_pass_is_accepted(self) -> None:
        cases = load_cases(ASSETS / "cases.json")
        self.assertEqual([], validate_evaluation(passing_evaluation(cases), cases))

    def test_missing_or_failed_criterion_fails_without_averaging(self) -> None:
        cases = load_cases(ASSETS / "cases.json")
        evaluation = copy.deepcopy(passing_evaluation(cases))
        evaluation["case_results"][0]["criteria"].pop()
        evaluation["case_results"][1]["criteria"][0]["verdict"] = "FAIL"
        self.assertGreaterEqual(len(validate_evaluation(evaluation, cases)), 2)

    def test_duplicate_extra_and_malformed_results_fail_closed(self) -> None:
        cases = load_cases(ASSETS / "cases.json")
        evaluation = copy.deepcopy(passing_evaluation(cases))
        evaluation["case_results"][1] = copy.deepcopy(evaluation["case_results"][0])
        evaluation["case_results"][0]["criteria"].append(
            {"criterion_id": "unexpected", "verdict": "PASS", "evidence": "x"}
        )
        evaluation["output_contract_checks"][1] = "malformed"
        failures = validate_evaluation(evaluation, cases)
        self.assertTrue(any("case ids" in item for item in failures))
        self.assertTrue(any("exactly once" in item for item in failures))
        self.assertTrue(any("must be an object" in item for item in failures))

    def test_blank_evidence_and_contradictory_pass_fail_closed(self) -> None:
        cases = load_cases(ASSETS / "cases.json")
        evaluation = copy.deepcopy(passing_evaluation(cases))
        evaluation["case_results"][0]["criteria"][0]["evidence"] = "  "
        evaluation["case_results"][0]["criteria"][1]["verdict"] = "FAIL"
        evaluation["output_contract_checks"][0]["evidence"] = ""
        failures = validate_evaluation(evaluation, cases)
        self.assertTrue(any("criterion evidence is blank" in item for item in failures))
        self.assertTrue(any("PASS contradicts" in item for item in failures))
        self.assertTrue(any("output-contract evidence is blank" in item for item in failures))

    def test_pass_cannot_hide_reported_weaknesses_or_fixes(self) -> None:
        cases = load_cases(ASSETS / "cases.json")
        evaluation = passing_evaluation(cases)
        evaluation["weaknesses"] = ["hidden weakness"]
        evaluation["consolidated_fixes"] = ["required fix"]
        self.assertEqual(2, len(validate_evaluation(evaluation, cases)))

    def test_output_contract_checks_are_complete_and_bound_to_each_case(self) -> None:
        cases = load_cases(ASSETS / "cases.json")
        evaluation = passing_evaluation(cases)
        evaluation["output_contract_checks"][0]["output_contract"] = "analysis"
        evaluation["output_contract_checks"].pop()
        failures = validate_evaluation(evaluation, cases)
        self.assertTrue(any("output-contract" in item for item in failures))

    def test_identity_binds_skill_and_every_eval_asset(self) -> None:
        identity = gate_identity(ROOT, ASSETS)
        self.assertEqual(6, len(identity["assets"]))
        self.assertIn("sota-evidence-fixture.md", identity["assets"])
        self.assertEqual(64, len(identity["skill_tree_sha256"]))

    def test_full_pack_derives_one_live_case_per_profile(self) -> None:
        cases = load_profile_cases(ROOT)
        self.assertEqual(len(load_markdown_graph(ROOT)["task_profiles"]), len(cases))
        self.assertEqual(len(cases), len({case["id"] for case in cases}))
        self.assertEqual({"framework", "software", "skills"}, {case["area"] for case in cases})
        self.assertTrue(all(case["output_contract"] == "analysis" for case in cases))

    def test_pass_evidence_is_bound_to_exact_case_pack(self) -> None:
        with temporary_workspace(prefix="fpf-evidence-pack-") as temporary:
            root = Path(temporary)
            path = root / "evidence.json"
            identity = {"skill_tree_sha256": "x", "assets": {}}
            value = build_evidence(identity, {}, {}, root, "test", ["case-a"], "release")
            write_json(path, value)
            self.assertEqual([], check_evidence(path, identity, ["case-a"], "release"))
            failures = check_evidence(path, identity, ["case-b"], "full-profiles")
            self.assertIn("quality-gate evidence is for a different case pack", failures)

    def test_ci_contains_no_live_quality_gate(self) -> None:
        ci = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertNotIn("fpf_skill_quality_gate", ci)
        self.assertNotIn("codex exec", ci)

    def test_subject_and_evaluator_define_metadata_boundaries(self) -> None:
        subject = (ASSETS / "subject-prompt.md").read_text(encoding="utf-8")
        evaluator = (ASSETS / "evaluator-prompt.md").read_text(encoding="utf-8")
        schema = json.loads((ASSETS / "subject-output.schema.json").read_text(encoding="utf-8"))
        for text in (subject, evaluator):
            self.assertIn("commands_executed", text)
            self.assertIn("methodology_sources_used", text)
            self.assertIn("Help", text)
            self.assertIn("Plan", text)
        self.assertIn('Plan uses only `["$fpf plan"]`', subject)
        self.assertIn("stopped before native execution", subject)
        self.assertIn("not methodology sources", subject)
        self.assertIn("manager-doer-warden", subject)
        self.assertIn("Every new non-Help invocation is Plan-first", subject)
        self.assertIn("explicit without-Plan instruction", subject)
        self.assertIn("candidate-meta.md", subject)
        self.assertIn("fpf-YYYY-MM-DD-<whole-task-summary>-<uuid>", subject)
        self.assertIn("one numbered step set per actually executed canonical command", subject)
        self.assertIn("warden_verdict = PASS", evaluator)
        self.assertIn("prior_validated_plan", subject)
        self.assertIn("same_doer_resumed = true", evaluator)
        for gate in (
            "No errors", "Full workflow worked", "All required artifacts were created",
            "Artifacts have the correct structure", "The result is aligned to the task",
        ):
            self.assertIn(gate, evaluator)
        self.assertIn("structured subject result is the evaluation boundary", evaluator)
        self.assertIn("Do not require `candidate.md`, `candidate-meta.md`, a warden envelope", evaluator)
        self.assertIn("Do not invent another provenance", evaluator)
        orchestration = schema["properties"]["orchestration"]
        self.assertIn("artifact_sets", orchestration["properties"])
        self.assertNotIn("temporary_files", orchestration["properties"])
        self.assertIn("run_directory_leaf", orchestration["required"])
        self.assertIn("whole_task_summary", orchestration["required"])
        files = orchestration["properties"]["artifact_sets"]["items"]["properties"]["files"]
        self.assertEqual(2, files["minItems"])
        self.assertEqual(2, files["maxItems"])
        self.assertEqual("string", files["prefixItems"][0]["type"])
        self.assertEqual("string", files["prefixItems"][1]["type"])
        self.assertEqual("candidate.md", files["prefixItems"][0]["const"])
        self.assertEqual("candidate-meta.md", files["prefixItems"][1]["const"])

    def test_subject_runner_allows_only_managed_temporary_transport(self) -> None:
        cli = (
            ROOT / "service/scripts/fpf_skill_quality_gate/fpf_skill_quality_gate_workers/cli.py"
        ).read_text(encoding="utf-8")
        self.assertIn('sandbox="workspace-write"', cli)
        self.assertIn("Path(tempfile.gettempdir())", cli)

    def test_evaluator_keeps_compact_plan_and_flexible_analysis_depth(self) -> None:
        evaluator = (ASSETS / "evaluator-prompt.md").read_text(encoding="utf-8")
        self.assertIn("exactly one top-level `Proposed plan` heading", evaluator)
        self.assertEqual(1, evaluator.count("Accept Markdown `#` or `##`"))
        self.assertEqual(1, evaluator.count("never fail only because one of those two depths"))


class CodexRunnerContractTests(unittest.TestCase):
    def test_runner_is_ephemeral_read_only_structured_and_noninteractive(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary)
            output = root / ".runtime/result.json"
            captured: list[str] = []

            def complete(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
                captured.extend(command)
                output.write_text(json.dumps({"result": "ok"}), encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, "", "")

            with patch("shutil.which", return_value="/opt/codex"), patch(
                "subprocess.run", side_effect=complete,
            ), patch.dict("os.environ", {"CODEX_HOME": str(root / "source-home")}):
                (root / "source-home").mkdir()
                (root / "source-home/auth.json").write_text("{}", encoding="utf-8")
                result = run_codex(
                    "prompt", root / "schema.json", output, root,
                    executable="codex", model=None, timeout=30,
                    state_home=root / ".runtime/codex-home",
                )

            self.assertEqual({"result": "ok"}, result)
            self.assertEqual(["/opt/codex", "-a", "never", "exec"], captured[:4])
            for required in ("--ephemeral", "--ignore-user-config", "--ignore-rules", "read-only", "--output-schema"):
                self.assertIn(required, captured)
            auth_link = root / ".runtime/codex-home/auth.json"
            self.assertTrue(auth_link.is_symlink())
            self.assertEqual((root / "source-home/auth.json").resolve(), auth_link.resolve())

    def test_runner_can_grant_only_the_system_temporary_root_to_subjects(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary)
            output = root / ".runtime/result.json"
            captured: list[str] = []

            def complete(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
                captured.extend(command)
                output.write_text(json.dumps({"result": "ok"}), encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, "", "")

            temporary_root = root / "system-temp"
            temporary_root.mkdir()
            with patch("shutil.which", return_value="/opt/codex"), patch(
                "subprocess.run", side_effect=complete,
            ), patch.dict("os.environ", {"CODEX_HOME": str(root / "source-home")}):
                (root / "source-home").mkdir()
                (root / "source-home/auth.json").write_text("{}", encoding="utf-8")
                run_codex(
                    "prompt", root / "schema.json", output, root,
                    executable="codex", model=None, timeout=30,
                    state_home=root / ".runtime/codex-home",
                    sandbox="workspace-write",
                    additional_writable_dirs=(temporary_root,),
                )

            self.assertIn("workspace-write", captured)
            self.assertIn("--add-dir", captured)
            self.assertIn(str(temporary_root), captured)


if __name__ == "__main__":
    unittest.main()
