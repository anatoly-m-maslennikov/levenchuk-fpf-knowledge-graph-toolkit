# FPF Analytical Contract

Apply this contract to every analytical node declared in `graph.yaml`. Load it once for a single-node call and once for an explicit composition, even when several nodes declare it.

<!-- output-settings:start -->
## Output and report settings

Embedded defaults: `output_language = "auto"` (`auto`, `en`, or `ru`); `output_style = "general"`; `fpf_terms_explained = "off"`; `save_report = "on"` (`on` or `off`); `report_style = "plain"` (`plain` or `caprmedio`, consulted only when saving is on). Explicit user instruction overrides an optional active-project `.caprmedio/settings.toml` setting, which overrides the installed `.fpf-runtime.toml` defaults, which override these embedded defaults. Absence of CAPRMEDIO settings is normal and never blocks standalone FPF execution.
Resolve `output_language` before output style. `en` means English and loads no language resource. `ru` means Russian and loads only `references/fpf-output-language-ru.md`. With `auto`, use Russian when the user's invocation or residual task contains meaningful Russian Cyrillic text; otherwise use English. Never infer language from quoted source text, identifiers, paths, or citations alone. Never preload an unselected language resource.
For output style, load at most one mode resource:
- `natural`: load none; allow FPF terms. On first use, explain each term per `fpf_terms_explained`: `full` up to three short lines, `short` one sentence, `off` none.
- `general`: load only `references/fpf-output-style-general.md`.
- `ste`: load only `references/fpf-output-style-ste.md`.
Never preload an unselected resource. If the selected file is missing, report it; do not substitute. Keep exact FPF locators and source paths in compact evidence or source records, not narrative prose.
Return the complete artifact in chat. When `save_report = "on"`, consult `report_style`, then load only `references/fpf-report-persistence.md` and follow it; never replace chat delivery with a summary or pointer.
<!-- output-settings:end -->

## Resolve the FPF edition and declared entrypoints

1. Resolve an accessible FPF edition in this order: a source named in the request; a path, URI, attachment, corpus, or connected item already in context; the verified installed `repository_root/FPF-Knowledge-Graph` runtime hint; another optional environment or workspace hint; then a bounded search of accessible task-relevant roots or providers. A source explicitly named by the user overrides the installed hint.
2. Use the verified bundle produced under `references/fpf-context-connector.md`. `primary_method` is the node's direct method; `result_projection` defines an expected projection; `routing_method` or `routing_entrypoint` starts task-dependent pattern discovery; `conditional_method` is present only when its declared condition holds.
3. Treat hydrated core sections as real FPF source content with exact repository paths and line ranges. When a Solution record has `complete = false`, open only the exact subsection needed for the current claim; never treat the excerpt as the complete pattern.
4. For another FPF edition, resolve the same stable ID through that edition's index or native locator. Do not force a repository path onto a non-file-backed source. If the ID cannot be resolved, report the stale or incompatible binding and request the exact missing source rather than silently substituting a nearby pattern.
5. Use practical-use cards, usage guidance, hubs, contents, and term or relation indexes only to route to direct patterns. Inspect the relevant Problem frame, Problem, Forces, Solution, Consequences, and ordinary boundary of every direct pattern materially used.
6. Never load a monolithic or explicitly unsafe or oversized FPF source wholesale. Use the connector bundle, targeted graph pages, or exact sections within the node's retrieval budget. Budget exhaustion produces `insufficient basis`, never a semantic pass. Keep discovered source locations task-local; never persist a user-specific path into this reusable package.
7. Search only accessible, task-relevant roots or providers. Never scan an entire device, account, or network. If several editions remain plausible and the choice affects the result, ask which is authoritative. If none can be verified, report what was checked and request a path, URI, attachment, corpus, or connected source.

## Review campaign continuation

Before resolving FPF sources or starting native work, when the task cites a prior FPF report, finding, repair, closure check, or review campaign, load `references/fpf-review-campaign.md` and preserve its campaign envelope, existing fingerprints, evaluation profile, review budget, and stop rule. This workflow reference is not an FPF methodology source. Return any updated campaign handoff in `## Task, scope, and boundaries`; do not reset the campaign merely because another analytical node or composition is running.

## Optional delegated work

Delegation must not change the required result. Resource or retrieval limits alone do not justify cancellation, replacement, or duplicate work. Pending work may remain pending while only non-conflicting work continues. Stop it only for user cancellation or override, or a confirmed safety or protected-scope violation. If delegation is unavailable, execute directly.

## Result delivery

Return the complete native artifact with every required section and evidence record. Do not replace it with a summary, abbreviated surrogate, or pointer to another result.

Organize it under exactly these four top-level Markdown headings, in this order:

1. `## Task, scope, and boundaries`
2. `## High-confidence results (>=95%)`
3. `## Open questions (confidence <95%)`
4. `## Skills used`

In section 1, state the task and receiving use, target and current state, scope and exclusions, inputs, sources and evidence, authority, dependencies, and stop condition. In sections 2 and 3, preserve every native result requirement from the selected node prompt as a subsection or item; do not omit, merge away, or summarize it.

In section 4, list every skill actually executed for this result in execution order, using its exact canonical `$fpf <command>` invocation from the router, and state each skill's role in one concise sentence. Do not list tools, the base model, or merely proposed or recommended downstream skills as used. For a single-node result, list only that executed analytical command.

Immediately after the skill list, add this compact Markdown subsection:

#### FPF sources consulted (N read; M used)

- `FPF-Knowledge-Graph/<relative-path>.md` — **used**: <brief evidence role>
- `FPF-Knowledge-Graph/<relative-path>.md` — **screened only**

List every FPF source document actually opened exactly once. **Used** means it materially supports a result; **screened only** means it was read but not relied on. Do not list merely discovered-but-unopened files, project evidence, tools, or absolute machine paths. Prefer repository-root-relative `FPF-Knowledge-Graph/...` paths; for a non-file-backed edition, use a stable URI or item identifier.

Assign confidence to each material result and state its evidence basis. Confidence is claim-level epistemic confidence under the available evidence, not a statistical probability, artifact-wide score, importance, severity, authorization, acceptance, assurance, or gate result. Use these bands inside section 3:

- **90–94%:** probable answer, but confirmation is still needed.
- **Below 90%:** materially uncertain.

Never round up to 95%, hide conflicting, unsupported, or insufficient-basis results, or omit a lower-confidence finding. For each open question include the best current answer, confidence band or value, missing evidence or input, consequence, and exact next evidence or action. A high-confidence determination that the basis is insufficient belongs in section 2; the unresolved substantive question belongs in section 3. If no open questions remain, keep section 3 and write `None identified within the declared scope`.
