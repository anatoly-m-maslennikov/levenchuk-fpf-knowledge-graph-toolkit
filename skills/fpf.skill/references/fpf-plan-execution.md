# FPF Plan Execution

This contract turns one validated FPF Plan into a resumable ordered run. It governs approval, step inheritance, blocking questions, the operator-adjustable decision threshold, and automatic continuation. It does not expand the Plan's scope or grant authority omitted from it.

## Decision threshold

The blocking-decision confidence threshold defaults to 95%. The operator may explicitly set any percentage from 0% through 100% for one invocation or active Plan, for example `blocking threshold 90%` or `decision_threshold=90%`. Do not infer an override from percentages used as evidence, issue confidence, fix confidence, quality targets, or quoted text.

Resolve the threshold once while proposing the Plan and record it in metadata. Preserve it across exact `do`, every step, blocking question, answer, revision, and final result. When it differs from 95%, state `blocking threshold: <value>% (operator override)` in the first numbered Plan step. The operator may explicitly change it during an active Plan; record the new value and apply it to the next unresolved blocking decision without requiring another `do`.

An invalid, missing, or out-of-range override is not guessed. Ask the operator for a value from 0% through 100%. This threshold controls only whether an unresolved material decision is returned to the operator. It never weakens an exact `STOP_*` gate, required evidence, mutation or decision authority, persistence safety, CAPRMEDIO admission, or warden validation.

## Plan identity and approval

The only approvable Plan is the most recent validated, released, unexecuted FPF Plan in the same conversation. Its numbered steps, shared task, exclusions, dependencies, gates, and expected final result are the complete execution boundary.

Exact `do` approves that Plan once. It does not approve earlier Plans, already-started Plans, conditional follow-ups omitted from the numbered list, target mutation, external communication, credentials, or project decisions not explicitly authorized in the Plan. With no approvable Plan, stop at `STOP_NO_APPROVABLE_PLAN`.

## Ordered run and inherited results

Execute numbered steps in order and create exactly one `step-NNN/` artifact set for each executed step. A step starts only after the preceding step's set reaches warden `PASS` or returns a validated graph-declared stop. Pass the preceding immutable set's complete candidate, metadata, evidence ledger, stable issue and fix registries, decisions, unresolved gaps, and stop conditions into the next step. The next step records that predecessor set and distinguishes inherited evidence from its own findings.

Intermediate step sets are invocation-local temporary artifacts. Do not release or durably persist them. After the final runnable step set passes, create `final/`, consolidate only the validated step sets under the analysis finalizer, and validate that final set through the warden. Record every stopped or unexecuted suffix step truthfully. Never overwrite a passed step set or let an unvalidated step feed its successor.

Do not re-route an approved Plan. If its target, evidence frontier, authority, or relevant context materially changed after approval, treat the necessary choice as a blocking decision. If a declared graph handoff fails without a user-resolvable choice, use its exact `STOP_*` state rather than asking a question.

## Blocking-question rule

Ask a question only when all of these are true:

1. a decision is required before the next safe action;
2. the decision can materially change route, scope, result, or authority;
3. available evidence and the approved Plan do not support one choice at confidence greater than or equal to the active blocking-decision threshold; and
4. the user can resolve the decision.

Do not ask merely because an issue, fix, or other analytical claim has confidence below the active threshold. Preserve such claims in the appropriate registry with evidence and uncertainty. Do not move ordinary evidence gaps into a blocking question when execution can safely continue.

A blocking-question candidate has exactly this shape:

```markdown
# Blocking question

<one concise question naming the decision and why it blocks the current numbered step>

1. **<recommended variant> (Recommended)** - <impact>
2. **<variant>** - <impact>
3. **<optional variant>** - <impact>

Reply with the option number or label. Execution will resume automatically.
```

Provide two or three mutually exclusive variants. Put the recommended variant first only when evidence supports that recommendation; otherwise state that no variant is recommended. Never include an “Other” variant. The metadata records a stable question ID, the active threshold, the decision confidence below that threshold, its evidence basis, affected step, and all variants.

After the user answers, resolve the decision against the listed variants. If confidence becomes greater than or equal to the active threshold, resume the same step and automatically continue through all remaining runnable steps without another `do`. If the answer is ambiguous and confidence remains below the active threshold, ask one narrower question under this same contract. A new unrelated request cancels automatic continuation.

## Validation boundary

The warden validates the proposed Plan, every step artifact set, every released blocking question, and the final consolidated set. It verifies run-directory identity, whole-task summary, set kind, Plan identity, step order, predecessor-set receipts, question necessity and confidence, canonical commands, and final completeness. A warden PASS validates one exact set; it does not grant missing execution authority.
