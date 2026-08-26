# FPF command composition

Load this resource only when the router returns `mode: composition`. It governs ordered execution, shared state, consolidation, and persistence for the selected analytical nodes. It does not authorize target mutation, project decisions, or execution past a missing authority gate.

## Invocation contract

The explicit syntax is:

`$fpf <command> + <command> [ + <command> ... ] <shared task>`

Spaces around `+` are mandatory. Every segment must start with an exact analytical command or alias. Task text is permitted only after the last command and becomes the shared task for the entire composition. `help` and `plan` cannot be composed. Execute only the ordered nodes returned by the router; never infer another node from keywords.

The router admits only adjacent pairs declared as graph edges. An admitted edge proves only that a handoff is structurally legal. It does not prove that required evidence, target state, owner disposition, or mutation authority exists.

## One composition envelope

Create one envelope before running the first node and carry it through every executed node:

- shared task, receiving use, scope, exclusions, and decision owner;
- exact selected sequence and current step;
- target identity plus semantic and carrier frontiers;
- frozen evaluation profile and protected trade-offs;
- one stable finding registry;
- one repair and improvement registry;
- predecessor evidence and node handoffs;
- permitted next transition and stop condition.

When the sequence contains `design-challenge`, `quality-improve`, or `alignment-audit`, or continues an earlier review, load `references/fpf-review-campaign.md`. Use its campaign envelope as the composition envelope and preserve its review budget. A new node, report, or composition does not reset that budget.

## Execute lazily and stop at gates

Run nodes from left to right. Load only the current node prompt and the references it actually requires. Give it the shared task, current envelope, and preceding native handoff.

Each executed node must complete its native analysis and evidence record, but treat that result as an intermediate composition record. Do not return or persist it as a separate report. Merge its evidence, findings, proposed corrections, decisions, changes, verification, open questions, source trace, and stop condition into the shared envelope.

Before starting the next node, verify that its declared target state and prerequisites now exist. Stop the composition when:

- project disposition or mutation authority is required but absent;
- the next node requires evidence, a changed version, or an applied repair that does not exist;
- review-campaign policy forbids the transition or requires external work;
- the current node returns insufficient basis for the handoff;
- the user cancels or overrides the sequence.

Do not manufacture a decision, claim that a proposed correction was applied, or run a closure audit against an unchanged target. Record every unexecuted suffix node and the exact unmet run condition in the final artifact.

## Stable consolidated findings

Merge findings by stable fingerprint: Entity of Concern, bounded context, affected claim, and failure predicate. Different wording, evidence, severity, or discovering node does not create another issue when that predicate is the same.

The final finding registry must include every issue or weak point stated by any executed node within the declared scope and evaluation profile. It is not a claim that no issue exists outside that boundary. For each finding record:

- stable finding ID and concise issue or weakness;
- affected target, claim, and bounded context;
- evidence and discovering or updating nodes;
- consequence and protected trade-offs;
- confidence and coverage limit;
- lifecycle state: `OPEN`, `DECIDED`, `APPLIED`, `VERIFIED`, `DEFERRED`, `REJECTED`, or `SUPERSEDED`.

When later evidence repeats a predicate, update the existing finding. When it contradicts earlier evidence, preserve the conflict and lower confidence rather than choosing silently.

## One repair and improvement list

Produce one deduplicated ordered list that addresses the entire final finding registry. Group compatible actions into the smallest coherent repair batches. For every action record:

- stable action ID and exact repair or improvement;
- finding IDs addressed;
- affected carriers or change surface;
- owner and required authority;
- dependencies and execution order;
- state: `PROPOSED`, `AUTHORIZED`, `APPLIED`, `VERIFIED`, `DEFERRED`, or `REJECTED`;
- expected result and protected trade-offs;
- deterministic or semantic verification criterion.

Every finding must map to at least one action or an explicit disposition explaining why no action will be taken. Every action must map back to one or more findings. Merge duplicate actions that solve the same predicates. Separate already applied and verified actions from remaining work; never present completed work as an open recommendation.

## Convergence and late findings

The composition is one bounded campaign, not an autonomous review-and-fix loop.

- A full design challenge runs at most once for one unchanged semantic frontier and profile.
- Accepted changes may enter `quality-improve` only with sufficient authority and a recoverable target version.
- A post-application alignment audit runs at most once and uses closure mode when verifying the registered repair set.
- The same failure predicate reopens the same finding and requires a targeted closure check, not another full review.
- A new issue inside the frozen profile is added to the same registry and returned for owner disposition.
- An issue outside the profile becomes a separate concern or successor-campaign candidate.
- A material semantic change permits only the required delta challenge over the changed claim and affected neighborhood.

Stop when the frontier and profile are unchanged and no permitted transition remains.

## Final consolidated artifact

Return exactly one complete Markdown artifact under the standard four top-level headings:

1. `## Task, scope, and boundaries`
2. `## High-confidence results (>=95%)`
3. `## Open questions (confidence <95%)`
4. `## Skills used`

Preserve every material native result from executed nodes inside this envelope. Under high-confidence results include, in order:

1. **Composition execution and stop state** — requested sequence, executed prefix, unexecuted suffix, handoffs, gates, and final stop reason.
2. **Consolidated issues and weak points** — the complete deduplicated finding registry within scope.
3. **Consolidated fixes and improvements** — the single mapped and ordered action list.
4. **Verification, residual risk, and coverage** — applied and verified actions, unresolved findings, inspected scope, exclusions, and successor conditions.

Keep lower-confidence issues, fixes, and evidence gaps under `## Open questions (confidence <95%)` while retaining their IDs and mappings. Do not hide them to make the consolidated lists appear complete.

Under `## Skills used`, list every node actually executed in order. Then include one unioned `#### FPF sources consulted (N read; M used)` subsection. List each opened source once and identify the nodes for which it was used or screened. Do not list an unexecuted suffix node as used.

## Persist once

Resolve output and report settings once for the whole composition. Intermediate node instructions to return and persist complete artifacts apply to their internal records; this composition contract replaces separate delivery with the one final consolidated artifact.

When saving is on, load `references/fpf-report-persistence.md` once after consolidation and use report node ID `composition`. Save exactly the same Markdown returned in chat. CAPRMEDIO mode creates one Analysis Report Atom for the complete composition scope, not one Atom per node.
