---
type: "fpf-section"
context:
  - "FPF"
page_type: "fpf-section"
mode: "canonical-generated"
fpf_id: "FPF.Reference:5"
title: "Local Closure Inside An Open World"
part: "[[00_Hubs/FPF - First Principles Framework Architectural Reference (non-normative)]]"
parents:
  - "[[00_Hubs/FPF - First Principles Framework Architectural Reference (non-normative)]]"
source_file: "FPF-Spec.md"
source_revision: "fb3b6a4ad1d51d732a365f75f7d68337c7a751e2"
source_sha256: "03e2d58f56ef5e271d6e5481a042845eb1848994c221bed7fb384311b2a1a236"
generated_on: "2026-10-25"
source_lines:
  - 1178
  - 1198
status: "generated"
generated: true
---


FPF assumes an open world. New evidence can arrive. A better mathematical model may appear. A source publication, source-use record, or telemetry relation may become stale. A competitor may change the state of the art. A user need may shift. A new concern may reveal that the same system should be described differently.

Engineering and management still need local closure. A bridge cannot wait for all possible facts. A gate decision cannot cite the entire universe. A release, experiment, procurement, safety case, or architecture review therefore defines what counts as sufficient for the next action.

The old open-world versus closed-world distinction is a useful didactic picture. In an open world, absence of proof is not proof of absence. If a name is missing from a party guest list, the list may be incomplete. In a locally closed operational world, absence from the accepted manifest matters. If a name is missing from the aircraft manifest, the airline acts as if that passenger is not on the flight.

FPF does not transform the open world into a closed one. It lets a project build small closed worlds for declared purposes:

- the exact source, scope, model-use organization, working situation, comparison basis, or other subject-defined boundary states what is current for this decision;
- an EntityOfConcern states what project entity the reasoning is about;
- a description states what can be relied on and under what relation;
- evidence and assurance state what claim is credible enough for the local use;
- a gate or decision states what boundary is crossed;
- a reopen condition states when local closure is no longer enough.

This is why FPF patterns often look strict. The strictness is local. It lets a project act while keeping the wider world open. A local closure is not a claim that nothing else exists. It is a declared scope for responsible action.

Local closure also does not license ceremony. Before a method, route, or review makes an action mandatory, ask whether a materially plausible result can change a named substantive decision within the nearest substantive horizon, whether the action realizes an already selected result, or whether removing it changes an assurance or recovery condition on which the use relies. This contribution is necessary but does not by itself make a proposed inquiry obtainable or worth requiring. Use [[A_Kernel Architecture Cluster/11_Ontological Parsimony/01_A.11.OP - Decision-Relevant Least Action and Operational Parsimony- Test a Proposed Requirement|A.11.OP]] for that screen and its boundary with direct duties and assurance. When the demand's worth remains open, [[C_Kernel Extension Specifications/02_11_Decision Theory (Decsn-CAL)/03_C.11.DUA - Make Advice and Evidence Demands Worth Their Burden|C.11.DUA]] compares its attainable contribution and whole burden; a current local choice uses [[C_Kernel Extension Specifications/02_11_Decision Theory (Decsn-CAL)/00_C.11 - Decision Theory (Decsn-CAL)|C.11]]. The result can be a qualified answer on the present basis.
