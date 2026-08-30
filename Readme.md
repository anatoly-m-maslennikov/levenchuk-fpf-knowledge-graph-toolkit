# Levenchuk’s FPF Knowledge Graph Toolkit

An Obsidian-ready, LLM-friendly usability fork of the original [First Principles Framework (FPF)](https://github.com/ailev/FPF).

## About this fork and FPF

This repository does not claim authority over upstream FPF. The canonical upstream source and its evolution remain in [ailev/FPF](https://github.com/ailev/FPF). This toolkit keeps a revision-bound local source package and may apply explicit repository-owned patches before graph conversion; any such patch is a toolkit change, not an upstream FPF change.

The FPF graph uses upstream revision [`563f4c8`](https://github.com/ailev/FPF/commit/563f4c8e06a319cbd375b66cdbb2df27a5f8b9ef), dated **2026-08-25**. The NPF projection is packaged under the same full repository HEAD; its unchanged narrativization bytes remain traceable through the source metadata.

FPF was created by **Anatoly Levenchuk, with AI-agent assistance**. It is a pattern language for making difficult engineering, research, management, governance, and human/AI work explicit and reviewable. It separates entities from descriptions, evidence, decisions, plans, and performed work; scopes claims to their intended use; and identifies the direct patterns governing a question.

The effective conversion sources are in [`.fpf-original-563f4c8e06a319cbd375b66cdbb2df27a5f8b9ef/`](.fpf-original-563f4c8e06a319cbd375b66cdbb2df27a5f8b9ef/). The folder contains every file tracked by that upstream HEAD and SHA-256 metadata for upstream and effective bytes. Its patch list is currently empty because upstream contains `F.0.2 Conceptual Synthesis across Source Ontologies`; a future repository-owned patch must live in this same revision-named folder and appear in the metadata. A script stages the verified package and generates smaller linked notes, hubs, indexes, and frontmatter. Runtime copies and graph backups are deleted after acceptance; the revision-named source package remains tracked.

## Why this version

The current specification is roughly 12 MB. Loading it for every question consumes many LLM tokens and weakens retrieval focus. This fork provides:

- bounded LLM retrieval of relevant patterns, with lower context cost;
- Obsidian hubs, links, backlinks, folders, frontmatter, and graph navigation;
- Obsidian CLI access for scripts and agents to search or read individual notes;
- pattern, relation, and term indexes with source-line metadata;
- shared human/agent navigation, incremental Git diffs, and automatic link validation.

## Repository layout

- [`FPF-Knowledge-Graph/`](FPF-Knowledge-Graph/) — generated graph and validation output.
- [`NPF-Knowledge-Graph/`](NPF-Knowledge-Graph/) — generated narrativization and narrative-studies graph using canonical `NSTD.*` identifiers and project-local `NPF` graph labels.
- [`skills/`](skills/) — the end-user `fpf.skill`, its bundled runtime helpers, and the global end-user installer.
- [`service/`](service/README.md) — original-FPF conversion, graph generation, validation, settings tools, project service skills, and their installer.
- [`service/tests/`](service/tests/) — every repository test and the deterministic maintenance-suite runner.
- [`service/scripts/build_fpf_obsidian_graph/`](service/scripts/build_fpf_obsidian_graph/) — generator.
- [`service/scripts/graph_npf_convert_from_original/`](service/scripts/graph_npf_convert_from_original/) — transactional NPF converter using the same configured original repository.
- [`skills/settings.toml.example`](skills/settings.toml.example) — tracked defaults template for the external end-user skill control panel.
- [`.fpf-original-563f4c8e06a319cbd375b66cdbb2df27a5f8b9ef/`](.fpf-original-563f4c8e06a319cbd375b66cdbb2df27a5f8b9ef/) — digest-bound full source package for upstream HEAD `563f4c8`; currently unpatched because upstream includes the required synthesis pattern.

## Included skills

The portable methodology package hardcodes no repository path, tool, operating system, or project layer. Its installer records the absolute local toolkit path in machine-local settings inside the installed skill, allowing runtime discovery of the bundled graph without requiring CAPRMEDIO. Installers expose it as the global Personal `$fpf` entry. This project exposes only the converter and evaluator service skills, avoiding a duplicate project-local `$fpf`. The original-to-graph converter skill resolves this owning checkout and its external control panel at runtime.

The single end-user `$fpf` package is a lazy bilingual prompt graph with a thin entry skill. General Help shows only three areas—framework, software, and skills—and exact area Help calls load one localized page directly; every other call loads one internal runtime prompt, which owns graph routing and execution. Its schema-4 YAML command graph separates analytical intent from a catalog of 22 reusable task profiles. Stable FPF IDs resolve through one repository-root-relative node catalog, so command and profile bindings do not duplicate paths or rediscover titles. A two-part connector returns only selected command/profile metadata, then hydrates only their verified FPF core sections; conditional patterns remain unloaded until their declared condition applies. Its standalone defaults are automatic English/Russian selection, general-language output, `save_report = "on"`, and `report_style = "plain"` (`plain` or `caprmedio`). Russian command aliases and natural-language routing select the same canonical prompt nodes; canonical command identifiers, FPF IDs, paths, code, quotations, and citations remain unchanged. An explicit user request overrides installed runtime defaults, which override embedded defaults; skill preferences are never read from the analyzed repository's `.caprmedio` directory, and `report_style` is consulted only when saving is on. Russian-language and style instructions each live once under the package references, and prompts load only the selected resources. See the [skills README](skills/README.md#output-and-report-defaults) for the portable contract.

| Command | Use case | Result |
|---|---|---|
| [`$fpf help`](skills/fpf.skill/prompts/help/en/fpf-help.md) | Show general information and select framework, software, or skills Help. | Help only; never saves. |
| [`$fpf plan`](skills/fpf.skill/prompts/fpf-plan.md) | Turn one question into the right FPF workflow. | Minimal ordered calls; never executes or saves. |
| [`$fpf problem frame`](skills/fpf.skill/prompts/fpf-problem-frame.md) | Bound an ambiguous need before solution work. | TaskSignature, problem-side result, acceptance boundary, or honest blocker. |
| [`$fpf structure recover`](skills/fpf.skill/prompts/fpf-structure-recover.md) | Recover what currently obtains without redesign. | Current entities, relations, boundaries, structure map, and missing information. |
| [`$fpf applicability scan`](skills/fpf.skill/prompts/fpf-applicability-scan.md) | Decide whether FPF is useful and which patterns apply. | Smallest relevant set, basis, use, and stop boundary. |
| [`$fpf design challenge`](skills/fpf.skill/prompts/fpf-design-challenge.md) | Challenge a proposal or not-yet-implemented decision. | Bounded finding with evidence and supported corrections. |
| [`$fpf alignment audit`](skills/fpf.skill/prompts/fpf-alignment-audit.md) | Check implemented or accepted work. | Per-claim semantic/mechanical audit with a bounded verdict. |
| [`$fpf sota harvest`](skills/fpf.skill/prompts/fpf-sota-harvest.md) | Map a bounded, plural state of the art. | Reconstructible corpus, claims, traditions, and disagreements. |
| [`$fpf options explore`](skills/fpf.skill/prompts/fpf-options-explore.md) | Generate and compare diverse candidates. | Candidate set, declared-coordinate evaluation, and decision handoff. |
| [`$fpf evaluation design`](skills/fpf.skill/prompts/fpf-evaluation-design.md) | Define how a target will be evaluated. | Characteristics, scales, checks, evidence, cases, and stop rules without execution. |
| [`$fpf decision synthesize`](skills/fpf.skill/prompts/fpf-decision-synthesize.md) | Choose among evaluated alternatives. | Recoverable decision, accepted losses, reopen triggers, and optional ADR. |
| [`$fpf quality improve`](skills/fpf.skill/prompts/fpf-quality-improve.md) | Improve a versioned target under a declared evaluation frame. | Target change, rerun comparison, trade-offs, and outcome. |
| [`graph-fpf-convert-from-original`](service/skills/graph-fpf-convert-from-original.skill/SKILL.md) | Convert canonical `ailev/FPF` into this repository's generated graph. | Transactional backup, deterministic tests, and repair-loop coordination. |
| [`graph-fpf-evaluate-conversion-result`](service/skills/graph-fpf-evaluate-conversion-result.skill/SKILL.md) | Evaluate one generated conversion candidate. | Exhaustive mechanical coverage, bounded semantic fidelity, historical regression probes, broader graph risks, and a classified verdict. |

The ten analytical nodes may save their complete result when `save_report = "on"`: `plain` preserves the plain Markdown copy, while `caprmedio` follows the verified CAPRMEDIO Analysis Report Atom adapter, including narrowest-containing-Scope-Unit selection and the BSEED special case. That does not authorize edits to the target. `$fpf help` and `$fpf plan` remain ephemeral and ignore report persistence and `report_style`.

Analytical commands can be composed explicitly with spaces around `+`, for example `$fpf design challenge + quality improve + alignment audit <shared task>`. A composition follows only legal graph handoffs, shares one campaign and stable finding registry, and stops at missing evidence or authority gates. It returns and saves one consolidated artifact: every issue and weak point found within the declared scope and evaluation profile, one deduplicated fixes and improvements list mapped to those findings, and the final verification and residual-risk state. Intermediate nodes do not create separate reports.

Prefix an explicit stack with `plan` to validate and render it without execution, for example `$fpf plan sota harvest + options explore + design challenge <shared task>`. The planner returns a copy-ready composition, never loads the analytical prompts, and never saves a report.

Near-match command typos produce canonical suggestions only in the non-executing planner/error path. A fuzzy match never launches an analytical node; the corrected command must be invoked explicitly.

Russian aliases can be used for direct calls and compositions, for example `$fpf проверка дизайна + улучшение качества + аудит согласованности <общая задача>`. `output_language = "auto"` chooses Russian when the invocation or residual task contains meaningful Russian Cyrillic text and English otherwise; `ru` or `en` fixes the language. `$fpf справка` opens the Russian area selector; `$fpf справка фреймворки`, `$fpf справка ПО`, and `$fpf справка навыки` open one area page directly.

Multi-step reviews use one shared [review-campaign protocol](skills/fpf.skill/references/fpf-review-campaign.md): stable finding fingerprints, explicit phases, one full challenge and one post-application audit per unchanged semantic frontier, targeted closure checks, and a hard stop when neither the frontier nor evaluation profile changed. This prevents design challenge and alignment audit from repeatedly reviewing the same unchanged target.

## Installing end-user and service skills

This repository is the source of truth for every bundled skill. [`skills/`](skills/) owns the end-user methodology package and its installer; [`service/`](service/) owns all repository tooling and the two project-only service skills. The complete repo-owned packages are portable cores; no provider-specific metadata is required. The `.skill` suffix is only this repository's source-folder convention.

The repository is a locked `uv` project pinned to Python 3.12. Python bytecode is routed to ignored `.runtime/pycache`; source folders must contain no `.pyc` files. Run its installers for Codex and Claude Code directly through `uv`; no activated environment, explicit interpreter, or cache-prefix setting is required:

```bash
uv run -m skills.install_fpf_skills.for_codex --apply
uv run -m skills.install_fpf_skills.for_claude --apply
uv run -m service.scripts.install_service_skills --apply
```

The install method is read only from `[skills].install_method` in the external control panel: `copy` creates self-contained package entries and `symlink` creates live entry links to this checkout. In both modes, the installed `fpf` folder itself is real. Each install writes an operational `.fpf-skills-install.json` receipt plus a real machine-local `.fpf-runtime.toml` inside that installed folder, so settings never resolve back into the source checkout. The runtime settings record the current skill version, absolute path of this toolkit checkout, and standalone output defaults; they are generated installation state, excluded from the reusable package, and not another authoring authority. `CODEX_HOME` and `CLAUDE_CONFIG_DIR` are respected, and `--destination` can select an exact skills directory. The same `uv run -m` commands work on native Windows; select `copy` in the control panel when symlink privileges are unavailable.

All installers are read-only without `--apply`. Use `--check` on the same command to verify packages, settings migration, cleanup state, and receipts. The Codex and Claude adapters under `skills/install_fpf_skills/` install only the end-user `fpf` package globally. On apply, the global installer moves any former `skills/settings*.toml` and `.caprmedio/settings*.toml` into the external control directory, preserves the prior current panel as an append-only `settings.<old-skill-version>.toml` snapshot, creates a new version-bearing `settings.toml` with all compatible values migrated, and projects it into the installed `fpf/.fpf-runtime.toml`. Existing external preferences always win over a legacy root `.fpf-runtime.toml`; `--apply --overwrite` explicitly imports its compatible preferences after preserving the previous external panel as another versioned snapshot. Known legacy names—including former global service-skill copies, `.skill`-suffixed copies, interrupted install/backup entries, the root runtime file, stale service receipts, and installer temporaries—are migration signals rather than ownership proof: apply moves them intact to `<harness-home>/.fpf-skills-quarantine/<UTC timestamp>/` and reports that path. Existing version snapshots and quarantined items are never deleted or overwritten; repeated same-second quarantines receive a numeric suffix. Unknown third-party skills remain untouched. `service.scripts.install_service_skills` installs only the two packages from `service/skills/` into `.agents/skills`, using symlinks by default or `--method copy` when required. It rejects any end-user or unknown project-discovery entry.

## Updating from upstream

Fetch or check out the original `ailev/FPF` repository outside the active Obsidian vault and treat it as read-only input. On first use, [`service/scripts/init_settings/`](service/scripts/init_settings/) creates the live control panel outside this repository at `<checkout-parent>/.<checkout-name>/settings.toml` from the tracked example; `FPF_TOOLKIT_CONFIG_DIR` overrides that directory. `[package]` identifies the `fpf` skill and its current version, `[paths].fpf_original_repo` points to the upstream checkout, and `[skills]` is the one control surface for portable language, output, report, and installer defaults. Existing five-setting and former in-repository control panels remain compatible: installer apply moves them outside, snapshots the old file, preserves paths and preferences, adds missing defaults such as `output_language = "auto"`, and writes the current package version into the new file. Edit only the external current control panel when the checkout or preferences differ; version snapshots are retained history. An explicit graph-builder `--source` still overrides the derived `FPF-Spec.md` path.

For a new upstream HEAD, first run `uv run -m service.scripts.graph_fpf_convert_from_original --refresh-source-package`. It copies every upstream-tracked file into a package whose folder name includes the full upstream commit, applies any colocated `.patch` files in filename order, and writes digest metadata. It never makes a local source patch, commit, or push in the external checkout; fast-forwarding that checkout to upstream is the refresh precondition. Then run `--check-settings` and `--stage-sources`; both reconstruct the effective result from the recorded upstream commit and fail if a patch, metadata record, stored byte, or file inventory differs. Run the FPF converter and then `uv run -m service.scripts.graph_npf_convert_from_original`; both read only the staged effective package and preserve their current graphs as temporary `.bak` trees. Run the deterministic suite, prepare the eval pack, and execute the separate evaluator. After it writes revision- and tree-bound PASS evidence, run `--finalize-accepted`. Finalization reruns the complete suite and clears the runtime stage plus every root `*-Knowledge-Graph.bak` tree while retaining the tracked revision-named package. Failed tests, failed evaluation, or stale evidence preserve all temporary inputs and backups.

The NPF projection uses the same staged checkout and reads `Narrativization-and-Narrative-Studies-Principles-Framework.md`. It writes `NPF-Knowledge-Graph`, temporarily rotates an existing projection to `NPF-Knowledge-Graph.bak`, and participates in the complete acceptance suite before cleanup.

## Local live quality gate

GitHub Actions remains deterministic and model-free. Before a skill release, run `uv run -m service.scripts.fpf_skill_quality_gate` from a normal local terminal with a logged-in, writable Codex CLI profile. It first requires the complete deterministic suite, then uses ephemeral read-only `codex exec` turns against the current source package for five bounded English/Russian and cross-area cases, followed by a separate structured semantic evaluator. Every declared criterion must pass independently; scores are never averaged. A failure returns all weaknesses and one consolidated fix list, exits non-zero, and does not refresh PASS evidence. A pass writes digest-bound local evidence under `.runtime/fpf-skill-quality-evaluation.json`; `uv run -m service.scripts.fpf_skill_quality_gate --check` rejects missing or stale evidence without making a model call. Use `--model <model>` to pin the local model when release policy requires it. This live gate is intentionally absent from `.github/workflows/ci.yml`.

Regenerate from the repository root:

```bash
uv run -m service.scripts.build_fpf_obsidian_graph \
  --source-revision 563f4c8e06a319cbd375b66cdbb2df27a5f8b9ef \
  --generated-on 2026-08-26 --clean
```

The report and every generated note record this revision, the SHA-256 of the exact source bytes, and the supplied generation date. Check the [`validation report`](FPF-Knowledge-Graph/00_Index/FPF%20-%20Validation%20Report.json) for zero broken links, then review the diff.

## Citation

Cite the original: `Levenchuk, Anatoly. First Principles Framework (FPF). https://github.com/ailev/FPF`
