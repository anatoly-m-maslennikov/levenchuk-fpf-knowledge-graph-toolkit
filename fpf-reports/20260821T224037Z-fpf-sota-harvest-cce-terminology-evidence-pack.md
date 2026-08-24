## Task, scope, and boundaries

:codex-annotation{index="1"}

Task: execute the first routed call and produce a complete CCE terminology and evidence pack for a later, precise comparison with FPF language.

Resolved subject: in this context, **CCE** means **Common Conditions of use Elements**. It is a controlled vocabulary for describing conditions on the use of biomedical data, samples, registries, biobanks, and related resources. It is not the Canadian construction-contract form, continuous concurrent engineering, or another expansion of the acronym.

Receiving use: this report is the evidence handoff for a separate comparison call. That later call can compare CCE concepts and statement structure with FPF concepts. It should not have to rediscover what CCE means.

Included:

- CCE version 1.0, its 20 published terms, design principles, development method, validation basis, and stated limits.
- Digital Use Conditions (DUC), because CCE terms are neutral and DUC supplies the rule, scope, and optional parameter that turn them into policy statements.
- Three neighboring approaches: DUO, ODRL, and DPV.
- Current public implementation evidence from the DUC Generic 2.0 and EPND DUC profilers.
- Published disagreements about CCE/DUC design.
- Provisional comparison questions for the next FPF call, without claiming equivalence.

Excluded:

- A full CCE-to-FPF mapping or verdict.
- Legal advice or proof that a CCE/DUC profile complies with any law.
- Claims that CCE covers every governance condition, every biomedical setting, or every current implementation.
- Evaluation of confidential policies, consent forms, or data-access decisions.

Evidence date: 2026-08-22. The core CCE and DUC publications are from 2024. Current public implementation pages were checked during this run. The relevant local FPF source is from graph edition `f0b498ddfdf562242984ff7ab7a2557b55af6690`, generated on 2026-08-22.

Source policy: author-defined CCE meaning comes from the primary CCE paper; DUC structure comes from the primary DUC paper; present tool behavior comes from live implementation pages; neighboring standards come from their primary specifications or maintained repositories; criticism is attributed to its authors rather than presented as settled fact.

Saved report: `fpf-reports/20260821T224037Z-fpf-sota-harvest-cce-terminology-evidence-pack.md`

## High-confidence results (>=95%)

### Direct answer

**CCE is a small domain vocabulary, not a complete language or policy model.** The primary paper defines it as a version 1.0 categorization framework and explicitly says it is not an ontology. Its terms name conditions of use but do not say whether a condition is permitted, forbidden, obligatory, or absent. [Primary CCE paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC11078919/)

The technically precise stack is:

`CCE term + DUC rule + DUC scope + optional DUC parameter = one use-condition statement`

For example:

`Research Use + Permitted + Whole of asset`

CCE provides `Research Use`. DUC provides `Permitted` and `Whole of asset`. Calling the whole result “CCE language” is understandable shorthand, but it hides the distinction between the vocabulary and the statement structure. The DUC paper deliberately leaves its vocabulary layer open, so DUC can use CCE, DUO, ICO, a documented application vocabulary, or user-defined terms. [Primary DUC paper](https://www.nature.com/articles/s41597-024-03280-6)

### Harvest contract

- Question: What exactly is CCE, what terms and structures does it define, what does it claim, what does it not claim, and which neighboring approaches must be considered before comparing it with FPF?
- Unit of comparison: published concepts and statement structures, not project names or broad philosophical resemblance.
- Minimum evidence: the primary CCE and DUC publications, at least two neighboring traditions, one current implementation surface, and one independent critical comparison.
- Acceptance condition: an explicit term inventory, operational model, evidence ledger, disagreements, limits, and a clean handoff to the later FPF comparison.
- Stop condition: stop after the CCE evidence pack is reconstructible; do not read unrelated FPF patterns or begin the mapping prematurely.
- Refresh condition: rerun the harvest if CCE publishes a new numbered vocabulary release, DUC changes its rule model, or the comparison target changes from terminology to legal compliance or executable policy matching.

### CorpusLedger — sources and why they were used

| ID | Source and edition | Tradition | Role in this report | Status |
|---|---|---|---|---|
| CCE-1 | [Sanchez Gonzalez et al., “Common conditions of use elements,” Scientific Data 11:465 (2024), DOI 10.1038/s41597-024-03279-z](https://pmc.ncbi.nlm.nih.gov/articles/PMC11078919/) | CCE | Primary authority for the acronym, v1.0 terms, definitions, design principles, validation, and CCE-to-DUO mapping | Used |
| DUC-1 | [Jeanson et al., “Getting your DUCs in a row,” Scientific Data 11:464 (2024), DOI 10.1038/s41597-024-03280-6](https://www.nature.com/articles/s41597-024-03280-6) | DUC | Primary authority for the statement syntax, limits, profile metadata, and intended uses | Used |
| DUC-2 | [DUC Generic 2.0 profiler](https://ducejprd.le.ac.uk/profile) | DUC implementation | Current public evidence that validation targets CCE v1 and that the live fields are term, rule, scope, and optional parameter | Used |
| DUC-3 | [EPND DUC Profiler](https://ducepnd.le.ac.uk/) | DUC implementation | Current public evidence of CCE/DUC use in an EPND workflow | Used |
| DUO-1 | [Lawson et al., “The Data Use Ontology,” Cell Genomics (2021)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8591903/) | DUO | Peer-reviewed definition and original use model for the ontology neighboring CCE | Used |
| DUO-2 | [EBISPOT/DUO maintained repository](https://github.com/EBISPOT/DUO) | DUO | Current versioning, governance, implementation, and legal-limit statements | Used |
| ODRL-1 | [W3C ODRL Information Model 2.2, Recommendation (2018)](https://www.w3.org/TR/odrl-model/) | ODRL | Primary standard for policies built from permissions, prohibitions, duties, parties, assets, actions, and constraints | Used |
| DPV-1 | [W3C Community Group Final Report: Data Privacy Vocabulary (2024)](https://www.w3.org/community/reports/dpvcg/CG-FINAL-dpv-20240801/) | DPV | Primary vocabulary and ontology for personal-data processing, purposes, roles, legal bases, and related privacy concepts | Used |
| ALT-1 | [Pandit and Esteves, “Enhancing Data Use Ontology for health-data sharing by extending it with ODRL and DPV,” Semantic Web (2024)](https://journals.sagepub.com/doi/pdf/10.3233/SW-243583) | ODRL + DPV alternative | Independent technical comparison and explicit criticism of CCE/DUC | Used |
| DUC-P1 | [Cafe-Variome/DucCCE source repository](https://github.com/Cafe-Variome/DucCCE) | DUC implementation | Helpful implementation lead, but no release history was needed to establish the vocabulary contract | Screened, parked |
| DUC-P2 | [DUC specification record cited by the primary paper](https://doi.org/10.5281/zenodo.7767323) | DUC | A pin for future schema-level work; the peer-reviewed paper and current profiler were sufficient for this terminology pack | Identified, parked |

Flow record: 11 sources identified, 11 screened, 9 used, 2 parked, 0 silently discarded. The set covers three distinct design traditions: CCE+DUC, DUO, and ODRL+DPV.

### ClaimSheets — source claims separated from this review

#### CCE-1: Common Conditions of use Elements

- Source claim: CCE v1.0 is a 20-item set of controlled concepts for data and sample use conditions.
- Source claim: each term is intended to be atomic, non-directional, generalized, and widely applicable.
- Source claim: the list was reduced from 76 extracted candidates through review, alpha testing, and community feedback.
- Source claim: four biobanks, three patient registries, and one data platform created policy profiles with the final terms; no participant requested an additional CCE term during that exercise.
- Source limit: the authors call CCE foundational rather than a complete policy, anticipate public versioning, and retain free text for detail.
- Reviewer interpretation: the validation supports practical usefulness in the tested settings. It does not prove universal completeness or formal semantic independence.

#### DUC-1: Digital Use Conditions

- Source claim: DUC is a syntactic standard for use-condition metadata, not a fixed semantic vocabulary.
- Source claim: every statement has a condition term, rule, and scope; a parameter is optional.
- Source claim: allowed rules are `Obligatory`, `Permitted`, `Forbidden`, and `No Requirement`; scope is `Whole of asset` or `Part of asset`.
- Source claim: statements in one profile are independent and have equal standing. The first version deliberately omits dependencies between statements because tested Boolean structures confused users.
- Source limit: perfect unsupervised machine interpretation is described as unrealistic; automated triage was not validated in the reported work.
- Reviewer interpretation: DUC favors usability and consistent structure over full logical expressiveness.

#### DUO-1 and DUO-2: Data Use Ontology

- Source claim: DUO is an OWL ontology for tagging biomedical datasets with permissions and conditions, supporting discovery and access screening.
- Source claim: stable releases are date-versioned, identifiers are retained, and meaning-changing terms are deprecated rather than silently rewritten.
- Source limit: DUO is not a legal-compliance tool; adopters remain responsible for lawful decisions.
- Reviewer interpretation: DUO provides stronger formal hierarchy and release governance than CCE v1, but some DUO terms combine the concept and its direction in ways CCE deliberately separates.

#### ODRL-1 and DPV-1: reusable standards

- Source claim: ODRL represents policies using assets, parties, actions, permissions, prohibitions, duties, and constraints, with profiles for domain-specific vocabulary.
- Source claim: DPV represents personal-data processing, purposes, actors, legal bases, technologies, and related privacy concepts using a structured vocabulary and ontology.
- Reviewer interpretation: ODRL+DPV offers broader policy and legal context than CCE+DUC, at the cost of more concepts, mappings, and semantic-web machinery.

#### ALT-1: published critical comparison

- Authors’ position: separating CCE concepts from DUC rules is an improvement over terms that combine both.
- Authors’ criticism: DUC overlaps with ODRL, `No Requirement` lacks clear deontic meaning, some CCE terms have hidden type information, CCE lacks a taxonomy and extension mechanism, and the legal coverage is thin.
- Authors’ proposal: reuse ODRL for rules and DPV for vocabulary instead of maintaining a separate CCE/DUC rules stack.
- Reviewer interpretation: this is a well-specified rival design, not a neutral consensus statement. It provides valid comparison dimensions and unresolved challenges.

### Exact CCE v1.0 vocabulary

The primary paper divides the terms into nine criterion terms and eleven process terms. The descriptions below are compact paraphrases of the published definitions. [CCE v1.0 tables](https://pmc.ncbi.nlm.nih.gov/articles/PMC11078919/)

#### Criterion terms

| Term | Plain meaning |
|---|---|
| Clinical Care Use | Use in patient healthcare or related services |
| Clinical Research Use | Human-subject research intended to advance medical knowledge |
| Commercial Entity | Use by a commercial-sector organization, whether profitable or not |
| Disease Specific Use | Research concerning named diseases or disease groups |
| Geographical Area | Use within named geographic regions |
| Profit Motivated Use | Use intended to produce profit |
| Regulatory Jurisdiction | Use under a shared legal framework or oversight authority |
| Research Use | General research exploration or innovation |
| Use As Control | Use as a reference, benchmark, or control |

#### Process terms

| Term | Plain meaning |
|---|---|
| Collaboration | Use involving collaboration, commonly with the resource provider |
| Ethics Approval | Evidence of approval by an ethics or oversight body |
| Fees | Payment as a condition of access or use |
| Publication Moratorium | Publication withheld until a date or other condition is met |
| Publication | Derived results made available to the scientific community |
| (Re-)Identification Of Individuals Mediated By The Resource Provider | Identification or re-identification with provider involvement |
| (Re-)Identification Of Individuals Without Involvement Of The Resource Provider | Identification or re-identification without provider involvement |
| Return Of Incidental Findings | Unplanned findings returned to the resource provider |
| Return Of Results | Planned results returned to the resource provider |
| Time Period | A time limit on use |
| User Authentication | Identity proofing before access or use |

### Why the vocabulary has these boundaries

The paper documents several deliberate splits:

- `Geographical Area` and `Regulatory Jurisdiction` are separate because a legal area does not necessarily match a simple geography.
- `Clinical Care Use` and `Clinical Research Use` are separate because patient care and research are different purposes.
- The two re-identification terms are separate because provider-mediated contact and independent re-identification have different operational meanings.
- `Commercial Entity` and `Profit Motivated Use` are separate because an organization’s sector and a particular use’s profit motive are different facts.

These examples show what the authors mean by “atomic”: avoid combining distinctions that may vary independently. They do not establish atomicity as a mathematically proved property.

### Operational model: objects, actions, and outputs

| Element | Meaning in CCE/DUC |
|---|---|
| Resource or asset | The data, sample, collection, registry, biobank, or other object governed by a profile |
| Condition term | A neutral category such as `Research Use` or `Time Period` |
| Rule | Whether that condition is permitted, forbidden, obligatory, or has no requirement |
| Scope | Whether the statement covers the whole asset or part of it |
| Parameter | Optional detail, such as a country, disease, date, duration, or free-text qualification |
| Statement | One term-rule-scope combination, optionally qualified by a parameter |
| Profile | One or more independent statements plus optional metadata and asset references |

Normal workflow:

1. Identify the governed asset or resource.
2. Select a neutral condition term.
3. Add one rule.
4. State whether the rule covers all or part of the asset.
5. Add a parameter only when the statement needs more detail.
6. Combine independent statements into a profile.
7. Validate and export the profile, commonly as JSON.

The current DUC Generic 2.0 interface exposes these same fields and says that current validation targets CCE-aligned structures and `CCE terms v1`. [Current DUC Generic 2.0 profiler](https://ducejprd.le.ac.uk/profile)

### Small examples

1. Dataset-wide research permission:

   `Research Use | Permitted | Whole of asset`

2. A geographic restriction on only part of a biobank collection:

   `Geographical Area | Permitted | Part of asset | Country = UK`

3. A twelve-month limit:

   `Time Period | Obligatory | Whole of asset | Months = 12`

4. A distinction that CCE preserves but DUO can combine:

   `Commercial Entity | Permitted` and `Profit Motivated Use | Forbidden`

   This allows commercial-sector use that is not profit-motivated. The CCE paper’s mapping shows that DUO’s “non-commercial use only” bundles these dimensions.

### SoTA_Set — three design traditions

| Dimension | CCE + DUC | DUO | ODRL + DPV |
|---|---|---|---|
| Main goal | Easy, regular statements about biomedical use conditions | Ontology tags for biomedical data-use permissions and restrictions | General machine-readable policy rules plus privacy and legal vocabulary |
| Basic unit | Neutral CCE term, then a separate DUC rule and scope | Ontology term, sometimes combining concept and direction | Policy rule over an action, asset, party, duty, and constraints |
| Formal structure | Simple JSON-oriented statement model | OWL ontology and hierarchy | W3C policy information model plus structured vocabularies |
| Domain | Data, samples, and biomedical resources | Mainly health, clinical, and biomedical research data | General digital rights and privacy/data-protection domains |
| Expressiveness | Deliberately bounded; no dependencies between statements in v1 | Supports ontology relationships but not every conditional policy arrangement | Richer parties, constraints, duties, policy types, legal context, and extension profiles |
| Adoption cost | Lower conceptual and tooling burden | Requires ontology-compatible tagging and matching | Higher modeling and semantic-web burden |
| Version governance | Published CCE v1.0; public future versioning anticipated | Maintained date-versioned releases and stable identifiers | Formal W3C recommendation and maintained DPV releases |
| Main known risk | Simplicity can hide types, dependencies, and legal detail | Composite or directional terms can reduce flexibility | Complexity can discourage correct adoption |

This is not a winner ranking. The approaches optimize for different balances of simplicity, formal semantics, legal detail, and implementation cost.

### Bridges and partial mappings

- CCE to DUO: the CCE paper provides direct, rule-assisted, combined, and missing mappings. Five CCE terms had no DUO match in its table: `Fees`, `Regulatory Jurisdiction`, `Return Of Incidental Findings`, and the two re-identification variants. [Published CCE-to-DUO mapping](https://pmc.ncbi.nlm.nih.gov/articles/PMC11078919/)
- DUC to other vocabularies: DUC deliberately permits controlled vocabularies or ontologies other than CCE. The current DUC Generic page lists CCE v1, DUC-compatible DUO, and DUC-compatible ICO terms.
- CCE/DUC to ODRL/DPV: Pandit and Esteves propose mappings, but their own analysis identifies mismatches. Some CCE terms look like actions; others are better represented as purposes, locations, durations, organizational measures, or constraints. This bridge is a proposal, not an official CCE or W3C conformance result.

### What CCE does and does not claim

Supported claims:

- A small vocabulary can make common use-condition concepts more consistent.
- Separating a neutral condition from its rule allows the same concept to be permitted, forbidden, or required.
- The 20 terms were usable by the tested biobanks, registries, and data platform for creating policy profiles.
- CCE can act as a shared layer for comparison or translation across other vocabularies.

Claims not supported by the evidence:

- CCE is a complete policy language.
- CCE is an ontology.
- Twenty terms are universally sufficient.
- A CCE/DUC profile proves legal compliance.
- Free-text parameters are fully machine-interpretable.
- Independent DUC statements can represent arbitrary conditional logic.
- Current tools prove production-scale adoption or correct automated access decisions.

### Disagreement record

1. **Atomicity.** The CCE authors present atomicity as a design requirement supported by iterative splits and testing. Pandit and Esteves argue that several terms still contain hidden categories, such as purpose, actor, duration, or technical measure, and should be organized in a taxonomy. Both observations can be true: a term may be operationally useful as one selectable item while remaining decomposable in a richer information model.

2. **`No Requirement`.** DUC includes it as one of four rules. The ODRL/DPV comparison argues that it does not by itself say permitted, prohibited, or obligatory, so automated matching can be ambiguous.

3. **New simple stack versus reuse of standards.** CCE/DUC favors a small, teachable structure. The rival proposal favors ODRL and DPV to avoid another rules language and gain policy types, formal constraints, and legal vocabulary. The trade-off is simplicity versus expressive and standards-based machinery.

4. **Legal coverage.** CCE includes jurisdiction as a condition category, but does not model laws, legal bases, controller roles, safeguards, or data-subject rights. DPV covers more of that landscape. Neither vocabulary by itself proves compliance.

5. **Automation.** CCE/DUC aims to improve machine-readable comparison, but the DUC paper explicitly says perfect unsupervised interpretation is unrealistic and did not validate automated triage. A structured profile is better input for automation; it is not evidence that an access decision is correct.

### Handoff to the later CCE-versus-FPF call

The next call should compare specific functions, not match names by intuition. The first comparison questions should be:

- How does FPF define and test a “single concept,” and is that compatible with CCE’s operational notion of atomicity?
- Where does FPF separate a descriptive category from permission, prohibition, or obligation?
- How does FPF represent the governed object, statement scope, context, and optional qualification?
- Does FPF permit independent statements only, or can it represent dependencies and conditional combinations that DUC v1 omits?
- How does FPF handle versioned vocabularies, stable identifiers, mappings, and disagreement between alternative models?
- Is the intended FPF object a vocabulary term, a claim, a policy statement, a specification, or a larger knowledge artifact?

These are search leads only. No CCE term has yet been declared equivalent to an FPF term.

## Open questions (confidence <95%)

### 1. Is CCE v1.0 still the latest formally governed vocabulary release?

Best current answer: probably yes. The current DUC Generic 2.0 profiler still labels its system vocabulary `CCE terms v1`, and no public CCE v2 release was found.

Confidence: 92% — probable, but confirmation is still needed.

Missing evidence: a canonical CCE release registry with numbered, immutable releases and a public change history.

Consequence: “current CCE” could refer to a newer unpublished or differently hosted term set.

Next action: obtain the maintainers’ canonical registry or version-history link before a production implementation pins CCE.

### 2. Which artifact is the authoritative machine-readable CCE registry?

Best current answer: the paper is authoritative for v1.0 terminology, while current tools implement it; a single, clearly governed machine-readable source was not established.

Confidence: 85% — materially uncertain.

Missing evidence: an official vocabulary file with stable term identifiers, release metadata, ownership, and deprecation policy.

Consequence: two implementations could use the same labels but different identifiers or revisions.

Next action: ask the CCE/DUC maintainers to identify the canonical term registry and governance process.

### 3. Are all 20 CCE terms formally independent and atomic?

Best current answer: they were designed and tested to be operationally atomic, but this was not demonstrated as formal semantic independence.

Confidence: 90% — probable, but confirmation is still needed.

Missing evidence: explicit identity criteria, formal type assignments, counterexample tests, and dependency analysis for each term.

Consequence: a later CCE-to-FPF comparison could mistakenly treat a usability design rule as a formal theory of atomic concepts.

Next action: in the comparison call, test representative terms such as `Clinical Research Use`, `Time Period`, and `User Authentication` against FPF’s exact concept and relation rules.

### 4. What should `No Requirement` mean in automated matching?

Best current answer: it records that the profile states no requirement for the selected condition, but its effect depends on profile defaults and matching rules.

Confidence: 82% — materially uncertain.

Missing evidence: a normative truth table covering `No Requirement`, unstated conditions, profile permission mode, conflicts, and requests.

Consequence: different engines may interpret the same profile differently.

Next action: retrieve the pinned DUC schema and matching algorithm, then run worked cases against all rule/default combinations.

### 5. Can CCE/DUC represent policies with dependencies without semantic loss?

Best current answer: not directly in DUC v1. The paper deliberately makes statements independent and suggests multiple profiles as an indirect workaround.

Confidence: 90% — probable, but confirmation is still needed for newer implementations.

Missing evidence: current schema behavior for conjunction, disjunction, exceptions, precedence, and dependencies.

Consequence: a complex source policy may be flattened into statements that change its meaning.

Next action: test a policy such as “profit-motivated use is permitted only in jurisdictions A or B after ethics approval” against the current schema.

### 6. Are the proposed ODRL/DPV mappings accepted by CCE/DUC maintainers?

Best current answer: no acceptance evidence was found. They are a published rival proposal.

Confidence: 88% — materially uncertain.

Missing evidence: an official mapping release, conformance statement, or maintainer decision.

Consequence: treating the mappings as standard could create false interoperability claims.

Next action: classify every mapping in the next comparison as official, author-proposed, reviewer-proposed, or locally inferred.

### 7. What is the precise CCE-to-FPF relationship?

Best current answer: unresolved by design in this call. The most plausible comparison axes are term atomicity, separation of neutral concepts from rules, object and scope representation, conditional composition, and version governance.

Confidence: 60% — materially uncertain.

Missing evidence: targeted reading of the relevant FPF patterns and worked mappings using the same CCE examples.

Consequence: a broad comparison now would invite loose analogy and false equivalence.

Next action: execute the routed comparison call using this report as the CCE evidence pack and retrieve only the FPF patterns required by the seven handoff questions.

## Skills used

- `fpf-sota-harvest` — executed to resolve the corpus, preserve competing approaches, separate source claims from reviewer interpretation, and produce this reconstructible terminology and evidence pack.

No other FPF skill was executed. `fpf-route` supplied the earlier plan but was not rerun here.

#### FPF sources consulted (1 read; 1 used)

- **Used:** `FPF-Knowledge-Graph/G_Discipline SoTA Patterns Kit/03_02_SoTA Harvester & Synthesis/00_G.02 - SoTA Harvester & Synthesis.md` — supplied the bounded harvest contract, source ledger, claim records, plural comparison, disagreement preservation, stop rule, and refresh rule.

#### Research sources consulted

- **Used:** primary CCE paper, primary DUC paper, current DUC Generic 2.0 profiler, current EPND DUC profiler, primary DUO paper, maintained DUO repository, W3C ODRL 2.2, W3C Community Group DPV report, and the peer-reviewed ODRL/DPV critique.
- **Screened but parked:** the DucCCE implementation repository and the Zenodo DUC schema record; neither was needed to establish the terminology contract, and both remain useful for schema-level follow-up.

<oai-mem-citation>
<citation_entries>
MEMORY.md:1096-1113|note=[used bounded FPF retrieval and evidence separation rules]
MEMORY.md:1172-1181|note=[used current FPF skill and report persistence conventions]
</citation_entries>
<rollout_ids>
019fb801-af36-7993-8d2c-b98cbd0dfc55
019fc257-ad77-7d31-b3e2-1b6b37cc0274
</rollout_ids>
</oai-mem-citation>
