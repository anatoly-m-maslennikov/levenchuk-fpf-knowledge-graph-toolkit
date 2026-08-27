from __future__ import annotations

import hashlib
import json
from pathlib import Path

from service.filesystem_policy import remove_directory
from .assign_names import assign_names
from .models import FPF_PROFILE, GraphProfile, Page
from .patterns import INDEX_DIR, LINK_RE
from .relations import normalize_relation_targets
from .render import render_hub, render_master_index, render_page, render_relation_index, render_term_index
from .source_parser import build_pages, parse_headings


def remove_os_metadata(root: Path) -> None:
    """Keep platform-created metadata outside the deterministic generated tree."""
    for path in root.rglob(".DS_Store"):
        path.unlink()


def validate(
    out_dir: Path,
    hubs: list[Page],
    pages: list[Page],
    id_to_page: dict[str, str],
    profile: GraphProfile = FPF_PROFILE,
) -> dict:
    page_names = {f"{INDEX_DIR}/{name}" for name in profile.index_files} | {
        h.page_name for h in hubs
    } | {p.page_name for p in pages}
    broken = []
    for path in out_dir.rglob("*.md"):
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in LINK_RE.finditer(text):
            target = match.group(1)
            if target not in page_names:
                broken.append({"file": path.name, "target": target})
    unresolved = []
    for p in pages:
        for rel, refs in p.relations.items():
            for ref in refs:
                if ref not in id_to_page:
                    unresolved.append({"source": p.page_name, "relation": rel, "target": ref})
    return {
        "hubs": len(hubs),
        "pages": len(pages),
        "ids": len(id_to_page),
        "markdown_files": len(list(out_dir.rglob("*.md"))),
        "broken_links_count": len(broken),
        "broken_links_sample": broken[:50],
        "unresolved_relations_count": len(unresolved),
        "unresolved_relations_sample": unresolved[:50],
    }


def build_graph(
    source: Path,
    out_dir: Path,
    clean: bool,
    source_revision: str,
    generated_on: str,
    profile: GraphProfile = FPF_PROFILE,
) -> dict:
    source_sha256 = hashlib.sha256(source.read_bytes()).hexdigest()
    lines, headings = parse_headings(source)
    hubs, pages = build_pages(lines, headings, profile)
    normalize_relation_targets(pages)
    hub_by_title, id_to_page = assign_names(hubs, pages, profile)
    if clean and out_dir.exists():
        remove_directory(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for page in pages:
        path = out_dir / f"{page.page_name}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_page(page, source.name, source_revision, source_sha256, generated_on, hub_by_title, id_to_page, profile), encoding="utf-8")
    for hub in hubs:
        path = out_dir / f"{hub.page_name}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_hub(hub, pages, source.name, source_revision, source_sha256, generated_on, profile), encoding="utf-8")
    index_dir = out_dir / INDEX_DIR
    index_dir.mkdir(parents=True, exist_ok=True)
    master_name, relation_name, term_name = profile.index_files
    (index_dir / f"{master_name}.md").write_text(render_master_index(hubs, pages, source.name, source_revision, source_sha256, generated_on, profile), encoding="utf-8")
    (index_dir / f"{relation_name}.md").write_text(render_relation_index(pages, id_to_page, source.name, source_revision, source_sha256, generated_on, profile), encoding="utf-8")
    (index_dir / f"{term_name}.md").write_text(render_term_index(pages, source.name, source_revision, source_sha256, generated_on, profile), encoding="utf-8")
    remove_os_metadata(out_dir)
    report = validate(out_dir, hubs, pages, id_to_page, profile)
    report_metadata = {"source": source.name, "out_dir": out_dir.name, "source_revision": source_revision, "source_sha256": source_sha256, "generated_on": generated_on}
    if profile != FPF_PROFILE:
        report_metadata["framework"] = profile.label
    report.update(report_metadata)
    (index_dir / f"{profile.label} - Validation Report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report
