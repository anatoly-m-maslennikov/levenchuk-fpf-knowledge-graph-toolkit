---
name: fpf
description: Route and run one command or an explicit + composition in English or Russian through the repository's First Principles Framework (FPF) prompt graph. Use when the user invokes $fpf, asks for area-specific FPF help or planning, or analyzes framework, software, or skill development.
---

# FPF

Use the complete invocation, but do not preload graph prompts or references.
Treat the textual `/fpf` prefix like `$fpf` in the exact checks below.

- For empty `$fpf`, exact `$fpf help`, `$fpf ?`, `$fpf commands`, or `$fpf usage`, load `prompts/help/en/fpf-help.md`, return it, and stop. Never run the router or save a report.
- For exact `$fpf справка`, `$fpf помощь`, `$fpf команды`, or `$fpf как пользоваться`, load `prompts/help/ru/fpf-help.md`, return it, and stop. Never run the router or save a report.
- For exact English area Help (`help framework`, `help software`, or `help skills`), load the matching `prompts/help/en/fpf-help-<area>.md`, return it, and stop.
- For exact Russian area Help (`справка фреймворки`, `справка ПО`, or `справка навыки`), load the matching `prompts/help/ru/fpf-help-<area>.md`, return it, and stop.
- For every other invocation, load `prompts/fpf-runtime.md` completely and follow it with the complete invocation.

Never load `prompts/fpf-runtime.md` for a fast Help call. Never load either Help file for a non-Help call unless the runtime routes there.
