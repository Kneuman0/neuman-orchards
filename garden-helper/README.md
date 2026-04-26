# Garden Helper

Local prototype for a FarmBot-oriented garden digital twin:

- canonical `garden_snapshot.json` schema
- xardin-compatible SQLite memory with geometry sidecar tables
- snapshot sync adapter
- FarmBot bundle export/import
- local FarmBot Web App runtime prep helper

## Quick Start

```powershell
cd "G:\My Drive\Home Docs\Garden\garden-helper"
python -m pip install -e .
python -m garden_helper init-db
python -m garden_helper import-snapshot .\examples\example_garden_snapshot.json
python -m garden_helper export-memory-context
python -m garden_helper export-farmbot-bundle --out .\examples\example_farmbot_bundle.json
python -m garden_helper prepare-farmbot-stack
```

Default SQLite database path:

- [data/garden-memory.db](/G:/My%20Drive/Home%20Docs/Garden/garden-helper/data/garden-memory.db)

Default FarmBot runtime path:

- [runtime/farmbot-web-app](/G:/My%20Drive/Home%20Docs/Garden/garden-helper/runtime/farmbot-web-app)

## FarmBot Workflow

The visual layer now targets the official FarmBot Web App instead of the retired square-foot planner fork.

Key commands:

- `import-snapshot`: upsert a canonical garden snapshot into the local SQLite memory store
- `export-memory-context`: export the current persistent garden state plus a canonical snapshot view
- `export-farmbot-bundle`: convert a canonical snapshot or current memory state into FarmBot-compatible resources
- `import-farmbot-bundle`: convert a FarmBot bundle back into the canonical snapshot/memory model
- `prepare-farmbot-stack`: clone or update FarmBot Web App and write a local `.env`

The FarmBot bundle encodes:

- `farmbot.web_app_config` for map size
- `farmbot.point_groups` for beds and obstacles
- `farmbot.points` for plantings
- `garden_helper_sidecar` for exact canonical geometry, observations, and sync metadata

## Structure

- [schemas/garden_snapshot.schema.json](/G:/My%20Drive/Home%20Docs/Garden/garden-helper/schemas/garden_snapshot.schema.json)
- [src/garden_helper](/G:/My%20Drive/Home%20Docs/Garden/garden-helper/src/garden_helper)
- [examples](/G:/My%20Drive/Home%20Docs/Garden/garden-helper/examples)
- [plans/farmbot_cutover_plan.md](/G:/My%20Drive/Home%20Docs/Garden/garden-helper/plans/farmbot_cutover_plan.md)
- [tests](/G:/My%20Drive/Home%20Docs/Garden/garden-helper/tests)
