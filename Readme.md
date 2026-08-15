# Levenchuk’s FPF Knowledge Graph Toolkit

An Obsidian-ready, LLM-friendly usability fork of the original [First Principles Framework (FPF)](https://github.com/ailev/FPF).

## About this fork and FPF

This repository does not redefine FPF or claim authority over it. The canonical source and its evolution remain in [ailev/FPF](https://github.com/ailev/FPF).

This build uses upstream FPF revision [`9a9a42e`](https://github.com/ailev/FPF/commit/9a9a42e4d154021ca3f7415e0009a4214832f65f), dated **2026-08-02**.

FPF was created by **Anatoly Levenchuk, with AI-agent assistance**. It is a pattern language for making difficult engineering, research, management, governance, and human/AI work explicit and reviewable. It separates entities from descriptions, evidence, decisions, plans, and performed work; scopes claims to their intended use; and identifies the direct patterns governing a question.

The normative content is not rewritten. A script generates smaller linked notes, hubs, indexes, and frontmatter from the upstream source; the monolithic source itself is not stored in this repository.

## Why this version

The current specification is roughly 12 MB. Loading it for every question consumes many LLM tokens and weakens retrieval focus. This fork provides:

- bounded LLM retrieval of relevant patterns, with lower context cost;
- Obsidian hubs, links, backlinks, folders, frontmatter, and graph navigation;
- Obsidian CLI access for scripts and agents to search or read individual notes;
- pattern, relation, and term indexes with source-line metadata;
- shared human/agent navigation, incremental Git diffs, and automatic link validation.

## Repository layout

- [`FPF-Knowledge-Graph/`](FPF-Knowledge-Graph/) — generated graph and validation output.
- [`scripts/build_fpf_obsidian_graph.py`](scripts/build_fpf_obsidian_graph.py) — generator.
- [`skills/`](skills/) — portable agent skills, including suite-wide defaults in [`skills/fpf-route.skill/fpf-settings.toml`](skills/fpf-route.skill/fpf-settings.toml) and the synchronization helper [`scripts/sync_fpf_skill_settings.py`](scripts/sync_fpf_skill_settings.py).

## Included skills

The skills discover FPF at runtime and assume no repository path, tool, operating system, or project layer.

Their build-time default is general-language output. A result may use a different style only when the user explicitly requests it. General and STE instructions each live once in the `fpf-route` references; a skill loads only the selected style file, and natural output loads neither. See the [skills README](skills/README.md#output-language-defaults) for the portable contract.

| Skill | Use case | Result |
|---|---|---|
| [`fpf-route`](skills/fpf-route.skill/SKILL.md) | Turn one question into the right FPF workflow. | Minimal ordered skill calls with copy-ready tasks and handoffs. |
| [`fpf-applicability-scan`](skills/fpf-applicability-scan.skill/SKILL.md) | Decide whether FPF is useful and which patterns apply. | Smallest relevant set, basis, first result, use, and stop boundary. |
| [`fpf-design-challenge`](skills/fpf-design-challenge.skill/SKILL.md) | Challenge a proposal or not-yet-implemented decision. | Bounded finding with evidence and supported corrections. |
| [`fpf-alignment-audit`](skills/fpf-alignment-audit.skill/SKILL.md) | Check implemented or accepted work. | Per-claim semantic/mechanical audit with a bounded verdict. |
| [`fpf-sota-harvest`](skills/fpf-sota-harvest.skill/SKILL.md) | Map a bounded, plural state of the art. | Reconstructible corpus, claims, traditions, and disagreements. |
| [`fpf-options-explore`](skills/fpf-options-explore.skill/SKILL.md) | Generate and compare diverse candidates. | Candidate set, declared-coordinate evaluation, and decision handoff. |
| [`fpf-decision-synthesize`](skills/fpf-decision-synthesize.skill/SKILL.md) | Choose among evaluated alternatives. | Recoverable decision, accepted losses, reopen triggers, and optional ADR. |
| [`fpf-quality-improve`](skills/fpf-quality-improve.skill/SKILL.md) | Improve a versioned target under a declared evaluation frame. | Target change, rerun comparison, trade-offs, and outcome. |

All are read-only by default. Findings do not approve designs, authorize work, provide assurance, or make gate decisions.

## Installing the skills

This repository is the source of truth for every bundled `fpf-*` skill. Each complete repo-owned `SKILL.md` package is the portable core; no provider-specific metadata is required. The `.skill` suffix is only this repository's folder convention; installers use the unprefixed `name` declared in `SKILL.md`.

Python installers are included for Codex and Claude Code:

```bash
python3 scripts/install_fpf_skills_for_codex.py --apply
python3 scripts/install_fpf_skills_for_claude.py --apply
```

The portable default is a real copied installation. For a live installation that follows this checkout, add `--method symlink`. The chosen method is saved in the real harness-local `fpf-route/fpf-settings.toml`; later `--apply` and `--check` calls reuse it when `--method` is omitted. In symlink mode, that `fpf-route` directory is a local wrapper: its `SKILL.md` and `fpf-settings.toml` are real local files, while `references` links to this checkout. This makes the route entry discoverable while preserving shared live references. `CODEX_HOME` and `CLAUDE_CONFIG_DIR` are respected, and `--destination` can select an exact skills directory. The scripts use only the Python standard library and support macOS, Linux, WSL, and native Windows. On native Windows, use `py scripts\install_fpf_skills_for_codex.py --apply` (or the Claude filename) and keep the default copy mode when symlink privileges are unavailable.

Both installers are read-only without `--apply`. Use `--check` to verify all eight packages and their saved settings. With `--method symlink`, `--apply` refreshes known FPF package links, including earlier route wrappers whose `SKILL.md` was linked, when they point to an old or missing checkout; unmanaged real files and directories remain protected as conflicts.

## Updating from upstream

Fetch or check out upstream `FPF-Spec.md` outside the active Obsidian vault, then pass its path explicitly to the generator.

Regenerate from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_fpf_obsidian_graph.py \
  --source /path/to/FPF-Spec.md \
  --source-revision 9a9a42e4d154021ca3f7415e0009a4214832f65f \
  --generated-on 2026-08-02 --clean
```

The report and every generated note record this revision, the SHA-256 of the exact source bytes, and the supplied generation date. Check the [`validation report`](FPF-Knowledge-Graph/00_Index/FPF%20-%20Validation%20Report.json) for zero broken links, then review the diff.

## Citation

Cite the original: `Levenchuk, Anatoly. First Principles Framework (FPF). https://github.com/ailev/FPF`
