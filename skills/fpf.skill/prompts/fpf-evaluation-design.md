# FPF Evaluation Design

Produce a read-only **Evaluation Design Record**. Define how a bounded target will be evaluated; do not run the evaluation, claim a pass, improve the target, or make a release decision.

## Resolve scope and sources

1. Resolve the exact target and version or state, characteristic bearer, receiving use, evaluation question, authority, available evidence, risks, and protected trade-offs.
2. Use graph-declared `E.22` as the primary quality-question method and `A.19.ECS` as the evaluation-space projection. Use task-profile bindings to specialize tests, evidence, architecture, framework, or skill concerns.
3. If target identity, receiving use, or characteristic bearer is unresolved, return `insufficient basis` and the exact prerequisite rather than inventing metrics or tests.

## Design workflow

1. State one decision-relevant evaluation question without assuming that a preferred metric, test, proxy, or tool is valid.
2. Define characteristics, scales, levels or coordinates, observation or test operations, baselines, comparison rules, uncertainty, evidence, and validity or freshness windows.
3. Distinguish hard constraints, informative indicators, regression sentinels, exploratory checks, and separately authorized gates.
4. Define representative cases, counterexamples, failure paths, protected trade-offs, and the conditions for pass, fail, abstain, stop, refresh, or redesign of the evaluation.
5. Make the design rerunnable and recoverable. Stop before executing checks or converting results into assurance, authorization, or release.

## Boundaries

- A test, metric, dashboard, benchmark, or passing suite is an evaluation carrier or result, not automatically the quality characteristic or evidence claim.
- Do not collapse multiple quality coordinates into one score without a declared lawful aggregation and receiving use.
- Do not treat a gate profile as authority to release or transform the target.
- Remain read-only unless the user separately authorizes changes outside this analytical result.

## Native result requirements

1. **Target, bearer, receiving use, evaluation question, and resolved FPF source**
2. **Characteristics, scales, baselines, and protected trade-offs**
3. **Checks, cases, operations, evidence, and uncertainty plan**
4. **Comparison, regression, validity, and gate boundaries**
5. **Rerun contract and pass/fail/abstain/stop conditions**

Do not report evaluation results, improvement, assurance, approval, or release authorization.
