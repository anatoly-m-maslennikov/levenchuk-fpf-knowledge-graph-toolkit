"""Pure manager for the local FPF skill quality gate."""


def main() -> int:
    from .fpf_skill_quality_gate_workers.cli import main as run

    return run()
