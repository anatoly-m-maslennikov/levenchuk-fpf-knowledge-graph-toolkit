# FPF Options Explore

Produce a read-only **Candidate Exploration Pack**. Generate and compare options; do not make the receiving project decision.

## Resolve scope and FPF source

1. Resolve the question, Entity of Concern, bounded context, receiving use, evaluator, and decision owner from the request and accessible evidence.
2. Use graph-declared `B.5.2.1` as the primary method. Open conditional `G.9` only when the requested alternatives require benchmark or parity comparison.
3. Use six direct-pattern pages as the default ceiling; entry and index pages do not count. If the required edition or evidence cannot be verified, return `insufficient basis` and name the missing source.

## Review campaign continuation

Candidate evidence may inform owner disposition, but this node does not reset the campaign or recreate an existing defect as a new finding.

## Define the exploration contract

Before generating options, record:

- the question, scope, baseline, and receiving use;
- what counts as interesting, for whom, and relative to which familiar options;
- declared quality measures and protected constraints;
- novelty and diversity axes, admissible risk, cost, reversibility, and time horizon;
- evidence inputs, exploration budget, policy pins, and stop criteria.

If “interesting” remains undefined, ask for the missing distinctions or return `insufficient basis`; do not substitute an internet-average preference.

## Workflow

1. Generate a provenance-bearing `CandidateSet` using NQD-guided creative abduction. Keep hypotheses explicitly abductive.
2. Evaluate candidates only in the declared quality coordinates. Preserve useful diversity, archive state, and the applicable decision/reasoning record.
3. Treat novelty, diversity, illumination, coverage, and regret as telemetry unless the exploration contract explicitly promotes one into a decision criterion.
4. When comparison is requested, pin the baseline, comparator edition, freshness window, normalization or bridge rules, and policy. Produce `ParityPlan@Context` before `ParityReport@Context`.
5. Return the candidate set, Pareto front when justified, retained alternatives, evidence gaps, and handoff requirements. Do not silently collapse several measures into one opaque score.

## Boundaries

- Do not claim that a novel candidate is superior, selected, approved, or implementable.
- Do not manufacture diversity through cosmetic wording; distinguish candidates by declared mechanisms, structures, or trade-offs.
- Route an actual selection and ADR request to `$fpf decision synthesize` after candidates have recoverable evaluation evidence.
- Remain layer-agnostic and artifact-agnostic. Remain read-only unless the user separately authorizes implementation or file writes.

## Native result requirements

1. **Exploration contract and resolved FPF source**
2. **CandidateSet and provenance**
3. **Declared-coordinate evaluation and diversity map**
4. **Parity plan/report**, when applicable
5. **Retained options, exclusions, and evidence gaps**
6. **Stop condition and decision handoff**
