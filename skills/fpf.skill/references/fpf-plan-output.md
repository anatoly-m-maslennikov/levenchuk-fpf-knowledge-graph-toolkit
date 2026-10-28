# FPF Plan Output Finalizer

Load this file after `prompts/fpf-plan.md` and after all routing decisions are complete. It is the final authority for Plan response shape. Do not execute a proposed step, inspect FPF methodology, save a report, emit an issue/fix registry, or include copy-ready invocation boilerplate.

Return exactly one compact numbered Plan:

```markdown
# Proposed plan

1. **`$fpf <canonical command>`** - <concise action, inputs, boundary, expected result, and stop condition>.
2. **`$fpf <canonical command>`** - <concise action>; uses the complete validated result of step 1 as <named handoff>.
3. **`$fpf <canonical command>`** - <concise action>; uses the complete validated result of step 2 as <named handoff>.

Reply `do` to execute this plan.
```

Use one to the smallest useful number of steps. Number every step once in execution order. Preserve exact canonical command identifiers with spaces. Each step must state enough target, scope, input, result, dependency, authority, and stop information to execute safely, but remain one compact list item. Step N after the first explicitly names the result inherited from step N-1. The default blocking-decision threshold is 95% and is omitted from the compact Plan; when the operator overrides it, append `blocking threshold: <value>% (operator override)` to step 1.

Do not add “High-confidence results,” “Proposed sequence,” “Copy-ready task,” the old four-section Plan envelope, a separate skills list, or a copied composition command. Routing details live in metadata unless a correction, unresolved choice, gate, or stop must be visible to the operator.

If a route-affecting question prevents a safe executable Plan, replace the affected step with two or three canonical variants and their impacts; do not tell the operator to reply `do` until the Plan is unambiguous. A merely lower-confidence analytical finding is not a Plan question.

The final line is exactly `Reply \`do\` to execute this plan.` only when every numbered step is executable. It means the proposed analytical nodes have not run, FPF methodology sources were not consulted, no report was saved, and exact `do` will approve only this most recent Plan.

Before writing `candidate.md`, verify: the only top-level heading is `Proposed plan`; the body is one ordered list; every command is canonical; every later step names its inherited prior result; any non-default threshold is visible in step 1 and matches metadata; there is no copy-ready invocation; `commands_executed` contains only `$fpf plan`; methodology sources are empty; persistence is off; and the approval line is present only for an executable Plan.
