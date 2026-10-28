# FPF command composition

Load this resource when the Markdown command graph admits an explicit composition or when exact `do` approves a validated ordered FPF Plan. It governs ordered execution, shared state, consolidation, and persistence for the selected analytical nodes. It does not authorize target mutation, project decisions, or execution past a missing authority gate.

## Invocation contract

The explicit syntax is:

`$fpf <command> + <command> [ + <command> ... ] <shared task>`

Spaces around `+` are mandatory. Every segment must start with an exact analytical command or alias. Task text is permitted only after the last command and becomes the shared task for the entire composition. `help` and `plan` cannot be composed. Execute only the ordered nodes explicitly matched through the Markdown graph; never infer another node from keywords.

Admit only adjacent pairs declared under `Legal composition handoffs` in the Markdown graph. An admitted edge proves only that a handoff is structurally legal. For every pair, bind the current node's result to the edge's `Producer output`, pass only its declared `Consumer input`, verify `Required evidence`, and evaluate the `Gate predicate`. If any field cannot be satisfied, stop with the row's exact `STOP_*` state and state which field failed; never replace it with a generic “insufficient context” diagnosis.

For an approved Plan, `references/fpf-plan-execution.md` supplies approval and continuation semantics. The numbered Plan supplies the ordered commands and shared task; this composition contract supplies the typed handoffs and one-envelope behavior. The Plan does not make an undeclared graph edge legal.

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

Each executed node must complete its native analysis and evidence record as one temporary `step-NNN/` artifact set. The same warden validates that set before its result can enter the next node. Do not return or durably persist it as a separate report. Merge only validated step-set evidence, findings, proposed corrections, decisions, changes, verification, open questions, source trace, and stop condition into the shared envelope.

Before starting the next node, verify that its declared target state and prerequisites now exist. Stop the composition when:

- project disposition or mutation authority is required but absent;
- the next node requires evidence, a changed version, or an applied repair that does not exist;
- review-campaign policy forbids the transition or requires external work;
- the current node returns insufficient basis for the handoff;
- the user cancels or overrides the sequence.

Do not manufacture a decision, claim that a proposed correction was applied, or run a closure audit against an unchanged target. Record every unexecuted suffix node, the exact graph-declared stop state, the failed handoff field, and the unmet run condition in the final artifact.

## Stable consolidated issues

Merge findings by stable fingerprint: Entity of Concern, bounded context, affected claim, and failure predicate. Different wording, evidence, severity, or discovering node does not create another issue when that predicate is the same.

The final issue registry must include every issue or weak point stated by any executed node within the declared scope and evaluation profile. It is not a claim that no issue exists outside that boundary. For each issue record:

- stable issue ID and concise issue or weakness;
- affected target, claim, and bounded context;
- evidence and discovering or updating nodes;
- consequence and protected trade-offs;
- issue confidence, its evidence basis, and coverage limit or uncertainty;
- lifecycle state: `OPEN`, `DECIDED`, `APPLIED`, `VERIFIED`, `DEFERRED`, `REJECTED`, or `SUPERSEDED`.

When later evidence repeats a predicate, update the existing issue. When it contradicts earlier evidence, preserve the conflict and lower confidence rather than choosing silently.

## One repair and improvement register

Produce one deduplicated ordered list that addresses the entire final issue registry. Group compatible actions into the smallest coherent repair batches. A fix can address more than one issue, but every issue must map to a fix or an explicit disposition. For every fix or improvement variant record:

- stable fix ID and exact repair or improvement;
- issue IDs addressed;
- relationship: `alternative`, `complementary`, or `required prerequisite`;
- affected carriers or change surface;
- owner and required authority;
- dependencies and execution order;
- state: `PROPOSED`, `AUTHORIZED`, `APPLIED`, `VERIFIED`, `DEFERRED`, or `REJECTED`;
- fix confidence and its own evidence basis, distinct from every issue confidence;
- expected result and protected trade-offs;
- deterministic or semantic verification criterion; and
- recommendation: `preferred`, `acceptable`, or `rejected`.

Every fix must map back to one or more issues. Merge duplicate fixes that solve the same change predicate and retain every addressed issue ID. Separate already applied and verified fixes from remaining work; never present completed work as an open recommendation. The final order is the one consolidated register for resolving all stated issues and weak points without a repeated full-audit loop.

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

## Persist once

Resolve output and report settings once for the whole composition. Intermediate step sets are complete temporary artifacts but never separate durable reports; this composition contract keeps one final consolidated delivery artifact.

When saving is on, load `references/fpf-report-persistence.md` once after consolidation and use report node ID `composition`. Save exactly the same Markdown returned in chat. CAPRMEDIO mode creates one Analysis Report Atom for the complete composition scope, not one Atom per node.

## Final delivery

After the composition and after loading its one enabled persistence protocol, load `references/fpf-analysis-output.md` before file creation. Use its composition receipt extension and one consolidated analytical envelope as the final authority; never return native node layouts or a short stop response.
