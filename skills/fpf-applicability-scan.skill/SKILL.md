---
name: fpf-applicability-scan
description: Identify which First Principles Framework (FPF) patterns are relevant to one bounded question without reading the full methodology. Locate and use an accessible FPF source without assuming its path, storage, operating system, tools, repository layout, or user setup. Use when the user asks what FPF can contribute, which FPF ideas or patterns fit, what to borrow from FPF, or whether FPF is applicable to a proposal, document, policy, workflow, model, system, or other target.
---

# FPF Applicability Scan

<!-- output-settings:start -->
## Output language settings

This package's build-time defaults are `output_style = "general"` and `fpf_terms_explained = "off"`. An explicit user request for a result overrides these embedded defaults.

Apply this contract to the result narrative. Keep exact FPF locators and source paths in compact evidence or source records, not in narrative prose.

- `natural` uses unredacted natural FPF result language and may use FPF terms. In this mode only, `fpf_terms_explained = "full"` explains each FPF term on first use in at most three short lines; `short` uses one brief clause or sentence (about half to one line); and `off` adds no explanation.
- `general` uses no FPF terms in the narrative. Use ordinary-language synonyms instead. The explanation setting is ignored.
- `ste` uses no FPF terms in the narrative. Use simplified synonyms and an ASD-STE100 Issue 9-inspired overlay: short clear sentences, one topic per sentence, active voice where practical, and vertical lists for complex text. This is guidance only and makes no formal-conformance claim. The explanation setting is ignored.
<!-- output-settings:end -->

Produce a read-only **Pattern Applicability Finding**. Stop at a bounded recommendation; do not redesign the target or authorize changes.

## Resolve sources

1. Resolve the target and its current authority from the user request and accessible context. Do not assume a repository, Git, an artifact schema, or named layers.
2. Resolve an accessible FPF edition in this order: a source named in the request; a path, URI, attachment, corpus, or connected item already in context; an optional environment or workspace hint; then a bounded search of accessible workspace or storage roots. Treat configuration hints as optional, never required.
3. Verify candidates by content, not container name. A usable source must identify itself as FPF and expose navigable direct patterns with the relevant Problem frame, Problem, Forces, Solution, and Consequences; practical-use cards, usage guidance, hubs, contents, and indexes are supporting landmarks.
4. Do not require a particular environment variable, directory or repository name, application, version-control system, home-directory layout, shell, local filesystem, or operating system. Use the discovery and retrieval capabilities available in the current runtime.
5. Search only accessible, task-relevant roots or providers; never scan an entire device, account, or network. If several editions remain plausible and the choice affects the finding, ask the user which is authoritative. If none can be verified, report what was checked and request a path, URI, attachment, corpus, or connected source.
6. Never load a monolithic or explicitly unsafe/oversized FPF source wholesale. Use split or indexed pages or targeted section retrieval. If the runtime can only load the entire oversized source, request another accessible representation. Keep the resolved source locator task-local; never persist a discovered user-specific location into this reusable skill.

## Scan workflow

1. State the current question, Entity of Concern, bounded context, and receiving use.
2. Route from the resolved edition's Practical-Use Cards entry point or its equivalent. Use its usage guide, table of contents, hubs, and term/relation indexes only to locate direct patterns.
3. Compare plausible cards by situation, exact first-result difference, and stop/return conditions. A card or pattern-family name alone is not a finding.
4. Inspect each selected direct pattern's Problem frame, Problem, Forces, Solution, Consequences, and ordinary boundary.
5. Use six direct-pattern pages as the default retrieval budget. Entry pages and index searches do not count. If the budget cannot support a claim, return `insufficient basis` and name the exact additional pages or project evidence needed; do not broaden silently.
6. Recommend only the smallest useful set of direct patterns. Do not create an ordered whole-project FPF program unless the receiving use requires one.

## Optional delegated work

Delegation must not change the required result. Resource or retrieval limits alone do not justify cancellation, replacement, or duplicate work. Pending work may remain pending while only non-conflicting work continues. Stop it only for user cancellation or override, or a confirmed safety or protected-scope violation. If delegation is unavailable, execute directly.

## Per-candidate record

For every candidate, record:

- project question and target claim;
- Entity of Concern and bounded context;
- selected practical-use card;
- direct pattern, source edition, stable locator, and inspected Solution;
- expected first useful result and receiving use;
- project evidence and direct FPF basis;
- reviewer inference, if any;
- applicability: `applicable`, `not applicable`, or `insufficient basis`;
- stop/return condition and exact next source when applicable.

Use stable citations appropriate to the source, such as file-and-line, URI-and-section, attachment, corpus, or connected-item locators. A citation is a pointer, not a substitute for the applicability record.

## Boundaries

- Keep FPF recommendation separate from project authority and operator decisions.
- Label direct FPF claims, project evidence, reviewer inference, and operator decisions distinctly.
- Apply only lenses selected by the current question; do not run ontological, assurance, lifecycle, or other checks as universal rituals.
- Remain layer-agnostic: discover the requested scope at runtime and treat a named layer, several layers, or a layerless target identically.
- Remain read-only unless the user separately authorizes implementation.

## Output

Return the complete listed artifact with every required section and evidence record, including any optional delegated work. Do not replace it with a summary, abbreviated surrogate, or pointer to another result.

### Required result envelope

Organize the complete native artifact under exactly these four top-level Markdown headings, in this order:

1. `## Task, scope, and boundaries`
2. `## High-confidence results (>=95%)`
3. `## Open questions (confidence <95%)`
4. `## Skills used`

In section 1, state the task and receiving use, target and current state, scope and exclusions, inputs, sources and evidence, authority, dependencies, and stop condition. In sections 2 and 3, keep every native requirement below as a subsection or item; do not omit, merge away, or summarize it.

In section 4, list every skill actually executed for this result in execution order, using its exact canonical skill ID, and state each skill's role in one concise sentence. Do not list tools, the base model, or merely proposed or recommended downstream skills as used. If no other skill was executed, list only `fpf-applicability-scan`.

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

1. **Question, scope, and resolved FPF source**
2. **Pattern Applicability Findings**
3. **Recommended smallest set**
4. **Excluded or unchecked claims**
5. **Stop/return condition**

Do not claim that FPF made, approved, or authorized a project decision.
