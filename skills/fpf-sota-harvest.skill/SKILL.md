---
name: fpf-sota-harvest
description: Harvest and synthesize a bounded, plural state of the art with First Principles Framework (FPF) evidence without reading the full methodology. Locate FPF without assuming the user's storage, tools, operating system, repository layout, or setup. Use when the user asks for SoTA harvesting, an evidence-backed field map, rival-tradition comparison, a reconstructible research synthesis pack, or a current landscape that must preserve disagreements instead of producing a generic summary.
---

# FPF SoTA Harvest

<!-- output-settings:start -->
## Output language settings

Defaults: `output_style = "general"`; `fpf_terms_explained = "off"`. Explicit user values override them.
Load at most one mode resource:
- `natural`: load none; allow FPF terms. On first use, explain each term per `fpf_terms_explained`: `full` up to three short lines, `short` one sentence, `off` none.
- `general`: load only `fpf-route/references/output-style-general.md`.
- `ste`: load only `fpf-route/references/output-style-ste.md`.
Never preload an unselected resource. If the selected file is missing, report it; do not substitute. Keep exact FPF locators and source paths in compact evidence or source records, not narrative prose.
<!-- output-settings:end -->

Produce a read-only **SoTA Synthesis Pack** for one declared frame. Preserve reconstructibility and plurality; do not silently fuse rival traditions.

## Resolve scope and FPF source

1. Resolve the research question, Entity of Concern, frame, receiving use, intended audience, source policy, freshness boundary, and decision or work receiver.
2. Resolve an accessible FPF edition from a user-supplied path, URI, attachment, corpus, connected item, optional runtime hint, or bounded search of accessible task-relevant roots. Verify candidates by FPF identity and navigable direct patterns, not container names.
3. Locate `SoTA Harvester & Synthesis` by title and content. Inspect its Problem frame, Problem, Forces, Solution, Consequences, and ordinary boundary. Use practical-use cards, contents, hubs, and indexes only for routing.
4. Never load the full methodology or an oversized source wholesale. Use targeted sections. Use six direct-pattern pages as the default ceiling; entry and index pages do not count.
5. Keep the source locator task-local. Cite FPF and research evidence with stable file, URI, attachment, corpus, or connected-item locators. If required current evidence is inaccessible, return `insufficient basis` rather than a timeless or generic substitute.

## Define the harvest contract

Record:

- the domain question and declared comparison or generation frame;
- included and excluded traditions, languages, source classes, dates, and jurisdictions when relevant;
- admission, credibility, freshness, and source-use rules;
- required evidence granularity and unresolved disagreement policy;
- time, retrieval, and publication boundaries.

## Workflow

1. Build a reconstructible `CorpusLedger` before synthesis. Record source identity, edition/date, admissibility, role, and locator.
2. Create `ClaimSheets` that separate source claims, evidence anchors, reviewer synthesis, and operator decisions.
3. Construct the `SoTA_Set` and an explicit inventory of rival traditions, methods, characteristic axes, strengths, limits, and untranslatable distinctions.
4. Record crossings or bridges only when their mapping basis is explicit. Use a palette or `BridgeMatrix` where supported; keep unresolved incompatibilities visible.
5. Produce the smallest synthesis pack sufficient for the receiving use. Treat archive, front, pool, shortlist, or selection as later conditional results, not automatic consequences of harvesting.

## Boundaries

- Do not equate popularity, recency, search rank, or citation count with SoTA status without the declared frame.
- Do not silently harmonize incompatible terms, evidence standards, or schools.
- Do not claim exhaustive coverage beyond the corpus ledger and explicit exclusions.
- Remain layer-agnostic and domain-agnostic. Remain read-only unless the user separately authorizes publication or file writes.

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

In section 4, list every skill actually executed for this result in execution order, using its exact canonical skill ID, and state each skill's role in one concise sentence. Do not list tools, the base model, or merely proposed or recommended downstream skills as used. If no other skill was executed, list only `fpf-sota-harvest`.

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

1. **Harvest contract and resolved FPF source**
2. **CorpusLedger and coverage boundary**
3. **ClaimSheets and evidence anchors**
4. **SoTA_Set, traditions, palette, and bridges**
5. **Disagreements, exclusions, and insufficient basis**
6. **Receiving use and refresh/return condition**
