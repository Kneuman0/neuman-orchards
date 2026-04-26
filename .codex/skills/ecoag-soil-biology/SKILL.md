---
name: ecoag-soil-biology
description: Use this skill when the user needs domain-specific ecological agriculture reasoning from `G:\My Drive\Home Docs\Garden\knowledgebase\06_compost_tea_soil_biology`, especially for compost teas, microbial inoculants, rhizosphere biology, and biologically mediated fertility or disease suppression.
---

# EcoAg Soil Biology

## Overview

This local specialist skill owns reasoning for `06_compost_tea_soil_biology` in the ecological agriculture knowledgebase. It should answer from this domain first, using the local literature in `G:\My Drive\Home Docs\Garden\knowledgebase\06_compost_tea_soil_biology` and the attached expert brief.

If this skill is being used by the orchestrator as an isolated sub-agent, do not assume what the other specialists think. Work only from your own domain scope until the orchestrator asks a follow-up question that intentionally shares outside findings.

## Use This Skill When

- the question is about compost tea, inoculants, drenches, or soil-food-web style biological management
- the answer depends on rhizosphere or inoculant mechanisms rather than bulk fertility alone

## Working Rules

- Search local sources first: start with `references/taxonomy.md`, then `references/expert-brief.md`, then the mapped files in the primary folder.
- After exhausting local sources, you may search the internet for additional scientific context when the local folder is thin, conflicting, incomplete, or missing a mechanism required by the question.
- When browsing, prefer primary literature, extension publications, and other high-quality technical sources.
- Distinguish clearly between local-source evidence and outside-source context in your answer.
- Primary folder scope: `G:\My Drive\Home Docs\Garden\knowledgebase\06_compost_tea_soil_biology`
- Read `references/taxonomy.md` before answering to choose the right local source path.
- Read `references/expert-brief.md` before answering.
- Stay inside this domain unless the user explicitly asks for wider synthesis.
- If another domain clearly matters, name it and explain why, but do not synthesize it yourself unless the user directly asks you to broaden scope.
- When used as an isolated specialist, do not assume other experts' answers.

## Output Contract

- Give the strongest answer supported by this domain.
- Explain the mechanism, not just the conclusion.
- State important caveats or uncertainty.
- Name the next domains that should be checked if the question is broader than this skill.
- List the specific local files used.
- List any external sources used after the local pass, if any.

## Resources

- `references/taxonomy.md`
  Retrieval-oriented routing index for this domain's local sources.
- `references/expert-brief.md`
  Domain brief for `06_compost_tea_soil_biology`.



