from __future__ import annotations

from collections import defaultdict

from .frontmatter import frontmatter, provenance_lines, wiki
from .markdown import linkify_line, remove_empty_table_columns, demote_headings
from .models import FPF_PROFILE, GraphProfile, Page


def render_page(
    page: Page,
    source_name: str,
    source_revision: str,
    source_sha256: str,
    generated_on: str,
    hub_by_title: dict[str, str],
    id_to_page: dict[str, str],
    profile: GraphProfile = FPF_PROFILE,
) -> str:
    body_lines = remove_empty_table_columns(demote_headings(page.body))
    body = [linkify_line(x, id_to_page, profile) for x in body_lines]
    return frontmatter(
        page,
        source_name,
        source_revision,
        source_sha256,
        generated_on,
        hub_by_title,
        id_to_page,
        profile,
    ) + "\n".join(body).rstrip() + "\n"


def render_hub(
    hub: Page,
    pages: list[Page],
    source_name: str,
    source_revision: str,
    source_sha256: str,
    generated_on: str,
    profile: GraphProfile = FPF_PROFILE,
) -> str:
    children = [p for p in pages if p.parent_hub == hub.title]
    out = [frontmatter(hub, source_name, source_revision, source_sha256, generated_on, {}, {}, profile)]
    out.append(f"# {hub.title}\n")
    out.append(f"Source lines: `{hub.start}-{hub.end}` in `{source_name}`.\n")
    out.append("## Pages\n")
    for p in children:
        label = p.framework_id or p.title
        out.append(f"- {wiki(p.page_name, label)} — {p.title}")
    out.append("\n## Table\n")
    out.append("| ID | Page | Type | Lines |")
    out.append("|---|---|---|---|")
    for p in children:
        out.append(f"| {p.framework_id} | {wiki(p.page_name)} | {p.page_type} | {p.start}-{p.end} |")
    return "\n".join(out).rstrip() + "\n"


def render_master_index(
    hubs: list[Page],
    pages: list[Page],
    source_name: str,
    source_revision: str,
    source_sha256: str,
    generated_on: str,
    profile: GraphProfile = FPF_PROFILE,
) -> str:
    index_name = profile.index_files[0]
    out = ["---", f'type: "{profile.key}-index"', "context:", f'  - "{profile.label}"', 'page_type: "master-index"', 'mode: "index-generated"', f'title: "{index_name}"', *provenance_lines(source_name, source_revision, source_sha256, generated_on), "generated: true", "---", "", f"# {index_name}", "", "## Hubs", ""]
    for hub in hubs:
        count = sum(1 for p in pages if p.parent_hub == hub.title)
        out.append(f"- {wiki(hub.page_name)} — {count} pages")
    out += ["", "## Pages", "", "| ID | Page | Parent | Lines |", "|---|---|---|---|"]
    hub_name = {h.title: h.page_name for h in hubs}
    for p in pages:
        parent = wiki(hub_name[p.parent_hub]) if p.parent_hub in hub_name else ""
        out.append(f"| {p.framework_id} | {wiki(p.page_name)} | {parent} | {p.start}-{p.end} |")
    return "\n".join(out) + "\n"


def render_relation_index(
    pages: list[Page],
    id_to_page: dict[str, str],
    source_name: str,
    source_revision: str,
    source_sha256: str,
    generated_on: str,
    profile: GraphProfile = FPF_PROFILE,
) -> str:
    index_name = profile.index_files[1]
    out = ["---", f'type: "{profile.key}-index"', "context:", f'  - "{profile.label}"', 'page_type: "relation-index"', 'mode: "index-generated"', f'title: "{index_name}"', *provenance_lines(source_name, source_revision, source_sha256, generated_on), "generated: true", "---", "", f"# {index_name}", "", "| Relation | Source | Target | Resolved |", "|---|---|---|---|"]
    for p in pages:
        for rel, refs in sorted(p.relations.items()):
            for ref in refs:
                target = wiki(id_to_page[ref]) if ref in id_to_page else ref
                out.append(f"| {rel} | {wiki(p.page_name)} | {target} | {'yes' if ref in id_to_page else 'no'} |")
    return "\n".join(out) + "\n"


def render_term_index(
    pages: list[Page],
    source_name: str,
    source_revision: str,
    source_sha256: str,
    generated_on: str,
    profile: GraphProfile = FPF_PROFILE,
) -> str:
    term_pages: dict[str, list[Page]] = defaultdict(list)
    for p in pages:
        for term in p.terms:
            term_pages[term].append(p)
    index_name = profile.index_files[2]
    out = ["---", f'type: "{profile.key}-index"', "context:", f'  - "{profile.label}"', 'page_type: "term-index"', 'mode: "index-generated"', f'title: "{index_name}"', *provenance_lines(source_name, source_revision, source_sha256, generated_on), "generated: true", "---", "", f"# {index_name}", ""]
    for term in sorted(term_pages):
        links = ", ".join(wiki(p.page_name, p.framework_id or p.title) for p in term_pages[term][:25])
        more = f" (+{len(term_pages[term]) - 25} more)" if len(term_pages[term]) > 25 else ""
        out.append(f"- `{term}` — {links}{more}")
    return "\n".join(out).rstrip() + "\n"
