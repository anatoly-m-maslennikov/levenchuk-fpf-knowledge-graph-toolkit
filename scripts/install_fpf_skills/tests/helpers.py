from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from scripts.install_fpf_skills.install_fpf_skills import Harness, run
from scripts.install_fpf_skills.install_fpf_skills_workers import cli
from scripts.install_fpf_skills.install_fpf_skills_workers.catalog import load_catalog


CATALOG = load_catalog(cli.CATALOG_PATH)
END_USER_SKILLS = list(CATALOG["end_user_skills"])
SERVICE_SKILLS = list(CATALOG["project_service_skills"])


def make_source(root: Path) -> Path:
    skills = root / "skills"
    for name in END_USER_SKILLS + SERVICE_SKILLS:
        package = skills / f"{name}.skill"
        package.mkdir(parents=True)
        (package / "SKILL.md").write_text(f"---\nname: {name}\n---\n", encoding="utf-8")
    references = skills / "fpf.skill" / "references"
    references.mkdir()
    (references / "routing.md").write_text("route references\n", encoding="utf-8")
    return skills


def write_settings(root: Path, method: str) -> tuple[Path, Path]:
    control = root / ".caprmedio"
    control.mkdir(parents=True, exist_ok=True)
    text = (
        '[paths]\nfpf_original_repo = "../../FPF"\n\n[skills]\n'
        'output_style = "general"\nfpf_terms_explained = "off"\n'
        'save_report = "on"\nreport_style = "plain"\n'
        f'install_method = "{method}"\n'
    )
    settings = control / "settings.toml"
    example = control / "settings.toml.example"
    settings.write_text(text, encoding="utf-8")
    example.write_text(text, encoding="utf-8")
    return settings, example


def run_installer(
    source: Path, settings_root: Path, destination: Path,
    arguments: list[str] | None = None,
) -> int:
    settings, example = write_settings(settings_root, "symlink")
    harness = Harness("test", "TEST_FPF_HOME", ".test-fpf")
    arguments = arguments or ["--apply", "--destination", str(destination)]
    with (
        patch.object(cli, "SOURCE_SKILLS", source),
        patch.object(cli, "SETTINGS_PATH", settings),
        patch.object(cli, "EXAMPLE_PATH", example),
    ):
        return run(harness, arguments)


def run_with_method(
    source: Path, settings_root: Path, destination: Path,
    method: str, arguments: list[str],
) -> int:
    settings, example = write_settings(settings_root, method)
    harness = Harness("test", "TEST_FPF_HOME", ".test-fpf")
    with (
        patch.object(cli, "SOURCE_SKILLS", source),
        patch.object(cli, "SETTINGS_PATH", settings),
        patch.object(cli, "EXAMPLE_PATH", example),
    ):
        return run(harness, arguments)
