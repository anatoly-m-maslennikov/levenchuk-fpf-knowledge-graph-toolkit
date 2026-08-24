---
type: "npf-pattern"
context:
  - "NPF"
page_type: "npf-pattern"
mode: "canonical-generated"
npf_id: "NSTD.1"
title: "Source-Structure Intake and Narrative Purpose"
part: "[[00_Hubs/NPF - Preface - Cross-Cutting Ideas And Principles]]"
parents:
  - "[[00_Hubs/NPF - Preface - Cross-Cutting Ideas And Principles]]"
source_file: "Narrativization-and-Narrative-Studies-Principles-Framework.md"
source_revision: "d77339d7056433de3ee55ad863860ee4b3006f6f"
source_sha256: "80f2d5ec3524b7947a3c36928bf774f61a9c68d4efc9ec5fc0d23206f01534e4"
generated_on: "2026-08-24"
source_lines:
  - 167
  - 481
status: "generated"
generated: true
---


> **Type:** DPF pattern body

> **Primary EntityOfConcern:** `NarrativePurposeIntake@Context`, a DPF-local relation record for one narrative rendering case.

## [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose|NSTD.1]]:1 - Problem frame

Use this pattern when a writer, narrator, teacher, architect, researcher, commentator, story designer, or tool starts with a message, lesson, theme, persuasive effect, desired memory, live commentary line, or future scenario before naming the source structures that must survive the narrative rendering.

First useful move: write `NarrativePurposeIntake@Context` with admitted source basis refs, selected source structures, source-structure selection rationale, source temporal posture, rendering mediation mode, narrating or rendering worker, reader-interest or use hypothesis, intended reader or listener role and use, narrative purpose, blocked purpose overread, source-return owner, and any ethics or assurance owner.

What goes wrong if missed: purpose absorbs admitted source basis and selected source structure. The narrative may become memorable, but readers cannot recover which structure was selected, which uncertainty was retained, or which claims need source return.

What this buys: the writer can choose a narrative aim without letting that aim widen evidence, assurance, ethics, policy, or work authority.

Not this pattern when the issue is only publication face, source-pack admission, evidence sufficiency, or ethics mediation. Use the direct owner and return here only when narrative purpose must be tied to selected source structure.

## [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose|NSTD.1]]:2 - Problem

Narrative purpose is useful because a narrative rendering is made for someone and for some use. But ordinary purpose language is often too broad: "make it inspiring", "tell the story", "explain the architecture", "make learners care". Those phrases do not say which structures must be preserved, which distinctions may be coarsened, and which downstream use is blocked.

## [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose|NSTD.1]]:3 - Forces

| Force | Tension |
| --- | --- |
| Reader usefulness vs source discipline | A narrative needs a purpose, but the purpose cannot replace selected source structures. |
| Motivation vs authority | Motivation helps attention, but it does not create evidence, assurance, ethics clearance, or work permission. |
| Domain vocabulary vs FPF owners | Narratology and communication terms help design, but source-use, evidence, ethics, and assurance claims have FPF owners. |
| Writing speed vs replayability | Fast writing starts from message; replayable writing starts from source structure and use. |

## [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose|NSTD.1]]:4 - Solution

Create one intake record before drafting or evaluating the narrative.

```text
NarrativePurposeIntake@Context:
  sourceBasisRefs:
  selectedSourceStructureRefs:
  unfoldingStructureRefs?:
  demonstrativeSliceRefs?:
  sourceStructureSelectionRationale:
  sourceTemporalPosture:
  renderingMediationMode: direct-source-structure | architecture-mediated | mixed
  architectureMediationRef?:
  sourceStructureOwnerRef?:
  narratingOrRenderingWorkerRef?:
  readerOrListenerRoleRefs:
  readerInterestOrUseHypothesis:
  intendedReaderOrListenerUse:
  narrativePurpose:
  blockedPurposeOverread:
  sourceReturnOwner:
  ethicsOrAssuranceOwner?:
  refreshCondition?:
```

Use `unfoldingStructureRefs?` only when one selected source structure is governed as a constraint-governed unfolding structure by `A.22.CGUS`, `E.18.3`, or a local FPF block. Use `demonstrativeSliceRefs?` only for the slice the narrative renders for the reader; the slice is not the whole selected structure.

Then apply these moves:

1. Name admitted source basis refs, selected source structures, source-structure selection rationale, and source temporal posture.
2. Name the rendering mediation mode and any architecture mediation, source-structure owner, or telemetry source that remains live.
3. Name the narrating or rendering worker, reader-interest or use hypothesis, and intended reader or listener role and use in project terms.
4. State the narrative purpose as a relation to the selected source structures and reader or listener use.
5. State what the purpose may not justify: evidence, assurance, policy, work, ethics, or decision use.
6. Name the source-return owner and any neighboring FPF owner.

Use the intake in four passes, not as one form-filling gesture.

| Pass | Question | Output |
| --- | --- | --- |
| Source pass | What admitted source basis or source pack is being rendered, and which selected source structures must remain recoverable for the declared use? | Source-basis refs or source-pack refs, selected source structure refs, and source-return condition. |
| Use pass | Who will use the narrative, for what work or understanding, and what must they be able to recover or decide not to decide? | Reader or listener role, reader-interest hypothesis, intended use, and non-use boundary. |
| Mediation pass | Is the work direct source-structure rendering, architecture-mediated rendering, or mixed? What temporal posture changes source obligations? | Rendering mediation mode, temporal posture, architecture mediation refs, and live telemetry or source-return refs. |
| Authority pass | Which claims are tempting but not granted by the narrative purpose? | Blocked purpose overread plus evidence, assurance, ethics, policy, work, and decision owner exits. |

The intake is good enough to compose only when the selected source structures can be stated without looking at the current prose version. If the only answer is "the important bits are the bits I happened to write about", selection is still hidden. Return to the admitted source basis, name candidate structures, and choose by reader use. If the reader use is also vague, stop at an orientation cue or source-pack note; do not present the carrier-borne content as an admitted narrative rendering.

Use contrast cases before drafting:

- Admissible: "This route helps new FPF readers reconstruct why `EntityOfConcern`, forces, and neighboring-pattern exits matter during pattern use." The selected structures are named and the use is reconstructive.
- Below floor: "Make the seminar inspiring so people like FPF." Motivation is a possible engagement device, but source structures and reconstruction use are missing.
- Wrong owner: "Use the narrative to prove FPF is correct." That is evidence or assurance work, not narrative-purpose work.

For prospective or fictional material, the selected source structure may come from a constrained source pack rather than from already-realized facts. The intake must still name the canon references, scenario assumptions, design constraints, or future-state hypotheses admitted for the case. "The story world wants it" is not a source-structure selection rationale; the worker must state which admitted source-pack constraints make the narrative route legitimate for private planning, teaching, or scenario exploration.

When `selectedSourceStructureRefs` includes a constraint-governed unfolding structure, name the Core governing pattern and the selected structure ref before purpose is finalized. The selected structure may be `ConstraintGovernedUnfoldingStructure@Context`, an `E.18.3` transformation-flow unfolding structure, a P2S local block, an improvement-loop block, or a narrative-ordering block under `A.6.3.NAR`. The narrative purpose may choose one `DemonstrativeUnfoldingSlice@Context` for reader use, but it must state what branches, alternatives, loops, constraints, admissible next forms, and direct exits are preserved or lost. The slice is not the whole selected structure and not a work order.

Use role-specific intake prompts when the worker is stuck.

| Worker situation | Prompt | Expected answer |
| --- | --- | --- |
| Teacher or trainer | "After the narrative, what should learners reconstruct from source without relying on my story?" | Source spine, reconstruction task, and source-return condition. |
| Architect or analyst | "Which structure, trade-off, candidate, telemetry, or decision memory must survive the narrative?" | Architecture or source-structure refs plus rendering mediation mode. |
| Scientist or researcher | "Which mechanism, calculation, failed attempt, source uncertainty, or unresolved tension is being rendered?" | Mechanism or event support, uncertainty, evidence owner, and source return. |
| Story designer | "Which canon, premise, agency, continuity, or causal plot constraint governs this route?" | Bounded source pack and non-publication boundary when needed. |
| Live commentator | "Which observation, inference, prediction, and later official source must stay distinguishable?" | Temporal posture, uncertainty markers, and refresh condition. |
| Tool builder | "Which part is admitted source basis, which part is method, which part is generated carrier, and who admits it?" | Split between admitted source basis, method, generated carrier, and admission owner; generated-carrier admission route; human responsibility. |

If the answer names only mood, audience reaction, style, genre, or desired conclusion, the intake is not ready. Those can be legitimate later choices under [[NSTD/03_04_Voice, Focalization, and Agency/00_NSTD.04 - Voice, Focalization, and Agency|NSTD.4]], [[NSTD/04_05_Engagement, Attention, and Motivation/00_NSTD.05 - Engagement, Attention, and Motivation|NSTD.5]], `C.2.LS`, or `E.17`, but they cannot select the source structure by themselves.

Minimum worked intake cases:

```text
NarrativePurposeIntake@FPFLearningRoute:
  sourceBasisRefs: selected FPF pattern bodies and relation records
  selectedSourceStructureRefs: EntityOfConcern discipline; problem frame; forces; solution; neighboring exits; quality and improvement loop
  unfoldingStructureRefs: A.22.CGUS only when the lesson explicitly teaches source-to-next-use unfolding
  demonstrativeSliceRefs: first seminar route through selected pattern-use positions
  sourceStructureSelectionRationale: learners must reconstruct how a practitioner chooses and uses a pattern
  sourceTemporalPosture: prospective planned learning route over current source corpus
  renderingMediationMode: direct-source-structure unless architecture-of-FPF explanation is opened
  narratingOrRenderingWorkerRef: teacher or course designer
  readerOrListenerRoleRefs: new FPF author or reviewer
  readerInterestOrUseHypothesis: learner needs usable entry, not complete monolith memory
  intendedReaderOrListenerUse: reconstruct one pattern-use route and apply it to a new case
  narrativePurpose: orient attention and sequence learning tasks around source-returnable pattern use
  blockedPurposeOverread: lesson is not evidence that FPF is correct and not replacement for pattern bodies
  sourceReturnOwner: FPF source patterns and teaching publication-carrier relation
  refreshCondition: FPF edition, learner telemetry, or route evaluation changes
```

```text
NarrativePurposeIntake@HomotopyExplanation:
  sourceBasisRefs: formal definitions, examples, diagrams, proof-status notes, and selected textbook or lecture source basis
  selectedSourceStructureRefs: definition dependency; example and counterexample relation; theorem prerequisite; formal-source return
  sourceStructureSelectionRationale: learner needs an intuitive route that preserves formal boundaries
  sourceTemporalPosture: retrospective or atemporal explanation over existing mathematical material
  renderingMediationMode: direct-source-structure unless a teaching architecture is explicitly used
  narratingOrRenderingWorkerRef: teacher, explainer, or tool-assisted author
  readerOrListenerRoleRefs: learner who must later distinguish intuition from proof
  readerInterestOrUseHypothesis: learner needs recoverable dependency order and analogy boundary
  intendedReaderOrListenerUse: use examples and return to formal statements without treating metaphor as theorem
  narrativePurpose: make abstractions followable while preserving proof-status boundary
  blockedPurposeOverread: narrative does not prove the theorem, replace notation, or authorize informal equivalence
  sourceReturnOwner: mathematical source or proof owner
  refreshCondition: source correction, learner failure, or changed learning objective
```

```text
NarrativePurposeIntake@LiveCommentary:
  sourceBasisRefs: live observations, official event feed, telemetry, recording, later official result
  selectedSourceStructureRefs: event order; score state; possession or control changes; actor roles; uncertainty markers
  sourceStructureSelectionRationale: listener needs orientation during an unfolding event stream
  sourceTemporalPosture: live unfolding source with later refresh
  renderingMediationMode: direct-source-structure
  narratingOrRenderingWorkerRef: commentator or live analyst
  readerOrListenerRoleRefs: listener following the event and later checking the official event record
  readerInterestOrUseHypothesis: listener needs distinction between observation, inference, prediction, and official correction
  intendedReaderOrListenerUse: follow the event without treating provisional interpretation as fact
  narrativePurpose: maintain orientation and attention under uncertainty
  blockedPurposeOverread: commentary is not official evidence, blame assignment, or final tactical analysis
  sourceReturnOwner: event source owner, official record, recording, telemetry
  refreshCondition: official correction, telemetry, or post-event evidence changes
```

```text
NarrativePurposeIntake@FictionalContinuationProbe:
  sourceBasisRefs: admitted canon or local source pack for private storycraft test
  selectedSourceStructureRefs: canon constraints; continuity; premise and theme; character agency; causal plot support
  sourceStructureSelectionRationale: storycraft probe tests whether the DPF protects source constraints under dramatic pressure
  sourceTemporalPosture: prospective fictional source structure
  renderingMediationMode: direct-source-structure unless fictional organization or technology architecture is live
  narratingOrRenderingWorkerRef: story designer or tool-assisted writer
  readerOrListenerRoleRefs: private reviewer of storycraft plan
  readerInterestOrUseHypothesis: reviewer needs to see whether continuity and agency survive the route
  intendedReaderOrListenerUse: private design critique, not publication
  narrativePurpose: produce a source-returnable continuation route for testing
  blockedPurposeOverread: no authorization, no exhaustive canon authority, no publication permission
  sourceReturnOwner: source-pack and canon owner; rights and publication owner when those claims are made
  refreshCondition: source-pack correction, canon selection change, generated-carrier admission change
```

## [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose|NSTD.1]]:5 - Archetypal Grounding

### Mature worked slice: FPF seminar from source spine to admitted route

Start with a weak request: "Tell a motivating story about FPF so people want to use it." This is not yet a narrative purpose intake. The source structure is hidden, the reader use is vague, and motivation is being asked to carry adoption, evidence, and teaching value at once.

Repair it in the intake, not later in style.

```text
NarrativePurposeIntake@FPFSeminarOrientation:
  sourceBasisRefs: selected FPF pattern bodies and relation records
  selectedSourceStructureRefs:
    - EntityOfConcern discipline
    - Problem frame and forces
    - Solution as admissible move under conditions
    - neighboring-pattern exits
    - quality and improvement loop entry
  sourceStructureSelectionRationale: new practitioners fail when they treat patterns as recipes rather than condition-bound moves
  sourceTemporalPosture: prospective planned learning route over current FPF source corpus
  renderingMediationMode: direct-source-structure
  narratingOrRenderingWorkerRef: seminar author
  readerOrListenerRoleRefs: new FPF practitioner; team lead evaluating local adoption
  readerInterestOrUseHypothesis: reader wants a first usable route through FPF without learning every pattern first
  intendedReaderOrListenerUse: reconstruct one pattern-use route and choose the next governing pattern
  narrativePurpose: orient attention and motivation toward source-returnable pattern use
  blockedPurposeOverread: not proof that FPF is correct; not replacement for pattern bodies; not authority for a local project
  sourceReturnOwner: selected FPF pattern body and relation record
  ethicsOrAssuranceOwner: none unless the seminar makes assurance, policy, or affected-party claims
  refreshCondition: FPF edition or selected-source pattern changes; learner reconstruction test fails
```

Now the narrative worker can compose. The first paragraph may be memorable, but every memorable move has a source return. "A pattern is not a recipe" returns to source conditions, forces, and neighboring exits. "Start with the thing being changed" returns to `EntityOfConcern`. "Do not optimize the visible proxy indicator" returns to quality and proxy-risk owners. The seminar publication carrier can be engaging, but the intake prevents it from becoming a local mythology about FPF.

Evaluation through [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] later asks whether learners can rebuild the route: identify the source structure, say why the selected order was didactic, name what the story intentionally omitted, and return to the pattern body when they need authority. If learners only repeat the slogan "patterns are not recipes", [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose|NSTD.1]] did not select enough source structure for the declared use.

### Mature worked slice: architecture-mediated narrative

An architect wants a narrative explaining a system's future structure after candidate synthesis. Do not start with "tell the journey from chaos to architecture". Start by deciding whether the narrative is architecture-mediated. If it is, architecture work remains live before narrative work.

```text
NarrativePurposeIntake@ArchitectureDecisionStory:
  sourceBasisRefs: architecture candidate set, selected architecture description, decision record, expected characteristics, known residuals
  selectedSourceStructureRefs:
    - problem situation and forces
    - candidate structures considered
    - selected structure and rejected alternatives
    - expected architecture characteristics
    - residual exceptions and developer continuation boundary
    - telemetry or later actual-structure feedback condition
  sourceTemporalPosture: prospective future holon structure before implementation
  renderingMediationMode: architecture-mediated
  architectureMediationRef: architecture description and candidate synthesis records
  readerOrListenerRoleRefs: developer team; product steward; later evaluator
  intendedReaderOrListenerUse: understand what structure to preserve while implementing and what may be locally detailed
  narrativePurpose: carry structural intent and trade-off rationale into development work
  blockedPurposeOverread: not the architecture itself; not implementation order; not assurance that realized structure will match
  sourceReturnOwner: architecture description, architecture decision record, and future telemetry route
  refreshCondition: candidate set, selected architecture, decision, or actual-structure feedback changes
```

This case teaches the architecture bridge. The narrative worker is not exempt from architecture owners just because the output is prose. `C.33` is live for structural-information capture and loss; `C.34` is live if correspondence between described and realized structure matters; `E.17` is live if the carrier is published; architecture decision owners remain live for decision authority. [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose|NSTD.1]] only binds the narrative purpose to selected structures and reader use.

### Mature worked slice: franchise continuation probe

For a continuation-style storycraft probe using a well-known space-opera franchise such as `Star Wars`, the selected source is a bounded private source pack. The intake must state canon scope, character-agency constraints, continuity constraints, premise constraints, and non-publication boundary before any scene or plot move is accepted.

A bad intake says: "Write a surprising sequel that feels epic." A repaired intake says: "For private storycraft testing, render a continuation premise that preserves admitted canon constraints, character agency, causal consequence, and theme tension; block publication, rights, and authority claims." If a surprising turn works only because the source pack was ignored, the failure belongs to [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose|NSTD.1]] before [[NSTD/01_02_Structure-to-Sequence Ordering/00_NSTD.02 - Structure-to-Sequence Ordering|NSTD.2]] or [[NSTD/04_05_Engagement, Attention, and Motivation/00_NSTD.05 - Engagement, Attention, and Motivation|NSTD.5]] can repair it.

### Role-specific mature first moves

| Worker | First source-selection move | Common hidden overread | Repair before composing |
| --- | --- | --- | --- |
| Teacher | Name the source spine and reconstruction task. | Learner interest means learning occurred. | Add source-return question and later [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation]] row. |
| Architect | Name selected structures, candidates, residuals, and actual-structure feedback. | Explanatory story is the architecture decision. | Route decision authority to architecture decision owners. |
| Scientist | Name mechanism, calculation, uncertainty, and proof or evidence boundary. | Story coherence is evidence closure. | Add evidence owner and source-return condition. |
| Story designer | Name source pack, continuity, agency, and non-use boundary. | Dramatic surprise authorizes source violation. | Reopen source-pack selection before ordering. |
| Live commentator | Name event stream, provisional interpretation, and later official return. | Live causal claim is settled fact. | Mark uncertainty and telemetry return. |
| AI-agent operator | Name source plan, schema, admission owner, and evaluation route. | Fluent generated prose is an admitted rendering. | Send carrier to [[NSTD/06_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning]] and `C.35` before [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation]]. |

### What this pattern teaches about FPF

[[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose|NSTD.1]] is often the first place where a narrative worker learns why FPF separates admitted source basis, description, evidence, assurance, ethics, publication, and improvement. The pattern does not ask for more paperwork. It asks the worker to stop one very common collapse: "I have a purpose, therefore I know what the story should say." In FPF terms, a purpose is a relation to an `EntityOfConcern`, a role use, and selected source structures. It is not the admitted source basis, not the authority, and not the quality result.

An FPF seminar route wants learners to understand why pattern use is condition-based rather than recipe following. The selected source structures are `EntityOfConcern`, problem frame, forces, solution, consequences, and neighboring-pattern exits. The purpose is orientation for later reconstruction tasks. It is not permission to replace pattern bodies with seminar slogans. Source return points to the FPF patterns and the seminar publication carrier stays outside this DPF body.

A homotopy explanation starts differently. The admitted source basis is a mathematical corpus: definitions, examples, maps, equivalences, proof-status boundaries, and formal sources. The intended reader is not "any curious person"; it might be an undergraduate who must later distinguish intuitive pictures from formal definitions. The purpose can be "make paths, deformations, and invariants followable", but the blocked overread says that the narrative does not prove the theorem, replace formal notation, or license analogy as definition. The intake therefore protects formal return before any metaphor is selected.

A live football commentary has a live unfolding source posture. The commentator's purpose may be orientation and suspense, but the selected structures are event order, score state, possession changes, player actions, provisional interpretation, and later official source return. The intake blocks the overread that a dramatic prediction, blame cue, or emotional framing is evidence. If later official statistics contradict the live interpretation, the refresh condition is not optional.

A franchise-continuation storycraft test uses a prospective fictional source posture. The source structures are admitted canon constraints, continuity requirements, premise constraints, character-agency constraints, and non-publication boundary. The purpose may be private storycraft testing, not authorized sequel publication. The intake must state that publication rights, exhaustive canon authority, and moral permission are outside this DPF case.

## [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose|NSTD.1]]:6 - Bias-Annotation

This pattern blocks purpose-primacy drift: the message, theme, desired memory, or persuasion effect is allowed to choose source structures after the fact. Treating purpose as the source-selection owner collapses selected source structure, reader use, and authority boundary. Repair by reopening the intake, naming selected structures, and writing the blocked purpose overread before drafting or evaluating. Scope: DPF-local for narrative renderings; it does not govern all communication, evidence, assurance, or publication work.

## [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose|NSTD.1]]:7 - Conformance Checklist

| Check | Passing condition |
| --- | --- |
| `CC-NSTD1-1` | Admitted source basis and selected source structures are named before purpose is finalized. |
| `CC-NSTD1-2` | Source-structure selection rationale explains why these structures are needed for the reader or listener use. |
| `CC-NSTD1-3` | Source temporal posture and rendering mediation mode are explicit. |
| `CC-NSTD1-4` | Narrating or rendering worker, reader-interest or use hypothesis, and intended reader or listener role are named. |
| `CC-NSTD1-5` | Intended use is narrower than general persuasion, inspiration, or entertainment. |
| `CC-NSTD1-6` | Purpose states non-admissible downstream use. |
| `CC-NSTD1-7` | Evidence, assurance, ethics, policy, and work claims route to direct owners when made. |
| `CC-NSTD1-8` | Source-return owner and refresh condition are present when source currentness or hidden distinctions matter. |

## [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose|NSTD.1]]:8 - Common Anti-Patterns and How to Avoid Them

| Anti-pattern | What fails | Repair |
| --- | --- | --- |
| Message-first drafting | The theme chooses the structure after the fact. | Reopen intake and name selected source structures before drafting. |
| Tacit selection as craft | The worker or model foregrounds structures, but no rationale ties them to reader use. | Reconstruct the selection rationale and reader-interest hypothesis before evaluating or improving the narrative. |
| Motivation as truth support | A moving narrative is treated as stronger evidence. | Route evidence to `A.10` and keep motivation as reader-use support. |
| Purpose without blocked use | The same narrative is reused for decision, policy, or work. | Add blocked purpose overread and source-return condition. |

## [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose|NSTD.1]]:9 - Consequences

The benefit is early kind stability: admitted source basis, selected structure, narrative rendering, reader use, and authority boundaries stop competing. The cost is one small intake record before drafting.

## [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose|NSTD.1]]:10 - Rationale

Narrative design traditions often begin with audience and communicative aim. FPF keeps that value, but it binds aim to selected source structure. This avoids semio-bias: the narrative is a rendering relation over source structure, not a free-standing communication product.

## [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose|NSTD.1]]:11 - SoTA-Echoing

### Operational comparison against domain vocabulary

This DPF intentionally translates domain vocabulary into FPF owner work instead of importing it whole. When narratology says story, discourse, and presentation, this package asks: what source structure is selected, what order is chosen, what is foregrounded, and what source return remains? When cognitive narratology says event model, transportation, perspective, or memory, this package asks: which reconstruction target, engagement device, viewpoint, or evaluation characteristic is being changed? When NLG says content planning, discourse planning, and realization, this package asks: what is the source plan, what is the ordering rule, what is the generated carrier, and what admission and evaluation route owns it?

The practical consequence is a repair rule. If a domain term helps the worker choose or repair a narrative move, keep it as DPF vocabulary. If it starts carrying evidence, assurance, ethics, agency, publication, or Core ontology, route the claim to the FPF owner and state the blocked overread.

Hoffmann's "The Tensions of Scientific Storytelling" shows that scientific story construction can organize attempts, mechanisms, and unresolved tensions for readers; Schmid's `Narratology: An Introduction` and Chihaia's `Introductions to Narratology: Theory, Practice and the Afterlife of Structuralism` show that presentation and audience-facing narrative traditions differ by source tradition; Castricato et al.'s "Towards a Formal Model of Narratives" supports explicit narrator-to-reader information flow, reader story-model evolution, and uncertainty; Dahlstrom and Ho's "Ethical Considerations of Using Narrative to Communicate Science" warns that communicative purpose can become persuasion risk. The DPF adapts audience and purpose only after source-structure selection, temporal posture, rendering mediation mode, and role split are named. When a purpose, reader-use, science-storytelling, teaching, future-scenario, or persuasion-risk claim depends on a cited source basis, name that source basis and keep the claim within its boundary.

## [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose|NSTD.1]]:12 - Relations

Uses `A.6.3.NAR` for Core relation ownership, `A.16.1` when the first honest material is only a pre-articulation narrative cue, `C.2.LS` when language-state facets or thresholds shape the intake, `G.2` for source-pack claims, `C.33` when architecture-relevant structural-information capture or loss is current, [[NSTD/05_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] when non-architecture narrative epiplexity is evaluated, `D.1` through `D.5` when affected parties or persuasion are live, `A.10` for evidence, `B.3` for assurance, `E.10` and `F.18` for durable wording or naming repairs, and `G.11` for source and telemetry refresh. Support-map entry: open `Architecture and Narrative Work Bridge` when `renderingMediationMode` is `architecture-mediated` or `mixed`; open `Source Use And Refresh Map` when a cited source basis is relied on or stale; open `DPF Precision Restoration And Owner Map` when a local narrative term threatens to become ontology; open `Name And Edition Route` only for DPF-prefix or edition questions.

## [[NSTD/00_01_Source-Structure Intake and Narrative Purpose/00_NSTD.01 - Source-Structure Intake and Narrative Purpose|NSTD.1]]:End
