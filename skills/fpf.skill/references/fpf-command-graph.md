# FPF Markdown Command Graph

This file is the complete runtime routing index. It is Markdown data, not an instruction to execute another program. Load it for every non-fast-Help invocation. New requests are Plan-first; direct analytical execution requires an explicit operator instruction to proceed without a Plan.

## Routing precedence

1. Strip one leading `$fpf` or textual `/fpf` marker and preserve the remaining original text.
2. Apply the manager-supplied authority mode. `plan-first` is the default for every new request. `direct-without-plan` is valid only after an explicit operator bypass instruction; never infer it from a command, `+` stack, `run`, `do it`, `now`, or urgency.
3. In plan-first mode, recognize an explicit `plan` prefix, one command, or a legal `<command> + ...` stack as constraints on the proposed Plan. They never execute before exact `do`.
4. Treat spaced ` + ` as a requested stack only when every segment before the shared task starts with a complete canonical command or alias. Otherwise `+` is ordinary task text. A valid requested stack is normalized to canonical commands and returned as a Plan.
5. Prefer the longest complete command or alias at the beginning of the invocation. Preserve every character after that matched span as the task. Remove only an explicit without-Plan authority directive from the residual task.
6. Without an explicit command, use routing cues only when one analytical node is clearly stronger than every alternative. Match complete words or phrases; never match substrings such as `API` inside `capital`.
7. In plan-first mode, return the smallest useful Plan even for one selected node. In direct-without-plan mode, ambiguity produces a blocking question or exact `STOP_*` state; it never silently changes to a Plan at `step-001/`.
8. A correction suggestion is never an executed route. Select at most one task profile after selecting the command; a profile specializes context and never changes analytical intent.

Canonical command identifiers remain English. Russian commands and aliases select the same nodes. `help` and `plan` never save reports; every node marked `yes` under `Saves report` is analytical and may save one final report only after exact `do` or an explicit without-Plan bypass.

## Areas and profile files

| Area | English cues | Russian cues | Profile file |
|---|---|---|---|
| `framework` | `framework`, `frameworks`, `framework development` | `фреймворк`, `фреймворки`, `разработка фреймворков` | [framework profiles](../profiles/fpf-profiles-framework.md) |
| `software` | `software`, `software development`, `code` | `софт`, `ПО`, `разработка ПО`, `программирование` | [software profiles](../profiles/fpf-profiles-software.md) |
| `skills` | `skill`, `skills`, `skill development` | `навык`, `навыки`, `разработка навыков` | [skills profiles](../profiles/fpf-profiles-skills.md) |

Load no profile file when the area is absent or ambiguous. Load only the selected area's file and select at most one profile by complete alias or routing-cue match.

## Command nodes

| ID | Command | Russian command | Aliases | Routing cues | Prompt | Saves report | FPF bindings |
|---|---|---|---|---|---|---|---|
| `help` | `help` | `справка` | `?`<br>`commands`<br>`usage`<br>`справка`<br>`помощь`<br>`команды`<br>`как пользоваться` | — | [Help](../prompts/help/en/fpf-help.md) | no | — |
| `plan` | `plan` | `план` | `planner`<br>`route`<br>`workflow`<br>`which skill`<br>`план`<br>`планировщик`<br>`маршрут`<br>`рабочий процесс`<br>`какой навык` | `plan`<br>`route`<br>`sequence`<br>`workflow`<br>`which skill`<br>`what should i use`<br>`then`<br>`план`<br>`маршрут`<br>`последовательност`<br>`рабочий процесс`<br>`какой навык`<br>`что использовать`<br>`затем` | [Plan](../prompts/fpf-plan.md) | no | — |
| `problem-frame` | `problem frame` | `рамка проблемы` | `frame problem`<br>`task frame`<br>`problem shaping`<br>`рамка проблемы`<br>`сформулировать проблему`<br>`постановка задачи` | `problem frame`<br>`task frame`<br>`problem statement`<br>`acceptance boundary`<br>`task signature`<br>`problem`<br>`requirements`<br>`clarify`<br>`рамка проблемы`<br>`постановка задачи`<br>`требования`<br>`уточнить` | [Problem frame](../prompts/fpf-problem-frame.md) | yes | `C.22.2@primary_method`<br>`C.22@routing_method` |
| `structure-recover` | `structure recover` | `восстановить структуру` | `recover structure`<br>`current structure`<br>`as-is map`<br>`map current`<br>`восстановить структуру`<br>`текущая структура`<br>`карта текущего состояния` | `structure recover`<br>`recover structure`<br>`map current`<br>`current structure`<br>`as is`<br>`current state`<br>`recover`<br>`восстановить структуру`<br>`текущая структура`<br>`текущее состояние` | [Structure recover](../prompts/fpf-structure-recover.md) | yes | `A.22@primary_method`<br>`C.33@result_projection` |
| `applicability-scan` | `applicability scan` | `скан применимости` | `applicability`<br>`scan`<br>`relevant patterns`<br>`скан применимости`<br>`применимость`<br>`релевантные паттерны`<br>`подходящие паттерны` | `apply`<br>`applicable`<br>`applicability`<br>`relevant`<br>`fpf patterns`<br>`which patterns`<br>`what fpf can contribute`<br>`применим`<br>`релевант`<br>`подходящ`<br>`паттерны fpf` | [Applicability scan](../prompts/fpf-applicability-scan.md) | yes | `E.11.PUR@routing_method` |
| `sota-harvest` | `sota harvest` | `обзор исследований` | `sota`<br>`state of the art`<br>`research harvest`<br>`обзор sota`<br>`состояние области`<br>`обзор исследований`<br>`карта исследований` | `sota`<br>`state of the art`<br>`research`<br>`field map`<br>`evidence map`<br>`landscape`<br>`current evidence`<br>`исследован`<br>`состояние области`<br>`актуальные данные` | [SOTA harvest](../prompts/fpf-sota-harvest.md) | yes | `G.2@primary_method` |
| `options-explore` | `options explore` | `исследовать варианты` | `options`<br>`explore options`<br>`alternatives`<br>`варианты`<br>`исследовать варианты`<br>`альтернативы`<br>`сравнить варианты` | `options`<br>`alternatives`<br>`candidates`<br>`explore`<br>`compare`<br>`non-obvious`<br>`вариант`<br>`альтернатив`<br>`кандидат`<br>`сравн` | [Options explore](../prompts/fpf-options-explore.md) | yes | `B.5.2.1@primary_method`<br>`G.9@conditional_method` when alternatives require benchmark or parity comparison |
| `evaluation-design` | `evaluation design` | `дизайн оценки` | `design evaluation`<br>`evaluation frame`<br>`test strategy`<br>`test plan`<br>`verification plan`<br>`дизайн оценки`<br>`план тестирования`<br>`стратегия тестирования`<br>`план проверки` | `evaluation design`<br>`evaluation frame`<br>`evaluation plan`<br>`gate profile`<br>`test strategy`<br>`verification plan`<br>`success criteria`<br>`acceptance tests`<br>`quality criteria`<br>`дизайн оценки`<br>`критерии качества` | [Evaluation design](../prompts/fpf-evaluation-design.md) | yes | `E.22@primary_method`<br>`A.19.ECS@result_projection` |
| `design-challenge` | `design challenge` | `проверка дизайна` | `challenge`<br>`challenge design`<br>`critique`<br>`stress test`<br>`проверка дизайна`<br>`критика дизайна`<br>`стресс тест дизайна`<br>`оспорить дизайн` | `design`<br>`proposal`<br>`challenge`<br>`critique`<br>`stress test`<br>`before implementation`<br>`architecture`<br>`taxonomy`<br>`дизайн`<br>`до реализации` | [Design challenge](../prompts/fpf-design-challenge.md) | yes | `E.11.PUA@routing_entrypoint` |
| `decision-synthesize` | `decision synthesize` | `синтез решения` | `decision`<br>`decide`<br>`synthesize decision`<br>`adr`<br>`синтез решения`<br>`принять решение`<br>`выбрать решение` | `decision`<br>`decide`<br>`choose`<br>`selection`<br>`adr`<br>`evaluated alternatives`<br>`reopen trigger`<br>`решени`<br>`выбер` | [Decision synthesize](../prompts/fpf-decision-synthesize.md) | yes | `C.32.PAD@primary_method`<br>`C.32.ADR@result_projection` |
| `quality-improve` | `quality improve` | `улучшение качества` | `improve`<br>`quality`<br>`improvement loop`<br>`улучшение качества`<br>`улучшить качество`<br>`повысить качество`<br>`цикл улучшения`<br>`улучшение` | `improve`<br>`improvement`<br>`quality`<br>`versioned`<br>`baseline`<br>`re-evaluate`<br>`evaluation frame`<br>`улучш`<br>`качеств`<br>`повторно оцен` | [Quality improve](../prompts/fpf-quality-improve.md) | yes | `E.23@primary_method` |
| `alignment-audit` | `alignment audit` | `аудит согласованности` | `audit`<br>`alignment`<br>`final review`<br>`closure audit`<br>`аудит согласованности`<br>`проверка согласованности`<br>`финальная проверка`<br>`аудит закрытия` | `audit`<br>`alignment`<br>`implemented`<br>`accepted work`<br>`final review`<br>`closure`<br>`regression`<br>`verify`<br>`аудит`<br>`согласован`<br>`реализован`<br>`регресси` | [Alignment audit](../prompts/fpf-alignment-audit.md) | yes | `E.11.PUA@routing_entrypoint` |

## Legal composition handoffs

An edge permits only an explicit user-requested stack. It never authorizes automatic execution.

Each row is a typed handoff contract. The producer must emit the declared output, the consumer receives only the declared input, and the edge runs only when its evidence and gate predicate are satisfied. Otherwise stop with the exact declared stop state and leave the remaining suffix unexecuted.

| From | To | Producer output | Consumer input | Required evidence | Gate predicate | Stop state |
|---|---|---|---|---|---|---|
| `problem-frame` | `structure-recover` | accepted problem frame and scope boundary | bounded subject requiring an as-is map | identified target and accessible current-state carriers | frame is accepted and recovery is necessary | `STOP_NO_CURRENT_STATE_EVIDENCE` |
| `problem-frame` | `applicability-scan` | accepted bounded question | question whose relevant FPF patterns are unknown | explicit scope, receiving use, and exclusions | question is bounded enough to screen patterns | `STOP_UNBOUNDED_QUESTION` |
| `problem-frame` | `sota-harvest` | accepted research question | bounded evidence-harvest request | evidence boundary, recency need, and receiving use | external current evidence is needed and permitted | `STOP_UNBOUNDED_RESEARCH` |
| `problem-frame` | `options-explore` | accepted problem-side result | option-generation frame | accepted problem, constraints, and protected trade-offs | alternatives are warranted without reopening the frame | `STOP_NO_OPTION_BASIS` |
| `problem-frame` | `evaluation-design` | accepted target and receiving use | evaluation target and decision use | target identity, success boundary, and owner | an evaluation can change a declared decision or gate | `STOP_NO_EVALUATION_TARGET` |
| `applicability-scan` | `structure-recover` | selected applicable structures to inspect | bounded recovery focus | pattern selection plus identified current carriers | recovery is needed to determine whether patterns obtain | `STOP_NO_CURRENT_STATE_EVIDENCE` |
| `applicability-scan` | `sota-harvest` | bounded methodological evidence gaps | research frame for unresolved current claims | selected patterns and exact unresolved claims | current external evidence is required to resolve the gaps | `STOP_UNBOUNDED_RESEARCH` |
| `applicability-scan` | `options-explore` | applicable pattern set with limits | option-generation basis | supported patterns, forces, and exclusions | patterns permit materially distinct candidates | `STOP_NO_OPTION_BASIS` |
| `applicability-scan` | `evaluation-design` | governing evaluation patterns | evaluation-method constraints | supported pattern claims and receiving quality question | patterns constrain a testable evaluation | `STOP_NO_EVALUATION_TARGET` |
| `sota-harvest` | `options-explore` | bounded current evidence map | evidence-backed option basis | sourced findings, conflicts, and coverage limits | evidence supports distinct candidates without silent choice | `STOP_NO_OPTION_BASIS` |
| `sota-harvest` | `evaluation-design` | current evaluation-practice map | evidence-backed evaluation inputs | sourced practices, limits, and applicability conditions | practices can be translated into target-specific checks | `STOP_NO_EVALUATION_TARGET` |
| `sota-harvest` | `design-challenge` | bounded current evidence map | evidence-grounded proposal challenge | sourced findings, applicability limits, and a concrete proposal or current design | the proposal can be distinguished from the evidence map and challenged against it | `STOP_NO_CHALLENGE_TARGET` |
| `structure-recover` | `options-explore` | verified current-state structure | baseline and change boundary | carrier-backed as-is map and unresolved structural gaps | baseline is sufficient to distinguish alternatives | `STOP_NO_OPTION_BASIS` |
| `structure-recover` | `evaluation-design` | exact bearers, relations, and boundaries | observable evaluation surface | verified carriers and relation evidence | target observations can be bound to named bearers | `STOP_NO_EVALUATION_TARGET` |
| `structure-recover` | `design-challenge` | verified recovered current state | proposal-versus-current-state challenge basis | as-is carriers and separately identified proposal | proposal and current state are distinguishable | `STOP_NO_CHALLENGE_TARGET` |
| `options-explore` | `evaluation-design` | candidate set and comparison needs | candidates requiring comparable tests | distinct candidates, forces, and protected trade-offs | one evaluation frame can compare candidates fairly | `STOP_NO_EVALUATION_TARGET` |
| `options-explore` | `design-challenge` | explicit candidate proposal | bounded challenge target | selected candidate identity and stated assumptions | one proposal is concrete enough to challenge | `STOP_NO_CHALLENGE_TARGET` |
| `options-explore` | `decision-synthesize` | evaluated alternatives with trade-offs | comparable decision set | alternatives, criteria, evidence, and owner | alternatives are comparable and decision authority exists | `STOP_NO_COMPARABLE_ALTERNATIVES` |
| `evaluation-design` | `design-challenge` | declared criteria, tests, and failure predicates | evaluation-aware challenge frame | target-bound checks and stop conditions | proposal can be challenged against declared criteria | `STOP_NO_CHALLENGE_TARGET` |
| `evaluation-design` | `decision-synthesize` | comparable evaluation evidence | decision evidence set | results for every candidate under one declared frame | evidence is complete enough for the owner to decide | `STOP_NO_COMPARABLE_ALTERNATIVES` |
| `evaluation-design` | `quality-improve` | rerunnable evaluation frame | bounded versioned improvement target | baseline result, target version, and mutation authority | an authorized change can be re-evaluated | `STOP_NO_AUTHORIZED_CHANGE` |
| `design-challenge` | `decision-synthesize` | accepted challenge findings and residual risks | challenged decision set | dispositions for blocking findings and named owner | remaining alternatives are comparable after challenge | `STOP_NO_COMPARABLE_ALTERNATIVES` |
| `design-challenge` | `quality-improve` | accepted findings mapped to bounded repairs | authorized improvement target | accepted issue IDs, recoverable baseline, and authority | repair scope is bounded and target mutation is authorized | `STOP_NO_AUTHORIZED_CHANGE` |
| `decision-synthesize` | `quality-improve` | recorded decision and authorized change set | decision-bounded improvement target | decision record, owner, baseline, and change authority | implementation of the selected change is authorized | `STOP_NO_AUTHORIZED_CHANGE` |
| `quality-improve` | `alignment-audit` | changed target plus rerun evidence | closure-audit target | before and after identities, applied fixes, and test evidence | declared repairs were actually applied and can be audited | `STOP_NO_APPLIED_CHANGE` |
| `design-challenge` | `alignment-audit` | accepted findings with claimed applied repairs | targeted closure-audit set | issue-to-repair mapping and changed carrier evidence | every audited repair is applied, not merely proposed | `STOP_NO_APPLIED_CHANGE` |

## FPF source resolution

Each binding is `<stable-id>@<relation>`. Resolve each selected command/profile stable ID through the exact ID row in `<repository_root>/FPF-Knowledge-Graph/00_Index/FPF - Index.md`, follow that row's page link, and verify the page frontmatter contains the same `fpf_id`. Load no unselected page. A `conditional_method` is loaded only when its stated condition is true.

From each selected page, inspect only the available Problem frame, Problem, Forces, Solution, and Consequences sections needed for the task. If a required section is absent or a needed section is too large to inspect completely, report that limitation instead of inventing content.
