## Task, scope, and boundaries

Review the repository-managed `$fpf` end-user skill as the design baseline for its next revision. The receiving use is owner disposition: decide which repairs to authorize before implementation.

- **Target:** package version `0.1.2`, repository commit `92a5ba45ceb1e8032b8cb9cd331463385b78178b`, plus the installed Codex copy used for this run.
- **Scope:** skill packaging, routing, command composition, selective context loading, evaluation, installer/runtime settings, report persistence, maintainability, and user experience.
- **Excluded:** implementation, project approval, CAPRMEDIO internals, and original-FPF conversion except where they constrain the end-user skill.
- **Decision owner:** Anatoly. This review proposes findings and actions; it does not authorize them.
- **Evidence:** live repository inspection, three adversarial router probes, the complete deterministic suite, seven bounded FPF pages, and current primary documentation from OpenAI, the Agent Skills specification, Anthropic, and LangGraph.
- **Saved report:** `fpf-reports/20260828T112658Z-fpf-composition-review-current-fpf-skill-design.md`.

### Campaign handoff

- **Campaign:** `FPF-SKILL-DESIGN-20260828-92A5BA4`; phase `CHALLENGE_COMPLETE_AWAITING_OWNER_DISPOSITION`.
- **Semantic frontier:** the current single-entry `$fpf` design and its claims of lazy prompt-graph routing, legal composition, bounded context retrieval, one consolidated result, and portable installation.
- **Carrier frontier:** `skills/fpf.skill/**`, `skills/install_fpf_skills/**`, relevant `service/tests/fpf_skill/**`, installed runtime settings, and commit `92a5ba4`.
- **Evaluation profile:** task preservation, routing precision, composition validity, context economy, evidence traceability, semantic output quality, portability, persistence integrity, and maintenance cost.
- **Predecessor:** none supplied. Historical context was used only to preserve the established global end-user/project-local service boundary and additive settings migration.
- **Allowed next action:** owner disposition of findings and proposed repair batches. Do not repeat a full challenge on this unchanged frontier.

The requested one-run composition executed completely: `$fpf sota harvest` → `$fpf options explore` → `$fpf design challenge`. :codex-annotation{index="1"}

## High-confidence results (>=95%)

### 1. Composition execution and stop state

- **Executed prefix:** all three requested nodes.
- **Unexecuted suffix:** none.
- **Handoffs:** the evidence map supplied comparison axes; candidate exploration supplied four materially different alternatives; the challenge consolidated their implications against the current design.
- **Gate state:** no evidence or authority gate blocked read-only analysis. Mutation remains unauthorized.
- **Deterministic evidence:** router validation reports 12 nodes, 25 legal edges, 22 task profiles, and 9 declared evaluation cases. Repository validation passed, and all 18 maintenance-suite cases passed.
- **Stop reason:** the full challenge budget for this frozen frontier is consumed; findings now return to the owner.

### 2. SoTA synthesis

#### Harvest contract and coverage

The research frame was current practice for local agent skills and prompt/workflow graphs as of 2026-08-28. Included sources had to be primary specifications or official product/framework documentation. Community advice, popularity rankings, and generic prompt-engineering articles were excluded.

#### CorpusLedger

| Source | Tradition and admitted role | Freshness/use |
|---|---|---|
| [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills) | Codex/ChatGPT host behavior, discovery, progressive disclosure, `agents/openai.yaml`, trigger testing | Current page, accessed 2026-08-28 |
| [Agent Skills specification](https://agentskills.io/specification) | Portable package contract, frontmatter, resources, validation, progressive disclosure | Current specification, accessed 2026-08-28 |
| [Anthropic: Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) | Three-level context-loading model | Current page, accessed 2026-08-28 |
| [Anthropic: Claude Code skills](https://code.claude.com/docs/en/skills) | Invocation controls, concise bodies, native stacking, and skill evaluation | Current page, accessed 2026-08-28 |
| [OpenAI: Tool search](https://developers.openai.com/api/docs/guides/tools-tool-search) | Deferred loading and namespace-size guidance | Current page, accessed 2026-08-28 |
| [OpenAI: Programmatic Tool Calling](https://developers.openai.com/api/docs/guides/tools-programmatic-tool-calling) | Boundary between predictable coded orchestration and semantic model judgment | Current page, accessed 2026-08-28 |
| [OpenAI: Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals) | Trace grading, datasets, repeatable workflow evaluation | Current page, accessed 2026-08-28 |
| [LangGraph Graph API](https://langchain-ai.github.io/langgraph/how-tos/state-reducers/) | Explicit state, nodes, edges, reducers, compilation, and recursion limits | Current official documentation, accessed 2026-08-28 |

#### ClaimSheets and evidence anchors

1. **Progressive disclosure is a shared design principle.** OpenAI, the Agent Skills specification, and Anthropic all separate always-visible metadata, loaded skill instructions, and on-demand resources. The current 17-line `SKILL.md` aligns well; the composition runtime does not, because it hydrates all selected-node and profile pages before the first analytical node.
2. **Metadata is part of routing and product UX.** OpenAI explicitly makes implicit selection depend on the description and supports `agents/openai.yaml`; the portable specification supports `compatibility` and `metadata.version`. The current skill has a good concise description but omits host UI metadata and portable dependency/version declarations.
3. **Predictable control flow belongs in code; semantic judgment belongs with the model.** OpenAI recommends programmatic orchestration for predictable dependent calls with explicit limits and structured failure, while keeping semantic evaluation and approval-sensitive work direct. The current design scripts routing and hydration but leaves handoff validation, trace creation, and persistence compliance largely to prose.
4. **Workflow graphs need explicit state and validation beyond adjacency.** LangGraph's official model uses a shared state schema, node updates, edges, compilation checks, and execution limits. The FPF graph validates adjacency but has no machine-readable handoff schemas or gate predicates.
5. **Skill evaluation must separate activation from output quality.** Anthropic recommends fresh-session with/without baselines, assertion grading, token/duration measurement, blind version comparison, and positive/negative trigger tests. OpenAI recommends end-to-end traces first, then repeatable datasets. Current tests cover deterministic routing and data shape, not final analytical quality.

These traditions are complementary rather than interchangeable: the Agent Skills sources specify portable packaging; OpenAI and Anthropic add host behavior; LangGraph supplies a workflow-engine comparison, not a requirement to adopt LangGraph.

#### Receiving use and refresh condition

Refresh this evidence map when the Agent Skills specification, Codex/Claude skill-loading behavior, or the repository's execution architecture materially changes. Do not treat this bounded corpus as exhaustive.

### 3. Candidate exploration

#### Exploration contract

The baseline is the current single global `$fpf` package. Protected constraints are one end-user entrypoint, fast Help, English/Russian support, bounded FPF retrieval, a separate project-local service boundary, preserved settings history, and no autonomous review/fix loop.

#### CandidateSet and provenance

- **O1 — Patch the current architecture:** retain the prompt graph and prose runtime; repair parser defects, add tests, and add metadata. Lowest migration cost, but leaves model-enforced orchestration and weak observability.
- **O2 — Compiled hybrid:** retain one `$fpf` skill and YAML graph, but compile typed command grammar, handoff contracts, per-step context manifests, traces, and persistence validation into deterministic helpers. Model judgment remains inside analytical nodes. Medium migration cost and the best fit with the protected constraints.
- **O3 — Native skill split:** publish each analytical node as a separate host-native skill and keep `$fpf` only as a planner/router. Strong host-native progressive disclosure, but expands the global skill list, weakens the one-entry UX, and recreates collision/discovery concerns.
- **O4 — Workflow/plugin runtime:** move composition into a full workflow engine or plugin with durable state, tracing, retries, and typed node I/O. Strongest runtime guarantees; highest complexity and weakest cross-host portability.

#### Declared-coordinate parity map

| Option | One-entry UX | Task preservation | Context economy | Deterministic enforcement | Observability/evals | Cross-host portability | Migration cost |
|---|---|---|---|---|---|---|---|
| Current baseline | High | Low-Medium | Medium for single node; Low for stacks | Medium-Low | Low | Medium | None |
| O1 patch | High | High after fixes | Medium | Medium | Medium | High | Low |
| O2 compiled hybrid | High | High | High | High for control flow | High | Medium-High | Medium |
| O3 native split | Medium-Low | High | High | Host-dependent | Medium-High | Medium | Medium-High |
| O4 workflow/plugin | High | High | High | Very High | Very High | Low-Medium | High |

No option is selected by this analysis. O2 is retained as the most coherent improvement direction; O1 is a useful first repair batch; O3 and O4 remain boundary alternatives if the protected constraints change.

### 4. Consolidated issues and weak points

| ID | Severity | Challenge finding and evidence | Consequence | State |
|---|---|---|---|---|
| **F-01** | High | **Result: concern.** A stacked run hydrates every selected-node and profile binding at once. This run produced 7 patterns and 97,979 JSON characters before the first analysis. The runtime explicitly requests one all-node hydration, while the context builder materializes every binding. | Token/latency cost grows with stack length; later-node context can bias earlier work and defeats the claimed per-node laziness. | OPEN |
| **F-02** | High | **Result: concern.** Normalized alias length is used to slice original text. Probe: `$fpf as-is map architecture dependencies` returned only `dependencies`; `architecture` was lost. See [route_fpf.py](/Users/am/Documents/My_Repos/levenchuk-fpf-knowledge-graph-toolkit/skills/fpf.skill/scripts/route_fpf.py:354) and [composition.py](/Users/am/Documents/My_Repos/levenchuk-fpf-knowledge-graph-toolkit/skills/fpf.skill/scripts/route_fpf_workers/composition.py:20). | The analytical node may answer a materially different task without warning. | OPEN |
| **F-03** | High | **Result: concern.** Any task text containing spaced ` + ` is parsed as composition syntax. Probe: `design challenge Evaluate speed + safety tradeoffs` was rejected as an invalid second command. See [composition.py](/Users/am/Documents/My_Repos/levenchuk-fpf-knowledge-graph-toolkit/skills/fpf.skill/scripts/route_fpf_workers/composition.py:9). | Ordinary technical, mathematical, and trade-off language becomes unusable without an undocumented rewrite. | OPEN |
| **F-04** | Medium | **Result: concern.** English aliases and keywords use substring containment. Probe: `capital allocation` matched the `API` keyword and attached the interface/migration profile. See [route_fpf.py](/Users/am/Documents/My_Repos/levenchuk-fpf-knowledge-graph-toolkit/skills/fpf.skill/scripts/route_fpf.py:56). | Irrelevant FPF pages can be loaded and influence analysis; false matches grow with the profile catalog. | OPEN |
| **F-05** | High | **Result: concern.** The nine declared output-evaluation cases are only checked for valid references and non-empty fields; they are never run against skill outputs. Thirteen of 22 profiles have no declared output case. See [test_route_fpf.py](/Users/am/Documents/My_Repos/levenchuk-fpf-knowledge-graph-toolkit/service/tests/fpf_skill/test_route_fpf.py:168). | Passing 18 deterministic tests proves structural correctness, not routing robustness, analytical completeness, language parity, or improvement over no skill. | OPEN |
| **F-06** | High | **Result: concern.** Graph edges contain only `from`, `to`, and a prose relation. Validation checks node existence, not input/output shape, required evidence, or gate predicates. | A legal edge can still deliver an unusable handoff; the model must infer contracts and stop behavior repeatedly. | OPEN |
| **F-07** | Medium-High | **Result: concern.** Routing and bounded file access are scripted, but composition state, gate checks, source-use traces, exact chat/report identity, and non-overwriting persistence are enforced mainly by instructions. No machine-readable run receipt or artifact hash is produced. | Failures are difficult to replay, grade, or distinguish from model noncompliance; persistence can drift from the returned artifact. | OPEN |
| **F-08** | Medium | **Result: concern.** The source folder `fpf.skill` does not match frontmatter `name: fpf`, so it is installer-shaped rather than directly conforming to the portable directory-name rule. The installed copy is normalized, but the package also lacks standard `compatibility`/version metadata and OpenAI's optional `agents/openai.yaml`. | Direct validation/distribution is weaker, dependencies are implicit, and Codex renders the UI name as “Fpf” rather than a controlled “FPF.” | OPEN |
| **F-09** | Low | **Result: concern.** The persistence contract still says “seven executable FPF skills,” while the graph and README define ten. See [fpf-report-persistence.md](/Users/am/Documents/My_Repos/levenchuk-fpf-knowledge-graph-toolkit/skills/fpf.skill/references/fpf-report-persistence.md:3). | Documentation drift reduces trust in generated/shared contracts and is not caught by current checks. | OPEN |
| **F-10** | Medium | **Result: concern.** Validation hard-codes the exact analytical-node set and minimum catalog counts instead of compiling behavior from typed declarations. See [route_fpf.py](/Users/am/Documents/My_Repos/levenchuk-fpf-knowledge-graph-toolkit/skills/fpf.skill/scripts/route_fpf.py:198). | Every graph extension requires synchronized Python, YAML, tests, Help, and prose edits; count checks can pass while semantic coverage remains uneven. | OPEN |

### 5. Strengths within inspected scope

- The 17-line entrypoint and direct Help bypass are genuinely thin and match progressive-disclosure practice.
- One global end-user skill plus project-local service skills avoids the duplicate-name discovery problem; OpenAI documents that same-name skills are shown separately rather than merged.
- Explicit compositions fail closed on unknown commands and illegal adjacency; typo suggestions do not execute silently.
- Context hydration verifies safe relative paths, FPF IDs, source revisions, and bounded core sections.
- Installed settings correctly carry package version `0.1.2` and the absolute local repository path; the installer preserves versioned settings snapshots.
- The live checkout was clean before report creation, repository validation passed, and all 18 deterministic suite cases passed.

### 6. Consolidated fixes and improvements

| Action | Exact proposed repair | Findings | Owner/authority | Dependencies and order | Verification | State |
|---|---|---|---|---|---|---|
| **A-01** | Replace word-count slicing with source-span parsing; use boundary-aware token matching; add an explicit `--` task delimiter or escaping rule so literal ` + ` is safe. | F-02, F-03, F-04 | Maintainer; owner authorizes behavior change | First | Regression probes preserve the complete task; positive/negative English/Russian corpora show no substring leakage. | PROPOSED |
| **A-02** | Change composition hydration to return a compact manifest first, then hydrate only the current node's bindings with a total context budget and reusable cache keyed by graph/source revision. | F-01, F-07 | Maintainer | After A-01; before broad evals | This same stack loads only G.2 initially; measured peak context, time, and tokens improve without source-loss regressions. | PROPOSED |
| **A-03** | Add typed node input/output and handoff contracts, gate predicates, and stop reasons to YAML; compile and validate the graph before routing. | F-06, F-10 | Maintainer; owner approves schema revision | After grammar stabilization | Every edge has a producer schema, consumer schema, and executable compatibility/gate test; invalid compositions fail with the exact missing field. | PROPOSED |
| **A-04** | Build a real skill-eval harness: fresh-session with/without baseline, positive and negative triggers, task-preservation assertions, final-artifact facets, source-trace checks, English/Russian parity, blind A/B, tokens, time, and representative stack trajectories. Cover all 22 profiles or explicitly justify exclusions. | F-01–F-06, F-10 | Maintainer/evaluator | Uses A-01 to A-03 contracts | Machine-readable eval results show pass rate, evidence per assertion, latency/token overhead, and version comparison; semantic cases are executed, not only schema-checked. | PROPOSED |
| **A-05** | Emit one machine-readable composition receipt with invocation, resolved nodes/profile, graph and source revisions, per-node context IDs, gates, stop state, timings, findings/actions IDs, final artifact hash, and report path. | F-05, F-07 | Maintainer | After typed contracts | A failed or stopped run is replayable; the receipt and Markdown agree on executed nodes, sources, gates, and hash. | PROPOSED |
| **A-06** | Move plain report creation into an atomic deterministic helper that selects a non-existing filename, writes UTF-8 once, and verifies the chat/report content hash. Keep CAPRMEDIO as a separate governed adapter. | F-07 | Maintainer; existing persistence authority | Can follow A-05 | Concurrent-save and collision tests pass; saved bytes hash to the finalized artifact; no overwrite occurs. | PROPOSED |
| **A-07** | Make the source package directly standards-valid or clearly mark it as an installer source; add portable `metadata.version` and `compatibility`, plus `agents/openai.yaml` for “FPF” display metadata and invocation policy. Validate both source and installed artifacts. | F-08 | Maintainer; owner chooses source-folder migration | Independent after A-01 | Agent Skills reference validation passes; Codex shows “FPF”; Codex and Claude smoke installs still route Help and one analysis. | PROPOSED |
| **A-08** | Generate inventory-dependent prose and Help fragments from YAML, or lint every stated node/profile count and persisted-node label against the graph. | F-09, F-10 | Maintainer | After schema choice | Deliberately changing node count fails checks until generated/docs output is refreshed; “seven” cannot survive with ten nodes. | PROPOSED |

Recommended execution order is A-01 → A-02 → A-03 → A-04 → A-05/A-06 → A-07/A-08. This is a proposed repair sequence, not project authorization.

### 7. Verification, residual risk, and coverage

- **Applied or verified repairs:** none; this run was read-only.
- **Verified current behavior:** all declared deterministic checks pass, and F-02 through F-04 reproduce on the live router despite that green suite.
- **Residual risk:** semantic output quality and cross-host runtime cost remain unmeasured; the current green status must not be interpreted as design adequacy.
- **Coverage limit:** no CAPRMEDIO path, Claude installation, concurrent report write, or model-version matrix was executed.
- **Successor condition:** after an authorized repair batch changes meaning, run a delta design challenge on the changed claims; after application, run one alignment audit against the frozen finding IDs and regression matrix.

## Open questions (confidence <95%)

### Q-01 — Actual context and latency cost across hosts (92%)

Best current answer: F-01 is materially expensive because the hydrated bundle is 97,979 characters, but tokenization, caching, and latency vary by host/model. Missing evidence: instrumented Codex and Claude runs over single-node and 2–4-node stacks. Consequence: the exact priority of A-02 relative to A-01 is not quantified. Next action: add token/time telemetry to A-04 and benchmark current versus per-step hydration.

### Q-02 — `uv` project-lock warning (85%)

Every live `uv run` emitted `Failed to acquire project environment lock: Could not create temporary file`, while commands and all tests succeeded. The project and `.venv` were writable, so the root cause is unresolved. Consequence: noisy runtime and a possible concurrency/cache defect remain outside the skill-design verdict. Next action: reproduce with verbose `uv` diagnostics and a clean temporary clone/environment; do not attribute it to the FPF parser without evidence.

### Q-03 — Directly portable source folder versus installer-only source (92%)

Best current answer: retaining `fpf.skill` is acceptable only if the repository explicitly defines it as an installer source and validates the normalized installed `fpf/` artifact. Missing input: the owner's intended distribution contract. Consequence: A-07 could be either a folder rename or a documentation/validation clarification. Next action: decide whether users may copy the repository package directly without the installer.

## Skills used

- `$fpf sota harvest` — built the bounded current evidence map and preserved differences among packaging, host, orchestration, and evaluation traditions.
- `$fpf options explore` — generated and compared four materially different architectural directions without selecting one.
- `$fpf design challenge` — challenged the current design baseline and consolidated the complete finding/action registries.

#### FPF sources consulted (7 read; 7 used)

- `FPF-Knowledge-Graph/G_Discipline SoTA Patterns Kit/03_02_SoTA Harvester & Synthesis/00_G.02 - SoTA Harvester & Synthesis.md` — **used** by SoTA harvest for corpus, plurality, evidence, and refresh boundaries.
- `FPF-Knowledge-Graph/B_Trans-disciplinary Reasoning Cluster/04_05_Canonical Reasoning Cycle/02_Abductive Loop/02_B.05.02.01 - Creative Abduction with NQD.md` — **used** by options exploration for materially distinct candidates.
- `FPF-Knowledge-Graph/G_Discipline SoTA Patterns Kit/10_09_Parity and Benchmark Harness/00_G.09 - Parity and Benchmark Harness.md` — **used** by options exploration for declared-coordinate comparison.
- `FPF-Knowledge-Graph/E_The FPF Constitution and Authoring Guides/10_11_First-Practical Entry and Pattern-Use Discoverability Discipline/01_E.11.PUA - Pattern Use in a Working Situation and First Useful Result.md` — **used** by design challenge for receiving-use, reliance, and decision-boundary checks.
- `FPF-Knowledge-Graph/B_Trans-disciplinary Reasoning Cluster/00_01_Holon Aggregation and Part-Whole Construction/05_B.01.05 - Gammamethod - Order-Sensitive Method Composition and Work Enactment.md` — **used** for ordered composition and handoff boundaries.
- `FPF-Knowledge-Graph/C_Kernel Extension Specifications/12_24_Agentic Tool-Use and Call Planning (C.Agent-Tools-CAL)/00_C.24 - Agentic Tool-Use and Call Planning (C.Agent-Tools-CAL).md` — **used** for plan/work separation, call-state, and stop rules.
- `FPF-Knowledge-Graph/A_Kernel Architecture Cluster/20_Constraint Validity for Transformation Steps/00_A.20 - Constraint Validity for Transformation Steps.md` — **used** to separate tested constraints, not-run states, and project gate decisions.

<oai-mem-citation>
<citation_entries>
MEMORY.md:1128-1137|note=[Preserved bounded retrieval, service boundary, and settings history constraints]
</citation_entries>
<rollout_ids>
019fb801-af36-7993-8d2c-b98cbd0dfc55
01a0267c-29db-7682-a17c-ba04199e3576
</rollout_ids>
</oai-mem-citation>
