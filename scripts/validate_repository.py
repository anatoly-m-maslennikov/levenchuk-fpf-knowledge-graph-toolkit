#!/usr/bin/env python3
"""Validate the portable FPF projection and bundled skill packages."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "FPF-Knowledge-Graph"
REPORT_PATH = GRAPH / "00_Index" / "FPF - Validation Report.json"
README_PATH = ROOT / "Readme.md"
CI_PATH = ROOT / ".github" / "workflows" / "ci.yml"
SKILLS = ROOT / "skills"
ROUTING_SCENARIOS_PATH = SKILLS / "fpf-route.skill" / "references" / "routing-scenarios.json"
EXPECTED_SKILL_PACKAGES = {
    "fpf-alignment-audit.skill",
    "fpf-applicability-scan.skill",
    "fpf-decision-synthesize.skill",
    "fpf-design-challenge.skill",
    "fpf-options-explore.skill",
    "fpf-quality-improve.skill",
    "fpf-route.skill",
    "fpf-sota-harvest.skill",
}
ROUTABLE_SKILL_PACKAGES = EXPECTED_SKILL_PACKAGES - {"fpf-route.skill"}
FULL_REPORT_CONTRACT = (
    "Return the complete listed artifact with every required section and evidence record, "
    "including any optional delegated work. Do not replace it with a summary, abbreviated "
    "surrogate, or pointer to another result."
)
RESULT_ENVELOPE_HEADINGS = (
    "`## Task, scope, and boundaries`",
    "`## High-confidence results (>=95%)`",
    "`## Open questions (confidence <95%)`",
    "`## Skills used`",
)
RESULT_ENVELOPE_CONTRACT = (
    "Organize the complete native artifact under exactly these four top-level Markdown headings, in this order:",
    "list every skill actually executed for this result in execution order",
    "merely proposed or recommended downstream skills as used",
    "Assign confidence to each material result and state its evidence basis.",
    "**90–94%:** probable answer, but confirmation is still needed.",
    "**Below 90%:** materially uncertain.",
    "Never round up to 95%",
    "None identified within the declared scope",
    "Preserve these native artifact requirements:",
)
SOURCE_TRACE_CONTRACT = (
    "Immediately after the skill list in section 4, add this compact source disclosure:",
    "<details>",
    "<summary>FPF sources consulted (",
    "List every FPF source document actually opened exactly once.",
    "**Used** means it materially supports a result; **screened only** means it was read but not relied on.",
    "absolute machine paths",
    "use a stable URI or item identifier",
    "If the renderer does not support `<details>`",
)
EXPECTED_NATIVE_OUTPUT_COUNTS = {
    "fpf-alignment-audit": 7,
    "fpf-applicability-scan": 5,
    "fpf-decision-synthesize": 6,
    "fpf-design-challenge": 5,
    "fpf-options-explore": 6,
    "fpf-quality-improve": 6,
    "fpf-route": 6,
    "fpf-sota-harvest": 6,
}


FORBIDDEN_PORTABILITY_PATTERNS = (
    r"\bcod" + r"ex\b",
    r"\bopen" + r"ai\b",
    r"\bcla" + r"ude\b",
    r"\bgr" + r"ok\b",
    r"\bopen" + r"code\b",
    r"\binter" + r"rupt_agent\b",
    r"\bsubagent " + r"lifecycle\b",
    r"\broot-side " + r"polling\b",
    r"agents/open" + r"ai\.yaml",
    r"\.cod" + r"ex/",
    r"\.cla" + r"ude/",
    r"\.gr" + r"ok/",
    r"\$fpf" + r"-",
    r"\bparallel " + r"calls\b",
    r"\bparallel " + r"joins\b",
)


def main() -> int:
    errors: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    require(not (ROOT / "FPF-Spec.md").exists(), "root FPF-Spec.md must remain absent")
    require(not (ROOT / "FPF-Spec").exists(), "legacy FPF-Spec graph directory must remain absent")
    require(not (ROOT / "FPF-Spec-original").exists(), "the monolithic source must not be bundled")

    try:
        report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read validation report: {exc}")
        report = {}

    markdown_files = sorted(GRAPH.rglob("*.md"))
    require(report.get("source") == "FPF-Spec.md", "report source must be portable")
    require(report.get("out_dir") == "FPF-Knowledge-Graph", "report output path must be portable")
    for key in ("source_revision", "source_sha256", "generated_on"):
        require(isinstance(report.get(key), str) and bool(report[key]), f"report missing {key}")
    require(re.fullmatch(r"[0-9a-f]{64}", report.get("source_sha256", "")) is not None, "report source SHA-256 is invalid")
    require(report.get("broken_links_count") == 0, "generated graph contains broken wiki-links")
    require(report.get("markdown_files") == len(markdown_files), "report Markdown count does not match disk")

    fpf_ids: list[str] = []
    for path in markdown_files:
        text = path.read_text(encoding="utf-8", errors="replace")
        require(text.startswith("---\n"), f"missing frontmatter: {path.relative_to(ROOT)}")
        require("[[[" not in text, f"malformed triple-bracket link: {path.relative_to(ROOT)}")
        for key in ("source_revision", "source_sha256", "generated_on"):
            match = re.search(rf'^{key}: "([^"\n]+)"$', text, re.MULTILINE)
            require(match is not None and match.group(1) == report.get(key), f"generated provenance mismatch: {path.relative_to(ROOT)} ({key})")
        match = re.search(r'^fpf_id: "([^"]+)"', text, re.MULTILINE)
        if match:
            fpf_ids.append(match.group(1))

    require(report.get("ids") == len(fpf_ids), "report FPF ID count does not match generated pages")
    require(len(fpf_ids) == len(set(fpf_ids)), "generated FPF IDs are not unique")

    readme = README_PATH.read_text(encoding="utf-8")
    for raw_target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", readme):
        if raw_target.startswith(("http://", "https://", "#")):
            continue
        target = unquote(raw_target).split("#", 1)[0]
        require((ROOT / target).exists(), f"README link does not exist: {raw_target}")

    ci_text = CI_PATH.read_text(encoding="utf-8")
    push_block = re.search(r"(?ms)^  push:\n(?P<body>.*?)(?=^  pull_request:)", ci_text)
    pull_request_block = re.search(r"(?ms)^  pull_request:\n(?P<body>.*?)(?=^  workflow_dispatch:)", ci_text)
    require(push_block is not None, "CI is missing its push trigger")
    require(pull_request_block is not None, "CI is missing its pull-request trigger")
    if push_block:
        push_branches = set(re.findall(r"^      - (\S+)$", push_block.group("body"), re.MULTILINE))
        require(push_branches == {"dev", "main"}, "CI push branches must be exactly dev and main")
    if pull_request_block:
        pull_request_branches = set(
            re.findall(r"^      - (\S+)$", pull_request_block.group("body"), re.MULTILINE)
        )
        require(pull_request_branches == {"main"}, "CI pull-request base must be exactly main")
    require("am/dev" not in ci_text, "CI must not reference retired am/dev")
    for condition in (
        "github.event.pull_request.user.login == 'anatoly-m-maslennikov'",
        "github.event.pull_request.head.repo.full_name == github.repository",
        "github.event.pull_request.head.ref == 'dev'",
        "github.event.pull_request.base.ref == 'main'",
        "!github.event.pull_request.draft",
    ):
        require(condition in ci_text, f"CI owner auto-merge condition missing: {condition}")

    skill_paths = sorted(SKILLS.glob("*.skill/SKILL.md"))
    actual_skill_packages = {path.parent.name for path in skill_paths}
    require(
        actual_skill_packages == EXPECTED_SKILL_PACKAGES,
        "FPF skill package set does not match the expected catalog",
    )
    route_text = (SKILLS / "fpf-route.skill" / "SKILL.md").read_text(encoding="utf-8")
    route_entries = re.findall(r"^\| `([^`]+)` \|", route_text, re.MULTILINE)
    route_catalog = set(route_entries)
    require(route_catalog == {name.removesuffix(".skill") for name in ROUTABLE_SKILL_PACKAGES}, "fpf-route catalog must contain exactly the seven executable packages")
    require(len(route_entries) == len(route_catalog), "fpf-route catalog must not contain duplicate skill rows")
    require("fpf-route" not in route_catalog, "fpf-route must not route recursively")

    try:
        routing_fixture = json.loads(ROUTING_SCENARIOS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read routing scenarios: {exc}")
        routing_fixture = {}
    scenarios = routing_fixture.get("scenarios", [])
    require(routing_fixture.get("schema_version") == 1, "routing scenario schema version must be 1")
    require(isinstance(scenarios, list) and bool(scenarios), "routing scenarios must be a non-empty list")
    scenario_ids: list[str] = []
    covered_routable_skills: set[str] = set()
    allowed_target_states = {
        "open question",
        "research need",
        "proposal",
        "evaluated alternatives",
        "versioned improvement target",
        "implemented or accepted work",
    }
    routable_names = {name.removesuffix(".skill") for name in ROUTABLE_SKILL_PACKAGES}
    if isinstance(scenarios, list):
        for index, scenario in enumerate(scenarios):
            label = f"routing scenario #{index + 1}"
            require(isinstance(scenario, dict), f"{label} must be an object")
            if not isinstance(scenario, dict):
                continue
            scenario_id = scenario.get("id")
            require(isinstance(scenario_id, str) and bool(scenario_id), f"{label} missing id")
            if isinstance(scenario_id, str):
                scenario_ids.append(scenario_id)
                label = f"routing scenario {scenario_id}"
            require(isinstance(scenario.get("question"), str) and bool(scenario["question"].strip()), f"{label} missing question")
            require(scenario.get("target_state") in allowed_target_states, f"{label} has invalid target state")
            sequence = scenario.get("expected_sequence")
            require(isinstance(sequence, list) and bool(sequence), f"{label} must have a non-empty expected sequence")
            if isinstance(sequence, list):
                invalid = set(sequence) - routable_names
                require(not invalid, f"{label} references unroutable skills: {sorted(invalid)}")
                require(len(sequence) == len(set(sequence)), f"{label} must not repeat a skill")
                covered_routable_skills.update(set(sequence) & routable_names)
            require(
                isinstance(scenario.get("stop_condition"), str) and bool(scenario["stop_condition"].strip()),
                f"{label} missing stop condition",
            )
    require(len(scenario_ids) == len(set(scenario_ids)), "routing scenario IDs must be unique")
    require(covered_routable_skills == routable_names, "routing scenarios must cover every executable FPF skill")

    skills_readme = (SKILLS / "README.md").read_text(encoding="utf-8")
    for package_name in sorted(EXPECTED_SKILL_PACKAGES):
        require(f"`{package_name}`" in skills_readme, f"skill catalog omits {package_name}")
    for portability_path in (SKILLS / "README.md", README_PATH):
        portability_text = portability_path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_PORTABILITY_PATTERNS:
            require(
                re.search(pattern, portability_text, re.IGNORECASE) is None,
                f"runtime-specific portability term in {portability_path.relative_to(ROOT)}: {pattern}",
            )
    for skill_path in skill_paths:
        package = skill_path.parent
        expected_name = package.name.removesuffix(".skill")
        skill_text = skill_path.read_text(encoding="utf-8")
        frontmatter = re.match(r"\A---\n(.*?)\n---\n", skill_text, re.DOTALL)
        require(frontmatter is not None, f"missing skill frontmatter: {skill_path.relative_to(ROOT)}")
        if frontmatter:
            name = re.search(r"^name:\s*(\S+)\s*$", frontmatter.group(1), re.MULTILINE)
            description = re.search(r"^description:\s*(.+)$", frontmatter.group(1), re.MULTILINE)
            require(name is not None and name.group(1) == expected_name, f"skill name mismatch: {expected_name}")
            require(description is not None and bool(description.group(1).strip()), f"missing skill description: {expected_name}")

        for pattern in FORBIDDEN_PORTABILITY_PATTERNS:
            require(re.search(pattern, skill_text, re.IGNORECASE) is None, f"runtime-specific portability term in {expected_name}: {pattern}")
        require(not (package / "agents").exists(), f"provider-specific metadata directory present: {expected_name}")
        require(not any(package.rglob("*.yaml")), f"provider-specific metadata file present: {expected_name}")

        references = set(re.findall(r"(?<![\w-])\$?(fpf-[a-z][a-z-]*)(?![\w-])", skill_text))
        installed_names = {name.removesuffix(".skill") for name in EXPECTED_SKILL_PACKAGES}
        require(references <= installed_names, f"unresolved FPF skill reference in {expected_name}: {sorted(references - installed_names)}")
        require(FULL_REPORT_CONTRACT in skill_text, f"missing full-report delivery contract: {expected_name}")
        heading_positions = [skill_text.find(heading) for heading in RESULT_ENVELOPE_HEADINGS]
        require(all(position >= 0 for position in heading_positions), f"missing four-section result envelope: {expected_name}")
        require(heading_positions == sorted(heading_positions), f"result envelope headings out of order: {expected_name}")
        for contract_text in RESULT_ENVELOPE_CONTRACT:
            require(contract_text in skill_text, f"missing result-envelope contract in {expected_name}: {contract_text}")
        if expected_name != "fpf-route":
            for contract_text in SOURCE_TRACE_CONTRACT:
                require(contract_text in skill_text, f"missing FPF source-trace contract in {expected_name}: {contract_text}")
        require("</details>" in skill_text, f"missing FPF source-trace disclosure close in {expected_name}")
        native_marker = "Preserve these native artifact requirements:"
        native_block = skill_text.split(native_marker, 1)[1] if native_marker in skill_text else ""
        native_items = re.findall(r"^\d+\. \*\*", native_block, re.MULTILINE)
        require(
            len(native_items) == EXPECTED_NATIVE_OUTPUT_COUNTS[expected_name],
            f"native output requirement count changed: {expected_name}",
        )
        if "Produce a read-only" in skill_text:
            require("Remain read-only unless" in skill_text or expected_name == "fpf-route", f"missing read-only boundary: {expected_name}")
        if expected_name == "fpf-route":
            require("Execution boundary" in skill_text, "fpf-route missing execution boundary")
            require(
                "<summary>Routing basis and FPF methodology sources</summary>" in skill_text,
                "fpf-route must disclose its routing basis and methodology-source exception",
            )
            require(
                "Do not present an empty or zero-count FPF source trace" in skill_text,
                "fpf-route must prohibit misleading zero-count methodology traces",
            )
            require(
                "Use ordinary Markdown headings and lists. Do not wrap the artifact or any section in a fenced code block."
                in skill_text,
                "fpf-route missing ordinary-Markdown output contract",
            )
        if expected_name == "fpf-decision-synthesize":
            require("only when the user authorizes it" in skill_text, "decision synthesis missing write authority boundary")
        if expected_name == "fpf-quality-improve":
            require("Apply changes only when authorized." in skill_text, "quality improvement missing change authority boundary")

    help_result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_fpf_obsidian_graph.py"), "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    require(help_result.returncode == 0 and "--source SOURCE" in help_result.stdout, "generator must require --source")
    require("--source-revision SOURCE_REVISION" in help_result.stdout, "generator must require --source-revision")
    require("--generated-on GENERATED_ON" in help_result.stdout, "generator must require --generated-on")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        json.dumps(
            {
                "markdown_files": len(markdown_files),
                "fpf_ids": len(fpf_ids),
                "broken_links": report.get("broken_links_count"),
                "skill_packages": len(skill_paths),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
