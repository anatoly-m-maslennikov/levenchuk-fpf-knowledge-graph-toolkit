# FPF Markdown Context Connector

Use this contract only after the Markdown command graph selects one or more analytical nodes. Help and Plan never load it.

## Direct Markdown resolution

1. Read the selected node's FPF bindings from `references/fpf-command-graph.md`.
2. If one task profile was selected, read only its `FPF context` line from the selected area profile file.
3. Deduplicate stable IDs while preserving every command/profile use and relation.
4. Resolve each stable ID through the exact ID row in `<repository_root>/FPF-Knowledge-Graph/00_Index/FPF - Index.md`, follow its page link, and verify the page frontmatter carries the same `fpf_id`.
5. Load a `conditional_method` only when its written condition is satisfied. Record it as skipped otherwise.

For a non-file-backed edition explicitly selected by the user, resolve the same stable IDs through that edition's native index or stable locators. Never invent repository paths for a URI, attachment, corpus, or connected item.

## Conditional and bounded retrieval

Inspect only the available Problem frame, Problem, Forces, Solution, and Consequences sections required for the current task. Record absent headings as a source condition. When a Solution section is too large for the current context, open only the exact relevant subsection and record that the full section was not inspected. Never silently infer omitted content.

For a composition, resolve bindings only for the current node immediately before it executes. Reuse an already opened page when its stable ID and edition are identical; do not preload later-node context.

## Invocation-local context ledger and budget

Maintain one compact in-context ledger for this invocation. It is part of the reasoning handoff, not a file, cache, generated artifact, or reusable source. For every declared binding record: edition identity, stable ID, relation and owning node/profile, resolved locator, `fpf_id` verification, inspected sections, `used`, `screened only`, `skipped conditional`, or `deferred`, and any retrieval limit.

- A single-node call may open at most 6 distinct FPF pages.
- A composition may open at most 18 distinct FPF pages across the complete run and at most 6 previously unopened pages for one current node.
- One page inspection is limited to its task-relevant core sections and exact needed subsections; it never grants a whole-page or neighborhood preload.
- Reuse is allowed only inside the same invocation when both edition identity and stable ID match. Never create or consult a persistent context cache.
- Before opening a page, count it against the budget. If a required binding would exceed the budget, stop the affected node or composition with `STOP_CONTEXT_BUDGET_EXHAUSTED`, list every deferred binding, and return `insufficient basis`; never discard an already selected required binding silently.

Derive the final `FPF sources consulted` subsection from this ledger. The counts must equal its opened `used` plus `screened only` entries; skipped, deferred, or merely resolved-but-unopened entries are not counted as read.

## Analytical handoff

Give the analytical prompt:

- the residual user task and resolved language;
- the selected task profile, if any;
- the selected command and profile binding relations;
- the exact opened FPF page paths or stable locators;
- the relevant inspected sections and any skipped conditional binding;
- every missing section or bounded-retrieval limitation.
- the current compact context-ledger entries and remaining page budget.

This connector supplies methodology context, not a finding, verdict, authority decision, or report. The analytical prompt remains responsible for evidence, confidence, boundaries, and its native result.
