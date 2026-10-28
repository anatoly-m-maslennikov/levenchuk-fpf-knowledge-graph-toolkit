# Repository service

This boundary contains the toolkit's repository-service implementation:

- `scripts/` contains converters, graph builders, validators, settings synchronization, and the project service-skill installer;
- `skills/` contains only the two project-discovered graph conversion service skills;
- `tests/` contains every repository test, the deterministic case catalog, and its suite runner.

Graph converters share one builder and transactional backup mechanism. After `graph_fpf_convert_from_original --refresh-source-package` and `--stage-sources`, run `graph_fpf_convert_from_original`, `graph_npf_convert_from_original`, and `graph_cad_convert_from_original` through `uv run -m service.scripts.<tool>`. Their outputs are `FPF-Knowledge-Graph`, `NPF-Knowledge-Graph`, and `CAD-Knowledge-Graph`. Matching `validate_fpf_graph`, `validate_npf_graph`, and `validate_cad_graph` commands check structure, links, and source provenance. Each graph records the packaged upstream HEAD; source metadata also retains each publication's last-change revision.

The end-user `$fpf` package, its runtime helpers, and its global installer remain under the repository's top-level `skills/` boundary. Repository commands use the `service.scripts.<tool>` module path. Project-module bytecode is redirected into the ignored `.runtime/pycache` boundary; uv's ignored environment remains isolated under `.venv`.
