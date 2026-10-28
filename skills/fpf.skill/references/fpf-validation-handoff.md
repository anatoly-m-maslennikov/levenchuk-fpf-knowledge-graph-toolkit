# FPF Candidate Validation Handoff

This contract governs the only filesystem handoff between the FPF doer, manager, and warden. It is invocation-local transport, not a methodology source, durable report, project artifact, cache, or evidence that analysis or validation occurred.

## One two-file artifact set per unit

One run directory under the host's system temporary root uses the leaf `fpf-<YYYY-MM-DD>-<whole-task-summary>-<uuid>`. The summary is derived once from the complete task and never from a substep. The run contains only `plan/`, numbered `step-NNN/`, and `final/` artifact-set directories that the workflow actually needs. Every set contains exactly `candidate.md` and `candidate-meta.md`.

A default Plan-first request uses `plan/`, including a request that names one command or a `+` stack. An explicitly without-Plan single-node call uses `step-001/`. An explicitly without-Plan multi-step call uses exactly one numbered set per executed subtask plus `final/` for consolidation. Both paths in a set must resolve inside that same set directory. Reject symlinks, path traversal, pre-existing unrelated content, an unexpected set, a third file in a set, or a path outside the selected temporary root.

`candidate.md` contains the complete proposed user-facing result and nothing else. It must already use the applicable finalizer and include the truthful planned report outcome. It is not released and no durable report is created before warden `PASS`.

`candidate-meta.md` is plain Markdown and contains exactly these headings in order:

```markdown
# FPF Candidate Metadata

## Identity
- Schema: `fpf-candidate-meta-v4`
- Run ID: `<run-id>`
- Run directory: `<absolute fpf-YYYY-MM-DD-whole-task-summary-uuid path>`
- Whole-task summary: `<the stable whole-task slug>`
- Artifact set ID: `<plan, step-NNN, or final>`
- Artifact set kind: `<plan, step, or final>`
- Attempt: `<positive integer>`
- Complete invocation: `<verbatim invocation>`
- Candidate path: `<absolute temporary path>`
- Active workspace: `<absolute workspace path>`

## Execution
- Authority mode: `plan-first`, `direct-without-plan`, or `approved-plan`
- Output contract: `help`, `plan`, `blocking-question`, or `analysis`
- Finalizer: `<skill-relative Markdown path or not-applicable for Help>`
- Execution mode: `single`, `composition`, `plan-proposal`, or `approved-plan`
- Plan ID: `<stable invocation-local ID or none>`
- Plan state: `not-applicable`, `PROPOSED`, `APPROVED`, `BLOCKING_QUESTION`, or `COMPLETE`
- Blocking-decision threshold: `<0-100 percent; default 95%>`
- Step command: `<canonical command or none>`
- Total planned steps: `<positive integer or none>`
- Current step: `<positive integer of total, complete, or none>`
- Completed steps: `<ordered canonical step numbers and commands, or none>`
- Predecessor artifact set: `<absolute candidate and metadata paths, or none>`
- Prior-result handoff: `<source set, target set, and transferred result, or none>`
- Blocking question: `<stable question ID, active threshold, decision confidence below that threshold, evidence basis, affected step, and 2-3 variants, or none>`
- Canonical commands executed: `<ordered list or none>`
- Selected profile: `<profile ID or none>`
- Stop state: `<COMPLETE or exact STOP_* state>`

## Evidence
- Methodology sources consulted: `<ordered path and used/screened-only status, or none>`
- Evidence locations: `<ordered locations and purpose, or none>`
- Unresolved gaps: `<stable gap IDs or none>`

## Persistence
- Requested: `yes` or `no`
- Style: `plain`, `caprmedio`, or `not-applicable`
- Status: `DEFERRED_PENDING_VALIDATION`, `NOT_REQUESTED`, or exact stopped-unsaved state
- Planned action: `none`, `plain-exclusive-create`, or `caprmedio-governed-create`
- Planned destination: `<path, governed target, or none>`
- Durable report already created: `no`

## Candidate completeness
- Candidate finalizer check: `complete`
- Native result check: `complete` or exact stopped-before-native state
- Manager may release after PASS: `yes`
```

Do not use YAML frontmatter, JSON, or another sidecar. Lists may use multiple indented Markdown items, but the required field labels remain exact and appear once.

## Doer write and revision rules

The doer loads the finalizer before writing. On attempt 1 for a set, create both files. On manager-forwarded warden feedback, revise that set, increment `Attempt`, and replace both files in the same set directory. Replacement is permitted only before that set reaches warden `PASS`. A passed set is immutable. Never create `.bak`, numbered candidates inside a set, logs, verdicts, or caches.

The metadata must describe the exact current candidate, not intended future analysis. Every set records the same run directory, whole-task summary, Plan ID, authority mode, and active threshold unless the operator explicitly changes the threshold. A default proposal records `plan-first`, `plan`, `plan-proposal`, `PROPOSED`, no completed steps, and only `$fpf plan` as executed even when the invocation names analytical commands. A direct step records `direct-without-plan`; an approved Plan step records `approved-plan`. A step set records `step`, its one canonical command, its ordinal, and its passed predecessor set when present. A blocking question temporarily occupies the uncompleted current step set and records `BLOCKING_QUESTION`; after the answer that same unpassed set may be replaced. A final set records `final`, `COMPLETE`, every actually completed step, and every passed predecessor handoff.

Each step candidate is a complete temporary analytical artifact for that subtask. Its evidence and source trace cover that step while distinguishing inherited predecessor evidence. Intermediate step persistence is `NOT_REQUESTED`. Only a direct single-node set or the final consolidated set may declare deferred durable persistence.

Methodology sources list only direct FPF pages actually opened; prompts, Help, contracts, graphs, profiles, tools, and project evidence belong elsewhere. Evidence locations distinguish source evidence from routing or contract files. Unresolved gaps match the candidate. Persistence remains deferred until manager delivery, and `Durable report already created` remains `no`.

The doer returns only `STEP_READY`, `CANDIDATE_READY`, or `QUESTION_READY`, the set kind, the two exact paths, and the set-local attempt number. It never emits the candidate as its agent response and never sends feedback directly to the warden.

Return readiness only after both complete files have been written and read back. Missing or partial files remain production work, not a validation submission. The manager verifies readiness independently before dispatching the warden and follows the recovery procedure in `prompts/fpf-manager.md` if production is interrupted. A replacement receives the same unpassed set and preserved approved state only after the previous writer is confirmed stopped. Recovery increments the assigned attempt, preserves all passed sets, and creates no extra files; partial work remains unvalidated.

## Warden and manager rules

The warden is read-only and returns its verdict to the manager, never through a file. The manager forwards a `REVISE` response unchanged to the same doer. The manager never repairs candidate bytes.

`PASS` binds the verdict to the exact run ID, artifact set ID and kind, set-local attempt, candidate path, authority mode, Plan ID, Plan state, predecessor set, and blocking-question state. It does not prove a later modified file. The manager therefore rereads both files, freezes passed step sets, supplies only passed sets to later steps, and performs release or delivery without reshaping the validated final or single-call `candidate.md`.
