---
type: "fpf-knowledge-page"
context:
  - "FPF"
page_type: "fpf-knowledge-page"
mode: "canonical-generated"
title: "How to Use This Repository"
part: "[[00_Hubs/FPF - First Principles Framework (FPF) Readme]]"
parents:
  - "[[00_Hubs/FPF - First Principles Framework (FPF) Readme]]"
source_file: "FPF-Spec.md"
source_revision: "7f7c592f4d633e54cdb202d622d6e0e05df41517"
source_sha256: "6bdfe1a4347fde18dd50d69d16599f1513890a921627ec602d1d1b075109b48d"
generated_on: "2026-08-24"
source_lines:
  - 810
  - 847
status: "generated"
generated: true
---


Start with the practical-use card that recognizes the current project question. If several fit, compare their situations, first-result differences, and stop or return conditions before inspecting the selected pattern.

Use the `Preface` for the cross-cutting ideas and the repeated-use explanation. Use the Table of Contents when you already know the pattern family or need a search-oriented overview. Use the selected pattern body for its Solution. Once one pattern is current, use [[E_The FPF Constitution and Authoring Guides/10_11_First-Practical Entry and Pattern-Use Discoverability Discipline/01_E.11.PUA - Pattern Use in a Working Situation and First Useful Result|E.11.PUA]] to follow that Solution to the smallest useful result or an honest missing-basis stop. Name a receiving use only when an actual continuation or later reliance is current. Use [[E_The FPF Constitution and Authoring Guides/10_11_First-Practical Entry and Pattern-Use Discoverability Discipline/02_E.11.PUR - Pattern-Use Applicability, Recommendation, and Coordination|E.11.PUR]] to judge applicability, recommendation, coordination, or ordering among candidate pattern uses, and to stop on an earlier result that still answers the concern. An ordinary reversible judgement may remain conversational; make it addressable only when a named later use needs that support. Use extended cases when the compact card and selected pattern are not enough.

If you use an AI assistant, attach or index `FPF-Spec.md` and ask for plain-language project help first. Let internal pattern names enter the conversation only when they make the reasoning more precise.

A good first prompt is:

```text
You have the FPF specification as a file.
Help me with this current project question:
[short project description and question]

Use plain language for engineer-managers.
Compare the relevant semantic practical-use cards when several fit:
ARCHITECTURE, WORKING-DOCUMENTS, OPTION-COMPARISON,
PROBLEM-SHAPING, IMPROVEMENT, COSTLY-ACTION, TIME,
CAUSAL-USE, DESCRIPTION-USE, NAMING, WORDING,
MATHEMATICAL-MODELING, SOTA-PORTFOLIO, DPF-AUTHORING,
DPF-SUITE-GUIDE, SYSTEM-RECOGNITION, or SYSTEM-DELIMITATION.

Then inspect the selected pattern and its `Solution`.
Answer in this order:
- one useful result for the current situation, or an honest stop if no truthful result can yet be given;
- the current project question or action that result answers;
- any exact missing definition or test, applicable rule, case fact, information, or authority needed before a truthful answer is possible.
If those lines are sufficient and no downstream identity, application, publication, or reliance is current, stop there.
Only when the result's exact identity or obtaining basis, its application or publication, or later reliance changes the claim, also give:
- the selected pattern and `Solution`, the current EntityOfConcern, and the exact kind of result or basis on which it obtains;
- the exact Method, plan, dated Work, transformation, evaluation, decision, or other identified use object it answers;
- the exact relation or application binding that makes it a result for that object, or the supported local claim when no such relation is asserted.
Name what it lets us do next only when that continuation is current. If it cannot continue, state the exact missing definition, predicate or test, applicable rule, case fact, information, or authority.
Keep comparison conversational unless a named receiving use relies on an addressable record.
Do not turn the card into a whole-project plan.
```
