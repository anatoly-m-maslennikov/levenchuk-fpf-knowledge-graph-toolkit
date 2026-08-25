---
type: "npf-pattern"
context:
  - "NPF"
page_type: "npf-pattern"
mode: "canonical-generated"
npf_id: "NSTD.4"
title: "Voice, Focalization, and Agency"
part: "[[00_Hubs/NPF - Preface - Cross-Cutting Ideas And Principles]]"
parents:
  - "[[00_Hubs/NPF - Preface - Cross-Cutting Ideas And Principles]]"
source_file: "Narrativization-and-Narrative-Studies-Principles-Framework.md"
source_revision: "d77339d7056433de3ee55ad863860ee4b3006f6f"
source_sha256: "80f2d5ec3524b7947a3c36928bf774f61a9c68d4efc9ec5fc0d23206f01534e4"
generated_on: "2026-08-26"
source_lines:
  - 959
  - 1214
status: "generated"
generated: true
---


> **Type:** DPF pattern body

> **Primary EntityOfConcern:** `NarrativeViewpointAgencyDiscipline@Context`, a DPF-local record for one viewpoint and agency treatment.

## [[NSTD/03_04_Voice, Focalization, and Agency/00_NSTD.04 - Voice, Focalization, and Agency|NSTD.4]]:1 - Problem frame

Use this pattern when narrator, voice, viewpoint, focalized object, protagonist, actant, personification, or agency treatment changes what a reader understands, remembers, trusts, blames, or treats as capable of action.

First useful move: state viewpoint or focalized object, what it reveals, what it hides, and whether any source bearer is being personified or treated as an actor.

What goes wrong if missed: viewpoint looks like style while it changes source visibility and responsibility assignment. A structure, institution, model, or document can be written as if it decided, wanted, knew, or authorized.

What this buys: the narrative can use viewpoint and protagonist design without smuggling agency, capability, responsibility, or moral permission.

## [[NSTD/03_04_Voice, Focalization, and Agency/00_NSTD.04 - Voice, Focalization, and Agency|NSTD.4]]:2 - Problem

Narratology terms such as voice, focalization, protagonist, and actant are useful because they describe how narrative directs attention. But FPF cannot let those terms replace role, assignment, capability, responsibility, evidence, or ethics owners.

## [[NSTD/03_04_Voice, Focalization, and Agency/00_NSTD.04 - Voice, Focalization, and Agency|NSTD.4]]:3 - Forces

| Force | Tension |
| --- | --- |
| Reader orientation vs ontological discipline | A focalized object helps readers, but it may not be an actor. |
| Storycraft roles vs FPF roles | Protagonist and actant are narrative functions, not `U.Role` by default. |
| Personification vs responsibility | Personification can teach, but responsibility and moral standing need direct owners. |
| Future agency profile vs current owner | `C.9` is planned, so current agency work must not rely on it operationally. |

## [[NSTD/03_04_Voice, Focalization, and Agency/00_NSTD.04 - Voice, Focalization, and Agency|NSTD.4]]:4 - Solution

Create a viewpoint and agency discipline record when viewpoint is load-bearing.

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

Operational owner rules:

1. Use `A.13` for agential participation and agency spectrum when current.
2. Use `A.2` and `A.2.1` for role values and role assignments.
3. Use `A.2.2` for capability.
4. Use `D.1` through `D.5` for value, harm, conflict, bias, responsibility, and assurance-facing ethics claims.
5. Use `A.19.ECS` and `C.16` for any local agency characteristic or evaluation scale.
6. Mention `C.9` only as planned and non-operational until admitted.

Review viewpoint in four passes.

| Pass | What to inspect | Repair if failed |
| --- | --- | --- |
| Reveal or hide pass | What source structures become visible or invisible because of this viewpoint? | Add hidden-structure note, source-return link, or alternate viewpoint. |
| Function and kind pass | Is protagonist, actant, narrator, voice, or focalized object being treated as an FPF role, agent, capability, or responsibility bearer? | Split narrative function from FPF owner claim. |
| Literalization pass | Which personifications would become false if read literally? | Mark metaphor or personification, lower wording, or name the literal owner. |
| Affected-party pass | Does the viewpoint erase harmed parties, dissenting roles, uncertainty, or downstream reliance pressure? | Route to `D.1` through `D.5`, add counter-viewpoint, or block downstream use. |

Use narrative-function terms positively, but only inside their lane.

| Narrative function | Useful for | Not enough for |
| --- | --- | --- |
| Protagonist | Centering attention or action path. | Responsibility, role assignment, moral standing, or capability. |
| Actant | Describing function in a plot or transformation. | `U.Role`, `U.RoleAssignment`, or method ownership. |
| Voice | Controlling stance, distance, confidence, or witness posture. | Evidence strength, source authority, or ethical permission. |
| Focalization | Selecting what the reader sees and from whose constraints. | Completeness, neutrality, or source truth. |
| Personification | Teaching or memory aid for abstract structures. | Actual agency, decision authority, or intent. |

When a phrase has both narrative value and ontological risk, keep the phrase only if the record states the safe reading. "The architecture wants fewer dependencies" may be safe in a teaching aside if the same passage says that architects choose structures to reduce dependency under stated characteristics. It is unsafe when the sentence becomes decision rationale, blame assignment, or evidence of system behavior.

The strongest repair is often not deletion. Good narrative sometimes needs viewpoint and personification. Repair by adding the missing owner split: who actually decides, which structure is being highlighted, what is hidden, which source should be returned to, and which moral or work claim is not being made.

## [[NSTD/03_04_Voice, Focalization, and Agency/00_NSTD.04 - Voice, Focalization, and Agency|NSTD.4]]:5 - Archetypal Grounding

### Mature worked slice: viewpoint without false agency

An architecture explanation says: "The database wants to protect consistency, while the service wants speed." This can be a useful teaching viewpoint, but literal reading creates false agency and hides the real owners: architecture decision, component responsibility, consistency requirement, latency requirement, and trade-off.

```text
NarrativeViewpointRecord@ArchitecturePersonification:
  narrativeRenderingRef: ArchitectureExplanation@v1
  viewpointOrVoiceKind: didactic personification
  focalizedSourceStructureRef: consistency and latency trade-off across selected architecture structures
  narrativeFunction: make the trade-off memorable and traversable
  hiddenOrWeakenedSourceStructureRefs: actual component responsibility, decision record, measured characteristics
  agencyOrResponsibilityRisk: component metaphor may be read as actor agency or authority
  literalizationRepair: lower "wants" to "is treated as protecting" or name the real owner
  sourceReturnCondition: return to architecture description and decision record for authority
```

Before:

> The database refuses to let the service move fast.

After:

> In this teaching view, we personify the consistency boundary as the part that "pushes back." Literally, the owner is the architecture decision: consistency is protected by transaction and replication choices, and the service latency trade-off returns to the decision record and later telemetry.

This repair keeps the narrative value while protecting ontology. The viewpoint is a lens over selected source structures, not a new actor.

### Mature worked slice: narrator and reader roles

A narrative rendering about a future project can speak from the viewpoint of "the future user". That may help the team notice consequences, but the imagined user is not evidence and not an affected-party consultation. [[NSTD/03_04_Voice, Focalization, and Agency/00_NSTD.04 - Voice, Focalization, and Agency|NSTD.4]] requires the narrative worker to state the role boundary:

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

### Viewpoint repair ladder

1. **Keep as ordinary style** when the phrase is clearly not claim-bearing and no reader use depends on it.
2. **Mark as viewpoint** when it helps attention but could be mistaken for source structure.
3. **Lower the wording** when metaphor or focalization implies agency, evidence, certainty, or responsibility.
4. **Name the literal owner** when architecture, evidence, ethics, work, decision, or assurance authority is touched.
5. **Reject the move** when the viewpoint works only by hiding a source constraint or affected-party boundary.

### Calibration for viewpoint quality

| Value | Viewpoint condition |
| --- | --- |
| `2` | Voice or focalization is effective, but agency, responsibility, evidence, or source visibility can be misread. |
| `3` | Viewpoint function is named, but literalization repair is incomplete. |
| `4` | Viewpoint, source structure, hidden structures, and owner exits are recoverable for one declared use. |
| `5` | A reader can shift viewpoint or remove the metaphor and still recover the same source structure and owner routing. |

### FPF owner teaching

[[NSTD/03_04_Voice, Focalization, and Agency/00_NSTD.04 - Voice, Focalization, and Agency|NSTD.4]] makes the parallel with architecture views explicit for narrators. A viewpoint selects and highlights structure for a use. It is valuable for attention, but it does not create a new `U.Role`, `U.RoleAssignment`, responsibility bearer, evidence source, or decision authority. The narrative vocabulary may say narrator, focalization, protagonist, actant, or voice; FPF keeps asking which owner carries the claim if the wording becomes load-bearing.

A technical story says "the architecture wants to reduce coupling." [[NSTD/03_04_Voice, Focalization, and Agency/00_NSTD.04 - Voice, Focalization, and Agency|NSTD.4]] repairs this as personification for reader orientation. The source structure is an architecture candidate with coupling and cohesion characteristics. The architecture is not an agent and has no responsibility. The actor may be an architect role assignment, and the decision or method claim goes to its direct owner.

In a franchise storycraft case, the protagonist may be the center of narrative attention while agency discipline asks whether the character's action is supported by admitted canon, premise constraints, and causal plot support. "The Force guided the decision" may be a story-world explanation, but it is not a license to skip character motivation, source constraints, or responsibility language when the case is used as a DPF probe.

In a homotopy explanation, a space, path, or loop may be written as if it "wants" to deform or "remembers" a hole. That can help intuition, but the focalized object is not an agent. The repair is to state the formal relation being highlighted and where the personification stops.

In live commentary, viewpoint may follow one player, coach, or tactical unit. That can make the stream intelligible, but it may hide off-ball actions, referee uncertainty, or later official correction. The commentary record needs the hidden-structure note before blame or capability claims are treated as stable.

Use a literalization rewrite ladder.

| Risky phrase | Safe if read as | Repair if literal reading would be false |
| --- | --- | --- |
| "The architecture wants..." | Shorthand for a selected quality pressure. | Name the architect, decision, characteristic, or trade-off owner. |
| "The paper proves..." | Shorthand for a source claim inside the paper. | Name proof status, evidence owner, or author claim. |
| "The model knows..." | Shorthand for model output behavior. | Name the training-data claim, admitted source basis claim, or method claim and admission boundary. |
| "The protagonist represents the system..." | Reader-facing focalization. | State which source structures the protagonist highlights and hides. |
| "The market punished..." | Aggregate outcome narrative. | Name actual actors, mechanism uncertainty, evidence owner, or lower the claim. |

When the phrase is kept for readability, put the safe reading close enough that a reader will not need a hidden glossary. "The architecture wants fewer dependencies" can be followed by "more precisely, the selected architecture characteristic rewards fewer dependency edges under this trade-off." If that clarification ruins the passage, the passage was probably carrying more authority than the source supports.

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

The practitioner should be able to fill at least a compact version of this record before using strong agency language. If the record feels too heavy for the use, lower the language: use "is presented as", "the route follows", "the example highlights", or "the story treats" rather than "decides", "knows", "forces", or "is responsible".

## [[NSTD/03_04_Voice, Focalization, and Agency/00_NSTD.04 - Voice, Focalization, and Agency|NSTD.4]]:6 - Bias-Annotation

This pattern blocks story-function agency drift: protagonist, actant, focalized object, voice, or personification is read as role assignment, capability, responsibility, or moral standing. Repair by splitting narrative function from current FPF owners for agency, role, capability, responsibility, ethics, evidence, and assurance claims. Scope: DPF-local for viewpoint and agency treatment in narrative renderings; it does not create a new agency ontology.

## [[NSTD/03_04_Voice, Focalization, and Agency/00_NSTD.04 - Voice, Focalization, and Agency|NSTD.4]]:7 - Conformance Checklist

| Check | Passing condition |
| --- | --- |
| `CC-NSTD4-1` | Viewpoint, voice, focalized object, or protagonist choice is named when load-bearing. |
| `CC-NSTD4-2` | Revealed and hidden source structures are explicit. |
| `CC-NSTD4-3` | Protagonist, actant, and focalized object remain narrative functions unless direct owner admits role, assignment, agency, capability, or responsibility. |
| `CC-NSTD4-4` | `C.9` is not used as an operational owner while planned only. |
| `CC-NSTD4-5` | Personification has a repair route: literal owner, lowered wording, or source-return note. |

## [[NSTD/03_04_Voice, Focalization, and Agency/00_NSTD.04 - Voice, Focalization, and Agency|NSTD.4]]:8 - Common Anti-Patterns and How to Avoid Them

| Anti-pattern | What fails | Repair |
| --- | --- | --- |
| Protagonist as responsible agent | Narrative centrality becomes moral or operational responsibility. | Split protagonist function from `A.13`, `A.2.1`, and ethics owner claims. |
| Episteme as actor | A paper, standard, pattern, or model "decides" or "knows". | Rewrite as source-use, evidence, method description, or author work through direct owners. |
| Viewpoint hides harmed party | A compelling viewpoint erases affected parties. | Route to `D.1` through `D.5` and add a source-return or viewpoint correction. |

## [[NSTD/03_04_Voice, Focalization, and Agency/00_NSTD.04 - Voice, Focalization, and Agency|NSTD.4]]:9 - Consequences

The benefit is that storycraft remains available without agency inflation. The cost is that some memorable phrases need repair or explicit personification status.

## [[NSTD/03_04_Voice, Focalization, and Agency/00_NSTD.04 - Voice, Focalization, and Agency|NSTD.4]]:10 - Rationale

Narrative voice and focalization are not decorative only. They shape source visibility and responsibility cues. FPF therefore treats them as source-structure rendering choices that may trigger role, agency, capability, ethics, evidence, or assurance owners.

## [[NSTD/03_04_Voice, Focalization, and Agency/00_NSTD.04 - Voice, Focalization, and Agency|NSTD.4]]:11 - SoTA-Echoing

Schmid's `Narratology: An Introduction` and Chihaia's `Introductions to Narratology: Theory, Practice and the Afterlife of Structuralism` supply voice, focalization, actant, and perspective vocabulary as narrative-function language; Chen and Xu's "Neural and Behavioral Evidence for Differential Processing of Narrative Perspective in Novel Reading" gives current support that perspective can change processing; Nguyen-Trung and Nguyen's "Narrative-Integrated Thematic Analysis" keeps LLM-assisted narrative analysis tied to human interpretive agency. The DPF adopts the attentional and perspective value, while rejecting any automatic agency or responsibility import.

Operational payload:

- From narratology, voice, focalization, protagonist, and actant are useful because they locate attention and function inside a narrative. [[NSTD/03_04_Voice, Focalization, and Agency/00_NSTD.04 - Voice, Focalization, and Agency|NSTD.4]] keeps them as narrative functions unless another FPF owner admits a stronger claim.
- From perspective-processing evidence, viewpoint can change what readers process and remember. It is not ornamental. The pattern therefore requires revealed and hidden source structures.
- From LLM-assisted narrative analysis, machine-suggested themes or viewpoints do not remove human interpretive responsibility. Tool-mediated viewpoint choices need admission and human owner routing.
- From FPF agency and role patterns, narrative centrality is not role assignment. A character, model, architecture, organization, or source can be focalized without becoming an agent.
- From ethics patterns, viewpoint can erase affected parties. When harm, blame, policy, or responsibility is live, a single compelling viewpoint is insufficient.

The practical consequence is that viewpoint is both a design tool and a risk locus. It earns its place by revealing needed source structure and naming what it hides.

## [[NSTD/03_04_Voice, Focalization, and Agency/00_NSTD.04 - Voice, Focalization, and Agency|NSTD.4]]:12 - Relations

Uses `A.6.3.NAR`, `A.13`, `A.2`, `A.2.1`, `A.2.2`, `A.19.ECS`, `C.16`, `D.1` through `D.5`, `A.10`, `B.3`, and `G.11`. Reopen when viewpoint changes source visibility or when new source-pack or FPF agency owners change the owner map. Support-map entry: open `Architecture and Narrative Work Bridge` when viewpoint or focalization is really an architecture view and viewpoint over selected structures; open `Semiotic And Language-Precision Bridge` when voice, focalization, salience, sign, or language-state choice changes interpretation; open `DPF Precision Restoration And Owner Map` when protagonist, actant, agency, personification, or responsibility wording needs owner split.

## [[NSTD/03_04_Voice, Focalization, and Agency/00_NSTD.04 - Voice, Focalization, and Agency|NSTD.4]]:End
