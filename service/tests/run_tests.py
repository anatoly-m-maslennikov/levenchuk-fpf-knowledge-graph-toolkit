"""Run deterministic checks for graph conversion from original FPF."""

from pathlib import Path

from .suite_runner import main as run


ROOT = Path(__file__).resolve().parents[2]
CASES = Path(__file__).parent / "test_cases.json"


def main() -> int:
    return run(ROOT, CASES)


if __name__ == "__main__":
    raise SystemExit(main())
