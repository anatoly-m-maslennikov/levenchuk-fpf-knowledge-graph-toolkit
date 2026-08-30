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

## Analytical handoff

Give the analytical prompt:

- the residual user task and resolved language;
- the selected task profile, if any;
- the selected command and profile binding relations;
- the exact opened FPF page paths or stable locators;
- the relevant inspected sections and any skipped conditional binding;
- every missing section or bounded-retrieval limitation.

This connector supplies methodology context, not a finding, verdict, authority decision, or report. The analytical prompt remains responsible for evidence, confidence, boundaries, and its native result.
