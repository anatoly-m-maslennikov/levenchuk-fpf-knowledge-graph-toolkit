---
name: fpf-options-explore
description: Generate and compare diverse candidate options with bounded First Principles Framework (FPF) evidence without reading the full methodology. Locate FPF without assuming the user's storage, tools, operating system, repository layout, or setup. Use when the user asks for non-obvious or interesting solutions, NQD exploration, OEE/QD parity, alternative generation before a decision or ADR, or comparison of method families without prematurely selecting one winner.
---

# FPF Options Explore

Produce a read-only **Candidate Exploration Pack**. Generate and compare options; do not make the receiving project decision.

## Resolve scope and FPF source

1. Resolve the question, Entity of Concern, bounded context, receiving use, evaluator, and decision owner from the request and accessible evidence.
2. Resolve an accessible FPF edition from a user-supplied path, URI, attachment, corpus, connected item, optional runtime hint, or bounded search of accessible task-relevant roots. Verify candidates by FPF identity and navigable direct patterns, not container names.
3. Locate direct patterns by title and content. Inspect `Creative Abduction with NQD`; inspect `Parity and Benchmark Harness` only when method-family or OEE/QD comparison is required. Read their Problem frame, Problem, Forces, Solution, Consequences, and ordinary boundary.
4. Never load the full methodology or an oversized source wholesale. Use entry/index pages and targeted sections. Use six direct-pattern pages as the default ceiling; entry and index pages do not count.
5. Keep the source locator task-local. Cite it with the most stable available file, URI, attachment, corpus, or connected-item locator. If no edition can be verified, return `insufficient basis` and state what source is required.

## Define the exploration contract

Before generating options, record:

- the question, scope, baseline, and receiving use;
- what counts as interesting, for whom, and relative to which familiar options;
- declared quality measures and protected constraints;
- novelty and diversity axes, admissible risk, cost, reversibility, and time horizon;
- evidence inputs, exploration budget, policy pins, and stop criteria.

If “interesting” remains undefined, ask for the missing distinctions or return `insufficient basis`; do not substitute an internet-average preference.

## Workflow

1. Generate a provenance-bearing `CandidateSet` using NQD-guided creative abduction. Keep hypotheses explicitly abductive.
2. Evaluate candidates only in the declared quality coordinates. Preserve useful diversity, archive state, and the applicable decision/reasoning record.
3. Treat novelty, diversity, illumination, coverage, and regret as telemetry unless the exploration contract explicitly promotes one into a decision criterion.
4. When comparison is requested, pin the baseline, comparator edition, freshness window, normalization or bridge rules, and policy. Produce `ParityPlan@Context` before `ParityReport@Context`.
5. Return the candidate set, Pareto front when justified, retained alternatives, evidence gaps, and handoff requirements. Do not silently collapse several measures into one opaque score.

## Boundaries

- Do not claim that a novel candidate is superior, selected, approved, or implementable.
- Do not manufacture diversity through cosmetic wording; distinguish candidates by declared mechanisms, structures, or trade-offs.
- Route an actual selection and ADR request to `fpf-decision-synthesize` after candidates have recoverable evaluation evidence.
- Remain layer-agnostic and artifact-agnostic. Remain read-only unless the user separately authorizes implementation or file writes.

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

In section 4, list every skill actually executed for this result in execution order, using its exact canonical skill ID, and state each skill's role in one concise sentence. Do not list tools, the base model, or merely proposed or recommended downstream skills as used. If no other skill was executed, list only `fpf-options-explore`.

Immediately after the skill list in section 4, add this compact source disclosure:

<details>
<summary>FPF sources consulted (N read; M used)</summary>

- `FPF-Knowledge-Graph/<relative-path>.md` — **used**: <brief evidence role>
- `FPF-Knowledge-Graph/<relative-path>.md` — **screened only**

</details>

List every FPF source document actually opened exactly once. **Used** means it materially supports a result; **screened only** means it was read but not relied on. Do not list merely discovered-but-unopened files, project evidence, tools, or absolute machine paths. Prefer `FPF-Knowledge-Graph/...` graph-root-relative paths; for a non-file-backed FPF edition, use a stable URI or item identifier. If the renderer does not support `<details>`, show the same compact list without the wrapper.

Assign confidence to each material result and state its evidence basis. Confidence is the reviewer's claim-level epistemic confidence under the available evidence, not a statistical probability, artifact-wide score, importance, severity, authorization, acceptance, assurance, or gate result. Use these bands inside section 3:

- **90–94%:** probable answer, but confirmation is still needed.
- **Below 90%:** materially uncertain.

Never round up to 95%, hide conflicting, unsupported, or insufficient-basis results, or omit a lower-confidence finding. For each open question include the best current answer, confidence band or value, missing evidence or input, consequence, and exact next evidence or action. A high-confidence determination that the basis is insufficient belongs in section 2; the unresolved substantive question belongs in section 3. If no open questions remain, keep section 3 and write `None identified within the declared scope`.

Preserve these native artifact requirements:

1. **Exploration contract and resolved FPF source**
2. **CandidateSet and provenance**
3. **Declared-coordinate evaluation and diversity map**
4. **Parity plan/report**, when applicable
5. **Retained options, exclusions, and evidence gaps**
6. **Stop condition and decision handoff**
