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
        self.assertLessEqual(len(cases), 12)
        self.assertEqual({"general", "framework", "software", "skills"}, {case["area"] for case in cases})
        self.assertEqual(
            {"help", "plan", "analysis"},
            {case["output_contract"] for case in cases},
        )
        case_ids = {case["id"] for case in cases}
        for required in (
            "plan-typo-correction-no-execution", "ambiguous-substring-safe-fallback",
            "literal-plus-single-analysis", "russian-design-challenge-analysis",
            "composition-stops-with-typed-handoff", "plain-persistence-readonly-stop",
        ):
            self.assertIn(required, case_ids)

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
        self.assertEqual(5, len(identity["assets"]))
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
            ):
                result = run_codex(
                    "prompt", root / "schema.json", output, root,
                    executable="codex", model=None, timeout=30,
                )

            self.assertEqual({"result": "ok"}, result)
            self.assertEqual(["/opt/codex", "-a", "never", "exec"], captured[:4])
            for required in ("--ephemeral", "--ignore-user-config", "--ignore-rules", "read-only", "--output-schema"):
                self.assertIn(required, captured)


if __name__ == "__main__":
    unittest.main()
