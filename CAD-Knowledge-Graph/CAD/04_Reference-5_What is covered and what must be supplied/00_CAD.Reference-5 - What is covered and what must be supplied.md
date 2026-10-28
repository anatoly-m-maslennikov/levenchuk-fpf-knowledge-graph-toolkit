---
type: "cad-section"
context:
  - "CAD"
page_type: "cad-section"
mode: "canonical-generated"
cad_id: "CAD.Reference:5"
title: "What is covered and what must be supplied"
part: "[[00_Hubs/CAD - Control Architecture Design Architectural Reference]]"
parents:
  - "[[00_Hubs/CAD - Control Architecture Design Architectural Reference]]"
source_file: "CONTROL-ARCHITECTURE-DESIGN-PRINCIPLES-FRAMEWORK.md"
source_revision: "fb3b6a4ad1d51d732a365f75f7d68337c7a751e2"
source_sha256: "72d4c479741c828c7df8b70874ece00756a0e3d377f69f7f1d89f3fbe21704e7"
generated_on: "2026-10-25"
source_lines:
  - 265
  - 274
status: "generated"
generated: true
---


The first quantitative use needs a usable plant model, initial conditions, uncertainty sets, candidate channels and delivery conditions, a specified feedback law or finite family, required state/input limits, and a control objective. [[CAD/09_05_Choose Observations and Internal State for Control/00_CAD.05 - Choose Observations and Internal State for Control|CAD.5]] develops information and action constructions for that class. [[CAD/10_01_Derive a Control Decomposition from the Whole Problem/00_CAD.01 - Derive a Control Decomposition from the Whole Problem|CAD.1]]–[[CAD/13_04_Co-design and Realize the Whole Control Architecture/00_CAD.04 - Co-design and Realize the Whole Control Architecture|CAD.4]] add planning models, command reconstruction, error sets, joint constraints and execution choices when their assumptions fit.

The methods do not promise arbitrary nonlinear or learned-controller synthesis, identification of an unknown plant, security of a communication channel, or certification of a physical installation. Those are real neighboring tasks: an unsupported disturbance envelope or an unbounded communication delay can defeat a mathematically correct conclusion here. Obtain the missing model or guarantee, restrict the intended use, or retain the negative result. The separate continuous-time branch in [[CAD/12_03_Construct a Jointly Admissible Command Domain/00_CAD.03 - Construct a Jointly Admissible Command Domain|CAD.3]]:4.5 needs its stated derivative, Lipschitz and forward-containment premises; sampled constraints do not establish intersample safety.

A proposed architecture, a mathematically qualified model and a physically qualified implementation support different claims. The practitioner should be able to answer which observation times and executed inputs were used, which error bound holds over the allowed run, which one action works for all compatible states, what preserves continuation, and how computation realizes those conditions. The full patterns supply these tests; the questions here do not replace their derivations.

The examples favor transparent linear calculations and explicitly bounded uncertainties. Exact sets can be expensive and outer sets conservative. A stochastic expected-cost task may justify a different estimator and schedule; [[CAD/09_05_Choose Observations and Internal State for Control/00_CAD.05 - Choose Observations and Internal State for Control|CAD.5]]:11 compares that alternative. An unqualified biological analogy or a component score cannot replace the chosen model and control criterion.
