---
name: graph-fpf-evaluate-conversion-result
description: Evaluate one generated FPF knowledge-graph conversion result against its bounded eval pack, canonical source slices, previous graph, and deterministic-test evidence. Use after graph-fpf-convert-from-original produces a candidate graph, or when the user asks whether an FPF graph conversion result is faithful, navigable, regression-safe, and ready to accept. Do not use for converting the graph or reviewing FPF methodology claims.
---

# Graph FPF Evaluate Conversion Result

Produce an input-read-only **FPF Graph Conversion Evaluation**. Judge the generated projection and its converter evidence; do not mutate the graph, converter, staged source, backup, tests, or settings. The sole permitted write is the revision-bound PASS evidence described below.

This is a project-service evaluator for `graph-fpf-convert-from-original`, not an `$fpf` methodology prompt. A passing evaluation supports acceptance of one conversion result only. It does not establish that FPF itself is correct, complete, or suitable for another project.

## Resolve the evaluation subject

Locate one toolkit checkout containing:

- `FPF-Knowledge-Graph/` and `FPF-Knowledge-Graph.bak/`;
- `scripts/graph_fpf_convert_from_original/prepare_eval.py`;
- `scripts/graph_fpf_convert_from_original/run_tests.py`;
- `scripts/validate_fpf_graph/`;
- `.runtime/original-fpf-sources/FPF-Spec.md` in the staged, manifest-verified patched package.

Prefer the active workspace and bounded accessible project roots. Do not assume a user name, home directory, operating system, or repository parent.

Use a caller-supplied current eval pack when its revision and graph paths match the current candidate. Otherwise run `<python> -X pycache_prefix=.runtime/pycache -m scripts.graph_fpf_convert_from_original.prepare_eval` from the toolkit root and capture its JSON result. Do not write an ad hoc replacement pack.

Require deterministic-suite evidence for the same current graph revision. If it is missing or stale, run `<python> -X pycache_prefix=.runtime/pycache -m scripts.graph_fpf_convert_from_original.run_tests`. A deterministic failure is evidence, not permission to repair; return it to the converter.

## Apply the complete evaluation profile

Load `references/evaluation-profile.md` completely before evaluating. It defines the mandatory issue families, historical regression probes, exhaustive mechanical coverage, bounded semantic coverage, syntax-risk strata, and finding classes. Do not replace it with a generic graph review.

Run all fourteen issue families with exhaustive whole-tree checks for every mechanically decidable invariant in the profile. Separately build a bounded semantic set from `selected_eval_targets`. Preserve deterministic ordering and include:

- one representative for every present top-level FPF ID family;
- every selected added, moved, or retitled target;
- both current and backup carriers when the pack supplies both paths;
- every removed ID in the delta-accountability case, without inventing a current carrier.

Add one carrier from every populated syntax-risk stratum in the profile. If the supplied target set is too large for bounded inspection, retain every top-level family and risk stratum, then choose first, middle, and last targets within each change kind. Report the exact selection rule, selected count, and omitted count. A sample supports only bounded semantic fidelity; it does not reduce exhaustive mechanical coverage.

For source comparison, open only the effective staged source ranges named by selected generated carriers, plus the minimum adjacent heading context needed to interpret them. Use the colocated patch and metadata when a selected range differs from upstream. Never load the monolithic source wholesale.

## Run the evaluation cases

Evaluate all fourteen required issue families in `references/evaluation-profile.md` separately with exact file, FPF ID, source-range, report-field, raw-tree scan, or command evidence. Exercise every historical regression probe and every populated syntax-risk stratum. A passing generic validator does not waive a missing probe.

For every case return `PASS`, `FAIL`, or `INSUFFICIENT EVIDENCE`. Classify each non-pass item as exactly one of: `converter defect`, `deterministic-test defect`, `eval-pack defect`, `repository-integration defect`, `upstream-source condition`, or `unavailable evidence`.

## Determine the verdict

- `PASS` only when all fourteen conversion-result issue families pass, every historical regression probe is exercised, exhaustive mechanical checks cover the entire tree, the bounded semantic set covers every populated risk stratum, the deterministic suite passes for the same revision, and no converter, test, eval-pack, or integration defect remains. Faithfully exposed upstream-source conditions do not by themselves block conversion acceptance; report them separately and do not translate PASS into a claim that the upstream FPF source is internally complete.
- `FAIL` when evidence demonstrates any converter, deterministic-test, eval-pack, or repository-integration defect.
- `UPSTREAM CONDITION` when a canonical-source condition prevents a faithful complete projection or makes required conversion evidence indeterminate even though no tooling repair can resolve it. Do not use this verdict merely because a faithfully projected source contains an exposed dangling, planned, legacy, or otherwise defective source claim.
- `INSUFFICIENT EVIDENCE` when required current/backup carriers, source ranges, revisions, test evidence, or permissions are unavailable.

Do not average case results, hide a failed case behind a high aggregate score, or downgrade a semantic-fidelity defect because mechanical tests pass.

## Handoff

For every tooling defect, provide a stable finding ID, affected FPF IDs and paths, failure predicate, expected evidence, actual evidence, minimal reproduction, and the converter or test boundary that owns repair. Tell `graph-fpf-convert-from-original` to restart from conversion after an authorized repair; do not perform the repair in this skill.

For every upstream-source condition, including one reported alongside PASS, cite the bounded upstream/effective source range as applicable, state its effect separately from conversion quality, and explain why generated output is faithful. Never patch generated notes to conceal the condition, invent missing content, or modify the external source repository. Treat an explicit repository-owned source patch as part of the evaluated effective source, with its provenance verified separately.

For `PASS` only, write `.runtime/fpf-conversion-evaluation.json` as a JSON object containing exactly `schema_version: 1`, `evaluator: "graph-fpf-evaluate-conversion-result"`, `verdict: "PASS"`, `current_revision`, `backup_revision`, `current_tree_sha256`, and `backup_tree_sha256`. Compute each tree digest over every regular file in sorted relative-path order as `relative_path + NUL + bytes + NUL`, excluding `.DS_Store`; reject symlinks. Do not write this file for `FAIL`, `UPSTREAM CONDITION`, or `INSUFFICIENT EVIDENCE`. A stale evidence file is not part of the new result and the converter finalizer must reject it when revisions or tree bytes differ.

## Result

Return:

- candidate and backup revisions;
- eval-pack identity and deterministic-suite evidence;
- bounded-set selection and coverage limits;
- all fourteen issue-family verdicts, historical regression probes, and syntax-risk-stratum coverage with evidence;
- consolidated classified findings and repair owner;
- upstream-source conditions, kept separate from conversion-result defects and the conversion verdict;
- overall verdict: `PASS`, `FAIL`, `UPSTREAM CONDITION`, or `INSUFFICIENT EVIDENCE`;
- exact handoff to the converter, or `no converter repair required`.
- PASS-evidence path and bound tree digests when the verdict is `PASS`.
