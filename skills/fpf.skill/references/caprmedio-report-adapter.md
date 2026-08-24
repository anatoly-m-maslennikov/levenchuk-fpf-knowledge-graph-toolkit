# CAPRMEDIO Analysis Report adapter

Load this adapter only when report saving is on and `report_style = "caprmedio"`.

## Preconditions

Verify from accessible current project authority that the workspace is CAPRMEDIO-governed. Resolve the configured control root, current Scope Unit topology, role folders, Analysis Report Atom type, identity and filename rules, required metadata and relations, admission checks, and the project-native Atom creation operation. Filesystem nesting is not structural evidence.

If any required fact or write permission is below 95% confidence, do not guess, do not hand-build a carrier, and do not fall back to plain delivery. Return the complete chat artifact and record the exact unsaved reason in `## Task, scope, and boundaries`.

## Deterministic Scope Unit selection

1. Extract the complete analysis scope from the declared target, bounded context, and evidence actually used.
2. Map every scoped item to a current Scope Unit using project authority.
3. Select the narrowest structural Scope Unit whose declared scope contains the complete analysis scope. Equivalently, choose the deepest proven common container: one feature for a feature-only analysis, its owning layer for multiple features in that layer, and the project root for cross-layer or project-wide analysis.
4. If two candidates are incomparable or containment is not proven, stop unsaved.

### BSEED special case

BSEED layers form an ordered semantic dependency chain, not an ordinary feature tree.

- If the complete analysis scope maps to one BSEED Scope Unit, select that unit.
- If it maps only to multiple BSEED Scope Units, select the lowest downstream BSEED unit whose declared cumulative scope contains every mapped BSEED unit.
- If it combines BSEED scope with project, layer, or feature scope and current authority does not declare one ordinary structural container for both, select the project root only when its declared scope explicitly contains both domains. Otherwise stop unsaved.

Never infer BSEED containment from filenames, folder nesting, numeric prefixes, or presumed layer order.

## Atom creation

Use the project-native Atom creation operation to create exactly one non-normative Analysis Report Atom in the selected Scope Unit's current `Analysis` role folder. Supply the current valid Atom identity, filename, metadata, relations, and admission inputs. Do not directly write around the operation when a governed creator exists.

Preserve the complete four-section FPF artifact as the report body. CAPRMEDIO carrier metadata or a required title may wrap it. Record `Saved report: <path>` and the selected Scope Unit in `## Task, scope, and boundaries`.

Run the project-native admission and integrity checks. A created but unadmitted or invalid carrier is not a saved report result; report the failure and do not claim persistence succeeded.
