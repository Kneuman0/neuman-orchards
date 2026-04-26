from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .schema import Bed, GardenDimensions, GardenSnapshot, Observation, Obstacle, PlantCatalogEntry, Planting


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB_PATH = ROOT / "data" / "garden-memory.db"


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS garden_state (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    width REAL NOT NULL,
    height REAL NOT NULL,
    raw_json TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    sun_exposure TEXT,
    size TEXT,
    notes TEXT,
    active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS location_adjacency (
    location_id INTEGER NOT NULL REFERENCES locations(id),
    adjacent_id INTEGER NOT NULL REFERENCES locations(id),
    PRIMARY KEY (location_id, adjacent_id)
);

CREATE TABLE IF NOT EXISTS plants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS plantings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plant_id INTEGER NOT NULL REFERENCES plants(id),
    location_id INTEGER REFERENCES locations(id),
    quantity INTEGER,
    date_planted TEXT,
    date_removed TEXT,
    active INTEGER NOT NULL DEFAULT 1,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    planting_id INTEGER REFERENCES plantings(id),
    location_id INTEGER REFERENCES locations(id),
    activity_type TEXT NOT NULL,
    description TEXT NOT NULL,
    quantity TEXT,
    timestamp TEXT NOT NULL,
    source TEXT NOT NULL,
    source_key TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS observations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    planting_id INTEGER REFERENCES plantings(id),
    location_id INTEGER REFERENCES locations(id),
    observation TEXT NOT NULL,
    kind TEXT,
    possible_cause TEXT,
    timestamp TEXT NOT NULL,
    source TEXT NOT NULL,
    photo_ref TEXT,
    source_key TEXT UNIQUE,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sync_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_id TEXT NOT NULL UNIQUE,
    imported_at TEXT NOT NULL,
    source_path TEXT,
    warnings_json TEXT NOT NULL,
    stats_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS location_geometry (
    location_id INTEGER PRIMARY KEY REFERENCES locations(id),
    external_bed_id TEXT NOT NULL UNIQUE,
    snapshot_id TEXT NOT NULL,
    x REAL NOT NULL,
    y REAL NOT NULL,
    w REAL NOT NULL,
    h REAL NOT NULL,
    type TEXT NOT NULL,
    raw_json TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS obstacle_geometry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    external_obstacle_id TEXT NOT NULL UNIQUE,
    snapshot_id TEXT NOT NULL,
    name TEXT NOT NULL,
    x REAL NOT NULL,
    y REAL NOT NULL,
    w REAL NOT NULL,
    h REAL NOT NULL,
    type TEXT NOT NULL,
    notes TEXT,
    metadata_json TEXT NOT NULL,
    raw_json TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS plant_catalog_map (
    plant_id INTEGER NOT NULL REFERENCES plants(id),
    external_plant_id TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL,
    cultivar TEXT,
    species TEXT,
    source TEXT,
    metadata_json TEXT NOT NULL,
    raw_json TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS planting_geometry (
    planting_id INTEGER PRIMARY KEY REFERENCES plantings(id),
    external_planting_id TEXT NOT NULL UNIQUE,
    external_bed_id TEXT NOT NULL,
    snapshot_id TEXT NOT NULL,
    status TEXT NOT NULL,
    grid_cells_json TEXT NOT NULL,
    raw_json TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS observation_links (
    observation_id INTEGER PRIMARY KEY REFERENCES observations(id),
    external_observation_id TEXT NOT NULL UNIQUE,
    snapshot_id TEXT NOT NULL,
    raw_json TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_locations_name ON locations(name);
CREATE INDEX IF NOT EXISTS idx_plants_name ON plants(name);
CREATE INDEX IF NOT EXISTS idx_plantings_location_id ON plantings(location_id);
CREATE INDEX IF NOT EXISTS idx_activities_timestamp ON activities(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_observations_timestamp ON observations(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_obstacle_geometry_external_id ON obstacle_geometry(external_obstacle_id);
"""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class GardenMemoryStore:
    def __init__(self, db_path: str | Path = DEFAULT_DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._connection: sqlite3.Connection | None = None

    @property
    def connection(self) -> sqlite3.Connection:
        if self._connection is None:
            self._connection = sqlite3.connect(self.db_path)
            self._connection.row_factory = sqlite3.Row
            self._connection.execute("PRAGMA foreign_keys=ON")
            self._connection.execute("PRAGMA journal_mode=WAL")
            self._connection.executescript(SCHEMA_SQL)
        return self._connection

    def close(self) -> None:
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def write_sync_run(
        self,
        snapshot_id: str,
        warnings: list[str],
        stats: dict[str, Any],
        source_path: str | None = None,
    ) -> None:
        self.connection.execute(
            """
            INSERT INTO sync_runs (snapshot_id, imported_at, source_path, warnings_json, stats_json)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(snapshot_id) DO UPDATE SET
                imported_at=excluded.imported_at,
                source_path=excluded.source_path,
                warnings_json=excluded.warnings_json,
                stats_json=excluded.stats_json
            """,
            (
                snapshot_id,
                utc_now(),
                source_path,
                json.dumps(warnings),
                json.dumps(stats),
            ),
        )
        self.connection.commit()

    def upsert_garden_state(self, garden: GardenDimensions) -> None:
        now = utc_now()
        self.connection.execute(
            """
            INSERT INTO garden_state (id, width, height, raw_json, updated_at)
            VALUES (1, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                width=excluded.width,
                height=excluded.height,
                raw_json=excluded.raw_json,
                updated_at=excluded.updated_at
            """,
            (
                garden.width,
                garden.height,
                json.dumps(asdict(garden)),
                now,
            ),
        )

    def upsert_location(self, bed: Bed, snapshot_id: str) -> int:
        row = self.connection.execute(
            "SELECT location_id FROM location_geometry WHERE external_bed_id = ?",
            (bed.bed_id,),
        ).fetchone()

        size = f"{bed.w:g}x{bed.h:g} ft"
        description = f"{bed.type} bed"
        now = utc_now()

        if row:
            location_id = int(row["location_id"])
            self.connection.execute(
                """
                UPDATE locations
                SET name = ?, description = ?, size = ?, notes = ?, active = 1, updated_at = ?
                WHERE id = ?
                """,
                (bed.name, description, size, bed.notes, now, location_id),
            )
        else:
            cursor = self.connection.execute(
                """
                INSERT INTO locations (name, description, size, notes, active, updated_at)
                VALUES (?, ?, ?, ?, 1, ?)
                """,
                (bed.name, description, size, bed.notes, now),
            )
            location_id = int(cursor.lastrowid)

        self.connection.execute(
            """
            INSERT INTO location_geometry (location_id, external_bed_id, snapshot_id, x, y, w, h, type, raw_json, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(location_id) DO UPDATE SET
                external_bed_id=excluded.external_bed_id,
                snapshot_id=excluded.snapshot_id,
                x=excluded.x,
                y=excluded.y,
                w=excluded.w,
                h=excluded.h,
                type=excluded.type,
                raw_json=excluded.raw_json,
                updated_at=excluded.updated_at
            """,
            (
                location_id,
                bed.bed_id,
                snapshot_id,
                bed.x,
                bed.y,
                bed.w,
                bed.h,
                bed.type,
                json.dumps(asdict(bed)),
                now,
            ),
        )
        return location_id

    def upsert_obstacle(self, obstacle: Obstacle, snapshot_id: str) -> int:
        now = utc_now()
        cursor = self.connection.execute(
            """
            INSERT INTO obstacle_geometry
            (external_obstacle_id, snapshot_id, name, x, y, w, h, type, notes, metadata_json, raw_json, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(external_obstacle_id) DO UPDATE SET
                snapshot_id=excluded.snapshot_id,
                name=excluded.name,
                x=excluded.x,
                y=excluded.y,
                w=excluded.w,
                h=excluded.h,
                type=excluded.type,
                notes=excluded.notes,
                metadata_json=excluded.metadata_json,
                raw_json=excluded.raw_json,
                updated_at=excluded.updated_at
            """,
            (
                obstacle.obstacle_id,
                snapshot_id,
                obstacle.name,
                obstacle.x,
                obstacle.y,
                obstacle.w,
                obstacle.h,
                obstacle.type,
                obstacle.notes,
                json.dumps(obstacle.metadata),
                json.dumps(asdict(obstacle)),
                now,
            ),
        )
        return int(cursor.lastrowid or 0)

    def find_plant_by_external_id(self, external_plant_id: str) -> sqlite3.Row | None:
        return self.connection.execute(
            """
            SELECT p.*, m.display_name, m.cultivar, m.species, m.source
            FROM plant_catalog_map m
            JOIN plants p ON p.id = m.plant_id
            WHERE m.external_plant_id = ?
            """,
            (external_plant_id,),
        ).fetchone()

    def find_plant_by_name(self, name: str) -> list[sqlite3.Row]:
        lowered = name.casefold()
        return self.connection.execute(
            "SELECT * FROM plants WHERE lower(name) = ? OR lower(type) = ?",
            (lowered, lowered),
        ).fetchall()

    def upsert_plant(self, plant: PlantCatalogEntry) -> int:
        existing = self.find_plant_by_external_id(plant.plant_id)
        now = utc_now()
        plant_name = plant.cultivar or plant.display_name
        notes_parts = []
        if plant.species:
            notes_parts.append(f"species={plant.species}")
        if plant.source:
            notes_parts.append(f"source={plant.source}")
        notes_blob = "; ".join(notes_parts) if notes_parts else None

        if existing:
            plant_db_id = int(existing["id"])
            self.connection.execute(
                """
                UPDATE plants SET name = ?, type = ?, notes = ?, updated_at = ?
                WHERE id = ?
                """,
                (plant_name, plant.type, notes_blob, now, plant_db_id),
            )
        else:
            name_matches = self.find_plant_by_name(plant_name)
            if len(name_matches) == 1:
                plant_db_id = int(name_matches[0]["id"])
                self.connection.execute(
                    """
                    UPDATE plants SET name = ?, type = ?, notes = ?, updated_at = ?
                    WHERE id = ?
                    """,
                    (plant_name, plant.type, notes_blob, now, plant_db_id),
                )
            else:
                cursor = self.connection.execute(
                    "INSERT INTO plants (name, type, notes, updated_at) VALUES (?, ?, ?, ?)",
                    (plant_name, plant.type, notes_blob, now),
                )
                plant_db_id = int(cursor.lastrowid)

        self.connection.execute(
            """
            INSERT INTO plant_catalog_map
            (plant_id, external_plant_id, display_name, cultivar, species, source, metadata_json, raw_json, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(external_plant_id) DO UPDATE SET
                plant_id=excluded.plant_id,
                display_name=excluded.display_name,
                cultivar=excluded.cultivar,
                species=excluded.species,
                source=excluded.source,
                metadata_json=excluded.metadata_json,
                raw_json=excluded.raw_json,
                updated_at=excluded.updated_at
            """,
            (
                plant_db_id,
                plant.plant_id,
                plant.display_name,
                plant.cultivar,
                plant.species,
                plant.source,
                json.dumps(plant.metadata),
                json.dumps(asdict(plant)),
                now,
            ),
        )
        return plant_db_id

    def upsert_planting(
        self,
        planting: Planting,
        plant_db_id: int,
        location_id: int,
        snapshot_id: str,
    ) -> int:
        row = self.connection.execute(
            "SELECT planting_id FROM planting_geometry WHERE external_planting_id = ?",
            (planting.planting_id,),
        ).fetchone()
        now = utc_now()
        is_active = 1 if planting.status.casefold() not in {"removed", "inactive", "harvested"} else 0
        date_removed = None if is_active else now[:10]
        notes = planting.notes
        if planting.metadata:
            notes = f"{notes}\nmetadata={json.dumps(planting.metadata, sort_keys=True)}".strip()

        if row:
            planting_db_id = int(row["planting_id"])
            self.connection.execute(
                """
                UPDATE plantings
                SET plant_id = ?, location_id = ?, quantity = ?, date_planted = ?, date_removed = ?, active = ?, notes = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    plant_db_id,
                    location_id,
                    planting.quantity,
                    planting.date_planted,
                    date_removed,
                    is_active,
                    notes,
                    now,
                    planting_db_id,
                ),
            )
        else:
            cursor = self.connection.execute(
                """
                INSERT INTO plantings (plant_id, location_id, quantity, date_planted, date_removed, active, notes, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    plant_db_id,
                    location_id,
                    planting.quantity,
                    planting.date_planted,
                    date_removed,
                    is_active,
                    notes,
                    now,
                ),
            )
            planting_db_id = int(cursor.lastrowid)

        self.connection.execute(
            """
            INSERT INTO planting_geometry
            (planting_id, external_planting_id, external_bed_id, snapshot_id, status, grid_cells_json, raw_json, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(planting_id) DO UPDATE SET
                external_planting_id=excluded.external_planting_id,
                external_bed_id=excluded.external_bed_id,
                snapshot_id=excluded.snapshot_id,
                status=excluded.status,
                grid_cells_json=excluded.grid_cells_json,
                raw_json=excluded.raw_json,
                updated_at=excluded.updated_at
            """,
            (
                planting_db_id,
                planting.planting_id,
                planting.bed_id,
                snapshot_id,
                planting.status,
                json.dumps([asdict(cell) for cell in planting.grid_cells]),
                json.dumps(asdict(planting)),
                now,
            ),
        )
        return planting_db_id

    def upsert_observation(
        self,
        observation: Observation,
        snapshot_id: str,
        location_id: int | None = None,
        planting_id: int | None = None,
    ) -> int:
        row = self.connection.execute(
            """
            SELECT o.id
            FROM observation_links l
            JOIN observations o ON o.id = l.observation_id
            WHERE l.external_observation_id = ?
            """,
            (observation.observation_id,),
        ).fetchone()

        now = utc_now()
        if row:
            observation_db_id = int(row["id"])
            self.connection.execute(
                """
                UPDATE observations
                SET planting_id = ?, location_id = ?, observation = ?, kind = ?, timestamp = ?, photo_ref = ?, source = ?, source_key = ?
                WHERE id = ?
                """,
                (
                    planting_id,
                    location_id,
                    observation.description,
                    observation.kind,
                    observation.timestamp,
                    observation.photo_ref,
                    "snapshot_import",
                    observation.observation_id,
                    observation_db_id,
                ),
            )
        else:
            cursor = self.connection.execute(
                """
                INSERT INTO observations
                (planting_id, location_id, observation, kind, timestamp, source, photo_ref, source_key)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    planting_id,
                    location_id,
                    observation.description,
                    observation.kind,
                    observation.timestamp,
                    "snapshot_import",
                    observation.photo_ref,
                    observation.observation_id,
                ),
            )
            observation_db_id = int(cursor.lastrowid)

        self.connection.execute(
            """
            INSERT INTO observation_links (observation_id, external_observation_id, snapshot_id, raw_json)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(observation_id) DO UPDATE SET
                external_observation_id=excluded.external_observation_id,
                snapshot_id=excluded.snapshot_id,
                raw_json=excluded.raw_json
            """,
            (
                observation_db_id,
                observation.observation_id,
                snapshot_id,
                json.dumps(asdict(observation)),
            ),
        )
        return observation_db_id

    def commit(self) -> None:
        self.connection.commit()

    def export_context(self) -> dict[str, Any]:
        stored_garden = self.connection.execute(
            "SELECT width, height FROM garden_state WHERE id = 1"
        ).fetchone()
        beds = self.connection.execute(
            """
            SELECT l.id, l.name, l.notes, g.external_bed_id, g.x, g.y, g.w, g.h, g.type
            FROM locations l
            JOIN location_geometry g ON g.location_id = l.id
            WHERE l.active = 1
            ORDER BY l.name
            """
        ).fetchall()

        garden_width = 0.0
        garden_height = 0.0
        bed_items: list[dict[str, Any]] = []
        for bed in beds:
            garden_width = max(garden_width, float(bed["x"]) + float(bed["w"]))
            garden_height = max(garden_height, float(bed["y"]) + float(bed["h"]))
            bed_items.append(
                {
                    "bed_id": bed["external_bed_id"],
                    "name": bed["name"],
                    "x": bed["x"],
                    "y": bed["y"],
                    "w": bed["w"],
                    "h": bed["h"],
                    "type": bed["type"],
                    "notes": bed["notes"] or "",
                }
            )

        obstacles = self.connection.execute(
            """
            SELECT external_obstacle_id, name, x, y, w, h, type, notes, metadata_json
            FROM obstacle_geometry
            ORDER BY external_obstacle_id
            """
        ).fetchall()
        obstacle_items = []
        for obstacle in obstacles:
            garden_width = max(garden_width, float(obstacle["x"]) + float(obstacle["w"]))
            garden_height = max(garden_height, float(obstacle["y"]) + float(obstacle["h"]))
            obstacle_items.append(
                {
                    "obstacle_id": obstacle["external_obstacle_id"],
                    "name": obstacle["name"],
                    "x": obstacle["x"],
                    "y": obstacle["y"],
                    "w": obstacle["w"],
                    "h": obstacle["h"],
                    "type": obstacle["type"],
                    "notes": obstacle["notes"] or "",
                    "metadata": json.loads(obstacle["metadata_json"] or "{}"),
                }
            )

        plant_catalog = self.connection.execute(
            """
            SELECT m.external_plant_id, m.display_name, p.type, m.cultivar, m.species, m.source, m.metadata_json
            FROM plant_catalog_map m
            JOIN plants p ON p.id = m.plant_id
            ORDER BY m.display_name
            """
        ).fetchall()
        plant_catalog_items = [
            {
                "plant_id": row["external_plant_id"],
                "display_name": row["display_name"],
                "type": row["type"],
                "cultivar": row["cultivar"],
                "species": row["species"],
                "source": row["source"],
                "metadata": json.loads(row["metadata_json"] or "{}"),
            }
            for row in plant_catalog
        ]

        plantings = self.connection.execute(
            """
            SELECT
                pg.external_planting_id,
                pg.external_bed_id,
                m.external_plant_id,
                pt.quantity,
                pt.date_planted,
                pg.status,
                pt.notes,
                pg.grid_cells_json
            FROM planting_geometry pg
            JOIN plantings pt ON pt.id = pg.planting_id
            JOIN plant_catalog_map m ON m.plant_id = pt.plant_id
            ORDER BY pg.external_bed_id, pg.external_planting_id
            """
        ).fetchall()
        planting_items = [
            {
                "planting_id": row["external_planting_id"],
                "bed_id": row["external_bed_id"],
                "plant_id": row["external_plant_id"],
                "quantity": row["quantity"],
                "grid_cells": json.loads(row["grid_cells_json"]),
                "date_planted": row["date_planted"],
                "status": row["status"],
                "notes": row["notes"] or "",
            }
            for row in plantings
        ]

        observations = self.connection.execute(
            """
            SELECT l.external_observation_id, o.timestamp, o.kind, o.observation, o.photo_ref,
                   lg.external_bed_id, pg.external_planting_id
            FROM observation_links l
            JOIN observations o ON o.id = l.observation_id
            LEFT JOIN location_geometry lg ON lg.location_id = o.location_id
            LEFT JOIN planting_geometry pg ON pg.planting_id = o.planting_id
            ORDER BY o.timestamp DESC
            """
        ).fetchall()
        observation_items = [
            {
                "observation_id": row["external_observation_id"],
                "timestamp": row["timestamp"],
                "kind": row["kind"] or "observation",
                "description": row["observation"],
                "photo_ref": row["photo_ref"],
                "bed_id": row["external_bed_id"],
                "planting_id": row["external_planting_id"],
            }
            for row in observations
        ]

        recent_activity = self.connection.execute(
            """
            SELECT activity_type, description, timestamp
            FROM activities
            ORDER BY timestamp DESC
            LIMIT 20
            """
        ).fetchall()

        latest_sync = self.connection.execute(
            "SELECT snapshot_id, imported_at, warnings_json, stats_json FROM sync_runs ORDER BY imported_at DESC LIMIT 1"
        ).fetchone()
        latest_sync_payload = None
        if latest_sync:
            latest_sync_payload = dict(latest_sync)
            latest_sync_payload["warnings"] = json.loads(latest_sync_payload.pop("warnings_json"))
            latest_sync_payload["stats"] = json.loads(latest_sync_payload.pop("stats_json"))

        return {
            "garden": {
                "width": stored_garden["width"] if stored_garden else (garden_width or 20),
                "height": stored_garden["height"] if stored_garden else (garden_height or 18),
            },
            "beds": bed_items,
            "obstacles": obstacle_items,
            "plant_catalog": plant_catalog_items,
            "plantings": planting_items,
            "observations": observation_items,
            "recent_activity": [dict(row) for row in recent_activity],
            "latest_sync": latest_sync_payload,
        }

    def import_snapshot(
        self,
        snapshot: GardenSnapshot,
        *,
        source_path: str | None = None,
        skipped_plant_ids: set[str] | None = None,
    ) -> dict[str, int]:
        skipped_plant_ids = skipped_plant_ids or set()
        location_ids: dict[str, int] = {}
        plant_ids: dict[str, int] = {}
        planting_ids: dict[str, int] = {}

        stats = {
            "garden_state_upserted": 0,
            "beds_upserted": 0,
            "obstacles_upserted": 0,
            "plants_upserted": 0,
            "plantings_upserted": 0,
            "observations_upserted": 0,
            "plantings_skipped": 0,
        }

        self.upsert_garden_state(snapshot.garden)
        stats["garden_state_upserted"] += 1

        for bed in snapshot.beds:
            location_ids[bed.bed_id] = self.upsert_location(bed, snapshot.sync_metadata.snapshot_id)
            stats["beds_upserted"] += 1

        for obstacle in snapshot.obstacles:
            self.upsert_obstacle(obstacle, snapshot.sync_metadata.snapshot_id)
            stats["obstacles_upserted"] += 1

        for plant in snapshot.plant_catalog:
            if plant.plant_id in skipped_plant_ids:
                continue
            plant_ids[plant.plant_id] = self.upsert_plant(plant)
            stats["plants_upserted"] += 1

        for planting in snapshot.plantings:
            if planting.plant_id in skipped_plant_ids:
                stats["plantings_skipped"] += 1
                continue
            planting_ids[planting.planting_id] = self.upsert_planting(
                planting,
                plant_ids[planting.plant_id],
                location_ids[planting.bed_id],
                snapshot.sync_metadata.snapshot_id,
            )
            stats["plantings_upserted"] += 1

        for observation in snapshot.observations:
            location_id = location_ids.get(observation.bed_id or "")
            planting_id = planting_ids.get(observation.planting_id or "")
            self.upsert_observation(
                observation,
                snapshot.sync_metadata.snapshot_id,
                location_id=location_id,
                planting_id=planting_id,
            )
            stats["observations_upserted"] += 1

        self.write_sync_run(snapshot.sync_metadata.snapshot_id, [], stats, source_path=source_path)
        self.commit()
        return stats
