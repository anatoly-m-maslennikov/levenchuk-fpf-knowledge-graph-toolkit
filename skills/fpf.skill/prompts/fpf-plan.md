# FPF Plan

<!-- output-settings:start -->
## Output and report settings

Embedded defaults: `output_language = "auto"` (`auto`, `en`, or `ru`); `output_style = "general"`; `fpf_terms_explained = "off"`; `save_report = "on"` (`on` or `off`); `report_style = "plain"` (`plain` or `caprmedio`, consulted only when saving is on). Explicit user instruction overrides the installed `.fpf-runtime.toml` defaults, which override these embedded defaults. Skill preferences are never read from a target repository's `.caprmedio/settings.toml`; CAPRMEDIO remains an optional report adapter selected by the external skill setting.
Resolve `output_language` before output style. `en` means English and loads no language resource. `ru` means Russian and loads only `references/fpf-output-language-ru.md`. With `auto`, use Russian when the user's invocation or residual task contains meaningful Russian Cyrillic text; otherwise use English. Never infer language from quoted source text, identifiers, paths, or citations alone. Never preload an unselected language resource.
For output style, load at most one mode resource:
- `natural`: load none; allow FPF terms. On first use, explain each term per `fpf_terms_explained`: `full` up to three short lines, `short` one sentence, `off` none.
- `general`: load only `references/fpf-output-style-general.md`.
- `ste`: load only `references/fpf-output-style-ste.md`.
Never preload an unselected resource. If the selected file is missing, report it; do not substitute. Keep exact FPF locators and source paths in compact evidence or source records, not narrative prose.
`$fpf plan` is the exception: it remains ephemeral, ignores report persistence and `report_style`, never creates a report file, and never loads `references/fpf-report-persistence.md`, even though the suite default is on.
<!-- output-settings:end -->

Produce a read-only **FPF Skill Plan** for one question. Route work among the available FPF prompt nodes; do not answer the question, inspect the FPF methodology, or execute the proposed calls.

## Route contract

1. Restate the question as one bounded receiving use. Identify the target state: open question, research need, proposal, evaluated alternatives, versioned improvement target, or implemented/accepted work.
2. Resolve the smallest useful sequence from the available skills. One call is a valid sequence. Do not propose a full lifecycle when the requested result stops earlier.
3. Rewrite every call as a self-contained, copy-ready task. Preserve the user's intent without embedding an expected finding, preferred option, or approval outcome.
4. Make dependencies, independent calls, decision ownership, missing inputs, and stop conditions explicit. The active runtime chooses scheduling.
5. If no available FPF skill fits, return no call and explain which required trigger or input is absent. Never route to `$fpf plan` recursively.

When the router supplies an invalid explicit `+` composition, explain the rejected segment or handoff and return the smallest legal corrected composition or ordinary sequence. Do not execute it. Explicit composition is appropriate only when the user wants one ordered run with one shared task and consolidated result; ordinary proposed sequences remain separate calls unless the user requests stacking.

When the router supplies a valid explicit meta-plan (`mode: plan`, `planned_nodes`, and `execution_disabled = true`), treat the returned ordered nodes as the requested sequence. Do not re-route from keywords, load any analytical prompt, or execute any node. Validate the declared graph handoffs, make the shared task self-contained, expose every run condition and stop gate, and return one copy-ready executable composition for a later user-authorized invocation. The `plan` prefix itself is not part of that copy-ready composition.

When the router supplies `suggestions`, list the possible canonical corrections with the router's evidence and keep them explicitly unselected. A single strong suggestion may be shown as the smallest copy-ready correction, but it remains a proposed invocation: do not silently replace the user's text, execute it, or claim that fuzzy matching selected an analytical node.

## Review campaign routing

When the question cites a prior FPF report, finding, repair, closure check, or review campaign, load `references/fpf-review-campaign.md` before selecting calls. Treat it as routing policy, not as an FPF methodology source. Compare the semantic frontier, carrier frontier, evaluation profile, campaign phase, and finding states first.

- Route a new or materially changed proposal to one full `$fpf design challenge`.
- Route accepted and applied repairs to `$fpf alignment audit`; request `closure` mode when only registered findings and frozen regressions need verification.
- Return no FPF call when the permitted next action is owner disposition, repair application, or targeted mechanical verification outside an FPF skill.
- Return a no-call stop plan when both the semantic frontier and evaluation profile are unchanged and the campaign budget has already been used.
- Never restart a full sequence merely because another skill produced the latest report.

In every campaign route, carry the campaign ID, frontiers, evaluation profile, predecessor, finding fingerprints and states, allowed next transition, and stop condition into each copy-ready task. A no-call route is a complete valid result when the shared protocol requires stop or external action.

## Skill selection

| Skill | Select when the next required result is |
|---|---|
| `$fpf problem frame` | A bounded TaskSignature, accepted problem-side result, acceptance boundary, or honest blocker before solution work |
| `$fpf structure recover` | A current-state map of exact entities, relations, boundaries, rules, and selected structures without redesign |
| `$fpf applicability scan` | The smallest relevant set of direct FPF patterns for a bounded question |
| `$fpf sota harvest` | A current, reconstructible, plural field or evidence map |
| `$fpf options explore` | Diverse candidate options and declared-coordinate comparison without selection |
| `$fpf evaluation design` | A rerunnable evaluation question, characteristic space, check/evidence plan, and stop rules without execution |
| `$fpf design challenge` | A bounded challenge of a proposed or not-yet-implemented design |
| `$fpf decision synthesize` | A recoverable choice among already evaluated alternatives and, when requested, its ADR projection |
| `$fpf quality improve` | A versioned target-change and re-evaluation loop under declared quality coordinates |
| `$fpf alignment audit` | A bounded audit of implemented or accepted work against relevant FPF patterns |

## Sequencing rules

- Order calls by evidence dependency, not by the table order.
- Use the router's optional task profile to specialize the subject and FPF context; never let a profile term such as DDD, TDD, architecture, or skill decide analytical intent by itself.
- Use `$fpf problem frame` when the need, subject, task family, or acceptance boundary is unresolved. Do not use it to restate an already accepted problem or smuggle in a preferred solution.
- Use `$fpf structure recover` when the next result is descriptive current-state structure. Do not substitute proposal critique or implementation audit for recovery.
- Use `$fpf applicability scan` first only when FPF relevance or direct-pattern selection is genuinely unresolved. Do not add it merely because the question mentions FPF.
- Put `$fpf sota harvest` before option generation only when current external evidence or rival traditions are needed.
- Put `$fpf options explore` before `$fpf decision synthesize`; never ask decision synthesis to invent unevaluated alternatives.
- Use `$fpf evaluation design` before improvement, comparison-based decision, or implementation review when characteristics, checks, evidence, or stop rules are missing. It defines an evaluation but never reports a pass.
- Put `$fpf design challenge` before a decision when a concrete unimplemented proposal needs stress-testing. Route implemented work to `$fpf alignment audit` instead.
- Use `$fpf decision synthesize` only when alternatives, evaluation evidence, and project decision authority are recoverable. Otherwise name the missing prerequisite.
- Use `$fpf quality improve` directly when a versioned target, baseline, evaluation frame, and allowed change surface exist. Do not prepend an alignment audit unless FPF alignment is itself a required baseline claim.
- Put `$fpf alignment audit` after implementation or acceptance, never as approval for a proposal.
- Mark calls as independent only when neither consumes the other's output. Name the required handoff or join artifact for the next step; the active runtime chooses scheduling.
- End at the user's receiving use. Present later steps only as conditional follow-ups. When review-campaign policy applies, obey its full-review budget and stop rule.
- For an explicitly requested stack, use only legal graph edges, keep the shared task after the final command, and mark every evidence, authority, application, or decision gate that can stop the composed run before its suffix executes.

## Maintainer evaluation

`references/fpf-routing-scenarios.md` is the repository's behavioral scenario matrix. It is Markdown test evidence for maintainers, not required runtime context. When changing routing rules or the skill catalog, update that matrix and run the repository's deterministic maintenance suite outside the installed skill.

## Address each task

For every proposed call, write an imperative task that includes:

- the target or claim and its current state;
- bounded context and intended receiving use;
- available input artifacts and the exact prior-step handoff, if any;
- project authority or decision owner when relevant;
- the selected skill's native result;
- explicit exclusions and the stop or return condition.

Do not use vague tasks such as “apply FPF” or “review everything.” Do not ask a skill to make an authorization, assurance, gate, or project decision outside its own contract.

## Final delivery

After routing is complete, load `references/fpf-plan-output.md` and follow it as the final authority for response shape. Do not return before applying that finalizer.
