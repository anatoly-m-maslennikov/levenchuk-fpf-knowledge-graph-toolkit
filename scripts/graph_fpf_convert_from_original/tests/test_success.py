import unittest
from pathlib import Path

from scripts.filesystem_policy import temporary_workspace
from scripts.graph_fpf_convert_from_original.graph_fpf_convert_from_original import convert_graph
from scripts.graph_fpf_convert_from_original.tests.helpers import initialize_graphs, make_builder, make_source


class SuccessfulConversionTests(unittest.TestCase):
    def test_rotates_current_graph_and_replaces_old_backup(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary) / "toolkit"
            root.mkdir()
            source = make_source(Path(temporary) / "FPF")
            graph, backup = initialize_graphs(root)
            builder = root / "builder.py"
            make_builder(builder)

            result = convert_graph(
                root=root, builder=builder, source=source, generated_on="2026-08-22"
            )

            self.assertTrue((graph / "new.txt").is_file())
            self.assertTrue((backup / "current.txt").is_file())
            self.assertFalse((backup / "older.txt").exists())
            self.assertTrue(result["replaced_previous_backup"])

    def test_identical_rerun_preserves_meaningful_predecessor(self) -> None:
        with temporary_workspace() as temporary:
            root = Path(temporary) / "toolkit"
            root.mkdir()
            source = make_source(Path(temporary) / "FPF")
            graph, backup = initialize_graphs(root)
            builder = root / "builder.py"
            make_builder(builder)

            convert_graph(root=root, builder=builder, source=source, generated_on="2026-08-22")
            before = (backup / "current.txt").read_bytes()
            result = convert_graph(
                root=root, builder=builder, source=source, generated_on="2026-08-22"
            )

            self.assertEqual(before, (backup / "current.txt").read_bytes())
            self.assertFalse(result["replaced_previous_backup"])
