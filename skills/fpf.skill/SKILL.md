---
name: fpf
description: Route and run one command or an explicit + composition through the repository's First Principles Framework (FPF) prompt graph. Use when the user invokes $fpf, asks for FPF help or planning, or wants an applicability scan, SoTA harvest, option exploration, design challenge, decision synthesis, quality improvement, or alignment audit.
---

# FPF

Treat this package as a lazy-loaded prompt graph. Do not preload every prompt.

## Resolve the node or composition

1. Pass the complete invocation text to `scripts/route_fpf.py` when local script execution is available:

   `python3 <this-skill-directory>/scripts/route_fpf.py --text "<complete invocation>"`

2. For a single-node result, use the returned `prompt` path relative to this skill directory. If script execution is unavailable, reproduce the same precedence from `graph.json`: explicit composition first, longest exact command or alias next, then keyword score, then `plan` as the safe fallback.
3. Preserve the returned residual `task`; it is the input to the selected prompt.

If the router returns `composition_error`, pass it to `$fpf plan` with the original task so the plan can explain the invalid handoff and the smallest legal correction.

Canonical invocation is `$fpf`. A textual `/fpf` prefix is accepted by the resolver for portability, but a Codex skill is invoked as `$fpf`.

## Execute the resolved mode

For `mode: composition`, load `references/composition.md` completely. Execute only the returned ordered `nodes`, lazily loading one prompt at a time. Share one campaign and finding registry, stop at unmet authority or evidence gates, and return and persist one consolidated artifact with every in-scope issue or weakness plus one mapped fixes and improvements list. Do not emit or save separate intermediate node reports.

For a single-node result:

- `help`: load `prompts/help.md`, return its help page, and stop. Never save a report.
- `plan`: load `prompts/plan.md`, produce only the call plan, and stop. Do not execute proposed nodes and never save a report.
- Any analytical node: load only its returned prompt, execute that contract on the residual task, and follow its output and report settings.

The seven analytical prompts may refer to shared files under `references/`. Load a referenced file only when its prompt says to do so. In particular, load `references/report-persistence.md` only after report saving resolves to on; load the CAPRMEDIO adapter only when the selected report style is `caprmedio`.

Do not treat a graph edge as permission to execute another node. Edges are legal handoffs for `$fpf plan` and validators for an explicit `+` composition. A direct analytical call still executes one node unless the user explicitly composes commands.

## Maintainer checks

After changing the graph, prompts, aliases, or help page, run:

`python3 <this-skill-directory>/scripts/route_fpf.py --check`

`python3 -m unittest discover -s <this-skill-directory>/scripts/tests -p 'test_*.py'`
