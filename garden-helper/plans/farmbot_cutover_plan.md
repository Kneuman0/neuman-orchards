# FarmBot Garden Interface Plan

## Status

As of **April 26, 2026**, the FarmBot cutover is only **partially complete**.

Implemented today:

- canonical `garden_snapshot.json` schema remains the local garden interchange format
- local SQLite garden memory persists beds, obstacles, plant catalog, plantings, observations, and sync runs
- FarmBot bundle export/import exists
  - beds and obstacles map to FarmBot `PointGroup` zones
  - plantings map to FarmBot `Plant` points
  - sidecar metadata preserves exact IDs and canonical geometry
- CLI support exists for:
  - `init-db`
  - `import-snapshot`
  - `export-memory-context`
  - `export-farmbot-bundle`
  - `import-farmbot-bundle`
  - `prepare-farmbot-stack`
- obsolete `garden-planner` and VeggieTools code was removed

Not complete today:

- there is **not yet a real MCP garden server** exposing this state to agents as garden resources/tools
- there is **not yet live FarmBot API sync**
- there is **not yet a bidirectional "reason over FarmBot, then write back into FarmBot" workflow**
- there is **not yet a stable self-hosted FarmBot UI runtime on this Windows setup**
  - current evidence points to Docker Desktop + Windows bind-mounted filesystem issues during Rails boot

## Primary Objective

The objective is now explicit:

**FarmBot should become the precise visual interface through which we communicate about your garden.**

That means:

- you can create or edit beds, obstacles, and plant placements in FarmBot
- I can pull that exact spatial state into an MCP garden server
- I can reason over that state using the local ecological-agriculture specialist skills
- I can give advice tied to exact beds, positions, crops, and histories
- I can propose changes back into FarmBot as either:
  - a **draft/suggested plot** for you to review
  - an **approved direct change** to the active plot

The end state is:

- **FarmBot owns the spatial interface**
- **MCP owns persistent memory and agent access**
- **the local skill experts own agronomic reasoning**

## Communication Model

This is the interface model we are building toward:

1. You edit the garden visually in FarmBot.
2. The FarmBot layout is imported into the MCP garden server.
3. Agents read exact bed dimensions, positions, crop placements, and history from MCP resources/tools.
4. The local specialist skills analyze that precise state.
5. I return recommendations that reference exact beds and plantings.
6. I can produce a FarmBot-compatible draft layout or apply approved changes.
7. The resulting FarmBot layout is re-imported so MCP stays current.

This is the core requirement for precise garden collaboration.

## Current Architecture

### Current implemented pieces

- **Canonical schema**
  - `garden`
  - `beds`
  - `obstacles`
  - `plant_catalog`
  - `plantings`
  - `observations`
  - `sync_metadata`

- **Local persistence**
  - SQLite store in `garden-helper/data/garden-memory.db`
  - geometry sidecar tables for beds, obstacles, and plantings

- **FarmBot adapter**
  - export canonical snapshot or memory state to `garden-helper-farmbot-bundle/v1`
  - import FarmBot bundle back into canonical snapshot and memory

- **Runtime prep**
  - FarmBot repo checkout
  - `.env` generation
  - `docker compose config` validation

### Current missing pieces

- **MCP server layer**
  - the current project stores garden state locally, but it does not yet expose it as MCP resources/tools

- **FarmBot as live source**
  - the current import/export path is file/bundle based, not live API based

- **Agent write-back**
  - the current code can export a FarmBot bundle, but it does not yet create or update live FarmBot resources through the FarmBot API

- **Expert integration**
  - the current code does not yet route imported FarmBot context into the local ecological-agriculture orchestrator as an operational garden context

## Target Architecture

### 1. FarmBot is the spatial source of truth

FarmBot should be where beds and plant positions are drawn, moved, and reviewed.

Inbound data we need from FarmBot:

- map size
- bed rectangles / growing zones
- obstacle rectangles / exclusion zones
- plant points and their metadata
- optional FarmBot-native saved gardens or draft layouts, if available

### 2. MCP garden server is the agent-facing memory layer

We need a real MCP server in front of the current SQLite-backed garden memory.

That MCP server should expose at minimum:

- `garden://current`
  - latest imported garden state
- `garden://beds`
  - stable bed IDs, dimensions, positions, notes
- `garden://plantings`
  - exact planting locations, quantities, statuses
- `garden://observations`
  - plant and bed observations
- tools:
  - `import_from_farmbot(...)`
  - `export_to_farmbot(...)`
  - `create_farmbot_draft(...)`
  - `apply_farmbot_changes(...)`
  - `record_observation(...)`

### 3. Local skill experts reason over MCP state

For substantive garden advice, the local expert pack should use the imported FarmBot state as grounding.

The intended flow is:

- MCP garden server provides precise garden state
- the ecological-agriculture orchestrator reads that state
- relevant specialists are activated in parallel
- advice references exact bed IDs, sizes, and plantings

Examples:

- "Bed `bed-north-1` is 4 x 12 ft and already has tomatoes on the west half, so the expert recommendation is to keep the east edge for basil, onions, or a beneficial strip rather than another solanaceous crop."
- "Your carrot density in `bed-root-2` is above the imported spacing pattern, so damping-off and thinning pressure are likely to be higher."

### 4. Outbound changes must support two modes

We need both:

- **Draft mode**
  - create a suggested FarmBot layout for review
  - do not overwrite the active layout
  - tag draft resources clearly

- **Apply mode**
  - create/update FarmBot resources directly after approval
  - preserve stable IDs and sync history

## Clear Objectives

The next implementation phase should optimize for these objectives:

### Objective 1: precise inbound capture

If you draw beds in FarmBot, I must be able to import them into MCP without losing:

- bed names
- bed size
- bed position
- obstacle zones
- stable identifiers

### Objective 2: precise expert reasoning

If you ask for planning or troubleshooting, my answer must be grounded in the imported FarmBot layout, not generic assumptions.

### Objective 3: precise outbound proposals

If I suggest a planting plan, companion layout, succession plan, or bed revision, I must be able to render that suggestion back into FarmBot in a viewable form.

### Objective 4: precise approved edits

If you approve a change, I must be able to write that change back into FarmBot and then re-import the resulting state into MCP.

## Gaps To Close

### Gap 1: no MCP server yet

Current state:

- local SQLite and Python service exist
- no MCP server wrapper exists

Required:

- implement MCP resources and tools on top of the current `GardenTwinService`

### Gap 2: no live FarmBot API sync yet

Current state:

- bundle import/export exists
- no live read/write to FarmBot API exists

Required:

- add API-based importer/exporter once FarmBot runtime is stable
- keep bundle import/export as fallback and test fixture format

### Gap 3: no draft proposal model yet

Current state:

- export can create a FarmBot bundle
- no explicit "draft layout" model exists

Required:

- define how suggested layouts appear in FarmBot
- likely choices:
  - separate draft bundle files
  - tagged PointGroups / Plant points
  - FarmBot saved-garden equivalent if supported

### Gap 4: no expert-facing MCP garden context yet

Current state:

- specialists can reason from local literature
- they do not yet consume imported FarmBot geometry automatically

Required:

- create an orchestrator-facing context format derived from MCP garden state
- require expert answers to cite exact beds/plantings when relevant

### Gap 5: FarmBot runtime instability on Windows

Current state:

- Docker prep works
- Rails boot stalls when loading railties on Windows bind-mounted source

Required:

- move FarmBot runtime to a Linux-native filesystem in WSL2 or another Linux host
- validate first full FarmBot boot there before investing in live API sync work

## Revised Implementation Sequence

### Phase 1: stabilize FarmBot runtime

- run FarmBot from WSL2/Linux-native filesystem
- complete Rails boot
- complete DB setup and key generation
- verify web UI loads
- verify manual bed creation is possible

### Phase 2: build MCP garden server

- expose the current local garden memory through MCP resources/tools
- support import/export of FarmBot bundle files first
- keep stable IDs throughout

### Phase 3: implement inbound FarmBot -> MCP workflow

- define import operation from FarmBot-created beds and plantings
- store the resulting state in MCP-backed memory
- verify subsequent agent reads reflect exact FarmBot geometry

### Phase 4: connect local skill experts to imported garden context

- feed MCP garden state into the ecological-agriculture orchestrator
- require exact spatial references in planning/troubleshooting responses

### Phase 5: implement outbound MCP -> FarmBot proposals

- generate viewable FarmBot draft layouts
- allow agent-created suggestions to appear in FarmBot for review

### Phase 6: implement approved write-back

- allow direct changes to active FarmBot resources after approval
- re-import immediately after write-back

## Acceptance Tests

These are the tests that matter now.

### Test 1: FarmBot bed authoring -> MCP import

- I manually create one or more raised beds in FarmBot
- the importer pulls them into the MCP garden server
- the imported MCP state preserves:
  - bed IDs
  - bed names
  - bed dimensions
  - bed coordinates

Pass condition:

- asking for the current garden state returns those exact beds from MCP

### Test 2: FarmBot plant placement -> MCP import

- I place plants in FarmBot
- the importer maps them into stable plantings in MCP-backed memory

Pass condition:

- agent-visible garden state includes exact plant counts, positions, and statuses tied to the correct beds

### Test 3: expert reasoning on imported FarmBot geometry

- I ask a planning or troubleshooting question after FarmBot import
- the local ecological-agriculture orchestrator and specialists are used

Pass condition:

- the answer references exact beds and plantings from imported state
- the answer is materially different from a generic garden answer because it uses real geometry and crop state

### Test 4: draft layout generation back into FarmBot

- I ask for a new bed plan, succession plan, or revision
- the system generates a FarmBot-viewable draft layout

Pass condition:

- I can open FarmBot and inspect the suggested layout visually
- the suggestion is clearly separated from the current accepted layout

### Test 5: approved direct change into FarmBot

- I approve a suggested change
- the agent writes the change into FarmBot

Pass condition:

- the change appears in FarmBot
- the resulting FarmBot state can be re-imported into MCP with stable IDs preserved

### Test 6: closed-loop garden conversation

- I modify a bed in FarmBot
- the system imports it into MCP
- I ask for advice
- the specialists answer using imported state
- I request a revised layout
- the agent creates a FarmBot draft

Pass condition:

- FarmBot is the visual conversation surface
- MCP is the garden memory surface
- agent responses remain spatially precise end to end

## Immediate Next Step

The next highest-value step is:

**stop treating FarmBot as just a bundle target and make it a usable, stable interface first.**

Concretely:

- get FarmBot fully booting on WSL2/Linux-native storage
- confirm manual bed creation in the UI
- then implement the MCP server layer for inbound import of those FarmBot-authored beds

Until that happens, the current code is a strong adapter prototype, but not yet the precise FarmBot-centered garden conversation interface we actually want.
