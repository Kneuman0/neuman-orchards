from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from garden_helper.memory import GardenMemoryStore
from garden_helper.schema import GardenSnapshot
from garden_helper.sync import GardenTwinService

EXAMPLE_SNAPSHOT = ROOT / "examples" / "example_garden_snapshot.json"


class GardenTwinSyncTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "garden-memory.db"
        self.service = GardenTwinService(db_path=self.db_path)

    def tearDown(self) -> None:
        self.service.close()
        self.temp_dir.cleanup()

    def load_example(self) -> dict:
        return json.loads(EXAMPLE_SNAPSHOT.read_text(encoding="utf-8"))

    def test_import_creates_locations_and_plantings(self) -> None:
        report = self.service.import_snapshot(EXAMPLE_SNAPSHOT, source_path=str(EXAMPLE_SNAPSHOT))
        self.assertEqual(report["stats"]["beds_upserted"], 2)
        self.assertEqual(report["stats"]["obstacles_upserted"], 1)
        self.assertEqual(report["stats"]["plants_upserted"], 2)
        self.assertEqual(report["stats"]["plantings_upserted"], 2)

        context = self.service.export_memory_context()["memory_context"]
        self.assertEqual(len(context["beds"]), 2)
        self.assertEqual(len(context["obstacles"]), 1)
        self.assertEqual(len(context["plantings"]), 2)
        self.assertEqual(context["garden"]["width"], 20)
        self.assertEqual(context["garden"]["height"], 18)
        self.assertEqual(context["beds"][0]["bed_id"], "bed-raised-1")

    def test_reimport_rename_preserves_same_location_geometry_binding(self) -> None:
        original = self.load_example()
        self.service.import_snapshot(original)

        renamed = self.load_example()
        renamed["beds"][0]["name"] = "Main Tomato Bed"
        self.service.import_snapshot(renamed)

        store = GardenMemoryStore(self.db_path)
        row = store.connection.execute(
            """
            SELECT l.id, l.name
            FROM locations l
            JOIN location_geometry g ON g.location_id = l.id
            WHERE g.external_bed_id = ?
            """,
            ("bed-raised-1",),
        ).fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row["name"], "Main Tomato Bed")
        store.close()

    def test_move_planting_between_beds_keeps_same_planting_record(self) -> None:
        original = self.load_example()
        self.service.import_snapshot(original)

        moved = self.load_example()
        moved["plantings"][0]["bed_id"] = "bed-raised-2"
        moved["plantings"][0]["grid_cells"] = [
            {"row": 2, "col": 1},
            {"row": 2, "col": 2},
            {"row": 3, "col": 1},
            {"row": 3, "col": 2}
        ]
        self.service.import_snapshot(moved)

        store = GardenMemoryStore(self.db_path)
        row = store.connection.execute(
            """
            SELECT pg.external_planting_id, pg.external_bed_id, pt.location_id
            FROM planting_geometry pg
            JOIN plantings pt ON pt.id = pg.planting_id
            WHERE pg.external_planting_id = ?
            """,
            ("planting-bed1-tomato-1",),
        ).fetchone()
        self.assertEqual(row["external_bed_id"], "bed-raised-2")
        store.close()

    def test_bad_plant_name_produces_warning_and_skips_plantings(self) -> None:
        bad = self.load_example()
        bad["plant_catalog"][0]["display_name"] = "???"
        report = self.service.import_snapshot(bad)
        self.assertTrue(report["warnings"])
        self.assertEqual(report["stats"]["plantings_skipped"], 1)

    def test_export_round_trip_is_valid_snapshot_shape(self) -> None:
        self.service.import_snapshot(EXAMPLE_SNAPSHOT)
        exported = self.service.export_memory_context()["snapshot"]
        snapshot = GardenSnapshot.from_dict(exported)
        self.assertEqual(snapshot.garden.width, 20)
        self.assertEqual(len(snapshot.obstacles), 1)
        self.assertEqual(snapshot.beds[0].bed_id, "bed-raised-1")

    def test_import_farmbot_bundle_round_trip(self) -> None:
        self.service.import_snapshot(EXAMPLE_SNAPSHOT)
        bundle = self.service.export_farmbot_bundle()

        second_db = Path(self.temp_dir.name) / "garden-memory-second.db"
        second_service = GardenTwinService(db_path=second_db)
        try:
            report = second_service.import_farmbot_bundle(bundle)
            self.assertEqual(report["stats"]["beds_upserted"], 2)
            self.assertEqual(report["stats"]["obstacles_upserted"], 1)
            context = second_service.export_memory_context()["memory_context"]
            self.assertEqual(context["garden"]["width"], 20)
            self.assertEqual(context["obstacles"][0]["obstacle_id"], "obstacle-compost")
        finally:
            second_service.close()


if __name__ == "__main__":
    unittest.main()
