---
type: "npf-pattern"
context:
  - "NPF"
page_type: "npf-pattern"
mode: "canonical-generated"
npf_id: "NSTD.7"
title: "Automated Narrativization and Story Planning"
part: "[[00_Hubs/NPF - Preface - Cross-Cutting Ideas And Principles]]"
parents:
  - "[[00_Hubs/NPF - Preface - Cross-Cutting Ideas And Principles]]"
source_file: "Narrativization-and-Narrative-Studies-Principles-Framework.md"
source_revision: "d77339d7056433de3ee55ad863860ee4b3006f6f"
source_sha256: "80f2d5ec3524b7947a3c36928bf774f61a9c68d4efc9ec5fc0d23206f01534e4"
generated_on: "2026-08-24"
source_lines:
  - 1773
  - 2030
status: "generated"
generated: true
---


> **Type:** DPF pattern body

> **Primary EntityOfConcern:** `AutomatedNarrativizationAdmissionCase@Context`, a DPF-local case record for generated or tool-assisted narrative output.

## [[NSTD/06_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning|NSTD.7]]:1 - Problem frame

Use this pattern when LLM, NLG, graph-to-text, data-to-text, story-planning, schema-governed generation, or search is used to produce or repair narrative renderings.

First useful move: split admitted source basis, generated carrier, source-to-narrative relation, structure capture or loss, correspondence, generation method, evaluation, evidence, assurance, and human admission responsibility.

What goes wrong if missed: generated fluency, schema compliance, controllability, or story-plan coherence becomes source authority.

What this buys: automation can help produce narrative candidates without admitting them as source-grounded renderings before checks.

## [[NSTD/06_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning|NSTD.7]]:2 - Problem

Automated systems can produce fluent, coherent-looking, and controllable-looking narratives that fail source grounding, plot or event consistency, schema constraints, source-return discipline, ethical boundary, or human interpretive responsibility. The issue is not whether generation is useful. It is what kind of object has been produced and what owner can use it.

## [[NSTD/06_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning|NSTD.7]]:3 - Forces

| Force | Tension |
| --- | --- |
| Fast generation vs admission | Tools can produce carriers quickly, but admission requires owner checks. |
| Schema control vs source truth | A valid story schema does not prove source fidelity. |
| Fluency vs correspondence | Fluent text can lose selected structure. |
| Automation vs responsibility | Human responsibility for source selection and admission remains explicit. |

## [[NSTD/06_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning|NSTD.7]]:4 - Solution

Use a kind-splitting record before evaluating or publishing generated output as a narrative rendering.

```text
AutomatedNarrativizationAdmissionCase@Context:
  sourceMaterialOrSourcePackRef:
  generatedCarrierRef:
  generationMethodOrMethodDescriptionRef:
  sourcePlanRef?:
  plotOrEventPlanRef?:
  schemaConstraintRefs?:
  c35AdmissionRef:
  narRelationRef:
  structureCaptureLossRef:
  correspondenceRef:
  evaluationRef:
  evidenceOwnerRefs?:
  assuranceOwnerRefs?:
  humanAdmissionResponsibilityRef:
  nonAdmissibleUse:
  repairOrRejectCondition:
```

Owner split:

| Claim kind | Owner |
| --- | --- |
| Source basis or source pack | `G.2`, `A.10`, `E.17.EFP` |
| Generated or discovered carrier admission | `C.35` |
| Source-to-narrative relation | `A.6.3.NAR` and this DPF |
| Structure capture and loss | `C.33` for architecture-relevant carriers; [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation]] epiplexity basis for non-architecture DPF cases |
| Correspondence or preservation | `C.34` |
| Generation procedure | method or method-description owner, with source-pack grounding |
| Narrative rendering quality evaluation | [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation]], `A.19.ECS`, `C.16` |
| Repeated quality improvement | `E.22` when the quality question is not framed, then `E.23` using [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation]] result rows and re-evaluation |
| Evidence | `A.10` |
| Assurance | `B.3` |
| Ethics, harm, bias, affected parties | `D.1` through `D.5` |
| Human responsibility for admission | role, assignment, work, decision, or governance owner as applicable |

Use a six-stage generated-narrative pipeline. Each stage may be lightweight, but it must not be skipped by a fluent final carrier.

| Stage | Required separation | Typical failure |
| --- | --- | --- |
| Source grounding | Admitted source basis, source pack, selected structures, source-currentness, and non-use boundary are named before generation. | The prompt is treated as admitted source basis; missing constraints are invented by the model. |
| Content planning | Source structures to include, omit, foreground, or protect are listed. | The generator chooses content implicitly and loses the denominator for epiplexity. |
| Discourse or sequence planning | Ordering rule, reveal rule, event plan, or learning route is stated. | Plausible prose hides wrong chronology, causality, proof order, or canon order. |
| Realization | Language state, style, compression, viewpoint, and engagement devices are selected as rendering choices. | Tone and fluency are mistaken for source fidelity. |
| Admission | `C.35` or an equivalent admission owner separates generated carrier from admitted narrative rendering. | Prompt output is used directly in teaching, publication, or decision support. |
| Evaluation and repair | [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation]] evaluates the admitted rendering, and low values route repair through the smallest owner. | Regeneration continues until it "sounds better" without re-evaluation. |

For schema-governed generation, treat schema compliance as one input, not as admission. A schema can constrain scene fields, character roles, location, source refs, branch structure, or game-engine requirements. It cannot prove that selected source structures were preserved, that evidence is sufficient, or that human responsibility was assigned. Record schema constraints in the admission case, then test structural and semantic correspondence through `C.34` and [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]].

For LLM-assisted analysis or theme generation, treat the model output as an interpretive aid. The worker must still own source selection, coding or theme acceptance, reflexive judgment, and downstream use. A generated theme, plot plan, or source plan may become admitted source basis for later narrative work only after admission and source-return conditions are explicit.

Use three probes before relying on automated output:

1. Source perturbation probe: remove or change one constraint in the admitted source basis and check whether the generated carrier changes in the expected way. If it does not, the output may not be grounded in the declared admitted source basis.
2. Structure recovery probe: ask a reader or evaluator to reconstruct selected source structures from the generated carrier without seeing the prompt. Low recovery returns to content planning or ordering.
3. Responsibility probe: ask who is accountable for source selection, admission, publication, and reliance. If the answer is "the model", the case is not admitted.

## [[NSTD/06_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning|NSTD.7]]:5 - Archetypal Grounding

### Mature generated-narrative pipeline: graph-to-text case

An AI agent receives a source graph and produces a polished explanation. [[NSTD/06_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning|NSTD.7]] treats the output as a candidate carrier until the source plan, method, admission, and evaluation path are explicit.

```text
GeneratedNarrativePipelineRecord@GraphToTextTeaching:
  sourceMaterialOrSourcePackRef: concept graph with dependency, example, counterexample, and evidence links
  selectedSourceStructureRefs: prerequisite chain, contrast pairs, evidence-return points
  generatorOrMethodRef: LLM-assisted graph-to-text workflow
  sourcePlanRef: selected nodes and relations to preserve
  discourseOrStoryPlanRef: didactic dependency order with contrast reveal
  realizationCarrierRef: generated prose candidate
  admissionOwnerRef: `C.35`
  evaluationOwnerRef: [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]]
  humanResponsibilityOwnerRef: human narrator or teacher
  blockedOverread: fluent output is not source truth, admission, evidence, assurance, or improvement
  refreshCondition: source graph, generator behavior, schema, or evaluation result changes
```

Pipeline steps:

1. Source plan: select nodes, relations, losses, and source-return refs.
2. Discourse plan: choose ordering rule through [[NSTD/01_02_Structure-to-Sequence Ordering/00_NSTD.02 - Structure-to-Sequence Ordering|NSTD.2]].
3. Realization: generate wording.
4. Admission: decide whether the carrier-borne output can be admitted and evaluated as a narrative rendering through `C.35`.
5. Evaluation: evaluate through [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]].
6. Repair: use `E.23` only after object version and changed slice are explicit.

### Probe suite for generated narrative

| Probe | Question | Pass condition | Failure repair |
| --- | --- | --- | --- |
| Source perturbation | If one source relation changes, does the generated narrative change at the right place? | The affected sentence, order marker, or source-return link changes. | Recover source plan; do not rely on prompt fluency. |
| Structure recovery | Can a reader reconstruct selected source structure from the output? | Reader recovers nodes and relations needed for declared use and knows lost relations. | Add source-return markers or narrow declared use. |
| Responsibility | Who is responsible for source selection, admission, and publication? | Human or tool-owner roles are explicit; generated output has no authority by fluency. | Route to `C.35`, `A.10`, `B.3`, `E.17`, or ethics owners. |
| Schema-governance | Does schema constrain output or only decorate the prompt? | Missing source slots prevent admission or lower evaluation. | Make schema executable or mark it as weak guide. |
| Improvement evidence | Is the new variant better under [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation]] rows? | Re-evaluation shows expected value movement without protected trade-off loss. | Keep variant as candidate and reframe through `E.22`/`E.23`. |

### Before and after repair: generated seminar outline

Before:

> The generated outline sounds coherent and covers all important ideas, so it can be used as a DPF learning route.

Failure: source plan, admission, reconstruction task, and evaluation route are missing. "Covers all important ideas" is the model's hidden selection, not a source structure.

After:

> The generated outline is a candidate teaching publication carrier. Its source plan selects `EntityOfConcern`, forces, solution, relation exits, and improvement loop. Its discourse plan uses didactic prerequisite order. It is not a DPF pattern and not a public teaching route until `C.35` admits the carrier and [[NSTD/07_08_Learning-Route Narrative Rendering and Reconstruction Return/00_NSTD.08 - Learning-Route Narrative Rendering and Reconstruction Return|NSTD.8]]/[[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] show that learners can reconstruct the source spine.

### Mature generated-storycraft boundary

For the franchise continuation probe, a generated scene is especially risky because fluency and tone can hide source-pack violations. The DPF does not need to teach storycraft in full. It needs to require source-plan and responsibility discipline:

- source pack before scene;
- continuity and agency constraints before plot twist;
- private-use boundary before publication-like wording;
- perturbation test before claiming consistency;
- [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] evaluation before improvement;
- human responsibility before any reliance-bearing use.

### Calibration for generated narrative

| Value | Generated-carrier condition |
| --- | --- |
| `2` | Output is fluent, but source plan, admission, or evaluation route is missing. |
| `3` | Source plan exists, but probes or responsibility split are incomplete. |
| `4` | Source plan, discourse plan, admission, evaluation, and responsibility are explicit for declared use. |
| `5` | Perturbation, recovery, responsibility, and improvement probes pass across at least two heterogeneous generated cases. |

### FPF owner teaching

[[NSTD/06_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning|NSTD.7]] is not a prompt-engineering trick. It applies FPF's carrier discipline to generated narrative: produced text is a carrier, not source truth; admission is separate from fluency; improvement needs evaluation rows; source currentness and generator behavior can decay. This is why `C.35`, `G.2`, `G.11`, `A.10`, `B.3`, `E.17`, [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]], and `E.23` remain visible.

An LLM drafts a story-like explanation of FPF pattern use from source notes. [[NSTD/06_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning|NSTD.7]] records the prompt output as generated carrier, the source notes as admitted source basis, the prompt and generator as method-description context, and `C.35` as admission owner. Only after selected source structures, losses, and source-return condition are recovered may [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] evaluate it as a narrative rendering.

A graph-to-text system turns an event graph into a match recap. The event graph, source timestamp, uncertainty markers, and official-result refresh route are admitted source basis for this rendering. The generated recap is a carrier. If the system adds causal explanations not in the graph, those claims are not admitted by graph-to-text success. Repair by lowering causal language, adding source return, or opening the evidence owner.

A game story-planning pipeline generates a branching scene. The schema may require objective, location, actors, traits, constraints, and available actions. [[NSTD/06_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning|NSTD.7]] treats those fields as method and source-plan support, not as proof of playable, coherent, or ethically acceptable narrative. Structural, semantic, executable, and human probes remain separate from fluency.

An LLM proposes themes from interview notes for qualitative narrative analysis. The generated theme list is not the researcher's interpretation by default. Human interpretive agency remains live: the researcher checks source excerpts, reflexive stance, alternative readings, and admissible use before any narrative rendering or report uses the generated material.

Use admission and rejection examples.

| Generated carrier | Admit as narrative rendering? | Reason |
| --- | --- | --- |
| A fluent summary from a prompt with no source refs. | No. | Admitted source basis and selected structure are not recoverable. |
| A graph-to-text candidate with source event ids, ordering rule, and explicit lost relations. | Candidate after `C.35`. | It can proceed to [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation]], but source recovery and relation strength still need value assignment. |
| A schema-valid RPG scene that ignores a required canon constraint. | No for source-faithful use. | Schema compliance does not establish correspondence. |
| A generated FPF seminar outline with source-spine refs and reconstruction tasks. | Candidate teaching publication carrier. | It remains outside DPF pattern bodies and needs [[NSTD/07_08_Learning-Route Narrative Rendering and Reconstruction Return/00_NSTD.08 - Learning-Route Narrative Rendering and Reconstruction Return]]/[[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation]]. |
| A generated metaphor for homotopy that helps intuition but lacks proof boundary. | Orientation cue only. | It may feed `A.16.1` or [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose]], not admitted rendering quality yet. |

When automated repair is used, preserve version identity. "Regenerate until better" destroys improvement evidence. Record the previous carrier, changed prompt or method, selected changed slice, expected value movement, protected trade-offs, and re-evaluation route. A generated variant can be more fluent and still worse on epiplexity, source return, or agency discipline.

Pipeline variants by source type:

| Source type | Content plan | Discourse or story plan | Admission danger | Evaluation focus |
| --- | --- | --- | --- | --- |
| Knowledge graph or event graph | Select nodes, edges, event ids, uncertainty, and omissions. | Choose traversal, grouping, and return links. | Treating graph coverage as semantic truth. | Epiplexity, ordering recoverability, relation strength. |
| Architecture source pack | Select structures, candidate trade-offs, decisions, telemetry, and residual exceptions. | Use decision-memory or trade-off route. | Treating generated explanation as architecture decision or assurance. | Structural-information capture, correspondence, source return. |
| Fictional canon or source pack | Select canon constraints, premise, agency, continuity, and non-use boundary. | Use causal plot plus reveal order. | Treating private generated scene as authorized continuation. | Continuity, character agency, causal support, rights boundary. |
| Teaching source spine | Select concepts, dependencies, examples, counterexamples, tasks. | Use didactic prerequisite route with repeated anchors. | Treating generated outline as source framework. | Reconstruction tasks, learning-route quality, source-return readiness. |
| Qualitative notes or interviews | Select excerpts, themes, alternative readings, reflexive stance. | Use analysis narrative with traceable source excerpts. | Treating generated theme as researcher judgment. | Human interpretive agency, source traceability, ethical boundary. |

If a pipeline variant requires a source type not covered by the current source pack, mark the case as a source-refresh trigger rather than silently generalizing. A graph-to-text claim, for example, may require a more specific graph-to-text source than a general NLG survey. A game narrative pipeline may need executable or playability probes that a plain text-generation source does not supply.

## [[NSTD/06_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning|NSTD.7]]:6 - Bias-Annotation

This pattern blocks generated-fluency admission drift: an LLM, NLG system, graph-to-text tool, schema, or story planner produces coherent text and that text is treated as admitted narrative rendering, evidence, assurance, or source authority. Repair by splitting generated carrier, admitted source basis, generation method, source-to-narrative relation, capture or loss, correspondence, evaluation, and human admission responsibility. Scope: DPF-local for automated narrativization; it does not replace `C.35` admission or source-pack owners.

## [[NSTD/06_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning|NSTD.7]]:7 - Conformance Checklist

| Check | Passing condition |
| --- | --- |
| `CC-NSTD7-1` | Generated carrier is separated from admitted source basis, selected source structure, admitted narrative rendering, evidence, and assurance. |
| `CC-NSTD7-2` | `C.35` admission is present before generated output feeds candidate, narrative, or teaching use. |
| `CC-NSTD7-3` | Source plan, plot or event plan, schema constraints, and generation method are named when relied on. |
| `CC-NSTD7-4` | Fluency, coherence, controllability, schema compliance, and story planning do not become authority, evidence, or admission. |
| `CC-NSTD7-5` | Human admission responsibility is explicit for source selection, interpretation, publication, and reliance-bearing use. |
| `CC-NSTD7-6` | A generated variant is not called an improvement unless an exact changed rendering version or changed slice is re-evaluated through [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation]] and handed to `E.22` or `E.23` with protected trade-offs, cost and risk, and expected re-evaluation form. |

## [[NSTD/06_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning|NSTD.7]]:8 - Common Anti-Patterns and How to Avoid Them

| Anti-pattern | What fails | Repair |
| --- | --- | --- |
| Fluent generated output as narrative rendering | Carrier admission and source recovery are skipped. | Apply `C.35`, recover selected structure, then evaluate through [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation]]. |
| Schema compliance as source fidelity | The story satisfies a schema but changes the selected source structure or a constraint in the admitted source basis. | Add `C.34` correspondence checks; use `C.33` capture-loss checks only for architecture-relevant structural-information use, and use [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation]] epiplexity for non-architecture source-structure loss. |
| Automation as responsibility holder | Tool output is treated as responsible admission. | Name human role assignment, method, work, decision, or governance owner. |
| Regeneration as improvement | The worker generates another fluent variant and treats it as quality movement. | Keep the variant as a generated carrier until admission, run [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation]] on the changed rendering version, and use `E.22` or `E.23` only after the improvement question, protected trade-offs, cost and risk, and re-evaluation form are explicit. |

## [[NSTD/06_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning|NSTD.7]]:9 - Consequences

The benefit is productive automation without false authority. The cost is an admission step and repair or rejection route for generated carriers.

## [[NSTD/06_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning|NSTD.7]]:10 - Rationale

Modern NLG, LLM, graph-to-text, data-to-text, and story-planning practice makes generation useful but not self-justifying. FPF already has the owners needed for admission, source, structure, correspondence, evaluation, evidence, assurance, and work responsibility.

## [[NSTD/06_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning|NSTD.7]]:11 - SoTA-Echoing

### Operational comparison against domain vocabulary

This DPF intentionally translates domain vocabulary into FPF owner work instead of importing it whole. When narratology says story, discourse, and presentation, this package asks: what source structure is selected, what order is chosen, what is foregrounded, and what source return remains? When cognitive narratology says event model, transportation, perspective, or memory, this package asks: which reconstruction target, engagement device, viewpoint, or evaluation characteristic is being changed? When NLG says content planning, discourse planning, and realization, this package asks: what is the source plan, what is the ordering rule, what is the generated carrier, and what admission and evaluation route owns it?

The practical consequence is a repair rule. If a domain term helps the worker choose or repair a narrative move, keep it as DPF vocabulary. If it starts carrying evidence, assurance, ethics, agency, publication, or Core ontology, route the claim to the FPF owner and state the blocked overread.

Gatt and Krahmer's `Survey of the State of the Art in Natural Language Generation` separates content planning, discourse planning, and realization; Alabdulkarim et al.'s "Automatic Story Generation: Challenges and Attempts" and Cardona-Rivera and Ware et al.'s "The Story So Far on Narrative Planning" keep story planning, plot structure, and consistency visible; Chakrabarty et al.'s "SceneCraft" and Rahman et al.'s "Game Knowledge Management System" show schema-governed and interactive generation pressures; Ma et al.'s "Text-to-Text Automatic Story Generation: A Survey" names coherence, consistency, diversity, controllability, datasets, and evaluation limits; Nguyen-Trung and Nguyen's "Narrative-Integrated Thematic Analysis" requires human interpretive agency. The DPF adopts these as owner-splitting requirements rather than as one automation pattern that grants trust.

Operational payload:

- From NLG, keep content planning, discourse planning, and realization separate. If a tool only returns final prose, reconstruct or reject the missing planning stages before reliance.
- From story-generation surveys, coherence and controllability are necessary but not sufficient. They must be connected to selected source structure, correspondence, admission, and declared use.
- From narrative planning, plot or event plan is a method artifact. It can guide generation but cannot become source truth.
- From schema-governed generation, schema fields can support repair and normalization, but schema compliance is not semantic fidelity or human evaluation.
- From interactive game generation, executable or playability probes may be needed when the narrative must function inside an engine or workflow; text fluency alone is the wrong evidence.
- From LLM-assisted qualitative analysis, human interpretive agency remains load-bearing. Generated themes, routes, or plans are aids until admitted by the responsible worker.

The practical consequence is that [[NSTD/06_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning|NSTD.7]] should make automated work more usable, not more magical. It protects speed by preventing hidden authority transfer from model output to source truth.

## [[NSTD/06_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning|NSTD.7]]:12 - Relations

Uses `G.2`, `C.35`, `A.6.3.NAR`, `C.33` for architecture-relevant structural-information capture or loss, `C.34`, [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]], `A.19.ECS`, `C.16`, `E.22`, `E.23`, `A.10`, `B.3`, `D.1` through `D.5`, and `G.11`. `E.22`/`E.23` apply only after carrier admission and [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] result rows exist; generation retries remain carrier candidates until re-evaluation. Reopen when admitted source basis, generator, method, schema, admission note, evaluation result, or generated-narrative SoTA changes. Support-map entry: open `Source Use And Refresh Map` when generation, NLG, story-planning, schema, or source-pack claims are relied on; open `DPF Precision Restoration And Owner Map` when generated source plan, plot plan, schema constraint, admission, correspondence, or responsibility words blur object kinds; open `Semiotic And Language-Precision Bridge` when prompt output changes language state, coarsening, cue, or quality wording.

## [[NSTD/06_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning|NSTD.7]]:End
