---
name: fpf
description: Route and run one command or an explicit + composition in English or Russian through the repository's First Principles Framework (FPF) prompt graph. Use when the user invokes $fpf, asks for FPF help or planning, or wants an applicability scan, SoTA harvest, option exploration, design challenge, decision synthesis, quality improvement, or alignment audit.
---

# FPF

Use the complete invocation, but do not preload graph prompts or references.
Treat the textual `/fpf` prefix like `$fpf` in the exact checks below.

- For empty `$fpf`, exact `$fpf help`, `$fpf ?`, `$fpf commands`, or `$fpf usage`, load `prompts/fpf-help.en.md`, return it, and stop. Never run the router or save a report.
- For exact `$fpf помощь`, `$fpf справка`, `$fpf команды`, or `$fpf как пользоваться`, load `prompts/fpf-help.ru.md`, return it, and stop. Never run the router or save a report.
- For every other invocation, load `prompts/fpf-runtime.md` completely and follow it with the complete invocation.

Never load `prompts/fpf-runtime.md` for a fast Help call. Never load either Help file for a non-Help call unless the runtime routes there.
