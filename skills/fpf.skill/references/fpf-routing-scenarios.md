# FPF Routing Scenarios

This maintainer fixture records expected routing behavior for the Markdown command graph. It is not runtime context and must not be loaded by normal `$fpf` calls.

| ID | Expected route | Mode | Route action | Question | Stop condition |
|---|---|---|---|---|---|
| `frame-development-problem` | `problem-frame` | single | calls | Frame the problem, task signature, and acceptance boundary before solution work. | Stop at the earliest honest problem-side result without generating options. |
| `recover-current-structure` | `structure-recover` | single | calls | Recover the current structure, relations, and boundaries as-is without redesigning them. | Return the smallest supported current-state map and exact missing information. |
| `discover-relevant-patterns` | `applicability-scan` | single | calls | Which FPF patterns directly apply to a bounded service-design question? | Return the smallest relevant direct-pattern set without proposing a full lifecycle. |
| `map-current-field` | `sota-harvest` | single | calls | Build a current, plural evidence map for a bounded technical field. | Stop after the reconstructible field map. |
| `generate-alternatives` | `options-explore` | single | calls | Generate diverse alternatives for a defined problem and compare them on declared coordinates. | Return compared options without selecting one. |
| `design-rerunnable-evaluation` | `evaluation-design` | single | calls | Design the evaluation frame, success criteria, checks, evidence, and stop rules without running it. | Return a rerunnable evaluation design without claiming a pass. |
| `challenge-proposal` | `design-challenge` | single | calls | Stress-test a concrete design proposal before implementation. | Return the bounded challenge; do not approve or implement it. |
| `record-decision` | `decision-synthesize` | single | calls | Choose among already evaluated alternatives and produce a recoverable decision record. | Do not invent new alternatives. |
| `improve-versioned-target` | `quality-improve` | single | calls | Improve a versioned artifact using its baseline and declared evaluation frame. | Do not expand the authorized change surface. |
| `audit-implemented-work` | `alignment-audit` | single | calls | Audit completed work against the relevant FPF patterns with replayable evidence. | Do not treat the audit as proposal approval. |
| `research-options-decision` | `sota-harvest` → `options-explore` → `decision-synthesize` | sequence | calls | Use current external evidence to develop alternatives, then support the authorized owner in choosing one. | Stop unless evidence, evaluated alternatives, and decision authority are recoverable. |
| `challenge-then-decide` | `design-challenge` → `decision-synthesize` | sequence | calls | Challenge one concrete candidate, then decide among the already evaluated alternatives. | Stop after challenge if authority or comparable evidence is missing. |
| `composed-challenge-improve-closure` | `design-challenge` → `quality-improve` → `alignment-audit` | composition | calls | `$fpf design challenge + quality improve + alignment audit Strengthen this versioned proposal and verify the accepted repair set.` | Share one finding registry and stop at unmet authority gates. |
| `meta-plan-research-options-challenge` | `sota-harvest` → `options-explore` → `design-challenge` | plan | calls | `$fpf plan sota harvest + options explore + design challenge Assess the current proposal.` | Return the stack without execution or persistence. |
| `campaign-applied-repairs-closure` | `alignment-audit` | closure | calls | The accepted repair batch is applied. Verify only registered findings and the frozen regression matrix. | Do not widen scope. |
| `campaign-unchanged-frontier-stop` | — | stop | stop | The same semantic frontier and evaluation profile already used their full challenge and audit budgets. Review it again. | Return no FPF call. |
| `campaign-repairs-not-applied` | — | external | external_action | The owner accepted the registered repairs, but they have not been applied. What FPF review runs next? | Apply repairs before closure review. |
| `campaign-material-semantic-change` | `design-challenge` | full | calls | An accepted repair materially changed the proposal's meaning. Challenge the successor semantic frontier. | Review the successor frontier once and preserve the predecessor. |
