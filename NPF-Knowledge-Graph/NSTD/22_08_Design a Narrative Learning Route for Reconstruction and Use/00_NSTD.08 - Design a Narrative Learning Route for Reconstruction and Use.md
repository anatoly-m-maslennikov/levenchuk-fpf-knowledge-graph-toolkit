---
type: "npf-pattern"
context:
  - "NPF"
page_type: "npf-pattern"
mode: "canonical-generated"
npf_id: "NSTD.8"
title: "Design a Narrative Learning Route for Reconstruction and Use"
part: "[[00_Hubs/NPF - Patterns]]"
parents:
  - "[[00_Hubs/NPF - Patterns]]"
source_file: "Narrativization-and-Narrative-Studies-Principles-Framework.md"
source_revision: "fb3b6a4ad1d51d732a365f75f7d68337c7a751e2"
source_sha256: "c5c274316d31db178d105526ee32e912c4ccd02a6c03279a42f83244612737ba"
generated_on: "2026-10-25"
source_lines:
  - 2488
  - 2921
status: "Stable"
uses:
  - "A.6.3.NAR"
  - "B.4"
  - "E.11"
  - "E.17"
  - "E.17.AUD"
  - "E.21"
  - "E.22"
  - "E.23"
  - "E.6"
  - "G.11"
  - "[[NSTD/15_01_Choose a Narrative's Purpose and the Source Structures It Must Preserve/00_NSTD.01 - Choose a Narrative's Purpose and the Source Structures It Must Preserve|NSTD.1]]"
  - "[[NSTD/16_02_Choose a Narrative Order That Keeps Needed Source Relations Recoverable/00_NSTD.02 - Choose a Narrative Order That Keeps Needed Source Relations Recoverable|NSTD.2]]"
  - "[[NSTD/19_05_Choose Narrative Engagement Devices for the Intended Experience or Use/00_NSTD.05 - Choose Narrative Engagement Devices for the Intended Experience or Use|NSTD.5]]"
  - "[[NSTD/20_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]]"
generated: true
---


> **Status:** Stable

> **Type:** DPF pattern body

> **Primary EntityOfConcern:** designing and repairing a narrative learning route so learners can reconstruct and use the relevant source relations.

## [[NSTD/22_08_Design a Narrative Learning Route for Reconstruction and Use/00_NSTD.08 - Design a Narrative Learning Route for Reconstruction and Use|NSTD.8]]:1 - Problem frame

Use this pattern when a complex source structure must be taught, explained, or learned through a narrative route, and the route must preserve enough structure for learners to reconstruct and apply it later. The governed object is the instructional route and its relation to source structure, not every explanation or reference publication. A publication used only for lookup or a professional decision need not become a course.

First useful move: begin at one consequential transition. Recover the current question, what the learner has already met, the contribution now needed and the support actually available there. Try the next task with that support, then repair the missing connection or choose the next useful teaching move.

Architecture warning: the source corpus may have a good reference architecture and still make a bad learning route if copied directly into the course. Engineers often make a blocked topic route: one coherent module after another, with each topic concentrated in its own lesson. That can be excellent for a reference manual, API, or architecture description, but weak for learning when learners must discriminate neighboring cases, retrieve earlier distinctions, and transfer the structure under varied cues.

What goes wrong if missed: the explanation is engaging and memorable, but learners retain examples, slogans, analogies, and mood while losing architecture, relation records, proof obligations, pattern-use routes, source-return conditions, or improvement cycles.

What this buys: a route that helps learners use the source ideas, with the needed material available when the next task requires it.

## [[NSTD/22_08_Design a Narrative Learning Route for Reconstruction and Use/00_NSTD.08 - Design a Narrative Learning Route for Reconstruction and Use|NSTD.8]]:2 - Problem

A learning narrative uses sequence, examples, repetition, analogy and motivation to help the learner reconstruct and use source ideas. Those choices can also conceal a prerequisite or make an illustrative route appear to be the only way to perform a method. This pattern describes how to design and repair the route. Worked examples belong in a pattern when they explain its method; a complete course script is a separate teaching product.

A common engineering failure is the reference-manual course. The course follows the module architecture of the source: first all of topic A, then all of topic B, then all of topic C, each with concentrated examples. Learners can follow each block locally, but later fail to choose the right pattern, distinguish nearby structures, remember earlier conditions, or transfer across domains. The repair is not to destroy the source architecture. Keep the source architecture as source return, then design a different learning-route architecture with deliberate interleaving, spaced retrieval, recurring anchors, and transfer tasks.

## [[NSTD/22_08_Design a Narrative Learning Route for Reconstruction and Use/00_NSTD.08 - Design a Narrative Learning Route for Reconstruction and Use|NSTD.8]]:3 - Forces

| Force | Tension |
| --- | --- |
| Didactic route vs source corpus | Learning order may differ from publication order, proof order, architecture order, or framework order. |
| Source architecture vs learning-route architecture | High cohesion and low coupling can be good for the source corpus but harmful when copied as blocked topic instruction. |
| Local fluency vs durable discrimination | Blocked topic lessons feel orderly and efficient, while interleaving can feel harder but can improve later choice and transfer. |
| Coverage vs spaced retrieval | A course can cover every topic once and still leave learners unable to retrieve earlier structures when they matter later. |
| Engagement vs reconstruction | Learners may enjoy a story, analogy, example, or lesson without reconstructing source structure. |
| Carrier specificity vs pattern generality | Lessons, slides, scripts, worked examples, and exercises are needed, but pattern bodies must stay general. |
| Local teaching evidence vs package authority | Test-run evidence helps a learning route, but does not by itself make the package authoritative. |

## [[NSTD/22_08_Design a Narrative Learning Route for Reconstruction and Use/00_NSTD.08 - Design a Narrative Learning Route for Reconstruction and Use|NSTD.8]]:4 - Solution

Design the needed transition and its continuation. The optional route note below helps when a team maintains a course, compares versions or coordinates several teaching materials. Keep the fields that those uses need; a short explanation does not require a full course record.

```text
LearningNarrativeRoute@Context:
  learnerUse:
  sourceStructureSpineRefs:
  unfoldingStructureRefs?:
  demonstrativeSliceRefs?:
  sourceArchitectureRef?:
  learningRouteArchitectureRule:
  learningStepOrderingRule:
  interleavingPlanRefs?:
  spacingOrRetrievalScheduleRefs?:
  recurringAnchorRefs?:
  sourceReturnLinkRefs:
  learnerReconstructionTaskRefs:
  applicationTaskRefs?:
  engagementBoundaryRef?:
  narrativeRenderingQualityEvaluationRef:
  improvementLoopInputRef?:
  learningPublicationCarrierRefs:
  blockedTopicOverread?:
  nonAdmissibleUse:
  refreshCondition:
```

A maintained course may have separate lessons, slides, exercises and recordings. Link them to the source ideas and learner tasks they serve. The size and publication form depend on the teaching work.

When teaching a constraint-governed unfolding structure, make the wider possibilities recoverable alongside the demonstrated path. Teach an omitted alternative or stop condition at the point where it changes the learner's action. A route note can link the wider structure and the taught slice when that helps maintenance.

The following design questions connect the route's components. They can be addressed together and revisited after an attempted task; each need not become a separate pass or work product.

| Design question | Useful result | Failure it addresses |
| --- | --- | --- |
| Which source ideas will the learner need? | The relations and operations needed for later reconstruction or application. | A memorable example with no usable connection to the subject. |
| Does the source organization suit learning here? | A reasoned choice of learning order, with the source organization still accessible. | Copying a reference topic map without considering the learning task. |
| What must be available before the next task? | A sequence or usable return that supplies the prerequisite at that point. | Requiring an operation before its necessary relation is available. |
| Must learners later distinguish neighboring cases? | Mixed selection or comparisons when the learner has enough support to use them. | Success based on the topic label rather than recognition of the case. |
| Must the idea remain available after a delay? | Suitable later retrieval attempts and feedback. | Immediate recognition mistaken for durable retrieval. |
| How does an aid connect to the current question and next use? | A meaningful term, diagram, question or case with its relation recoverable. | Remembering the aid but not what to do with it. |
| What must the learner recover or perform? | A task that exposes the needed distinction or operation. | Satisfaction mistaken for practical capability. |
| What result would change the route? | A scoped [[NSTD/20_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation]] judgement and a worthwhile next repair. | Treating every teaching change as an improvement. |

Do not optimize the learning-route architecture for local neatness. A locally neat blocked route can be globally weak: it gives learners the answer key for the current block, so they do not practice selecting the right owner under mixed cues. Interleaving is useful when the learner must later discriminate similar patterns, methods, proof obligations, architecture structures, or source-return owners. Spacing is useful when the learner must still retrieve a structure after other material has intervened. Use them as design moves with declared learner use, not as decorative variety.



### [[NSTD/22_08_Design a Narrative Learning Route for Reconstruction and Use/00_NSTD.08 - Design a Narrative Learning Route for Reconstruction and Use|NSTD.8]]:4.1 - Check attachment and support at the next use


Inspect the relation between a block or learning aid and both its surrounding context and its later use. What question is active, what distinction or action does this example, image, explanation or exercise enable, why is it needed here, and where will its result be used? A question, worked example, caption, short transition or later payoff can carry that relation. There is no compulsory five-field form and no quota of connective phrases. A repeated word is not enough when the reader still cannot connect the two uses.

Then inspect the route prefix: the material encountered up to the point where a new reconstruction or action is required. Identify the relevant distinctions already introduced, necessary prerequisites expected of this audience, newly introduced objects or relations, still-open questions and the means available now. Ask the reader to use those means on the next task. A relation shown only much later cannot support the current action unless a usable return makes it available. An overview is useful when it exposes the needed relation, not merely because it lists topics.

Keep three different repair questions separate:

- A missing attachment: restore the relation between the active question, the block or aid and its next use; correct a wrong return or an unexplained visual edge.
- An unsupported new demand: supply the necessary contrast, map, worked operation, recap, accessible representation or introduction order before relying on that operation. Check the promised prerequisite and assistance first; do not simplify away needed subject structure.
- A deliberate preparatory attempt: let the learner try a bounded problem before the explanation when that serves the learning design, preserve the attempted alternatives, and use subsequent instruction to compare and resolve them. Difficulty or an incorrect first attempt is not by itself a material defect, but unresolved failure is not evidence of productive preparation.

Use a stable supported initial case when the learner needs it to build the distinction before mixed selection. Interleaving, spacing and retrieval serve the declared later task; they do not require every first encounter to mix unfamiliar alternatives. Conversely, making every block easy by naming its answer does not test later independent selection. Judge the actual point and contribution rather than choosing one universal order.

Preserve the first response before a cue supplies the distinction being tested. Report the allowed help, help actually used, source contribution and the reader's prior expertise. A teacher-supported correction may fulfil the declared arrangement while leaving independent first recognition untested. An expert's successful reconstruction does not erase a contrary report from a less-prepared reader. Use an appropriately scoped observation if that reader's difficulty can change the repair.

Structural reconstruction demand is not experienced cognitive load. [[NSTD/20_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] applies C.2.8 as NarrativeRenderingEpiplexity to the narrative account, expression and observer under the selected reading conditions; it is neither a quantity to maximize unconditionally nor a burden meter. A material inspection or agent walkthrough can locate a missing relation and available support, but claims about human burden, learning, retention or transfer need their own observations and conditions. For reported burden, identify the person, segment, timing and instrument.

Recheck the changed attachment, the affected prefix and its next task while preserving unaffected source and route results. If the intended reader already recovers the relation and completes that task with the declared support, density alone is not a reason to insert another aid. Use `E.23` for a worthwhile repair; shortening, added pictures or extra repetition are not improvements without a changed useful result and protected qualities.

Use reconstruction tasks at several depths.

| Task depth | Example task | What it tests |
| --- | --- | --- |
| Recognition | "Which method addresses this difficulty, and what tells you so?" | Whether the learner recognizes the conditions of use. |
| Reconstruction | "Rebuild the pattern-use route from source basis, forces, solution, and exit." | Whether source structure survived the narrative. |
| Transfer | "Apply the same route to a different domain case." | Whether the learner learned structure rather than anecdote. |
| Boundary | "When would you use another method, and which one?" | Whether the learner can select a useful alternative. |
| Repair | "Given a low [[NSTD/20_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation]] row, choose the smallest repair route." | Whether improvement discipline survived the lesson. |

Examples, stories, rhythm, repetition and analogy can all support learning. Keep a device when it helps the intended task. If a learner retains the device but misses a necessary relation, repair that connection rather than automatically adding or removing examples.

For a small route, a short learner attempt or observed confusion may answer the current repair question. A repeated course may need to retain the version, audience, task, assistance and result so later comparisons remain interpretable. Collect more only when the result can change the design or intended use. A local teaching revision is not by itself a claim about evolution under `B.4`.

If the route is improved across runs, first evaluate the concrete route version through [[NSTD/20_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]]. Use `E.22` when learner value, floor, protected trade-offs, evidence, or result form are still underframed; use `E.23` to repair a declared changed slice such as source spine, learning-step order, reconstruction tasks, learning publication carrier, engagement boundary, or evaluation characteristic space. Use `G.11` when source currentness, learner telemetry, teaching-test evidence, generated practice, or FPF edition changes; use `B.4` only when making an evolution claim about the learning route as a holon across repeated operation.

## [[NSTD/22_08_Design a Narrative Learning Route for Reconstruction and Use/00_NSTD.08 - Design a Narrative Learning Route for Reconstruction and Use|NSTD.8]]:5 - Archetypal Grounding



### [[NSTD/22_08_Design a Narrative Learning Route for Reconstruction and Use/00_NSTD.08 - Design a Narrative Learning Route for Reconstruction and Use|NSTD.8]]:5.1 - Worked learning route: FPF onboarding


This example sketches the route that a seminar, tutorial or exercise sequence could realize. The note is optional; the important relation is between each teaching move and the next learner action.

```text
LearningNarrativeRoute@FPFOnboarding:
  learnerUse: new practitioner can apply one FPF pattern without treating it as a recipe
  sourceArchitectureRef: FPF pattern language and monolith and source pattern organization
  sourceSpineRefs:
    - `EntityOfConcern`
    - problem frame
    - forces
    - solution as condition-bound move
    - conformance and checking
    - neighboring exits
    - quality and improvement loop
  unfoldingStructureRefs: A.22.CGUS when the route teaches unfolding from source to next use
  demonstrativeSliceRefs: first pattern-use route through one selected project case
  learningRouteArchitectureRule: interleaved pattern-use route, not monolith-reference order
  learningStepOrder:
    - failed ordinary use
    - recover object of concern
    - read forces
    - choose solution move
    - check boundary and neighboring owner
    - repair one low-value result
  interleavingPlanRefs:
    - return to `EntityOfConcern` after forces, solution, and quality checks
    - mix adjacent owner-choice cases after each new pattern
    - revisit source-return boundary in examples from at least two domains
  spacingOrRetrievalScheduleRefs:
    - short delayed retrieval at the start of the next session
    - later mixed owner-choice task after intervening material
    - final transfer task with no block label
  reconstructionTasks:
    - name the source pattern section behind each story beat
    - choose the governing pattern for a new case
    - state one source-return condition
  engagementBoundaryRef: failure story is an archetype, not evidence
  evaluationRouteRef: `NSTD.6` learning-route rows
  improvementLoopInputRef: `E.23` when a comparison identifies a worthwhile improvement
```

In this onboarding route, the opening failed use may be preparation rather than a failed capability assessment. The subsequent recovery of the object of concern must work with the attempted alternatives: show which object the next move governs and why the tempting alternative does not answer that question. Before the later neighbor-choice task, inspect whether those neighboring entries and their distinguishing condition are already available. If not, introduce the contrast or provide an accessible source return; merely adding another unlabeled failure would not supply it. If the entries are available, the mixed case can test their selection instead of prompting the answer.

A concrete task in an introduction to FPF-based pattern use can use two neighboring NSTD methods already available in this publication. First make the distinction available: [[NSTD/16_02_Choose a Narrative Order That Keeps Needed Source Relations Recoverable/00_NSTD.02 - Choose a Narrative Order That Keeps Needed Source Relations Recoverable|NSTD.2]] changes presentation order while preserving needed relations; [[NSTD/17_03_Repair Missing or Unsupported Narrative Connections (Coherence and Event Models)/00_NSTD.03 - Repair Missing or Unsupported Narrative Connections (Coherence and Event Models)|NSTD.3]] examines the connection the account asserts. Then give the Readme's incident log, whose causal investigation is still open, and its draft “the change caused the failure”. Ask: “Would moving the two logged events into chronological order settle this sentence? Which question must the repair answer?”

A supplied response in this design example is: “Put the change before the failure, so the cause is clear.” That response preserves chronology but still infers cause from order. If the distinction was unavailable, provide it and work through the two claims before another selection task. If this was a deliberate preparatory attempt, subsequent instruction should use that attempted answer to explain why chronology leaves the causal question open. If both entries were already available, return to the sentence and ask what the log establishes; then use a mixed case to check whether the learner selects a connection repair rather than an ordering repair. These continuations answer different difficulties.

A later diagram or recap should connect that choice to the next use. A wrong figure return calls for correcting the attachment, not automatically redesigning the entire course. After the repair, ask the reader to recover that relation and use it under the declared support. This is a worked design example with a supplied response, not an observation of a learner or a demonstrated learning gain.

A seminar file can add timing, facilitation notes and complete exercises. This pattern keeps the examples needed to explain route design without prescribing a complete seminar.



### [[NSTD/22_08_Design a Narrative Learning Route for Reconstruction and Use/00_NSTD.08 - Design a Narrative Learning Route for Reconstruction and Use|NSTD.8]]:5.2 - Worked learning route: repair topic-blocked practice


An engineering team wants a course on architecture patterns. Their first outline looks clean:

```text
Lesson 1: all source-structure intake.
Lesson 2: all ordering rules.
Lesson 3: all viewpoint and agency.
Lesson 4: all engagement.
Lesson 5: all evaluation.
```

This outline gives learners the problem type inside each block. It may support first practice but leave later independent selection unpractised: a new failure may concern source selection, ordering, viewpoint, engagement, generation or the grounds for a claim.

Repair the route:

```text
LearningNarrativeRoute@ArchitecturePatternCourse:
  learnerUse: engineer chooses and repairs the right pattern under mixed project situations
  sourceArchitectureRef: topic map and source pattern bodies
  sourceSpineRefs:
    - selected source structure
    - ordering rule
    - viewpoint and agency split
    - engagement boundary
    - narrative rendering quality row
    - source-return and owner routing
  learningRouteArchitectureRule: spaced interleaving around recurring project cases
  learningStepOrder:
    - one motivating project failure
    - source-selection repair
    - different project failure requiring ordering repair
    - return to first failure and add viewpoint risk
    - mixed owner-choice exercise
    - delayed retrieval of source-return boundaries
    - final transfer to an unseen case
  interleavingPlanRefs:
    - every session mixes at least one current pattern with one earlier pattern
    - adjacent failure modes are compared side by side
    - examples rotate across FPF seminar, architecture explanation, homotopy explanation, generated carrier, and live commentary
  spacingOrRetrievalScheduleRefs:
    - start each session with a no-label retrieval task from a prior session
    - return to `EntityOfConcern`, source-return, and owner-routing at increasing delays
    - require one late repair of an old low-value row after new material intervenes
  blockedTopicOverread: a clean topic block is not evidence of durable pattern choice
  evaluationRouteRef: `NSTD.6` rows for transfer, source return, and learner reconstruction
```

The repaired route still preserves the source architecture. It simply refuses to treat that architecture as the course order. The learner sees a pattern, uses it, leaves it, then returns under a different cue. That is the point: source modules can stay modular while the learning route deliberately crosses module boundaries.



### [[NSTD/22_08_Design a Narrative Learning Route for Reconstruction and Use/00_NSTD.08 - Design a Narrative Learning Route for Reconstruction and Use|NSTD.8]]:5.3 - Worked learning route: homotopy explanation


```text
LearningNarrativeRoute@HomotopyIntro:
  learnerUse: learner distinguishes intuitive deformation picture from formal definition and proof boundary
  sourceSpineRefs:
    - topological space
    - path
    - homotopy relation under constraints
    - invariant
    - example and counterexample
    - proof-status return
  learningStepOrder:
    - image cue
    - constraint marker
    - formal definition return
    - example
    - counterexample
    - reconstruction task
  reconstructionTasks:
    - mark where analogy stops
    - state which deformations are not allowed
    - return one claim to formal source
  engagementBoundaryRef: vivid image cannot replace definition
  evaluationRouteRef: `NSTD.6` rows for ordering, language-state precision, and source return
```

If learners can retell the loop picture but cannot state the required constraint, repair the connection to the definition. A suitable example, counterexample or worked comparison may supply that repair.



### [[NSTD/22_08_Design a Narrative Learning Route for Reconstruction and Use/00_NSTD.08 - Design a Narrative Learning Route for Reconstruction and Use|NSTD.8]]:5.4 - Worked learning route: using this pattern language


A short course on this DPF may use the three probes: FPF seminar, franchise continuation, and homotopy explanation, with live commentary as a fourth transfer case. The route succeeds only if learners can see the same pattern set working across different domains:

| Step | Probe | Pattern focus | Transfer question |
| --- | --- | --- | --- |
| 1 | FPF seminar | [[NSTD/15_01_Choose a Narrative's Purpose and the Source Structures It Must Preserve/00_NSTD.01 - Choose a Narrative's Purpose and the Source Structures It Must Preserve]], [[NSTD/22_08_Design a Narrative Learning Route for Reconstruction and Use/00_NSTD.08 - Design a Narrative Learning Route for Reconstruction and Use]] | What source spine must survive a learning route? |
| 2 | Franchise continuation | [[NSTD/15_01_Choose a Narrative's Purpose and the Source Structures It Must Preserve/00_NSTD.01 - Choose a Narrative's Purpose and the Source Structures It Must Preserve]], [[NSTD/16_02_Choose a Narrative Order That Keeps Needed Source Relations Recoverable/00_NSTD.02 - Choose a Narrative Order That Keeps Needed Source Relations Recoverable]], [[NSTD/17_03_Repair Missing or Unsupported Narrative Connections (Coherence and Event Models)/00_NSTD.03 - Repair Missing or Unsupported Narrative Connections (Coherence and Event Models)]], [[NSTD/21_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning]] | What counts as source pack and event support when facts are prospective or fictional? |
| 3 | Homotopy explanation | [[NSTD/16_02_Choose a Narrative Order That Keeps Needed Source Relations Recoverable/00_NSTD.02 - Choose a Narrative Order That Keeps Needed Source Relations Recoverable]], [[NSTD/19_05_Choose Narrative Engagement Devices for the Intended Experience or Use/00_NSTD.05 - Choose Narrative Engagement Devices for the Intended Experience or Use]], [[NSTD/20_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation]] | Where does analogy stop and formal source return begin? |
| 4 | Live commentary | [[NSTD/17_03_Repair Missing or Unsupported Narrative Connections (Coherence and Event Models)/00_NSTD.03 - Repair Missing or Unsupported Narrative Connections (Coherence and Event Models)]], [[NSTD/20_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation]], `G.11` | Which claims are provisional until later source return? |

The transfer question is the actual teaching test. Remembering case names is not learning. The learner must choose the live pattern and repair the failure in a new situation.



### [[NSTD/22_08_Design a Narrative Learning Route for Reconstruction and Use/00_NSTD.08 - Design a Narrative Learning Route for Reconstruction and Use|NSTD.8]]:5.5 - Before and after repair: teaching material inside pattern body


Before:

> This pattern should include a full seminar script so readers can immediately teach narrativization.

Failure: a complete seminar script can obscure the reusable route method and its alternatives. A worked example that explains a particular operation remains useful inside the pattern.

After:

> This pattern explains how to design the learning route, with worked examples of its operations. A complete seminar script, slide deck and session notes are separate teaching products. Their learner tasks and source returns can be evaluated through [[NSTD/20_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]].



### [[NSTD/22_08_Design a Narrative Learning Route for Reconstruction and Use/00_NSTD.08 - Design a Narrative Learning Route for Reconstruction and Use|NSTD.8]]:5.6 - Evaluating the learning route


Select the outcome needed for the declared teaching use. Immediate reconstruction, delayed retrieval, discrimination among similar cases and transfer to a new case require different tasks and observations. Success at one does not establish the others. A one-off explanation may need only immediate reconstruction; a course promising durable independent use needs an appropriately delayed and varied task.

Use [[NSTD/20_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] with the observer, prior preparation, assistance and reading conditions stated. Keep an author's walkthrough distinct from an observed learner result.



### [[NSTD/22_08_Design a Narrative Learning Route for Reconstruction and Use/00_NSTD.08 - Design a Narrative Learning Route for Reconstruction and Use|NSTD.8]]:5.7 - Connecting route design to publication and improvement


[[NSTD/22_08_Design a Narrative Learning Route for Reconstruction and Use/00_NSTD.08 - Design a Narrative Learning Route for Reconstruction and Use|NSTD.8]] uses `E.11` for framework entry, `E.17` for publication form, `E.17.AUD` for a separately usable audience unit, [[NSTD/19_05_Choose Narrative Engagement Devices for the Intended Experience or Use/00_NSTD.05 - Choose Narrative Engagement Devices for the Intended Experience or Use|NSTD.5]] for engagement and [[NSTD/20_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] for evaluation. `E.22`/`E.23` support a selected improvement; `G.11` addresses an applicable source or practice refresh. A one-off explanation and a maintained course need different amounts of recorded design.

An FPF learning route, such as a seminar series or tutorial sequence, teaches the framework across several steps. The source-structure spine includes EntityOfConcern discipline, relation precision, pattern bodies, DPF authoring, architecture synthesis, evaluation, improvement loops, and source-return discipline. The learning order is didactic, not proof of FPF architecture. Learner tasks ask participants to reconstruct one pattern-use route from source basis and selected source structure, not only repeat a story or slogan.

A homotopy mini-course may start with pictures and deformation stories. Its reconstruction task should reveal whether the learner can recover the required definitions and conditions. When an analogy conceals a constraint, a counterexample or comparison can show why the formal boundary matters.

A DPF onboarding route may teach narrative rendering through three cases: FPF seminar, franchise storycraft, and live commentary. The route is successful only if learners can reconstruct why all three open [[NSTD/15_01_Choose a Narrative's Purpose and the Source Structures It Must Preserve/00_NSTD.01 - Choose a Narrative's Purpose and the Source Structures It Must Preserve|NSTD.1]], why different patterns become live later, and why [[NSTD/20_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] evaluates a declared rendering version rather than a general story. The test is transfer across cases, not recall of the case names.

Use [[NSTD/21_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning|NSTD.7]] to inspect a generated teaching draft against the source ideas and intended tasks. [[NSTD/20_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] can evaluate it before acceptance. Apply `C.35` only when the generated result is being used for architecture work; producing a slide or example does not itself select that pattern.

Distinguish versions when comparing repeated teaching or maintaining materials. The following optional note is useful when the comparison needs these details.

```text
LearningNarrativeRouteVersion@Context:
  routeRef:
  sourceSpineVersionRef:
  learnerRoleRef:
  learningStepOrderingRule:
  carrierRefs:
  reconstructionTaskRefs:
  evaluationResultRef:
  observedConfusionOrTelemetryRefs?:
  changedSliceSincePreviousVersion?:
  refreshCondition:
```

For a comparison, identify which material and order each group encountered and what changed. Re-evaluate the affected outcome before claiming improvement. An untracked slide change may still be useful, but cannot support a precise comparison of course versions. A relevant source change calls for reviewing the affected teaching content.

The following example plan connects subject content, the immediate teaching move and a later use. Adapt its timing and returns to the learner's task.

| Source-spine item | Narrative or teaching move | Interleaving or spacing move |
| --- | --- | --- |
| Pattern entry condition | Recognition story, contrast case, or failed-use story. | Return after two other pattern cases and ask for owner choice without a label. |
| Forces | Tension sequence, stakeholder conflict, or trade-off map. | Compare with a different pattern's forces in a mixed exercise. |
| Solution move | Demonstration, guided reconstruction, or worked slice. | Reuse the same project case later with a different repair owner. |
| Boundary and non-use | Counterexample, wrong-owner case, or blocked overread. | Start a later session with a delayed boundary retrieval question. |
| Relations | Neighboring-pattern exit exercise. | Interleave adjacent exits so the learner must discriminate them. |
| Quality and improvement | Low-value row and repair exercise. | Revisit an old low-value row after new material and require a changed-slice repair. |

The left column names the source ideas to recover; the middle names an immediate teaching move; the right shows a possible later return. Use the last column when delayed retrieval or mixed selection is part of the goal. Its presence alone does not establish learning, and its absence is not a defect in a route that does not need those outcomes.

Examples of different learning aims:

| Route type | Source spine | Narrative devices allowed | Reconstruction evidence |
| --- | --- | --- | --- |
| FPF onboarding route | Pattern entry, EoC, forces, solution, relations, checks, improvement loop. | Practitioner story, failed-use contrast, recurring source-return prompt. | Learner selects correct owner and reconstructs one pattern-use route. |
| Mathematical explanation route | Definitions, examples, theorem prerequisites, proof-status boundaries. | Analogy, diagram story, dependency sequence, counterexample. | Learner marks where analogy stops and returns to formal statement. |
| Architecture explanation route | Candidate structures, characteristics, decisions, trade-offs, telemetry. | Trade-off story, viewpoint over stakeholder role, decision-memory path. | Learner separates architecture description, decision, realized structure, and telemetry. |
| Generated teaching route | Selected source relations and the intended learner operation. | Generated examples or slides inspected through [[NSTD/21_07_Automated Narrativization and Story Planning/00_NSTD.07 - Automated Narrativization and Story Planning]], with `C.35` only for architecture use. | Learner tasks for the intended outcome; direct comparison with the sources where fidelity is claimed. |
| Live debrief route | Event record, provisional interpretation, official correction, source return. | Recap story, tension order, role viewpoint. | Learner distinguishes observation, inference, prediction, and official update. |

For a short one-off teaching note, the route can be tiny: one source-spine item, one ordering rule, one reconstruction question, one source-return link. For a repeated seminar or course, the route should have versioned carriers, task results, and low-value repairs. The size changes; the source-return discipline does not.

Do not use popularity as learning evidence. Attendance, satisfaction, applause, or "people liked the story" may be engagement telemetry, but it is not reconstruction evidence. Reconstruction evidence asks whether learners can rebuild the source relation, apply it to a new case, name a boundary, or choose a repair.

## [[NSTD/22_08_Design a Narrative Learning Route for Reconstruction and Use/00_NSTD.08 - Design a Narrative Learning Route for Reconstruction and Use|NSTD.8]]:6 - Bias-Annotation

A learning route can be mistaken for the subject it teaches: its lesson order, exercise sequence or analogy then replaces the source relations. Keep those relations available and show how each teaching move prepares the next learner task. Worked examples belong in a pattern when they explain its reusable method. Maintain a complete seminar or course separately when its timing, facilitation and session-specific exercises would obscure that method.

Copying the source corpus's modules into a course can leave later selection unpractised. Keep the source modules available, then add interleaving or spacing when the learner must later discriminate, retrieve or transfer relations across topic boundaries.

## [[NSTD/22_08_Design a Narrative Learning Route for Reconstruction and Use/00_NSTD.08 - Design a Narrative Learning Route for Reconstruction and Use|NSTD.8]]:7 - Conformance Checklist

| Check | Passing condition |
| --- | --- |
| `CC-NSTD8-1` | Learner use and source-structure spine are named. |
| `CC-NSTD8-2` | Learning-step ordering rule and source-return links are explicit. |
| `CC-NSTD8-3` | Learner reconstruction tasks test source structure, not only recall of narrative highlights. |
| `CC-NSTD8-4` | Worked examples explain the reusable method; a complete course or seminar script is maintained as a separate teaching product when needed. |
| `CC-NSTD8-5` | A claimed improvement identifies the compared route versions, affected outcome, relevant costs and protected qualities; [[NSTD/20_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation]] supports evaluation and `E.22`/`E.23` the applicable improvement question. |
| `CC-NSTD8-6` | Source organization and learning order are distinguished. Interleaving, spacing and delayed or mixed tasks are selected for the intended learning outcome and available support. |
| `CC-NSTD8-7` | Material attachments and consequential prefixes connect the current question, available structure/support and next use; missing relations, unsupported demands and deliberate preparatory attempts receive different repairs or continuation. |
| `CC-NSTD8-8` | First and helped responses, source contribution, prior expertise and human learning or burden claims retain their own evidence boundaries; structural density is not treated as observed cognitive load. |

## [[NSTD/22_08_Design a Narrative Learning Route for Reconstruction and Use/00_NSTD.08 - Design a Narrative Learning Route for Reconstruction and Use|NSTD.8]]:8 - Common Anti-Patterns and How to Avoid Them

| Anti-pattern | What fails | Repair |
| --- | --- | --- |
| Learning route as source structure | Lesson sequence, seminar order, analogy chain, or explainer order is treated as framework architecture, proof order, or source structure. | Declare learning-step ordering rule and source-return links. |
| Reference order chosen without examining the learning task | The topic map is copied into lessons without checking what the learner must subsequently recognize, select or use. | Keep a source-aligned introduction when it supplies the needed support. Add contrasts, mixed selection or delayed retrieval when the intended outcome calls for them. |
| Blocked practice fluency | Learners perform well inside a topic block because its label supplies the method choice. | Use an unlabelled or mixed new case to test selection or transfer. Add delayed retrieval when later availability is also part of the claim. |
| Complete course substituted for a pattern | Session-specific material hides the reusable method and its alternatives. | Keep the explanatory worked cases in the pattern; maintain the full course materials separately. |
| Recall as reconstruction | Learners remember examples but cannot use patterns. | Add reconstruction and application tasks; evaluate through [[NSTD/20_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation]]. |
| Fluent blocks without a usable connection | Each paragraph reads well, but the current question, aid or later use cannot be related. | Inspect both endpoints and the affected prefix; restore the missing relation or usable return, then repeat the next task. |
| Difficulty judged without its teaching function | Every hard transition is compressed, or every unsuccessful attempt is called productive. | Separate an unsupported demand from deliberate preparation; provide the missing support or make subsequent instruction resolve the attempted alternatives. |
| Teaching tweak as evolution | A revised slide, example, or prompt is described as evolved route quality without telemetry and re-evaluation. | Treat the tweak as an `E.23` changed slice after [[NSTD/20_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation]]; use `G.11` for refresh and reserve `B.4` for actual evolution claims over the route across operation. |

## [[NSTD/22_08_Design a Narrative Learning Route for Reconstruction and Use/00_NSTD.08 - Design a Narrative Learning Route for Reconstruction and Use|NSTD.8]]:9 - Consequences

The benefit is a path that helps learners recover and use the source ideas. Its cost is designing the necessary connections and obtaining observations proportionate to the learning claims made.

## [[NSTD/22_08_Design a Narrative Learning Route for Reconstruction and Use/00_NSTD.08 - Design a Narrative Learning Route for Reconstruction and Use|NSTD.8]]:10 - Rationale

Different learning aims require different combinations of explanation, examples, attempts, feedback and later returns. Keeping the subject structure accessible permits a teaching route to vary those combinations without making the lesson sequence the only account of the subject.

A modular source corpus can support lookup and a first introduction while still leaving later selection unpractised. When learners must choose among similar methods without a topic label, the learning route needs those contrasts and selection tasks. When later retrieval matters, it needs an appropriate delay and return. The source organization remains available; whether the learning order should follow it depends on the task and the support already available.

## [[NSTD/22_08_Design a Narrative Learning Route for Reconstruction and Use/00_NSTD.08 - Design a Narrative Learning Route for Reconstruction and Use|NSTD.8]]:11 - SoTA-Echoing

Mengelkamp et al.'s "Effects of Reading Goal Instructions on the Comprehension and Metacomprehension of Informative Narratives" makes study goals and metacomprehension risk visible; Georgiou et al.'s "Large-scale study of human memory for meaningful narratives" shows that long narratives can be remembered as gist and sequence rather than source detail; Hoffmann's "The Tensions of Scientific Storytelling" supplies a science-storytelling example where unresolved tension and source return matter. Dunlosky et al.'s "Improving Students' Learning With Effective Learning Techniques" rates practice testing and distributed practice as high-utility techniques and treats interleaved practice as promising for appropriate situations. Rohrer and Taylor's "The shuffling of mathematics problems improves learning" directly shows the risk of standard blocked textbook practice and the benefit of spaced and mixed practice in mathematics problems. Kang's "Spaced Repetition Promotes Efficient and Effective Learning" gives a policy-level synthesis: spacing repeated encounters with material improves long-term learning and can be combined with tests. [[NSTD/22_08_Design a Narrative Learning Route for Reconstruction and Use/00_NSTD.08 - Design a Narrative Learning Route for Reconstruction and Use|NSTD.8]] retains the Dunlosky, Rohrer–Taylor and Kang contributions as historical anchors for spacing and interleaving questions. The bounded source contributions here inform learning-route design, reconstruction and source return, not a complete pedagogy doctrine.

For the attachment and prefix-support work, [Noetel et al. (2022)](https://journals.sagepub.com/doi/10.3102/00346543211052329) supports mechanism-specific attention to signaling, correspondence and pacing rather than a rule to add pictures everywhere. [Sinha and Kapur (2021)](https://journals.sagepub.com/doi/abs/10.3102/00346543211019105) supports distinguishing problem solving followed by instruction from unsupported failure; its conditional, largely mathematics/physics evidence does not make all difficulty productive. [Wesenberg et al. (2025)](https://doi.org/10.1016/j.cedpsych.2024.102328) motivates checking whether a worked example also permits a consequentially wrong rule; the studied brief units do not establish a universal order for long routes. [Krieglstein et al. (2025)](https://doi.org/10.1007/s10648-024-09980-0) shows why retrospective load reports need an explicit timing and segment: the reported primacy effect concerns self-report in the studied setting, not a conversion from source-structure density to human burden. These contributions qualify the choice of support and the inference from a reader response; none validates this entire route method or its ordinal values.

Operational payload:

- From reading-goal work, declare the learner use before the lesson route. A route for curiosity, exam preparation, professional use, or framework authoring needs different reconstruction tasks.
- From metacomprehension risk, ask learners to reconstruct or apply source structure, not only rate whether they understood.
- From memory work, long routes need anchors and returns. Repetition should protect source spine rather than repeat slogans.
- For durable retrieval, consider spaced practice and delayed retrieval rather than infer retention from immediate success. Judge the result under the actual schedule and task.
- From interleaving work, blocked topic practice can hide the real choice problem. Mix adjacent owners, cases, or problem types when the learner must later decide which structure applies.
- Preserve the source organization for lookup and source return. A first introduction may follow it when that supplies the needed support; choose a different order for a later task that requires contrasts, mixed selection or delayed retrieval.
- From scientific storytelling, unresolved tension can be taught honestly. The route can preserve open questions instead of pretending closure.
- For a claimed teaching improvement, compare the relevant route versions and affected outcomes. A low score is not required before a worthwhile improvement can be considered.

The practical result is a route whose explanations, attempts and later returns support the declared learner use. Keep an adequate source-aligned segment; repair a missing connection, an unsupported demand or an unpractised selection only where it changes the intended result.

## [[NSTD/22_08_Design a Narrative Learning Route for Reconstruction and Use/00_NSTD.08 - Design a Narrative Learning Route for Reconstruction and Use|NSTD.8]]:12 - Relations

Uses `A.6.3.NAR`, `E.6`, `E.11`, `E.17`, `E.17.AUD`, [[NSTD/15_01_Choose a Narrative's Purpose and the Source Structures It Must Preserve/00_NSTD.01 - Choose a Narrative's Purpose and the Source Structures It Must Preserve|NSTD.1]], [[NSTD/16_02_Choose a Narrative Order That Keeps Needed Source Relations Recoverable/00_NSTD.02 - Choose a Narrative Order That Keeps Needed Source Relations Recoverable|NSTD.2]], [[NSTD/19_05_Choose Narrative Engagement Devices for the Intended Experience or Use/00_NSTD.05 - Choose Narrative Engagement Devices for the Intended Experience or Use|NSTD.5]], [[NSTD/20_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]], `E.21`, `E.22`, `E.23`, `B.4`, and `G.11`. [[NSTD/19_05_Choose Narrative Engagement Devices for the Intended Experience or Use/00_NSTD.05 - Choose Narrative Engagement Devices for the Intended Experience or Use|NSTD.5]] bounds motivation and interest; [[NSTD/20_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] evaluates one route version; `E.22` frames under-specified quality questions; `E.23` repairs a declared changed slice; `G.11` refreshes source, telemetry, edition, or practice currentness; `B.4` is only for evolution claims over the learning route. Reopen when learner use, source spine, source architecture, learning-route architecture, interleaving plan, spacing or retrieval schedule, teaching-test evidence, source currentness, edition, or evaluation result changes. Support-map entry: open `Architecture and Narrative Work Bridge` when the learning route narrates architecture, copies source architecture as course architecture, uses views, source spine, or actual-structure feedback; open `Semiotic And Language-Precision Bridge` when didactic coarsening, cue or backoff, explanation, style, or language-state choice matters; open `Source Use And Refresh Map` when teaching, memory, cognition, interleaving, spacing, or learner-test source support changes; use the refresh route when learner telemetry changes.

## [[NSTD/22_08_Design a Narrative Learning Route for Reconstruction and Use/00_NSTD.08 - Design a Narrative Learning Route for Reconstruction and Use|NSTD.8]]:End
