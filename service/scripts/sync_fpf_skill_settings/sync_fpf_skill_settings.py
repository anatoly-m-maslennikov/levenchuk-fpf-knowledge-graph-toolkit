"""Synchronize portable package defaults into FPF skill contracts."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from service.scripts.init_settings.init_settings import EXAMPLE_PATH, read_skill_settings


ROOT = Path(__file__).resolve().parents[3]
SETTINGS_TARGETS = (
    ("references/fpf-analysis-contract.md", False),
    ("prompts/fpf-plan.md", True),
)
START = "<!-- output-settings:start -->"
END = "<!-- output-settings:end -->"


def read_settings(path: Path = EXAMPLE_PATH) -> dict[str, str]:
    values, _ = read_skill_settings(
        path, path, create_if_missing=False,
    )
    return values


def _report_contract(is_plan: bool) -> str:
    if is_plan:
        return (
            "`$fpf plan` is the exception: it remains ephemeral, ignores report persistence and `report_style`, "
            "never creates a report file, and never loads `references/fpf-report-persistence.md`, even though "
            "the suite default is on."
        )
    return (
        'Return the complete artifact in chat. When `save_report = "on"`, consult `report_style`, then load '
        "only `references/fpf-report-persistence.md` and follow it; never replace chat delivery with a summary "
        "or pointer."
    )


def render_block(settings: dict[str, str], *, is_plan: bool) -> str:
    return f'''{START}
## Output and report settings

Embedded defaults: `output_language = "{settings["output_language"]}"` (`auto`, `en`, or `ru`); `output_style = "{settings["output_style"]}"`; `fpf_terms_explained = "{settings["fpf_terms_explained"]}"`; `save_report = "{settings["save_report"]}"` (`on` or `off`); `report_style = "{settings["report_style"]}"` (`plain` or `caprmedio`, consulted only when saving is on). Explicit user instruction overrides the installed `.fpf-runtime.toml` defaults, which override these embedded defaults. Skill preferences are never read from a target repository's `.caprmedio/settings.toml`; CAPRMEDIO remains an optional report adapter selected by the external skill setting.
Resolve `output_language` before output style. `en` means English and loads no language resource. `ru` means Russian and loads only `references/fpf-output-language-ru.md`. With `auto`, use Russian when the user's invocation or residual task contains meaningful Russian Cyrillic text; otherwise use English. Never infer language from quoted source text, identifiers, paths, or citations alone. Never preload an unselected language resource.
For output style, load at most one mode resource:
- `natural`: load none; allow FPF terms. On first use, explain each term per `fpf_terms_explained`: `full` up to three short lines, `short` one sentence, `off` none.
- `general`: load only `references/fpf-output-style-general.md`.
- `ste`: load only `references/fpf-output-style-ste.md`.
Never preload an unselected resource. If the selected file is missing, report it; do not substitute. Keep exact FPF locators and source paths in compact evidence or source records, not narrative prose.
{_report_contract(is_plan)}
{END}
'''


def replace_block(text: str, block: str, path: Path) -> str:
    pattern = re.compile(rf"{re.escape(START)}(?:\n.*)?\n{re.escape(END)}\n?", re.DOTALL)
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise ValueError(f"{path} must contain exactly one generated output settings block")
    return text[: matches[0].start()] + block + text[matches[0].end() :]


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="check synchronization (default)")
    mode.add_argument("--apply", action="store_true", help="write generated skill blocks")
    return parser.parse_args()


def _sync(apply: bool) -> tuple[list[Path], list[Path]]:
    settings = read_settings(EXAMPLE_PATH)
    targets = [(ROOT / "skills/fpf.skill" / relative, is_plan) for relative, is_plan in SETTINGS_TARGETS]
    paths = [path for path, _ in targets]
    missing = [path for path in paths if not path.is_file()]
    if missing:
        raise ValueError(f"missing methodology skill: {missing[0].relative_to(ROOT)}")
    stale: list[Path] = []
    for path, is_plan in targets:
        original = path.read_text(encoding="utf-8")
        updated = replace_block(original, render_block(settings, is_plan=is_plan), path)
        if original != updated:
            stale.append(path)
            if apply:
                path.write_text(updated, encoding="utf-8")
    return paths, stale


def main() -> int:
    args = _arguments()
    try:
        paths, stale = _sync(args.apply)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if stale and not args.apply:
        for path in stale:
            print(f"OUT OF SYNC: {path.relative_to(ROOT)}", file=sys.stderr)
        return 1
    print(f"FPF skill settings {'applied' if args.apply else 'checked'} for {len(paths)} contracts")
    return 0
