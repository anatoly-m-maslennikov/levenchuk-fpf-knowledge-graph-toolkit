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
4. Make dependencies, parallel calls, decision ownership, missing inputs, and stop conditions explicit.
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
- Mark calls as parallel only when neither consumes the other's output. Name the join artifact required by the next step.
- End at the user's receiving use. Present later steps only as conditional follow-ups.

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

Return:

1. **Question and routing assumptions**
2. **Proposed sequence**, using `$fpf-...` invocation names
3. **Copy-ready task for each call**
4. **Inputs, handoffs, parallel joins, and run conditions**
5. **Skipped skills and why**
6. **Execution boundary** — state that no proposed skill was executed
