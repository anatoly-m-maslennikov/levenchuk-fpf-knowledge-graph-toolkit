---
name: fpf-alignment-audit
description: Audit implemented or accepted work against relevant First Principles Framework (FPF) patterns with bounded, replayable evidence. Locate and use an accessible FPF source without assuming its path, storage, operating system, tools, repository layout, or user setup. Use when the user asks for a final FPF review, whether decisions were applied, whether a target is FPF-aligned, whether contradictions, gaps, leftovers, dead routes, or regressions remain, or whether an implemented document, policy, workflow, model, system, or change set is coherent after revision.
---

# FPF Alignment Audit

<!-- output-settings:start -->
## Output language settings

Defaults: `output_style = "general"`; `fpf_terms_explained = "off"`. Explicit user values override them.
Load at most one mode resource:
- `natural`: load none; allow FPF terms. On first use, explain each term per `fpf_terms_explained`: `full` up to three short lines, `short` one sentence, `off` none.
- `general`: load only `fpf-route/references/output-style-general.md`.
- `ste`: load only `fpf-route/references/output-style-ste.md`.
Never preload an unselected resource. If the selected file is missing, report it; do not substitute. Keep exact FPF locators and source paths in compact evidence or source records, not narrative prose.
<!-- output-settings:end -->

Produce a read-only **Bounded Alignment Finding**. Do not turn an audit report into project assurance, authorization, or a gate decision.

## Resolve scope and sources

1. Resolve the implemented target, accepted claims, current authority, affected dependencies, and requested receiving use from the request and accessible context. Do not assume named layers, a repository layout, Git, a fixed artifact schema, or software-only evidence.
2. Resolve an accessible FPF edition in this order: a source named in the request; a path, URI, attachment, corpus, or connected item already in context; an optional environment or workspace hint; then a bounded search of accessible workspace or storage roots. Treat configuration hints as optional, never required.
3. Verify candidates by content, not container name. A usable source must identify itself as FPF and expose navigable direct patterns with the relevant Problem frame, Problem, Forces, Solution, and Consequences; practical-use cards, usage guidance, hubs, contents, and indexes are supporting landmarks.
4. Do not require a particular environment variable, directory or repository name, application, version-control system, home-directory layout, shell, local filesystem, or operating system. Use the discovery and retrieval capabilities available in the current runtime.
5. Search only accessible, task-relevant roots or providers; never scan an entire device, account, or network. If several editions remain plausible and the choice affects the finding, ask the user which is authoritative. If none can be verified, report what was checked and request a path, URI, attachment, corpus, or connected source.
6. Never load a monolithic or explicitly unsafe/oversized FPF source wholesale. Use split or indexed pages or targeted section retrieval. If the runtime can only load the entire oversized source, request another accessible representation. Keep the resolved source locator task-local; never persist a discovered user-specific location into this reusable skill.
7. If only an unimplemented proposal exists, stop and recommend `fpf-design-challenge` instead.

## Define the audit contract

Before reviewing, enumerate:

- project claims whose alignment is being tested;
- target carriers or observed states;
- authority and evidence available for each claim;
- affected dependencies, projections, interfaces, or receiving uses;
- explicit exclusions and acceptance/refusal conditions.

Do not silently turn “review everything” into an unbounded repository or methodology read. State the chosen boundary and why it is sufficient or insufficient.

## Audit workflow

1. Route each claim from the relevant practical-use card to its direct governing FPF pattern. Inspect the pattern's Problem frame, Problem, Forces, Solution, Consequences, and ordinary boundary.
2. Use six direct-pattern pages as the default retrieval budget. Entry pages and index searches do not count. A budget exhaustion produces `insufficient basis`, never a semantic pass; name the exact additional pages or project evidence needed.
3. Inspect the implemented target and only the dependencies or projections required by the enumerated claims. Mark every unavailable or uninspected dependency explicitly.
4. Separate semantic findings from structural or mechanical verification. Parsing, link resolution, tests, or clean diffs do not by themselves prove semantic alignment.
5. Apply only claim-relevant lenses. These may include identity and revision meaning, evidence versus provenance, lifecycle transitions, authority, compatibility, projection faithfulness, unresolved blockers, or recursive impact. Do not run them as a universal layer checklist.
6. Stop at the smallest bounded finding supported by recoverable FPF and project evidence. Return when the claim, context, source edition, evidence, implementation state, governing pattern, or receiving use changes.

## Optional delegated work

Delegation must not change the required result. Resource or retrieval limits alone do not justify cancellation, replacement, or duplicate work. Pending work may remain pending while only non-conflicting work continues. Stop it only for user cancellation or override, or a confirmed safety or protected-scope violation. If delegation is unavailable, execute directly.

## Per-claim replay record

For every audited claim, record:

- claim and Entity of Concern;
- bounded context and receiving use;
- implemented carrier or observed state;
- direct FPF pattern, source edition, stable locator, and inspected Solution;
- project evidence and source status;
- expected and observed result;
- semantic and mechanical findings, kept separate;
- reviewer inference, explicitly labeled;
- inspected and uninspected dependencies;
- stop/return condition and exact next source when needed.

Use stable citations appropriate to the source, such as file-and-line, URI-and-section, attachment, corpus, or connected-item locators. A citation is a pointer, not a substitute for the replay record.

## Verdict states

Use only:

- `boundedly supported` — all enumerated claims have recoverable FPF and project evidence, and no semantic blocker was found within the stated scope;
- `unsupported` — a checked claim conflicts with its governing basis or the observed target;
- `insufficient basis` — required FPF source, project authority, evidence, dependency, or observation is missing or non-recoverable.

Never upgrade an unchecked claim through reviewer consensus. Reviewers using one evidence packet are reasoning-independent, not retrieval-independent; include coverage dissent and exact source requests when relevant.

## Authority and layer boundaries

- Return assurance, gate, release, authorization, or acceptance claims to their direct project governor.
- Distinguish direct FPF claims, project evidence, mechanical verification, reviewer inference, and operator decisions.
- Remain layer-agnostic: discover the requested scope at runtime and audit a single layer, several layers, or a layerless target by the same contract.
- Remain read-only unless the user separately authorizes corrections.

## Output

Return the complete listed artifact with every required section and evidence record, including any optional delegated work. Do not replace it with a summary, abbreviated surrogate, or pointer to another result.

### Required result envelope

Organize the complete native artifact under exactly these four top-level Markdown headings, in this order:

1. `## Task, scope, and boundaries`
2. `## High-confidence results (>=95%)`
3. `## Open questions (confidence <95%)`
4. `## Skills used`

In section 1, state the task and receiving use, target and current state, scope and exclusions, inputs, sources and evidence, authority, dependencies, and stop condition. In sections 2 and 3, keep every native requirement below as a subsection or item; do not omit, merge away, or summarize it.

In section 4, list every skill actually executed for this result in execution order, using its exact canonical skill ID, and state each skill's role in one concise sentence. Do not list tools, the base model, or merely proposed or recommended downstream skills as used. If no other skill was executed, list only `fpf-alignment-audit`.

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

1. **Audit contract, resolved FPF source, and inspected scope**
2. **Per-claim alignment matrix**
3. **Semantic blockers**
4. **Structural or mechanical failures**
5. **Residual gaps and optional improvements**
6. **Excluded or uninspected claims**
7. **Bounded verdict and stop/return condition**

Do not use an unqualified “FPF-aligned,” “all good,” or “passed” verdict.
