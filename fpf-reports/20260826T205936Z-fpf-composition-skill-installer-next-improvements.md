## Task, scope, and boundaries

Executed the previously prepared composition for the current end-user FPF skill and installer architecture. :codex-annotation{index="1"}

- Composition: `$fpf sota harvest + options explore + design challenge`
- Shared task: identify the strongest next improvements before further implementation.
- Receiving use: give the owner one deduplicated weakness list and one mapped improvement list, without selecting or implementing a project decision.
- Preserved constraints: FPF remains standalone by default; the repository installs only service skills locally; Codex receives one global end-user `fpf` skill; routing and validation remain deterministic; copy and symlink installation remain cross-platform concerns; CAPRMEDIO is optional.
- Semantic frontier: repository `levenchuk-fpf-knowledge-graph-toolkit`, branch `dev`, commit `18d0c5b`, version `0.1.1`.
- Carrier frontier: repository source plus the Personal Codex installation at `~/.codex/skills/fpf`.
- Evaluation profile: entry-point cost, routing predictability, deployment currentness, machine-local settings ownership, bilingual behavior, composition safety, artifact-level validation, and portability.
- Excluded: code changes, installer execution with `--apply`, project decision/ADR, CAPRMEDIO report admission, a Windows runtime trial, and a quantitative Codex UI latency benchmark.
- Campaign ID: `FPF-SKILL-ARCH-2026-08-27-01`.
- Stop condition: one SoTA harvest, one alternative-generation pass, and one design-challenge pass, followed by consolidation. That condition was reached.
- Report style: `plain`; this is a non-normative analysis artifact.
- Saved report: `fpf-reports/20260826T205936Z-fpf-composition-skill-installer-next-improvements.md`

## High-confidence results (>=95%)

### 1. Composition execution and stop state

The nodes executed in this order:

1. `$fpf sota harvest` — built the bounded evidence map and separated neighboring solution traditions.
2. `$fpf options explore` — generated five materially different architecture/operation options without choosing a winner.
3. `$fpf design challenge` — challenged the low-cost hardening option against the shared evidence and current repository state.

All three nodes completed. The campaign stopped after the first challenge pass because it produced stable, actionable findings; no repair was authorized, so no improvement or alignment-audit loop was entered. Every action below remains **PROPOSED** and requires owner disposition.

#### SoTA harvest contract

- Question: what current skill/prompt/workflow practices most strongly inform the next improvement of this FPF skill and its installer?
- Inclusion rule: primary specifications or official documentation that directly constrain skill packaging, discovery, prompt invocation, workflow state, or language identification; direct FPF patterns used by the composition method.
- Exclusion rule: secondary tutorials, vendor-comparison articles, generic “agent framework” surveys, and implementation advice without a primary contract.
- Freshness: current official web documentation accessed on 2026-08-27 in Asia/Tbilisi; stable RFC and repository-local FPF edition treated as enduring sources.
- Coverage floor: four distinct external traditions, exceeding the FPF `k = 3` plural-tradition floor.

#### Corpus ledger and claim sheets

| Tradition | Primary evidence | Material claim used | Confidence |
|---|---|---|---:|
| T1 — filesystem skills and progressive disclosure | [OpenAI Codex Skills](https://developers.openai.com/codex/skills), [Agent Skills specification](https://agentskills.io/specification), [Anthropic Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) | A skill can remain a small folder whose entry metadata loads first and whose instructions/resources load only when needed. Codex supports user and repository scopes; same-named skills are not merged. | 99% |
| T2 — user-controlled prompt registries | [MCP Prompts](https://modelcontextprotocol.io/specification/draft/server/prompts) | Discoverable, argument-bearing prompts can be exposed as explicit user commands. This is a distribution/discovery alternative, not automatically a better runtime for a small local skill. | 97% |
| T3 — durable workflow runtimes | [LangGraph workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents), [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) | Shared state, checkpoints, resume, and idempotent side-effect discipline become valuable for long-running or interruptible workflows. They add infrastructure that a short instruction-driven composition may not need. | 97% |
| T4 — language identification | [RFC 5646 / BCP 47](https://www.rfc-editor.org/info/rfc5646/) | Standard language tags provide a scalable identity and fallback basis when localization grows beyond two simple language choices. | 99% |

The traditions were not silently fused. T1 governs package loading, T2 governs prompt discovery, T3 governs durable execution, and T4 governs locale identity. The current repository primarily implements T1; it borrows explicit command semantics from T2 without needing an MCP server, and it does not yet have a receiving use that requires T3 or a locale set that requires full T4.

#### SoTA synthesis and bridges

- The 15-line source `skills/fpf.skill/SKILL.md`, separate Help resources, and deferred `fpf-runtime.md` agree with the progressive-disclosure model. This is a confirmed strength, not a redesign target. Confidence: 99%.
- Keeping one globally installed end-user `fpf` package and repository-only service skills is especially important because Codex documents that same-named skills from different locations are not merged and can both appear. Confidence: 99%.
- The deterministic `graph.json` is a useful lightweight prompt registry. Moving it behind MCP would improve external discovery and formal arguments only if distribution beyond the current local installer becomes a real requirement. Confidence: 96%.
- Durable checkpoints would improve recovery for genuinely long compositions, but introducing a stateful workflow engine now would exceed the demonstrated need and weaken the current portability advantage. Confidence: 97%.
- The current English/Russian split is adequate for two languages. BCP 47 becomes action-facing when a third language or regional variants are requested, not before. Confidence: 96%.

#### Option palette

Following FPF modularity guidance, comparison used only three live characteristics: user-path reliability, machine-state isolation, and operational complexity.

| Option | User-path reliability | Machine-state isolation | Operational complexity | Retention |
|---|---|---|---|---|
| O1 — harden the existing skill graph | High after meta-plan, typo-suggestion, freshness, and installed-artifact checks | Medium: copy mode is isolated; whole-folder symlink mode is not | Low | Pareto-retained; challenged below |
| O2 — hybrid linked installation | High | High: keep a real installed directory and real local settings, while linking immutable package content | Medium | Pareto-retained; needs a prototype |
| O3 — publish commands as MCP/plugin prompts | Medium to high for broad discovery | High | High | Deferred until broad distribution is required |
| O4 — move compositions to a durable workflow runtime | High for long/interrupted campaigns; unnecessary for short calls | High | Very high | Deferred until resume/checkpoint evidence is required |
| O5 — introduce a BCP-47 locale model now | No material gain for current English/Russian use | Neutral | Medium | Deferred until another locale or regional variant exists |

There is no scalar winner. O1 is the lowest-cost reliability frontier; O2 is the stronger state-isolation frontier. O3–O5 solve different future receiving uses and should not be folded into O1 merely because they are available.

#### Design challenge outcome for O1

O1 survives the challenge, but only as a bounded hardening package. It fails if interpreted as “add better parsing and stop”: the current stale Personal installation and the symlink settings ownership problem would remain unresolved. Its safe boundary is:

- make `plan` a true non-executing meta-command over a proposed analytical stack;
- offer typo corrections only in non-executing or error paths;
- prove the installed artifact, not only the repository source;
- give symlink-mode state ownership an explicit disposition;
- do not introduce MCP, a plugin, a workflow engine, or a generalized locale subsystem without a new receiving use.

### 2. Consolidated issues and weak points

| ID | Severity | State | Consolidated finding | Evidence and consequence | Confidence |
|---|---|---|---|---|---:|
| F-001 | High | OPEN | The Personal Codex installation is stale relative to the current repository source. | A fresh `uv run -m scripts.install_fpf_skills.for_codex --check` returned `OUT OF DATE: Codex: copy-managed-stale`; the repository is at `18d0c5b`, version `0.1.1`. The user can therefore invoke behavior that no longer matches the shipped source and documentation. | 100% |
| F-002 | High | OPEN | `plan` cannot currently act as a meta-prefix for “plan this explicit composition.” | The observed `$fpf plan sota harvers + options + design challenge` was treated as an illegal analytical composition because `plan` itself is non-analytical. The user’s intent was reasonable and required a manually rewritten copy-ready command. | 99% |
| F-003 | Medium | OPEN | A command typo has no deterministic safe suggestion path. | `harvers` did not match `sota harvest`; model inference repaired it outside the router. Silent fuzzy execution would be unsafe, but a planner/error-path suggestion is missing. | 98% |
| F-004 | High | OPEN | Whole-folder symlink installation does not isolate machine-local runtime settings from the source checkout. | The installer writes `<installed-fpf>/.fpf-runtime.toml`; in symlink mode `<installed-fpf>` is the source directory link. The test explicitly confirms the physical file appears in `source/fpf.skill/.fpf-runtime.toml`. This requires a writable source and shares one physical local-settings file across linked consumers. | 100% |
| F-005 | Medium | OPEN | Validation strongly proves repository and installer logic, but does not yet prove activation through a fresh real Codex installation. | The current repository validator passed (`300` FPF IDs, `348` Markdown files, `8` NPF IDs, `3` skill packages), and all 9 installer unit tests passed. Yet the actual Personal installation is stale, so source tests and live deployment demonstrably diverge. | 99% |
| F-006 | Medium | OPEN | The `uv` validation wrapper emits a project-environment lock warning on every fresh command. | Installer check, installer tests, and repository validation all continued successfully but emitted `WARN Failed to acquire project environment lock: Could not create temporary file`. The pass results remain valid; the warning is an unresolved reproducibility/operability defect. | 100% |
| F-007 | Medium | OPEN | The main architectural risk is now overextension, not missing framework machinery. | Current primary sources show valid heavier alternatives, but the demonstrated receiving use is a small local bilingual skill. Adding plugin/MCP, durable orchestration, or generalized locale infrastructure now would add entities and operational surfaces without an action-facing distinction. | 97% |

Confirmed strengths that should be preserved:

- thin fast-Help entry and deferred runtime loading;
- one global end-user package and project-only service packages;
- explicit graph commands, aliases, legal edges, and a shared composition registry;
- standalone plain reporting with optional CAPRMEDIO adaptation;
- separate English and Russian Help files;
- safe copy installation and a deterministic managed-install receipt;
- passing current repository validation and installer unit suite.

### 3. Consolidated fixes and improvements

All actions are **PROPOSED**. They are ordered by dependency and mapped to every finding so that later alignment work can use one closure list.

| Action | Proposed change | Addresses | Acceptance evidence |
|---|---|---|---|
| A-001 | Refresh the Personal Codex installation from the current repository, run installer `--check`, and verify that the installed package contains the expected `.fpf-runtime.toml` and current source digest. | F-001, F-005 | `copy-current` or intentionally chosen `symlink-current`; current Help and plan smoke calls use the refreshed package. |
| A-002 | Define `$fpf plan <analytical command> [+ <analytical command> ...] <shared task>` as an explicit meta-plan grammar. Validate commands and edges, return a corrected copy-ready stack, and hard-disable execution of the suffix. | F-002 | Deterministic English and Russian scenarios prove the suffix is planned but never executed; illegal edges produce an explanatory plan result. |
| A-003 | Add edit-distance/alias suggestions only to Help, plan, and invalid-command/composition fallback paths. Never use a fuzzy match to execute an analytical node. | F-003 | `harvers` suggests `sota harvest`; ambiguous misspellings list alternatives; no fuzzy scenario crosses an execution boundary. |
| A-004 | Add an installed-artifact end-to-end matrix: install into an isolated destination by copy and symlink, check freshness, inspect runtime-settings placement, run the installed router checks, and exercise fast Help, meta-plan, composition, and English/Russian aliases. Keep actual Codex-host activation as a separate manual/runtime proof. | F-001, F-002, F-003, F-004, F-005 | The matrix runs against installed paths, not source paths; a stale copy fails; refreshed copy passes; symlink behavior is asserted according to A-005’s disposition. |
| A-005 | Explicitly choose one symlink-state policy: (a) document and accept writable-source/shared-settings semantics, (b) prototype a real installed directory containing a real `.fpf-runtime.toml` plus links to immutable package children, or (c) retire symlink mode and retain copy mode. Do not silently change the policy. | F-004 | Owner disposition plus tests for the selected ownership invariant on supported platforms. |
| A-006 | Diagnose the `uv` project-environment lock warning separately from temporary-test-directory cleanup; repair its actual ownership/path cause, then rerun the repository validator and installer suite without the warning. | F-006 | The same three fresh commands pass with no lock warning; no guessed permission change is accepted as proof. |
| A-007 | Keep O1 architecturally thin. Record explicit reopen triggers for MCP/plugin distribution, durable workflow state, and full locale tagging instead of implementing them now. | F-007 | No new runtime service is introduced; successor work starts only when one of the stated receiving uses is present. |
| A-008 | If a third language or regional variant is requested, adopt BCP-47 identifiers, per-locale Help/alias resources, and deterministic fallback tests. Until then, preserve the current `en`/`ru` model. | Future locale risk; F-007 | Trigger absent: no change. Trigger present: locale identity and fallback behavior are tested without increasing the main skill entry cost. |

### 4. Verification, residual risk, and coverage

Verification performed during this composition:

- repository frontier confirmed at `18d0c5b` on `dev`;
- source graph inspected: requested edges `sota-harvest -> options-explore -> design-challenge` are legal;
- Personal Codex install check reproduced `copy-managed-stale`;
- repository validation passed with `300` FPF IDs, `348` Markdown files, `8` NPF IDs, and `3` skill packages;
- all 9 installer unit tests passed, including copy refresh, runtime-settings repair, conflict preservation, single-skill migration, and symlink repair;
- symlink test/source inspection confirmed that the runtime-settings file physically lands in the linked source package;
- external evidence met the plural-tradition coverage floor;
- one challenge pass covered the retained low-cost option and explicitly preserved the isolation alternative.

Residual risks:

- no action has been applied, so F-001 remains live and the installed skill can still differ from this report’s analyzed source;
- actual Codex UI activation and response latency were not benchmarked;
- symlink behavior was tested locally, not across every supported operating system;
- the root cause of the `uv` lock warning is intentionally not guessed;
- O2 has not been prototyped, so its cross-platform complexity is estimated rather than demonstrated;
- external specifications and vendor documentation can change and should be refreshed when a successor design starts.

The action map covers every high-confidence finding: F-001 → A-001/A-004; F-002 → A-002/A-004; F-003 → A-003/A-004; F-004 → A-004/A-005; F-005 → A-001/A-004; F-006 → A-006; F-007 → A-007/A-008. No owner disposition, implementation, or closure claim is implied.

## Open questions (confidence <95%)

- Which symlink disposition best matches the owner’s intended workflow: explicitly shared source state, hybrid linked content with local settings, or copy-only installation? Current confidence in any one choice: 75%.
- Is broad third-party distribution a near-term requirement? If yes, MCP/plugin packaging becomes more competitive; if this remains a personal/repository tool, it probably does not. Confidence: 70%.
- Will compositions become long-running enough to need interruption, resume, or durable checkpoints? Current evidence says no, but there is no measured duration/abandonment dataset. Confidence: 80%.
- Is a third language or a regional language variant planned? Without that trigger, BCP-47 refactoring has no demonstrated payoff. Confidence: 70%.
- What is the root cause of the `uv` project-environment lock warning: directory ownership, file mode, stale lock state, or a runtime restriction? No cause reached 95%; it requires focused diagnosis.
- What user-visible latency threshold should fast Help and plan satisfy in the Codex host? The architecture minimizes loaded files, but no quantitative target or measurement exists. Confidence in any threshold: below 60%.

## Skills used

- `fpf` — explicit three-node composition using the source package at `skills/fpf.skill` and the installed runtime contract.
  - `$fpf sota harvest`
  - `$fpf options explore`
  - `$fpf design challenge`

#### FPF sources consulted (5 read; 5 used)

- `FPF-Knowledge-Graph/G_Discipline SoTA Patterns Kit/03_02_SoTA Harvester & Synthesis/00_G.02 - SoTA Harvester & Synthesis.md` — bounded corpus, claim sheets, plural traditions, bridge matrix, and coverage floor.
- `FPF-Knowledge-Graph/B_Trans-disciplinary Reasoning Cluster/04_05_Canonical Reasoning Cycle/02_Abductive Loop/02_B.05.02.01 - Creative Abduction with NQD.md` — candidate diversity, declared quality components, Pareto retention, provenance, and no opaque scalar winner.
- `FPF-Knowledge-Graph/E_The FPF Constitution and Authoring Guides/10_11_First-Practical Entry and Pattern-Use Discoverability Discipline/00_E.11 - First-Practical Entry and Pattern-Use Discoverability Discipline.md` — recognizable entry, bounded search, first useful result, ordinary stop, and wrong-turn recovery.
- `FPF-Knowledge-Graph/A_Kernel Architecture Cluster/11_Ontological Parsimony/00_A.11 - Ontological Parsimony.md` — prefer existing composition until a new action-facing distinction is materially required.
- `FPF-Knowledge-Graph/C_Kernel Extension Specifications/19_31_Modularity and Reusable Structure Characteristics/00_C.31 - Modularity and Reusable Structure Characteristics.md` — compare a small set of live characteristics rather than collapsing modularity into one score.
