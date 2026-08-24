---
type: "npf-knowledge-page"
context:
  - "NPF"
page_type: "npf-knowledge-page"
mode: "canonical-generated"
title: "DPF Relation Records"
part: "[[00_Hubs/NPF - Preface - Cross-Cutting Ideas And Principles]]"
parents:
  - "[[00_Hubs/NPF - Preface - Cross-Cutting Ideas And Principles]]"
source_file: "Narrativization-and-Narrative-Studies-Principles-Framework.md"
source_revision: "d77339d7056433de3ee55ad863860ee4b3006f6f"
source_sha256: "80f2d5ec3524b7947a3c36928bf774f61a9c68d4efc9ec5fc0d23206f01534e4"
generated_on: "2026-08-24"
source_lines:
  - 2648
  - 2788
status: "generated"
generated: true
---


These `PatternFrameworkRelationRecord@NarrativizationAndNarrativeStudiesPrinciplesFramework` records state package relations that matter during use, refresh, and reuse.

```text
PatternFrameworkRelationRecord@NarrativizationAndNarrativeStudiesPrinciplesFramework:
  relationId: PFR-NSTD-CORE-DEP-001
  sourceRef: NarrativizationAndNarrativeStudiesPrinciplesFramework@2026-06-30
  targetRef: FPFCorePatternSet@current
  relationFunction: Framework edition dependency
  governedUse: DPF patterns rely on FPF Core relation, source, evaluation, ethics, evidence, assurance, generated-carrier, publication, and refresh owners
  directGoverningPatternRef: E.4.PFR
  dependencyOrEditionEffect: DPF depends on Core; Core has no reverse dependency
  blockedStrongerReading: not Core specialization by dependency and not permission to redefine Core owners
  refreshOrSupersessionCondition: refresh when relevant FPF Core edition changes
```

```text
PatternFrameworkRelationRecord@NarrativizationAndNarrativeStudiesDPF:
  relationId: PFR-NSTD-NAR-SPEC-001
  sourceRef: [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose|NSTD.1]] through [[NSTD/07_08_Learning-Route Narrative Rendering and Reconstruction Return/00_NSTD.08 - Learning-Route Narrative Rendering and Reconstruction Return|NSTD.8]]
  targetRef: A.6.3.NAR
  relationFunction: Specialization and pattern-use support
  governedUse: DPF narrows Core structure-to-narrative rendering for narrative studies and teaching uses
  directGoverningPatternRef: A.6.3.NAR
  dependencyOrEditionEffect: DPF inherits Core relation obligations and adds domain checks
  blockedStrongerReading: DPF does not redefine Core A.6.3.NAR, E.17.EFP, source, evidence, ethics, or assurance owners
  sourceReturnCondition: return to Core when a DPF row tries to govern the source-to-rendering relation generally
  refreshOrSupersessionCondition: refresh when A.6.3.NAR changes the Core relation slots or source-return obligations
```

```text
PatternFrameworkRelationRecord@NarrativizationAndNarrativeStudiesDPF:
  relationId: PFR-NSTD-CGUS-DEP-001
  sourceRef: [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose|NSTD.1]], [[NSTD/01_02_Structure-to-Sequence Ordering/00_NSTD.02 - Structure-to-Sequence Ordering|NSTD.2]], [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]], and [[NSTD/07_08_Learning-Route Narrative Rendering and Reconstruction Return/00_NSTD.08 - Learning-Route Narrative Rendering and Reconstruction Return|NSTD.8]]
  targetRef: A.22.CGUS
  relationFunction: Downstream use of constraint-governed unfolding structures
  governedUse: narrative rendering may select, order, evaluate, or teach a demonstrative slice over a wider constraint-governed unfolding structure
  directGoverningPatternRef: A.22.CGUS
  dependencyOrEditionEffect: DPF depends on Core CGUS distinctions; Core has no reverse dependency on this DPF
  blockedStrongerReading: narrative sequence, learning route, or framework carrier is not the selected unfolding structure by presentation
  sourceReturnCondition: return to A.22.CGUS or the local FPF governing pattern when preserved and lost structure, admissible next form, direct exit, or stop condition is missing
  refreshOrSupersessionCondition: refresh when A.22.CGUS, E.18.3, A.6.3.NAR, or local CGUS block guidance changes
```

```text
PatternFrameworkRelationRecord@NarrativizationAndNarrativeStudiesDPF:
  relationId: PFR-NSTD-SRC-REUSE-001
  sourceRef: Source Use And Refresh Map under G.2
  targetRef: [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose|NSTD.1]] through [[NSTD/07_08_Learning-Route Narrative Rendering and Reconstruction Return/00_NSTD.08 - Learning-Route Narrative Rendering and Reconstruction Return|NSTD.8]]
  relationFunction: Source or decision reuse
  governedUse: source rows support narratology, science-storytelling, teaching, evaluation, and generation claims by value
  directGoverningPatternRef: G.2
  blockedStrongerReading: source rows do not become ethical, evidence, assurance, or authority owners
  sourceReturnCondition: return to G.2 when source classification, currentness, rival tradition, or exact source row is missing
  refreshOrSupersessionCondition: refresh when source basis or SoTA currentness changes
```

```text
PatternFrameworkRelationRecord@NarrativizationAndNarrativeStudiesDPF:
  relationId: PFR-NSTD-EVAL-001
  sourceRef: [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]]
  targetRef: [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose|NSTD.1]] through [[NSTD/07_08_Learning-Route Narrative Rendering and Reconstruction Return/00_NSTD.08 - Learning-Route Narrative Rendering and Reconstruction Return|NSTD.8]]
  relationFunction: Quality framing, evaluation, or improvement
  governedUse: evaluate one narrative rendering version or learning route for declared use and feed repair to E.23 when values exist
  directGoverningPatternRef: A.19.ECS
  preservationOrAdmissionRef: NarrativeRenderingQualityEvaluationCharacteristicSpace@Context
  blockedStrongerReading: [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] is not evidence, assurance, admission, publication, gate, decision, or pattern-quality authority
  sourceReturnCondition: return to A.19.ECS or C.16 when object kind, scale, value meaning, or measurement basis is defective
  refreshOrSupersessionCondition: refresh when evaluation floor, characteristics, use, evidence basis, or low-value repair route changes
```

```text
PatternFrameworkRelationRecord@NarrativizationAndNarrativeStudiesDPF:
  relationId: PFR-NSTD-IMPROVEMENT-001
  sourceRef: NarrativeRenderingQualityEvaluationResult@Context
  targetRef: E.22 and E.23
  relationFunction: Narrative rendering quality-loop transfer
  governedUse: improve one exact narrative rendering version or declared changed slice by rerunning [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] after repairs
  directGoverningPatternRef: E.23; E.22 when the improvement question needs framing
  preservationOrAdmissionRef: NarrativeRenderingImprovementLoopInput@Context
  blockedStrongerReading: an [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] low value, style suggestion, prompt retry, or generated variant is not an improvement claim until the changed object version is re-evaluated
  sourceReturnCondition: return to [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] when object version, declared use, result rows, protected trade-offs, allowed change slice, cost and risk, or expected re-evaluation form is missing
  refreshOrSupersessionCondition: refresh through G.11 when source currentness, reader telemetry, teaching-test evidence, FPF edition, generated-narrative practice, or evaluation characteristic space changes
```

```text
PatternFrameworkRelationRecord@NarrativizationAndNarrativeStudiesDPF:
  relationId: PFR-NSTD-GENCARRIER-001
  sourceRef: generated or discovered carrier that may carry a candidate narrative rendering
  targetRef: [[NSTD/06_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning|NSTD.7]]
  relationFunction: Produced-carrier admission
  governedUse: admit or reject generated narrative output before it is evaluated as narrative rendering or used in teaching
  directGoverningPatternRef: C.35
  preservationOrAdmissionRef: AutomatedNarrativizationAdmissionCase@Context
  blockedStrongerReading: generated fluency, coherence, controllability, or schema compliance is not source authority, evidence, assurance, or admission
  sourceReturnCondition: return to C.35 when produced carrier, described structure, preserved structure, lost structure, or receiving owner is missing
  refreshOrSupersessionCondition: refresh when generator, source plan, schema, source edition, or admission result changes
```

```text
PatternFrameworkRelationRecord@NarrativizationAndNarrativeStudiesDPF:
  relationId: PFR-NSTD-TEACHING-CARRIER-001
  sourceRef: external FPF seminar or teaching test-run publication carrier
  targetRef: [[NSTD/07_08_Learning-Route Narrative Rendering and Reconstruction Return/00_NSTD.08 - Learning-Route Narrative Rendering and Reconstruction Return|NSTD.8]]
  relationFunction: Publication or teaching publication-carrier relation
  governedUse: teaching files expose or test a learning narrative route without entering DPF pattern bodies
  directGoverningPatternRef: E.17
  preservationOrAdmissionRef: LearningNarrativeRoute@Context
  blockedStrongerReading: teaching publication carrier is not the DPF pattern body, not FPF source authority, and not a narrative rendering quality result
  sourceReturnCondition: return to source patterns when teaching examples lose selected source structure
  refreshOrSupersessionCondition: refresh when learner telemetry, session sequence, source structure spine, or carrier publication condition changes
```

```text
PatternFrameworkRelationRecord@NarrativizationAndNarrativeStudiesDPF:
  relationId: PFR-NSTD-TEACHING-EVAL-001
  sourceRef: external FPF seminar or teaching test-run publication carrier
  targetRef: [[NSTD/07_08_Learning-Route Narrative Rendering and Reconstruction Return/00_NSTD.08 - Learning-Route Narrative Rendering and Reconstruction Return|NSTD.8]] and [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]]
  relationFunction: Narrative-route evaluation and improvement relation
  governedUse: evaluate learner reconstruction and source-return readiness for the learning route, then feed repair to E.23 when values exist
  directGoverningPatternRef: [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]]; E.23 when improvement values exist
  preservationOrAdmissionRef: NarrativeRenderingQualityResultRow@Context
  blockedStrongerReading: evaluation result is not publication permission, source authority, evidence, assurance, or package authority
  sourceReturnCondition: return to [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] when evaluated object kind, value meaning, evidence basis, or low-value repair route is missing
  refreshOrSupersessionCondition: refresh when learner telemetry, quality floor, evaluation result, or improvement route changes
```

```text
PatternFrameworkRelationRecord@NarrativizationAndNarrativeStudiesDPF:
  relationId: PFR-NSTD-ETHICS-EVIDENCE-ASSURANCE-001
  sourceRef: [[NSTD/03_04_Voice, Focalization, and Agency/00_NSTD.04 - Voice, Focalization, and Agency|NSTD.4]] and [[NSTD/04_05_Engagement, Attention, and Motivation/00_NSTD.05 - Engagement, Attention, and Motivation|NSTD.5]]
  targetRef: D.1-through-D.5, A.10, B.3
  relationFunction: Governing-pattern relation
  governedUse: route agency, responsibility, persuasion, harm, evidence, and assurance claims out of narrative-effects vocabulary
  directGoverningPatternRef: direct owner named by claim kind
  blockedStrongerReading: viewpoint, protagonist, actant, engagement, or fluency does not assign responsibility, capability, evidence, assurance, or moral permission
  sourceReturnCondition: return to direct owner when claim-bearing ethics, evidence, assurance, or responsibility language appears
  refreshOrSupersessionCondition: refresh when FPF ethics, evidence, or assurance owner guidance changes
```
