# `$fpf` help

`$fpf` is one skill backed by a graph of lazily loaded prompts. Give it a direct command or a natural-language task.

English and Russian routing are supported. Canonical command identifiers remain English; `$fpf справка` opens the Russian help page.

## Command tree

```text
$fpf
├── help                  show this page; never saves
├── plan                  return a call plan only; never executes or saves
├── applicability scan    find relevant FPF patterns
├── sota harvest           build a bounded current evidence map
├── options explore        generate and compare alternatives
├── design challenge       challenge a proposal before implementation
├── decision synthesize    choose among evaluated alternatives and project an ADR
├── quality improve        change and re-evaluate a versioned target
└── alignment audit        audit implemented or accepted work
```

The seven analytical commands return their complete artifact in chat and save a report by default. `$fpf help` and `$fpf plan` never save.

Direct analytical commands are `$fpf applicability scan`, `$fpf sota harvest`, `$fpf options explore`, `$fpf design challenge`, `$fpf decision synthesize`, `$fpf quality improve`, and `$fpf alignment audit`.

## Stack analytical commands

Use ` + ` with spaces to request one explicit ordered composition:

`$fpf design challenge + quality improve + alignment audit Strengthen this versioned proposal.`

Put the shared task only after the last command. Every adjacent pair must be a legal graph handoff. The run uses one campaign, one finding registry, and one final report. It stops at missing evidence, decision, or mutation-authority gates instead of inventing permission or repeatedly restarting review.

The final artifact contains one deduplicated list of every issue and weak point found within the declared scope and evaluation profile, plus one ordered fixes and improvements list mapped back to those findings. Intermediate commands do not save separate reports.

## Examples

- `$fpf help`
- `$fpf plan We need current research, options, and an owner decision.`
- `$fpf design challenge Review this proposed scope model before implementation.`
- `$fpf design challenge + quality improve Strengthen this versioned proposal.`
- `$fpf design challenge + quality improve + alignment audit Repair and verify this versioned proposal.`
- `$fpf alignment audit Verify the accepted repairs against the registered findings.`
- `$fpf Which FPF patterns are relevant to this bounded service-design question?`

Use `$fpf plan` when you want the workflow but do not want any analytical prompt executed. For a direct command, the text after the command is passed to that prompt as its task. In a composition, task text belongs only after the final command.

## Report modes

FPF works standalone by default. The installer-managed `.fpf-runtime.toml` records the absolute local toolkit-repository path and defaults to `save_report = "on"` with `report_style = "plain"`; no CAPRMEDIO installation or project is required. An optional active-project `.caprmedio/settings.toml` or an explicit user instruction can select `report_style = "caprmedio"`, with the explicit instruction taking priority. CAPRMEDIO mode creates a non-normative Analysis Report Atom in the narrowest proven Scope Unit that contains the analysis scope. It fails closed when topology or Atom admission rules cannot be resolved.

## Output language

The default `output_language = "auto"` selects Russian when the invocation or residual task contains meaningful Russian Cyrillic text and English otherwise. `ru` and `en` fix the language. Exact commands, FPF IDs and locators, source paths, code, direct quotations, URLs, and citation targets are not translated.

Canonical Codex syntax is `$fpf`. The resolver also understands a textual `/fpf` prefix when another host passes it through, but this does not register a native custom slash command.
