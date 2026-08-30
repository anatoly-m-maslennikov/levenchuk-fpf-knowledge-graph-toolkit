"""Compile repository Python sources using the project runtime cache boundary."""

import compileall
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    paths = (ROOT / "service", ROOT / "skills")
    return 0 if all(compileall.compile_dir(path, quiet=1) for path in paths) else 1


if __name__ == "__main__":
    raise SystemExit(main())
