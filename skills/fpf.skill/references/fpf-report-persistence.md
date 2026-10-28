# Portable report persistence

Load this resource inside the doer only after an analytical FPF node resolves `save_report = "on"`. `$fpf plan` ignores report persistence and `report_style`: it never loads this resource and never writes a report. The doer resolves the exact delivery plan but creates no durable report; only the manager may perform the declared action after warden `PASS`.

Resolve `report_style` only now, after report saving is on: explicit user instruction overrides the installed `.fpf-runtime.toml` default, which overrides the embedded default `plain`. Never read this skill preference from a target repository's `.caprmedio/settings.toml`. Accepted values are exactly `plain` and `caprmedio`. Build the complete Markdown artifact once as the complete four-section FPF artifact and always return it in chat; never return a summary, placeholder, or pointer instead.

## Plain report delivery (`report_style = "plain"`)

Use an explicit user destination when given. Otherwise use `fpf-reports/` at the active task or project workspace. Keep the reported path portable and relative to that workspace or the user-provided destination root. Do not silently create a report in an identified input or source tree, including `FPF-Knowledge-Graph/`; the active workspace's own top-level `fpf-reports/` is allowed when that workspace is itself the input repository unless the user excludes it. Create the directory only when saving is enabled and permitted. Use UTF-8.

Name each file `<UTC-timestamp>-fpf-<node-id>-<short-task-slug>.md`, where the timestamp contains only digits, `T`, and `Z`; use the selected analytical node ID from the Markdown command graph, or `composition` for an explicit stacked run; and reduce the task slug to a short lowercase ASCII hyphenated form. Never overwrite: inspect the destination immediately before writing; if the proposed path exists, append `-2`, then `-3`, and so on before `.md` until the chosen path is absent.

Require a host-native file operation that guarantees create-if-absent and complete UTF-8 content. This Markdown-only skill does not bundle an atomic writer. If the host cannot guarantee exclusive non-overwriting creation, plan no write and use `STOPPED_UNSAVED: NO_EXCLUSIVE_CREATE`; do not weaken the contract by doing a check-then-overwrite write.

After selecting a creatable path, add `Saved report: <path>` to `## Task, scope, and boundaries`, finalize `candidate.md` once, and record `plain-exclusive-create` plus the same path in `candidate-meta.md`. After warden `PASS`, the manager creates the durable file with those exact UTF-8 bytes, reads it back immediately, and compares its complete text with the candidate. Release `SAVED` only when the path was new and the read-back text is identical. A collision returns to the same doer for a new path and another warden pass. A failed or unverifiable read-back ends blocked as `FAILED_VERIFICATION`, identifies the suspect path, and never claims that a report was saved. Never claim atomicity, durability, or a content hash unless the host operation itself supplies that exact guarantee or digest; a hash is supplemental evidence, not a runtime requirement.

## CAPRMEDIO report delivery (`report_style = "caprmedio"`)

Load only `references/fpf-caprmedio-report-adapter.md` and follow it. That adapter owns CAPRMEDIO detection, narrowest-containing-Scope-Unit selection, the BSEED special case, governed Analysis Report Atom creation, and admission validation. One composed run creates one complete Analysis Report Atom, never one Atom per intermediate node. Do not duplicate or improvise those mechanics here.

Use only current project authority and the project-native governed creator to resolve one exact Analysis Report Atom action. The doer records `caprmedio-governed-create` and the resolved governed target without performing it. After warden `PASS`, the manager creates exactly one Atom with the validated candidate bytes and verifies admission. Never infer topology from folders and never introduce an end-user runtime helper.

Saving either style is non-normative result delivery only. It never authorizes changes to analyzed targets or CAPRMEDIO authority.
