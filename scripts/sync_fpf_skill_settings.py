#!/usr/bin/env python3
"""Synchronize generated output-language settings into portable FPF skills."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SETTINGS_PATH = ROOT / "skills" / "fpf-route.skill" / "fpf-settings.toml"
SKILL_GLOB = "fpf-*.skill/SKILL.md"
START = "<!-- output-settings:start -->"
END = "<!-- output-settings:end -->"
ALLOWED_OUTPUT_STYLES = {"natural", "general", "ste"}
ALLOWED_EXPLANATION_MODES = {"full", "short", "off"}


def read_settings(path: Path) -> dict[str, str]:
    """Read the intentionally small, flat TOML settings file."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"cannot read {path}: {exc}") from exc

    values: dict[str, str] = {}
    for line_number, line in enumerate(text.splitlines(), start=1):
        content = line.split("#", 1)[0].strip()
        if not content:
            continue
        match = re.fullmatch(r'(output_style|fpf_terms_explained|install_method)\s*=\s*"([a-z]+)"', content)
        if match is None:
            raise ValueError(f"invalid setting syntax at {path}:{line_number}")
        key, value = match.groups()
        if key in values:
            raise ValueError(f"duplicate setting {key!r} in {path}")
        values[key] = value

    if set(values) != {"output_style", "fpf_terms_explained", "install_method"}:
        raise ValueError("settings must contain exactly output_style, fpf_terms_explained, and install_method")
    if values["output_style"] not in ALLOWED_OUTPUT_STYLES:
        raise ValueError("output_style must be natural, general, or ste")
    if values["fpf_terms_explained"] not in ALLOWED_EXPLANATION_MODES:
        raise ValueError("fpf_terms_explained must be full, short, or off")
    if values["install_method"] not in {"copy", "symlink"}:
        raise ValueError("install_method must be copy or symlink")
    return values


def render_block(settings: dict[str, str]) -> str:
    """Render the portable contract embedded in each standalone skill."""
    return f'''{START}
## Output language settings

This package's build-time defaults are `output_style = "{settings["output_style"]}"` and `fpf_terms_explained = "{settings["fpf_terms_explained"]}"`. An explicit user request for a result overrides these embedded defaults.

Apply this contract to the result narrative. Keep exact FPF locators and source paths in compact evidence or source records, not in narrative prose.

- `natural` uses unredacted natural FPF result language and may use FPF terms. In this mode only, `fpf_terms_explained = "full"` explains each FPF term on first use in at most three short lines; `short` uses one brief clause or sentence (about half to one line); and `off` adds no explanation.
- `general` uses no FPF terms in the narrative. Use ordinary-language synonyms instead. The explanation setting is ignored.
- `ste` uses no FPF terms in the narrative. Use simplified synonyms and an ASD-STE100 Issue 9-inspired overlay: short clear sentences, one topic per sentence, active voice where practical, and vertical lists for complex text. This is guidance only and makes no formal-conformance claim. The explanation setting is ignored.
{END}
'''


def replace_block(text: str, block: str, path: Path) -> str:
    pattern = re.compile(rf"{re.escape(START)}(?:\n.*)?\n{re.escape(END)}\n?", re.DOTALL)
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise ValueError(f"{path} must contain exactly one generated output settings block")
    return text[: matches[0].start()] + block + text[matches[0].end() :]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="check synchronization without writing (default)")
    mode.add_argument("--apply", action="store_true", help="write generated blocks into every FPF skill")
    args = parser.parse_args()

    try:
        settings = read_settings(SETTINGS_PATH)
        paths = sorted((ROOT / "skills").glob(SKILL_GLOB))
        if len(paths) != 8:
            raise ValueError(f"expected exactly 8 FPF skills, found {len(paths)}")
        block = render_block(settings)
        stale: list[Path] = []
        for path in paths:
            original = path.read_text(encoding="utf-8")
            updated = replace_block(original, block, path)
            if original != updated:
                stale.append(path)
                if args.apply:
                    path.write_text(updated, encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if stale and not args.apply:
        for path in stale:
            print(f"OUT OF SYNC: {path.relative_to(ROOT)}", file=sys.stderr)
        return 1
    print(f"FPF skill settings {'applied' if args.apply else 'checked'} for {len(paths)} packages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
