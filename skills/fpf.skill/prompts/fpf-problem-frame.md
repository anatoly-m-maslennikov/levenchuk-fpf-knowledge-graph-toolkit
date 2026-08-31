# FPF Problem Frame

Produce a read-only **Problem Frame Record**. Stop at the earliest honest problem-side result; do not generate options, select a solution, or authorize work.

## Resolve scope and sources

1. Resolve the observed difficulty, Entity of Concern, affected user or system, bounded context, receiving use, available evidence, authority, and current language state.
2. Use graph-declared `C.22.2` as the primary problem-card method and `C.22` for task typing. Use task-profile bindings only to specialize the subject; they do not predetermine that a problem exists.
3. If the input is still only a cue, preserve it as such and return the missing discriminator. Do not force a cue, preference, solution idea, or implementation request into a completed problem statement.

## Framing workflow

1. Separate observations, adverse or unresolved relations, stakeholder interpretations, constraints, desired effects, and proposed solutions.
2. State the smallest task family and TaskSignature adequate for the receiving use: subject, transformation or judgement sought, inputs, result kind, constraints, evidence needs, and exclusions.
3. Test whether an actual problem claim is supportable for the named affected subject and use. Preserve conflicting interpretations and unsupported causal claims.
4. Define the acceptance boundary for the problem statement itself: what must be known before option generation, design, implementation, or evaluation can begin.
5. Stop at one accepted bounded problem statement, a narrower inquiry question, a preserved cue pack, or an exact blocker.

## Boundaries

- Do not smuggle a preferred solution into the problem definition.
- Do not treat urgency, stakeholder rank, a project label, or an existing ticket as proof that the framed problem obtains.
- Do not invent requirements, acceptance criteria, authority, evidence, or causal support.
- Remain read-only unless the user separately authorizes changes outside this analytical result.

## Native result requirements

1. **Observed situation, receiving use, and resolved FPF source**
2. **TaskSignature and task-family assignment**
3. **Problem-side result** — accepted problem statement, inquiry question, preserved cue, or blocker
4. **Constraints, distinctions, evidence, and exclusions**
5. **Acceptance boundary and exact next admissible step**

Do not return a solution proposal, option ranking, implementation plan, or project authorization.
