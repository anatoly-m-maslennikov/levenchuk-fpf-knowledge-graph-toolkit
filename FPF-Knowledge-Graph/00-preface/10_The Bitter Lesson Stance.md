---
type: "fpf-knowledge-page"
context:
  - "FPF"
page_type: "fpf-knowledge-page"
mode: "canonical-generated"
title: "The Bitter Lesson Stance"
part: "[[00_Hubs/FPF - Preface (non-normative)]]"
parents:
  - "[[00_Hubs/FPF - Preface (non-normative)]]"
source_file: "FPF-Spec.md"
source_revision: "7f7c592f4d633e54cdb202d622d6e0e05df41517"
source_sha256: "6bdfe1a4347fde18dd50d69d16599f1513890a921627ec602d1d1b075109b48d"
generated_on: "2026-08-24"
source_lines:
  - 1101
  - 1118
status: "generated"
generated: true
---


FPF also carries a Bitter-Lesson-compatible stance. In AI, software, and open-ended engineering, systems that can use more search, more data, more compute, and more general learning often outperform brittle hand-coded procedure scripts when the domain changes or scale grows.

FPF does not turn that observation into blind automation. It translates it into an architectural preference:

- state goals, constraints, budgets, and checks more clearly;
- give agents and teams freedom to search within those declared bounds;
- keep safety, evidence, assurance, and gate conditions explicit;
- measure outcomes and refresh policies when the environment or model changes;
- avoid hiding brittle procedure scripts inside prose that looks like general guidance.

The important separation is between design-time constraints and run-time action. A designer may declare inadmissible actions, risk budgets, cost ceilings, admitted tools, escalation conditions, evidence minima, or acceptance criteria. That differs from prescribing the acting system's complete action sequence.

Some uses need a specified procedure: safety, regulation, legal compliance, reproducibility, and training can make a method description or work instruction current. FPF does not forbid that. It keeps the claim kind explicit. A procedure script is a method description or work instruction; a constraint set is a different object; a monitor is not evidence of success; a gate is not the work itself.

This stance helps with human and AI work alike. A team can use general agents, search, simulation, model refresh, or state-of-the-art harvesting without surrendering safety. The freedom lives inside constraints, budgets, evidence, and typed checks.
