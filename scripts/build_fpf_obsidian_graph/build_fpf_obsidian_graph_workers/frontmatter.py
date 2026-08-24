from __future__ import annotations

from .models import FPF_PROFILE, GraphProfile, Page


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def yaml_list(values: list[str], indent: int = 2) -> list[str]:
    if not values:
        return [" " * indent + "[]"]
    return [" " * indent + "- " + yaml_quote(v) for v in values]


def wiki(page: str, alias: str = "") -> str:
    return f"[[{page}|{alias}]]" if alias and alias != page else f"[[{page}]]"


def provenance_lines(source_name: str, source_revision: str, source_sha256: str, generated_on: str) -> list[str]:
    return [
        f"source_file: {yaml_quote(source_name)}",
        f"source_revision: {yaml_quote(source_revision)}",
        f"source_sha256: {yaml_quote(source_sha256)}",
        f"generated_on: {yaml_quote(generated_on)}",
    ]


def frontmatter(
    page: Page,
    source_name: str,
    source_revision: str,
    source_sha256: str,
    generated_on: str,
    hub_by_title: dict[str, str],
    id_to_page: dict[str, str],
    profile: GraphProfile = FPF_PROFILE,
) -> str:
    mode = "canonical-generated" if page.kind == "page" else "index-generated"
    out = ["---", f"type: {yaml_quote(page.page_type)}", "context:", *yaml_list([profile.label])]
    out += [f"page_type: {yaml_quote(page.page_type)}", f"mode: {yaml_quote(mode)}"]
    if page.framework_id:
        out.append(f"{profile.id_field}: {yaml_quote(page.framework_id)}")
    out.append(f"title: {yaml_quote(page.title)}")
    out += _parent_lines(page, hub_by_title)
    out += provenance_lines(source_name, source_revision, source_sha256, generated_on)
    out += ["source_lines:", f"  - {page.start}", f"  - {page.end}", f"status: {yaml_quote(page.status)}"]
    if page.normativity:
        out.append(f"normativity: {yaml_quote(page.normativity)}")
    if page.terms:
        out += ["terms:", *yaml_list(page.terms)]
    out += _relation_lines(page, id_to_page)
    out += ["generated: true", "---"]
    return "\n".join(out) + "\n\n"


def _parent_lines(page: Page, hub_by_title: dict[str, str]) -> list[str]:
    if not page.parent_hub:
        return []
    parent = wiki(hub_by_title.get(page.parent_hub, page.parent_hub))
    return [f"part: {yaml_quote(parent)}", "parents:", *yaml_list([parent])]


def _relation_lines(page: Page, id_to_page: dict[str, str]) -> list[str]:
    result: list[str] = []
    for relation, references in sorted(page.relations.items()):
        values = [wiki(id_to_page[ref], ref) if ref in id_to_page else ref for ref in references]
        result += [f"{relation}:", *yaml_list(values)]
    return result
