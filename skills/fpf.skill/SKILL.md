---
name: fpf
description: Plan and, after approval, run one command or an explicit + composition in English or Russian through the repository's First Principles Framework (FPF) prompt graph. Use when the user invokes $fpf, asks for FPF help or planning, analyzes framework, software, or skill development, replies exact do to an outstanding FPF Plan, explicitly requests execution without a Plan, or answers its blocking question.
---

# FPF

Use the complete invocation, but do not preload graph prompts or references. The installed end-user runtime is Markdown-only: never run Python, uv, a shell command, or another executable to route or execute `$fpf`.
Treat the textual `/fpf` prefix like `$fpf` in the exact checks below.

- For empty `$fpf`, exact `$fpf help`, `$fpf ?`, `$fpf commands`, or `$fpf usage`, load `prompts/help/en/fpf-help.md`, return it, and stop. Never run the router or save a report. Help pages are interface copy, not FPF methodology sources.
- For exact `$fpf справка`, `$fpf помощь`, `$fpf команды`, or `$fpf как пользоваться`, load `prompts/help/ru/fpf-help.md`, return it, and stop. Never run the router or save a report. Help pages are interface copy, not FPF methodology sources.
- For exact English area Help (`help framework`, `help software`, or `help skills`), load the matching `prompts/help/en/fpf-help-<area>.md`, return it, and stop. Treat that Help page as interface copy, not an FPF methodology source.
- For exact Russian area Help (`справка фреймворки`, `справка ПО`, or `справка навыки`), load the matching `prompts/help/ru/fpf-help-<area>.md`, return it, and stop. Treat that Help page as interface copy, not an FPF methodology source.
- For exact `do` after the most recent unexecuted validated FPF Plan, or for an answer to an outstanding FPF blocking question, load `prompts/fpf-manager.md` completely and resume that Plan with its retained doer, warden, per-step artifact sets, and conversation state. Never require a second `do` after a blocking answer.
- For every other invocation, load `prompts/fpf-manager.md` completely and follow it with the complete invocation. A new invocation produces a Plan by default, including when it starts with one command or an explicit `+` stack. Direct execution is allowed only when the operator explicitly asks to proceed without a Plan. The manager delegates candidate production to one resumable doer and exact-result validation to one independent warden before releasing or persisting anything.

Never load `prompts/fpf-manager.md` for a fast Help call. Never load either Help file for a non-Help call unless the delegated runtime routes there.
