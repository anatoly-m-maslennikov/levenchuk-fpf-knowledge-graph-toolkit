---
name: fpf-quality-improve
description: Define and run a bounded quality-improvement loop for a versioned target using First Principles Framework (FPF) evidence without reading the full methodology. Locate FPF without assuming the user's storage, tools, operating system, repository layout, or setup. Use when the user asks to improve an artifact, policy, workflow, method, model, organization, service, harness, framework, or other target while preserving trade-offs, rerunning evaluation, and distinguishing real result change from activity or repeated testing.
---

# FPF Quality Improve

Produce a **Quality Improvement Loop Record** for one target version under one declared evaluation frame. Improvement requires a target change and a demonstrated declared-coordinate result change.

## Resolve scope and FPF source

1. Resolve the target identity and version, Entity of Concern, current state, evaluation frame, quality coordinates, receiving use, authority, evidence, protected trade-offs, cost/risk account, and allowed change surface.
2. Resolve an accessible FPF edition from a user-supplied path, URI, attachment, corpus, connected item, optional runtime hint, or bounded search of accessible task-relevant roots. Verify candidates by FPF identity and navigable direct patterns, not container names.
3. Locate `Quality Improvement Loop Method` by title and content. Inspect its Problem frame, Problem, Forces, Solution, Consequences, and ordinary boundary. Use practical-use cards, contents, hubs, and indexes only for routing.
4. Never load the full methodology or an oversized source wholesale. Use targeted sections. Use six direct-pattern pages as the default ceiling; entry and index pages do not count.
5. Keep the source locator task-local and cite stable FPF, target, and evaluation evidence. If target identity, baseline, or rerunnable evaluation is missing, return `insufficient basis` and name the exact prerequisite.

## Define the loop contract

Record:

- target version and bounded change surface;
- baseline evaluation and declared quality-result coordinates;
- protected trade-offs and refusal conditions;
- intended result change and receiving use;
- cost, risk, reversibility, evidence, and uncertainty;
- stop, continue, rollback, and method-switch criteria.

## Workflow

1. Run or recover the baseline evaluation before proposing improvement. Separate evaluation evidence from reviewer inference.
2. Select one bounded change hypothesis tied to an intended declared-coordinate result change. Preserve target identity and create a new recoverable version when the change is applied.
3. Apply changes only when authorized. Record actual affected carriers and implementation evidence; activity alone is not a changed target version.
4. Rerun the same evaluation or a justified compatible revision. Compare results in the declared coordinates and expose uncertainty, regressions, displaced costs, and protected-trade-off effects.
5. Record the outcome as improved, not demonstrated, regressed, or insufficient basis within the bounded frame. Use the declared criteria to stop, continue, rollback, or switch method.

## Boundaries

- Retrying a process, rerunning a harness, producing more text, or changing an evaluation without changing the target does not establish improvement.
- A cleaner diff, passing test, or favorable proxy does not establish semantic quality unless it is part of the declared result coordinates.
- Do not optimize one coordinate by silently externalizing cost or damaging protected trade-offs.
- Remain layer-agnostic and artifact-agnostic. Remain read-only unless the user authorizes target changes.

## Optional delegated work

Delegation must not change the required result. Resource or retrieval limits alone do not justify cancellation, replacement, or duplicate work. Pending work may remain pending while only non-conflicting work continues. Stop it only for user cancellation or override, or a confirmed safety or protected-scope violation. If delegation is unavailable, execute directly.

## Output

Return the complete listed artifact with every required section and evidence record, including any optional delegated work. Do not replace it with a summary, abbreviated surrogate, or pointer to another result.

### Required result envelope

Organize the complete native artifact under exactly these four top-level Markdown headings, in this order:

1. `## Task, scope, and boundaries`
2. `## High-confidence results (>=95%)`
3. `## Open questions (confidence <95%)`
4. `## Skills used`

In section 1, state the task and receiving use, target and current state, scope and exclusions, inputs, sources and evidence, authority, dependencies, and stop condition. In sections 2 and 3, keep every native requirement below as a subsection or item; do not omit, merge away, or summarize it.

In section 4, list every skill actually executed for this result in execution order, using its exact canonical skill ID, and state each skill's role in one concise sentence. Do not list tools, the base model, or merely proposed or recommended downstream skills as used. If no other skill was executed, list only `fpf-quality-improve`.

Immediately after the skill list in section 4, add this compact Markdown subsection:

#### FPF sources consulted (N read; M used)

- `FPF-Knowledge-Graph/<relative-path>.md` — **used**: <brief evidence role>
- `FPF-Knowledge-Graph/<relative-path>.md` — **screened only**

List every FPF source document actually opened exactly once. **Used** means it materially supports a result; **screened only** means it was read but not relied on. Do not list merely discovered-but-unopened files, project evidence, tools, or absolute machine paths. Prefer `FPF-Knowledge-Graph/...` graph-root-relative paths; for a non-file-backed FPF edition, use a stable URI or item identifier.

Assign confidence to each material result and state its evidence basis. Confidence is the reviewer's claim-level epistemic confidence under the available evidence, not a statistical probability, artifact-wide score, importance, severity, authorization, acceptance, assurance, or gate result. Use these bands inside section 3:

- **90–94%:** probable answer, but confirmation is still needed.
- **Below 90%:** materially uncertain.

Never round up to 95%, hide conflicting, unsupported, or insufficient-basis results, or omit a lower-confidence finding. For each open question include the best current answer, confidence band or value, missing evidence or input, consequence, and exact next evidence or action. A high-confidence determination that the basis is insufficient belongs in section 2; the unresolved substantive question belongs in section 3. If no open questions remain, keep section 3 and write `None identified within the declared scope`.

Preserve these native artifact requirements:

1. **Loop contract and resolved FPF source**
2. **Baseline target version and evaluation**
3. **Bounded change hypothesis and implementation evidence**
4. **Re-evaluation and declared-coordinate comparison**
5. **Trade-offs, costs, risks, and uncertainty**
6. **Outcome and stop/continue/rollback/switch decision**
