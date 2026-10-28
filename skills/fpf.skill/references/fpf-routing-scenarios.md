# FPF Routing Scenarios

This maintainer fixture records expected routing behavior for the Markdown command graph. It is not runtime context and must not be loaded by normal `$fpf` calls.

| ID | Expected route | Mode | Route action | Question | Stop condition |
|---|---|---|---|---|---|
| `frame-development-problem` | `problem-frame` | plan | plans | Frame the problem, task signature, and acceptance boundary before solution work. | Propose the earliest honest problem-side result without generating options. |
| `recover-current-structure` | `structure-recover` | plan | plans | Recover the current structure, relations, and boundaries as-is without redesigning them. | Propose the smallest supported current-state recovery. |
| `discover-relevant-patterns` | `applicability-scan` | plan | plans | Which FPF patterns directly apply to a bounded service-design question? | Propose the smallest relevant direct-pattern scan without a full lifecycle. |
| `map-current-field` | `sota-harvest` | plan | plans | Build a current, plural evidence map for a bounded technical field. | Propose the bounded evidence harvest. |
| `generate-alternatives` | `options-explore` | plan | plans | Generate diverse alternatives for a defined problem and compare them on declared coordinates. | Propose option exploration without selection. |
| `design-rerunnable-evaluation` | `evaluation-design` | plan | plans | Design the evaluation frame, success criteria, checks, evidence, and stop rules without running it. | Propose evaluation design without claiming a pass. |
| `challenge-proposal` | `design-challenge` | plan | plans | Stress-test a concrete design proposal before implementation. | Propose one bounded challenge; do not execute it. |
| `record-decision` | `decision-synthesize` | plan | plans | Choose among already evaluated alternatives and produce a recoverable decision record. | Propose decision synthesis without inventing alternatives. |
| `improve-versioned-target` | `quality-improve` | plan | plans | Improve a versioned artifact using its baseline and declared evaluation frame. | Propose bounded improvement under the authorized surface. |
| `audit-implemented-work` | `alignment-audit` | plan | plans | Audit completed work against the relevant FPF patterns with replayable evidence. | Propose the audit without treating it as approval. |
| `research-options-decision` | `sota-harvest` → `options-explore` → `decision-synthesize` | plan | plans | Use current external evidence to develop alternatives, then support the authorized owner in choosing one. | Propose the sequence; exact `do` is required before execution. |
| `challenge-then-decide` | `design-challenge` → `decision-synthesize` | plan | plans | Challenge one concrete candidate, then decide among the already evaluated alternatives. | Propose the sequence and expose its authority gate. |
| `composed-challenge-improve-closure` | `design-challenge` → `quality-improve` → `alignment-audit` | composition-direct | calls | `$fpf design challenge + quality improve + alignment audit Strengthen this versioned proposal and verify the accepted repair set. Execute without a plan.` | Share one finding registry and stop at unmet authority gates. |
| `meta-plan-research-options-challenge` | `sota-harvest` → `options-explore` → `design-challenge` | plan | plans | `$fpf plan sota harvest + options explore + design challenge Assess the current proposal.` | Return the stack without execution or persistence. |
| `default-plan-command-stack` | `sota-harvest` → `design-challenge` → `quality-improve` | plan | plans | `$fpf sota harvest + design challenge + quality improve Review the current repository.` | Return the stack as a Plan; command text alone is not execution authority. |
| `campaign-applied-repairs-closure` | `alignment-audit` | closure | calls | The accepted repair batch is applied. Verify only registered findings and the frozen regression matrix. | Do not widen scope. |
| `campaign-unchanged-frontier-stop` | — | stop | stop | The same semantic frontier and evaluation profile already used their full challenge and audit budgets. Review it again. | Return no FPF call. |
| `campaign-repairs-not-applied` | — | external | external_action | The owner accepted the registered repairs, but they have not been applied. What FPF review runs next? | Apply repairs before closure review. |
| `campaign-material-semantic-change` | `design-challenge` | full | calls | An accepted repair materially changed the proposal's meaning. Challenge the successor semantic frontier. | Review the successor frontier once and preserve the predecessor. |
