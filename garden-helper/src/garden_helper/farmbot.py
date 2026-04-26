from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import asdict
from datetime import datetime, timezone
from math import ceil, sqrt
from pathlib import Path
from typing import Any

from .ids import new_prefixed_id, slugify, stable_plant_id, strip_display_label
from .schema import (
    Bed,
    GardenDimensions,
    GardenSnapshot,
    GridCell,
    Observation,
    Obstacle,
    PlantCatalogEntry,
    Planting,
    SnapshotMetadata,
    load_snapshot,
)


MM_PER_FOOT = 304.8
BUNDLE_FORMAT = "garden-helper-farmbot-bundle/v1"


class FarmBotBundleError(ValueError):
    pass


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ft_to_mm(value: float) -> int:
    return int(round(float(value) * MM_PER_FOOT))


def mm_to_ft(value: float) -> float:
    return round(float(value) / MM_PER_FOOT, 4)


def _base_criteria() -> dict[str, Any]:
    return {
        "day": {"op": "<", "days_ago": 0},
        "string_eq": {},
        "number_eq": {},
        "number_lt": {},
        "number_gt": {},
    }


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def _first_string(values: Any, default: str | None = None) -> str | None:
    items = _string_list(values)
    return items[0] if items else default


def _grid_cells_string(cells: list[GridCell]) -> str:
    return ";".join(f"{cell.row},{cell.col}" for cell in cells)


def _parse_grid_cells(value: str) -> list[GridCell]:
    cells: list[GridCell] = []
    for part in filter(None, (value or "").split(";")):
        row_text, _, col_text = part.partition(",")
        if not row_text or not col_text:
            continue
        cells.append(GridCell(row=int(row_text), col=int(col_text)))
    return cells


def _status_to_stage(status: str) -> str:
    normalized = (status or "planned").casefold()
    if normalized in {"planned", "plan", "seeded"}:
        return "planned"
    if normalized in {"planted", "active", "growing"}:
        return "planted"
    if normalized in {"harvested", "removed", "inactive"}:
        return "harvested"
    return status or "planned"


def _stage_to_status(stage: str, fallback: str = "planned") -> str:
    normalized = (stage or "").casefold()
    if normalized == "planned":
        return "planned"
    if normalized in {"planted", "active"}:
        return "planted"
    if normalized in {"harvested", "removed"}:
        return "harvested"
    return fallback


def _zone_resource(
    *,
    name: str,
    x1_mm: int,
    y1_mm: int,
    x2_mm: int,
    y2_mm: int,
    kind: str,
    stable_id: str,
) -> dict[str, Any]:
    criteria = _base_criteria()
    criteria["number_gt"] = {"x": x1_mm, "y": y1_mm}
    criteria["number_lt"] = {"x": x2_mm, "y": y2_mm}
    criteria["string_eq"] = {
        "gh_kind": [kind],
        "gh_id": [stable_id],
    }
    return {
        "name": name,
        "sort_type": "xy_ascending",
        "point_ids": [],
        "criteria": criteria,
        "member_count": 0,
    }


def _cell_bounds_mm(bed: Bed, cell: GridCell) -> tuple[int, int, int, int]:
    left = ft_to_mm(bed.x + cell.col)
    top = ft_to_mm(bed.y + cell.row)
    right = ft_to_mm(bed.x + cell.col + 1)
    bottom = ft_to_mm(bed.y + cell.row + 1)
    return left, top, right, bottom


def _points_in_rect(left: int, top: int, right: int, bottom: int, count: int) -> list[tuple[int, int]]:
    if count <= 0:
        return []
    if count == 1:
        return [((left + right) // 2, (top + bottom) // 2)]

    width = max(1, right - left)
    height = max(1, bottom - top)
    cols = max(1, ceil(sqrt(count)))
    rows = max(1, ceil(count / cols))
    xs = [int(round(left + ((idx + 1) * width / (cols + 1)))) for idx in range(cols)]
    ys = [int(round(top + ((idx + 1) * height / (rows + 1)))) for idx in range(rows)]

    coords: list[tuple[int, int]] = []
    for x in xs:
        for y in ys:
            coords.append((x, y))
            if len(coords) == count:
                return coords
    return coords


def _centroid_for_cells(bed: Bed, cells: list[GridCell]) -> tuple[int, int]:
    if not cells:
        return ft_to_mm(bed.x + 0.5), ft_to_mm(bed.y + 0.5)
    left = min(_cell_bounds_mm(bed, cell)[0] for cell in cells)
    top = min(_cell_bounds_mm(bed, cell)[1] for cell in cells)
    right = max(_cell_bounds_mm(bed, cell)[2] for cell in cells)
    bottom = max(_cell_bounds_mm(bed, cell)[3] for cell in cells)
    return (left + right) // 2, (top + bottom) // 2


def _estimate_radius_mm(bed: Bed, planting: Planting) -> int:
    cell_area_sq_mm = MM_PER_FOOT * MM_PER_FOOT
    occupied_cells = max(1, len(planting.grid_cells))
    area_per_point = (cell_area_sq_mm * occupied_cells) / max(1, planting.quantity)
    spacing = sqrt(area_per_point)
    return max(12, int(round(spacing * 0.35)))


def _plant_points_for_planting(
    bed: Bed,
    planting: Planting,
    plant: PlantCatalogEntry,
    snapshot_id: str,
) -> list[dict[str, Any]]:
    meta = {
        "gh_kind": "planting_point",
        "gh_snapshot_id": snapshot_id,
        "gh_bed_id": planting.bed_id,
        "gh_planting_id": planting.planting_id,
        "gh_plant_id": planting.plant_id,
        "gh_display_name": plant.display_name,
        "gh_quantity": str(planting.quantity),
        "gh_grid_cells": _grid_cells_string(planting.grid_cells),
        "gh_status": planting.status,
        "gh_notes": planting.notes,
    }

    points: list[tuple[int, int]] = []
    if planting.quantity <= 1:
        points = [_centroid_for_cells(bed, planting.grid_cells)]
    else:
        cells = planting.grid_cells or [GridCell(row=0, col=0)]
        base, extra = divmod(planting.quantity, len(cells))
        for index, cell in enumerate(cells):
            count = base + (1 if index < extra else 0)
            if count <= 0:
                continue
            left, top, right, bottom = _cell_bounds_mm(bed, cell)
            points.extend(_points_in_rect(left, top, right, bottom, count))

    radius = _estimate_radius_mm(bed, planting)
    openfarm_slug = plant.metadata.get("openfarm_slug") or slugify(plant.display_name)
    resources: list[dict[str, Any]] = []
    for index, (x_mm, y_mm) in enumerate(points, start=1):
        point_meta = dict(meta)
        point_meta["gh_point_index"] = str(index)
        point_meta["gh_point_count"] = str(len(points))
        resources.append(
            {
                "name": plant.display_name,
                "pointer_type": "Plant",
                "openfarm_slug": openfarm_slug,
                "plant_stage": _status_to_stage(planting.status),
                "planted_at": planting.date_planted,
                "radius": radius,
                "depth": 0,
                "z": 0,
                "x": x_mm,
                "y": y_mm,
                "meta": point_meta,
            }
        )
    return resources


def snapshot_to_farmbot_bundle(snapshot: GardenSnapshot | dict[str, Any] | str | Path) -> dict[str, Any]:
    if isinstance(snapshot, (str, Path)):
        snapshot_obj = load_snapshot(snapshot)
    elif isinstance(snapshot, GardenSnapshot):
        snapshot_obj = snapshot
    elif isinstance(snapshot, dict):
        snapshot_obj = GardenSnapshot.from_dict(snapshot)
    else:
        raise FarmBotBundleError("snapshot_to_farmbot_bundle requires a snapshot payload or path")

    beds_by_id = {bed.bed_id: bed for bed in snapshot_obj.beds}
    plants_by_id = {plant.plant_id: plant for plant in snapshot_obj.plant_catalog}

    point_groups: list[dict[str, Any]] = []
    for bed in snapshot_obj.beds:
        point_groups.append(
            _zone_resource(
                name=bed.name,
                x1_mm=ft_to_mm(bed.x),
                y1_mm=ft_to_mm(bed.y),
                x2_mm=ft_to_mm(bed.x + bed.w),
                y2_mm=ft_to_mm(bed.y + bed.h),
                kind="bed",
                stable_id=bed.bed_id,
            )
        )

    for obstacle in snapshot_obj.obstacles:
        point_groups.append(
            _zone_resource(
                name=obstacle.name,
                x1_mm=ft_to_mm(obstacle.x),
                y1_mm=ft_to_mm(obstacle.y),
                x2_mm=ft_to_mm(obstacle.x + obstacle.w),
                y2_mm=ft_to_mm(obstacle.y + obstacle.h),
                kind="obstacle",
                stable_id=obstacle.obstacle_id,
            )
        )

    points: list[dict[str, Any]] = []
    for planting in snapshot_obj.plantings:
        bed = beds_by_id[planting.bed_id]
        plant = plants_by_id[planting.plant_id]
        points.extend(_plant_points_for_planting(bed, planting, plant, snapshot_obj.sync_metadata.snapshot_id))

    sidecar = {
        "schema_version": 1,
        "garden": asdict(snapshot_obj.garden),
        "beds": {
            bed.bed_id: asdict(bed)
            for bed in snapshot_obj.beds
        },
        "obstacles": {
            obstacle.obstacle_id: asdict(obstacle)
            for obstacle in snapshot_obj.obstacles
        },
        "plant_catalog": {
            plant.plant_id: {
                "display_name": plant.display_name,
                "type": plant.type,
                "cultivar": plant.cultivar,
                "species": plant.species,
                "source": plant.source,
                "metadata": plant.metadata,
            }
            for plant in snapshot_obj.plant_catalog
        },
        "observations": [asdict(observation) for observation in snapshot_obj.observations],
        "sync_metadata": asdict(snapshot_obj.sync_metadata),
    }

    return {
        "format": BUNDLE_FORMAT,
        "generated_at": _utc_now(),
        "farmbot": {
            "web_app_config": {
                "map_size_x": ft_to_mm(snapshot_obj.garden.width),
                "map_size_y": ft_to_mm(snapshot_obj.garden.height),
            },
            "point_groups": point_groups,
            "points": points,
        },
        "garden_helper_sidecar": sidecar,
    }


def write_farmbot_bundle(path: str | Path, payload: dict[str, Any]) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(f"{json.dumps(payload, indent=2)}\n", encoding="utf-8")
    return target


def _load_bundle(payload: dict[str, Any] | str | Path) -> dict[str, Any]:
    if isinstance(payload, dict):
        bundle = payload
    else:
        bundle = json.loads(Path(payload).read_text(encoding="utf-8"))
    if bundle.get("format") != BUNDLE_FORMAT:
        raise FarmBotBundleError(f"unsupported FarmBot bundle format: {bundle.get('format')!r}")
    return bundle


def _zone_identity(group: dict[str, Any]) -> tuple[str | None, str | None]:
    string_eq = ((group.get("criteria") or {}).get("string_eq") or {})
    return _first_string(string_eq.get("gh_kind")), _first_string(string_eq.get("gh_id"))


def _point_meta(point: dict[str, Any]) -> dict[str, str]:
    raw = point.get("meta") or {}
    return {str(key): str(value) for key, value in raw.items() if value is not None}


def _cells_from_positions(points: list[dict[str, Any]], bed: Bed) -> list[GridCell]:
    cells: dict[tuple[int, int], GridCell] = {}
    for point in points:
        x_ft = mm_to_ft(point.get("x", 0))
        y_ft = mm_to_ft(point.get("y", 0))
        col = max(0, int(x_ft - bed.x))
        row = max(0, int(y_ft - bed.y))
        cells[(row, col)] = GridCell(row=row, col=col)
    return list(cells.values()) or [GridCell(row=0, col=0)]


def farmbot_bundle_to_snapshot(payload: dict[str, Any] | str | Path) -> GardenSnapshot:
    bundle = _load_bundle(payload)
    farmbot = bundle.get("farmbot") or {}
    sidecar = bundle.get("garden_helper_sidecar") or {}
    sidecar_garden = sidecar.get("garden") or {}
    sidecar_beds = sidecar.get("beds") or {}
    sidecar_obstacles = sidecar.get("obstacles") or {}
    sidecar_catalog = sidecar.get("plant_catalog") or {}
    sync_metadata_raw = sidecar.get("sync_metadata") or {}

    config = farmbot.get("web_app_config") or {}
    garden = GardenDimensions(
        width=float(sidecar_garden.get("width", mm_to_ft(config.get("map_size_x", ft_to_mm(20))))),
        height=float(sidecar_garden.get("height", mm_to_ft(config.get("map_size_y", ft_to_mm(18))))),
    )

    beds: list[Bed] = []
    obstacles: list[Obstacle] = []
    for group in farmbot.get("point_groups") or []:
        kind, stable_id = _zone_identity(group)
        criteria = group.get("criteria") or {}
        number_gt = criteria.get("number_gt") or {}
        number_lt = criteria.get("number_lt") or {}
        x1 = float(number_gt.get("x", 0))
        y1 = float(number_gt.get("y", 0))
        x2 = float(number_lt.get("x", x1))
        y2 = float(number_lt.get("y", y1))
        if kind == "bed":
            bed_id = stable_id or new_prefixed_id("bed")
            extra = sidecar_beds.get(bed_id) or {}
            beds.append(
                Bed(
                    bed_id=bed_id,
                    name=str(extra.get("name") or group.get("name") or bed_id),
                    x=float(extra.get("x", mm_to_ft(x1))),
                    y=float(extra.get("y", mm_to_ft(y1))),
                    w=float(extra.get("w", mm_to_ft(max(0, x2 - x1)))),
                    h=float(extra.get("h", mm_to_ft(max(0, y2 - y1)))),
                    type=str(extra.get("type") or "raised"),
                    notes=str(extra.get("notes") or ""),
                    metadata=dict(extra.get("metadata") or {}),
                )
            )
        elif kind == "obstacle":
            obstacle_id = stable_id or new_prefixed_id("obstacle")
            extra = sidecar_obstacles.get(obstacle_id) or {}
            obstacles.append(
                Obstacle(
                    obstacle_id=obstacle_id,
                    name=str(extra.get("name") or group.get("name") or obstacle_id),
                    x=float(extra.get("x", mm_to_ft(x1))),
                    y=float(extra.get("y", mm_to_ft(y1))),
                    w=float(extra.get("w", mm_to_ft(max(0, x2 - x1)))),
                    h=float(extra.get("h", mm_to_ft(max(0, y2 - y1)))),
                    type=str(extra.get("type") or "obstacle"),
                    notes=str(extra.get("notes") or ""),
                    metadata=dict(extra.get("metadata") or {}),
                )
            )

    beds_by_id = {bed.bed_id: bed for bed in beds}
    plant_catalog: dict[str, PlantCatalogEntry] = {}
    grouped_points: dict[str, list[dict[str, Any]]] = defaultdict(list)
    fallback_groups: dict[tuple[str, str, str], str] = {}

    for point in farmbot.get("points") or []:
        if point.get("pointer_type") != "Plant":
            continue
        meta = _point_meta(point)
        planting_id = meta.get("gh_planting_id")
        if not planting_id:
            key = (
                meta.get("gh_bed_id", "unknown-bed"),
                meta.get("gh_plant_id", stable_plant_id(point.get("name") or "plant")),
                point.get("name") or "Plant",
            )
            planting_id = fallback_groups.setdefault(key, new_prefixed_id("planting"))
        grouped_points[planting_id].append(point)

        plant_id = meta.get("gh_plant_id") or stable_plant_id(point.get("name") or "plant")
        if plant_id not in plant_catalog:
            extra = sidecar_catalog.get(plant_id) or {}
            display_name = meta.get("gh_display_name") or str(point.get("name") or plant_id)
            plant_catalog[plant_id] = PlantCatalogEntry(
                plant_id=plant_id,
                display_name=display_name,
                type=(str(extra.get("type")) if extra.get("type") else None),
                cultivar=(str(extra.get("cultivar")) if extra.get("cultivar") else None),
                species=(str(extra.get("species")) if extra.get("species") else None),
                source=(str(extra.get("source")) if extra.get("source") else "farmbot"),
                metadata=dict(extra.get("metadata") or {}),
            )
            plant_catalog[plant_id].metadata.setdefault(
                "openfarm_slug",
                str(point.get("openfarm_slug") or slugify(display_name)),
            )

    plantings: list[Planting] = []
    for planting_id, points in grouped_points.items():
        points.sort(key=lambda item: int(_point_meta(item).get("gh_point_index", "0")))
        meta = _point_meta(points[0])
        bed_id = meta.get("gh_bed_id")
        bed = beds_by_id.get(bed_id or "")
        if not bed:
            continue
        plant_id = meta.get("gh_plant_id") or stable_plant_id(points[0].get("name") or "plant")
        quantity = int(meta.get("gh_quantity", len(points)))
        imported_cells = _cells_from_positions(points, bed)
        meta_cells = _parse_grid_cells(meta.get("gh_grid_cells", ""))
        if quantity == 1 and len(meta_cells) > len(imported_cells):
            grid_cells = meta_cells
        else:
            grid_cells = imported_cells
        plantings.append(
            Planting(
                planting_id=planting_id,
                bed_id=bed.bed_id,
                plant_id=plant_id,
                quantity=quantity,
                grid_cells=grid_cells,
                date_planted=points[0].get("planted_at"),
                status=_stage_to_status(points[0].get("plant_stage", ""), meta.get("gh_status", "planned")),
                notes=meta.get("gh_notes", ""),
                metadata={
                    "farmbot_point_count": len(points),
                },
            )
        )

    observations = [
        Observation.from_dict(item)
        for item in sidecar.get("observations") or []
    ]

    snapshot_metadata = SnapshotMetadata(
        snapshot_id=str(sync_metadata_raw.get("snapshot_id") or new_prefixed_id("snapshot")),
        exported_at=str(sync_metadata_raw.get("exported_at") or bundle.get("generated_at") or _utc_now()),
        source_app_version=str(sync_metadata_raw.get("source_app_version") or "garden-helper-farmbot-import"),
        metadata=dict(sync_metadata_raw.get("metadata") or {}),
    )

    plantings.sort(key=lambda planting: (planting.bed_id, planting.planting_id))
    ordered_catalog = sorted(plant_catalog.values(), key=lambda plant: plant.plant_id)
    beds.sort(key=lambda bed: bed.bed_id)
    obstacles.sort(key=lambda obstacle: obstacle.obstacle_id)

    return GardenSnapshot(
        garden=garden,
        beds=beds,
        obstacles=obstacles,
        plant_catalog=ordered_catalog,
        plantings=plantings,
        observations=observations,
        sync_metadata=snapshot_metadata,
    )
