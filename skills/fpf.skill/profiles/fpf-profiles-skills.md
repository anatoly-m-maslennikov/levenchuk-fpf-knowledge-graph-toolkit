# FPF Skills Task Profiles

Load this file only when the task is about skill development. Select at most one profile. Match complete words or phrases, never substrings. A profile adds bounded FPF context but never changes the selected analytical command.

## `skills.trigger-and-scope` — Skill trigger and scope

Frame the skill's receiving use, task family, trigger boundary, exclusions, authority, and honest fallback.

- Aliases: `skill trigger`, `skill scope`, `skill task family`
- Routing cues: `trigger description`, `when to use skill`, `skill boundary`
- FPF context: `C.22@profile_context`, `E.11.PUR@profile_context`
- Example → `problem-frame`: Frame the problem and skill trigger boundary for this agent skill.
- Example → `alignment-audit`: Audit the installed skill trigger and scope against the accepted contract.
- Evaluation case `skills-trigger-eval` → `problem-frame`: Frame one skill task family and its trigger boundary.
- Required facets: receiving use, task family, positive trigger, exclusion, honest fallback
- Forbidden inference: A broad description improves routing coverage without increasing false activation.

## `skills.prompt-contract` — Skill prompt contract

Design and evaluate the reusable method description, inputs, outputs, gates, and quality contract carried by a skill prompt.

- Aliases: `skill prompt`, `prompt contract`, `skill instructions`
- Routing cues: `SKILL.md`, `prompt design`, `instruction contract`, `native result`
- FPF context: `A.3.2@profile_context`, `A.15.5@profile_context`, `E.22@profile_context`
- Example → `design-challenge`: Challenge this proposed skill prompt contract before publishing it.
- Example → `quality-improve`: Improve this versioned skill prompt and re-evaluate its contract.
- Evaluation case `skills-prompt-contract-eval` → `design-challenge`: Challenge a skill prompt contract, its inputs, outputs, gates, and authority.
- Required facets: task family, required input, native result, authority gate, honest fallback
- Forbidden inference: More instructions automatically improve skill behavior.

## `skills.graph-composition` — Skill graph and composition

Model skill nodes, order-sensitive compositions, handoffs, authority gates, and loop-prevention rules.

- Aliases: `skill graph`, `prompt graph`, `skill composition`
- Routing cues: `command graph`, `skill handoff`, `prompt composition`, `router`
- FPF context: `B.1.5@profile_context`, `C.24@profile_context`, `A.20@profile_context`
- Example → `structure-recover`: Recover the current skill graph, handoffs, and composition structure.
- Example → `options-explore`: Explore alternative skill-graph compositions without choosing one.
- Evaluation case `skills-graph-composition-eval` → `design-challenge`: Challenge a skill graph composition, its handoffs, authority gates, and loop prevention.
- Required facets: node authority, legal handoff, shared state, stop condition, loop budget
- Forbidden inference: A graph edge authorizes automatic execution.

## `skills.tool-and-context-connector` — Skill tools and context connector

Design tool-call planning, interfaces, dependency boundaries, and minimal context hydration for a skill.

- Aliases: `skill connector`, `context connector`, `skill tools`
- Routing cues: `tool call`, `context loading`, `Markdown graph`, `prompt link`
- FPF context: `C.24@profile_context`, `A.6.C@profile_context`, `B.1.1@profile_context`
- Example → `structure-recover`: Recover the current skill connector and tool-call dependency structure.
- Example → `design-challenge`: Challenge the proposed context connector before implementation.
- Evaluation case `skills-connector-eval` → `design-challenge`: Challenge a lazy context connector and its file-access plan.
- Required facets: selected input, dependency boundary, access precondition, returned context, failure path
- Forbidden inference: File availability proves that reading it is necessary or that its content is true.

## `skills.evaluation-cases` — Skill evaluation cases

Define representative tasks, expected artifacts, counterexamples, evidence, regression cases, and pass or stop rules.

- Aliases: `skill evaluation`, `skill evals`, `skill test cases`
- Routing cues: `evaluation pack`, `routing cases`, `golden cases`, `regression scenarios`
- FPF context: `G.4@profile_context`, `A.19.ECS@profile_context`, `A.21@profile_context`
- Example → `evaluation-design`: Design the skill evaluation cases and acceptance checks.
- Example → `alignment-audit`: Audit the implemented skill against its frozen skill evaluation cases.
- Evaluation case `skills-evaluation-cases-eval` → `evaluation-design`: Design skill evaluation cases with routing examples, counterexamples, evidence, and stop rules.
- Required facets: representative task, counterexample, expected artifact, evidence, pass or stop rule
- Forbidden inference: Structural validation proves semantic prompt quality.

## `skills.install-portability-and-runtime` — Skill installation, portability, and runtime

Analyze copied or linked installation, runtime discovery, compatibility, dependency, and cross-platform boundaries.

- Aliases: `skill installation`, `skill portability`, `skill runtime`
- Routing cues: `installer`, `installation`, `portability`, `runtime settings`, `cross platform`
- FPF context: `C.34@profile_context`, `A.20@profile_context`, `A.10@profile_context`
- Example → `design-challenge`: Challenge the proposed skill installation and portability design.
- Example → `alignment-audit`: Audit the installed skill runtime and compatibility evidence.
- Evaluation case `skills-install-runtime-eval` → `alignment-audit`: Audit skill installation, portability, runtime settings, and cross-platform behavior.
- Required facets: copy install, linked install, runtime discovery, settings ownership, platform boundary
- Forbidden inference: A successful source-level test proves the installed skill works.

## `skills.quality-regression-and-release` — Skill quality, regression, and release

Improve a versioned skill under stable evaluation cases and connect regression evidence to a bounded release decision.

- Aliases: `skill quality`, `skill regression`, `skill release`
- Routing cues: `skill maintenance`, `skill refactor`, `skill release gate`
- FPF context: `E.23@profile_context`, `B.3@profile_context`, `A.21@profile_context`
- Example → `quality-improve`: Improve this versioned skill regression target and rerun its evaluation.
- Example → `evaluation-design`: Design the skill release evaluation and gate profile.
- Evaluation case `skills-regression-eval` → `alignment-audit`: Audit a changed skill regression target against frozen routing and evaluation cases.
- Required facets: versioned target, frozen cases, rerun evidence, regressions, release boundary
- Forbidden inference: Passing deterministic tests alone proves semantic adequacy.
