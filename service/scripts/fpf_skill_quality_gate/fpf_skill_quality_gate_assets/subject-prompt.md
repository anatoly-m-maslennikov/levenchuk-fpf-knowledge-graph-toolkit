You are the subject of a local end-to-end quality evaluation of the repository's end-user FPF skill.

Operate read-only. Do not edit or create repository files. Do not use an installed or remembered `$fpf` skill. Start from `skills/fpf.skill/SKILL.md` in this checkout and execute the supplied invocation exactly through that source package. Follow its lazy-loading boundaries, its Markdown command/profile graph, and the repository-root-relative FPF graph. Do not run Python, uv, shell commands, or bundled executables as part of the end-user skill runtime. Obey any explicit report-saving instruction, but never claim persistence that the read-only host cannot perform.

Return the complete user-facing result in `response_markdown`. Set `output_contract` to the case's declared `help`, `plan`, or `analysis` contract. In `commands_executed`, report only canonical commands whose native contract actually ran: Help uses `[]`, Plan uses only `["$fpf plan"]`, and a composition omits any consumer that stopped before native execution. In `methodology_sources_used`, report only direct FPF methodology pages materially used in the response; Help pages, skill prompts, runtime contracts, command/profile graphs, project evidence, and tools are not methodology sources. Help and Plan therefore use `[]`. `report_saved` must reflect observed behavior. Do not discuss this evaluation prompt or grade your own response.

Case:

{{CASE_JSON}}
