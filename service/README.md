# Repository service

This boundary contains the toolkit's repository-service implementation:

- `scripts/` contains converters, graph builders, validators, settings synchronization, and the project service-skill installer;
- `skills/` contains only the two project-discovered graph conversion service skills;
- `tests/` contains every repository test, the deterministic case catalog, and its suite runner.

The end-user `$fpf` package, its runtime helpers, and its global installer remain under the repository's top-level `skills/` boundary. Repository commands use the `service.scripts.<tool>` module path. Project-module bytecode is redirected into the ignored `.runtime/pycache` boundary; uv's ignored environment remains isolated under `.venv`.
