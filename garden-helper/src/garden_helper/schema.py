from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "schemas" / "garden_snapshot.schema.json"


class SnapshotValidationError(ValueError):
    pass


def _as_float(value: Any, field_name: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise SnapshotValidationError(f"{field_name} must be numeric") from exc


def _as_int(value: Any, field_name: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise SnapshotValidationError(f"{field_name} must be an integer") from exc


@dataclass(slots=True)
class GardenDimensions:
    width: float
    height: float

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GardenDimensions":
        return cls(
            width=_as_float(data.get("width"), "garden.width"),
            height=_as_float(data.get("height"), "garden.height"),
        )


@dataclass(slots=True)
class Bed:
    bed_id: str
    name: str
    x: float
    y: float
    w: float
    h: float
    type: str
    notes: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Bed":
        bed_id = str(data.get("bed_id") or "").strip()
        if not bed_id:
            raise SnapshotValidationError("beds[].bed_id is required")
        return cls(
            bed_id=bed_id,
            name=str(data.get("name") or bed_id),
            x=_as_float(data.get("x", 0), f"beds[{bed_id}].x"),
            y=_as_float(data.get("y", 0), f"beds[{bed_id}].y"),
            w=_as_float(data.get("w"), f"beds[{bed_id}].w"),
            h=_as_float(data.get("h"), f"beds[{bed_id}].h"),
            type=str(data.get("type") or "raised"),
            notes=str(data.get("notes") or ""),
            metadata=dict(data.get("metadata") or {}),
        )


@dataclass(slots=True)
class Obstacle:
    obstacle_id: str
    name: str
    x: float
    y: float
    w: float
    h: float
    type: str = "obstacle"
    notes: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Obstacle":
        obstacle_id = str(data.get("obstacle_id") or data.get("id") or "").strip()
        if not obstacle_id:
            raise SnapshotValidationError("obstacles[].obstacle_id is required")
        return cls(
            obstacle_id=obstacle_id,
            name=str(data.get("name") or obstacle_id),
            x=_as_float(data.get("x", 0), f"obstacles[{obstacle_id}].x"),
            y=_as_float(data.get("y", 0), f"obstacles[{obstacle_id}].y"),
            w=_as_float(data.get("w", data.get("diam", 1)), f"obstacles[{obstacle_id}].w"),
            h=_as_float(data.get("h", data.get("diam", 1)), f"obstacles[{obstacle_id}].h"),
            type=str(data.get("type") or "obstacle"),
            notes=str(data.get("notes") or ""),
            metadata=dict(data.get("metadata") or {}),
        )


@dataclass(slots=True)
class PlantCatalogEntry:
    plant_id: str
    display_name: str
    type: str | None = None
    cultivar: str | None = None
    species: str | None = None
    source: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PlantCatalogEntry":
        plant_id = str(data.get("plant_id") or "").strip()
        if not plant_id:
            raise SnapshotValidationError("plant_catalog[].plant_id is required")
        display_name = str(data.get("display_name") or "").strip()
        if not display_name:
            raise SnapshotValidationError(f"plant_catalog[{plant_id}].display_name is required")
        return cls(
            plant_id=plant_id,
            display_name=display_name,
            type=(str(data["type"]).strip() if data.get("type") else None),
            cultivar=(str(data["cultivar"]).strip() if data.get("cultivar") else None),
            species=(str(data["species"]).strip() if data.get("species") else None),
            source=(str(data["source"]).strip() if data.get("source") else None),
            metadata=dict(data.get("metadata") or {}),
        )


@dataclass(slots=True)
class GridCell:
    row: int
    col: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GridCell":
        return cls(
            row=_as_int(data.get("row"), "grid_cells[].row"),
            col=_as_int(data.get("col"), "grid_cells[].col"),
        )


@dataclass(slots=True)
class Planting:
    planting_id: str
    bed_id: str
    plant_id: str
    quantity: int
    grid_cells: list[GridCell]
    date_planted: str | None = None
    status: str = "planned"
    notes: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Planting":
        planting_id = str(data.get("planting_id") or "").strip()
        if not planting_id:
            raise SnapshotValidationError("plantings[].planting_id is required")
        bed_id = str(data.get("bed_id") or "").strip()
        plant_id = str(data.get("plant_id") or "").strip()
        if not bed_id or not plant_id:
            raise SnapshotValidationError(f"plantings[{planting_id}] must include bed_id and plant_id")
        raw_cells = data.get("grid_cells") or []
        if not isinstance(raw_cells, list) or not raw_cells:
            raise SnapshotValidationError(f"plantings[{planting_id}].grid_cells must be a non-empty list")
        return cls(
            planting_id=planting_id,
            bed_id=bed_id,
            plant_id=plant_id,
            quantity=_as_int(data.get("quantity", 1), f"plantings[{planting_id}].quantity"),
            grid_cells=[GridCell.from_dict(item) for item in raw_cells],
            date_planted=(str(data["date_planted"]).strip() if data.get("date_planted") else None),
            status=str(data.get("status") or "planned"),
            notes=str(data.get("notes") or ""),
            metadata=dict(data.get("metadata") or {}),
        )


@dataclass(slots=True)
class Observation:
    observation_id: str
    timestamp: str
    kind: str
    description: str
    photo_ref: str | None = None
    bed_id: str | None = None
    planting_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Observation":
        observation_id = str(data.get("observation_id") or "").strip()
        if not observation_id:
            raise SnapshotValidationError("observations[].observation_id is required")
        bed_id = str(data.get("bed_id") or "").strip() or None
        planting_id = str(data.get("planting_id") or "").strip() or None
        if not bed_id and not planting_id:
            raise SnapshotValidationError(
                f"observations[{observation_id}] must reference bed_id or planting_id"
            )
        return cls(
            observation_id=observation_id,
            timestamp=str(data.get("timestamp") or ""),
            kind=str(data.get("kind") or "observation"),
            description=str(data.get("description") or ""),
            photo_ref=(str(data["photo_ref"]).strip() if data.get("photo_ref") else None),
            bed_id=bed_id,
            planting_id=planting_id,
            metadata=dict(data.get("metadata") or {}),
        )


@dataclass(slots=True)
class SnapshotMetadata:
    snapshot_id: str
    exported_at: str
    source_app_version: str
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SnapshotMetadata":
        snapshot_id = str(data.get("snapshot_id") or "").strip()
        if not snapshot_id:
            raise SnapshotValidationError("sync_metadata.snapshot_id is required")
        return cls(
            snapshot_id=snapshot_id,
            exported_at=str(data.get("exported_at") or ""),
            source_app_version=str(data.get("source_app_version") or "unknown"),
            metadata=dict(data.get("metadata") or {}),
        )


@dataclass(slots=True)
class GardenSnapshot:
    garden: GardenDimensions
    beds: list[Bed]
    obstacles: list[Obstacle]
    plant_catalog: list[PlantCatalogEntry]
    plantings: list[Planting]
    observations: list[Observation]
    sync_metadata: SnapshotMetadata

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GardenSnapshot":
        if not isinstance(data, dict):
            raise SnapshotValidationError("snapshot payload must be an object")

        required = ("garden", "beds", "plant_catalog", "plantings", "observations", "sync_metadata")
        missing = [key for key in required if key not in data]
        if missing:
            raise SnapshotValidationError(f"snapshot is missing keys: {', '.join(missing)}")

        snapshot = cls(
            garden=GardenDimensions.from_dict(dict(data["garden"])),
            beds=[Bed.from_dict(item) for item in data.get("beds") or []],
            obstacles=[Obstacle.from_dict(item) for item in data.get("obstacles") or []],
            plant_catalog=[PlantCatalogEntry.from_dict(item) for item in data.get("plant_catalog") or []],
            plantings=[Planting.from_dict(item) for item in data.get("plantings") or []],
            observations=[Observation.from_dict(item) for item in data.get("observations") or []],
            sync_metadata=SnapshotMetadata.from_dict(dict(data["sync_metadata"])),
        )
        snapshot.validate()
        return snapshot

    def validate(self) -> None:
        bed_ids = {bed.bed_id for bed in self.beds}
        if len(bed_ids) != len(self.beds):
            raise SnapshotValidationError("beds[].bed_id values must be unique")

        plant_ids = {plant.plant_id for plant in self.plant_catalog}
        if len(plant_ids) != len(self.plant_catalog):
            raise SnapshotValidationError("plant_catalog[].plant_id values must be unique")

        planting_ids = {planting.planting_id for planting in self.plantings}
        if len(planting_ids) != len(self.plantings):
            raise SnapshotValidationError("plantings[].planting_id values must be unique")

        for planting in self.plantings:
            if planting.bed_id not in bed_ids:
                raise SnapshotValidationError(
                    f"planting {planting.planting_id} references unknown bed_id {planting.bed_id}"
                )
            if planting.plant_id not in plant_ids:
                raise SnapshotValidationError(
                    f"planting {planting.planting_id} references unknown plant_id {planting.plant_id}"
                )

        for observation in self.observations:
            if observation.bed_id and observation.bed_id not in bed_ids:
                raise SnapshotValidationError(
                    f"observation {observation.observation_id} references unknown bed_id {observation.bed_id}"
                )
            if observation.planting_id and observation.planting_id not in planting_ids:
                raise SnapshotValidationError(
                    "observation "
                    f"{observation.observation_id} references unknown planting_id {observation.planting_id}"
                )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def load_snapshot(path: str | Path) -> GardenSnapshot:
    with Path(path).open("r", encoding="utf-8") as handle:
        return GardenSnapshot.from_dict(json.load(handle))


def write_snapshot(path: str | Path, snapshot: GardenSnapshot | dict[str, Any]) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = snapshot.to_dict() if isinstance(snapshot, GardenSnapshot) else snapshot
    with target.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    return target
