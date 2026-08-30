# FPF Framework Task Profiles

Load this file only when the task is about framework development. Select at most one profile. Match complete words or phrases, never substrings. A profile adds bounded FPF context but never changes the selected analytical command.

## `framework.problem-and-scope` — Framework problem and scope

Frame the recurring problem, intended users, authority, and boundary before creating framework structure.

- Aliases: `framework problem`, `framework scope`
- Routing cues: `framework requirements`, `framework boundary`, `framework purpose`
- FPF context: `C.22@profile_context`, `E.4.PFAD@profile_context`
- Example → `problem-frame`: Frame the framework problem and acceptance boundary for this initiative.
- Example → `design-challenge`: Challenge the proposed framework scope before authoring it.
- Evaluation case `framework-problem-scope-eval` → `problem-frame`: Frame the framework problem, receiving use, authority, and acceptance boundary.
- Required facets: recurring problem, receiving use, authority, scope boundary, acceptance boundary
- Forbidden inference: A broad framework purpose is an executable requirement.

## `framework.concepts-and-terminology` — Framework concepts and terminology

Recover or improve load-bearing concepts, kinds, distinctions, and names without confusing wording with ontology.

- Aliases: `framework terminology`, `framework concepts`
- Routing cues: `concept model`, `kind boundary`, `framework vocabulary`, `terminology`
- FPF context: `E.10@profile_context`, `F.18@profile_context`, `A.7@profile_context`
- Example → `structure-recover`: Recover the current structure of the framework terminology and kind boundaries.
- Example → `quality-improve`: Improve this versioned framework terminology using its quality criteria.
- Evaluation case `framework-concept-boundary-eval` → `design-challenge`: Challenge proposed framework terminology and a concept split without treating wording as ontology.
- Required facets: exact subject, kind boundary, intended use, nearest false inference, decision owner
- Forbidden inference: A clearer label proves a valid ontological distinction.

## `framework.pattern-authoring` — Framework pattern authoring

Design and assess framework patterns, their owning framework, applicability, and edition discipline.

- Aliases: `pattern authoring`, `framework pattern`
- Routing cues: `author pattern`, `pattern contract`, `pattern framework relation`
- FPF context: `E.4.DPF@profile_context`, `E.4.PFR@profile_context`
- Example → `options-explore`: Explore alternatives for authoring this new framework pattern.
- Example → `alignment-audit`: Audit the implemented framework pattern against its authoring contract.
- Evaluation case `framework-pattern-authoring-eval` → `design-challenge`: Challenge a framework pattern authoring proposal and its applicability contract.
- Required facets: owning framework, recurring problem, applicability, pattern contract, edition discipline
- Forbidden inference: One successful example proves a reusable framework pattern.

## `framework.architecture` — Framework architecture

Recover, synthesize, compare, or challenge the selected structures that make a framework usable and maintainable.

- Aliases: `framework architecture`, `framework structure`
- Routing cues: `framework modules`, `framework dependencies`, `framework organization`
- FPF context: `E.4@profile_context`, `C.30@profile_context`, `C.32@profile_context`
- Example → `structure-recover`: Map current framework architecture and dependencies as-is.
- Example → `design-challenge`: Stress-test the proposed framework architecture before implementation.
- Evaluation case `framework-architecture-eval` → `structure-recover`: Recover the current framework architecture, modules, and dependencies before redesign.
- Required facets: selected structure, module boundary, dependency, receiving use, unknown relation
- Forbidden inference: Folder structure is automatically framework architecture.

## `framework.edition-and-migration` — Framework edition and migration

Preserve framework identity, pattern relations, and intended use across editions, migrations, and integrations.

- Aliases: `framework migration`, `framework edition`
- Routing cues: `edition compatibility`, `framework upgrade`, `framework integration`
- FPF context: `E.4.PFR@profile_context`, `E.4.PFIP@profile_context`, `C.34@profile_context`
- Example → `evaluation-design`: Design an evaluation plan for framework edition compatibility.
- Example → `alignment-audit`: Audit the completed framework migration for semantic preservation.
- Evaluation case `framework-edition-preservation-eval` → `alignment-audit`: Audit a completed framework edition migration for preserved pattern identity and intended use.
- Required facets: source edition, target edition, correspondence basis, lost content, reopen condition
- Forbidden inference: Matching filenames prove semantic preservation.

## `framework.publication-and-discoverability` — Framework publication and discoverability

Make framework forms, practical entries, and pattern-use routes discoverable without turning examples into compulsory workflows.

- Aliases: `framework publication`, `framework discoverability`
- Routing cues: `practical entry`, `publication form`, `help navigation`
- FPF context: `E.11.PFP@profile_context`, `E.11.PUR@profile_context`
- Example → `applicability-scan`: Find relevant FPF patterns for framework publication discoverability.
- Example → `design-challenge`: Challenge the proposed framework help and practical-entry design.
- Evaluation case `framework-publication-eval` → `design-challenge`: Challenge framework publication and discoverability through its help navigation.
- Required facets: audience, practical entry, navigation route, optional example, false prescription risk
- Forbidden inference: A published example is a compulsory workflow.

## `framework.quality-and-coverage` — Framework quality and coverage

Define and improve framework quality, structural coverage, missing information, and protected trade-offs.

- Aliases: `framework quality`, `framework coverage`
- Routing cues: `coverage gaps`, `framework completeness`, `framework quality criteria`
- FPF context: `E.22@profile_context`, `E.23@profile_context`, `C.33@profile_context`
- Example → `evaluation-design`: Define the quality criteria and evaluation frame for framework coverage.
- Example → `quality-improve`: Improve the versioned framework coverage and re-evaluate it.
- Evaluation case `framework-coverage-eval` → `evaluation-design`: Define a framework coverage evaluation without collapsing coverage into page count.
- Required facets: coverage bearer, receiving use, characteristic, scale, missing-structure return
- Forbidden inference: More patterns automatically mean better coverage.
