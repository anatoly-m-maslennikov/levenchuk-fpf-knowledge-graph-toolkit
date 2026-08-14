---
name: fpf-route
description: Route one question into the smallest useful ordered sequence of existing First Principles Framework (FPF) skills and rewrite it into a precise task for each call. Use when the user asks which FPF skill to use, wants an FPF workflow or skill chain, provides a broad question that may need several fpf-* skills, or invokes fpf or fpf-route for planning. Return a call plan only; do not execute the selected skills unless separately asked.
---

# FPF Route

Produce a read-only **FPF Skill Route** for one question. Route work among the available FPF skills; do not answer the question, inspect the FPF methodology, or execute the proposed calls.

## Route contract

1. Restate the question as one bounded receiving use. Identify the target state: open question, research need, proposal, evaluated alternatives, versioned improvement target, or implemented/accepted work.
2. Resolve the smallest useful sequence from the available skills. One call is a valid sequence. Do not propose a full lifecycle when the requested result stops earlier.
3. Rewrite every call as a self-contained, copy-ready task. Preserve the user's intent without embedding an expected finding, preferred option, or approval outcome.
4. Make dependencies, independent calls, decision ownership, missing inputs, and stop conditions explicit. The active runtime chooses scheduling.
5. If no available FPF skill fits, return no call and explain which required trigger or input is absent. Never route to `fpf-route` recursively.

## Skill selection

| Skill | Select when the next required result is |
|---|---|
| `fpf-applicability-scan` | The smallest relevant set of direct FPF patterns for a bounded question |
| `fpf-sota-harvest` | A current, reconstructible, plural field or evidence map |
| `fpf-options-explore` | Diverse candidate options and declared-coordinate comparison without selection |
| `fpf-design-challenge` | A bounded challenge of a proposed or not-yet-implemented design |
| `fpf-decision-synthesize` | A recoverable choice among already evaluated alternatives and, when requested, its ADR projection |
| `fpf-quality-improve` | A versioned target-change and re-evaluation loop under declared quality coordinates |
| `fpf-alignment-audit` | A bounded audit of implemented or accepted work against relevant FPF patterns |

## Sequencing rules

- Order calls by evidence dependency, not by the table order.
- Use `fpf-applicability-scan` first only when FPF relevance or direct-pattern selection is genuinely unresolved. Do not add it merely because the question mentions FPF.
- Put `fpf-sota-harvest` before option generation only when current external evidence or rival traditions are needed.
- Put `fpf-options-explore` before `fpf-decision-synthesize`; never ask decision synthesis to invent unevaluated alternatives.
- Put `fpf-design-challenge` before a decision when a concrete unimplemented proposal needs stress-testing. Route implemented work to `fpf-alignment-audit` instead.
- Use `fpf-decision-synthesize` only when alternatives, evaluation evidence, and project decision authority are recoverable. Otherwise name the missing prerequisite.
- Use `fpf-quality-improve` directly when a versioned target, baseline, evaluation frame, and allowed change surface exist. Do not prepend an alignment audit unless FPF alignment is itself a required baseline claim.
- Put `fpf-alignment-audit` after implementation or acceptance, never as approval for a proposal.
- Mark calls as independent only when neither consumes the other's output. Name the required handoff or join artifact for the next step; the active runtime chooses scheduling.
- End at the user's receiving use. Present later steps only as conditional follow-ups.

## Maintainer evaluation

`references/routing-scenarios.json` is the repository's behavioral scenario matrix. It is test evidence for maintainers, not required runtime context. When changing routing rules or the skill catalog, update the matrix and run `python3 scripts/validate_repository.py`.

## Address each task

For every proposed call, write an imperative task that includes:

- the target or claim and its current state;
- bounded context and intended receiving use;
- available input artifacts and the exact prior-step handoff, if any;
- project authority or decision owner when relevant;
- the selected skill's native result;
- explicit exclusions and the stop or return condition.

Do not use vague tasks such as “apply FPF” or “review everything.” Do not ask a skill to make an authorization, assurance, gate, or project decision outside its own contract.

## Output

Return the complete listed artifact with every required section and evidence record, including any optional delegated work. Do not replace it with a summary, abbreviated surrogate, or pointer to another result.

Use ordinary Markdown headings and lists. Do not wrap the artifact or any section in a fenced code block.

### Required result envelope

Organize the complete native artifact under exactly these four top-level Markdown headings, in this order:

1. `## Task, scope, and boundaries`
2. `## High-confidence results (>=95%)`
3. `## Open questions (confidence <95%)`
4. `## Skills used`

In section 1, state the task and receiving use, target and current state, scope and exclusions, inputs, sources and evidence, authority, dependencies, and stop condition. In sections 2 and 3, keep every native requirement below as a subsection or item; do not omit, merge away, or summarize it.

In section 4, list every skill actually executed for this result in execution order, using its exact canonical skill ID, and state each skill's role in one concise sentence. Do not list tools, the base model, or merely proposed or recommended downstream skills as used. If no other skill was executed, list only `fpf-route`; skills in the proposed sequence remain recommendations, not executed skills.

Immediately after the skill list in section 4, add this compact routing-basis disclosure:

<details>
<summary>Routing basis and FPF methodology sources</summary>

- **Routing basis used:** the embedded skill catalog, selection rules, and sequencing rules in `fpf-route`.
- **FPF methodology sources:** not applicable. The router neither opens the FPF knowledge graph nor makes methodology claims. Each downstream skill reports its own FPF sources when executed.

</details>

If the renderer does not support `<details>`, show the same disclosure without the wrapper. Do not present an empty or zero-count FPF source trace: source accounting is not applicable to a router that makes no methodology claims. This exception applies only to `fpf-route`; every executed downstream FPF skill must list the methodology sources it actually opened and distinguish **used** from **screened only**.

Assign confidence to each material result and state its evidence basis. Confidence is the reviewer's claim-level epistemic confidence under the available evidence, not a statistical probability, artifact-wide score, importance, severity, authorization, acceptance, assurance, or gate result. Use these bands inside section 3:

- **90–94%:** probable answer, but confirmation is still needed.
- **Below 90%:** materially uncertain.

Never round up to 95%, hide conflicting, unsupported, or insufficient-basis results, or omit a lower-confidence finding. For each open question include the best current answer, confidence band or value, missing evidence or input, consequence, and exact next evidence or action. A high-confidence determination that the basis is insufficient belongs in section 2; the unresolved substantive question belongs in section 3. If no open questions remain, keep section 3 and write `None identified within the declared scope`.

Preserve these native artifact requirements:

1. **Question and routing assumptions**
2. **Proposed sequence**, using canonical `fpf-...` skill IDs
3. **Copy-ready task for each call**
4. **Inputs, handoffs, independent calls, required join artifacts, and run conditions**
5. **Skipped skills and why**
6. **Execution boundary** — state that no proposed skill was executed
