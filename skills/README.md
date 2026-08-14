# FPF Skills

This directory contains portable AI-agent skill packages for bounded use of the First Principles Framework.

These directories are the source of truth. Each complete package is a portable core: no provider-specific metadata is required. Install, copy, or link a complete package through the active skill-capable harness's supported user or project discovery mechanism. The harness owns discovery, permissions, tools, and optional delegation; ordinary chat and raw API use are out of scope. The `.skill` suffix is only this repository's folder convention; where a runtime derives a skill ID from the installed directory name, use the unprefixed `name` declared in `SKILL.md`. Invocation notation is runtime-owned and absent from this portable core.

Routing:

- `fpf-route.skill` turns one question into the smallest useful ordered sequence of copy-ready FPF skill calls without executing them.

Review and applicability:

- `fpf-applicability-scan.skill` identifies the smallest relevant set of FPF patterns for one question.
- `fpf-design-challenge.skill` challenges a proposed or not-yet-implemented design with bounded FPF evidence.
- `fpf-alignment-audit.skill` audits implemented or accepted work against relevant FPF patterns.

Generative and operational use:

- `fpf-options-explore.skill` generates diverse NQD-guided candidates and optionally compares method families through a pinned parity contract.
- `fpf-sota-harvest.skill` builds a reconstructible, plural SoTA synthesis pack without silently fusing rival traditions.
- `fpf-decision-synthesize.skill` records a recoverable project decision after candidate synthesis, then projects it into an audience-specific ADR.
- `fpf-quality-improve.skill` runs a bounded improvement loop that requires both a target-version change and demonstrated result change in declared quality coordinates.

Each package contains its complete `SKILL.md` contract. The skills discover an accessible FPF edition at runtime and do not assume this repository path, a specific operating system, or a particular workspace layout.

## Output language defaults

[`fpf-route.skill/fpf-settings.toml`](fpf-route.skill/fpf-settings.toml) is the source for the suite-wide defaults: `output_style = "general"`, `fpf_terms_explained = "off"`, and `install_method = "copy"`. The generated settings block in every package keeps each standalone copy portable; run `python3 scripts/sync_fpf_skill_settings.py --apply` from the repository root after changing either output setting, then run `--check`.

The repository installers for Codex and Claude Code copy packages by default and accept `--method symlink` for a live link to the checkout. The selected method is written to the real harness-local `fpf-route/fpf-settings.toml`, outside the repository, so later installations and updates reuse it automatically. In symlink mode, `fpf-route` is a local wrapper directory: every source entry except `fpf-settings.toml` links to this package, while the local settings file records the actual selected method. Both modes work on macOS, Linux, and WSL. Copy mode also avoids native Windows symlink-permission requirements.

An explicit user request overrides these embedded defaults for that result. `natural` retains natural FPF language, applies `full`, `short`, or `off` term explanations, and loads no style file. `general` loads only [`output-style-general.md`](fpf-route.skill/references/output-style-general.md); `ste` loads only [`output-style-ste.md`](fpf-route.skill/references/output-style-ste.md). Skills never preload the unselected file. In every style, retain exact FPF locators and source paths in compact evidence or source records rather than narrative prose.

Every result preserves its complete native artifact under four top-level sections: task, scope, and boundaries; high-confidence results at 95% or above; open questions below 95%, distinguishing probable answers at 90–94% from materially uncertain answers below 90%; and skills actually used, in execution order with each skill's role.

The skills-used section also contains a compact plain-Markdown FPF source trace. Methodology-consuming skills list every FPF source actually opened exactly once, distinguish files materially used as evidence from files only screened, and report read/used totals. Repository graph files use portable `FPF-Knowledge-Graph/...` paths, while non-file-backed editions use stable source identifiers. `fpf-route` is the explicit exception: because it uses its embedded skill catalog and makes no methodology claims, it reports that routing basis and marks FPF methodology sources as not applicable instead of showing a misleading zero-count trace.
