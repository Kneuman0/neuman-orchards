# Topic Routing

Use this file first. It decides which domain experts to load or spawn.

## Knowledgebase Scope

Primary expert domains:

- `01_core_microfarm_permaculture`
- `02_intensive_vegetable_systems`
- `03_biochar`
- `04_bokashi_em`
- `05_compost_soil_fertility`
- `06_compost_tea_soil_biology`
- `07_fungi_mycorrhiza_biostimulants`
- `08_forest_gardens_agroforestry`
- `09_mid_atlantic_priority`
- `10_companion_planting_intercropping`
- `11_wild_plants_foraged_integration`
- `12_beneficial_insects_pest_indicators`

Support data only:

- `13_inventories_and_local_lists`

## Default Grounding

For most substantive ecological-agriculture questions, ground the orchestrator first in:

- `01_core_microfarm_permaculture`
- `Bec_Hellouin_summary.md`

Then route to the narrower experts.

This is especially important for:

- garden and farm planning
- yearly timelines
- succession-heavy designs
- any question that spans multiple practices or lifecycle stages

## First Routing Question

What is the decision the user is actually making?

- whole-system design or viability: route first to `01` and `02`
- annual bed layout, succession, turnover: route first to `02`
- climate fit or timing: always add `09`
- charcoal or carbon amendment decisions: add `03`
- bokashi, fermentation, EM, LAB: add `04`
- composting or baseline fertility: add `05`
- teas, drenches, inoculants, soil-food-web style claims: add `06`
- fungi, mycorrhizae, biostimulants, rhizosphere effects: add `07`
- perennial layers, food forests, alley cropping: add `08`
- plant combinations, trap crops, spatial mixing: add `10`
- edible weeds, foraged integration, wild-to-garden transfer: add `11`
- pests, beneficials, insectary plants, pest-as-signal questions: add `12`

## Routing By Capability

### Garden planning from image

Default pack:

- `01`
- `02`
- `09`
- `10`
- `12`
- support data from `13`

Common add-ons:

- `05`, `06`, `07`, `03`, `04` for soil-building-heavy plans
- `08` and `11` for perennial, wild, or edible-edge designs

### Direct questions

Use the smallest pack that still captures the mechanism. Do not stop at one topic if the answer depends on interactions.

### Interview / weekly timeline

Default pack:

- `01`
- `02`
- `09`
- `12`
- support data from `13`

Add other topics based on the current phase and the actual crops or systems under discussion.

## High-Value Expert Packs

### Soil building and fertility

- `05`
- `03`
- `04`
- `06`
- `07`
- `09`

### Pest diagnosis

- `12`
- `10`
- `05`
- `07`
- `09`

### Food forest or perennial polyculture

- `08`
- `11`
- `12`
- `10`
- `09`
- support data from `13`

### Ecological annual vegetable production

- `01`
- `02`
- `10`
- `12`
- `05`
- `09`
- support data from `13`

### System design or viability

- `01`
- `02`
- `09`

## Routing Guardrails

- Always add `09_mid_atlantic_priority` when timing, climate transferability, or feasibility matters.
- Always add support data from `13_inventories_and_local_lists` when the answer names plants, sequences crops, or builds a timeline.
- If the user asks about pests, do not answer only from `12` until you have checked whether `05`, `07`, or `10` materially changes the interpretation.
- If the user asks about forest gardens, do not answer only from `08` until you have checked `11` and `12`.
- If the user asks about companion planting, do not answer only from `10` until you have checked whether the real question is pest control, fertility transfer, or timing.
