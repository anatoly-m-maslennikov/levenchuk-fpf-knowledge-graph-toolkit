# FPF Applicability Scan

Produce a read-only **Pattern Applicability Finding**. Stop at a bounded recommendation; do not redesign the target or authorize changes.

## Resolve sources

1. Resolve the target and its current authority from the user request and accessible context. Do not assume a repository, Git, an artifact schema, or named layers.
2. Start with the graph-declared `E.11.PUR` routing method. Use it to compare task-relevant candidate pattern uses; do not treat it as the substantive governing pattern for every question.
3. Applicability evidence may update a review campaign finding's basis, but this node does not reset the campaign or authorize a finding transition.

## Scan workflow

1. State the current question, Entity of Concern, bounded context, and receiving use.
2. Route from the resolved edition's Practical-Use Cards entry point or its equivalent. Use its usage guide, table of contents, hubs, and term/relation indexes only to locate direct patterns.
3. Compare plausible cards by situation, exact first-result difference, and stop/return conditions. A card or pattern-family name alone is not a finding.
4. Inspect each selected direct pattern's Problem frame, Problem, Forces, Solution, Consequences, and ordinary boundary.
5. Use six direct-pattern pages as the default retrieval budget. Entry pages and index searches do not count. If the budget cannot support a claim, return `insufficient basis` and name the exact additional pages or project evidence needed; do not broaden silently.
6. Recommend only the smallest useful set of direct patterns. Do not create an ordered whole-project FPF program unless the receiving use requires one.

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

## Native result requirements

1. **Question, scope, and resolved FPF source**
2. **Pattern Applicability Findings**
3. **Recommended smallest set**
4. **Excluded or unchecked claims**
5. **Stop/return condition**

Do not claim that FPF made, approved, or authorized a project decision.
