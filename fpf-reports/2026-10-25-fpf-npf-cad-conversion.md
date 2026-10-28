# FPF Graph Conversion Evaluation

Date: 2026-10-25  
Evaluator: `graph-fpf-evaluate-conversion-result`  
Overall verdict: **PASS**

The current FPF, NPF, and initial CAD projections satisfy the conversion acceptance profile. All fourteen issue families pass, all eight historical regression probes were exercised, and all twelve syntax-risk strata are populated and covered.

The final deterministic suite passed all 24 commands with no failures. Revision-bound schema 3 PASS evidence was written to `.runtime/fpf-conversion-evaluation.json` and independently verified through the acceptance checker.

This verdict supports acceptance of these conversion results. It does not establish that the upstream frameworks are internally complete, that their methods suit another project, or that the repository is ready for release.

## 1. Evaluation subject and source identity

Repository: `levenchuk-fpf-knowledge-graph-toolkit`

Current source revision for all three graphs:

```text
fb3b6a4ad1d51d732a365f75f7d68337c7a751e2
```

Generation date: `2026-10-25`

The external `FPF-original` checkout was clean and its committed HEAD matched this revision. The revision-named source package contains all 49 upstream-tracked files, with the exact tracked path list recorded in its metadata. Every upstream, effective-package, and staged-source digest matched. There are no repository-owned patches in this package.

The evaluated effective sources were staged under `.runtime/original-fpf-sources/`. No unscoped root `FPF-Spec.md` was present.

| Projection | Source filename | Effective source SHA-256 |
|---|---|---|
| FPF | `FPF-Spec.md` | `03e2d58f56ef5e271d6e5481a042845eb1848994c221bed7fb384311b2a1a236` |
| NPF | `Narrativization-and-Narrative-Studies-Principles-Framework.md` | `c5c274316d31db178d105526ee32e912c4ccd02a6c03279a42f83244612737ba` |
| CAD | `CONTROL-ARCHITECTURE-DESIGN-PRINCIPLES-FRAMEWORK.md` | `72d4c479741c828c7df8b70874ece00756a0e3d377f69f7f1d89f3fbe21704e7` |

The actual backup identities were retained rather than replaced with same-revision candidate copies:

| Projection | Current revision | Actual backup revision |
|---|---|---|
| FPF | `fb3b6a4ad1d51d732a365f75f7d68337c7a751e2` | `563f4c8e06a319cbd375b66cdbb2df27a5f8b9ef` |
| NPF | `fb3b6a4ad1d51d732a365f75f7d68337c7a751e2` | `d77339d7056433de3ee55ad863860ee4b3006f6f` |
| CAD | `fb3b6a4ad1d51d732a365f75f7d68337c7a751e2` | None: legitimate initial projection |

The NPF predecessor records its older file-scoped source revision. That observed identity is bound in the evidence; it was not rewritten to the FPF predecessor’s repository revision.

## 2. Generated inventory and exhaustive checks

| Projection | Hubs | Canonical pages | Unique IDs | Markdown files | Broken wiki-links |
|---|---:|---:|---:|---:|---:|
| FPF | 14 | 434 | 422 | 451 | 0 |
| NPF | 6 | 29 | 26 | 38 | 0 |
| CAD | 7 | 17 | 14 | 27 | 0 |
| Total | 27 | 480 | 462 | 516 | 0 |

Independent source-heading enumeration, with fenced content excluded, found exactly:

- FPF: 14 H1 units and 434 H2 units.
- NPF: 6 H1 units and 29 H2 units.
- CAD: 7 H1 units and 17 H2 units.

These counts agree with the generated carriers. No source-range bounds or fused-unit errors were found.

All 480 canonical bodies matched their staged source ranges after removing the declared heading, link, identifier-display, and table-formatting transformations. All 27 hub preambles also matched their source content before the first real child H2. No child-pattern paragraphs were duplicated into hubs.

Fenced content received a separate exact comparison without stripping formatting:

| Projection | Source fenced blocks | Blocks changed in generated output |
|---|---:|---:|
| FPF | 678 | 0 |
| NPF | 42 | 0 |
| CAD | 0 | 0 |

Whole-tree prose scans found no malformed triple-bracket links, raw wiki-link alias pipes inside tables, or broken relative Markdown file destinations.

| Projection | Ordinary Markdown links inspected | Broken relative file destinations |
|---|---:|---:|
| FPF | 1,389 | 0 |
| NPF | 86 | 0 |
| CAD | 64 | 0 |

Every canonical page was reachable from its master index. All 480 page-to-parent links had reciprocal child references in their hubs.

The largest generated path segments were 167 bytes for FPF, 96 for NPF, and 87 for CAD, below the 170-byte filename bound. No unsafe path segments, Unicode normalization problems, case-insensitive collisions, or embedded symlinks were found.

There were no `.DS_Store` files. Retired empty directory shells remained—89 in FPF and 9 in NPF—with no graph content. They were treated as filesystem shells, not generated carriers. CAD had none.

## 3. Eval-pack identity and bounded semantic selection

Eval-pack SHA-256:

```text
c2fd16a9357fa302087db33b553ebfd541844499a70e13dca2d4efd08bf0f23d
```

The raw FPF inventories contain 300 predecessor IDs and 422 current IDs:

| Change kind | Population | Pack-selected IDs |
|---|---:|---|
| Added | 123 | `A.1.CSD`, `C.37.CF`, `FPF.Reference:End` |
| Removed | 1 | `I.2` |
| Moved | 183 | `A.0`, `B.5`, `G.Core` |
| Retitled | 135 | `A.0`, `C.2.3`, `G.Core` |

The exact pack selection policy is:

> all changes through 12 per kind; otherwise first-middle-last; all removed IDs and top-level roots

The pack selects 15 distinct IDs and omits 295 changed IDs from direct semantic sampling. This omission applies only to bounded semantic inspection; mechanically decidable checks covered every generated carrier.

The selected IDs are:

```text
A.0
A.1.CSD
B.1
B.5
C.11
C.2.3
C.37.CF
D.1
E.1
F.0.1
FPF.Reference:1
FPF.Reference:End
G.0
G.Core
I.2
```

This covers every present top-level family: `A`, `B`, `C`, `D`, `E`, `F`, `FPF`, and `G`.

For every selected ID with both paths, both current and predecessor carriers were inspected. `I.2` was inspected only in the predecessor, with its absence from current source structure checked independently. No current carrier was invented for it.

Six additional current carriers cover the remaining syntax risks:

```text
A.1
A.2.3
A.6.5
A.15.8.MS
A.18
00-readme/00_Start here.md
```

The resulting FPF bounded set comprises 20 current carriers and 11 predecessor carriers.

Additional source comparisons covered all five CAD patterns and their architectural-reference carriers. NPF semantic inspection included `NSTD.1`, `NSTD.6`, and `NSTD.Reference:12`. All canonical CAD and NPF bodies were also included in the exhaustive normalized-content comparison.

Direct semantic inspection used bounded source slices and adjacent heading context. The monolithic FPF source was not loaded wholesale into model context. The result supports bounded semantic fidelity, not an assertion that every upstream proposition was independently interpreted or evaluated.

## 4. Fourteen required issue families

| # | Issue family | Verdict | Evidence |
|---|---|---|---|
| 1 | Source identity, safety, and authority | PASS | Clean upstream HEAD matches the full revision-named package; all 49 tracked paths and upstream/effective/staged digests agree; no patches or unscoped root monolith. |
| 2 | Transaction, backup, and rollback integrity | PASS | Actual FPF and NPF predecessors remain bound separately from the candidate; CAD has a legitimate initial state. Transaction, rollback, repeated-revision backup, and acceptance-preservation tests passed. |
| 3 | Completeness and exact reconstruction | PASS | Independent raw H1/H2 counts match all 27 hubs and 480 canonical pages. Whole-tree validators and clean-rebuild regressions passed. The removed `I.2` is accounted for. |
| 4 | Boundary parsing and source-range fidelity | PASS | Every canonical range is within source bounds and contains no following H1/H2 unit. Fenced headings and table-shaped false headings are covered by regressions. |
| 5 | Normative content and Markdown preservation | PASS | All 480 canonical bodies and 27 H1 preambles preserve normalized source wording and order. All 720 fenced blocks remain exact. CAD’s license, edition, and opening scope are retained. |
| 6 | Linkification and rendering | PASS | No prose triple-bracket corruption, table alias-pipe corruption, or broken relative Markdown destinations. Reference-style links, definitions, source-local anchors, and cross-source links were verified after repair. |
| 7 | Identity stability and collision handling | PASS | No duplicate IDs. Delta inventories match current and predecessor carriers; stable IDs survive title/path changes. Disambiguation and clean-removal regressions passed. |
| 8 | Folder topology and reading order | PASS | Source-order construction is preserved, including CAD.5 preceding CAD.1–CAD.4, nested/alphanumeric IDs, new reference sections, and unprefixed pages. No child content is duplicated into hubs. |
| 9 | Filesystem portability and path hygiene | PASS | All paths checked for unsafe segments, normalization, byte length, case collisions, and symlinks; maximum segment lengths stay below the declared bound. Empty retired shells are separately reported. |
| 10 | Provenance and replayability | PASS | Every generated Markdown carrier has matching source filename, revision, hash, and explicit generation date. Reports use portable names. Relocation, repeated-build, and declared-input regressions passed. |
| 11 | Navigation, indexes, and reachability | PASS | Every canonical page is master-index reachable; all 480 parent links are reciprocal. Index paths are current. Term counts do not reach the 120-term per-page truncation limit; observed maximum is 20. |
| 12 | Relation extraction and classification | PASS | Final frontmatter/index relation multisets agree exactly: FPF 5,187, NPF 126, CAD 0. Slash chains, plain/bold labels, continuation boundaries, and every unresolved occurrence were checked. |
| 13 | Eval-pack and validator independence | PASS | Raw scans independently checked counts, source boundaries, identifiers, content, paths, links, fences, navigation, and relation multisets. The pack now truthfully includes 12 unprefixed carriers and prioritizes the actual unresolved-reference carrier. |
| 14 | Repository and consumer compatibility | PASS | All 24 deterministic commands passed, including graph validators, reproducibility, installer tests, skill compatibility, repository integration, settings synchronization, script architecture, and patch hygiene. Acceptance evidence passed its independent identity/digest checker. |

No converter, deterministic-test, eval-pack, or repository-integration defect remains open in the evaluated result.

## 5. Historical regression probes

| Machine ID | Verdict | Exercise and evidence |
|---|---|---|
| `unscoped-root-source` | PASS | Confirmed absence of root `FPF-Spec.md`; canonical originals are packaged under the revision-named hidden directory and staged under `.runtime`. |
| `stale-tree-after-moves` | PASS | Current raw inventories account for 183 moves and one removal. Clean-rebuild deletion regression and whole-tree expected-path checks passed. |
| `triple-bracket-linkification` | PASS | Whole-tree prose scan found none. Real B.5 reference-style links remain valid after expansion and source-target rewriting. |
| `table-pipe-corruption` | PASS | Whole-tree table scan found no raw alias pipes; controlled empty-column and alias regressions passed. |
| `absolute-path-provenance` | PASS | Generated metadata and report source/output identities remain portable; checkout relocation regression passed. |
| `implicit-generation-date` | PASS | Every current carrier records the explicit date `2026-10-25`; repeatability tests use declared generation dates. |
| `missing-source-hashes` | PASS | Every carrier’s source SHA-256 matches its projection report and staged source bytes. |
| `wrong-semantic-link-target` | PASS | Source-anchor navigation regressions passed. Selected real links, including CAD’s architectural-reference subsection and FPF B.5’s referenced patterns, preserve the intended target. |

All eight probes were exercised; none was waived by a generic validator result.

## 6. Syntax-risk coverage

All twelve pack strata are populated and receive `PASS`; none is reported as `NOT_PRESENT`.

| Stratum | Pack population | Selected carrier | Evidence inspected |
|---|---:|---|---|
| Bracketed reference adjacent to punctuation | 1 | `A.2.3` | Source line 5659’s bracketed reference syntax and surrounding fenced content remain intact. |
| Existing wiki-link or Markdown link | 422 | `A.0` | Existing links and generated references remain distinct; additional real reference-style links were checked in B.5. |
| Markdown table with generated links | 335 | `A.0` | Source table content, link rendering, and column integrity; empty-column behavior exercised by the deterministic fixture. |
| Fenced code with heading/ID-like text | 161 | `A.1` | Source lines 2598–2607 plus the exhaustive exact comparison of 720 fenced blocks. |
| Relation-section variants | 395 | `A.0` | Supplemented with F.18 plain labels and continuation bullets, G.3 bold labels, and the unknown-label boundary regression. |
| Non-ASCII title or path | 23 | `A.0` | Source title, generated sanitized path, Unicode normalization, and current/predecessor carriers. |
| Long or similar title | 4 | `A.6.5` | Source range 23488–23858, title/path correspondence, and portable segment bound. |
| Alphanumeric or deeply nested ID | 42 | `A.15.8.MS` | Source range 32112–32437, exact ID, owner folder, and navigation. |
| Unprefixed H2 routing | 12 | `00-readme/00_Start here.md` | Source range 593–608 and its actual canonical carrier; the earlier false “absent” result is corrected. |
| Added, moved, or retitled since backup | 306 | `A.0` | Current/predecessor title, path, source range, and preserved ID; supplemented by every pack-selected change target. |
| Unresolved placeholder/reference risk | 303 | `A.18` | Actual unresolved relation prioritized; source line 34903 contains the legacy `C.MM‑CHR` wording. |
| Root of every top-level family | 8 | `A.0` plus all pack family representatives | `A`, `B`, `C`, `D`, `E`, `F`, `FPF`, and `G` are represented. |

Risk populations are candidate inventories for inspection, not counts of defects.

## 7. Demonstrated findings and repair closure

These findings arose during evaluation, were returned to the converter, and were independently rechecked after authorized repairs.

| Finding | Classification | Demonstrated defect | Closure |
|---|---|---|---|
| EVAL-001 | Converter defect | FPF source lines 46730 and 46820 used reference-style Markdown links; generated B.5 nested wiki-links inside them and produced triple closing brackets. | CLOSED: reference links and definitions are protected/expanded correctly; real B.5 links and whole-tree prose scan pass. |
| EVAL-002 | Converter defect | NPF source line 406’s `../FPF-Spec.md` became a broken relative link from its split carrier. | CLOSED: generated `NSTD.Reference:12` uses the revision-bound upstream FPF source URL; no broken relative Markdown destination remains. |
| EVAL-003 | Converter defect | FPF source lines 117747–117748 contained slash-separated reference chains; extraction omitted real targets and emitted truncated `F.0`. | CLOSED: all intended chain IDs are retained, truncated `F.0` is absent, and regression tests pass. |
| EVAL-004 | Converter defect | Plain and unbulleted bold relation labels were ignored, losing or misclassifying F.18 and G.3 dependencies. | CLOSED: labels and continuation bullets retain their source categories; selected real frontmatter and indexes agree. |
| EVAL-005 | Eval-pack defect | The pack reported no unprefixed H2 risk because it scanned only identified carriers; twelve such pages existed. | CLOSED: all twelve are inventoried, `Start here` is selected, and the actual unresolved-reference carrier is prioritized. |
| EVAL-006 | Converter defect | Linewise rendering changed IDs and sometimes syntax inside real fenced code: 112 FPF pages and six NPF pages were affected. | CLOSED: rendering is fence-aware; all 678 FPF and 42 NPF source blocks match generated blocks exactly. |
| EVAL-007 | Converter defect | A later unknown label could inherit the preceding relation category; F.18’s non-use discussion leaked an F.9 reference into `coordinates_with`. | CLOSED: the continuation boundary is respected. F.18 retains `builds_on F.9` and no longer has `coordinates_with F.9`. |
| EVAL-008 | Converter defect | H1-only preamble content was omitted, including CAD’s license, author attribution, edition, and opening scope. | CLOSED: all 27 hub preambles preserve source content, including CAD source lines 1462–1464. Child pattern bodies are not copied into hubs. |

The final complete suite passed after these repairs and the final regeneration. Earlier passing runs were not substituted for the final candidate’s evidence.

## 8. Source conditions and external references

### FPF legacy reference

FPF has one unresolved projected relation token: `C.MM`.

The bounded source evidence is `FPF-Spec.md`, line 34903, inside A.18’s source range 34753–34914. The source refers to the “Measurement & Metrics Characterization spec (`C.MM‑CHR`)” and also names C.16.

The generated body preserves that wording. The relation remains visibly unresolved and is classified as a non-catalog token or legacy alias. No nonexistent pattern body was fabricated and no resolution was asserted.

Classification: `upstream-source condition`.

Effect: this prevents treating the source’s naming references as completely uniform. It does not block acceptance of a faithful conversion.

### NPF external framework dependencies

NPF exposes 104 relation occurrences whose targets belong to other framework namespaces:

| Target family | Occurrences |
|---|---:|
| A | 32 |
| B | 8 |
| C | 25 |
| D | 8 |
| E | 20 |
| F | 1 |
| G | 10 |
| Total | 104 |

Every occurrence is present in the report and relation index. The validator classifies these as `external framework target outside this projection`.

These are external dependencies of the NSTD projection, not missing internal NSTD bodies. For example, source lines 404–409 explicitly state the framework’s dependence on FPF Core and identify A.6.3.NAR, C.2.8, A.19.ECS, C.16, E.4.PFR, and G.11.

The evaluation does not assert that every external dependency was independently evaluated. Keeping those references external and visible is faithful projection behavior.

CAD reports zero unresolved relation occurrences. Its internal navigation and architectural-reference links remain available independently of its empty extracted relation index.

## 9. Deterministic-suite evidence

The final current-candidate suite finished with:

```text
exit code: 0
cases: 24
failures: []
```

Manifest SHA-256:

```text
7d3d66e663e8ab1bbb3b50e98972150bb724d7bbee90eacf844e86422d724044
```

The exact case names bound in the evidence are:

```text
compile
settings-unit
settings-preflight
converter-transaction
graph-validator
npf-converter
npf-validator
cad-converter
cad-validator
reproducible-generation
installer
fpf-skill-runtime
service-installer-unit
suite-contract-unit
methodology-settings-sync
generated-graph
generated-npf-graph
generated-cad-graph
eval-pack
skill-graph-compatibility
repository-integration
architecture-unit
architecture
patch-hygiene
```

These are deterministic command cases, some of which run multiple unit tests. The count is not a claim that the repository contains only 24 individual assertions.

## 10. Bound tree digests and PASS evidence

Tree hashes include every regular file in sorted relative-path order using:

```text
relative_path + NUL + file_bytes + NUL
```

`.DS_Store` is excluded and symlinks are rejected.

| Projection | Current tree SHA-256 |
|---|---|
| FPF | `b35e47c9e2293a38a0ff13bc5ccca5c1d3fa13a4cdaf8a907d1f833f43ab7d63` |
| NPF | `6a9a312ab4083ba58609a304dc86c2a48d57aa1bd4aeff3d13cf0eb0972a2c33` |
| CAD | `011dbf399343955d9b4263a8b972f72ca9f724f099632452b73063646abe2a31` |

| Projection | Backup tree SHA-256 |
|---|---|
| FPF | `239254be9813cb4f887fa09ce13fe1cb6c1290b1be0cc3f374b2622ddcb5ee1a` |
| NPF | `394c7bc177e70fb163e5b491811e0d332d880537d9d033dff67c95837ae6c276` |
| CAD | `null` — initial projection |

PASS evidence:

```text
.runtime/fpf-conversion-evaluation.json
schema_version: 3
evaluator: graph-fpf-evaluate-conversion-result
verdict: PASS
```

The acceptance checker independently verified its exact fields, source revision, projection manifest, current and backup digests, eval-pack digest, fourteen family verdicts, eight probe verdicts, twelve stratum verdicts, semantic-selection identity, and deterministic-suite identity.

The evaluator’s sole deliverable write was this PASS evidence file. It did not modify generated graphs, sources, converters, tests, or settings.

## 11. Handoff and limits

**No converter repair required.**

The converter can proceed with acceptance finalization. The finalizer must perform its required complete-suite rerun and remove only the manifest-bound staged source and predecessor directories after that rerun passes. The tracked revision-named source package remains.

This report records the graph and backup identities at evaluation time. It does not itself perform cleanup or assert that the later finalizer has finished.

The mechanical checks cover the complete generated trees. Semantic inspection remains bounded by the documented selection. The single FPF legacy token and the NPF external dependencies are exposed separately and have not been hidden, invented away, or converted into unsupported claims of upstream completeness.

## 12. Converter handoff: implementation and finalization

This section is the implementing agent's handoff, appended after the independent evaluator's complete native report above.

Final state: **complete** for the requested conversion work.

- Refreshed FPF and NPF and generated the initial CAD graph from upstream repository HEAD `fb3b6a4ad1d51d732a365f75f7d68337c7a751e2`.
- Added `service.scripts.graph_cad_convert_from_original` and `service.scripts.validate_cad_graph`, their tests, and CAD integration into the deterministic suite and acceptance manifest.
- Added support for upstream's current `DPFs/` source layout while retaining compatibility with older root-level editions. Graph provenance identifies the packaged repository HEAD; source metadata separately retains each publication's last-change commit.
- Corrected shared rendering, links, relation extraction, hub preambles, backup retention, and risk selection as documented above, with regression coverage. The original source text was not patched.
- Updated the repository and service README files and the two conversion-service skill contracts. `skill-refactor` guided only these service-contract updates; it did not change end-user analytical behavior.
- The methodology compatibility check inspected 422 graph IDs and 11 methodology prompts and reported `update_required = false`. No end-user `$fpf` prompt change was required by this graph refresh.

The finalization command completed with exit code 0:

```bash
uv run --locked -m service.scripts.graph_fpf_convert_from_original --finalize-accepted
```

It independently verified the revision-bound PASS evidence and staged source bytes, reran the entire 24-command deterministic suite successfully, and cleared the contents of these exact temporary paths:

```text
.runtime/original-fpf-sources
FPF-Knowledge-Graph.bak
NPF-Knowledge-Graph.bak
```

A post-finalization file scan found no remaining files in those paths. The managed filesystem may retain empty directory shells. CAD was an initial projection and had no predecessor backup. The cleanup removed only temporary copies; the evaluated original/effective source package remains at `.fpf-original-fb3b6a4ad1d51d732a365f75f7d68337c7a751e2/`, and previously tracked graph versions remain recoverable through Git.

The canonical external input used was the clean `FPF-original` checkout, with origin `git@githuba:ailev/FPF.git`. The external machine-local control panel points to that checkout. The older checkout under `Documents/Repos/FPF` was not modified because its location was not writable in this session.

Final patch hygiene passed. Nothing was staged, committed, or pushed; pre-existing worktree changes were preserved.

Not run: the separate live LLM methodology-skill quality gate. Deterministic runtime/installer/compatibility checks and the independent conversion evaluation passed, but they do not establish live skill-release readiness.
