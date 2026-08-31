# FPF Markdown Runtime

Treat this package as a lazily loaded Markdown graph. Never run Python, uv, a shell command, a bundled helper, or another executable to route or execute `$fpf`. Do not preload every prompt, task profile, or FPF page.

## Resolve installed settings and the FPF edition

For every non-fast-Help invocation, read the installer-managed `.fpf-runtime.toml` inside the logical installed skill directory as plain text. It is machine-local configuration, not a CAPRMEDIO file or executable dependency. Read its `repository_root` and `[defaults]` values when present. Verify that `<repository_root>/FPF-Knowledge-Graph/00_Index/FPF - Index.md` exists and identifies an FPF index before using it as the default edition. An explicitly supplied FPF source overrides this hint.

The installed defaults are standalone: `report_style = "plain"` and CAPRMEDIO is optional. Skill preferences are never read from an analyzed project's `.caprmedio/settings.toml`. Explicit user instructions override installed settings. When settings are absent or stale, Help and routing still work from embedded defaults, but analytical execution stops unless another FPF edition is verified.

## Route through Markdown

1. Resolve `output_language`: explicit instruction, then installed default, then `auto`. Accepted values are `auto`, `en`, and `ru`. With `auto`, choose Russian only when the invocation or residual task contains meaningful Russian Cyrillic text.
2. Load `references/fpf-command-graph.md` completely and apply its routing precedence to the complete invocation.
3. Preserve the original residual task after the matched command span. Never reconstruct or shorten it from normalized words.
4. When one development area is clear, load only its linked profile file and select at most one profile by complete alias or phrase. A profile adds context but never changes the selected analytical command.
5. If no command is unambiguous, select `plan`. Suggestions remain unexecuted proposals.

Canonical identifiers remain English and canonical invocation is `$fpf`; Russian aliases are equivalent. Textual `/fpf` remains accepted for portability.

## Execute the selected Markdown node

For an explicit legal composition, load `references/fpf-composition.md`, `references/fpf-analysis-contract.md`, and `references/fpf-context-connector.md` completely. Execute the selected prompts from left to right, loading only the current prompt and its selected command/profile FPF bindings. At each edge, enforce its typed producer output, consumer input, required evidence, gate predicate, and exact `STOP_*` state. Share one campaign and finding registry, stop at every evidence or authority gate, and do not emit or save intermediate node reports. When saving is enabled, load and resolve the one persistence protocol without creating the file. Then load `references/fpf-analysis-output.md` last, build its one consolidated artifact, and perform only an allowed exact create and read-back without reshaping it.

For a single node:

- `help`: load exactly the selected localized Help page, return it, and stop. Never save a report.
- `plan`: load `prompts/fpf-plan.md`, then load `references/fpf-plan-output.md` last and return only that call plan. Never execute proposed nodes or save a report.
- Any analytical node: load exactly the selected prompt from the command graph, `references/fpf-context-connector.md`, and `references/fpf-analysis-contract.md`. Pass the residual task, optional selected profile, and directly inspected FPF pages as methodology context. When saving is enabled, load and resolve the persistence protocol without creating the file. Then load `references/fpf-analysis-output.md` last, build the artifact, and perform only an allowed exact create and read-back without reshaping it; the native result list never defines alternative top-level headings.

The selected node's native sections belong inside the last-loaded output finalizer and never replace it. A stop, missing input, unavailable report write, or unexecuted composition suffix changes the recorded state; it never permits a shorter response envelope.

Load `references/fpf-output-language-ru.md` only for Russian output. Load one selected output-style reference at most. Load `references/fpf-report-persistence.md` only after report saving resolves to on; load the CAPRMEDIO adapter only when report style is `caprmedio`.

An edge in the Markdown graph validates only an explicit `+` handoff. It never authorizes another node automatically. A direct analytical call executes one node.

## Runtime dependency boundary

The installed end-user package requires only native skill loading and Markdown/plain-text file access. Python, uv, PyYAML, subprocesses, executable permissions, virtual environments, and runtime caches are repository-maintainer concerns and must not be required by this runtime.
