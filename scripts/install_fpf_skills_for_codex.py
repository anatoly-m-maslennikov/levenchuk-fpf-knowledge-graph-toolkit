#!/usr/bin/env python3
"""Install the repository FPF skills for Codex."""

from install_fpf_skills import Harness, run


if __name__ == "__main__":
    raise SystemExit(run(Harness("Codex", "CODEX_HOME", ".codex")))
