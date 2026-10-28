---
type: "cad-section"
context:
  - "CAD"
page_type: "cad-section"
mode: "canonical-generated"
cad_id: "CAD.Reference:7"
title: "Sources, external suppliers and consequential change"
part: "[[00_Hubs/CAD - Control Architecture Design Architectural Reference]]"
parents:
  - "[[00_Hubs/CAD - Control Architecture Design Architectural Reference]]"
source_file: "CONTROL-ARCHITECTURE-DESIGN-PRINCIPLES-FRAMEWORK.md"
source_revision: "fb3b6a4ad1d51d732a365f75f7d68337c7a751e2"
source_sha256: "72d4c479741c828c7df8b70874ece00756a0e3d377f69f7f1d89f3fbe21704e7"
generated_on: "2026-10-25"
source_lines:
  - 285
  - 303
status: "generated"
generated: true
---


The full source comparisons belong with the affected Methods. [[CAD/09_05_Choose Observations and Internal State for Control/00_CAD.05 - Choose Observations and Internal State for Control|CAD.5]]:11 distinguishes the historical diversity-enabled sweet-spot model, internal prediction and applied-action feedback, bounded-set estimation and stochastic sensor scheduling. DeSS compares complementary components under a task and resource model; IFP concerns a controller's reuse of internal information. Neither establishes the other. The selected bounded-set construction is used because the stated task asks for hard sampled constraints, not because it is universally superior.

[[CAD/10_01_Derive a Control Decomposition from the Whole Problem/00_CAD.01 - Derive a Control Decomposition from the Whole Problem|CAD.1]]–[[CAD/13_04_Co-design and Realize the Whole Control Architecture/00_CAD.04 - Co-design and Realize the Whole Control Architecture|CAD.4]]:11 compare decomposition, reduced-model interfaces, invariant margins, governors, safety filters, inexact computation and switching under their different conditions. A reference governor can preserve a qualified loop; a safety filter changes the applied control law and therefore the error calculation; separate stable switching modes do not establish a common invariant domain. A more recent result matters when it changes the usable construction or comparison, not merely because it has a later date.

| External supplying publication | Contribution used here | Receiving use and return |
| --- | --- | --- |
| [FPF Core](https://github.com/ailev/FPF/blob/main/FPF-Spec.md), C.32.LCA | General construction of complete control-architecture alternatives and their joint conditions | CAD supplies the specialized numerical constructions. A changed general architecture requirement reopens the affected framing, not an unchanged algebraic identity. |
| FPF Core, C.30.LCA | Adequacy of a control-structure view | A view must expose the information, authority, timing and lower guarantees needed for its use. Its adequacy does not prove a control bound. |
| FPF Core, A.3.3.PI | Retaining information needed by future prediction and update | [[CAD/09_05_Choose Observations and Internal State for Control/00_CAD.05 - Choose Observations and Internal State for Control]] constructs a particular sufficient internal state and explains what a reduction must preserve. |
| FPF Core, C.39 and C.32 | Construction of useful connected ways and whole architecture alternatives | [[CAD/10_01_Derive a Control Decomposition from the Whole Problem/00_CAD.01 - Derive a Control Decomposition from the Whole Problem]] and [[CAD/13_04_Co-design and Realize the Whole Control Architecture/00_CAD.04 - Co-design and Realize the Whole Control Architecture]] use those general operations with control-specific models, alternatives and constraints. |
| [Systems Engineering DPF](https://github.com/ailev/FPF/blob/main/DPFs/Engineering%20DPF%20Suite/SYSTEMS-ENGINEERING-PRINCIPLES-FRAMEWORK.md), SYSE.5 and SYSE.6 | Functional organization, bearer alternatives and the system architecture decision | CAD results can supply that wider work. Control feasibility neither chooses every system bearer nor settles the whole project. |
| [Mathematical Modeling DPF](https://github.com/ailev/FPF/blob/main/DPFs/Foundational%20Thinking%20DPF%20Suite/MATHEMATICAL-MODELING-PRACTICE-DPF.md), MMP.9, MMP.18 and MMP.22 | Model reduction, compatible coupled models, and transformation of mathematical operations into workable performance | [[CAD/10_01_Derive a Control Decomposition from the Whole Problem/00_CAD.01 - Derive a Control Decomposition from the Whole Problem]]–[[CAD/13_04_Co-design and Realize the Whole Control Architecture/00_CAD.04 - Co-design and Realize the Whole Control Architecture]] provide the control-specific receiving operations. A changed model exchange or computational realization reopens the error or deadline premise that uses it. |

These remain external contributions. Core does not require this DPF for its own applications. Select an obtainable edition of a supplying publication and the exact relied-on content before applying it; a locator or title alone is not that content. If a relied-on premise changes, revisit its receiving use. If only the carrier or publication date changes, inspect compatibility rather than assuming either breakage or preservation.

For the domain construction, a changed plant, measurement model, uncertainty, command objective, admitted switching, timing or resource arrangement reopens the dependent calculation. A source correction reopens the particular claim imported from it. Unchanged information, interface or model results remain usable under their original conditions.
