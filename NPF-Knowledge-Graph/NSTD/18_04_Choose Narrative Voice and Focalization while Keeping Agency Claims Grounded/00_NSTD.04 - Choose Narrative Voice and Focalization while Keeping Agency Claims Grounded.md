---
type: "npf-pattern"
context:
  - "NPF"
page_type: "npf-pattern"
mode: "canonical-generated"
npf_id: "NSTD.4"
title: "Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded"
part: "[[00_Hubs/NPF - Patterns]]"
parents:
  - "[[00_Hubs/NPF - Patterns]]"
source_file: "Narrativization-and-Narrative-Studies-Principles-Framework.md"
source_revision: "fb3b6a4ad1d51d732a365f75f7d68337c7a751e2"
source_sha256: "c5c274316d31db178d105526ee32e912c4ccd02a6c03279a42f83244612737ba"
generated_on: "2026-10-25"
source_lines:
  - 1325
  - 1576
status: "Stable"
uses:
  - "A.10"
  - "A.13"
  - "A.19.ECS"
  - "A.2"
  - "A.2.1"
  - "A.2.2"
  - "A.6.3.NAR"
  - "B.3"
  - "C.16"
  - "D.1"
  - "D.5"
  - "G.11"
  - "[[NSTD/10_Reference-11_Working meanings and direct source returns/00_NSTD.Reference-11 - Working meanings and direct source returns|NSTD.Reference:11]]"
generated: true
---


> **Status:** Stable

> **Type:** DPF pattern body

> **Primary EntityOfConcern:** choosing and repairing narrative voice and viewpoint so that the reader can recover the relevant events, participants and responsibilities.

## [[NSTD/18_04_Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded/00_NSTD.04 - Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded|NSTD.4]]:1 - Problem frame

Use this pattern when narrator, voice, viewpoint, focalized object, protagonist, actant, personification, or agency treatment changes what a reader understands, remembers, trusts, blames, or treats as capable of action.

First useful move: state viewpoint or focalized object, what it reveals, what it hides, and whether any source bearer is being personified or treated as an actor.

What goes wrong if missed: viewpoint looks like style while it changes source visibility and responsibility assignment. A structure, institution, model, or document can be written as if it decided, wanted, knew, or authorized.

What this buys: the narrative can use viewpoint and protagonist design without smuggling agency, capability, responsibility, or moral permission.

## [[NSTD/18_04_Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded/00_NSTD.04 - Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded|NSTD.4]]:2 - Problem

A narrator's position determines what can be told and how it is presented. The reader may nevertheless attribute an action, knowledge or responsibility to a participant merely because that participant is prominent in the story. Choose the viewpoint for its narrative contribution and establish any consequential attribution on its own grounds.

## [[NSTD/18_04_Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded/00_NSTD.04 - Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded|NSTD.4]]:3 - Forces

| Force | Tension |
| --- | --- |
| Reader orientation vs ontological discipline | A focalized object helps readers, but it may not be an actor. |
| Narrative function and working participant | A protagonist centers the story; a real performer, assignment or responsibility requires a separate claim. |
| Personification vs responsibility | Personification can teach, but a memorable figure does not settle who may decide or who is responsible. |


## [[NSTD/18_04_Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded/00_NSTD.04 - Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded|NSTD.4]]:4 - Solution

Compare what the chosen viewpoint makes visible with what the reader needs. Add another view or a short clarification when a consequential relation is hidden. Use the optional record below when comparing viewpoints or handing the work to another author; the clarification can otherwise stay in the narrative itself.

```text
NarrativeViewpointAgencyDiscipline@Context:
  narrativeRenderingRef:
  viewpointOrVoice:
  focalizedObjectRef:
  revealedSourceStructureRefs:
  hiddenOrWeakenedSourceStructureRefs:
  narrativeFunctionTerms:
  personificationOrAgencyWording:
  directOwnerRefs:
  blockedAgencyOverread:
  repairAction:
```

Use the following distinctions only when they change interpretation or action:

1. A **narrative function** such as narrator, protagonist or actant describes a contribution to the account. Ordinary use of “role” can retain that meaning.
2. A **real participant** may be a person, organization or technical system. When a precise classification matters, `A.2` defines a local system-role kind whose candidates are `U.System` individuals. `A.2.1` separately establishes an obtaining `U.SystemRoleAssignment`; neither a label nor prominence in a story supplies that assignment.
3. A **precise agency claim** uses `A.13`: the System, the applicable local kind and the obtaining assignment. A claimed dated Work occurrence additionally uses `A.15.1`. Ordinary explanation does not require these identities unless it asserts the corresponding facts.
4. A **capability or responsibility claim** needs its own grounds. Use `A.2.2` for capability, the applicable organizational assignment for responsibility, and `D.1` through `D.5` when value, harm or affected-party conflicts matter.
5. An **agency measurement or profile** uses the selected characteristic and scale through `A.19.ECS`, `C.16` and `A.13` when that additional claim is needed.

Consider the following questions where the viewpoint could change the reader's understanding or action.

| Pass | What to inspect | Repair if failed |
| --- | --- | --- |
| What becomes visible? | Which relevant events or relations can the reader see from this viewpoint, and which remain hidden? | Add the needed fact, source return or alternate viewpoint. |
| What attribution follows? | Does prominence in the account imply an unsupported action, capability or responsibility? | Retain the narrative function and establish or correct the separate attribution. |
| Would a literal reading mislead here? | Is there a plausible reading that changes reliance or action? | Clarify that relation or participant. Keep an unambiguous metaphor. |
| Whose consequence is missing? | Does the viewpoint conceal a relevant effect, disagreement or uncertainty? | Add the affected perspective or qualify the use. Consult `D.1`–`D.5` when a value or harm conflict needs resolution. |

The following terms answer different narrative questions. Stronger factual claims require additional grounds.

| Narrative function | Useful for | Not enough for |
| --- | --- | --- |
| Protagonist | Centering attention or action path. | Responsibility, role assignment, moral standing, or capability. |
| Actant | Describing a participant's function in a plot or transformation. | A real System's classification, assignment, capability or responsibility. |
| Voice | Controlling stance, distance, confidence, or witness posture. | Evidence strength, source authority, or ethical permission. |
| Focalization | Selecting what the reader sees and from whose constraints. | Completeness, neutrality, or source truth. |
| Personification | Teaching or memory aid for abstract structures. | Actual agency, decision authority, or intent. |

Keep ordinary metonymy when the intended reader can recover the relevant action and participant. “The paper proves the lemma” can refer to the proof it contains; it needs no invented author-work record. If “the architecture wants fewer dependencies” would instead be used to justify a decision or assign blame, state the actual structural constraint, choice and responsible participant. Clarify the action-changing ambiguity, not every figurative verb.

A useful repair can retain the viewpoint while making the needed relation explicit: who decides, what structure is highlighted, what relevant fact is hidden, and where the reader can obtain it. Choose the smallest clarification that resolves the difficulty.

## [[NSTD/18_04_Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded/00_NSTD.04 - Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded|NSTD.4]]:5 - Archetypal Grounding



### [[NSTD/18_04_Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded/00_NSTD.04 - Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded|NSTD.4]]:5.1 - Worked slice: viewpoint without false agency


An architecture explanation says: “The database wants to protect consistency, while the service wants speed.” This personification can foreground a trade-off. For a reader diagnosing latency, however, the needed relation is how transaction and replication choices affect response time.

```text
NarrativeViewpointRecord@ArchitecturePersonification:
  narrativeRenderingRef: ArchitectureExplanation@v1
  viewpointOrVoiceKind: didactic personification
  focalizedSourceStructureRef: consistency and latency trade-off across selected architecture structures
  narrativeFunction: make the trade-off memorable and traversable
  hiddenOrWeakenedSourceStructureRefs: actual component responsibility, decision record, measured characteristics
  agencyOrResponsibilityRisk: component metaphor may be read as actor agency or authority
  literalizationRepair: explain the commit condition and latency consequence; identify who can change the configuration if that action is proposed
  sourceReturnCondition: return to architecture description and decision record for authority
```

Before:

> The database refuses to let the service move fast.

After:

> In this configuration the database waits for replica acknowledgement before confirming a commit. That choice protects the required consistency but increases the service's response time. To change the trade-off, consult the configuration decision and measured latency; the personification only helped introduce it.

This repair keeps the narrative value while protecting ontology. The viewpoint is a lens over selected source structures, not a new actor.



### [[NSTD/18_04_Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded/00_NSTD.04 - Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded|NSTD.4]]:5.2 - Worked slice: narrator and reader roles


A future-project scenario can speak from an imagined user's viewpoint to expose possible consequences. Describe it as a scenario so readers can distinguish the proposed experience from an actual user's report or consultation. For example:

```text
NarrativeViewpointRecord@FutureUserScenario:
  viewpointOrVoiceKind: prospective scenario voice
  focalizedSourceStructureRef: expected use situation and system interaction
  narrativeFunction: expose usability and risk questions before design is final
  hiddenOrWeakenedSourceStructureRefs: actual user evidence, policy claim, safety claim
  agencyOrResponsibilityRisk: imagined voice is treated as real stakeholder authority
  literalizationRepair: mark as scenario hypothesis and route evidence to user research owner
  sourceReturnCondition: return to source assumptions and later evidence
```



### [[NSTD/18_04_Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded/00_NSTD.04 - Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded|NSTD.4]]:5.3 - Choosing a viewpoint repair


Keep wording that already makes the relevant action clear. If a viewpoint hides a needed relation, add that relation, change perspective or name the responsible participant. Mark a scenario or metaphor when the reader could otherwise rely on it as an observation. Replace the device if its effect depends on concealing a fact needed for the intended use.

To compare alternatives, try a short literal account or another viewpoint and ask what the reader can now recover. For the database case, the comparison is whether the reader can explain the wait and locate the configurable choice. For the future-user case, it is whether the reader distinguishes a proposed experience from observed user evidence. Use [[NSTD/20_06_Declared-Use Narrative Rendering Quality Evaluation/00_NSTD.06 - Declared-Use Narrative Rendering Quality Evaluation|NSTD.6]] when a declared quality result is needed; these diagnostic questions are not a second ordinal scale.



### [[NSTD/18_04_Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded/00_NSTD.04 - Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded|NSTD.4]]:5.4 - FPF owner teaching


Viewpoint selects and highlights structure for a use. An architect's view, a narrator's voice and a protagonist's function can help recover different aspects of the same case. When a real agency, assignment, capability or responsibility claim matters, recover that claim separately under its applicable definition.

A technical story says “the architecture wants to reduce coupling.” The useful content may be a criterion favoring fewer dependencies under a stated trade-off. An architect or team makes the choice; a system-role assignment is a relation involving that participant, not the participant itself. An architecture decision records or expresses the choice rather than acting as its maker.

In a franchise continuation, a protagonist centers attention, while the chosen premises determine what action is plausible. “The Force guided the decision” may be a sufficient story-world explanation in one scene and leave a character's motivation unclear in another. Use the intended plot and reader effect to decide whether another connection is needed.

In a homotopy explanation, a space, path, or loop may be written as if it "wants" to deform or "remembers" a hole. That can help intuition, but the focalized object is not an agent. The repair is to state the formal relation being highlighted and where the personification stops.

In live commentary, viewpoint may follow one player, coach or tactical unit. This can make the stream intelligible while hiding off-ball actions or an uncertain ruling. Qualify a blame or capability claim when the unseen action or later official correction could change it; no commentary record is required merely to say so.

Use a literalization rewrite ladder.

| Risky phrase | Safe if read as | Repair if literal reading would be false |
| --- | --- | --- |
| "The architecture wants..." | Shorthand for a selected quality pressure. | State the structural criterion or trade-off; name the decision-maker if the choice or responsibility is at issue. |
| "The paper proves..." | The paper contains the claimed proof. | If proof status is disputed or conditional, identify the argument and its unresolved step or premise. |
| "The model knows..." | A shorthand whose relevant behavioral meaning is clear. | State the claimed behavior, available information or tested capability when the wording would change reliance. |
| "The protagonist represents the system..." | Reader-facing focalization. | State which source structures the protagonist highlights and hides. |
| "The market punished..." | A description of an aggregate outcome. | Describe the observed change and distinguish an established mechanism from a conjecture when the explanation affects reliance. |

Keep a necessary clarification close to the phrase. For example: “The architecture favors fewer dependencies under the selected trade-off.” If the figurative wording already conveys that relation unambiguously, no extra disclaimer is needed.

Use alternate viewpoint when one viewpoint hides a load-bearing source structure. A learner-facing story may first focalize the novice, then briefly switch to the maintainer who pays the cost of hidden coupling. A live commentary may follow the attacking player, then mark what the defensive line or official review could change. A future-scenario narrative may focalize a user, then return to the system owner for constraints and responsibility.

Filled viewpoint records:

```text
NarrativeViewpointAgencyDiscipline@ArchitecturePersonification:
  viewpointOrVoice: teacher voice using personification
  focalizedObjectRef: selected architecture candidate
  revealedSourceStructureRefs: coupling pressure; cohesion target; interface exception
  hiddenOrWeakenedSourceStructureRefs: architect role assignment; decision record; telemetry
  narrativeFunctionTerms: "architecture wants" as memory aid
  personificationOrAgencyWording: architecture described as wanting fewer dependencies
  directOwnerRefs: architect role assignment; architecture decision; characteristic evaluation
  blockedAgencyOverread: architecture is not an agent and has no responsibility
  repairAction: add "more precisely" sentence naming characteristic pressure and decision owner
```

```text
NarrativeViewpointAgencyDiscipline@FictionalProtagonistProbe:
  viewpointOrVoice: close protagonist viewpoint for private storycraft testing
  focalizedObjectRef: protagonist function in continuation route
  revealedSourceStructureRefs: character agency constraint; premise; causal plot support
  hiddenOrWeakenedSourceStructureRefs: alternative viewpoints; broader canon conflicts; publication rights
  narrativeFunctionTerms: protagonist; actant; motivation
  directOwnerRefs: source-pack and canon owner; agency and role owner when moral responsibility is claimed
  blockedAgencyOverread: protagonist centrality does not create moral permission or canon authority
  repairAction: record character action support and route rights and publication outside this DPF
```

```text
NarrativeViewpointAgencyDiscipline@LiveCommentaryView:
  viewpointOrVoice: commentator follows attacking side under time pressure
  focalizedObjectRef: attacking player or unit
  revealedSourceStructureRefs: possession, pressure, chance creation
  hiddenOrWeakenedSourceStructureRefs: defensive shape, off-ball movement, official review
  narrativeFunctionTerms: "forced", "wanted", "could not"
  directOwnerRefs: event source owner; evidence owner for claims; ethics owner if blame or harm framing appears
  blockedAgencyOverread: live focalization is not settled blame or capability assessment
  repairAction: mark provisional interpretation and later source-return route
```

Before relying on a strong agency claim, resolve the actual ambiguity in the text. A compact explanation can identify the acting system, the decision or the limited metaphor. Use a record only when its later use warrants one; lowering every verb to “is presented as” would itself obscure real actions.

## [[NSTD/18_04_Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded/00_NSTD.04 - Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded|NSTD.4]]:6 - Bias-Annotation

A vivid protagonist or personification can draw attention away from the grounds of an attribution. Compare the narrative function with the actual action, capability or responsibility being claimed, and repair only the consequential mismatch.

## [[NSTD/18_04_Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded/00_NSTD.04 - Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded|NSTD.4]]:7 - Conformance Checklist

| Check | Passing condition |
| --- | --- |
| `CC-NSTD4-1` | Viewpoint, voice, focalized object, or protagonist choice is named when load-bearing. |
| `CC-NSTD4-2` | The reader can recover the visible and hidden relations that matter for the intended use. |
| `CC-NSTD4-3` | Narrative function, real participant, local system-role kind, obtaining assignment, capability and responsibility are distinguished wherever the claim depends on them. |
| `CC-NSTD4-4` | Precise agency and Work claims use their current defining conditions; ordinary contribution wording does not require an invented assignment or Work record. |
| `CC-NSTD4-5` | A misleading personification is clarified or changed; an already clear metaphor needs no extra disclaimer. |

## [[NSTD/18_04_Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded/00_NSTD.04 - Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded|NSTD.4]]:8 - Common Anti-Patterns and How to Avoid Them

| Anti-pattern | What fails | Repair |
| --- | --- | --- |
| Protagonist as responsible agent | Narrative centrality becomes moral or operational responsibility. | Split protagonist function from `A.13`, `A.2.1`, and ethics owner claims. |
| Hidden participant | “The specification decided” leaves a consequential decision-maker unidentified. | Name the person, team or technical system that made the decision and the applicable assignment when required. Preserve harmless metonymy when the action is already clear. |
| Viewpoint hides harmed party | A compelling viewpoint erases affected parties. | Route to `D.1` through `D.5` and add a source-return or viewpoint correction. |

## [[NSTD/18_04_Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded/00_NSTD.04 - Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded|NSTD.4]]:9 - Consequences

The benefit is a usable viewpoint with clearer attribution. The cost is comparing what the viewpoint shows with what the reader needs; a short clarification may be enough.

## [[NSTD/18_04_Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded/00_NSTD.04 - Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded|NSTD.4]]:10 - Rationale

Voice and focalization change access to events, knowledge and consequences. A single viewpoint is often sufficient for a scene; an explanation or decision may need another perspective when the first conceals a relevant participant or relation.

## [[NSTD/18_04_Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded/00_NSTD.04 - Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded|NSTD.4]]:11 - SoTA-Echoing

Schmid's [Narratology: An Introduction](https://doi.org/10.1515/9783110226324) and Chihaia's [survey of introductions](https://www.diegesis.uni-wuppertal.de/index.php/diegesis/article/view/71) are historical anchors for voice, viewpoint and narratological traditions. Chen and Xu's [perspective and focalization study](https://pmc.ncbi.nlm.nih.gov/articles/PMC12937883/) (2026) found differences in reading-time and neural responses in its novel-reading tasks; it does not establish a universally better perspective. Nguyen-Trung and Nguyen's [NITA](https://doi.org/10.1080/14780887.2026.2638348) (2026) preserves the qualitative researcher's interpretive contribution. The distinction here between narrative function and actual agency is the DPF's synthesis with FPF, not a result established by those reading experiments.

For the database explanation, keeping the personification alone is a serious alternative: it is short and memorable. Adding the commit condition makes the latency consequence available for diagnosis while retaining the introduction. This is the pattern's selected combination of narrative viewpoint and explicit attribution. Its cost is a short technical clarification, justified here by the diagnostic use; purely expressive uses need a different comparison.

Use the cited traditions for their distinct contributions. Narratology supplies voice and focalization; perspective-processing studies show that viewpoint can change reading responses in the studied conditions. NITA concerns interpretation in qualitative research, not mandatory human approval of every generated story. FPF's role and agency distinctions apply when a real attribution needs to be resolved.

## [[NSTD/18_04_Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded/00_NSTD.04 - Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded|NSTD.4]]:12 - Relations

Uses `A.6.3.NAR`, `A.13`, `A.2`, `A.2.1`, `A.2.2`, `A.19.ECS`, `C.16`, `D.1` through `D.5`, `A.10`, `B.3`, and `G.11`. Reopen when viewpoint changes source visibility or when new source-pack or FPF agency owners change the owner map. Support-map entry: open `Architecture and Narrative Work Bridge` when viewpoint or focalization is really an architecture view and viewpoint over selected structures; open `Semiotic And Language-Precision Bridge` when voice, focalization, salience, sign, or language-state choice changes interpretation; open `NSTD.Reference:11 — Working meanings and direct source returns` when protagonist, actant, agency, personification, or responsibility wording needs owner split.

## [[NSTD/18_04_Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded/00_NSTD.04 - Choose Narrative Voice and Focalization while Keeping Agency Claims Grounded|NSTD.4]]:End
