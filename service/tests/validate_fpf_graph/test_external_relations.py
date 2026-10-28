"""Every cross-framework dependency remains visible in a split projection."""

import unittest
from pathlib import Path

from service.scripts.filesystem_policy import temporary_workspace
from service.scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.graph_io import validate
from service.scripts.build_fpf_obsidian_graph.build_fpf_obsidian_graph_workers.models import Heading, NPF_PROFILE, Page
from service.scripts.validate_fpf_graph.validate_fpf_graph_workers.report_checks import classify_unresolved


class ExternalRelationTests(unittest.TestCase):
    def test_all_dependencies_are_reported_and_classified(self) -> None:
        with temporary_workspace() as name:
            root = Path(name)
            page = Page("page", Heading(2, "NSTD.1", 1), 1, 1, [])
            page.relations = {"uses": [f"A.{index}" for index in range(75)]}
            report = validate(root, [], [page], {}, NPF_PROFILE)
            self.assertEqual(75, report["unresolved_relations_count"])
            self.assertEqual(75, len(report["unresolved_relations_sample"]))
            source = root / "source.md"
            source.write_text("# NPF\n", encoding="utf-8")
            errors, warnings = [], []
            classified = classify_unresolved(report, source, errors, warnings, NPF_PROFILE)
            self.assertEqual([], errors)
            self.assertEqual(75, len(classified))
            self.assertTrue(all(item["classification"] == "external framework target outside this projection" for item in classified))
