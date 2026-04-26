---
name: garden-plot-excel-planner
description: Generate Excel garden-plot workbooks that map one or more beds as 2-inch planting cells, with separate sheets for beds or succession phases and a summary/legend sheet. Use when the user provides bed dimensions, planting plans, spacing, seasonal phases, or crop placements and wants a `.xlsx` file showing exactly where each plant goes.
---

# Garden Plot Excel Planner

## Overview

Use this skill to turn a garden layout into a deterministic Excel workbook instead of hand-formatting a spreadsheet. The workbook uses 2-inch square planting cells, color-coded crop blocks, short crop codes, and separate sheets for beds or seasonal phases.

Default output location in this workspace: `G:\My Drive\Home Docs\Garden\raised_beds`, unless the user explicitly asks for another folder.

## Workflow

1. Confirm the planning scope.
- Collect bed names and dimensions.
- Collect plant placements or enough spacing/timing rules to derive placements.
- Collect succession phases if the same bed changes over time.
- If any bed dimension is not divisible by 2 inches, clarify it or state the rounding rule before building the workbook.

2. Build a plot spec.
- Read [references/workbook-spec.md](references/workbook-spec.md).
- Represent each bed with `width_in` and `length_in`.
- Use 1-based cell coordinates from the top-left corner of each bed sheet.
- Use separate phase sheets when occupancy changes meaningfully across the year.
- Keep crop codes short, usually 2-4 characters.
- Prefer plant labels that fit cleanly inside a 2-inch square. Use `label` when the full crop name is too long for the grid.
- Keep placements non-overlapping inside each bed-phase.
- Default to `crop-zone occupancy` rather than isolated point-spacing diagrams. In other words, map the productive zone each crop actually claims in the bed.
- If spacing details matter, carry them in notes, comments, or the summary sheet rather than leaving wide unlabeled voids between isolated plants.
- Leave blank grid space only when it is intentional and explicitly labeled or explained as access, airflow, recovery, or reserved succession space.

3. Generate the workbook.
- Write the plot spec to a temporary JSON file.
- Run `scripts/generate_garden_plot_workbook.py --spec <spec.json> --output <workbook.xlsx>`.
- Use one workbook per request unless the user explicitly wants separate files.

4. Validate the output.
- Inspect the script's JSON summary on stdout.
- Verify the expected sheets exist.
- Verify each bed dimension became the right number of 2-inch cells.
- If succession was requested, verify each bed-phase got its own sheet.
- Reopen the workbook with `openpyxl` only if a deeper spot-check is needed.
- Visually sanity-check occupancy: if a raised bed looks strangely empty, revisit the spec before delivering it.

5. Respond with the workbook.
- Return the output workbook path.
- Summarize beds, phases, and major layout assumptions.
- Note any rounding, spacing, or unresolved placement assumptions.

## Workbook Rules

- Each plotted grid cell represents 2 in x 2 in.
- Bed sheets are generated per bed per phase.
- The summary sheet carries the legend, assumptions, and crop/code lookup.
- Keep print scale at 100% so the 2-inch cell sizing is preserved across pages.
- Treat larger plant footprints as multi-cell blocks.
- By default, use multi-cell blocks to show occupied crop zones, not just the physical footprint of an individual transplant.
- Each occupied square should show a plant label, usually the crop name or a shorter display label.
- If the user wants each plant shown individually, create separate placements for each plant instead of one aggregate block.

## Resources

### scripts/
- `scripts/generate_garden_plot_workbook.py`
  Build a workbook from a JSON plot spec. Use this instead of hand-formatting sheets.

### references/
- [references/workbook-spec.md](references/workbook-spec.md)
  Plot spec schema, workbook structure, and a compact example.
