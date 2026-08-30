# FPF Software Task Profiles

Load this file only when the task is about software development. Select at most one profile. Match complete words or phrases, never substrings. A profile adds bounded FPF context but never changes the selected analytical command.

## `software.ddd-bounded-contexts` — DDD and bounded contexts

Recover exact model editions, use loci, bounded contexts, and cross-context relations before relying on DDD labels.

- Aliases: `DDD`, `domain driven design`, `bounded context`
- Routing cues: `bounded contexts`, `context map`, `domain model`, `ubiquitous language`
- FPF context: `A.1.1@profile_context`, `A.22@profile_context`, `F.9@profile_context`
- Example → `structure-recover`: Map current DDD bounded contexts and context relations.
- Example → `design-challenge`: Challenge the proposed DDD bounded-context split before implementation.
- Evaluation case `software-ddd-eval` → `structure-recover`: Recover current bounded-model uses and context relations before proposing a DDD redesign.
- Required facets: model edition, use locus, applicability relation, cross-context relation, missing discriminator
- Forbidden inference: A named bounded context is automatically a subsystem or team boundary.

## `software.business-logic` — Business logic and domain behavior

Recover business rules, state transitions, transformation flows, and constraints separately from their implementation carriers.

- Aliases: `business logic`, `domain logic`, `business rules`
- Routing cues: `state transition`, `domain behavior`, `workflow rules`, `invariants`
- FPF context: `A.3.3@profile_context`, `E.18@profile_context`, `A.20@profile_context`
- Example → `structure-recover`: Recover the current business logic, rules, and state transitions.
- Example → `options-explore`: Explore alternatives for implementing this business logic rule safely.
- Evaluation case `software-business-logic-eval` → `structure-recover`: Recover the business logic, domain rules, state transitions, and implementation carriers.
- Required facets: business rule, state transition, invariant, carrier, unresolved behavior
- Forbidden inference: Existing code structure is identical to the business logic model.

## `software.requirements-and-acceptance` — Requirements and acceptance

Frame software problems and decompose requirements, contracts, acceptance clauses, evidence, and action boundaries.

- Aliases: `software requirements`, `acceptance criteria`, `acceptance contract`
- Routing cues: `requirements`, `acceptance boundary`, `acceptance clauses`, `specification`
- FPF context: `C.22.2@profile_context`, `A.6.C@profile_context`, `G.4@profile_context`
- Example → `problem-frame`: Frame the software problem, requirements, and acceptance boundary.
- Example → `evaluation-design`: Design the evaluation and acceptance tests for these requirements.
- Evaluation case `software-requirements-eval` → `evaluation-design`: Design acceptance tests for software requirements and their acceptance clauses.
- Required facets: requirement bearer, acceptance clause, observable result, evidence, stop rule
- Forbidden inference: A written requirement is testable without an observable acceptance clause.

## `software.tdd` — Test-driven development

Analyze a project's TDD method through explicit behavior, evaluation questions, test evidence, and stopping rules.

- Aliases: `TDD`, `test driven development`, `test-first`
- Routing cues: `red green refactor`, `test first`, `test suite design`
- FPF context: `E.22@profile_context`, `A.19.ECS@profile_context`, `G.4@profile_context`
- Example → `evaluation-design`: Design the TDD evaluation frame and test strategy for this feature.
- Example → `quality-improve`: Improve this versioned TDD workflow and rerun its evaluation.
- Evaluation case `software-tdd-eval` → `evaluation-design`: Define the TDD evaluation frame for a feature before changing code.
- Required facets: observable behavior, test subject, evaluation operation, evidence, stop rule
- Forbidden inference: Test-first activity by itself proves improved software quality.

## `software.code-quality` — Code quality

Replace vague code-quality claims with exact bearers, characteristics, scales, trade-offs, and a rerunnable improvement loop.

- Aliases: `code quality`, `clean code`, `maintainability`
- Routing cues: `readability`, `complexity`, `cohesion`, `coupling`, `technical debt`
- FPF context: `C.16.Q@profile_context`, `C.25@profile_context`, `E.23@profile_context`
- Example → `evaluation-design`: Define measurable code-quality criteria and a verification plan.
- Example → `quality-improve`: Improve the code quality of this versioned module and re-evaluate it.
- Evaluation case `software-code-quality-eval` → `evaluation-design`: Define code quality criteria for maintainability, cohesion, coupling, and complexity.
- Required facets: quality bearer, characteristic, scale, trade-off, verification operation
- Forbidden inference: A clean-code label proves measurable code quality.

## `software.architecture` — Software architecture

Recover and evaluate selected software structures, candidate architectures, modularity, interfaces, and architectural decisions.

- Aliases: `software architecture`, `application architecture`, `system architecture`
- Routing cues: `architecture decision`, `module architecture`, `runtime architecture`, `data architecture`
- FPF context: `C.30@profile_context`, `C.31@profile_context`, `C.32@profile_context`
- Example → `structure-recover`: Recover the current software architecture and selected structures.
- Example → `options-explore`: Compare alternative software architecture candidates without selecting one.
- Evaluation case `software-architecture-eval` → `design-challenge`: Challenge a proposed software architecture and its claimed maintainability benefit.
- Required facets: architecture subject, selected structure, interface policy, quality bearer, causal boundary
- Forbidden inference: Low coupling by itself proves maintainability.

## `software.interfaces-dependencies-and-migration` — Interfaces, dependencies, and migration

Recover module relations, dependency direction, structural correspondence, compatibility, and migration boundaries.

- Aliases: `dependency migration`, `interface migration`, `module dependency`
- Routing cues: `API`, `interface`, `dependency`, `migration`, `compatibility`, `substitutability`
- FPF context: `A.6.M@profile_context`, `B.1.1@profile_context`, `C.34@profile_context`
- Example → `structure-recover`: Map current module dependencies and interface migration boundaries.
- Example → `design-challenge`: Challenge the proposed API migration and compatibility design.
- Evaluation case `software-interface-migration-eval` → `design-challenge`: Challenge an API interface migration and its dependency compatibility claim.
- Required facets: interface contract, dependency direction, compatibility bearer, migration boundary, rollback condition
- Forbidden inference: Matching method names prove substitutability.

## `software.release-evidence` — Release evidence and gates

Connect test and operational evidence to exact claims, assurance targets, and a separately authorized release gate.

- Aliases: `release evidence`, `release gate`, `deployment gate`
- Routing cues: `release readiness`, `test evidence`, `assurance`, `deployment`
- FPF context: `A.10@profile_context`, `B.3@profile_context`, `A.21@profile_context`
- Example → `evaluation-design`: Design the release-readiness evaluation, evidence, and gate checks.
- Example → `alignment-audit`: Audit the implemented release evidence against the accepted gate profile.
- Evaluation case `software-release-evidence-eval` → `alignment-audit`: Audit release evidence against the accepted release gate and assurance target.
- Required facets: release claim, evidence, assurance target, gate owner, residual risk
- Forbidden inference: A green test suite authorizes release.
