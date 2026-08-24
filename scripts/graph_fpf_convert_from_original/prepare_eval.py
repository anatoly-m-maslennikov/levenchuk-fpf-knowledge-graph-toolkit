"""Prepare a bounded path-and-provenance pack for evaluation."""

from pathlib import Path

from .graph_fpf_convert_from_original_workers.eval_pack import main as run


ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    return run(ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
