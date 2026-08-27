# FPF Context Connector

Use this helper only after routing selects one or more analytical nodes. Help and Plan never load it.

## Two-part connector

1. `scripts/read_fpf_graph.py` is the control-plane YAML reader. Request only the selected node IDs and optional task-profile ID. Its output intentionally omits aliases, keywords, examples, evaluation cases, fallback rules, unrelated nodes, unrelated profiles, and unrelated edges.
2. `scripts/prepare_fpf_context.py` is the data-plane context hydrator. Request the same selected node IDs, optional task-profile ID, and verified repository root. It returns only their shared contracts, node prompts, active command/profile FPF bindings, and verified core pattern sections.

Use the repository uv project:

`uv --project <repository-root> run python <skill-root>/scripts/read_fpf_graph.py --node <node-id>`

`uv --project <repository-root> run python <skill-root>/scripts/prepare_fpf_context.py --repository-root <repository-root> --node <node-id>`

When the router returns `task_profile`, append `--profile <task-profile-id>` to both calls. A profile identifies the subject area and typical task; the command node still owns the analytical operation and native result.

For an explicit composition, call the context hydrator once with every ordered node ID. It deduplicates shared contracts and repeated FPF pages.

The context hydrator is for a file-backed FPF graph whose repository root is known. When the user explicitly selects a different non-file-backed edition, use the YAML reader for the selected stable IDs, resolve those IDs through the edition's native index or locators, and construct the same bounded section records. Never force repository-relative paths onto a URI, attachment, corpus, or connected item.

## Conditional and bounded retrieval

Conditional FPF bindings are skipped by default and listed under `skipped_conditionals`. Include one only when the task satisfies its declared `when` condition, using `--include-conditional <FPF-ID>`.

The connector returns every available Problem frame, Problem, Forces, Solution, and Consequences section. It reports absent canonical headings under `missing_core_sections`; absence is a source condition, not permission to synthesize missing FPF text. A large Solution section is a bounded real excerpt with exact page and line ranges plus its remaining subsection headings. Treat `complete = false` as a retrieval instruction: open only the exact Solution subsection needed for the current claim. Never treat an excerpt as the complete pattern or silently infer omitted content.

## Analytical handoff

Give the analytical prompt:

- the residual user task and resolved language;
- the selected task profile, when any;
- the connector's selected `contracts` and `prompts` paths;
- the hydrated `patterns` records and their typed `uses`;
- any `skipped_conditionals` relevant to an unresolved decision;
- the exact source locator for every further subsection opened.

The connector supplies methodology context, not a finding, verdict, authority decision, or report. The analytical prompt remains responsible for task evidence, FPF reasoning, confidence, boundaries, and the native result artifact.
