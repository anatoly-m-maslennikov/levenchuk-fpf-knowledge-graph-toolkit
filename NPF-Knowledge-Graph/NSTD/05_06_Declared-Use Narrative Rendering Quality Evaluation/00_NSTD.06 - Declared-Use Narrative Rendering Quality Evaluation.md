---
type: "npf-pattern"
context:
  - "NPF"
page_type: "npf-pattern"
mode: "canonical-generated"
npf_id: "NSTD.6"
title: "Declared-Use Narrative Rendering Quality Evaluation"
part: "[[00_Hubs/NPF - Preface - Cross-Cutting Ideas And Principles]]"
parents:
  - "[[00_Hubs/NPF - Preface - Cross-Cutting Ideas And Principles]]"
source_file: "Narrativization-and-Narrative-Studies-Principles-Framework.md"
source_revision: "d77339d7056433de3ee55ad863860ee4b3006f6f"
source_sha256: "80f2d5ec3524b7947a3c36928bf774f61a9c68d4efc9ec5fc0d23206f01534e4"
generated_on: "2026-08-24"
source_lines:
  - 1476
  - 1772
status: "generated"
generated: true
---


> **Type:** DPF evaluation pattern body

> **Primary EntityOfConcern:** `NarrativeRenderingQualityEvaluationCharacteristicSpace@Context`, an evaluation `CharacteristicSpace` for one evaluated narrative rendering kind and declared use.

## [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]]:1 - Problem frame

Use this pattern when a team must decide whether one admitted narrative rendering version is good enough for one declared reader or listener use.

Evaluated object kind: `NarrativeRenderingVersion@Context`, meaning one admitted narrative rendering version with admitted source basis, selected source structures, declared use, ordering rule, and source-return condition. A source text, source pack, style guide, seminar script, slide deck, generated output before `C.35` admission, or broad communication plan is not this evaluated object.

First useful move: state "quality of which admitted narrative rendering version, for which declared use, under which temporal posture and rendering mediation mode, against which contrast cases?" Then name one admissible narrative rendering, one below-floor narrative rendering, and one wrong-kind object that must return to evaluation selection.

What goes wrong if missed: readability, elegance, engagement, expert approval, or generated fluency substitutes for epiplexity, source-return discipline, and bounded use.

What this buys: a repeatable evaluation that can feed `E.23` improvement without confusing characteristics, measurements, eval programs, evidence, assurance, or gates.

Quality target: this pattern evaluates quality for one declared use under source-structure selection fit, `NarrativeRenderingEpiplexity`, ordering recoverability, temporal-posture and role fit, source-return readiness, bounded engagement, and owner-routed evidence, assurance, ethics, publication, and work claims.

## [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]]:2 - Problem

Narrative rendering quality for declared use is not one property. A narrative can be fluent but structurally false, engaging but ethically unsafe, technically accurate but unusable for learners, or source-faithful but impossible to follow. A useful evaluation needs object-kind fit, characteristic slots, value meanings, evidence basis, missingness rules, floor, exceptional meaning, result-row shape, and repair actions.

## [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]]:3 - Forces

| Force | Tension |
| --- | --- |
| Fluency vs epiplexity | A readable narrative may pull too little selected source structure into the rendering for the declared use. |
| Engagement vs bounded use | A motivating narrative may overpersuade. |
| Local usability vs reusable scale | A project can use a small rubric, but DPF needs reusable value meanings. |
| Measurement vs evaluation | Some values may be measured through `C.16`; many are ordinal content evaluations. |
| Improvement vs Goodhart pressure | Indicatorized characteristics help loops, but unmeasured tracked concerns must prevent proxy capture. |

## [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]]:4 - Solution

Construct and use one narrative rendering quality evaluation characteristic space for one declared use.

```text
NarrativeRenderingQualityEvaluationCharacteristicSpace@Context:
  evaluatedObjectKindRef: NarrativeRenderingVersion@Context
  declaredUseScope:
  objectKindFitRule:
  discriminatingCaseSet:
  characteristicSlotSet:
  epiplexityBasisRule:
  scaleBindingSet:
  valueMeaningSet:
  evidenceBasisRule:
  missingnessAndLoweringRule:
  resultRowShape:
  floorAndExceptionalMeaning:
  protectedTradeoffSet:
  stopOrReopenCondition:
  neighboringGoverningPatternRefs:
```

Object-kind fit:

| Object-kind case | Handling |
| --- | --- |
| Admissible narrative rendering | Evaluate all load-bearing characteristics for the declared use. |
| Below-floor narrative rendering | Evaluate and return low-value repair actions. |
| Wrong-kind object before invocation | Return to evaluation selection; choose admitted source basis, style, seminar, generation, publication, or evidence owner. |
| Wrong-kind object after invocation | Record explicit object-kind-fit defect and stop; do not silently assign values to unrelated coordinates. |

Default value meanings for ordinal content evaluation:

| Value | Meaning |
| --- | --- |
| `0` | Wrong-kind object, no admissible basis, or evaluation must stop before value use. |
| `1` | Object is a narrative rendering but unusable for the declared use. |
| `2` | Orientation only; source return is needed before reliance. |
| `3` | Locally usable with named limitations and repair obligations. |
| `4` | Good for declared use with bounded losses and source return. |
| `5` | Strong for declared use; source relation, repair history, and boundary cases are replayable. |

Default floor: for reliance-bearing or teaching use, all load-bearing characteristics must be at least `4`, and `NarrativeRenderingEpiplexity`, `OrderingRecoverability`, and `SourceReturnReadiness` may not be below `4`. When the selected source structure is a constraint-governed unfolding structure, `DemonstrativeSliceRecoverability` is load-bearing and may not be below `4`. A local low-risk orientation use may set floor `3` only if non-admissible downstream use is explicit.

Result-row shape:

```text
NarrativeRenderingQualityResultRow@Context:
  narrativeRenderingVersionRef:
  declaredUseScopeRef:
  characteristicId:
  characteristicName:
  scaleRef:
  value:
  evidenceBasisRefs:
  missingnessClass:
  loweringReason:
  repairAction:
  directOwnerRefs:
  reopenCondition:
```

Package the rows before feeding an improvement loop:

```text
NarrativeRenderingQualityEvaluationResult@Context:
  evaluatedNarrativeRenderingVersionRef:
  declaredUseScopeRef:
  evaluationCharacteristicSpaceRef: NarrativeRenderingQualityEvaluationCharacteristicSpace@Context
  evaluationPurpose:
  evidenceBasisRefs:
  resultRows:
  protectedTradeoffSet:
  belowFloorRows:
  candidateImprovementProposalRows?:
  nonUseBoundary:
  stopOrReopenCondition:
```

When repeated improvement is wanted, open `E.22` first if the quality question is not already framed. Then use `E.23` with [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] as the object-under-improvement evaluation. This DPF does not mint a local loop kind.

```text
NarrativeRenderingImprovementLoopInput@Context:
  e22QuestionFrameRef?:
  objectUnderImprovementRef: NarrativeRenderingVersion@Context
  objectVersionBeforeRef:
  objectUnderImprovementEvaluationRef: [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]]
  improvementAim:
  protectedTradeoffSet:
  costAndRiskAccount:
  allowedChangeSlice:
    narrativeRenderingVersion | NSTD.1-intake | NSTD.2-ordering |
    NSTD.3-event-model | NSTD.4-viewpoint | NSTD.5-engagement |
    NSTD.7-generated-carrier-admission | NSTD.8-learning-route |
    evaluationCharacteristicSpace
  returnedFindingOrProposalRows:
  expectedReEvaluationResultForm: NarrativeRenderingQualityEvaluationResult@Context
  neighboringGoverningPatternRefs:
  stopContinueSwitchOrHoldCondition:
```

`E.23` may claim improvement only after the changed object version is re-evaluated through [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] or through a declared stronger evaluation. If the loop changes the source pack, source-currentness, generated-carrier admission, learning publication carrier, publication face, ethics claim, evidence claim, assurance claim, or evaluation characteristic space, the loop must name the neighboring governing pattern and either keep it as the allowed change slice or open separate work. Style edits, prompt retries, or additional drama are admissible loop operations only when their expected movement under [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] is stated and protected trade-offs are checked. `B.4` is relevant only when the narrative episteme or learning route is claimed to evolve across use and renewed operation; `G.11` handles refresh when source currentness, reader telemetry, teaching-test evidence, generated-narrative practice, or FPF edition changes.

Before assigning values, require construction-route evidence. The evaluator must be able to point to the records or source passages that played the role of [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose|NSTD.1]] source selection, [[NSTD/01_02_Structure-to-Sequence Ordering/00_NSTD.02 - Structure-to-Sequence Ordering|NSTD.2]] ordering, [[NSTD/02_03_Source Mechanism, Event Model, and Coherence/00_NSTD.03 - Source Mechanism, Event Model, and Coherence|NSTD.3]] event or mechanism support when live, [[NSTD/03_04_Voice, Focalization, and Agency/00_NSTD.04 - Voice, Focalization, and Agency|NSTD.4]] viewpoint and agency discipline when live, [[NSTD/04_05_Engagement, Attention, and Motivation/00_NSTD.05 - Engagement, Attention, and Motivation|NSTD.5]] engagement boundary when live, [[NSTD/06_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning|NSTD.7]] generated-carrier admission when live, and [[NSTD/07_08_Learning-Route Narrative Rendering and Reconstruction Return/00_NSTD.08 - Learning-Route Narrative Rendering and Reconstruction Return|NSTD.8]] learning-route design when live. If those records were not written before drafting, they may be reconstructed from source and carrier, but the reconstruction must be explicit. Do not allow "the narrative already looks good" to substitute for the missing construction route.

Use this evaluation sequence:

1. Object-kind fit: is this an admitted narrative rendering version, not source text, source pack, slide deck, prompt output, style guide, or broad communication plan?
2. Construction-route fit: can the evaluator recover the selected source structures, ordering rule, source-return condition, and live neighboring governing-pattern routes?
3. Declared-use fit: is the reader or listener use narrow enough to evaluate, and are non-admissible downstream uses stated?
4. Load-bearing characteristics: assign values only to the characteristics needed for the declared use, but include every characteristic whose failure would make the use unsafe or useless.
5. Low-value repair: for every value below floor, name the smallest repair route before proposing style, drama, or generation retries.
6. Re-evaluation route: if any repair changes the object version or selected source basis, plan a new [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] evaluation before claiming improvement.

Missingness and lowering rules:

| Missing or defect condition | Lowering rule |
| --- | --- |
| Selected source structures absent | `NarrativeRenderingEpiplexity` no higher than `1`; evaluation may stop as wrong object if the rendering has no recoverable source-structure denominator. |
| Ordering rule absent | `OrderingRecoverability` no higher than `2`. |
| Source temporal posture, rendering mediation mode, narrating worker, or reader role absent | `TemporalPostureAndRoleFit` no higher than `2`; return to [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose]] before trusting evaluation. |
| Source-structure selection rationale or reader-interest hypothesis absent | `NarrativeRenderingEpiplexity` no higher than `2`, `TemporalPostureAndRoleFit` no higher than `2`, and evaluation must return to [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose]] before style or engagement repair. |
| Source-return condition absent | `SourceReturnReadiness` no higher than `2`. |
| Constraint-governed unfolding structure is selected but the rendering declares only a sequence, route card, story line, or lesson chain | `DemonstrativeSliceRecoverability` no higher than `2`; return to [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose]], [[NSTD/01_02_Structure-to-Sequence Ordering/00_NSTD.02 - Structure-to-Sequence Ordering]], and `A.22.CGUS` or the local governing pattern before treating the narrative as a rendering of the wider structure. |
| Artistic, literary, simplified, or dramatic wording changes source recovery without owner routing | `LanguageStatePrecisionAndCoarseningFit` no higher than `2`; return to `C.2.LS`, `A.6.3.CSC`, `E.17.EFP`, `E.10`, `A.6.P`, or `C.16.Q` before treating style repair as improvement. |
| Early hook, vibe, story seed, or route hint is evaluated as an admitted narrative rendering | Wrong-kind object for this evaluation; return to `A.16.1`, then [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose]] and [[NSTD/01_02_Structure-to-Sequence Ordering/00_NSTD.02 - Structure-to-Sequence Ordering]] when route selection becomes explicit. |
| Engagement effect asserted without persuasion boundary when influence is live | `EngagementBoundedness` no higher than `3` and ethics owner must be named. |
| Generated output not admitted through `C.35` | Wrong-kind object for this evaluation; return to [[NSTD/06_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning]] and `C.35`. |
| Evidence or assurance claim made without owner | Relevant characteristic value lowered and claim routed to `A.10` or `B.3`. |

Default narrative rendering quality characteristics:

| Characteristic | Evaluation question | Low-value repair action |
| --- | --- | --- |
| `SourceStructureSelectionFit` | Are the selected source structures and reader-interest or use hypothesis explicit, non-magical, and well matched to the declared use? | Reopen [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose]]; reconstruct or revise the source-structure selection rationale before changing style, drama, or prompt wording. |
| `NarrativeRenderingEpiplexity` | How much of the selected source-structure denominator is recoverably pulled into this narrative rendering for the declared use, observer boundary, and source-return condition? | Reopen [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose]]; add source refs, source pins, preserved, foregrounded, or lost-structure accounting, or source-return links. Use `C.33` when architecture-relevant structural-information capture is current. |
| `OrderingRecoverability` | Can the reader say why this sequence was chosen and what it hides? | Reopen [[NSTD/01_02_Structure-to-Sequence Ordering/00_NSTD.02 - Structure-to-Sequence Ordering]]; state ordering rule, preserved relations, and lost relations. |
| `DemonstrativeSliceRecoverability` | When a constraint-governed unfolding structure is selected, can the reader recover the wider structure, the demonstrative slice, and the hidden branches, loops, alternatives, direct exits, or stop conditions? | Reopen [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose]] and [[NSTD/01_02_Structure-to-Sequence Ordering/00_NSTD.02 - Structure-to-Sequence Ordering]]; name the selected CGUS or local block, the demonstrative slice, preserved constraints, lost structure, and return to `A.22.CGUS` or the local governing pattern. |
| `TemporalPostureAndRoleFit` | Do source temporal posture, rendering mediation mode, narrating or rendering worker, reader or listener role, uncertainty, and source-return obligation match the declared use? | Reopen [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose]]; mark retrospective, live, prospective, architecture-mediated, or mixed posture; repair narrator and reader role split and lower claims that overread provisional or fictional structure. |
| `EventMechanismSupport` | Can the reader reconstruct events, mechanisms, dependencies, or state changes when required? | Reopen [[NSTD/02_03_Source Mechanism, Event Model, and Coherence/00_NSTD.03 - Source Mechanism, Event Model, and Coherence]]; add mechanism support or lower causal language. |
| `ViewpointAgencyDiscipline` | Does viewpoint reveal source structure without false agency, capability, responsibility, or permission? | Reopen [[NSTD/03_04_Voice, Focalization, and Agency/00_NSTD.04 - Voice, Focalization, and Agency]]; split protagonist, actant, role, agency, and ethics owners. |
| `EngagementBoundedness` | Does engagement support declared use without widening authority? | Reopen [[NSTD/04_05_Engagement, Attention, and Motivation/00_NSTD.05 - Engagement, Attention, and Motivation]]; add persuasion boundary or reduce engagement device. |
| `LanguageStatePrecisionAndCoarseningFit` | Does the chosen plain, technical, literary, compressed, didactic, or cue-like language state fit the declared use without hiding relation precision, quality sense, source loss, or route authority? | Publish the language-state facet profile when threshold-bearing, use `A.6.3.CSC` for narrowed-use coarsening, `E.17.EFP` for explanation-facing retelling, `A.16.1`/`A.16.2` for cue or backoff, and `E.10`, `A.6.P`, or `C.16.Q` for precision restoration. |
| `EthicsEvidenceAssuranceRouting` | Are value, harm, evidence, assurance, and policy claims routed to owners? | Route to `D.1` through `D.5`, `A.10`, `B.3`, or relevant owner. |
| `MediumAndPublicationFit` | Does the carrier fit the reader and use without changing the claim? | Route publication or audience-unit questions to `E.17`, `E.17.AUD`, or [[NSTD/07_08_Learning-Route Narrative Rendering and Reconstruction Return/00_NSTD.08 - Learning-Route Narrative Rendering and Reconstruction Return]]. |
| `SourceReturnReadiness` | Does the narrative tell readers when and where to return to the admitted source basis or direct governing pattern? | Add source-return condition or narrow admissible use. |

## [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]]:5 - Archetypal Grounding

### Mature value bank: full result rows

Use this bank when a narrative rendering "sounds good" and therefore tempts the worker to skip evaluation. Each row evaluates an admitted rendering version for one declared use. The same text may receive different values for a different use.

| Case | Characteristic | Value | Evidence basis | Low-value repair |
| --- | --- | --- | --- | --- |
| FPF seminar handout | `NarrativeRenderingEpiplexity` | `4` | Learners can recover `EntityOfConcern`, forces, solution, and neighboring exits from the handout. | To reach `5`, add a transfer task where learners choose a governing pattern for a new situation. |
| FPF seminar handout | `SourceReturnReadiness` | `5` | Every slogan-like line has a source pattern return and one reconstruction exercise. | No proposal unless source patterns change. |
| FPF seminar handout | `EngagementBoundaryFit` | `4` | Failure story is marked as archetype, not evidence. | Add an explicit evidence-owner exit if the story is used in public adoption material. |
| Homotopy explanation | `LanguageStatePrecisionAndCoarseningFit` | `3` | Analogy is vivid but learners may not know where formal conditions return. | Add an analogy-stop line and a formal boundary task. |
| Homotopy explanation | `OrderingRecoverability` | `4` | Didactic order is named and proof order is deferred by value. | To reach `5`, add a second problem where learner maps story order to formal dependency order. |
| Franchise continuation probe | `SourceReturnReadiness` | `4` | Private source-pack constraints and non-publication boundary are named. | Add a continuity perturbation test: change one premise and check whether event support remains valid. |
| Live commentary | `EventMechanismSupport` | `3` | Observation and provisional interpretation are separated, but later telemetry return is only generic. | Add specific official record, replay, or statistics return condition. |
| Generated graph-to-text narrative | `GeneratedCarrierAdmissionFit` | `2` | Output is fluent, but source plan and selected lost relations are not admitted. | Return to [[NSTD/06_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning]]; do not call this an admitted rendering yet. |

### Before and after evaluation repair

Before evaluation statement:

> The narrative is strong because readers liked it and remembered the main point.

Failure: engagement and memory are treated as total quality. Source recovery, relation strength, owner routing, and use boundary are absent.

After evaluation statement:

> For the declared onboarding use, the rendering receives value `4` on source recovery because learners can reconstruct the pattern-use route, value `3` on source-return readiness because two slogans lack pattern-body refs, and value `4` on engagement boundary because the failure story is marked as archetypal. The first repair is to add source-return refs for the slogans before changing style.

Now `E.23` has a real changed slice: add two source-return refs and re-evaluate. It is not "make it better somehow".

### Adjacent-value calibration

| Characteristic | `3` means | `4` means | `5` means |
| --- | --- | --- | --- |
| `NarrativeRenderingEpiplexity` | Some selected structure is recoverable, but important preserved or lost structure is implicit. | Selected structure, intentional loss, observer and use boundary, and source return are recoverable. | Recovery survives a heterogeneous transfer or perturbation case. |
| `OrderingRecoverability` | Order is named, but wrong reconstruction remains likely. | Order, preserved relations, lost relations, and misread block are explicit. | Conflicting order layers are handled and tested. |
| `EventMechanismSupport` | Events are coherent, but support strength is partly inferred from wording. | Relation strength and reconstruction target are explicit. | A wording or viewpoint change does not change recovered support strength. |
| `ViewpointOwnerRouting` | Viewpoint is useful, but agency or responsibility repair is incomplete. | Viewpoint function and literal owner exits are recoverable. | Reader can remove or swap viewpoint without losing source structure. |
| `EngagementBoundaryFit` | Interest exists, but source fidelity or persuasion boundary is weak. | Interest supports declared use while protecting source and owner exits. | A higher-engagement variant improves attention without lowering source recovery. |
| `GeneratedCarrierAdmissionFit` | Generated output is plausible, but source plan or admission is incomplete. | Source plan, method, admission, and evaluation route are explicit. | Source perturbation and responsibility probes both pass. |
| `LearningRouteReconstructionFit` | Learners can retell the route but not reliably reconstruct source relations. | Learners reconstruct source spine and source-return boundaries. | Learners transfer the route to a new case and identify the correct neighboring owner. |

### Evaluation-to-improvement repair input without process theatre

[[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] does not create a big improvement program. It creates result rows. A repeated improvement loop needs only:

```text
NarrativeRenderingImprovementLoopInput@Context:
  objectVersionRef: admitted narrative rendering version
  evaluationResultRefs: selected [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] rows
  improvementAim: raise one declared value without lowering protected trade-offs
  allowedChangedSlice: wording, source-return link, ordering marker, viewpoint repair, engagement device, generated source plan, or learning task
  protectedTradeoffSet: source fidelity, owner routing, engagement, cost, reader burden
  expectedReEvaluationForm: rerun the affected [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] rows and any neighbor owner checks
```

If the change is "regenerate until better", the object version and changed slice are gone. If the change is "add a source-return link and an analogy-stop task", `E.23` can operate and [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] can re-evaluate.

### FPF owner teaching

[[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] teaches that epiplexity is not a mood about detail. It asks how much selected structure is recoverable in this rendering, for this observer and use, with explicit losses and source returns. For architecture-relevant renderings, `C.33` remains the stronger owner. For ordinary narrative renderings, the DPF-local epiplexity basis keeps the same information discipline without pretending that every story is an architecture description.

Pass case: an FPF seminar handout narrates how a practitioner moves from problem frame to forces to solution and checks. It names FPF pattern source sections, ordering rule, learner reconstruction task, and source-return points. Values reach `4` or `5` for teaching orientation, but the handout is not evidence that FPF is correct.

Fail despite fluency: a polished architecture story says one chosen architecture "won" because it felt coherent, hides rejected candidates, omits architectural characteristics, and gives no source-return path. `NarrativeRenderingEpiplexity`, `OrderingRecoverability`, and `SourceReturnReadiness` fall below floor even if engagement is high.

Wrong-kind object: an LLM produces a fluent story before `C.35` carrier admission and before selected source structures are recoverable. The object returns to [[NSTD/06_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning|NSTD.7]] and `C.35`; [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] may record object-kind-fit value `0`, but it must not evaluate the text as an admitted narrative rendering.

## [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]]:6 - Bias-Annotation

This pattern blocks proxy-as-quality drift: readability, fluency, liking, engagement, expert approval, or generated-text benchmark value replaces object-kind fit and declared-use rendering quality. It also blocks the opposite drift where a test program is treated as the characteristic itself. Repair by selecting the evaluated object kind, scales, value meanings, evidence basis, missingness and lowering rules, floor, result rows, and repair actions. Scope: DPF-local for evaluating narrative rendering versions; it does not govern evidence, assurance, gate, decision, or publication authority.

## [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]]:7 - Conformance Checklist

| Check | Passing condition |
| --- | --- |
| `CC-NSTD6-1` | Evaluated object kind, declared use, and object-kind fit rule are explicit. |
| `CC-NSTD6-2` | At least three discriminating cases are present: pass, below-floor, and wrong-kind. |
| `CC-NSTD6-3` | Each characteristic binds one scale or is explicitly an ordinal content evaluation. |
| `CC-NSTD6-4` | Value meanings, evidence basis, missingness rules, floor, exceptional meaning, and stop or reopen condition are declared. |
| `CC-NSTD6-5` | Result rows include value, evidence basis, lowering reason, repair action, owner, and reopen condition. |
| `CC-NSTD6-6` | Measurement, eval program, evidence, assurance, gate, decision, publication, and pattern-quality claims route to owners. |
| `CC-NSTD6-7` | If repeated improvement is claimed, the `E.22` or `E.23` input names object version, [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation]] as evaluation, improvement aim, protected trade-offs, allowed change slice, cost and risk account, and expected re-evaluation form. |
| `CC-NSTD6-8` | No quality movement is claimed until the changed narrative rendering version or declared changed slice is re-evaluated by [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation]] or a declared stronger evaluation. |

## [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]]:8 - Common Anti-Patterns and How to Avoid Them

| Anti-pattern | What fails | Repair |
| --- | --- | --- |
| Fluency benchmark value as quality | Smoothness replaces structure recovery. | Lower source-related characteristics and repair through [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose]] through [[NSTD/02_03_Source Mechanism, Event Model, and Coherence/00_NSTD.03 - Source Mechanism, Event Model, and Coherence]]. |
| Style repair as precision repair | A nicer wording pass is treated as sufficient while relation kind, quality sense, language-state threshold, or coarsening loss remains hidden. | Lower `LanguageStatePrecisionAndCoarseningFit`; apply the selected FPF precision, coarsening, explanation, or language-state owner before assigning value movement to style gains. |
| Prompt loop as improvement | The worker keeps regenerating more engaging drafts without a named object version, allowed change slice, protected trade-offs, or re-evaluation. | Open `E.22` when needed, route the repair to `E.23`, and re-evaluate the changed version through [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation]]; otherwise keep the generated text as an unadmitted candidate carrier under [[NSTD/06_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning]] and `C.35`. |
| Evaluation theft | Quality result is used as evidence, assurance, or gate. | Keep [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation]] as evaluation; route wider use to `A.10`, `B.3`, or gate owner. |
| Wrong-kind evaluation | Source text, style guide, script, or generated output is evaluated as narrative rendering. | Apply object-kind fit and return to the correct evaluation or admission owner. |
| Characteristics as eval programs | Test scripts or automated checks are treated as characteristics. | Keep characteristics in `A.19.ECS`; automated evals are measurement or eval-program carriers under direct owners. |

## [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]]:9 - Consequences

The benefit is a usable improvement target: `E.23` can improve narrative versions because values, floors, evidence, and repairs are declared. The cost is heavier evaluation before reliance-bearing use.

## [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]]:10 - Rationale

`A.19.ECS` says improvement cannot be better than its evaluation. [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] specializes that lesson for narrative renderings: first recover object kind and use, then choose characteristics that discriminate narrative rendering quality for that declared use.

## [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]]:11 - SoTA-Echoing

FPF `A.19.ECS` and `C.16` supply the characteristic-space and result-row discipline. FPF `C.33` supplies the structural-information note for architecture-relevant carriers, while the same general epiplexity line supplies the broader DPF pressure: a carrier is useful only to the extent that selected structure is recoverable under an observer and use boundary. FPF `C.2.LS`, `A.16.1`, `A.16.2`, `A.6.3.CSC`, `E.17.EFP`, `E.10`, `A.6.P`, and `C.16.Q` supply the language-state, cue, backoff, coarsening, explanation, lexical, relation, and quality-term repairs that narrative work often needs under different vocabulary. Castricato et al.'s "Towards a Formal Model of Narratives" supports evaluating narrator-reader information flow, reader story-model evolution, uncertainty, and conveyed-information accuracy. Mengelkamp et al.'s "Effects of Reading Goal Instructions on the Comprehension and Metacomprehension of Informative Narratives" and Georgiou et al.'s "Large-scale study of human memory for meaningful narratives" make declared learner use, memory, and overconfidence measurable pressures. Ma et al.'s "Text-to-Text Automatic Story Generation: A Survey" and Rahman et al.'s "Game Knowledge Management System: Schema-Governed LLM Pipeline for Executable Narrative Generation in RPGs" show that generated narratives need coherence, controllability, structural and semantic evaluation, and human-study probes rather than fluency alone. The DPF adopts those moves through `A.19.ECS`, `C.16`, DPF-local epiplexity basis rules, and FPF owner-routing for language-state and precision repairs, not by importing a generic writing-quality rubric.

## [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]]:12 - Relations

Uses `A.19.ECS`, `A.17`, `A.18`, `C.16`, `C.16.Q`, `C.2.LS`, `A.16.1`, `A.16.2`, `A.6.3.CSC`, `E.17.EFP`, `E.10`, `A.6.P`, `C.33`, `E.22`, `E.23`, `B.4`, `A.10`, `B.3`, `E.17`, `C.35`, and `G.11`. `C.33` is used here only when the evaluated narrative rendering is an architecture-relevant structural-information carrier; non-architecture cases keep the epiplexity basis local to [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] until a broader FPF owner is admitted. `E.23` consumes [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] result rows only after object version, allowed change slice, protected trade-offs, cost and risk, and re-evaluation form are explicit. `B.4` is used only for an evolution claim over a narrative episteme, learning route, or other holon under repeated use; `G.11` handles currentness and refresh. Reopen when evaluated object kind, declared use, source pack, characteristic set, language-state profile, cue or backoff status, coarsening or explanation relation, precision-restoration result, epiplexity basis, value meanings, floor, evidence basis, allowed improvement slice, or low-value repair route changes. Support-map entry: open `Architecture and Narrative Work Bridge` when `NarrativeRenderingEpiplexity` is architecture-relevant or tied to `C.33`; open `Semiotic And Language-Precision Bridge` for language-state, coarsening, explanation, relation, or quality-word repairs; open `Source Use And Refresh Map` when evidence basis or source-currentness supports a value; open `DPF Precision Restoration And Owner Map` when a characteristic name risks becoming a new ontology.

## [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]]:End
