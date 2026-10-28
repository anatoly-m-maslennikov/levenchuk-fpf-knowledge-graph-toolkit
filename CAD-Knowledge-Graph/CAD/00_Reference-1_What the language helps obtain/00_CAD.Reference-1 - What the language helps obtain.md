---
type: "cad-section"
context:
  - "CAD"
page_type: "cad-section"
mode: "canonical-generated"
cad_id: "CAD.Reference:1"
title: "What the language helps obtain"
part: "[[00_Hubs/CAD - Control Architecture Design Architectural Reference]]"
parents:
  - "[[00_Hubs/CAD - Control Architecture Design Architectural Reference]]"
source_file: "CONTROL-ARCHITECTURE-DESIGN-PRINCIPLES-FRAMEWORK.md"
source_revision: "fb3b6a4ad1d51d732a365f75f7d68337c7a751e2"
source_sha256: "72d4c479741c828c7df8b70874ece00756a0e3d377f69f7f1d89f3fbe21704e7"
generated_on: "2026-10-25"
source_lines:
  - 70
  - 83
status: "generated"
generated: true
---


A controller acts on information that can be partial, old or costly to obtain. Its chosen action must affect the plant before another decision is due, fit the available actuation and leave an acceptable continuation. When planning and feedback are separated, their different models and time scales add another coupling: an attractive nominal command may be impossible for the lower loop to realize.

The useful result is a control architecture whose information, command meanings, error allowances and execution conditions are mutually consistent for the required task. The result may instead be a reasoned rejection: no tested realization fits, a sufficient enclosure is too coarse, or indistinguishable states make the required action impossible. These conclusions call for different next work.

There are two directly useful branches. [[CAD/09_05_Choose Observations and Internal State for Control/00_CAD.05 - Choose Observations and Internal State for Control|CAD.5]] constructs the information available to a specified controller. [[CAD/10_01_Derive a Control Decomposition from the Whole Problem/00_CAD.01 - Derive a Control Decomposition from the Whole Problem|CAD.1]]–[[CAD/13_04_Co-design and Realize the Whole Control Architecture/00_CAD.04 - Co-design and Realize the Whole Control Architecture|CAD.4]] develop a planning-and-feedback arrangement when separation has a useful reason. Their quantitative results connect where an estimate, command or timing claim is actually used. The language does not require every design to use both branches.

Its recurring tensions are concrete. A precise delayed sensor leaves recent disturbances unknown. A larger model can reduce modeling error while missing the deadline. A gain that reduces tracking error can consume more input authority. Conservative sets can protect a guarantee while excluding a useful design. All of these must be judged against the same task; a smaller isolated error measure is not automatically a better control result.

FPF C.43 supplies the common Method for connecting observation, choice and action in ongoing control. Apply it when the available assessment, alternatives and execution conditions still need to become one coherent continuation; an adequate architecture can remain unchanged. CAD specializes the engineering construction of the information, command and timing relations. Its state sets, error bounds and feasible commands give quantitative answers under declared models; they do not by themselves settle the legitimacy of a goal, the economics of competing resource uses or a developing subject's next worthwhile problem. Conversely, a common control mantra does not replace these calculations. A changed information delay returns to [[CAD/09_05_Choose Observations and Internal State for Control/00_CAD.05 - Choose Observations and Internal State for Control|CAD.5]] and its dependent bounds; an unavailable correction can reopen [[CAD/12_03_Construct a Jointly Admissible Command Domain/00_CAD.03 - Construct a Jointly Admissible Command Domain|CAD.3]] or the architecture choice; a changed goal first changes the task against which those results are used.

FPF C.43:4.5.1 also supplies the common construction of required temporal relations without imposing a periodic schedule. [[CAD/11_02_Construct the Planning and Feedback Interface/00_CAD.02 - Construct the Planning and Feedback Interface|CAD.2]] makes that construction executable through event ordering, behavior between updates and reset rules; [[CAD/09_05_Choose Observations and Internal State for Control/00_CAD.05 - Choose Observations and Internal State for Control|CAD.5]] preserves sample phase, information age and observation gaps, and [[CAD/13_04_Co-design and Realize the Whole Control Architecture/00_CAD.04 - Co-design and Realize the Whole Control Architecture|CAD.4]] qualifies the shared implementation schedule. An action can vary its timing while another required contribution continues, provided their joint resource and dynamic conditions still hold. Changing one of these relations reopens the dependent calculation; equal update frequencies alone do not preserve it.
