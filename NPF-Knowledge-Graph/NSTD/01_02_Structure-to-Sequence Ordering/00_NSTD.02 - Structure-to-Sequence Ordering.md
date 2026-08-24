---
type: "npf-pattern"
context:
  - "NPF"
page_type: "npf-pattern"
mode: "canonical-generated"
npf_id: "NSTD.2"
title: "Structure-to-Sequence Ordering"
part: "[[00_Hubs/NPF - Preface - Cross-Cutting Ideas And Principles]]"
parents:
  - "[[00_Hubs/NPF - Preface - Cross-Cutting Ideas And Principles]]"
source_file: "Narrativization-and-Narrative-Studies-Principles-Framework.md"
source_revision: "d77339d7056433de3ee55ad863860ee4b3006f6f"
source_sha256: "80f2d5ec3524b7947a3c36928bf774f61a9c68d4efc9ec5fc0d23206f01534e4"
generated_on: "2026-08-24"
source_lines:
  - 482
  - 714
status: "generated"
generated: true
---


> **Type:** DPF pattern body

> **Primary EntityOfConcern:** `NarrativeOrderingRule@Context`, a DPF-local relation slot set for one narrative rendering.

## [[NSTD/01_02_Structure-to-Sequence Ordering/00_NSTD.02 - Structure-to-Sequence Ordering|NSTD.2]]:1 - Problem frame

Use this pattern when a graph, mechanism, evidence set, architecture structure, candidate set, mathematical dependency structure, canon structure, or source tradition must be put into a sequence and the sequence changes what readers can recover.

First useful move: name the ordering rule, the source relations it preserves, the source relations it foregrounds, the source relations it coarsens or loses, and the source-return condition.

What goes wrong if missed: the order feels natural, but readers silently infer a different order kind: chronology, proof, causality, importance, decision order, work order, or moral priority.

What this buys: sequence becomes an explicit rendering choice rather than hidden ontology.

## [[NSTD/01_02_Structure-to-Sequence Ordering/00_NSTD.02 - Structure-to-Sequence Ordering|NSTD.2]]:2 - Problem

Narrative is sequential. Many source structures are not. Trees, graphs, mechanism diagrams, dependency sets, option sets, proof dependencies, and architecture views must be traversed. A chosen order preserves some relations and hides others. If the ordering rule is implicit, a fluent sequence can misrepresent the selected source structure.

## [[NSTD/01_02_Structure-to-Sequence Ordering/00_NSTD.02 - Structure-to-Sequence Ordering|NSTD.2]]:3 - Forces

| Force | Tension |
| --- | --- |
| Legibility vs structural fidelity | Linear order helps reading but cannot preserve every relation. |
| Teaching order vs source order | A good learning route may violate publication order or proof order. |
| Dramatic tension vs dependency truth | Suspense and reveal can hide prerequisites. |
| Compactness vs source return | The sequence needs to move, but hidden relations need return points. |

## [[NSTD/01_02_Structure-to-Sequence Ordering/00_NSTD.02 - Structure-to-Sequence Ordering|NSTD.2]]:4 - Solution

Declare the ordering rule before treating the narrative rendering as good enough for declared use.

```text
NarrativeOrderingRule@Context:
  narrativeRenderingRef:
  sourceStructureRefs:
  unfoldingStructureRef?:
  demonstrativeSliceRef?:
  orderingRuleKind:
  orderRationale:
  preservedSourceRelations:
  foregroundedSourceRelations:
  coarsenedOrLostSourceRelations:
  sourceReturnCondition:
  neighboringGoverningPatternRefs:
```

Admissible ordering-rule kinds include chronology, causality, dependency, discovery, didactic prerequisite, tension, traversal, viewpoint, publication, decision memory, and declared local rule. The name is not enough; the record must say what the rule preserves and loses.

Choose the rule through a four-question ordering test.

| Test | Ask | If unclear |
| --- | --- | --- |
| Source topology | Is the source primarily chain, graph, hierarchy, cycle, option set, event stream, proof dependency, architecture view, or canon field? | Return to [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose]]; selected source structure is not ready for sequencing. |
| Reader traversal | What path should the reader take first for the declared use: prerequisite, tension, discovery, causal, chronological, decision, viewpoint, or recap? | State two candidate rules and choose by reader-use effect, not by author taste. |
| Loss account | Which source relations become hidden or weaker under this order? | Add coarsened or lost relations and a source-return point before drafting. |
| Misread risk | What wrong order will readers infer if the rule is not stated? | Add a sentence or marker that blocks that inference. |

The ordering rule can be mixed, but only if the mixture is explicit. A teaching route may start with didactic prerequisites, use one discovery story to motivate a distinction, then return to formal dependency order. A live commentary may use chronological order for observations and causal order in a later recap. A franchise continuation may use reveal order for suspense while preserving an underlying causal or continuity order. The mixed rule must state where each order applies and what it must not imply.

When the selected source structure is a constraint-governed unfolding structure, the narrative order is a traversal or demonstration slice over that structure. The ordering rule must name the selected unfolding structure, the demonstrative slice used for reader orientation, the preserved constraints and invariants, and the branches, alternatives, loops, direct exits, or stop conditions hidden by the slice. The sequence in the narrative is not the whole unfolding structure and not a work order.

Use this repair table when the narrative feels coherent but readers reconstruct the wrong structure.

| Symptom | Likely hidden order | Repair |
| --- | --- | --- |
| Readers think the first-mentioned cause is the strongest cause. | Salience order mistaken for causal order. | Mark salience as viewpoint or teaching order; return causal-strength claims to the evidence or source governing pattern. |
| Learners can retell the lesson but fail formal exercises. | Didactic story order mistaken for proof order. | Add proof-return checkpoints and separate example order from theorem dependency. |
| Stakeholders think a narrative of architecture choices is the project decision sequence. | Explanation order mistaken for decision or work order. | Route decision claims to the architecture-decision governing pattern and name the explanatory order. |
| Fans like a reveal but continuity breaks. | Reveal order hides source canon constraints. | Add source-pack return and causal and continuity support before dramatic reveal. |
| A generated story has plausible steps but no preserved source graph. | Generator realization order mistaken for selected source structure. | Return to [[NSTD/06_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning]]; recover source plan and selected structure before evaluation. |

Do not evaluate the sequence by elegance first. A beautiful order that hides a critical dependency is below floor for declared use. Evaluate it through [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] only after the rule, preserved relations, foregrounded relations, lost relations, and source-return condition are in the record.

## [[NSTD/01_02_Structure-to-Sequence Ordering/00_NSTD.02 - Structure-to-Sequence Ordering|NSTD.2]]:5 - Archetypal Grounding

### Mature worked slice: graph-to-sequence serialization without source loss

Use this case when the source is not already a line. A knowledge graph about a domain has concepts, dependencies, counterexamples, evidence links, and practice routes. A narrative rendering must choose a traversal. If the traversal is not named, the reader may treat the story order as ontology, proof order, or historical order.

```text
NarrativeOrderingRule@HomotopyIntro:
  narrativeRenderingRef: HomotopyIntroNarrative@v1
  sourceStructureRefs:
    - topological space
    - path
    - deformation under constraints
    - invariant
    - example and counterexample
    - proof-status boundary
  orderingRuleKind: didactic prerequisite plus analogy-first cue
  orderRationale: learner needs visual intuition before formal return, but formal dependency must remain recoverable
  preservedSourceRelations: prerequisite relation; analogy-to-definition return; example-to-counterexample contrast
  foregroundedSourceRelations: deformation intuition and invariant question
  coarsenedOrLostSourceRelations: full proof order; advanced generality; categorical reformulation
  sourceReturnCondition: any claim about theorem, equivalence, or proof returns to formal statement and proof owner
  neighboringOwnerRefs: `A.6.3.CSC`, `E.17.EFP`, `A.10`, [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]]
```

This is a serialization decision with narrative consequences. The route can begin with a picture-like story about deforming paths, but the story must mark where analogy stops. A mature narrative might say, in ordinary prose, "The picture is a guide to the relation, not the definition; the formal boundary returns in the next step." That line is not decoration. It prevents the selected order from becoming false ontology.

### Before and after repair: architecture order

Before:

> We tried several designs and eventually found the architecture that solved the coordination problem.

Failure: chronology and success wording hide candidate selection, trade-off, decision authority, and realized-structure uncertainty. The reader may infer that the final candidate is proven, implemented, and telemetry-confirmed.

After:

> This explanation follows decision-memory order. First it states the coordination problem, then the candidate splits considered, then the selected trade-off and the residual interface exceptions. It does not give implementation order or proof that the realized structure already has the expected characteristics. For authority, return to the architecture decision record; for actual structure, return to telemetry after implementation.

What changed: the ordering rule became explicit, preserved relations are named, lost relations are named, and source-return is recoverable. [[NSTD/01_02_Structure-to-Sequence Ordering/00_NSTD.02 - Structure-to-Sequence Ordering|NSTD.2]] did not make the narrative longer for its own sake. It made the sequence truthful.

### Before and after repair: live commentary

Before:

> The midfield is late, so the press has failed, and that is why the match is turning.

Failure: live chronological observation is mixed with causal explanation and outcome projection. The source at that moment may support late movement and lost possession, but not a settled causal account.

After:

> In live order, the midfield line arrives late and the press opens space. Treat that causal reading as provisional until the replay, event data, or post-match analysis confirms it. For now the narrative preserves observation, uncertainty, and listener orientation.

What changed: chronology, provisional causality, and later source return are separated. This is the same FPF move as separating evidence, interpretation, and assurance, but in narrative-order vocabulary.

### Calibration for ordering values

| Value | Ordering condition |
| --- | --- |
| `2` | A readable sequence exists, but the ordering rule and lost relations are mostly hidden. |
| `3` | The ordering rule is named, but source-return and misread risks are weak. |
| `4` | The order preserves declared relations, states losses, and blocks the main wrong reconstruction for one use. |
| `5` | The order is replayable across at least two heterogeneous cases, with conflict between order layers explicitly handled and tested through [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation]]. |

### SoTA-to-action translation

Narratology often distinguishes source material, story, discourse, presentation, and focalization. [[NSTD/01_02_Structure-to-Sequence Ordering/00_NSTD.02 - Structure-to-Sequence Ordering|NSTD.2]] treats that as domain vocabulary and restores the FPF object before use: admit the source basis, select the source structure, choose the traversal or order, name what the order preserves and loses, then compose. NLG makes a similar split through content selection, document planning, microplanning, and realization. Fluent wording realization cannot repair a bad ordering rule.

A homotopy-theory explanation orders material by learner dependency: spaces, paths, homotopy, fundamental group, examples, proof-status boundaries. This is not the historical discovery order and not the formal proof order of a research monograph. The narrative must state that definitions and proof obligations remain in source-return formal statements.

An architecture narrative for a team may order structures by decision memory: first the coordination problem, then candidate splits, then chosen trade-off, then residual interface exceptions. That order is not the architecture structure itself and not the chronological order of implementation work. The preserved relations are coupling, cohesion, interface grammar, responsibility boundary, and expected trade-off. The lost relations may include low-level module detail and alternative candidates. Source return goes to architecture description, decision record, and telemetry if actual-structure feedback exists.

A franchise-continuation outline may order scenes by reveal and tension. That does not mean reveal order is causal order. The underlying causal and continuity order must still name premise constraint, character motivation, event cause, consequence, and canon-return point. If a later twist works only because a source constraint was hidden from the writer as well as from the reader, the order is not a legitimate reveal; it is a source-selection failure.

A scientific storytelling case may order experiments by tension: failed attempt, surprising measurement, revised hypothesis, unresolved conflict. That order can be useful because it mirrors inquiry, but it cannot make unresolved tension into evidence closure. The sequence must name which calculations, mechanisms, and experimental facts remain source-return points.

Worked repair sequence:

1. Initial symptom: "The team first tried A, then B, and finally discovered the right architecture."
2. Hidden-order diagnosis: chronology is being read as decision quality and finality.
3. Source topology repair: name candidate structures, quality characteristics, rejected alternatives, and telemetry or decision basis.
4. Ordering rule repair: call the narrative "decision-memory order", not proof, implementation order, or architecture structure.
5. Loss repair: state what the narrative omits, such as lower-level exceptions or candidates excluded for scope.
6. Source-return repair: link to architecture description, decision record, or candidate comparison when a reader needs authority.

Second worked repair sequence:

1. Initial symptom: "We introduce homotopy with loops, then groups, then examples, because that is the natural story."
2. Hidden-order diagnosis: "natural story" hides the didactic prerequisite order and may be mistaken for formal proof order.
3. Source topology repair: list definitions, examples, theorem prerequisites, proof-status boundaries, and formal-source returns.
4. Ordering rule repair: choose didactic dependency order and explicitly state where it diverges from formal order.
5. Loss repair: record which formal details are deferred and where they return.
6. Evaluation repair: [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] checks whether learners can reconstruct dependency and proof boundaries, not whether they enjoyed the story.

Case matrix for ordering work:

| Case | Candidate order | Preserves | Hides or weakens | Required source return |
| --- | --- | --- | --- | --- |
| FPF learning route | Didactic prerequisite order: entry condition, EoC, forces, solution, checks, exits, improvement. | Pattern-use route and learner build-up. | Monolith order, advanced variants, historical source evolution. | Source pattern body and relation records. |
| Homotopy explanation | Didactic dependency order with analogy before formal proof. | Learner accessibility and dependency sequence. | Full proof order, all lemmas, advanced generalization. | Formal statement, proof owner, example boundary. |
| Franchise continuation | Causal plot order plus reveal order. | Continuity, motivation, event consequence, source-pack return. | Exhaustive canon and publication rights. | Admitted canon refs and non-publication boundary. |
| Live commentary | Live chronological order plus provisional interpretation markers. | Event stream, uncertainty, listener orientation. | Later tactical recap, off-camera sources, official correction. | Official event record, telemetry, recording. |
| Architecture explanation | Decision-memory order or trade-off route. | Problem, candidate, selected trade-off, residual exception. | Implementation order, full structure, rejected-candidate detail. | Architecture description, candidate set, decision record, telemetry. |

Use the matrix as a pre-drafting design aid. The selected order should be visible before the narrative prose exists. If the matrix can only be filled after the text is written, the worker is reconstructing hidden choices and should mark the result as a repaired route, not as an originally controlled route.

When two orders conflict, preserve both as named layers. A learning route may teach prerequisites first and later show historical discovery. A mystery-like story may reveal effects before causes while keeping an internal causal order. A live recap may reorder events by causal explanation after first recording live chronology. The reader must be told which layer they are following.

## [[NSTD/01_02_Structure-to-Sequence Ordering/00_NSTD.02 - Structure-to-Sequence Ordering|NSTD.2]]:6 - Bias-Annotation

This pattern blocks natural-sequence drift: a chronological, didactic, dramatic, traversal, or slide order is treated as if it were the source structure itself. The bias is especially likely when the order feels intuitive to the author. Repair by naming the ordering rule, preserved relations, foregrounded relations, lost relations, and source-return condition. Scope: DPF-local for source-structure-to-sequence rendering; it does not govern general serialization formats or publication order.

## [[NSTD/01_02_Structure-to-Sequence Ordering/00_NSTD.02 - Structure-to-Sequence Ordering|NSTD.2]]:7 - Conformance Checklist

| Check | Passing condition |
| --- | --- |
| `CC-NSTD2-1` | Ordering rule and rationale are named. |
| `CC-NSTD2-2` | Preserved, foregrounded, and lost relations are explicit. |
| `CC-NSTD2-3` | Narrative order is not treated as physical time, proof order, work order, or decision authority without source support. |
| `CC-NSTD2-4` | Source-return condition is present when lost relations affect action or reliance. |
| `CC-NSTD2-5` | Preservation claims route to `C.34`; coarsening claims route to `A.6.3.CSC`, to `C.33` when architecture-relevant structural-information loss is current, or to [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation]] epiplexity when the loss question is non-architecture DPF evaluation. |

## [[NSTD/01_02_Structure-to-Sequence Ordering/00_NSTD.02 - Structure-to-Sequence Ordering|NSTD.2]]:8 - Common Anti-Patterns and How to Avoid Them

| Anti-pattern | What fails | Repair |
| --- | --- | --- |
| Natural-order assumption | The order is not named because it feels obvious. | Write the rule and one preserved or lost relation. |
| Tension as dependency | Reveal order is read as prerequisite order. | Split dramatic order from dependency order and add source return. |
| Slide order as source structure | A teaching sequence is treated as the corpus architecture. | Route the teaching publication carrier through [[NSTD/07_08_Learning-Route Narrative Rendering and Reconstruction Return/00_NSTD.08 - Learning-Route Narrative Rendering and Reconstruction Return]] and keep source structure separate. |

## [[NSTD/01_02_Structure-to-Sequence Ordering/00_NSTD.02 - Structure-to-Sequence Ordering|NSTD.2]]:9 - Consequences

The benefit is that a narrative path can be optimized for comprehension without pretending to preserve all source relations. The cost is explicit loss accounting.

## [[NSTD/01_02_Structure-to-Sequence Ordering/00_NSTD.02 - Structure-to-Sequence Ordering|NSTD.2]]:10 - Rationale

Narrative sequence is a transformation over structure. Making the ordering rule explicit preserves the useful similarity between serialization and narrativization: both choose an order for a structure, both preserve and lose relations, and both need a return path when the order is relied on.

## [[NSTD/01_02_Structure-to-Sequence Ordering/00_NSTD.02 - Structure-to-Sequence Ordering|NSTD.2]]:11 - SoTA-Echoing

Schmid's `Narratology: An Introduction` supplies the source-material, story, narrative, and presentation distinction as narratology vocabulary; Chihaia's `Introductions to Narratology: Theory, Practice and the Afterlife of Structuralism` keeps the DPF from treating one narratology tradition as the whole domain; Gatt and Krahmer's `Survey of the State of the Art in Natural Language Generation` makes content selection and realization separable; Cardona-Rivera and Ware et al.'s "The Story So Far on Narrative Planning" makes planned event and plot structure visible before wording. The DPF adopts that ordering discipline only after restoring admitted source basis, selected source structure, and FPF owner routes.

Operational payload:

- From Schmid, use selection, composition, and linearization as separate duties. A route may admit source basis and select source structure correctly but still linearize it badly. [[NSTD/01_02_Structure-to-Sequence Ordering/00_NSTD.02 - Structure-to-Sequence Ordering|NSTD.2]] therefore evaluates ordering independently from [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose|NSTD.1]] selection.
- From Chihaia, do not assume one narratology school's order terms are universal. If a term such as plot, discourse, fabula, perspective, or presentation is used, it must be translated into the local ordering rule and FPF owner terms.
- From NLG, content planning and realization are distinct. A generated or human-written text can realize fluent sentences while hiding the content plan. [[NSTD/01_02_Structure-to-Sequence Ordering/00_NSTD.02 - Structure-to-Sequence Ordering|NSTD.2]] asks for the plan before style.
- From narrative planning, plot order and event order may diverge. This is useful in storycraft and explanation, but the divergence must be recorded so readers do not infer false causality or dependency.
- From FPF architecture patterns, views and viewpoints are not free perspectives. When the narrative order traverses architecture-relevant structures, `C.30.ASV`, `C.33`, `C.34`, and architecture decision owners may become live.

The practical consequence is that "good order" is never a free aesthetic judgment. It is an ordering rule plus preserved relations, lost relations, and source return for one declared use.

## [[NSTD/01_02_Structure-to-Sequence Ordering/00_NSTD.02 - Structure-to-Sequence Ordering|NSTD.2]]:12 - Relations

Uses `A.6.3.NAR`, `A.6.3.CSC`, `C.33` for architecture-relevant structural-information capture or loss, `C.34`, `E.17`, `E.17.EFP`, `A.16.2` when a route must back off or respecify after overcommitment, `A.6.P` when ordering rationale hides relation-kind claims, [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]], and `G.11`. Non-architecture capture and loss questions feed the DPF-local epiplexity basis in [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]]. Reopen when source structure, reader use, ordering rule, source-return condition, route authority, relation precision, or low [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] ordering value changes. Support-map entry: open `Architecture and Narrative Work Bridge` when sequence is over architecture views, candidate structures, descriptions, correspondence, or actual-structure feedback; open `Semiotic And Language-Precision Bridge` or `DPF Precision Restoration And Owner Map` when ordering terms hide coarsening, relation-kind, or quality claims.

## [[NSTD/01_02_Structure-to-Sequence Ordering/00_NSTD.02 - Structure-to-Sequence Ordering|NSTD.2]]:End
