## Task, scope, and boundaries

The package already follows useful current practices: a small entrypoint, selective context loading, explicit approval, staged artifacts, and independent feedback. The strongest opportunities are to **measure real continuation and recovery, quantify repeatability and overhead, and declare host requirements before activation**. More prompt depth or more agents is not an evidence-backed default improvement.

This is a bounded SOTA harvest dated **2026-09-09** for the current repository’s `skills/` package, to inform later development. It compares published approaches with inspected source contracts; it is not an alignment verdict, release approval, or proof of runtime reliability. No skills-package changes or test runs were performed. This final consolidation preserves the validated harvest. Saved report: fpf-reports/20260908T225305Z-fpf-sota-harvest-current-repo-skills-package.md. Run status: `COMPLETE` within the stated coverage.

Local evidence, read from `/Users/am/Documents/My_Repos/levenchuk-fpf-knowledge-graph-toolkit/`:

- **L1:** [Skills documentation](/Users/am/Documents/My_Repos/levenchuk-fpf-knowledge-graph-toolkit/skills/README.md), [entrypoint](/Users/am/Documents/My_Repos/levenchuk-fpf-knowledge-graph-toolkit/skills/fpf.skill/SKILL.md), and [manager](/Users/am/Documents/My_Repos/levenchuk-fpf-knowledge-graph-toolkit/skills/fpf.skill/prompts/fpf-manager.md): loading, approval, recovery, and installation contracts.
- **L2:** [Cases](/Users/am/Documents/My_Repos/levenchuk-fpf-knowledge-graph-toolkit/service/scripts/fpf_skill_quality_gate/fpf_skill_quality_gate_assets/cases.json) and [subject prompt](/Users/am/Documents/My_Repos/levenchuk-fpf-knowledge-graph-toolkit/service/scripts/fpf_skill_quality_gate/fpf_skill_quality_gate_assets/subject-prompt.md): twelve release cases; continuation starts from supplied prior Plan state.
- **L3:** [Evaluator prompt](/Users/am/Documents/My_Repos/levenchuk-fpf-knowledge-graph-toolkit/service/scripts/fpf_skill_quality_gate/fpf_skill_quality_gate_assets/evaluator-prompt.md), [runner](/Users/am/Documents/My_Repos/levenchuk-fpf-knowledge-graph-toolkit/service/scripts/fpf_skill_quality_gate/fpf_skill_quality_gate_workers/codex_runner.py), [CLI](/Users/am/Documents/My_Repos/levenchuk-fpf-knowledge-graph-toolkit/service/scripts/fpf_skill_quality_gate/fpf_skill_quality_gate_workers/cli.py), and [evidence handling](/Users/am/Documents/My_Repos/levenchuk-fpf-knowledge-graph-toolkit/service/scripts/fpf_skill_quality_gate/fpf_skill_quality_gate_workers/evidence.py): source execution, one trial per case, structured-result evaluation and digest binding.

### Composition receipt

- Invocation: `$fpf plan sota harvest against the current repo skills package`; subsequent exact `do` approved Plan `d1174456-86bb-4b84-8c82-347c9b98a389-plan`.
- Profile: `none`. Requested sequence and executed prefix: `$fpf sota harvest`. Unexecuted suffix: none. Typed analytical edges: none; single step.
- Predecessor: validated `step-001/` attempt 1 supplies the complete harvest, sources, findings and improvements to `final/`; validated `plan/` supplies scope and approval. Both passed sets remain immutable. Active blocking threshold: 95%; no blocking decision arose.
- Result: `COMPLETE`; context ledger: 1 direct FPF page read, 1 used, 0 deferred. Carried IDs: I-001–I-004 and F-001–F-004.

## Issues, weak points, and improvements

### Native result

#### Harvest contract H-01

Question: which current, supported approaches can improve the package’s routing, context loading, composition, recovery, evaluation, and portability while preserving its Markdown-only end-user runtime? Receiver and decision owner: the repository maintainer. Comparison axes are task completion, host-observed correctness, recovery continuity, context burden, elapsed time, repeatability, and deployment requirements.

Admission: original specifications, maintainers’ documentation, original engineering guidance, and original research. Live documentation was retrieved on 2026-09-09; foundational 2024 guidance is retained alongside 2026 evidence. English sources only. No jurisdiction-specific claim is made. Search rank and novelty do not establish superiority. Research abstracts support bounded reported findings only; no numerical result is treated as independently replicated here.

Excluded: broad framework rankings, commercial feature comparisons, conversion correctness, full FPF graph audit, exhaustive installer/security audit, repository mutation, and framework migration. This is a targeted six-source corpus, not a systematic literature review.

#### CorpusLedger CL-01 and screening flow FL-01

Initial discovery used three query families: Agent Skills specification/progressive disclosure, composable workflows/evaluation, and agent-skill tracing/reliability. Relevant official pages were opened; the evaluation article and persistence page were followed into their applicable sections. Six sources below were admitted. Search-only results, Reddit, mirrors, generic summaries and unrelated papers were excluded from claim support. No exhaustive search-hit count is asserted.

| ID | Source and edition | Admission and role | Inspected anchor |
|---|---|---|---|
| S1 | [Agent Skills specification](https://agentskills.io/specification), live 2026-09-09 | Include; portable format authority | Compatibility, progressive disclosure, file references |
| S2 | [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents), 2024-12-19, live page warns tooling has changed | Include; foundational engineering patterns, not current product catalog | Routing, chaining, evaluator-optimizer, complexity trade-offs |
| S3 | [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), 2026-01-09 | Include; original evaluation practice | Research grading, nondeterminism, realistic harnesses, grader calibration |
| S4 | [Counterfactual Trace Auditing](https://arxiv.org/abs/2605.11946v2), 2026-05-28 v2 | Include cautiously; original preprint, abstract only | Paired with/without-skill traces and behavioral effects |
| S5 | [Is Progressive Disclosure All You Need?](https://arxiv.org/abs/2607.17598v1), 2026-07-20 v1 | Include cautiously; original preprint, abstract only | InfiniteBench, harness dependence, routing depth |
| S6 | [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence), live 2026-09-09 | Include; contrasting executable persistence model | Checkpointers versus stores, interruption and restart limits |

#### ClaimSheets CS-01–CS-06

| ID | Source claim | Local synthesis and applicability | Limit |
|---|---|---|---|
| CS-01 / S1 | Metadata can declare environment requirements; resources load on demand; the specification advises shallow reference chains. | The thin FPF entrypoint fits progressive loading. Its mandatory resumable subagents/shared files should also be visible in compatibility metadata. | Format compliance does not establish host capability. |
| CS-02 / S2 | Routing, chaining and evaluator feedback solve different problems; extra complexity should earn its cost through measured results. | FPF already combines these patterns. Compare actual quality and cost before changing the number of agents or workflow stages. | Engineering guidance is not an FPF benchmark. |
| CS-03 / S3 | Repeated trials expose variability; realistic environments and calibrated graders matter; rigid path matching can punish valid solutions. | Keep the existing five gates, but obtain stronger observation for required handoffs and artifact existence, plus repeated-run diagnostics. | Observe mandatory behavior only; do not prescribe incidental tool sequences. |
| CS-04 / S4 | Paired traces can reveal skill-induced behavior even when aggregate success changes little. | Measure excess planning, artifact churn, and recovery as diagnostic effects alongside completion. | The reported coding-task study does not prove FPF gains or losses. |
| CS-05 / S5 | In the reported long-document experiments, progressive disclosure depended on harness and corpus scale; deeper routing could hurt. | Test end-to-end loading paths before adding graph layers; a small entrypoint alone does not measure context cost. | Document QA differs from analytical skill orchestration; this is a test hypothesis. |
| CS-06 / S6 | Thread checkpoints support continuation; stores serve a different cross-thread purpose; in-memory checkpoints disappear on restart. | Use the distinction to specify exactly which interruptions FPF temporary artifacts and retained agent state can survive. | LangGraph is a contrasting implementation, not a dependency recommendation or equivalent guarantee. |

Each row separates a cited source claim from reviewer inference. No operator choice or implementation approval is implied.

#### SoTA_Set SS-01, palette PA-01, and BridgeMatrix BM-01

The palette contains four complementary or competing approaches; it is not a ranking or shortlist.

| Tradition / method family | Strength and validity region | Cost or failure mode | Explicit bridge to this package |
|---|---|---|---|
| MF-01: Portable file-based skills (S1, S5) | Discoverable, selective instructions across compatible hosts | Nested retrieval can add burden; format portability is narrower than execution portability | Preserve Markdown packaging; measure loading paths and declare host requirements. No guarantee transfers from file format to runtime. |
| MF-02: Composable evaluator workflows (S2) | Clear roles and useful feedback when criteria are assessable | Added latency and correlated judgment errors | Existing manager/doer/warden is a local implementation; test its benefit rather than assuming the pattern proves it. |
| MF-03: Outcome grading plus trace experiments (S3, S4) | Distinguishes completion from behavioral effects and variation | More trials and human calibration cost | Supplement the five existing gates with observations and diagnostics. A trace difference alone is not a failure. |
| MF-04: Executable checkpoint systems (S6) | Explicit persistence and replay boundaries | Runtime/storage dependencies and operational complexity | Transfer recovery questions, not the framework. Temporary files and retained agents are not interchangeable with persistent checkpoints. |

Object/measurement inventory OI-01: package = local `skills/fpf.skill`; host = orchestration/filesystem provider; trial = one task execution; artifact set = candidate plus metadata; quality = task-aligned result under the existing five gates. Candidate measurements: completion frequency, incorrect acceptance/rejection rate, recovery completion, extra user approvals, loaded bytes/files, latency and token use where observable. No thresholds are invented here.

Microexamples ME-01–ME-03: (1) discover a skill on a host unable to resume two agents and verify that compatibility is apparent before expensive work; (2) interrupt production before metadata exists, then observe recovery without premature validation; (3) compare the same task with current loading and a shallower reference path, retaining the output and authority contract. These are proposed experiments, not executed demonstrations.

Indicator branches IN-01: functional branch retains all five gates; repeatability branch observes several independent trials; efficiency branch compares cost only among task-correct runs. Naming proposals NP-01: use “format compatibility” and “execution compatibility” as distinct local documentation labels; no public FPF identifiers are minted. Generated-task family and registry publication: not requested. PA-01 is reconstructible from CL-01, CS-01–06, MF-01–04, BM-01, OI-01 and ME-01–03.

Disagreements remain visible: shallow references versus staged contract specialization; strict workflow requirements versus flexible agent paths; outcome sufficiency versus behavioral diagnostics; prompt-only dependencies versus executable persistence. There is insufficient basis to choose an architectural winner.

Receiving use and refresh: use this pack to define bounded experiments or a later evaluation-design task. Refresh relevant source claims when the host, package, source specification, or evaluation protocol changes; recheck live docs before implementation. Stop here with an evidence map, without automatically entering challenge or improvement.

### Issue registry

- **I-001 — Execution portability is declared late.** Affected context: discovery and activation of `fpf`. Evidence: L1 entrypoint has no `compatibility` field; manager requires separate resumable agents and a shared temporary filesystem; S1 supports expressing requirements. Consequence: a host may discover a portable-looking skill but cannot execute it. Confidence: **99%** for this documentation mismatch, based on inspected carriers. Limit: supported-host failure rates were not tested. State: `OPEN`. Fix: F-001.
- **I-002 — Recovery/continuation evidence is weaker than the required behavior.** Affected context: local live gate. Evidence: L2 continuation receives synthetic prior Plan state; no release case injects an interrupted doer; L3 evaluates reported artifact inventory rather than independently observing the relevant filesystem state. S3 motivates realistic environment observations. Consequence: these cases cannot by themselves prove actual retained-agent continuation and recovery. Confidence: **98%** for the bounded release-pack gap. Limit: other manual or test coverage may exist; no claim that the runtime is broken. State: `OPEN`. Fix: F-002.
- **I-003 — A passing run does not quantify repeatability or orchestration value.** Affected context: release evidence and performance decisions. Evidence: L3 invokes one subject trial per case; S2–S4 motivate measured cost, repeated results and behavioral comparison. Consequence: pass/fail alone cannot estimate reliability, overhead or benefit from the workflow. Confidence: **98%** for absent measurement in the inspected runner. Limit: no local benchmark was run; no inefficiency is established. State: `OPEN`. Fix: F-003.
- **I-004 — Loading depth has no demonstrated local benefit/cost balance.** Affected context: entrypoint → manager → runtime → contracts/node/FPF loading. Evidence: L1 and the executed installed contracts show several stages; S1 and S5 provide reasons to test depth. Consequence: adding graph layers could increase navigation burden without improving results. Confidence: **85%** that this is a worthwhile performance hypothesis, not a proven defect. Limit: S5 is abstract-level evidence from another task family; no FPF ablation or token trace was measured. State: `OPEN`. Fix: F-004.

### Fix and improvement register

1. **F-001 — Declare and verify execution requirements.** Addresses I-001. Exact change: add concise host capability requirements to package compatibility metadata and publish a small tested-host matrix. Relationship: `complementary`. Owner/authority: maintainer, package/docs edit approval. Order/dependencies: first; none. Expected result: limitations are visible at discovery. Trade-off: matrix requires maintenance. Fix confidence: **97%**, supported by S1 and concrete manager prerequisites. Verification: inspect installed metadata and smoke-test declared capability combinations. Recommendation: `preferred`. State: `PROPOSED`.
2. **F-002 — Add real continuation and interrupted-production local cases.** Addresses I-002. Exact change: run an actual Plan → `do` conversation and an interrupted-doer case; let the local harness observe the two files and essential state transitions. Keep observations inside the existing workflow/artifact gates; no extra user-facing proof bundle or sixth gate. Relationship: `complementary`. Owner/authority: maintainer, service-test edits and local execution. Order/dependencies: second; preserve current five-gate semantics. Expected result: evidence covers retained-state continuation and premature-validation prevention. Trade-off: host adapters and test duration. Fix confidence: **96%**, based on the concrete L2/L3 gap and S3. Verification: correct recovery passes; missing files, replayed completed work and a second unnecessary `do` fail the relevant existing gate. Recommendation: `preferred`. State: `PROPOSED`.
3. **F-003 — Add repeatability and cost diagnostics.** Addresses I-003. Exact change: repeat representative local cases with isolated trial state, record observed completion frequency and latency/token use when available, and compare controlled workflow variants diagnostically without changing default approval behavior. Relationship: `complementary`. Owner/authority: maintainer, service harness changes and bounded local model budget. Order/dependencies: third, after F-002 so measurements use trustworthy events. Expected result: measured reliability and overhead, not a single-run claim. Trade-off: cost and statistical uncertainty with small samples. Fix confidence: **95%**, supported by S2–S4. Verification: reproducible case/model/variant identity, retained per-trial outcomes, no averaging away a failed release gate. Recommendation: `preferred`. State: `PROPOSED`.
4. **F-004 — Run a loading-path experiment before restructuring prompts.** Addresses I-004. Exact change: compare current staged retrieval with a shallower reference variant under identical tasks and contracts; retain Markdown-only runtime. Relationship: `required prerequisite` to a context-depth refactor. Owner/authority: maintainer, isolated experiment and local model budget; no production change yet. Order/dependencies: fourth, uses F-003 diagnostics. Expected result: evidence for keeping or changing depth. Trade-off: experiment maintenance; results may be harness-specific. Fix confidence: **90%** that the experiment informs the decision, not that flattening wins; basis S1/S5 plus local chain. Verification: compare task correctness, authority compliance, observed loading and latency across the same cases; reject a variant with regressions. Recommendation: `acceptable`. State: `PROPOSED`.

## Unresolved evidence gaps

- **G-001 (I-002/F-002):** Best current answer: the release pack checks supplied continuation state but does not demonstrate the original Plan-producing session surviving interruption. Missing: observed host recovery traces and filesystem outcomes. Consequence: recovery reliability remains unconfirmed. Next evidence: actual Plan → `do` plus interrupted-production local trials.
- **G-002 (I-003/I-004, F-003/F-004):** Best current answer: neither benefit nor penalty is measured here. Missing: repeated task outcomes, loading and cost observations. Consequence: no justified architectural simplification or expansion. Next evidence: paired local experiments with pinned task and model identities.
- **G-003 (I-001/F-001):** Best current answer: requirements are explicit inside the manager; tested cross-host behavior was not inspected. Missing: fresh installed-host capability results. Consequence: no cross-host compatibility guarantee. Next evidence: supported-host smoke matrix.
- **G-004 (I-004/F-004):** Best current answer: S4/S5 suggest evaluation hypotheses only. Missing: full-paper methodological review and replication for this task family. Consequence: no numerical transfer or general superiority claim. Next evidence: review full methods before using these studies to justify an implementation choice.

## Skills used

`$fpf sota harvest`

### FPF sources consulted (1 read; 1 used)

- **Used:** `FPF-Knowledge-Graph/G_Discipline SoTA Patterns Kit/03_02_SoTA Harvester & Synthesis/00_G.02 - SoTA Harvester & Synthesis.md`, `fpf_id: G.2`, source revision `563f4c8e06a319cbd375b66cdbb2df27a5f8b9ef`. Inspected Problem frame, Problem, Forces, Solution §§4.2–4.4 and 4.6, Consequences, and introductory scope. Full Solution extensions were not inspected. Applied to source ledger, separate claims/inferences, plurality, bounded comparison and refresh conditions; not evidence of local runtime correctness.
