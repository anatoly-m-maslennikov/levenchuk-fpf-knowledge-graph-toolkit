#!/usr/bin/env python3
"""Install the repository FPF skills for Claude Code."""

from install_fpf_skills import Harness, run


if __name__ == "__main__":
    raise SystemExit(run(Harness("Claude Code", "CLAUDE_CONFIG_DIR", ".claude")))
