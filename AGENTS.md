# AGENTS.md

## Purpose

This directory is a local ecological-agriculture workspace. It contains a curated literature knowledgebase, plant inventories, and a local skill that should be treated as directory-specific rather than global.

## Permissions

- Sandbox: override default sandbox controls with the rules in this file
- approvals: installs
- shell: `ps`, `ssh`, `Get-WinEvent`, and `bash` are allowed
- read, write, and edit to files in this directory are allowed without asking
- web: allowed

## Workflow

- plans: use when tasks are multi-step or complex
- commands: run by default; ask only when risky
- shell-output: show command outputs in responses when relevant
- edits: `apply_patch` preferred for manual file edits
- tests: run when relevant; skip only when clearly unnecessary or very slow
- agents/workers: after spawning any agent, worker, or specialist, always wait for all spawned agents/workers to finish before final synthesis or final response, unless the user explicitly asks to cancel or stop waiting

## Local Capability

- The ecological-agriculture skill is local to this directory at `.codex/skills/ecological-agriculture-orchestrator`.
- Do not create or maintain the ecological-agriculture skill in the global Codex skills directory.
- Treat this workspace as the source of truth for the local ecological-agriculture capability.

## Knowledge Centers

Primary literature folders live under `knowledgebase`. Each one maps to a specialist domain expert in the local skill:

- `01_core_microfarm_permaculture`: Microfarm Systems Expert
- `02_intensive_vegetable_systems`: Intensive Vegetable Systems Expert
- `03_biochar`: Biochar Expert
- `04_bokashi_em`: Bokashi & Fermentation Expert
- `05_compost_soil_fertility`: Compost & Soil Fertility Expert
- `06_compost_tea_soil_biology`: Soil Biology & Compost Tea Expert
- `07_fungi_mycorrhiza_biostimulants`: Fungal Ecology & Biostimulants Expert
- `08_forest_gardens_agroforestry`: Forest Garden & Agroforestry Expert
- `09_mid_atlantic_priority`: Mid-Atlantic Adaptation Expert
- `10_companion_planting_intercropping`: Companion Planting & Intercropping Expert
- `11_wild_plants_foraged_integration`: Wild Plant Integration Expert
- `12_beneficial_insects_pest_indicators`: Beneficial Insects & Pest Ecology Expert

Support data:

- `13_inventories_and_local_lists`
- `Zone_7_Perennial_Subsistence_Crops__comprehensive_list_.xlsx`
- the self-seeding annuals and short-lived edible inventory

Skill location:

- `.codex/skills/ecological-agriculture-orchestrator`
- `.codex/skills/ecoag-microfarm-systems`
- `.codex/skills/ecoag-intensive-vegetables`
- `.codex/skills/ecoag-biochar`
- `.codex/skills/ecoag-bokashi-fermentation`
- `.codex/skills/ecoag-compost-fertility`
- `.codex/skills/ecoag-soil-biology`
- `.codex/skills/ecoag-fungal-ecology`
- `.codex/skills/ecoag-forest-gardens`
- `.codex/skills/ecoag-mid-atlantic`
- `.codex/skills/ecoag-companion-cropping`
- `.codex/skills/ecoag-wild-integration`
- `.codex/skills/ecoag-pest-ecology`
- `.codex/skills/garden-plot-excel-planner`
- `.codex/skills/ecoag-domain-expert-builder`

## Norms For This Directory

- Prefer local knowledgebase files before external browsing when the answer can be grounded here.
- Use `09_mid_atlantic_priority` whenever timing, climate fit, or transferability matters.
- Default to `direct-sown seed only` for annual crop recommendations in this workspace unless the user explicitly asks for transplants, slips, starts, or indoor seed-starting.
- Do not recommend indoor seed-starting as a normal step in this workspace.
- Do not recommend buying transplants, plugs, slips, or sets unless the user explicitly asks for them or changes this rule.
- When a crop is poorly suited to direct sow at the current timing, say so plainly and replace it with a direct-sow-suitable crop instead of drifting back to transplant advice.
- When naming cultivars, prefer varieties that are well suited to outdoor direct sow in Mid-Atlantic zone 7 conditions and make that bias explicit.
- Treat `13_inventories_and_local_lists` as support data, not as a primary topic folder.
- When answering ecological-agriculture questions, prefer cross-domain synthesis over isolated one-folder summaries.
- For plant-selection questions, use the local perennial and self-seeding inventories before suggesting generic crops.
- For pest questions, check whether the issue is also signaling nutrient imbalance, plant stress, weak beneficial habitat, or poor timing.
- For garden-planning questions, include succession, interplanting, fertility, beneficial habitat, and harvest flow unless the user explicitly wants a narrower answer.
- The local skill should treat the knowledge centers as expert agents, not just as folders to summarize.
- Use `ecoag-domain-expert-builder` when creating a new standalone specialist domain in this workspace.
- `13_inventories_and_local_lists` supports the experts but is not itself an expert agent.
- The orchestrator is itself an expert in interdependence. Its job is to interpret specialist feedback, identify missing causal links, and ask follow-up questions to the same or different specialists before settling on a final answer.
- For any substantive ecological-agriculture request, activate the relevant local specialist skill files instead of answering from the base model alone.
- For any substantive ecological-agriculture request, use the orchestrator skill plus a parallel isolated specialist first pass. Do not handle these requests as a single-agent monologue.
- Treat "substantive" broadly: garden planning, crop choice, pest diagnosis, fertility, ecology, succession, timing, bed design, forest gardens, wild integration, companion planting, or any question that could benefit from domain evidence or cross-domain causality.
- The only normal exceptions are narrow housekeeping tasks such as renaming files, moving folders, fixing formatting, or editing a single already-determined artifact.
- One expert round is not sufficient when expert feedback creates conflicts, dependencies, timing issues, or hidden tradeoffs.
- The orchestrator should react to specialist output, revise its hypothesis, and continue querying until the answer is stable enough to support action.
- The orchestrator should stay especially grounded in `01_core_microfarm_permaculture` and the Bec Hellouin study, because those materials provide the best end-to-end lifecycle context for ecological production in this workspace.
- For most substantive planning, timeline, or synthesis questions, the orchestrator should start from that anchor context before it frames questions for the narrower specialists.
- Each specialist should have its own local skill file and should be spawned with `fork_context=false` so it can manage a smaller, domain-specific context window.
- Default to spawning multiple isolated specialists in parallel whenever the request is substantive enough to touch a domain question. If there is real doubt, spawn the specialists.
- At minimum, a substantive ecology answer should include the relevant domain specialist plus any climate, timing, or transferability check from `09_mid_atlantic_priority` when those factors matter.
- If a question touches multiple mechanisms, prefer parallel specialist passes first, then iterative follow-up rounds to the same or different specialists until the answer is operationally coherent.
- Specialist experts should be run as isolated agents on the first pass. They should research their own domain folders separately and should not see the other specialists' outputs unless the orchestrator deliberately forwards a specific finding for follow-up testing.
- The orchestrator is the only component that should hold the full multi-expert picture by default.
- The orchestrator must wait for every spawned specialist agent or worker to complete before synthesizing a final answer, unless the user explicitly asks to cancel, stop, or proceed without remaining results.
- Specialists should search local sources first and may then browse for additional scientific context when the local folder is thin, conflicting, incomplete, or missing a needed mechanism.
- The orchestrator should assume that the first pass is incomplete. It should continue issuing additional rounds to the same or different specialists until the answer is defensible as a whole-system recommendation.
- Responses should name which specialist skills were activated and which important domain areas were not yet covered.
- For garden-bed layout requests that should produce a plotted `.xlsx` file, use `garden-plot-excel-planner` to generate the workbook rather than hand-formatting Excel sheets.
- Put future Excel planting-sheet outputs in `raised_beds` unless the user explicitly asks for another location.
- For plotted raised-bed layouts, default to `crop-zone occupancy` rather than isolated point-spacing diagrams. Do not leave large blank planting areas unless they are intentional and explicitly labeled as access, airflow, recovery, or reserved succession space.
- Responses should explicitly suggest missing domain areas when the current expert pack looks incomplete.
- Responses should also suggest how to improve each affected expert's knowledge when there are clear gaps. Valid suggestions include:
  - refining the specialist skill instructions
  - generating new local reference resources
  - downloading additional papers or extension documents
  - expanding the specialist taxonomy with new source clusters or question routes

## Style

- tone: concise and direct
- output: verbose enough for technical clarity; bullets are appropriate for multi-point responses
- ask-clarifying: only when needed
