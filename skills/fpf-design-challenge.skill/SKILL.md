---
name: fpf-design-challenge
description: Challenge one proposed or not-yet-implemented design with a bounded, evidence-backed First Principles Framework (FPF) review. Locate and use an accessible FPF source without assuming its path, storage, operating system, tools, repository layout, or user setup. Use when the user asks to review, critique, test, discuss, or reconsider a proposal, taxonomy, architecture, policy, workflow, model, role system, specification, or decision with FPF before treating it as accepted project authority.
---

# FPF Design Challenge

Produce a read-only **FPF Challenge Finding**. Challenge the current proposal without letting FPF impersonate the project's decision authority.

## Resolve scope and sources

1. Resolve the proposal, its intended effect, the current project authority, and the actual decision owner from the request and accessible context. Do not assume named layers, repository structure, Git, software artifacts, or a particular governance model.
2. Resolve an accessible FPF edition in this order: a source named in the request; a path, URI, attachment, corpus, or connected item already in context; an optional environment or workspace hint; then a bounded search of accessible workspace or storage roots. Treat configuration hints as optional, never required.
3. Verify candidates by content, not container name. A usable source must identify itself as FPF and expose navigable direct patterns with the relevant Problem frame, Problem, Forces, Solution, and Consequences; practical-use cards, usage guidance, hubs, contents, and indexes are supporting landmarks.
4. Do not require a particular environment variable, directory or repository name, application, version-control system, home-directory layout, shell, local filesystem, or operating system. Use the discovery and retrieval capabilities available in the current runtime.
5. Search only accessible, task-relevant roots or providers; never scan an entire device, account, or network. If several editions remain plausible and the choice affects the finding, ask the user which is authoritative. If none can be verified, report what was checked and request a path, URI, attachment, corpus, or connected source.
6. Never load a monolithic or explicitly unsafe/oversized FPF source wholesale. Use split or indexed pages or targeted section retrieval. If the runtime can only load the entire oversized source, request another accessible representation. Keep the resolved source locator task-local; never persist a discovered user-specific location into this reusable skill.
7. If the design is already implemented and the receiving use is final verification, stop and recommend `fpf-alignment-audit` instead.

## Challenge workflow

1. State the proposal claim, Entity of Concern, bounded context, intended result, receiving use, and decision owner.
2. Route from the relevant practical-use card to direct patterns. Inspect each selected pattern's Problem frame, Problem, Forces, Solution, Consequences, and ordinary boundary.
3. Select lenses from the proposal's actual uncertainty. Possible lenses include category boundaries, independent classification axes, Entity-versus-description/work/evidence distinctions, context and applicability, ontological parsimony, claim ownership, relation signatures, dependency direction, assurance, lifecycle, or compatibility. Never run the list mechanically.
4. Use six direct-pattern pages as the default retrieval budget. Entry pages and index searches do not count. If the budget cannot support a claim, return `insufficient basis` with the exact additional pages or project evidence needed; do not broaden silently.
5. Test whether the proposal preserves the target's stated distinctions, avoids hidden conflation, names its scope, and returns authority-bearing questions to the project decision owner.
6. Stop at the smallest challenge finding that makes the decision reviewable. Return when the proposal, context, evidence basis, governing pattern, or receiving use changes.

## Optional delegated work

Delegation must not change the required result. Resource or retrieval limits alone do not justify cancellation, replacement, or duplicate work. Pending work may remain pending while only non-conflicting work continues. Stop it only for user cancellation or override, or a confirmed safety or protected-scope violation. If delegation is unavailable, execute directly.

## Finding contract

Use only these FPF result states:

- `concern`;
- `no concern found within inspected scope`;
- `FPF not decisive`;
- `insufficient basis`.

For every finding, record:

- proposal claim and affected Entity of Concern;
- bounded context and receiving use;
- direct FPF pattern, source edition, stable locator, and inspected Solution;
- project evidence and direct FPF basis;
- reviewer inference, explicitly labeled;
- consequence if the concern remains unresolved;
- candidate correction or alternative, when supported;
- unchecked dependencies and stop/return condition.

Use stable citations appropriate to the source, such as file-and-line, URI-and-section, attachment, corpus, or connected-item locators. A citation is a pointer, not a substitute for the finding record.

## Authority boundary

- Do not return `adopt`, `revise`, `reject`, `approved`, or `blocked` as if FPF made the project decision.
- If the user requests a project disposition, place it in a separate **Project decision** section and identify its owner and basis.
- Keep direct FPF claims, project evidence, reviewer inference, and operator decisions distinct.
- Remain layer-agnostic: discover the target boundary at runtime and apply the same method to a layer, cross-layer design, or layerless target.
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

In section 4, list every skill actually executed for this result in execution order, using its exact canonical skill ID, and state each skill's role in one concise sentence. Do not list tools, the base model, or merely proposed or recommended downstream skills as used. If no other skill was executed, list only `fpf-design-challenge`.

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

1. **Proposal, resolved FPF source, and decision boundary**
2. **FPF Challenge Findings**, ordered by consequence
3. **Strengths within inspected scope**
4. **Unchecked claims and insufficient basis**
5. **Return to project authority**

Do not convert an FPF recommendation into authorization, assurance, or a gate result.
