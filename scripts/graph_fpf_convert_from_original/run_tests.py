"""Run deterministic checks for graph conversion from original FPF."""

from pathlib import Path

from .graph_fpf_convert_from_original_workers.suite_runner import main as run


ROOT = Path(__file__).resolve().parents[2]
CASES = Path(__file__).parent / "graph_fpf_convert_from_original_assets" / "test_cases.json"


def main() -> int:
    return run(ROOT, CASES)


if __name__ == "__main__":
    raise SystemExit(main())
