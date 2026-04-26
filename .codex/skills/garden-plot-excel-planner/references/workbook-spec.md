# Workbook Spec

Use this reference when preparing the JSON input for `scripts/generate_garden_plot_workbook.py`.

## Purpose

- Generate one `.xlsx` workbook per request.
- Represent each bed as a grid of 2-inch cells.
- Create one sheet per bed-phase when succession matters.
- Keep the workbook printable at 100% scale so each plotted cell remains 2 inches square.
- Default to showing `crop-zone occupancy` rather than sparse point-spacing diagrams unless the user explicitly wants the latter.

## Top-Level Keys

```json
{
  "title": "Zone 7 Spring Layout",
  "assumptions": [
    "Each cell represents 2 in x 2 in.",
    "Plant footprints were rounded up to whole cells."
  ],
  "cell_size_inches": 2,
  "beds": []
}
```

- `title`: Optional workbook title.
- `assumptions`: Optional list shown on the summary sheet.
- `cell_size_inches`: Must be `2`.
- `beds`: Required list of bed objects.

## Bed Object

```json
{
  "name": "Bed A",
  "width_in": 48,
  "length_in": 96,
  "notes": "North bed by the fence.",
  "phases": []
}
```

- `name`: Required bed name.
- `width_in`: Required physical bed width in inches.
- `length_in`: Required physical bed length in inches.
- `notes`: Optional bed note.
- `phases`: Optional list of phase objects.

If a bed does not need succession phases, you may omit `phases` and instead provide:

```json
{
  "name": "Bed A",
  "width_in": 48,
  "length_in": 96,
  "phase_name": "Current Layout",
  "placements": []
}
```

## Phase Object

```json
{
  "name": "Late Winter / Early Spring",
  "notes": "Direct-seeded cold-hardy crops.",
  "placements": []
}
```

- `name`: Required phase name.
- `notes`: Optional phase note.
- `placements`: Required list of placement objects.

Default interpretation:

- A placement usually represents the productive zone claimed by that crop in the bed.
- Do not use placements only as isolated plant-center markers if that leaves large unexplained blank areas.
- If exact plant count or spacing matters, put that detail in `notes` while keeping the bed visually representative of actual bed occupancy.

## Placement Object

```json
{
  "crop": "Spinach",
  "label": "Spinach",
  "code": "SPN",
  "x": 1,
  "y": 1,
  "w": 2,
  "h": 2,
  "color": "#A9D18E",
  "variety": "Bloomsdale",
  "notes": "Direct-seeded block."
}
```

- `crop`: Required crop name.
- `label`: Optional display label shown in each occupied grid square. Defaults to `crop`.
- `code`: Optional short label. Auto-generated if omitted.
- `x`: Required 1-based column position in 2-inch cells.
- `y`: Required 1-based row position in 2-inch cells.
- `w`: Optional width in cells. Defaults to `1`.
- `h`: Optional height in cells. Defaults to `1`.
- `color`: Optional hex fill color. Auto-assigned if omitted.
- `variety`: Optional variety or cultivar note.
- `notes`: Optional placement note.

Recommended use of `notes`:

- actual plant count
- in-row spacing
- whether the block is a full crop zone, one side of a trellis, or a reserved succession zone

## Coordinate Rules

- Coordinates are 1-based.
- `x=1`, `y=1` is the top-left plotted cell of the bed.
- A 48-inch-wide bed becomes `24` plotted columns.
- A 96-inch-long bed becomes `48` plotted rows.
- Dimensions and placements should resolve to whole 2-inch cells.

## Output Structure

- `Summary` sheet:
  - workbook title
  - assumptions
  - bed dimension table
  - crop legend with codes and colors
- One bed sheet per phase:
  - top metadata rows
  - 2-inch grid with row and column scale markers
  - color-coded crop blocks
  - crop code centered in each placement block

Occupancy rule:

- Large blank planting areas should be avoided unless they are intentionally left open and explained in the assumptions, bed notes, phase notes, or placement notes.

## Example

```json
{
  "title": "Sample Layout",
  "assumptions": [
    "Each cell is 2 in x 2 in.",
    "Blocks represent planned plant footprints, not exact root spread."
  ],
  "cell_size_inches": 2,
  "beds": [
    {
      "name": "Bed 1",
      "width_in": 48,
      "length_in": 96,
      "phases": [
        {
          "name": "Spring",
          "placements": [
            {"crop": "Spinach", "code": "SPN", "x": 1, "y": 1, "w": 3, "h": 4},
            {"crop": "Radish", "label": "Radish", "code": "RAD", "x": 4, "y": 1, "w": 2, "h": 4},
            {"crop": "Scallion", "label": "Scallion", "code": "SCA", "x": 6, "y": 1, "w": 2, "h": 4}
          ]
        },
        {
          "name": "Summer",
          "placements": [
            {"crop": "Bush Bean", "label": "Bush Bean", "code": "BEB", "x": 1, "y": 1, "w": 6, "h": 6},
            {"crop": "Basil", "label": "Basil", "code": "BAS", "x": 7, "y": 1, "w": 2, "h": 3}
          ]
        }
      ]
    }
  ]
}
```
