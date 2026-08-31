# FPF Plan Output Finalizer

Load this file after `prompts/fpf-plan.md` and after all routing decisions are complete. It is the final authority for Plan response shape. Do not execute a proposed call, inspect FPF methodology, save a report, or emit an issue/fix registry.

Start the response at the first heading below. Use these four canonical heading names exactly once and in this order at one consistent top level. That top level may be Markdown `#` or `##`; nested headings must be deeper.

## Task, scope, and boundaries

State the task and receiving use, target and current state, scope and exclusions, inputs, routing evidence, authority, dependencies, and overall stop condition.

## Routing decisions and recommendations

For every proposed call, include one record with: exact canonical `$fpf <command>`; target and purpose; prerequisites and inputs; prior handoff; expected native artifact or join artifact; selection and skipped-route basis; **Routing confidence** with concrete routing evidence; and run, stop, and authority conditions.

For every handoff, include a separate record with: producer and consumer canonical commands; transferred evidence; required graph edge and gate; **Routing confidence** with concrete routing evidence; and the exact stop or confirmation condition. Never label this field only `Handoff confidence`.

When two or more nodes form one requested stack, include one copy-ready composition using exact canonical commands and the complete shared task. For ambiguous intent, propose only exact canonical alternatives from the command graph; never emit a generic `$fpf <prose task>` call.

Preserve the native Plan requirements: routing assumptions, proposed sequence, copy-ready task for each call, inputs and handoffs, independent calls and joins, skipped skills, and the explicit statement that no proposed analytical node executed.

## Unresolved evidence gaps

List only missing evidence or unanswered routing questions that can change the route. For each, state consequence, exact evidence or decision needed, owner when known, and affected proposed calls. Otherwise write `None identified within the declared scope`.

## Skills used

List exactly `$fpf plan` and its routing role. Do not list proposed downstream commands, even when marked proposed.

### Routing basis and FPF methodology sources

- **Routing basis used:** the embedded command graph, skill catalog, selection rules, and sequencing rules.
- **FPF methodology sources:** not applicable; Plan opens no FPF methodology page and makes no methodology claim.

Before returning, verify that the only top-level heading names are the four above and their depth is consistent; every call and every handoff says **Routing confidence** and gives concrete evidence; every proposed command is canonical; `commands_executed` can contain only `$fpf plan`; methodology sources are empty; and `report_saved` is false.
