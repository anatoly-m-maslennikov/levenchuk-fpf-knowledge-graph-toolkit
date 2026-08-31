# FPF Analysis Output Finalizer

Load this file after the native analytical prompt, source retrieval, shared analytical contract, composition work when applicable, and the persistence protocol when saving is requested, but before file creation. It is the final authority for every analytical response shape, including stopped runs and unsaved reports. After finalization, an allowed exclusive create and read-back may deliver these exact bytes but must not reshape them.

Start the response at the first heading below. Use these four canonical heading names exactly once and in this order at one consistent top level. That top level may be Markdown `#` or `##`; nested headings must be deeper. Never use `High-confidence results`, `Open questions (confidence <95%)`, or a native prompt label as a top-level heading.

## Task, scope, and boundaries

State task and receiving use, target and current state, scope and exclusions, inputs, evidence and sources, authority, dependencies, stop state, and report outcome. A persistence failure changes the report outcome but never shortens this artifact.

For a composition, add `### Composition receipt` with: exact invocation; selected profile or `none`; requested sequence; executed prefix; unexecuted suffix; one result for every typed edge; exact final `STOP_*` state or `COMPLETE`; context-ledger read/used/deferred counts; and carried issue and fix IDs.

## Issues, weak points, and improvements

Preserve every native result requirement under `### Native result`, then provide exactly one `### Issue registry` and exactly one `### Fix and improvement register`. Do not repeat either register elsewhere.

Every issue record must explicitly contain: stable issue ID; issue or weak point; evidence; consequence; affected target or bounded context; issue confidence and evidence basis; coverage limit or uncertainty; lifecycle state; and mapped fix IDs or an explicit no-fix disposition.

Every fix record must explicitly contain: stable fix ID; exact change; addressed issue IDs; relationship: `alternative`, `complementary`, or `required prerequisite`; independent fix confidence and evidence basis; expected result; trade-offs; owner and required authority; dependencies and execution order; deterministic or semantic verification; recommendation (`preferred`, `acceptable`, or `rejected`); and state.

Deduplicate by failure predicate and change predicate. Keep lower-confidence issues in the issue registry. Do not present a proposed, applied, or verified state as another state.

For a composition, put execution and stop state before the registries and verification, residual risk, coverage, and successor conditions after them. One consolidated registry pair covers all executed nodes.

## Unresolved evidence gaps

List only genuine missing evidence or unanswered questions. Each gap needs a stable ID, linked issue or fix IDs when applicable, best current answer, missing evidence, consequence, and exact next evidence or action. Otherwise write `None identified within the declared scope`.

## Skills used

List only canonical analytical commands whose native analysis actually executed, in order. Do not list a consumer that stopped at its incoming handoff.

### FPF sources consulted (N read; M used)

List each direct FPF methodology page actually opened once, repository-root-relative or by stable non-file locator, marked **used** or **screened only**. Do not list Help pages, prompts, contracts, command/profile graphs, project evidence, tools, or discovered-but-unopened pages. If no direct page was usable, state the exact insufficient-basis condition instead of implying methodology grounding.

Before returning, verify all four heading names and their consistent depth, every required issue and fix field, one registry pair, the complete composition receipt when applicable, the complete native result, exact executed-skill trace, exact source trace, and truthful report state. Repair the response before emitting it if any check fails.
