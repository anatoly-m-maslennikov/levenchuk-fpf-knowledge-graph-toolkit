"""Relation IDs are complete references, including slash-separated chains."""

import unittest

from service.scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.models import CAD_PROFILE, Heading, Page
from service.scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.relations import extract_ids, extract_relations, normalize_relation_targets


class RelationChainTests(unittest.TestCase):
    def test_source_chains_preserve_every_id_without_phantom_prefixes(self) -> None:
        expected = ["A.3.1.QM", "B.1.5.CM", "F.0.1", "F.0.2", "F.1"]
        for text in (
            "F.0.1/F.1/F.0.2 and A.3.1.QM/B.1.5.CM",
            "`F.0.1/F.1/F.0.2`, `A.3.1.QM/B.1.5.CM`",
            "`F.0.1`/`F.1`/`F.0.2`, `A.3.1.QM`/`B.1.5.CM`",
            "F.0.1 / F.1 / F.0.2, A.3.1.QM / B.1.5.CM.",
            "F.0.1/ F.1 /F.0.2, A.3.1.QM/ B.1.5.CM.",
        ):
            with self.subTest(text=text):
                self.assertEqual(extract_ids(text), expected)

    def test_relations_section_receives_complete_chain(self) -> None:
        result = extract_relations([
            "### F.0.2.MA:12 - Relations",
            "- F.0.1/F.1/F.0.2 govern source meaning.",
            "- A.3.1.QM/B.1.5.CM qualify the Method claims.",
        ])
        self.assertEqual(result["related"], ["A.3.1.QM", "B.1.5.CM", "F.0.1", "F.0.2", "F.1"])


class RelationBoundaryTests(unittest.TestCase):
    def test_urls_paths_and_filenames_are_not_reference_chains(self) -> None:
        for text in (
            "https://example.test/F.0.1/F.1/F.0.2",
            "https://F.0.1/F.1/F.0.2",
            "/F.0.1/F.1/F.0.2", "docs/F.0.1/F.1", "F.0.1/file.md",
            r"C:\docs\F.0.1\F.1", "F.0.1.md", "`F.0.1/F.1.json`",
            "prefix-F.0.1/F.1", "F.0.1/F.1/unsupported",
        ):
            with self.subTest(text=text):
                self.assertEqual(extract_ids(text), [])

    def test_colon_reference_addresses_and_pattern_sections_survive(self) -> None:
        self.assertEqual(extract_ids("FPF.Reference:16/CAD.Reference:3.2"), ["CAD.Reference:3.2", "FPF.Reference:16"])
        self.assertEqual(extract_ids("CAD.5:4.7/CAD.2:4.1", CAD_PROFILE), ["CAD.2", "CAD.5"])
        self.assertEqual(extract_ids("A.1, B.2; C.3."), ["A.1", "B.2", "C.3"])


def _page(identifier: str) -> Page:
    return Page("page", Heading(2, identifier, 1), 1, 1, [], framework_id=identifier)


class QualifiedRelationTests(unittest.TestCase):
    def test_source_qualifiers_normalize_only_to_known_base_ids(self) -> None:
        pages = [_page("A.13"), _page("A.3.2"), _page("A.1-qualified")]
        pages[0].relations = {"related": ["A.13-qualified", "A.3.2-admitted", "A.1-qualified", "B.1-qualified"]}
        normalize_relation_targets(pages)
        self.assertEqual(pages[0].relations["related"], ["A.1-qualified", "A.13", "A.3.2", "B.1-qualified"])


class RelationLabelTests(unittest.TestCase):
    def test_plain_label_without_colon_sets_continuation_category(self) -> None:
        result = extract_relations([
            "### F.18:11 - Relations",
            "Builds on `F.0.1`, `F.1`, `F.2`, `F.3`, `F.5`, `F.8`, `F.9`, `F.13`, `F.14`, `F.15`, `C.2.1`, and `E.24.PUB`.",
            "Coordinates with:", "", "- `A.2`, `A.2.1`;", "- `A.3.1`.",
        ])
        self.assertEqual(len(result["builds_on"]), 12)
        self.assertEqual(result["coordinates_with"], ["A.2", "A.2.1", "A.3.1"])
        self.assertNotIn("related", result)

    def test_unbulleted_bold_labels_keep_their_source_categories(self) -> None:
        result = extract_relations([
            "### G.3:12 - Relations", "**Builds on:** `G.Core`, `G.1`.",
            "**Uses (via Extensions):** `G.0`, optional `C.18 and C.19`.",
            "- `C.20` is also consumed.", "**Publishes to:** `G.4`, `G.5`.",
            "**Constrains:** `A.1`.",
        ])
        self.assertEqual(result["builds_on"], ["G.1", "G.Core"])
        self.assertEqual(result["uses_via_extensions"], ["C.18", "C.19", "C.20", "G.0"])
        self.assertEqual(result["publishes_to"], ["G.4", "G.5"])
        self.assertEqual(result["constrains"], ["A.1"])


class RelationScopeTests(unittest.TestCase):
    def test_unbulleted_labels_outside_relations_are_not_extracted(self) -> None:
        self.assertEqual(extract_relations([
            "### Solution", "Builds on A.1", "**Builds on:** A.2",
            "### Relations", "- **Builds on:** A.3", "### Other", "**Used by:** A.4",
        ]), {"builds_on": ["A.3"]})

    def test_unknown_colon_label_suspends_continuation_until_known_label(self) -> None:
        for label in ("Constrained non-use:", "**Constrained non-use:**"):
            with self.subTest(label=label):
                result = extract_relations([
                    "### F.18:11 - Relations", "Coordinates with:", "- `A.2`.",
                    label, "", "- `F.18` creates no new kind under C.2.1.",
                    "- F.9 separately governs the Bridge.",
                    "Used by:", "- `A.10`.",
                ])
                self.assertEqual(result, {"coordinates_with": ["A.2"], "used_by": ["A.10"]})


if __name__ == "__main__":
    unittest.main()
