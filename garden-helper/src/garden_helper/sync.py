from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .farmbot import farmbot_bundle_to_snapshot, snapshot_to_farmbot_bundle
from .ids import strip_display_label
from .memory import DEFAULT_DB_PATH, GardenMemoryStore
from .schema import GardenSnapshot, load_snapshot
from .stack import DEFAULT_RUNTIME_DIR, prepare_farmbot_stack


class GardenTwinService:
    def __init__(
        self,
        db_path: str | Path = DEFAULT_DB_PATH,
        *,
        memory_store: GardenMemoryStore | None = None,
    ):
        self.memory_store = memory_store or GardenMemoryStore(db_path)

    def close(self) -> None:
        self.memory_store.close()

    def load_snapshot(self, payload: str | Path | dict[str, Any] | GardenSnapshot) -> GardenSnapshot:
        if isinstance(payload, GardenSnapshot):
            return payload
        if isinstance(payload, (str, Path)):
            return load_snapshot(payload)
        return GardenSnapshot.from_dict(payload)

    def normalize_plant_catalog(self, snapshot: GardenSnapshot) -> tuple[list[str], set[str]]:
        warnings: list[str] = []
        skipped: set[str] = set()
        seen_display_names: dict[str, str] = {}

        for plant in snapshot.plant_catalog:
            normalized = strip_display_label(plant.display_name)
            if not any(ch.isalpha() for ch in normalized):
                warnings.append(
                    f"plant_catalog entry {plant.plant_id} has no usable plant name; skipping it and dependent plantings"
                )
                skipped.add(plant.plant_id)
                continue
            key = normalized.casefold()
            if key in seen_display_names and seen_display_names[key] != plant.plant_id:
                warnings.append(
                    f"plant_catalog display name '{normalized}' appears more than once; using stable plant_id values to avoid silent merge"
                )
            else:
                seen_display_names[key] = plant.plant_id
        return warnings, skipped

    def import_snapshot(
        self,
        payload: str | Path | dict[str, Any] | GardenSnapshot,
        *,
        source_path: str | None = None,
    ) -> dict[str, Any]:
        snapshot = self.load_snapshot(payload)
        warnings, skipped = self.normalize_plant_catalog(snapshot)
        stats = self.memory_store.import_snapshot(snapshot, source_path=source_path, skipped_plant_ids=skipped)
        if warnings:
            self.memory_store.write_sync_run(snapshot.sync_metadata.snapshot_id, warnings, stats, source_path=source_path)
        return {
            "snapshot_id": snapshot.sync_metadata.snapshot_id,
            "warnings": warnings,
            "stats": stats,
        }

    def snapshot_from_memory(self) -> GardenSnapshot:
        context = self.memory_store.export_context()
        latest_sync = context.get("latest_sync")
        snapshot_id = latest_sync["snapshot_id"] if latest_sync else "snapshot-memory-export"
        return GardenSnapshot.from_dict(
            {
                "garden": context["garden"],
                "beds": context["beds"],
                "obstacles": context["obstacles"],
                "plant_catalog": context["plant_catalog"],
                "plantings": context["plantings"],
                "observations": context["observations"],
                "sync_metadata": {
                    "snapshot_id": snapshot_id,
                    "exported_at": latest_sync["imported_at"] if latest_sync else "",
                    "source_app_version": "garden-helper-memory-export",
                    "metadata": {
                        "recent_activity": context["recent_activity"],
                    },
                },
            }
        )

    def export_memory_context(self) -> dict[str, Any]:
        context = self.memory_store.export_context()
        snapshot = self.snapshot_from_memory().to_dict()
        return {
            "memory_context": context,
            "planner_context": context,
            "snapshot": snapshot,
        }

    def export_farmbot_bundle(
        self,
        payload: str | Path | dict[str, Any] | GardenSnapshot | None = None,
    ) -> dict[str, Any]:
        snapshot = self.snapshot_from_memory() if payload is None else self.load_snapshot(payload)
        return snapshot_to_farmbot_bundle(snapshot)

    def import_farmbot_bundle(
        self,
        payload: str | Path | dict[str, Any],
        *,
        source_path: str | None = None,
    ) -> dict[str, Any]:
        snapshot = farmbot_bundle_to_snapshot(payload)
        report = self.import_snapshot(snapshot, source_path=source_path)
        report["bundle_format"] = "garden-helper-farmbot-bundle/v1"
        return report

    def prepare_farmbot_stack(
        self,
        *,
        runtime_dir: str | Path = DEFAULT_RUNTIME_DIR,
        host: str | None = None,
        port: int = 3000,
    ) -> dict[str, Any]:
        return prepare_farmbot_stack(runtime_dir=runtime_dir, host=host, port=port)


def pretty_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True)
