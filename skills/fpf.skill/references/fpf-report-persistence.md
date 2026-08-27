# Portable report persistence

Load this resource only after one of the seven executable FPF skills resolves `save_report = "on"`. `$fpf plan` ignores report persistence and `report_style`: it never loads this resource and never writes a report.

Resolve `report_style` only now, after report saving is on: explicit user instruction overrides an optional active-project `.caprmedio/settings.toml` setting, which overrides the installed `.fpf-runtime.toml` default, which overrides the embedded default `plain`. Absence of CAPRMEDIO settings is normal. Accepted values are exactly `plain` and `caprmedio`. Build the complete Markdown artifact once as the complete four-section FPF artifact and always return it in chat; never return a summary, placeholder, or pointer instead.

## Plain report delivery (`report_style = "plain"`)

Use an explicit user destination when given. Otherwise use `fpf-reports/` at the active task or project workspace. Keep the reported path portable and relative to that workspace or the user-provided destination root. Do not silently create a report in an identified input or source tree, including `FPF-Knowledge-Graph/`; the active workspace's own top-level `fpf-reports/` is allowed when that workspace is itself the input repository unless the user excludes it. Create the directory only when saving is enabled and permitted. Use UTF-8.

Before saving, add the final report path to `## Task, scope, and boundaries` as `Saved report: <path>`. Save the same exact Markdown as the chat artifact. Name each file `<UTC-timestamp>-fpf-<node-id>-<short-task-slug>.md`, where the timestamp contains only digits, `T`, and `Z`; use the selected analytical node ID from `graph.yaml`, or `composition` for an explicit stacked run; and reduce the task slug to a short lowercase ASCII hyphenated form. Never overwrite: if the proposed path exists, append `-2`, then `-3`, and so on before `.md` until a new file can be created.

## CAPRMEDIO report delivery (`report_style = "caprmedio"`)

Load only `references/fpf-caprmedio-report-adapter.md` and follow it. That adapter owns CAPRMEDIO detection, narrowest-containing-Scope-Unit selection, the BSEED special case, governed Analysis Report Atom creation, and admission validation. One composed run creates one complete Analysis Report Atom, never one Atom per intermediate node. Do not duplicate or improvise those mechanics here.

Saving either style is non-normative result delivery only. It never authorizes changes to analyzed targets or CAPRMEDIO authority.
