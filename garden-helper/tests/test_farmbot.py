from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from garden_helper.farmbot import farmbot_bundle_to_snapshot, snapshot_to_farmbot_bundle
from garden_helper.schema import load_snapshot
from garden_helper.stack import prepare_farmbot_stack

EXAMPLE_SNAPSHOT = ROOT / "examples" / "example_garden_snapshot.json"


class FarmBotAdapterTests(unittest.TestCase):
    def test_snapshot_export_creates_farmbot_bundle(self) -> None:
        snapshot = load_snapshot(EXAMPLE_SNAPSHOT)
        bundle = snapshot_to_farmbot_bundle(snapshot)
        self.assertEqual(bundle["format"], "garden-helper-farmbot-bundle/v1")
        self.assertEqual(bundle["farmbot"]["web_app_config"]["map_size_x"], 6096)
        self.assertEqual(bundle["farmbot"]["web_app_config"]["map_size_y"], 5486)
        self.assertEqual(len(bundle["farmbot"]["point_groups"]), 3)
        self.assertEqual(len(bundle["farmbot"]["points"]), 5)

    def test_bundle_round_trip_preserves_ids(self) -> None:
        bundle = snapshot_to_farmbot_bundle(EXAMPLE_SNAPSHOT)
        snapshot = farmbot_bundle_to_snapshot(bundle)
        self.assertEqual(snapshot.garden.width, 20)
        self.assertEqual(snapshot.garden.height, 18.0)
        self.assertEqual(snapshot.beds[0].bed_id, "bed-raised-1")
        self.assertEqual(snapshot.obstacles[0].obstacle_id, "obstacle-compost")
        self.assertEqual(snapshot.plantings[0].planting_id, "planting-bed1-basil-1")
        self.assertEqual(snapshot.plantings[0].quantity, 4)
        self.assertEqual(snapshot.observations[0].observation_id, "obs-bed1-tomato-vigor")


class FarmBotStackPrepTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _run(self, command: list[str], cwd: Path) -> str:
        completed = subprocess.run(command, cwd=cwd, check=True, capture_output=True, text=True)
        return completed.stdout.strip()

    def _create_source_repo(self) -> Path:
        source = self.root / "source-repo"
        source.mkdir()
        (source / "docker-compose.yml").write_text("services:\n  web:\n    image: farmbot_web\n", encoding="utf-8")
        (source / "example.env").write_text("API_HOST=\nAPI_PORT=3000\n", encoding="utf-8")
        self._run(["git", "init", "--initial-branch=main"], cwd=source)
        self._run(["git", "config", "user.email", "test@example.com"], cwd=source)
        self._run(["git", "config", "user.name", "Garden Helper Tests"], cwd=source)
        self._run(["git", "add", "."], cwd=source)
        self._run(["git", "commit", "-m", "init"], cwd=source)
        return source

    def test_prepare_farmbot_stack_clones_repo_and_writes_env(self) -> None:
        source_repo = self._create_source_repo()
        runtime_dir = self.root / "runtime" / "farmbot-web-app"

        report = prepare_farmbot_stack(
            runtime_dir=runtime_dir,
            host="192.168.1.50",
            port=3200,
            repo_url=str(source_repo),
        )

        env_text = (runtime_dir / ".env").read_text(encoding="utf-8")
        self.assertIn("API_HOST=192.168.1.50", env_text)
        self.assertIn("API_PORT=3200", env_text)
        self.assertIn("MQTT_HOST=192.168.1.50", env_text)
        self.assertEqual(report["api_port"], 3200)
        self.assertIn("cloned_repo", report["actions"])


if __name__ == "__main__":
    unittest.main()
