# Interview / Weekly Timeline Workflow

Use this when the user wants the skill to keep them on track through a full year.

## Goal

Build a one-year operating timeline separated by week, then use that timeline to ask the user phase-appropriate questions and catch missing tasks.

## Base Inputs

- location and climate
- garden dimensions or number of beds
- annual versus perennial emphasis
- key crops or crop families
- perennial inventory already in use
- self-seeding annuals the user wants to rely on
- irrigation and season-extension setup

## Timeline Structure

Every weekly line should be able to hold:

- sowing or transplant tasks
- succession decisions
- compost, mulch, or residue handling
- biological or inoculant actions when relevant
- pest and disease watch points
- beneficial-habitat tasks
- expected harvests
- next-step triggers

## Phase Logic

Minimum yearly phases:

- late winter
- early spring
- mid spring
- late spring
- early summer
- midsummer
- late summer
- early fall
- late fall
- winter

Within each phase, convert to weeks if the user wants full operational tracking.

## Interview Mode

When the user asks for a check-in:

1. Identify the current week or phase.
2. Ground the phase in the end-to-end system logic from `01_core_microfarm_permaculture` and the Bec Hellouin materials.
3. Pull the expected tasks for that period.
4. Ask only the questions needed to reveal misses, delays, or bottlenecks.
5. If a missing task changes another domain, ask follow-up questions to the relevant specialist expert before finalizing the advice.
6. Continue follow-up questioning until the cascade effects are clear enough to advise the user confidently.
7. Report:
   - what should already be done
   - what is due now
   - what is likely to be forgotten next
   - how delays affect later succession or harvests

## Agent Pack

Default:

- `01_core_microfarm_permaculture`
- `02_intensive_vegetable_systems`
- `09_mid_atlantic_priority`
- `12_beneficial_insects_pest_indicators`
- support data from `13_inventories_and_local_lists`

Add:

- `08` and `11` for perennial or wild-integrated timelines
- `05`, `06`, `07`, `03`, `04` when soil-building actions are central to the user's system
- `10` when interplanting or trap-crop timing matters

## Output Requirement

If the user asks for a yearly plan, give both:

- a phase summary
- a week-by-week operating version

If the user asks for a live check-in, give:

- the current week or phase
- the checklist
- the gap analysis
- the next checkpoint
