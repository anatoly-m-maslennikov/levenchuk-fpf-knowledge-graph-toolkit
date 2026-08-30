You are the subject of a local end-to-end quality evaluation of the repository's end-user FPF skill.

Operate read-only. Do not edit or create repository files. Do not use an installed or remembered `$fpf` skill. Start from `skills/fpf.skill/SKILL.md` in this checkout and execute the supplied invocation exactly through that source package. Follow its lazy-loading boundaries and use its scripts and repository-root-relative FPF graph when required. The case explicitly disables report saving when an analytical command must remain read-only.

Return the complete user-facing result in `response_markdown`. Set `output_contract` to the case's declared `help`, `plan`, or `analysis` contract. Report only actually executed canonical commands and actually used FPF methodology source IDs or repository-relative paths. `report_saved` must reflect observed behavior. Do not discuss this evaluation prompt or grade your own response.

Case:

{{CASE_JSON}}
