# FarmBot Cutover Plan

## Decision

Switch the visual layer from the old `garden-planner` fork to a FarmBot-based workflow.

This cutover keeps the existing canonical snapshot schema and SQLite memory store, but changes the spatial interchange model to FarmBot resources:

- beds and rectangular areas become FarmBot `PointGroup` zones using `criteria.number_gt` / `criteria.number_lt`
- plantings become FarmBot `Plant` points with millimeter `x` / `y` coordinates
- geometry remains canonical in `garden_snapshot.json`
- observations remain in the local sidecar/memory layer unless explicitly mapped later

## Assumptions

- We are not rewriting or forking the FarmBot UI itself inside this pass.
- We will support FarmBot by:
  - exporting/importing FarmBot-compatible resource bundles
  - scaffolding a local FarmBot Web App runtime with Docker
  - removing the obsolete `garden-planner` fork and VeggieTools integration
- FarmBot zone geometry is sufficient for raised beds and obstacles because FarmBot renders rectangle areas from point-group numeric criteria.

## Implementation Shape

### 1. Canonical schema stays

The canonical local schema remains the system of record:

- `garden`
- `beds`
- `obstacles`
- `plant_catalog`
- `plantings`
- `observations`
- `sync_metadata`

No migration of the SQLite schema is required for this cutover.

### 2. Add a FarmBot adapter

Add Python conversion logic that can:

- export a canonical snapshot or memory export into a `farmbot_bundle.json`
- import a `farmbot_bundle.json` back into the canonical snapshot model

Bundle contents:

- `farmbot.web_app_config`
  - `map_size_x`
  - `map_size_y`
- `farmbot.point_groups`
  - bed zones
  - obstacle zones
- `farmbot.points`
  - `Plant` resources for plantings
- `garden_helper_sidecar`
  - observations
  - sync metadata

### 3. Bed mapping

Each bed exports to a FarmBot `PointGroup` zone:

- `criteria.number_gt.x = bed.x_mm`
- `criteria.number_gt.y = bed.y_mm`
- `criteria.number_lt.x = bed.x_mm + bed.w_mm`
- `criteria.number_lt.y = bed.y_mm + bed.h_mm`

Stable IDs are preserved in zone criteria string metadata:

- `gh_kind = bed`
- `gh_bed_id = <stable bed id>`
- `gh_bed_type = <raised|ground|...>`

### 4. Planting mapping

Each canonical planting exports into one or more FarmBot `Plant` points.

Rules:

- use millimeter coordinates
- preserve stable IDs in `meta`
- explode dense plantings into deterministic point grids inside each occupied cell
- keep `openfarm_slug` as a best-effort slugified crop identifier

Point metadata:

- `gh_kind = planting_point`
- `gh_bed_id`
- `gh_planting_id`
- `gh_plant_id`
- `gh_snapshot_id`

### 5. FarmBot local stack support

Add a local runtime helper that:

- clones or updates the official `FarmBot/Farmbot-Web-App`
- generates a `.env` file with local host/port and random secrets
- gives the user a clean path to `docker compose up`

Default runtime location:

- `garden-helper/runtime/farmbot-web-app`

### 6. Remove obsolete source

Remove:

- the old `planner/` tree based on `mvrieperry/garden-planner`
- VeggieTools-specific enrichment code
- tests and docs that only exist for the removed planner/integration

## CLI changes

Add:

- `export-farmbot-bundle`
- `import-farmbot-bundle`
- `prepare-farmbot-stack`

Keep:

- `init-db`
- `import-snapshot`
- `export-memory-context`

Remove:

- `lookup-plant`

## Verification

Minimum smoke checks for this cutover:

- canonical snapshot import still passes
- memory export still works
- FarmBot bundle export produces:
  - map size in mm
  - bed zones
  - plant points
- FarmBot bundle import reconstructs:
  - stable bed IDs
  - stable planting IDs
  - quantities and occupied cells
- local FarmBot stack prep writes a valid `.env`
- `docker compose config` succeeds in the prepared FarmBot runtime

## Known limits after this pass

- observations are preserved in sidecar data, not rendered in FarmBot
- FarmBot does not natively model “beds” as first-class records; zones are the closest fit
- full self-hosted FarmBot launch may still depend on Docker host/path behavior on this machine
