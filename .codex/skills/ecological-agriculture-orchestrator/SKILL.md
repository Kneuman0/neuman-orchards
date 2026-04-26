---
name: ecological-agriculture-orchestrator
description: Use this skill when the user wants ecological agriculture guidance that must connect multiple domain experts grounded in the local knowledgebase, especially garden design from images, succession and interplanting plans, cross-domain agronomy questions, pest diagnosis, soil-building strategy, forest-garden design, or season-by-season checklists and timelines.
---

# Ecological Agriculture Orchestrator

## Overview

This skill orchestrates the domain experts grounded in the topic folders under `G:\My Drive\Home Docs\Garden\knowledgebase` and treats them as a coordinated ecology stack rather than isolated subjects. The orchestrator itself is responsible for understanding the meaningful interdependence between the specialists, not just routing between them, and it must stay especially grounded in `01_core_microfarm_permaculture` and the Bec Hellouin study because those materials provide the best end-to-end lifecycle context in this workspace.

Treat `13_inventories_and_local_lists` as support data, not a primary expert agent. Use it for plant lists, zone-7 filtering, self-seeding annuals, and weekly scheduling.

This is not a monolith skill. For substantive ecological-agriculture work, the orchestrator must activate relevant specialist skills and run isolated specialist agents in parallel by default. Do not answer these requests from the orchestrator alone unless the task is plainly administrative and does not require domain judgment.

Workspace default for annual crop planning: assume the user is working from `direct-sown outdoor seed only` unless the user explicitly opts into transplants, slips, sets, plugs, or indoor seed-starting. If a crop does not fit that constraint, replace it with a direct-sow-suitable alternative rather than quietly reverting to transplant logic.

## Core Capabilities

### 1. Garden Planning From Images and Scale

Use this when the user provides a garden image, sketch, or photo plus dimensions or another reliable scale reference. The output should combine:

- physical layout
- crop placement
- succession planting
- interplanting and companion logic
- pest and beneficial habitat design
- soil-building actions
- weekly operating timeline

Read [references/garden-planning-workflow.md](references/garden-planning-workflow.md) before answering.

### 2. Cross-Domain Question Answering

Use this when the user asks a direct question and wants the best answer across the knowledgebase, especially where multiple mechanisms interact. Examples:

- pest pressure that may reflect fertility, stress, or habitat imbalance
- whether a soil amendment changes disease pressure, crop vigor, or succession timing
- how wild edible plants, forest gardens, and annual beds should be combined
- whether a practice is worth it in the Mid-Atlantic rather than in generic conditions

Read [references/direct-qa-workflow.md](references/direct-qa-workflow.md) before answering.

### 3. Interview / Weekly Timeline Mode

Use this when the user wants to be kept on track through the year. In this mode, the skill should:

- establish the garden context
- build a 52-week operating timeline
- ask phase-appropriate questions
- identify missing actions, timing conflicts, or weak spots

Read [references/interview-timeline-workflow.md](references/interview-timeline-workflow.md) before answering.

## Orchestration Rules

1. Start by reading [references/orchestrator-grounding.md](references/orchestrator-grounding.md).
2. Then read [references/topic-routing.md](references/topic-routing.md).
3. Then read [references/domain-expert-registry.md](references/domain-expert-registry.md).
4. Then read [references/interconnections.md](references/interconnections.md).
5. Then read [references/specialist-skill-map.md](references/specialist-skill-map.md).
6. Load only the domain-expert cards and specialist skills that are relevant for the current question.
7. Use `scripts/query_knowledgebase.py` to shortlist papers, notes, and inventory files before opening many documents manually.
8. Use `09_mid_atlantic_priority` whenever climate, timing, management feasibility, or transferability matters.
9. Use `13_inventories_and_local_lists` whenever the answer requires plant selection, succession planning, weekly timelines, or zone-7 filtering.
10. For any substantive ecology request, activate the relevant specialist skill files and spawn the corresponding isolated specialist agents in parallel unless the task is plainly administrative.
11. After the first round of specialist answers, explicitly evaluate interdependencies, conflicts, and missing mechanisms before final synthesis.
12. Continue asking follow-up questions to the same experts or additional experts until the orchestrator is satisfied that the answer is grounded, causally coherent, and operationally usable.
13. For annual crop recommendations in this workspace, filter for direct-sow feasibility and favor cultivars suited to outdoor direct sow under Mid-Atlantic zone 7 timing.

## Domain-Expert Model

This skill is explicitly agent-orchestrated. For any substantive ecological-agriculture request, spawn isolated specialist agents instead of keeping the work inside one context window. When the request is meaningfully cross-domain, spawn one `explorer` agent per relevant domain expert and keep that agent's read scope narrow:

- the user's current question
- the corresponding specialist skill from `references/specialist-skill-map.md`
- the corresponding expert card in `references/domain-experts/` if the specialist needs the brief as an extra reference
- the matching knowledgebase folder path
- inventory support files only if the domain needs them

Runtime rule: use `spawn_agent` with `fork_context=false` so each specialist manages its own context window for its own job.

Mandatory default:

- If the user is asking a real domain question, activate specialist skills.
- If the answer depends on evidence, mechanisms, timing, ecology, or management tradeoffs, run parallel isolated specialists first.
- If there is doubt about whether the question is cross-domain, treat it as cross-domain and run the specialists.
- The only routine reason to skip specialist spawning is that the task is administrative and does not require substantive domain judgment.

These specialist agents should be isolated from one another by default. On the first pass, do not give one specialist the outputs, conclusions, or notes from the other specialists.

Each expert agent should return:

- the strongest evidence-based answer from its folder
- the mechanism behind that answer
- constraints or caveats
- what other domain experts it should connect to
- the specific files it relied on

Do not delegate final synthesis. The main agent integrates the expert outputs, interrogates interdependencies, and continues expert questioning until it is satisfied that the answer is ready.

## Isolation Requirement

Each specialist expert should be able to spin up, receive a question, and conduct its own research separately from the others.

### First-pass isolation

For the first volley, each specialist should receive only:

- the user question
- the orchestrator's scoped sub-question for that expert
- its own specialist skill
- its own domain-expert card only if needed as a local brief
- its own knowledgebase folder path
- any support inventory files that are strictly necessary for that expert

Do not give the specialist:

- other experts' answers
- the orchestrator's draft conclusion
- other experts' file lists
- cross-expert synthesis notes

### Controlled follow-up

After the isolated first pass, the orchestrator may send a follow-up to the same expert or a different expert. Those follow-ups may include selected findings from other experts, but only when that sharing is necessary to test a dependency, resolve a conflict, or pressure-test a mechanism.

### Information-flow rule

The orchestrator is the only component that should see the full multi-expert picture by default.

## Interdependence Loop

The orchestrator must not stop after one round of expert answers when the recommendation depends on interactions.

The normal operating mode is multi-round: parallel isolated specialists first, then as many targeted follow-up rounds as needed to make the answer whole-system coherent.

### Grounding Pass

Before broad specialist synthesis, the orchestrator should ground itself in:

- `references/domain-experts/01-core-microfarm-permaculture.md`
- `G:\My Drive\Home Docs\Garden\knowledgebase\Bec_Hellouin_summary.md`
- when needed, the anchor files in `G:\My Drive\Home Docs\Garden\knowledgebase\01_core_microfarm_permaculture`

This grounding pass should shape the orchestrator's first hypothesis about system lifecycle, labor realism, ecological maturity, intensification, succession, and whole-farm dependencies before it questions the other specialists.

### Round 1

- Ask each relevant expert for its domain answer, mechanism, caveats, and handoffs.
- Run the relevant specialists in parallel, not serially, unless there is a hard dependency that prevents it.

### Interdependence Review

After Round 1, the orchestrator must ask:

- Which expert claims materially change another expert's recommendation?
- Which answers depend on assumptions that another expert has not yet tested?
- Where do timing, fertility, pest ecology, canopy structure, labor, or climate adaptation create hidden constraints?
- Which missing variable would most likely change the answer?

### Repeat Until Satisfied

If needed, keep sending follow-up questions:

- back to the same expert to pressure-test its assumptions in light of new feedback
- to a neighboring expert whose mechanism now looks causally important
- to `09_mid_atlantic_priority` whenever transferability or seasonal timing is still unresolved
- to inventory support from `13_inventories_and_local_lists` whenever plant choice, sequence, or harvest flow is still underspecified

There is no fixed volley limit. The orchestrator should keep iterating until it can defend the synthesis against the main unresolved dependencies.

### Stop Condition

Synthesize only when the orchestrator can state:

- what the main recommendation is
- why the contributing domains do or do not agree
- what interactions drive the final answer
- what residual uncertainty remains

## Default Expert Packs

Use these as defaults, then add or remove domain experts based on the actual question.

These are the normal initial packs for substantive questions. Do not treat them as optional suggestions when the request clearly falls into one of these modes.

### Garden Plan Pack

- `02_intensive_vegetable_systems`
- `09_mid_atlantic_priority`
- `10_companion_planting_intercropping`
- `12_beneficial_insects_pest_indicators`
- inventory support from `13_inventories_and_local_lists`

Add as needed:

- `05_compost_soil_fertility`, `06_compost_tea_soil_biology`, `07_fungi_mycorrhiza_biostimulants`, `03_biochar`, or `04_bokashi_em` for soil-building-heavy plans
- `08_forest_gardens_agroforestry` and `11_wild_plants_foraged_integration` when the design includes perennial layers, wild integration, or food-forest elements
- `01_core_microfarm_permaculture` when system design and labor realism matter

### Pest Diagnosis Pack

- `12_beneficial_insects_pest_indicators`
- `10_companion_planting_intercropping`
- `05_compost_soil_fertility`
- `07_fungi_mycorrhiza_biostimulants`
- `09_mid_atlantic_priority`

Add `06_compost_tea_soil_biology` when the user is asking about teas, inoculants, or disease suppression.

### Soil-Building Pack

- `05_compost_soil_fertility`
- `03_biochar`
- `04_bokashi_em`
- `06_compost_tea_soil_biology`
- `07_fungi_mycorrhiza_biostimulants`
- `09_mid_atlantic_priority`

### Forest-Garden / Wild-Integration Pack

- `08_forest_gardens_agroforestry`
- `11_wild_plants_foraged_integration`
- `12_beneficial_insects_pest_indicators`
- `10_companion_planting_intercropping`
- `09_mid_atlantic_priority`
- inventory support from `13_inventories_and_local_lists`

### Farm-System / Labor / Viability Pack

- `01_core_microfarm_permaculture`
- `02_intensive_vegetable_systems`
- `09_mid_atlantic_priority`

Add any biological domain that materially changes the recommendation.

## Minimum Synthesis Standard

Before finalizing an answer, explicitly check whether any of these would change the recommendation:

- climate and Mid-Atlantic timing
- succession timing across the season
- plant spacing, canopy structure, or interplanting effects
- soil biology and organic-matter management
- nutrient balance and plant stress
- beneficial insect habitat and pest feedback loops
- perennial / wild integration opportunities
- labor, harvest, and workflow implications

If at least one of these would materially change the answer, do not give a single-domain response.

If the answer did not involve specialist skill activation and a parallel first pass, treat that as a failure mode unless the task was genuinely administrative.

## Output Expectations

Default to concise answers, but make the interconnections explicit. When the answer is synthetic, include:

- the main recommendation
- why the recommendation changes when other domains are considered
- which domain experts contributed
- which specialist skills were activated
- the most relevant local files or papers
- any unresolved tension or tradeoff
- which domain areas may still need stronger coverage or more source material

For garden plans, also include:

- layout assumptions
- plant list
- succession sequence
- weekly or phase-based action calendar
- monitoring points

For interview mode, also include:

- current phase
- what should already be done
- what should happen next
- what is commonly missed

## Resources

### scripts/

- `scripts/query_knowledgebase.py`
  Use this first to search the local catalog and plant inventories by topic or keyword.
- `scripts/build_topic_indexes.py`
  Regenerates the domain-expert cards if the knowledgebase gains new resources or folders.

### references/

- [references/orchestrator-grounding.md](references/orchestrator-grounding.md)
  Grounding rules that anchor the orchestrator in `01_core_microfarm_permaculture` and the Bec Hellouin materials before specialist synthesis.
- [references/topic-routing.md](references/topic-routing.md)
  First-stop routing guide and expert-pack selector.
- [references/domain-expert-registry.md](references/domain-expert-registry.md)
  Registry of the specialist expert agents and their missions.
- [references/specialist-skill-map.md](references/specialist-skill-map.md)
  Map of the 12 local specialist skills that the orchestrator should use for isolated sub-agents.
- [references/interconnections.md](references/interconnections.md)
  Cross-topic synthesis heuristics and default ecological link checks.
- [references/iterative-orchestration.md](references/iterative-orchestration.md)
  Feedback-loop rules for reacting to specialist output and asking follow-up questions.
- [references/specialist-isolation.md](references/specialist-isolation.md)
  Rules for keeping specialist experts isolated on the first pass and only sharing cross-expert findings intentionally.
- [references/garden-planning-workflow.md](references/garden-planning-workflow.md)
  Garden-design workflow for image-based plans.
- [references/direct-qa-workflow.md](references/direct-qa-workflow.md)
  Question-answer workflow for cross-domain synthesis.
- [references/interview-timeline-workflow.md](references/interview-timeline-workflow.md)
  Weekly timeline and seasonal interview workflow.
- `references/domain-experts/*.md`
  Specialist expert cards for each knowledgebase domain.
