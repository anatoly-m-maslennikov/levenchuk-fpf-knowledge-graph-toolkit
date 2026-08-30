---
name: graph-fpf-convert-from-original
description: Refresh a revision-named source package with optional colocated patches from a read-only ailev/FPF checkout, stage it, convert its framework sources into generated graphs, and iterate through deterministic tests plus a dedicated result evaluator before clearing runtime sources and graph backups. Use when the user asks to update, rebuild, regenerate, or validate this repository's FPF graph.
---

# Graph FPF Convert From Original

Maintain the generated projection without loading the monolithic FPF source into model context. This repository-service package lives under `service/skills/`; it is conversion-tool maintenance, not an FPF methodology review.

Run repository modules from the toolkit root through its locked `uv` project with `uv run -m <module>`. Do not activate an environment or add an explicit interpreter or cache-prefix setting. The project pins Python and owns its ignored runtime and cache locations; the scripts themselves use only standard-library Python and Git and remain portable across Linux, macOS, and Windows.

## Resolve inputs

Locate one toolkit checkout containing:

- `service/scripts/graph_fpf_convert_from_original/`;
- `service/scripts/build_fpf_obsidian_graph/`;
- `service/scripts/validate_fpf_graph/`;
- `skills/settings.toml.example`.

Prefer the active workspace. Otherwise perform only a bounded search of accessible project roots. Do not assume a user name, home directory, operating system, or repository parent.

Treat configured `fpf_original_repo` as read-only input except for fast-forwarding it to the intended upstream HEAD. Then run `uv run -m service.scripts.graph_fpf_convert_from_original --refresh-source-package`. This copies every upstream-tracked file into `.fpf-original-<full-upstream-head>/`, applies any colocated `.patch` files in filename order, and records upstream and effective SHA-256 values. It must never author a patch, commit, or push in the external checkout.

Before conversion, run `uv run -m service.scripts.graph_fpf_convert_from_original --check-settings`. It must verify the configured committed upstream HEAD, the revision-named package inventory, patch digests, upstream digests, effective digests, and exact replay of the patches. Stop before graph mutation if any check fails.

Then run `uv run -m service.scripts.graph_fpf_convert_from_original --stage-sources`. It copies the verified package to `.runtime/original-fpf-sources`, including FPF, narrativization, any newly tracked upstream file, metadata, and patches. Conversion must read the staged effective files, not the external checkout or an unverified root copy.

The default evaluation skill is the separate project service `graph-fpf-evaluate-conversion-result`. Verify that it is accessible before mutation. A caller may explicitly name a different result-evaluation skill; when they do, use that evaluator and never silently substitute another. If the selected evaluator is unavailable, complete deterministic work and report `awaiting evaluation skill` rather than claiming the entire workflow passed.

## Convert and test

Running the converter mutates the generated tree, so require the user's refresh request or separate authorization. Preserve unrelated worktree changes; never reset or clean them.

1. Run `uv run -m service.scripts.graph_fpf_convert_from_original` from the toolkit root. It reads staged `FPF-Spec.md`, rotates `FPF-Knowledge-Graph` to `FPF-Knowledge-Graph.bak`, replaces an older backup transactionally, and rolls both graph paths back if conversion fails.
2. Run `uv run -m service.scripts.graph_npf_convert_from_original`. It reads the staged narrativization source and transactionally refreshes `NPF-Knowledge-Graph` and its backup. Add an explicit converter step for any newly supported staged framework; copying a new file does not imply a graph projection exists for it.
3. Run `uv run -m service.tests.run_tests`.
4. Classify every failure as a converter defect, deterministic-test defect, repository-integration defect, upstream-source condition, or unavailable evidence. Do not change the canonical FPF source and do not invent missing FPF content.
5. Fix authorized converter or test tooling defects. Then restart from conversion using the unchanged stage, rerun every applicable converter and the complete deterministic suite, and repeat until it passes. Restage only when the intended upstream commit changes. A targeted test may accelerate diagnosis but never replaces the complete rerun after a converter or test change.

Deterministic success requires exact filename and folder reconstruction, portable path hygiene, unique IDs, matching provenance and source ranges, zero broken wiki-links, reproducible generation, installer/package consistency, repository validation, script-architecture validation, and no stale hard-coded graph dependencies in any non-help prompt of the single methodology skill. It is necessary but not sufficient: the dedicated evaluator must also exercise every historical regression probe, all broader issue families, exhaustive mechanical coverage, and the bounded semantic-risk strata in its `references/evaluation-profile.md`. Script architecture means one `<tool_name>.py` manager, optional `<tool_name>_workers/` and `<tool_name>_assets/`, all tests under `service/tests/`, Python files no longer than 200 lines, atomic objects no longer than 40 lines, no source-tree bytecode caches, and one live settings authority outside the repository, projected into the installed skill. Platform metadata such as `.DS_Store` is not generated content and may be reported separately. Unresolved source references remain visible and classified; do not make the projection silently authoritative by deleting them.

## Evaluate the conversion result

1. Run `uv run -m service.scripts.graph_fpf_convert_from_original.prepare_eval` to produce the bounded revision, path-change, representative-ID, and relation-integrity pack.
2. Execute `graph-fpf-evaluate-conversion-result` unless the caller explicitly selected another result evaluator. Pass the pack, deterministic-suite evidence, current and backup graph roots, and canonical source locator. Preserve the evaluator's read-only boundary and let it select only the graph files and bounded source ranges required by its evaluation cases.
3. Preserve the evaluator's native result and evidence. Do not terminate delegated evaluation because of elapsed time or token budget alone; stop only for user cancellation or override, a confirmed safety/protected-scope violation, or the evaluator's own completed result.
4. If evaluation exposes a converter, deterministic-test, or eval-utility defect, fix the authorized tooling, rerun conversion, rerun the complete deterministic suite, rebuild the eval pack, and rerun the same evaluation skill with the same acceptance criteria.
5. If evaluation exposes only an upstream FPF condition, preserve it as an upstream finding. Never patch generated notes or the external checkout. A repository-owned source patch is a separate explicit source change: store it beside the revision-named originals, refresh the package, and restart the complete conversion and evaluation flow.

Only a `PASS` evaluator result may write `.runtime/fpf-conversion-evaluation.json`. Schema 2 binds the evaluator, current and backup revisions and tree digests, eval-pack digest, all required issue-family and historical-probe verdicts, syntax-risk coverage, semantic selection counts, and the exact deterministic-suite manifest and case list. Any other verdict must not create acceptance evidence.

## Close the loop

After deterministic tests and the specified evaluation pass:

1. Rerun `uv run -m service.tests.run_tests` once on the final converter and graph.
2. Confirm converter, test runner, graph validator, eval-pack utility, repository validation, and evaluator instructions still agree on paths, provenance, failure states, and restart boundaries.
3. Review the `skill-graph-compatibility` result. Update the `$fpf` prompt graph only when the new graph invalidates a hard-coded ID, graph path, revision, discovery rule, or retrieval assumption. A changed FPF title or folder alone does not require a skill edit when discovery remains dynamic.
4. Run `uv run -m service.scripts.graph_fpf_convert_from_original --finalize-accepted`. The finalizer verifies revision-bound evaluator evidence, verifies staged effective source bytes against the candidate, reruns the complete deterministic suite, and only then clears `.runtime/original-fpf-sources` plus every toolkit-root `*-Knowledge-Graph.bak` tree. It retains `.fpf-original-<full-upstream-head>/` and its patches.

If evidence is missing, stale, non-PASS, byte-mismatched, or the final suite fails, do not delete anything. Preserve the staged originals and all backups for diagnosis and restart from the owning failed boundary.

## Result

Report:

- settings preflight, canonical source repository, remote, revision, and generation date;
- staged-source revision and copied tracked-file inventory;
- converter and temporary-backup result;
- deterministic suite cases and failures;
- result-evaluation skill, evaluation cases, evidence, and verdict, or `awaiting evaluation skill`;
- each repair-loop iteration and why it restarted;
- remaining upstream-source conditions, kept separate from tooling defects;
- whether methodology skills require updates and the exact evidence;
- acceptance-evidence path and the exact staged-source and backup paths deleted, or why cleanup was withheld;
- final state: `complete`, `awaiting evaluation skill`, `tooling failed`, or `conversion failed and rolled back`.

Never translate successful conversion or evaluation into a claim that FPF itself is correct, complete, or aligned with another project.
