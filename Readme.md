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
- [`scripts/`](scripts/README.md) — repository tools, one directory per tool with colocated tests.
- [`scripts/build_fpf_obsidian_graph/`](scripts/build_fpf_obsidian_graph/) — generator.
- [`scripts/graph_npf_convert_from_original/`](scripts/graph_npf_convert_from_original/) — transactional NPF converter using the same configured original repository.
- [`.caprmedio/settings.toml.example`](.caprmedio/settings.toml.example) — tracked template for the repository's single ignored control panel.
- [`.fpf-original-563f4c8e06a319cbd375b66cdbb2df27a5f8b9ef/`](.fpf-original-563f4c8e06a319cbd375b66cdbb2df27a5f8b9ef/) — digest-bound full source package for upstream HEAD `563f4c8`; currently unpatched because upstream includes the required synthesis pattern.
- [`skills/`](skills/) — portable agent skills whose embedded defaults are synchronized from the control panel by [`scripts/sync_fpf_skill_settings/`](scripts/sync_fpf_skill_settings/).

## Included skills

The methodology skill discovers FPF at runtime and assumes no repository path, tool, operating system, or project layer. Installers expose it as the global Personal `$fpf` entry. This project exposes only the converter and evaluator service skills, avoiding a duplicate project-local `$fpf`. The original-to-graph converter skill resolves this owning checkout and its ignored repository setting at runtime.

The single end-user `$fpf` package is a lazy bilingual prompt graph with a thin entry skill. Exact English and Russian Help calls load separate pages directly; every other call loads one internal runtime prompt, which owns graph routing and execution. Its build-time defaults are automatic English/Russian selection, general-language output, `save_report = "on"`, and `report_style = "plain"` (`plain` or `caprmedio`). Russian command aliases and natural-language routing select the same canonical prompt nodes; canonical command identifiers, FPF IDs, paths, code, quotations, and citations remain unchanged. A result may use a different language, style, or report setting when the user explicitly requests it; an accessible harness-local or repository suite setting otherwise overrides the embedded defaults; `report_style` is consulted only when saving is on. Russian-language and style instructions each live once under the package references, and prompts load only the selected resources. See the [skills README](skills/README.md#output-and-report-defaults) for the portable contract.

| Command | Use case | Result |
|---|---|---|
| [`$fpf help`](skills/fpf.skill/prompts/fpf-help.en.md) | Show the prompt tree and examples. | Help only; never saves. |
| [`$fpf plan`](skills/fpf.skill/prompts/fpf-plan.md) | Turn one question into the right FPF workflow. | Minimal ordered calls; never executes or saves. |
| [`$fpf applicability scan`](skills/fpf.skill/prompts/fpf-applicability-scan.md) | Decide whether FPF is useful and which patterns apply. | Smallest relevant set, basis, use, and stop boundary. |
| [`$fpf design challenge`](skills/fpf.skill/prompts/fpf-design-challenge.md) | Challenge a proposal or not-yet-implemented decision. | Bounded finding with evidence and supported corrections. |
| [`$fpf alignment audit`](skills/fpf.skill/prompts/fpf-alignment-audit.md) | Check implemented or accepted work. | Per-claim semantic/mechanical audit with a bounded verdict. |
| [`$fpf sota harvest`](skills/fpf.skill/prompts/fpf-sota-harvest.md) | Map a bounded, plural state of the art. | Reconstructible corpus, claims, traditions, and disagreements. |
| [`$fpf options explore`](skills/fpf.skill/prompts/fpf-options-explore.md) | Generate and compare diverse candidates. | Candidate set, declared-coordinate evaluation, and decision handoff. |
| [`$fpf decision synthesize`](skills/fpf.skill/prompts/fpf-decision-synthesize.md) | Choose among evaluated alternatives. | Recoverable decision, accepted losses, reopen triggers, and optional ADR. |
| [`$fpf quality improve`](skills/fpf.skill/prompts/fpf-quality-improve.md) | Improve a versioned target under a declared evaluation frame. | Target change, rerun comparison, trade-offs, and outcome. |
| [`graph-fpf-convert-from-original`](skills/graph-fpf-convert-from-original.skill/SKILL.md) | Convert canonical `ailev/FPF` into this repository's generated graph. | Transactional backup, deterministic tests, and repair-loop coordination. |
| [`graph-fpf-evaluate-conversion-result`](skills/graph-fpf-evaluate-conversion-result.skill/SKILL.md) | Evaluate one generated conversion candidate. | Exhaustive mechanical coverage, bounded semantic fidelity, historical regression probes, broader graph risks, and a classified verdict. |

The seven analytical nodes may save their complete result when `save_report = "on"`: `plain` preserves the plain Markdown copy, while `caprmedio` follows the verified CAPRMEDIO Analysis Report Atom adapter, including narrowest-containing-Scope-Unit selection and the BSEED special case. That does not authorize edits to the target. `$fpf help` and `$fpf plan` remain ephemeral and ignore report persistence and `report_style`.

Analytical commands can be composed explicitly with spaces around `+`, for example `$fpf design challenge + quality improve + alignment audit <shared task>`. A composition follows only legal graph handoffs, shares one campaign and stable finding registry, and stops at missing evidence or authority gates. It returns and saves one consolidated artifact: every issue and weak point found within the declared scope and evaluation profile, one deduplicated fixes and improvements list mapped to those findings, and the final verification and residual-risk state. Intermediate nodes do not create separate reports.

Russian aliases can be used for direct calls and compositions, for example `$fpf проверка дизайна + улучшение качества + аудит согласованности <общая задача>`. `output_language = "auto"` chooses Russian when the invocation or residual task contains meaningful Russian Cyrillic text and English otherwise; `ru` or `en` fixes the language. `$fpf справка` opens the Russian help page, whose command tree uses the primary Russian aliases.

Multi-step reviews use one shared [review-campaign protocol](skills/fpf.skill/references/fpf-review-campaign.md): stable finding fingerprints, explicit phases, one full challenge and one post-application audit per unchanged semantic frontier, targeted closure checks, and a hard stop when neither the frontier nor evaluation profile changed. This prevents design challenge and alignment audit from repeatedly reviewing the same unchanged target.

## Installing the skills

This repository is the source of truth for every bundled skill. [`fpf.skill`](skills/fpf.skill/) is the one end-user methodology package; repository-service skills use a different name. The complete repo-owned package is the portable core; no provider-specific metadata is required. The `.skill` suffix is only this repository's source-folder convention; installers use `name: fpf` from `SKILL.md`.

The repository is a locked `uv` project pinned to Python 3.12. Run its installers for Codex and Claude Code directly through `uv`; no activated environment, explicit interpreter, or cache-prefix setting is required:

```bash
uv run -m scripts.install_fpf_skills.for_codex --apply
uv run -m scripts.install_fpf_skills.for_claude --apply
```

The install method is read only from `[skills].install_method` in the toolkit's `.caprmedio/settings.toml`: `copy` creates self-contained directories and `symlink` creates live links to this checkout. Each install writes an operational `.fpf-skills-install.json` receipt plus machine-local `.fpf-runtime.toml` settings beside the installed skill. The runtime settings record the absolute path of this toolkit checkout and standalone output defaults; they are generated installation state, not another authoring authority. `CODEX_HOME` and `CLAUDE_CONFIG_DIR` are respected, and `--destination` can select an exact skills directory. The same `uv run -m` commands work on native Windows; select `copy` in the control panel when symlink privileges are unavailable.

Both installers are read-only without `--apply`. Use `--check` to verify the single end-user `fpf` package and its receipt. Applying over the former eight-package suite removes only unmodified installer-managed legacy packages; modified or unmanaged legacy packages block migration and remain untouched. The separate conversion and conversion-result-evaluation service skills are deliberately not installed globally, while project discovery deliberately excludes the end-user `fpf` package.

## Updating from upstream

Fetch or check out the original `ailev/FPF` repository outside the active Obsidian vault and treat it as read-only input. On first use, [`scripts/init_settings/`](scripts/init_settings/) creates ignored `.caprmedio/settings.toml` from the tracked example. `[paths].fpf_original_repo` points to that repository; `[skills]` is the one control surface for portable language, output, report, and installer defaults. Existing five-setting control panels remain compatible and resolve the missing `output_language` as `auto`. Edit only this local control panel when the checkout or preferences differ. An explicit graph-builder `--source` still overrides the derived `FPF-Spec.md` path.

For a new upstream HEAD, first run `uv run -m scripts.graph_fpf_convert_from_original --refresh-source-package`. It copies every upstream-tracked file into a package whose folder name includes the full upstream commit, applies any colocated `.patch` files in filename order, and writes digest metadata. It never makes a local source patch, commit, or push in the external checkout; fast-forwarding that checkout to upstream is the refresh precondition. Then run `--check-settings` and `--stage-sources`; both reconstruct the effective result from the recorded upstream commit and fail if a patch, metadata record, stored byte, or file inventory differs. Run the FPF converter and then `uv run -m scripts.graph_npf_convert_from_original`; both read only the staged effective package and preserve their current graphs as temporary `.bak` trees. Run the deterministic suite, prepare the eval pack, and execute the separate evaluator. After it writes revision- and tree-bound PASS evidence, run `--finalize-accepted`. Finalization reruns the complete suite and clears the runtime stage plus every root `*-Knowledge-Graph.bak` tree while retaining the tracked revision-named package. Failed tests, failed evaluation, or stale evidence preserve all temporary inputs and backups.

The NPF projection uses the same staged checkout and reads `Narrativization-and-Narrative-Studies-Principles-Framework.md`. It writes `NPF-Knowledge-Graph`, temporarily rotates an existing projection to `NPF-Knowledge-Graph.bak`, and participates in the complete acceptance suite before cleanup.

Regenerate from the repository root:

```bash
uv run -m scripts.build_fpf_obsidian_graph \
  --source-revision 563f4c8e06a319cbd375b66cdbb2df27a5f8b9ef \
  --generated-on 2026-08-26 --clean
```

The report and every generated note record this revision, the SHA-256 of the exact source bytes, and the supplied generation date. Check the [`validation report`](FPF-Knowledge-Graph/00_Index/FPF%20-%20Validation%20Report.json) for zero broken links, then review the diff.

## Citation

Cite the original: `Levenchuk, Anatoly. First Principles Framework (FPF). https://github.com/ailev/FPF`
