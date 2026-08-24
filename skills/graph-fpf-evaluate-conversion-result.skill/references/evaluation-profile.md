# FPF graph conversion evaluation profile

This profile is the acceptance authority for `graph-fpf-evaluate-conversion-result`. It combines known historical regressions with adjacent failure families that deterministic self-checks can miss.

## Coverage rule

Use two distinct coverage modes and report them separately.

### Exhaustive mechanical coverage

Run the complete deterministic suite and whole-tree validators against every generated entry. Require coverage of all paths, files, directories, frontmatter carriers, declared IDs, source ranges, generated links, relation occurrences, index entries, validation-report fields, and installer/repository integration checks. A sample cannot replace these exhaustive checks.

Independently inspect raw outputs for each historical regression probe below. Do not treat a self-reported zero count as sufficient when the same converter produced both the graph and the report.

### Bounded semantic coverage

Semantic equivalence, link intention, relation direction, and retrieval usefulness require bounded direct inspection. Use every changed high-risk target supplied by the eval pack, at least one target from every top-level FPF family, and the deterministic syntax-risk strata below. Compare only cited effective source ranges plus minimal adjacent heading context, consulting the patch and upstream bytes when a selected range differs.

State the semantic selection rule, selected targets, omitted population, and the limit of the resulting claim. Never describe sampled semantic review as exhaustive source equivalence.

## Required issue families

Every issue family is mandatory. Mark each `PASS`, `FAIL`, or `INSUFFICIENT EVIDENCE` with exact evidence.

### 1. Source identity, safety, and authority

- The external `ailev/FPF` checkout is read-only and its committed HEAD matches the revision encoded in `.fpf-original-<full-upstream-head>/`.
- The revision-named tracked package contains every upstream-tracked file, optional colocated patches, and metadata; replaying any patches over the recorded commit reproduces every effective byte and SHA-256 exactly.
- The effective package, including FPF, narrativization, newly tracked files, metadata, and patches, is staged under `.runtime/original-fpf-sources`; monolithic files do not appear unscoped at the toolkit root or inside a generated graph.
- Candidate, backup, eval pack, deterministic output, and source locator all refer to the same intended conversion event.

Historical regression: an unscoped vault-visible root `FPF-Spec.md` could crash or pollute Obsidian; revision-named hidden source packaging and runtime staging prevent that while keeping repository patches reviewable.

### 2. Transaction, backup, and rollback integrity

- `FPF-Knowledge-Graph.bak/` is the complete predecessor, not a partial or same-revision copy of the candidate.
- Rotation replaces an older backup transactionally.
- A failed conversion restores both candidate and backup byte-for-byte and leaves no partial or mixed-revision source stage.
- Evaluation never mistakes an interrupted partial tree for a candidate.
- Staged effective sources and graph backups remain available through evaluation and are cleared only by the acceptance finalizer after revision-bound PASS evidence and a final complete deterministic-suite pass. The tracked revision-named source package and patches remain.

### 3. Completeness and exact reconstruction

- Every source H1/H2 unit expected by the parser has exactly one correct hub or page carrier.
- Every expected generated Markdown path exists; no unexpected, misplaced, stale, or orphan Markdown path remains.
- Clean rebuilds remove carriers deleted or moved upstream.
- Counts for hubs, pages, IDs, Markdown files, relations, and indexes agree across source-derived expectations, raw tree, validation report, and eval pack.

Historical regression: large upstream changes created extensive moves and renames; checking only the report missed stale tree state.

### 4. Boundary parsing and source-range fidelity

- H1 becomes the intended hub, H2 becomes the intended page, and H3+ remains inside the H2 page.
- Headings inside fenced code are not parsed as structure.
- table rows shaped like `# | ...` are not parsed as H1 headings.
- `source_lines` are present where required, within source bounds, and delimit exactly the intended source unit.
- Adjacent units are neither fused nor truncated; preface, readme, unprefixed, reserved, and annex sections stay in their correct families.

### 5. Normative content and Markdown preservation

- Selected generated bodies preserve canonical wording, order, lists, blockquotes, tables, code fences, inline code, ordinary Markdown links, and heading hierarchy except for declared projection transformations.
- Status, normativity, page type, mode, terms, and parent metadata agree with the source unit.
- YAML quoting and escaping preserve titles and values containing punctuation or Unicode.
- No converter-authored interpretation silently enters normative content.

### 6. Linkification and rendering regressions

- Bracketed source constructs such as `[B.2.P: note]` never become malformed triple-bracket links such as `[[[...]]`.
- Existing wiki-links and ordinary Markdown links are protected from nested or duplicate linkification.
- Backticked identifiers remain syntactically valid and link only when intended.
- Wiki-link aliases inside Markdown tables do not introduce raw `|` column separators or phantom columns.
- Removing all-empty table columns does not remove meaningful cells, damage separator alignment, or alter non-table text.
- Code blocks, link destinations, URL fragments, and filename-like tokens are not spuriously linkified.

Historical regressions: malformed triple-bracket links and table pipe corruption required dedicated generator protections.

### 7. Identity stability and collision handling

- Every `fpf_id` is unique and mapped to exactly one current carrier.
- Stable upstream IDs remain stable across candidate and backup even when titles or paths change.
- Added, removed, moved, and retitled IDs in the eval pack match the raw trees and source evolution.
- Duplicate titles or sanitized names receive deterministic, non-overwriting disambiguation.
- Every removed ID has recoverable upstream evidence; conversion must not silently drop it.

### 8. Folder topology and reading order

- Part roots, ID-prefix folders, owner pages, descendants, and leaf pages follow the declared topology.
- Source order, not lexical ID order, controls numbered folder and filename prefixes where specified.
- Top-level `.0` pages, alphanumeric IDs, descendant-owning pages, unprefixed H2 pages, preface/readme pages, and reserved/annex sections route correctly.
- A title-only change does not detach descendants, create duplicate folders, or reorder unrelated siblings.

### 9. Filesystem portability and path hygiene

- Path segments have no unsafe characters, leading/trailing spaces or dots, hidden generated files, unsupported file types, or embedded symlinks. Empty directory shells retained by a managed filesystem contain no graph content and are reported separately rather than counted as generated paths.
- Unicode is NFC-normalized; dash-like characters are normalized according to the filename contract.
- Segment byte lengths stay within the portable bound and no case-insensitive collision exists.
- Paths and output bytes are independent of checkout location, username, path separator, locale, and filesystem case behavior.
- `.DS_Store` and equivalent platform metadata are excluded from generated-content counts and deterministic comparisons; their presence is reported separately, not treated as FPF content.

### 10. Provenance and replayability

- Every page, hub, and index has the exact source filename, source revision, source SHA-256, and explicit generation date required by the profile.
- Validation reports use portable source/output names rather than stale absolute checkout paths.
- Repository rename or relocation does not change generated bytes when all declared inputs are unchanged.
- Two clean builds from identical source bytes, source revision, generation date, and converter revision produce byte-identical trees.
- Changing a declared input changes the corresponding provenance and nothing unrelated.

Historical regressions: absolute/path-sensitive report fields became stale after checkout rename; implicit current dates and missing source hashes made rebuilds non-replayable.

### 11. Navigation, indexes, and reachability

- Every page is reachable from the master index or its intended hub; no page is an unintended navigation orphan.
- Hub child counts and parent links agree bidirectionally.
- Master, relation, and term indexes reference current paths and contain no stale backup paths.
- Term extraction and index truncation indicators are honest; a present source term is not silently assigned to the wrong page.
- A selected user query can recover the intended pattern through title, ID, hub, term, or relation navigation without loading the monolith.

Broader risk: a link may resolve mechanically yet route to the wrong semantic target.

### 12. Relation extraction and classification

- Relation labels, direction, multiplicity, and targets match the selected source declarations.
- Frontmatter relations and the relation index agree occurrence-for-occurrence.
- Resolved links target the intended pattern, not merely an existing path with a similar ID or title.
- Every unresolved relation occurrence is exposed, not only a sample, and classified against the source catalog.
- Classify catalog targets marked as current or stable but missing a generated pattern body, and uncataloged numeric targets, as upstream-source defects. An explicitly `Planned` catalog target may remain an upstream warning when the source states that it supplies no current governing force. Legacy aliases and non-catalog tokens also remain visible and classified. These conditions block a claim that the upstream FPF source is internally complete, but they do not block conversion acceptance when every occurrence is exposed exactly and the projection neither invents a carrier nor marks the target resolved. Hidden or misclassified occurrences, fabricated generated content, and spurious resolution are conversion defects.

Historical condition: seven unresolved relations were legitimate source-family placeholders, so zero unresolved relations is not the universal acceptance rule; correct exhaustive classification is.

### 13. Eval-pack and validator independence

- Eval-pack counts and target paths are recomputed from raw current and backup trees.
- Risk strata include bracket syntax, tables, fenced code, non-ASCII paths, long paths, relation-rich pages, unprefixed pages, duplicate-title disambiguation, added/removed/moved/retitled IDs, and every top-level family.
- The evaluator checks at least one raw invariant not derived through the same parser as the converter.
- A validator and converter agreeing through shared faulty parsing is not accepted as independent evidence.
- Missing targets or a biased pack are classified as `eval-pack defect`, not silently compensated for by evaluator preference.

### 14. Repository and consumer compatibility

- Repository validation, script-architecture validation, reproducibility, installer tests, settings synchronization, and patch hygiene pass on the same candidate.
- Acceptance finalization rejects missing, stale, non-PASS, revision-mismatched, or tree-digest-mismatched evidence and preserves staged sources and backups on any final-suite failure.
- `$fpf` prompts contain no stale hard-coded graph IDs, paths, revisions, or retrieval assumptions.
- The end-user `$fpf` package remains separate from both graph service skills; global installation excludes the service skills.
- Project discovery exposes exactly the two graph service skills and excludes the end-user `$fpf` package, preventing duplicate Project and Personal skill entries.
- The generated graph remains usable through portable filesystem access and Obsidian wiki-link semantics.

## Syntax-risk strata for semantic inspection

Select at least one current carrier for every populated stratum:

- bracketed FPF reference adjacent to punctuation;
- existing wiki-link or Markdown link;
- Markdown table with generated links and with an all-empty source column;
- fenced code containing heading-like or ID-like text;
- relation section using heading, bold-label, and continuation bullets;
- non-ASCII title or path;
- long sanitized title and duplicate/similar title;
- alphanumeric and deeply nested FPF IDs;
- unprefixed H2 page under preface, readme, and a Part hub;
- page added, removed, moved, or retitled since backup;
- page with unresolved source-family placeholder relation;
- root representative from every current top-level ID family.

If a stratum is absent, record `not present in candidate` with the raw search evidence. Do not silently omit it.

## Finding classification

Classify every non-pass as exactly one of:

- `converter defect`;
- `deterministic-test defect`;
- `eval-pack defect`;
- `repository-integration defect`;
- `upstream-source condition`;
- `unavailable evidence`.

A historical probe that is not exercised by the current deterministic suite is a coverage gap. Classify the missing regression check as a test or eval-pack defect even when the sampled candidate currently looks correct.
