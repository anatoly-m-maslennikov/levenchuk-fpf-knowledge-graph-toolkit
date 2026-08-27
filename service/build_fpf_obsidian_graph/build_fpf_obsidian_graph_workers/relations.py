from __future__ import annotations

from collections import defaultdict

from .models import FPF_PROFILE, GraphProfile, Page
from .patterns import BACKTICK_ID_RE, BOLD_REL_LABEL_RE, BULLET_RE, FRONTMATTER_NORM_RE, FRONTMATTER_STATUS_RE, HEADING_RE, ID_RE, QUALIFIED_RELATION_ID_RE, RANGE_RELATION_ID_RE, REL_LABEL_RE, U_TERM_RE


def extract_relations(
    body: list[str],
    profile: GraphProfile = FPF_PROFILE,
) -> dict[str, list[str]]:
    rels: dict[str, set[str]] = defaultdict(set)
    in_rel = False
    current = "related"
    for line in body:
        hm = HEADING_RE.match(line)
        if hm:
            ht = hm.group(2).lower()
            in_rel = "relations" in ht or "see also" in ht
            current = "related"
            continue
        bold = BOLD_REL_LABEL_RE.match(line)
        if bold:
            current = normalize_relation(bold.group(1))
            for ref in extract_ids(bold.group(2), profile):
                rels[current].add(ref)
            continue
        if not in_rel:
            continue
        bm = BULLET_RE.match(line)
        if not bm:
            continue
        item = bm.group(1)
        label = REL_LABEL_RE.match(item)
        if label:
            current = normalize_relation(label.group(1))
            item = label.group(2)
        for ref in extract_ids(item, profile):
            rels[current].add(ref)
    return {k: sorted(v) for k, v in rels.items() if v}


def normalize_relation(label: str) -> str:
    return label.lower().replace(" ", "_").replace("-", "_")


def extract_ids(text: str, profile: GraphProfile = FPF_PROFILE) -> list[str]:
    refs = set(BACKTICK_ID_RE.findall(text)) | set(ID_RE.findall(text))
    if not profile.multi_root_relations:
        refs = {ref for ref in refs if len(ref.split(".", 1)[0]) == 1}
    return sorted(r for r in refs if "." in r and not r.startswith("U."))


def normalize_relation_targets(pages: list[Page]) -> None:
    """Resolve qualified references and compact numeric ranges to real FPF IDs."""
    known_ids = {page.framework_id for page in pages if page.framework_id}
    for page in pages:
        normalized_relations: dict[str, list[str]] = {}
        for relation, targets in page.relations.items():
            normalized: set[str] = set()
            for target in targets:
                if target in known_ids:
                    normalized.add(target)
                    continue
                qualified = QUALIFIED_RELATION_ID_RE.fullmatch(target)
                if qualified and qualified.group(1) in known_ids:
                    normalized.add(qualified.group(1))
                    continue
                compact_range = RANGE_RELATION_ID_RE.fullmatch(target)
                if compact_range:
                    start_parts = compact_range.group("start").split(".")
                    end_parts = compact_range.group("end").split(".")
                    if (
                        start_parts[:-1] == end_parts[:-1]
                        and start_parts[-1].isdigit()
                        and end_parts[-1].isdigit()
                    ):
                        first, last = int(start_parts[-1]), int(end_parts[-1])
                        prefix = ".".join(start_parts[:-1])
                        expanded = {f"{prefix}.{number}" for number in range(first, last + 1)}
                        if first <= last and last - first <= 50 and expanded <= known_ids:
                            normalized.update(expanded)
                            continue
                normalized.add(target)
            if normalized:
                normalized_relations[relation] = sorted(normalized)
        page.relations = normalized_relations


def enrich(page: Page, profile: GraphProfile = FPF_PROFILE) -> None:
    first = "\n".join(page.body[:100])
    m = FRONTMATTER_STATUS_RE.search(first)
    if m:
        page.status = m.group(1).strip()
    m = FRONTMATTER_NORM_RE.search(first)
    if m:
        page.normativity = m.group(1).strip()
    text = "\n".join(page.body)
    page.terms = sorted(set(U_TERM_RE.findall(text)))[:120]
    page.relations = extract_relations(page.body, profile)
