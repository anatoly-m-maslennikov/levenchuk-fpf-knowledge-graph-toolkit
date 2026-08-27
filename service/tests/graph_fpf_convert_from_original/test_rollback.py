import unittest
from pathlib import Path

from service.filesystem_policy import temporary_workspace
from service.graph_fpf_convert_from_original.graph_fpf_convert_from_original import convert_graph
from service.tests.graph_fpf_convert_from_original.helpers import initialize_graphs, make_builder, make_source


class FailedConversionTests(unittest.TestCase):
    def test_restores_graph_and_previous_backup(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary) / "toolkit"
            root.mkdir()
            source = make_source(Path(temporary) / "FPF")
            graph, backup = initialize_graphs(root)
            builder = root / "builder.py"
            make_builder(builder, fail=True)

            with self.assertRaisesRegex(ValueError, "graph builder failed"):
                convert_graph(
                    root=root, builder=builder,
                    source=source, generated_on="2026-08-22",
                )

            self.assertTrue((graph / "current.txt").is_file())
            self.assertTrue((backup / "older.txt").is_file())
