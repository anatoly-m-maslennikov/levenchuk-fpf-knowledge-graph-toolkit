---
type: "fpf-knowledge-page"
context:
  - "FPF"
page_type: "fpf-knowledge-page"
mode: "canonical-generated"
title: "Local Closure Inside An Open World"
part: "[[00_Hubs/FPF - Preface (non-normative)]]"
parents:
  - "[[00_Hubs/FPF - Preface (non-normative)]]"
source_file: "FPF-Spec.md"
source_revision: "563f4c8e06a319cbd375b66cdbb2df27a5f8b9ef"
source_sha256: "c9551f2a4b52c9e57972a11552ab945f52a3522f433c54395221b16bef375ac7"
generated_on: "2026-08-26"
source_lines:
  - 859
  - 877
status: "generated"
generated: true
---


FPF assumes an open world. New evidence can arrive. A better mathematical model may appear. A source publication, source-use record, or telemetry relation may become stale. A competitor may change the state of the art. A user need may shift. A new concern may reveal that the same system should be described differently.

Engineering and management still need local closure. A bridge cannot wait for all possible facts. A gate decision cannot cite the entire universe. A release, experiment, procurement, safety case, or architecture review therefore defines what counts as sufficient for the next action.

The old open-world versus closed-world distinction is a useful didactic picture. In an open world, absence of proof is not proof of absence. If a name is missing from a party guest list, the list may be incomplete. In a locally closed operational world, absence from the accepted manifest matters. If a name is missing from the aircraft manifest, the airline acts as if that passenger is not on the flight.

FPF does not transform the open world into a closed one. It lets a project build small closed worlds for declared purposes:

- a bounded context states which meanings and invariants are current;
- an EntityOfConcern states what project entity the reasoning is about;
- a description states what can be relied on and under what relation;
- evidence and assurance state what claim is credible enough for the local use;
- a gate or decision states what boundary is crossed;
- a reopen condition states when local closure is no longer enough.

This is why FPF patterns often look strict. The strictness is local. It lets a project act while keeping the wider world open. A local closure is not a claim that nothing else exists. It is a declared scope for responsible action.
