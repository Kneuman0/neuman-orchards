# Open-Source Garden Planning Tool Research

Research date: 2026-04-25

## Objective

Find open-source or open-data tools that could represent a garden more richly than spreadsheets, especially so Codex can:

- understand what is growing where
- reason about spatial relationships between plants
- analyze bed configuration, spacing, crop families, succession, pest habitat, fertility demand, and shade
- propose and render layout changes
- support follow-up questions about why a design choice was made

## Short Conclusion

There is no perfect open-source "garden planner plus AI design partner" yet. The best path is probably one of these:

1. Use or fork **Jninty** if you want a garden-specific app with plant records, scheduling, and a visual garden map.
2. Use **QGIS/QField** if you want the strongest spatial truth model.
3. Build a lightweight local garden twin using **GeoJSON** plus a Leaflet/Konva web UI if the main goal is a Codex-readable/editable garden interface.

For AI-assisted analysis, the most important piece is not the UI. It is the underlying data model. A clean GeoJSON/GeoPackage representation would let Codex analyze and render proposed changes much more reliably than Excel.

## Best Candidates

| Tool | Fit | Why It Matters | Caveats |
|---|---:|---|---|
| [Jninty](https://github.com/HapiCreative/jninty) | High | Local-first open-source garden management PWA. Includes plant inventory, journal, schedules, seed bank, task rules, expenses, and a visual garden map. Uses React/TypeScript, PouchDB/IndexedDB, optional CouchDB sync, and Konva for the garden map. | Young project with low GitHub stars at research time. Need inspect export format and map data model before adopting. |
| [QGIS](https://github.com/qgis/QGIS) + [QField](https://github.com/opengisch/QField) | Very high | Best spatial foundation. Beds can be polygons; plants can be points/circles; paths, trellises, irrigation, shade, pests, soil tests, and observations can be layers. QField allows mobile/offline field editing. | Less garden-friendly UI. More GIS than gardening app. Needs a garden-specific schema and styling. |
| [MyPermaGarden](https://www.mypermagarden.app/en) | Medium-high | Permaculture-oriented app built around QGIS/QField. Claims association advice, planned zones, crop rotations, collaboration, offline/mobile workflow, and regional data export. Source: [GitLab project](https://gitlab.com/mypermagarden/mypermagarden-qgis). | License language includes a non-commercial clause despite GPL/open-source language, so it may not be clean OSI-style open source. Needs maturity check. |
| [FarmBot Web App](https://github.com/FarmBot/Farmbot-Web-App) | Medium-high | Strong garden map model: drag/drop plants on X/Y bed map, row/grid planting, plant spread visualization, overlap feedback, saved gardens, REST JSON API. | Tied to FarmBot robot concepts and device control. Likely too heavy unless automation is interesting later. |
| [GoGrow](https://github.com/DaytimeLobster/gogrow) | Medium | Self-hosted homestead planning and image annotation app using Leaflet. Good for annotating overhead photos/maps. | In maintenance mode as of 2026. Less plant-aware and less suitable as the main garden data model. |
| [HortusFox](https://github.com/danielbrendel/hortusfox-web) | Medium-low | Self-hosted collaborative plant management with locations, photos, tasks, calendar, history, REST API, weather, inventory. | Better for plant care records than precise spatial bed layout. |
| [Growstuff](https://github.com/Growstuff/growstuff) | Low-medium | Open-source/open-data food gardening platform with planting/harvest records and API. | Not primarily a spatial planner. |
| [OpenFarm](https://github.com/openfarmcc/OpenFarm) | Data source / legacy | Public-domain growing-guide data historically used by FarmBot, including spacing, companions, water, sun/shade, etc. | Project appears legacy/inactive; useful for data inspiration more than a current app. |
| [Permapeople](https://permapeople.org/knowledgebase/api-docs.html) | Data source | Regenerative/permaculture plant database API, CC BY-SA 4.0, with plant profiles and public garden plans. | Data license requires attribution/share-alike; commercial access not free. Planner code availability is unclear. |

## Notes From Sources

- Jninty describes itself as a local-first open-source PWA where data lives in IndexedDB with optional CouchDB sync. It includes plant inventory, journal, growing guides, planting calendar, seed bank, and a visual garden bed layout editor.
- QGIS is mature free/open-source GIS under GPL. QField is a mobile, touch-optimized QGIS field interface that works offline and can sync field changes back to QGIS.
- MyPermaGarden is built from QGIS and QField and is aimed directly at permaculture garden design, association advice, zones, crop rotations, and shared garden management.
- FarmBot's software docs describe a farm designer where plants are placed on a map, moved by X/Y coordinates, added in rows/grids, grouped, and visualized with spread overlap feedback.
- GoGrow is a self-hosted homestead management and image annotation app using Leaflet, but the repository says it is in maintenance mode.
- Growstuff is open-source/open-data and has useful planting/harvest records, but not the spatial layout interface needed here.
- OpenFarm remains useful as a structured plant-growing knowledge source, though the maintainers describe the project as not having reached sustainable traction.
- Permapeople offers an API for plant data under CC BY-SA 4.0 and has public garden plans, but its role is better as plant data than as the main spatial editor.

## Recommended Architecture For This Workspace

Use a garden data model that can survive across tools:

```text
garden/
  beds.geojson
  plantings.geojson
  infrastructure.geojson
  observations.geojson
  seasons/
    2026-spring.geojson
    2026-summer.geojson
  renders/
    current-layout.png
    proposed-layout.png
```

### Core Layers

**beds**

- geometry: polygon
- fields: `bed_id`, `name`, `length_ft`, `width_ft`, `soil_notes`, `mulch`, `sun`, `irrigation`, `last_amended`, `constraints`

**plantings**

- geometry: point or polygon
- fields: `planting_id`, `bed_id`, `crop`, `cultivar`, `family`, `date_sown`, `date_expected_done`, `status`, `spacing_in`, `spread_in`, `height_in`, `fertility_demand`, `water_demand`, `notes`

**infrastructure**

- geometry: line/polygon/point
- fields: `type`, `name`, `height`, `material`, `seasonal`, `notes`
- examples: trellis, path, fence, water line, shade source, compost, insectary strip

**observations**

- geometry: point/polygon
- fields: `date`, `type`, `severity`, `crop`, `description`, `photo`, `action_taken`
- examples: slug damage, damping-off, nutrient deficiency, harvest, soil test location

### Why GeoJSON/GeoPackage Beats Excel

- It preserves actual geometry, not just cells.
- It lets Codex calculate distance, adjacency, overlap, rows, paths, edge effects, and bed occupancy.
- It can be rendered into maps automatically.
- It can round-trip through QGIS, QField, Leaflet, Python, and web apps.
- It supports future time layers for succession planting.

## Practical Recommendation

### Option A: Fastest Garden-App Trial

Try Jninty first.

Why:

- It is garden-specific.
- It is local-first.
- It has export/import.
- It has a visual garden map.
- It is modern React/TypeScript and probably forkable.

Research task before adopting:

- Inspect its internal map data model.
- Test whether the export includes bed geometry and plant coordinates in a readable format.
- See whether a Codex script can parse the backup ZIP into a garden-analysis JSON.

### Option B: Strongest Long-Term Garden Twin

Use QGIS/QField with a simple custom schema.

Why:

- Best spatial accuracy.
- Works with standard formats.
- Allows mobile field updates.
- Lets Codex consume and generate GeoJSON directly.

Downside:

- More setup.
- Less friendly than a purpose-built garden app.

### Option C: Best Codex-Native Interface

Build a small local app for this workspace:

- Leaflet or Konva canvas for editing
- GeoJSON as source of truth
- plant palette from local inventories
- import/export to QGIS
- render current and proposed plans
- Codex can read the same JSON and write proposed changes

This may become the best interface because it can be shaped around the actual workflow:

- "What is wrong with this bed?"
- "Where should I move these crops?"
- "Render a better version."
- "Why did you put that there?"
- "What changes if I add mulch, trellis, or a fall cover crop?"

## Evaluation Criteria For Any Candidate

Before adopting a tool, check:

- Can it export the full garden plan in a machine-readable format?
- Does it store plant coordinates, spacing, and bed geometry?
- Can it represent individual plants and grouped plantings?
- Can it track time/succession, not just a static layout?
- Can it store observations, photos, pest notes, and soil test data?
- Can Codex modify the data and render a proposed layout back?
- Is the license actually open enough for local customization?
- Is the project active enough to trust?

## Current Ranking

1. **Custom GeoJSON garden twin**: best fit to the Codex feedback loop.
2. **QGIS/QField**: best durable spatial foundation.
3. **Jninty**: best ready-made garden app to inspect or fork.
4. **FarmBot Web App**: best inspiration for coordinate-based plant layout, but probably overbuilt.
5. **MyPermaGarden**: interesting QGIS-based permaculture app, but license/maturity need checking.
6. **GoGrow / HortusFox / Growstuff**: useful side tools, not the main planning substrate.

## Next Research Steps

- Clone and inspect Jninty's data schema and map export.
- Create a minimal `garden_schema.md` for this workspace.
- Create sample `beds.geojson` and `plantings.geojson` for the existing raised beds.
- Test rendering a proposed layout from GeoJSON to PNG/SVG.
- Decide whether the UI should be QGIS/QField-first or a small local web app.

