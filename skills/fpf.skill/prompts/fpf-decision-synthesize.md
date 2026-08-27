# FPF Decision Synthesize

Produce a **Decision Package** in two ordered stages: the project decision relation, then its ADR-like publication projection. Do not let the record impersonate the decision or its authority.

## Resolve scope and FPF source

1. Resolve the decision question, Entity of Concern, evaluated candidates, decision owner, authority, evidence, criteria, constraints, affected structures, receiving work, and publication audience.
2. Use graph-declared `C.32.PAD` as the primary decision method and `C.32.ADR` as its result projection. Use six direct-pattern pages as the default ceiling; entry and index pages do not count.
3. If candidate synthesis, comparison evidence, or project authority is missing, return `insufficient basis` and the exact prerequisite; never invent a decision.

## Review campaign continuation

A decision owner may move a registered finding from `OPEN` to `DECIDED` when the decision relation supplies recoverable authority and evidence; otherwise leave its state unchanged.

## Stage 1: decision relation

1. Confirm that alternatives are materially distinct and recoverably evaluated. Route missing option generation or parity work to `$fpf options explore`.
2. Record the selected configuration only when the project decision owner or authoritative evidence supplies the selection.
3. Record the decision question, considered options, governing criteria, evidence, rationale, accepted losses, affected structures, method/work consequences, dependencies, confirmation path, and explicit reopen trigger.
4. If selection is not yet authorized, produce a **Decision-Ready Proposal** and identify the remaining owner action; do not label it decided.

## Stage 2: ADR projection

1. Project the recoverable decision relation for the named audience and receiving use.
2. Include question, context, options, outcome, rationale, accepted trade-offs, consequences, confirmation path, source links, status, and supersession condition.
3. Preserve traceability back to the decision relation and evaluated candidates. Tailor presentation without changing decision meaning.

## Boundaries

- An ADR file is not the decision, architecture, candidate comparison, authority act, or implementation.
- Do not convert an FPF recommendation into project approval or claim that FPF selected the option.
- Do not create a false consensus when evidence or authority remains contested.
- Remain layer-agnostic and artifact-agnostic. Write or modify project records only when the user authorizes it.

## Native result requirements

1. **Decision contract, authority, and resolved FPF source**
2. **Candidate and evidence readiness**
3. **Decision relation or Decision-Ready Proposal**
4. **ADR projection**, only when its source relation is recoverable
5. **Accepted losses, consequences, and reopen triggers**
6. **Unresolved authority/evidence and implementation handoff**
