# FPF Skills

This directory is the end-user boundary. It contains the portable `$fpf` package and its global installer only. Repository-service scripts and skills live under [`../service/`](../service/).

## `$fpf` prompt graph

[`fpf.skill`](fpf.skill/SKILL.md) is the single end-user package. Its root `SKILL.md` is only a thin dispatch gate: exact general and area-specific English/Russian Help calls load one matching page directly, while every other call lazily loads [`fpf-runtime.md`](fpf.skill/prompts/fpf-runtime.md). General Help exposes only framework, software, and skills. The runtime owns routing and execution; [`graph.yaml`](fpf.skill/graph.yaml) declares analytical commands, areas, legal handoffs, shared contracts, and one stable FPF-node path catalog, while [`profiles.yaml`](fpf.skill/profiles.yaml) declares 22 reusable task profiles and exactly one executable routing/context evaluation case per profile. The two-part [`fpf-context-connector.md`](fpf.skill/references/fpf-context-connector.md) contract selects only active YAML command/profile nodes and hydrates only their verified FPF sections. Shared analytical behavior lives once in [`fpf-analysis-contract.md`](fpf.skill/references/fpf-analysis-contract.md); node-specific judgment remains under [`prompts/`](fpf.skill/prompts/).

Canonical Codex invocation is `$fpf`:

- `$fpf help` shows the help page and never saves.
- `$fpf plan <question>` returns the smallest useful call plan without executing it and never saves. `plan` replaces the former `route` name; `route` remains a resolver alias.
- `$fpf problem frame <task>` returns the earliest honest problem-side result without proposing a solution.
- `$fpf structure recover <task>` recovers a bounded current-state map without redesigning it.
- `$fpf applicability scan <task>` finds the smallest relevant pattern set.
- `$fpf sota harvest <task>` builds a reconstructible plural evidence map.
- `$fpf options explore <task>` generates and compares candidates without selection.
- `$fpf evaluation design <task>` defines a rerunnable evaluation without executing it or claiming a pass.
- `$fpf design challenge <task>` challenges a proposal before implementation.
- `$fpf decision synthesize <task>` records a recoverable choice among evaluated alternatives and can project an ADR.
- `$fpf quality improve <task>` runs a bounded target-change and re-evaluation loop.
- `$fpf alignment audit <task>` audits implemented or accepted work.

Natural-language text after `$fpf` is scored independently for analytical intent and optional task profile in English or Russian. A profile such as DDD, TDD, code quality, framework migration, or skill evaluation supplies subject-specific FPF context but never changes the selected operation. One clear command match runs that analytical prompt; an unmatched or tied request falls back to `plan`. Only the runtime, selected node prompt, and selected profile bindings are loaded. Exact general and area Help calls bypass the runtime and router entirely. A textual `/fpf` prefix is accepted by the resolver for host portability, but a Codex skill is invoked as `$fpf`.

Exact analytical commands can be stacked with spaces around `+`: `$fpf design challenge + quality improve + alignment audit <shared task>`. Task text is allowed only after the last command, and every adjacent pair must be a declared graph edge. The nodes run lazily under one campaign envelope and stop at unmet evidence, decision, or mutation gates. One consolidated result and report contains the deduplicated issue registry, one mapped fixes and improvements list, verification state, residual risk, and the actually executed node/source trace; intermediate node reports are suppressed.

Russian aliases can be stacked in the same way: `$fpf проверка дизайна + улучшение качества + аудит согласованности <общая задача>`. The Russian help tree displays one primary Russian alias for every node; canonical English commands remain available. Exact FPF IDs and locators, source paths, filenames required by host contracts, code, direct quotations, URLs, and citation targets are never translated.

The end-user installers install only `fpf` globally for Codex or Claude Code; this project does not expose another project-local `$fpf` entry. The separate service installer exposes exactly two packages from [`../service/skills/`](../service/skills/) under [`.agents/skills/`](../.agents/skills/).

## Review campaigns

When work continues from an earlier FPF report or finding set, analytical prompts load the shared [`fpf-review-campaign.md`](fpf.skill/references/fpf-review-campaign.md) protocol. It preserves semantic and carrier frontiers, the frozen evaluation profile, predecessor, stable finding fingerprints, lifecycle states, and the one permitted next transition. For one unchanged semantic frontier and profile, the budget is one full design challenge and one full post-application alignment audit; registered repairs use targeted closure checks, and an unchanged frontier stops instead of restarting the sequence. An explicit stack is one campaign surface and cannot reset this budget.

`$fpf plan` applies these phase gates before proposing calls. The ten analytical nodes preserve the campaign handoff when they participate. A repeated report or different node does not reset the budget or create a new finding when the failure predicate is unchanged.

## Output and report defaults

The installer writes machine-local `.fpf-runtime.toml` settings inside the installed `fpf` skill folder. They contain `skill_version`, the absolute toolkit `repository_root`, and standalone defaults including `report_style = "plain"`; `<repository_root>/FPF-Knowledge-Graph` is the normal default FPF edition after content verification. No CAPRMEDIO installation or project is required. The installed directory remains a real directory for both methods: copy mode contains package copies, while symlink mode links its package entries individually, so `.fpf-runtime.toml` never resolves back into this repository. An explicit user request overrides installed defaults, which override embedded defaults. Skill preferences—including `report_style = "caprmedio"`—are never read from a target repository's `.caprmedio/settings.toml`. `output_language = "auto"` selects Russian when the invocation or residual task contains meaningful Russian Cyrillic text and English otherwise; `ru` and `en` fix the language. Russian output loads only [`fpf-output-language-ru.md`](fpf.skill/references/fpf-output-language-ru.md); English loads no language resource.

The tracked [`settings.toml.example`](settings.toml.example) defines portable embedded defaults. The live control panel and append-only `settings.<version>.toml` snapshots live outside the repository at `<checkout-parent>/.<checkout-name>/` by default; `FPF_TOOLKIT_CONFIG_DIR` selects another external directory. Installer apply migrates old `skills/settings*.toml` and `.caprmedio/settings*.toml` files there without overwriting history. Defaults set `output_style = "general"`, `fpf_terms_explained = "off"`, `save_report = "on"`, `report_style = "plain"`, and `install_method = "copy"`. The installer projects the five runtime values into `.fpf-runtime.toml`; `install_method` remains toolkit-only. `natural` loads no style file. `general` loads only [`fpf-output-style-general.md`](fpf.skill/references/fpf-output-style-general.md); `ste` loads only [`fpf-output-style-ste.md`](fpf.skill/references/fpf-output-style-ste.md). Prompts never preload an unselected language or style file. Generated embedded defaults live once in the shared analytical contract and once in the ephemeral Plan prompt. Change portable defaults in the tracked example and run `uv run -m service.scripts.sync_fpf_skill_settings --apply`; changing external personal settings never rewrites tracked prompts and requires only reinstalling the skill.

The ten analytical nodes always return their complete Markdown artifact in chat. When saving is on, they load [`fpf-report-persistence.md`](fpf.skill/references/fpf-report-persistence.md). Plain delivery writes a non-overwriting UTF-8 copy under the active workspace's `fpf-reports/` unless the user supplies a destination. CAPRMEDIO delivery then loads the isolated [`fpf-caprmedio-report-adapter.md`](fpf.skill/references/fpf-caprmedio-report-adapter.md), selects the narrowest proven Scope Unit containing the whole analysis, handles ordered BSEED scope specially, and creates one governed non-normative Analysis Report Atom. It fails closed when topology or Atom admission rules are unresolved. `$fpf help` and `$fpf plan` never load persistence and never create reports.

Every analytical or composed result preserves four top-level sections: task, scope, and boundaries; issues, weak points, and improvements; unresolved evidence gaps; and skills used. Each issue has its own confidence and evidence basis, while every mapped fix variant has an independent confidence and basis; the result ends with one deduplicated ordered fix register. `$fpf plan` instead uses routing decisions and recommendations with routing confidence, because it proposes calls without analysing the task or consulting FPF methodology sources. Methodology-consuming nodes include a compact FPF source trace.

## Installation and validation

The global installers under [`install_fpf_skills/`](install_fpf_skills/) use the `name: fpf` package identity and install only `fpf.skill`; repository-service graph skills are outside this boundary. Apply moves any old in-repository control panel and snapshots to external configuration, archives the prior current panel as append-only `settings.<old-skill-version>.toml`, creates a current-version `settings.toml` with compatible values migrated, and writes the same skill version into the installed runtime settings. Existing external preferences win over a legacy root `.fpf-runtime.toml` by default; only explicit `--apply --overwrite` imports its compatible preferences, after the prior external panel is preserved as a versioned snapshot. A known legacy name triggers migration, not an ownership assumption: every matched older-layout or interrupted-install item is moved intact to the timestamped sibling directory `.fpf-skills-quarantine/`, whose path the installer reports. No historical settings snapshot or quarantined item is deleted or overwritten, and unknown third-party skills are never swept. `service.scripts.install_service_skills` independently installs only `service/skills/*.skill` into project discovery and excludes `fpf`, preventing duplicate Project and Personal entries. Each installer maintains its own receipt.

Run package checks with:

```bash
uv run -m service.scripts.fpf_skill_quality_gate
uv run -m service.scripts.fpf_skill_quality_gate --check
```

This is the local release-quality gate: five isolated read-only subject runs plus an independent criterion-by-criterion semantic evaluator. It uses local Codex authentication, writes only ignored `.runtime` evidence, fails on any individual criterion, and returns every weakness with one consolidated fix list. CI never invokes the live gate or receives model credentials; its deterministic tests only validate the gate's static contract.

```bash
uv run -m skills.install_fpf_skills.for_codex --check
uv run -m skills.install_fpf_skills.for_claude --check
uv run skills/fpf.skill/scripts/route_fpf.py --check
uv run -m service.tests.run_tests
```
