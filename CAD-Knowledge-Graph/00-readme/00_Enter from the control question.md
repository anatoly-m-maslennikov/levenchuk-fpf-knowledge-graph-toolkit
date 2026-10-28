---
type: "cad-knowledge-page"
context:
  - "CAD"
page_type: "cad-knowledge-page"
mode: "canonical-generated"
title: "Enter from the control question"
part: "[[00_Hubs/CAD - Control Architecture Design Principles Framework Readme]]"
parents:
  - "[[00_Hubs/CAD - Control Architecture Design Principles Framework Readme]]"
source_file: "CONTROL-ARCHITECTURE-DESIGN-PRINCIPLES-FRAMEWORK.md"
source_revision: "fb3b6a4ad1d51d732a365f75f7d68337c7a751e2"
source_sha256: "72d4c479741c828c7df8b70874ece00756a0e3d377f69f7f1d89f3fbe21704e7"
generated_on: "2026-10-25"
source_lines:
  - 54
  - 67
status: "generated"
generated: true
---


| Your working difficulty | Obtain first | Direct entry |
| --- | --- | --- |
| A useful observation arrives after the action deadline, or different channels reveal different parts | An observation and memory arrangement, its error bound and the actions it permits; or a precise information limitation | [CAD.5](../CAD/09_05_Choose%20Observations%20and%20Internal%20State%20for%20Control/00_CAD.05%20-%20Choose%20Observations%20and%20Internal%20State%20for%20Control.md) |
| One calculation cannot use the needed horizon, information and execution time together | Competing decompositions and the couplings each would remove | [CAD.1](../CAD/10_01_Derive%20a%20Control%20Decomposition%20from%20the%20Whole%20Problem/00_CAD.01%20-%20Derive%20a%20Control%20Decomposition%20from%20the%20Whole%20Problem.md) |
| Planner and feedback code use a “reference” with different timing or meaning | The actual exchange and its derived error dynamics | [CAD.2](../CAD/11_02_Construct%20the%20Planning%20and%20Feedback%20Interface/00_CAD.02%20-%20Construct%20the%20Planning%20and%20Feedback%20Interface.md) |
| A stable controller cannot follow the requested command within state or actuator limits | A jointly admissible command/error domain with continuation, or a specific incompatibility | [CAD.3](../CAD/12_03_Construct%20a%20Jointly%20Admissible%20Command%20Domain/00_CAD.03%20-%20Construct%20a%20Jointly%20Admissible%20Command%20Domain.md) |
| A more accurate model, faster planner or extra sensor competes for limited resources | A comparison of complete feasible arrangements and the conditions of their realization | [CAD.4](../CAD/13_04_Co-design%20and%20Realize%20the%20Whole%20Control%20Architecture/00_CAD.04%20-%20Co-design%20and%20Realize%20the%20Whole%20Control%20Architecture.md) |

An engineer can use [[CAD/09_05_Choose Observations and Internal State for Control/00_CAD.05 - Choose Observations and Internal State for Control|CAD.5]] without introducing a planner or multiple layers. An engineer with a qualified lower loop can retain it and change command admission. If a current complete observation and a simple controller already meet the task, they remain a serious stopping alternative. Read the [Architectural Reference](../00_Hubs/CAD%20-%20Control%20Architecture%20Design%20Architectural%20Reference.md) when several results must fit together or a change reopens their conditions.

The intended reader can work with state-space models, feedback laws, bounded sets and elementary optimization. A reader who lacks those means needs instruction or a qualified control-engineering contributor. The examples are mathematical constructions. Before relying on a physical installation, establish its model, uncertainty and execution premises.
