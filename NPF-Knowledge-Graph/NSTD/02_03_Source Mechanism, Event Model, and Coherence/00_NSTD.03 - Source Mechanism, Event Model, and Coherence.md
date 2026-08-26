---
type: "npf-pattern"
context:
  - "NPF"
page_type: "npf-pattern"
mode: "canonical-generated"
npf_id: "NSTD.3"
title: "Source Mechanism, Event Model, and Coherence"
part: "[[00_Hubs/NPF - Preface - Cross-Cutting Ideas And Principles]]"
parents:
  - "[[00_Hubs/NPF - Preface - Cross-Cutting Ideas And Principles]]"
source_file: "Narrativization-and-Narrative-Studies-Principles-Framework.md"
source_revision: "d77339d7056433de3ee55ad863860ee4b3006f6f"
source_sha256: "80f2d5ec3524b7947a3c36928bf774f61a9c68d4efc9ec5fc0d23206f01534e4"
generated_on: "2026-08-26"
source_lines:
  - 715
  - 958
status: "generated"
generated: true
---


> **Type:** DPF pattern body

> **Primary EntityOfConcern:** `NarrativeEventMechanismSupport@Context`, a DPF-local support record for one narrative rendering.

## [[NSTD/02_03_Source Mechanism, Event Model, and Coherence/00_NSTD.03 - Source Mechanism, Event Model, and Coherence|NSTD.3]]:1 - Problem frame

Use this pattern when locally fluent narrative passages fail because readers cannot build a coherent model of source mechanism, event flow, dependency structure, architecture relation, state change, or proof dependency.

First useful move: state whether the selected source structure is event-like, mechanism-like, dependency-like, architecture-like, proof-like, canon-like, or mixed; then state what readers must reconstruct for the declared use.

What goes wrong if missed: fluency is mistaken for source coherence. Readers remember the story but cannot say what changed, why it changed, which relation mattered, or where the claim stops.

What this buys: coherence is tied to recoverable source structure, not to smooth prose alone.

## [[NSTD/02_03_Source Mechanism, Event Model, and Coherence/00_NSTD.03 - Source Mechanism, Event Model, and Coherence|NSTD.3]]:2 - Problem

Narratives often use events and agents because they are easy to follow. But many source structures are not event sequences. Architecture structures, mathematical definitions, evidence graphs, mechanism diagrams, and source packs can be misread when forced into a fiction-like event model.

## [[NSTD/02_03_Source Mechanism, Event Model, and Coherence/00_NSTD.03 - Source Mechanism, Event Model, and Coherence|NSTD.3]]:3 - Forces

| Force | Tension |
| --- | --- |
| Event readability vs non-event structures | Readers follow events easily, but not every source relation is an event. |
| Causal wording vs causal support | "Because" helps comprehension but may need `C.28`. |
| Mechanism clarity vs uncertainty | A good mechanism story can hide unknown or contested source relations. |
| Reconstruction vs entertainment | The declared use may require reconstruction, not only engagement. |

## [[NSTD/02_03_Source Mechanism, Event Model, and Coherence/00_NSTD.03 - Source Mechanism, Event Model, and Coherence|NSTD.3]]:4 - Solution

Use an event and mechanism support record when the narrative asks readers to understand change, dependency, or explanation.

```text
NarrativeEventMechanismSupport@Context:
  narrativeRenderingRef:
  sourceStructureKind:
  requiredReaderReconstruction:
  eventOrMechanismModel:
  participatingHolonOrRoleRefs?:
  dependencyOrConstraintRefs?:
  causalUseOwnerRef?:
  uncertaintyOrUnknownRefs?:
  reconstructionTaskRefs?:
  sourceReturnCondition:
```

Then perform four checks: source structure kind, reader reconstruction target, supported relation claims, and source return.

Build the support record before polishing the prose.

1. Convert each important passage into a source-support row: what changed, what relation is being suggested, what source structure backs it, and what remains unknown.
2. Mark the relation strength: observed event, temporal sequence, dependency, constraint, mechanism hypothesis, causal claim, proof dependency, architecture trade-off, canon continuity, or reader-facing analogy.
3. Mark the reconstruction target: after reading, what should the reader be able to state, distinguish, predict, update, or return to source for?
4. Mark the overclaim risk: which verbs, connectors, or story beats make the relation sound stronger than the source allows?
5. Add repair before style: lower the relation word, add uncertainty, add source return, or open the direct owner.

Use these relation-strength distinctions in narrative review.

| Narrative wording pressure | Minimum support needed | Direct owner when stronger |
| --- | --- | --- |
| "then" or "after" | Event or sequence source | Source or event owner if factual |
| "because" | Causal or mechanism support | `C.28`, evidence owner, or domain causal owner |
| "therefore" | Inference or proof support | Proof or evidence owner and source return |
| "had to" | Constraint or necessity support | Constraint, architecture, proof, or canon owner |
| "wanted" or "decided" | Agent or responsibility support | `A.13`, `A.2`, `A.2.1`, `D.*` when ethical |
| "shows that" | Evidence support | `A.10` and source owner |

For non-event structures, do not invent fake events just to make a story move. A proof dependency can be narrated as a sequence of questions and distinctions; an architecture view can be narrated as a path through forces and trade-offs; a source pack can be narrated as a controlled return route. The narrative event model is only a reader-facing scaffold. The selected source structure remains the denominator for reconstruction and later [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] evaluation.

Reader reconstruction tasks should be concrete:

- "Name the mechanism and the unresolved relation" is better than "understand the mechanism."
- "Distinguish observed event, inference, and prediction" is better than "follow the live story."
- "Point to the formal statement where the analogy stops" is better than "get the math intuition."
- "Recover which architecture trade-off was accepted and which exception remains" is better than "remember the project story."

If no reconstruction task can be written, the narrative may still be entertaining or orienting, but it is not yet a reliable structure-to-narrative rendering for a reliance-bearing use.

## [[NSTD/02_03_Source Mechanism, Event Model, and Coherence/00_NSTD.03 - Source Mechanism, Event Model, and Coherence|NSTD.3]]:5 - Archetypal Grounding

### Mature worked slice: event support in a scientific narrative

A science narrative says: "The failed experiment forced the theory to change." That line may be a useful story beat, but it hides several relation kinds: observed result, incompatibility with expectation, proposed mechanism, community decision, and later evidence. [[NSTD/02_03_Source Mechanism, Event Model, and Coherence/00_NSTD.03 - Source Mechanism, Event Model, and Coherence|NSTD.3]] repairs the relation support before the story is trusted.

```text
NarrativeEventSupportRecord@ExperimentTension:
  narrativeRenderingRef: ScienceStory@v1
  eventOrMechanismClaim: failed measurement challenged the prior mechanism hypothesis
  sourceStructureRef: measurement record, model expectation, uncertainty interval, alternative explanations
  relationStrength: observed mismatch plus mechanism hypothesis, not proof of forced theory change
  reconstructionTarget: reader can distinguish observed result, hypothesis pressure, and later evidence
  overclaimRisk: "forced", "proved", "settled", and "therefore" make the relation too strong
  sourceReturnCondition: return to measurement record and evidence owner for truth claim
```

Before:

> The experiment failed, so the old theory collapsed.

After:

> The measurement contradicted the expected value under the old mechanism model. The narrative uses that mismatch as tension, but the evidence claim remains narrower: the result pressures the mechanism and opens alternatives; it does not by itself prove which replacement is right.

The after version is not less narrative. It is a better narrative because the reader can reconstruct the event support and return to source when the claim becomes load-bearing.

### Mature worked slice: franchise plot support

In a continuation-style storycraft probe, a scene says that a character betrays an ally "because the plot needs a darker turn." That is a narrative-function explanation, not source support. Repair it as source structure:

```text
NarrativeEventSupportRecord@CharacterTurn:
  eventOrMechanismClaim: character changes allegiance under named pressure
  sourceStructureRef: admitted canon constraint, prior motivation, current dilemma, consequence chain
  relationStrength: plausible character-agency hypothesis within private source pack
  reconstructionTarget: reader can state motive, pressure, action, consequence, and canon-return condition
  overclaimRisk: author need or theme is treated as character cause
  sourceReturnCondition: return to source pack and agency constraints
```

This repair blocks a common beginner and stale-practice failure: plot events occur because the writer wants them. [[NSTD/02_03_Source Mechanism, Event Model, and Coherence/00_NSTD.03 - Source Mechanism, Event Model, and Coherence|NSTD.3]] asks what event support the reader can reconstruct. If the answer is "the writer needed a twist", the event belongs to story-planning repair, not admitted narrative rendering.

### Calibration for relation support

| Value | Relation-support condition |
| --- | --- |
| `2` | Events are followable, but cause, dependency, motivation, proof, or evidence strength is inferred from wording. |
| `3` | Relation kinds are named, but reconstruction target or overclaim risk is weak. |
| `4` | Each load-bearing event or mechanism claim has source support, relation strength, reconstruction target, and source return. |
| `5` | The rendering survives perturbation: if wording, order, or viewpoint changes, readers still recover the same relation strength and know where stronger claims return. |

### FPF owner teaching

[[NSTD/02_03_Source Mechanism, Event Model, and Coherence/00_NSTD.03 - Source Mechanism, Event Model, and Coherence|NSTD.3]] is where narrative workers learn that "because" is not one relation. It may carry chronology, cause, mechanism, evidence, proof dependency, motivation, trade-off, or analogy. FPF already has owners for evidence, assurance, relation precision, and architecture structure. This DPF pattern teaches how those owners become visible when the publication expression is a story.

An architecture explanation tells why a modular split reduced coordination cost but increased interface exceptions. The narrative event is "the split happened"; the source mechanism is coupling, interface grammar, evidence-reuse loss, and residual repair. The story must let the reader reconstruct the architecture trade-off, not only the before-and-after drama.

A science story can say that an experimental result "forced" a revised hypothesis only if the source line supports that constraint. Often the honest relation is weaker: the result made one hypothesis less useful, exposed a tension, or suggested a new mechanism to test. [[NSTD/02_03_Source Mechanism, Event Model, and Coherence/00_NSTD.03 - Source Mechanism, Event Model, and Coherence|NSTD.3]] keeps the tension narratable while preventing the narrative from closing evidence that the source left open.

A live match commentary says "the press is breaking down because the midfield line is late." The source event may support late midfield movement and lost possession; the causal claim may be provisional. The support record separates observed event, tactical interpretation, uncertainty, and later source return to recording or telemetry.

In a homotopy explanation, a deformation story may help learners track invariance, but it is not a proof by itself. The support record says which formal relation the story illustrates, what the learner should reconstruct, and where analogy must return to definitions or proof-status boundaries.

Use rewrite diagnostics when a sentence sounds good but may overclaim.

| Initial sentence | Source-support question | Safer narrative repair |
| --- | --- | --- |
| "The failed experiment revealed the true mechanism." | Did the source establish the mechanism or only expose a tension? | "The failed experiment exposed a tension that made this mechanism worth testing." |
| "The module split solved coordination." | Did it solve, reduce, move, or trade off coordination cost? | "The split reduced one coordination path and introduced interface exceptions." |
| "The character had no choice." | Is necessity supported by canon, causal constraint, or only dramatic pressure? | "The route presents the action as constrained by these canon and causal conditions." |
| "The proof idea is that loops remember holes." | Is this an analogy, definition, theorem, or proof step? | "The image helps track the invariant; the formal statement returns here." |
| "The team was outplayed because the press failed." | Is this observed cause, provisional interpretation, or later analysis? | "The live reading treats the late press as a provisional explanation to check against telemetry." |

If the repair makes the narrative less exciting, that is not automatically a defect. The repair preserves the source relation. Engagement can be rebuilt later through [[NSTD/04_05_Engagement, Attention, and Motivation/00_NSTD.05 - Engagement, Attention, and Motivation|NSTD.5]] around the safer relation instead of by restoring the overclaim.

Minimum support-record sketches:

```text
NarrativeEventMechanismSupport@ArchitectureTradeoff:
  sourceStructureKind: architecture-like and mechanism-like trade-off
  requiredReaderReconstruction: why the split reduces one coordination path while creating interface exceptions
  eventOrMechanismModel: selected modular split changes dependency paths and exception-handling burden
  dependencyOrConstraintRefs: coupling refs; interface grammar refs; residual repair refs
  causalUseOwnerRef: architecture or evidence owner when causal strength is claimed
  uncertaintyOrUnknownRefs: telemetry not yet collected; candidate alternatives omitted
  reconstructionTaskRefs: reader names trade-off and residual exception
  sourceReturnCondition: architecture description and decision record for reliance
```

```text
NarrativeEventMechanismSupport@HomotopyAnalogy:
  sourceStructureKind: proof-like and definition-like dependency
  requiredReaderReconstruction: distinguish intuitive deformation image from formal equivalence relation
  eventOrMechanismModel: path deformation story used as analogy for invariant tracking
  dependencyOrConstraintRefs: formal definitions; examples; counterexamples; theorem prerequisites
  causalUseOwnerRef: none unless a causal learning claim is made
  uncertaintyOrUnknownRefs: analogy may fail outside named examples
  reconstructionTaskRefs: learner states where analogy stops and where proof returns
  sourceReturnCondition: formal source statement for proof or exercise use
```

```text
NarrativeEventMechanismSupport@LiveCommentary:
  sourceStructureKind: live event stream with provisional interpretations
  requiredReaderReconstruction: observed event vs inference vs prediction vs official correction
  eventOrMechanismModel: state updates and tactical hypothesis under uncertainty
  participatingHolonOrRoleRefs: teams, players, officials, broadcast or event source roles when needed
  uncertaintyOrUnknownRefs: off-camera events; later telemetry; official review
  reconstructionTaskRefs: listener can say what was observed and what was inferred
  sourceReturnCondition: official record, recording, statistics, or telemetry
```

These sketches are not mandatory formats. They teach the level of detail needed before coherence becomes reviewable. The record can be shorter in low-risk cases, but it must still state source-structure kind, reconstruction target, relation strength, uncertainty, and source return.

## [[NSTD/02_03_Source Mechanism, Event Model, and Coherence/00_NSTD.03 - Source Mechanism, Event Model, and Coherence|NSTD.3]]:6 - Bias-Annotation

This pattern blocks fluent-coherence drift: smooth event language is mistaken for a mechanism, dependency, architecture, proof, or causal model. The bias appears when readers can retell the story but cannot reconstruct the selected source relation. Repair by naming the source-structure kind, the reconstruction target, the owner for causal or dependency claims, and the source-return condition. Scope: DPF-local for narrative coherence over selected source structure; it does not certify mechanism truth or causal evidence.

## [[NSTD/02_03_Source Mechanism, Event Model, and Coherence/00_NSTD.03 - Source Mechanism, Event Model, and Coherence|NSTD.3]]:7 - Conformance Checklist

| Check | Passing condition |
| --- | --- |
| `CC-NSTD3-1` | Source structure kind is named and not forced into event form when inappropriate. |
| `CC-NSTD3-2` | Reader reconstruction target is explicit. |
| `CC-NSTD3-3` | Causal, dependency, constraint, goal, obstacle, hierarchy, prediction, and update relations are routed to their owners when claim-bearing. |
| `CC-NSTD3-4` | Unknown, contested, or deferred source relations are visible. |
| `CC-NSTD3-5` | Teaching or reliance-facing use includes reconstruction tasks or source-return points. |

## [[NSTD/02_03_Source Mechanism, Event Model, and Coherence/00_NSTD.03 - Source Mechanism, Event Model, and Coherence|NSTD.3]]:8 - Common Anti-Patterns and How to Avoid Them

| Anti-pattern | What fails | Repair |
| --- | --- | --- |
| Fluent mechanism fiction | The passage reads well but cannot be reconstructed. | Add event or mechanism support fields and reconstruction task. |
| Causal overrun | Narrative causality exceeds supported causal-use claims. | Route to `C.28` or lower the claim to dependency or temporal sequence. |
| Event forcing | A graph, proof dependency, or architecture view is converted into fake events. | Name source structure kind and choose a better ordering rule through [[NSTD/01_02_Structure-to-Sequence Ordering/00_NSTD.02 - Structure-to-Sequence Ordering]]. |

## [[NSTD/02_03_Source Mechanism, Event Model, and Coherence/00_NSTD.03 - Source Mechanism, Event Model, and Coherence|NSTD.3]]:9 - Consequences

The benefit is that narrative coherence becomes testable. The cost is that some dramatic simplifications must be weakened or paired with source return.

## [[NSTD/02_03_Source Mechanism, Event Model, and Coherence/00_NSTD.03 - Source Mechanism, Event Model, and Coherence|NSTD.3]]:10 - Rationale

Narrative comprehension often depends on event models and causal schemas. FPF uses that strength but keeps event support distinct from causal evidence, mechanism truth, architecture evaluation, and proof status.

## [[NSTD/02_03_Source Mechanism, Event Model, and Coherence/00_NSTD.03 - Source Mechanism, Event Model, and Coherence|NSTD.3]]:11 - SoTA-Echoing

Tan T. Nguyen's "A Review of Mechanistic Models of Event Comprehension" supplies the event-comprehension pressure: readers build event, hierarchy, prediction, updating, and causal-like models. Hoffmann's "The Tensions of Scientific Storytelling" shows scientific narratives can organize mechanisms and unresolved theory and experiment tension without proving them. Gatt and Krahmer's `Survey of the State of the Art in Natural Language Generation` keeps content selection separate from wording realization. The DPF adapts these lines by making source-structure kind and reconstruction target explicit.

Operational payload:

- From event-comprehension work, assume readers will build event, causal-like, hierarchical, and prediction or update models even when the source is weaker. [[NSTD/02_03_Source Mechanism, Event Model, and Coherence/00_NSTD.03 - Source Mechanism, Event Model, and Coherence|NSTD.3]] therefore asks what model the reader is allowed to build.
- From scientific storytelling, unresolved tension is narratively useful. It must stay unresolved when the source is unresolved. A good story may preserve tension rather than close it.
- From NLG, a generated or edited realization can make a relation sound coherent even when content selection was wrong. [[NSTD/02_03_Source Mechanism, Event Model, and Coherence/00_NSTD.03 - Source Mechanism, Event Model, and Coherence|NSTD.3]] therefore reviews source-support rows, not only wording coherence.
- From FPF evidence and assurance owners, coherence is not evidence. If the narrative says "shows", "proves", "forces", or "because", the relation strength must be routed to the owner that can carry it.
- From architecture work, a mechanism-like story about structure must keep trade-offs, residual exceptions, and telemetry distinct. A before-and-after story is not by itself an architecture evaluation.

The practical consequence is that narrative coherence is a reconstruction promise. If the reader cannot reconstruct the source relation and its uncertainty boundary, smooth prose is a liability.

## [[NSTD/02_03_Source Mechanism, Event Model, and Coherence/00_NSTD.03 - Source Mechanism, Event Model, and Coherence|NSTD.3]]:12 - Relations

Uses `A.6.3.NAR`, [[NSTD/01_02_Structure-to-Sequence Ordering/00_NSTD.02 - Structure-to-Sequence Ordering|NSTD.2]], `C.28`, `A.10`, `B.3`, `C.33` for architecture-relevant structural-information capture or loss, `C.34`, [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]], and `G.11`. Non-architecture mechanism-support recovery feeds [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] epiplexity and event-mechanism values. Reopen when the source mechanism, causal support, reconstruction target, or evaluation result changes. Support-map entry: open `Architecture and Narrative Work Bridge` when event, mechanism, dependency, or coherence support is architecture-relevant; open `Source Use And Refresh Map` when a source or cognition claim supports reconstructability; open `DPF Precision Restoration And Owner Map` when event, mechanism, coherence, support, or cause language starts doing evidence or quality work.

## [[NSTD/02_03_Source Mechanism, Event Model, and Coherence/00_NSTD.03 - Source Mechanism, Event Model, and Coherence|NSTD.3]]:End
