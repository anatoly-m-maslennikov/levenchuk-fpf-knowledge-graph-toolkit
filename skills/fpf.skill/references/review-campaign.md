# Review campaign convergence

Load this resource only when a task continues, repairs, verifies, closes, or routes work from an existing FPF review, report, finding set, or explicit review campaign. Do not load it for an unrelated one-off skill call. This is shared workflow policy, not an FPF methodology source, and it does not appear in the FPF source trace.

## Campaign envelope

Use one versioned campaign for one semantic frontier and one evaluation profile. Recover the envelope from supplied reports or project evidence; do not invent missing authority or mark an inferred field as confirmed.

Record:

- `campaign_id`;
- `semantic_frontier`: exact claims and revisions whose meaning is under review, plus whether meaning changed;
- `carrier_frontier`: exact paths, versions, hashes, or observed states;
- `evaluation_profile`: frozen checks, direct FPF lenses, dependencies, regressions, and exclusions;
- `predecessor_report` or predecessor campaign;
- decision owner;
- current phase and permitted next transition;
- one shared finding registry.

A material meaning change creates a successor semantic frontier; preserve the predecessor instead of overwriting it. A carrier-only change does not create a new semantic frontier. A separately expanded evaluation profile requires explicit approval and a recorded predecessor.

## Stable findings

Give each finding one stable fingerprint derived from its Entity of Concern, bounded context, affected claim, and failure predicate. A skill name, report title, wording change, or new observation does not create a new finding when the predicate is the same. Add evidence and status to the existing fingerprint.

Use this lifecycle:

`OPEN -> DECIDED -> APPLIED -> VERIFIED`

Alternative terminal dispositions are `DEFERRED`, `REJECTED`, and `SUPERSEDED`, with the successor named. A failed closure check reopens the same fingerprint; it does not create a duplicate.

## Transition guards

| Current condition | Permitted next work | Do not do |
|---|---|---|
| New or materially changed proposal | One full `$fpf design challenge`, then owner disposition | Audit it as implemented or repeat the same full challenge |
| Challenge completed; disposition missing | Return findings to the decision owner | Continue automatically |
| Accepted repairs not applied | Apply the authorized repair batch outside the review skill | Run another full FPF review |
| Accepted repairs applied | One full `$fpf alignment audit` against the frozen profile | Restart design challenge because an audit found a defect |
| Registered mechanical or representation defect | Repair, then targeted deterministic closure checks | Restart the full sequence |
| Consequence-preserving semantic correction | Delta review of the changed claim and affected neighborhood only when required | Repeat the full-scope challenge |
| Semantic blocker requiring a decision | Return the consolidated campaign to the decision owner | Enter an autonomous review-and-fix loop |
| Unchanged semantic frontier and unchanged evaluation profile | Stop | Run any full review again |

`$fpf alignment audit` closure mode verifies registered fingerprints and the frozen regression matrix only. It must not silently widen scope. `$fpf design challenge` delta mode inspects only the changed claim and its declared affected neighborhood. A full review is not a substitute for applying an accepted repair.

## Late findings

When targeted closure finds another issue:

1. Same failure predicate: reopen the existing fingerprint.
2. Different issue inside the frozen profile: mark the earlier evaluation incomplete, add one finding to the same campaign, and stop for owner disposition.
3. Issue outside the frozen profile: record a separate concern or successor-campaign candidate; do not widen the current campaign.
4. Only a safety, authority, or data-loss blocker may cross these boundaries immediately; record why.

## Review budget and stop rule

For one semantic frontier and evaluation profile, permit at most:

- one full design challenge before acceptance or implementation;
- one full post-application alignment audit;
- as many targeted deterministic closure checks as registered findings require.

Permit another full review only after a recorded semantic-frontier change or approval of a distinct evaluation profile. Repeated execution, more prose, a new report, or a different skill does not reset the budget.

If a requested transition is forbidden, return the normal complete result envelope as a bounded stop result. State the exact campaign state, evidence for the unchanged frontier, why the requested call is not permitted, and the one allowed next action. Do not recreate old findings merely to fill a report.

## Campaign handoff

In `## Task, scope, and boundaries`, include a compact campaign handoff whenever this resource applies:

- campaign ID and current phase;
- semantic and carrier frontiers;
- evaluation profile and exclusions;
- predecessor;
- finding fingerprints with current states;
- exact allowed next action and stop condition.

Every participating skill consumes this handoff before doing work and returns the updated handoff. Skills may change finding states only when their native authority and evidence support the transition. Project acceptance and repair authorization remain with the named decision owner.

An explicit `+` composition is one campaign execution surface, not several campaigns. All composed nodes share this envelope, registry, profile, predecessor, and review budget. Intermediate node results update the shared state; only the final consolidated composition artifact is delivered and persisted. Composition never authorizes a forbidden transition or resets the budget.
