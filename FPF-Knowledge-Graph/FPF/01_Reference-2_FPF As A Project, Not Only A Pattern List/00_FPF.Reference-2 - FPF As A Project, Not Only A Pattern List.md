---
type: "fpf-section"
context:
  - "FPF"
page_type: "fpf-section"
mode: "canonical-generated"
fpf_id: "FPF.Reference:2"
title: "FPF As A Project, Not Only A Pattern List"
part: "[[00_Hubs/FPF - First Principles Framework Architectural Reference (non-normative)]]"
parents:
  - "[[00_Hubs/FPF - First Principles Framework Architectural Reference (non-normative)]]"
source_file: "FPF-Spec.md"
source_revision: "fb3b6a4ad1d51d732a365f75f7d68337c7a751e2"
source_sha256: "03e2d58f56ef5e271d6e5481a042845eb1848994c221bed7fb384311b2a1a236"
generated_on: "2026-10-25"
source_lines:
  - 1128
  - 1143
status: "generated"
generated: true
---


FPF is a project for improving how difficult reasoning is written, checked, taught, used by humans, and used by AI agents. The Core Specification is the normative center of that project, but it is not the whole project.

The Core Specification gives the pattern language: the named concepts, distinctions, pattern bodies, conformance checks, and relations that make FPF usable across domains. It says what the reasoning objects are and how exact claims are constituted and checked. When a project needs to know whether a diagram is architecture, whether a dashboard is evidence, whether a model output may be used for a decision, or whether a term is hiding several kinds, the Core pattern bodies provide the relevant action- or judgement-guiding content and the definitions or constraints the claim actually needs. A separate `U.MethodDescription`, admitted Method, or exact `ClaimGraph` locator is recovered only when that distinction is current. Evidence use depends on the relation between an exact episteme and a target claim ([[A_Kernel Architecture Cluster/02_System-Role Kinds and Assignments/04_A.02.04 - Episteme Evidence-Use and Status-Use Relations|A.2.4]]), with reliance checked under [[A_Kernel Architecture Cluster/10_Evidence Graph Referring- Claim-Bound Evidence and Provenance Graph/00_A.10 - Evidence Graph Referring- Claim-Bound Evidence and Provenance Graph|A.10]]; publication alone does not establish that relation. Actor, ownership, and external-authority claims need their own direct basis.

Domain principle frameworks explain the methods and evidence practices of their fields and identify the FPF content and editions on which they rely. A local practice framework supplies guidance for a bounded local setting and may also rely on a domain framework. A local guide that simply applies existing guidance needs no new framework boundary. [[E_The FPF Constitution and Authoring Guides/03_04_FPF Ecosystem Architecture- Framework Families, Products and DPF Suites/00_E.04 - FPF Ecosystem Architecture- Framework Families, Products and DPF Suites|E.4]] explains when a separate framework or adjacent product is useful and how its dependencies differ from its publication.

Other publications can teach, demonstrate or support this content: companion explanations, worked cases, tooling guides and research notes have different purposes. A companion may teach a method more slowly, and a tool may implement a publication form; the method, its explanation and the implementation retain their own identities. A useful explanation can be brought back into the supplying pattern when ordinary framework use needs it.

An architectural reference explains the named whole: its working subject, contributions, boundaries and connections, why they are arranged this way, and the consequences for use. This First Principles Framework Architectural Reference belongs to the Core edition it explains. A DPF carries the corresponding account of its own pattern language; a DPF Suite explains a composite discipline through its constituent DPFs. A Suite Architectural Reference connects their contributions and explains the grounds, alternatives and limits of that composition. Using a result from another field does not make that entire field a constituent. [[E_The FPF Constitution and Authoring Guides/03_04_FPF Ecosystem Architecture- Framework Families, Products and DPF Suites/00_E.04 - FPF Ecosystem Architecture- Framework Families, Products and DPF Suites|E.4]]:4.2, [[C_Kernel Extension Specifications/08_20_Composition of U.Discipline (Discipline-CAL)/00_C.20 - Composition of U.Discipline (Discipline-CAL)|C.20]] and [[E_The FPF Constitution and Authoring Guides/10_11_First-Practical Entry and Pattern-Use Discoverability Discipline/04_E.11.DSG - Architectural Reference|E.11.DSG]] supply those distinctions.

The FPF Library Architectural Reference explains the larger arrangement of Core, DPFs and Suites, including relations across Suite boundaries. One common account does not establish that all described disciplines are parts of one super-discipline. An architectural reference may be embedded in one framework file or published separately at a multifile assembly's scope; its function does not depend on its position or carrier. [[E_The FPF Constitution and Authoring Guides/10_11_First-Practical Entry and Pattern-Use Discoverability Discipline/03_E.11.PFP - Framework Publication Form Profile for Markdown|E.11.PFP]]:4.7 requires enough shared explanation, source-based reasons, alternatives and worked detail to understand and adapt the whole without internal design records. Complete Methods remain in their patterns. The architectural reference is available when that larger question matters; it is not an obligatory stage before using a known sufficient pattern result.

One file or website can expose several such publications. Their shared carrier provides access; each framework, Reference or companion keeps the content, edition and change conditions established for it. Core meanings remain defined in Core. Authors can revise domain and local methods while preserving those dependencies. The Core can therefore remain tool-agnostic while companions, tools and domain explanations change for their intended uses.
