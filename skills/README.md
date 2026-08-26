# FPF Skills

This directory contains one portable end-user First Principles Framework skill and two separate repository-service graph skills.

## `$fpf` prompt graph

[`fpf.skill`](fpf.skill/SKILL.md) is the single end-user package. Its root `SKILL.md` is only a thin dispatch gate: exact English and Russian Help calls load [`fpf-help.en.md`](fpf.skill/prompts/fpf-help.en.md) or [`fpf-help.ru.md`](fpf.skill/prompts/fpf-help.ru.md) directly, while every other call lazily loads [`fpf-runtime.md`](fpf.skill/prompts/fpf-runtime.md). The runtime owns routing and execution; [`graph.json`](fpf.skill/graph.json) declares commands, aliases, keywords, persistence flags, and legal handoffs; substantive node contracts remain under [`prompts/`](fpf.skill/prompts/).

Canonical Codex invocation is `$fpf`:

- `$fpf help` shows the help page and never saves.
- `$fpf plan <question>` returns the smallest useful call plan without executing it and never saves. `plan` replaces the former `route` name; `route` remains a resolver alias.
- `$fpf applicability scan <task>` finds the smallest relevant pattern set.
- `$fpf sota harvest <task>` builds a reconstructible plural evidence map.
- `$fpf options explore <task>` generates and compares candidates without selection.
- `$fpf design challenge <task>` challenges a proposal before implementation.
- `$fpf decision synthesize <task>` records a recoverable choice among evaluated alternatives and can project an ADR.
- `$fpf quality improve <task>` runs a bounded target-change and re-evaluation loop.
- `$fpf alignment audit <task>` audits implemented or accepted work.

Natural-language text after `$fpf` is scored against the graph in English or Russian. Russian aliases route to the same canonical English command identifiers. One clear match runs that analytical prompt; an unmatched or tied request falls back to `plan`. Only the runtime and selected node prompt are loaded. Exact `$fpf help` and `$fpf помощь` bypass the runtime and router entirely. A textual `/fpf` prefix is accepted by the resolver for host portability, but a Codex skill is invoked as `$fpf`.

Exact analytical commands can be stacked with spaces around `+`: `$fpf design challenge + quality improve + alignment audit <shared task>`. Task text is allowed only after the last command, and every adjacent pair must be a declared graph edge. The nodes run lazily under one campaign envelope and stop at unmet evidence, decision, or mutation gates. One consolidated result and report contains the deduplicated issue registry, one mapped fixes and improvements list, verification state, residual risk, and the actually executed node/source trace; intermediate node reports are suppressed.

Russian aliases can be stacked in the same way: `$fpf проверка дизайна + улучшение качества + аудит согласованности <общая задача>`. The Russian help tree displays one primary Russian alias for every node; canonical English commands remain available. Exact FPF IDs and locators, source paths, filenames required by host contracts, code, direct quotations, URLs, and citation targets are never translated.

The repository installers install the single end-user `fpf` package globally for Codex or Claude Code; this project does not expose another project-local `$fpf` entry. Project discovery under [`.agents/skills/`](../.agents/skills/) contains only two service skills: [`graph-fpf-convert-from-original.skill`](graph-fpf-convert-from-original.skill/SKILL.md) refreshes the full upstream HEAD into a revision-named tracked package, applies any colocated patches, stages the verified effective sources, performs transactional graph conversions and repair loops, and clears runtime sources plus backups only after acceptance; [`graph-fpf-evaluate-conversion-result.skill`](graph-fpf-evaluate-conversion-result.skill/SKILL.md) independently evaluates the candidate and emits revision-bound cleanup evidence only for PASS.

## Review campaigns

When work continues from an earlier FPF report or finding set, analytical prompts load the shared [`fpf-review-campaign.md`](fpf.skill/references/fpf-review-campaign.md) protocol. It preserves semantic and carrier frontiers, the frozen evaluation profile, predecessor, stable finding fingerprints, lifecycle states, and the one permitted next transition. For one unchanged semantic frontier and profile, the budget is one full design challenge and one full post-application alignment audit; registered repairs use targeted closure checks, and an unchanged frontier stops instead of restarting the sequence. An explicit stack is one campaign surface and cannot reset this budget.

`$fpf plan` applies these phase gates before proposing calls. The seven analytical nodes preserve the campaign handoff when they participate. A repeated report or different node does not reset the budget or create a new finding when the failure predicate is unchanged.

## Output and report defaults

An explicit user request overrides an accessible `.caprmedio/settings.toml` setting, which overrides the embedded default. `output_language = "auto"` selects Russian when the invocation or residual task contains meaningful Russian Cyrillic text and English otherwise; `ru` and `en` fix the language. Russian output loads only [`fpf-output-language-ru.md`](fpf.skill/references/fpf-output-language-ru.md); English loads no language resource. Existing five-setting control panels are read as `output_language = "auto"` for upgrade compatibility.

The tracked control-panel defaults also set `output_style = "general"`, `fpf_terms_explained = "off"`, `save_report = "on"`, `report_style = "plain"`, and `install_method = "copy"`. `natural` loads no style file. `general` loads only [`fpf-output-style-general.md`](fpf.skill/references/fpf-output-style-general.md); `ste` loads only [`fpf-output-style-ste.md`](fpf.skill/references/fpf-output-style-ste.md). Prompts never preload an unselected language or style file. The generated settings block in each of the eight non-help prompt files keeps the package portable. After changing a suite setting, run `uv run -m scripts.sync_fpf_skill_settings --apply`, then run `--check`.

The seven analytical nodes always return their complete Markdown artifact in chat. When saving is on, they load [`fpf-report-persistence.md`](fpf.skill/references/fpf-report-persistence.md). Plain delivery writes a non-overwriting UTF-8 copy under the active workspace's `fpf-reports/` unless the user supplies a destination. CAPRMEDIO delivery then loads the isolated [`fpf-caprmedio-report-adapter.md`](fpf.skill/references/fpf-caprmedio-report-adapter.md), selects the narrowest proven Scope Unit containing the whole analysis, handles ordered BSEED scope specially, and creates one governed non-normative Analysis Report Atom. It fails closed when topology or Atom admission rules are unresolved. `$fpf help` and `$fpf plan` never load persistence and never create reports.

Every analytical result preserves four top-level sections: task, scope, and boundaries; high-confidence results at 95% or above; open questions below 95%; and nodes actually used. Methodology-consuming nodes include a compact FPF source trace. `$fpf plan` is the explicit source-accounting exception because it makes no methodology claims.

## Installation and validation

The installers use the `name: fpf` package identity and install only `fpf.skill`; both repository-service graph skills are excluded. Conversely, project discovery exposes only the service skills and excludes `fpf`, preventing duplicate Project and Personal entries. A schema-2 receipt allows a safe migration from the former eight-package suite: unmodified installer-managed packages are removed, while modified or unmanaged legacy packages block migration and remain untouched.

Run package checks with:

```bash
uv run skills/fpf.skill/scripts/route_fpf.py --check
uv run -m unittest discover -s skills/fpf.skill/scripts/tests -p 'test_*.py'
uv run -m scripts.validate_repository
```
