# Repository tools

Each tool owns one directory under `scripts/`. The pure manager is named `<tool_name>.py`; atomic workers live in `<tool_name>_workers/`, reusable non-Python data lives in `<tool_name>_assets/`, and tests live under `tests/`. Python files are capped at 200 lines. Functions, methods, and classes target 25 lines and must not exceed 40.

Run commands from the repository root through the locked `uv` project. `uv` selects the pinned Python version, maintains the ignored `.venv`, and keeps its package cache under ignored `.runtime/uv-cache`; no environment activation, explicit interpreter, or cache-prefix setting is required.

| Tool | Command | Tests |
|---|---|---|
| `build_fpf_obsidian_graph` | `uv run -m scripts.build_fpf_obsidian_graph` | `uv run -m scripts.build_fpf_obsidian_graph.tests.test_reproducible_generation` |
| `check_fpf_skill_graph_compatibility` | `uv run -m scripts.check_fpf_skill_graph_compatibility` | Covered by the converter suite and repository validator |
| `graph_fpf_convert_from_original` | `uv run -m scripts.graph_fpf_convert_from_original` | `uv run -m unittest discover -s scripts/graph_fpf_convert_from_original/tests` |
| `graph_npf_convert_from_original` | `uv run -m scripts.graph_npf_convert_from_original` | `uv run -m unittest scripts.graph_npf_convert_from_original.tests.test_converter` |
| `init_settings` | `uv run -m scripts.init_settings` | `uv run -m unittest scripts.init_settings.tests.test_init_settings` |
| `install_fpf_skills` | `uv run -m scripts.install_fpf_skills.for_codex` or `uv run -m scripts.install_fpf_skills.for_claude` | `uv run -m unittest discover -s scripts/install_fpf_skills/tests` |
| `sync_fpf_skill_settings` | `uv run -m scripts.sync_fpf_skill_settings` | Covered by the converter suite and repository validator |
| `validate_fpf_graph` | `uv run -m scripts.validate_fpf_graph` | `uv run -m unittest scripts.validate_fpf_graph.tests.test_validator` |
| `validate_npf_graph` | `uv run -m scripts.validate_npf_graph` | `uv run -m unittest scripts.validate_npf_graph.tests.test_validator` |
| `validate_repository` | `uv run -m scripts.validate_repository` | Covered by the converter suite |
| `validate_script_architecture` | `uv run -m scripts.validate_script_architecture` | `uv run -m unittest discover -s scripts/validate_script_architecture/tests` |

Run the complete deterministic maintenance suite with `uv run -m scripts.graph_fpf_convert_from_original.run_tests`.

The FPF converter's source flow is `read-only ailev/FPF checkout -> --refresh-source-package -> revision-named tracked package with optional colocated patches -> --stage-sources -> conversion`. `--check-settings` verifies that replaying any patches over the recorded upstream commit produces the stored effective files exactly.

Tests and smoke checks retain their temporary workspaces for operating-system cleanup. This keeps validation compatible with managed runtimes that allow file writes and unlinking but prohibit directory deletion.
