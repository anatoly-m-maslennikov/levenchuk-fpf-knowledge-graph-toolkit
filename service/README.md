# Repository service

This boundary contains the toolkit's repository-service implementation:

- direct child packages contain converters, graph builders, validators, settings synchronization, and the project service-skill installer;
- `skills/` contains only the two project-discovered graph conversion service skills;
- `tests/` contains every repository test, the deterministic case catalog, and its suite runner.

No `scripts/` compatibility package is retained. The end-user `$fpf` package, its runtime helpers, and its global installer remain under the repository's top-level `skills/` boundary. Python bytecode belongs only under the ignored `.runtime/pycache` boundary.
