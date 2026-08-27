# FPF Runtime

Treat this package as a lazy-loaded prompt graph. Do not preload every prompt.

## Resolve installed settings and the default FPF edition

For every non-fast-Help invocation, look for the installer-managed `.fpf-runtime.toml` inside the logical installed skill directory. It is machine-local runtime configuration, not a CAPRMEDIO file and not part of the reusable package. Read its absolute `repository_root` and `[defaults]` values when present. Verify `<repository_root>/FPF-Knowledge-Graph` by content before using it as the default FPF edition; a source explicitly named by the user overrides this hint. Pass the verified graph root to an analytical node as its optional runtime hint.

The installed defaults are standalone: `report_style = "plain"` and no CAPRMEDIO installation or project is required. An active project's `.caprmedio/settings.toml` is optional and may override output or report defaults only when it is accessible; its absence is normal. Explicit user instructions override both project and installed settings. If installed settings are missing or the repository path is stale, Help and routing still work from embedded defaults, but report the stale installation before methodology analysis unless the user supplied another verified FPF edition.

## Resolve the node or composition

1. Resolve `output_language`: explicit user instruction overrides an optional active-project `.caprmedio/settings.toml` value, which overrides the installed default, which overrides the embedded default `auto`. Accepted values are `auto`, `en`, and `ru`.
2. Pass the complete invocation text and resolved language setting to `scripts/route_fpf.py`. When the verified repository root and `uv` are available, use the repository project so the YAML dependency and cache remain project-managed:

   `uv --project <repository-root> run python <this-skill-directory>/scripts/route_fpf.py --language "<auto|en|ru>" --text "<complete invocation>"`

3. If `uv` is unavailable, use another Python 3 environment only when it provides PyYAML. If local execution is unavailable, reproduce the same precedence from `graph.yaml`: explicit non-executing `plan <analytical command> + ...` meta-plan first, explicit executable composition next, longest exact command or alias next, then keyword score, then `plan` as the safe fallback.
4. Preserve the returned residual `task`, `language`, selected node IDs, and optional `task_profile`. The task profile identifies the development subject and supplies bounded FPF context; it never overrides the selected analytical intent. For `auto`, the router selects Russian only when the invocation or residual task contains meaningful Russian Cyrillic text; otherwise it selects English.

If the router returns `composition_error`, pass it to `$fpf plan` with the original task so the plan can explain the invalid handoff and the smallest legal correction.

If the router returns `suggestions`, route to `$fpf plan` and present them only as possible exact corrections. Preserve `execution_disabled = true`. Never convert a suggestion into an analytical call, silently repair the invocation, or load a suggested node's prompt. The user must invoke the corrected command or composition explicitly.

Canonical command identifiers remain English and canonical invocation is `$fpf`. Russian aliases and Russian natural-language routing are supported. A textual `/fpf` prefix is accepted by the resolver for portability, but a Codex skill is invoked as `$fpf`.

## Execute the resolved mode

For `mode: composition`, load `references/fpf-composition.md` and `references/fpf-context-connector.md` completely. For the configured file-backed edition, call `scripts/prepare_fpf_context.py` once with every returned ordered node ID, the verified repository root, and `--profile <task-profile-id>` when the router returned one; for an explicitly selected non-file-backed edition, follow the connector's stable-ID fallback. Include a conditional FPF ID only when the shared task satisfies its declared condition. Load the deduplicated contracts and one node-specific prompt at a time from the connector result; pass the selected task profile and hydrated pattern records as methodology context. Share one campaign and finding registry, stop at unmet authority or evidence gates, and return and persist one consolidated artifact with every in-scope issue or weakness plus one mapped fixes and improvements list. Do not emit or save separate intermediate node reports.

For a single-node result:

- `help`: load exactly the returned localized general or area Help prompt, return its page, and stop. Never save a report or load another Help page.
- `plan`: load `prompts/fpf-plan.md`, produce only the call plan, and stop. When the router returns `mode: plan`, preserve its `planned_nodes`, `planned_commands`, shared `task`, and `execution_disabled = true`; validate and render that proposed stack without loading its analytical prompts or the composition execution resource. Do not execute proposed nodes and never save a report.
- Any analytical node: load `references/fpf-context-connector.md`. For the configured file-backed edition, call `scripts/prepare_fpf_context.py` with the selected node ID, verified repository root, and `--profile <task-profile-id>` when the router returned one; for an explicitly selected non-file-backed edition, follow the connector's stable-ID fallback. Include a conditional FPF ID only when the residual task satisfies its declared condition. Load only the returned contracts and node prompt, pass the selected task profile and hydrated pattern records as methodology context, execute the combined contract on the residual task, and follow its output and report settings.

The connector's YAML reader and context hydrator are the normal analytical path; do not manually load unrelated graph nodes or FPF pages. Shared contracts and analytical prompts may refer to other files under `references/`. Load a referenced file only when the active contract says to do so. In particular, load `references/fpf-output-language-ru.md` only for Russian output; load `references/fpf-report-persistence.md` only after report saving resolves to on; load the CAPRMEDIO adapter only when the selected report style is `caprmedio`.

Do not treat a graph edge as permission to execute another node. Edges are legal handoffs for `$fpf plan` and validators for an explicit `+` composition. A direct analytical call still executes one node unless the user explicitly composes commands.

## Maintainer checks

After changing the graph, prompts, aliases, or Help pages, run:

`uv --project <repository-root> run python <this-skill-directory>/scripts/route_fpf.py --check`

`uv --project <repository-root> run -m service.tests.run_tests`
