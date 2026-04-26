---
name: ecoag-domain-expert-builder
description: Create new standalone ecological-agriculture domain experts in this local garden workspace, including the knowledgebase folder, literature-discovery workflow, downloaded-paper integration, expert brief, taxonomy, specialist skill, and orchestrator registration. Use when the user wants to add a new topic area that should behave like the existing `ecoag-*` specialist skills and be callable independently.
---

# EcoAg Domain Expert Builder

## Overview

Use this skill when a new ecological-agriculture domain should become a first-class local expert rather than just another folder of notes. It mirrors the current specialist pattern in this workspace: local knowledge folder, standalone specialist skill, expert brief, retrieval taxonomy, orchestrator card, registry entry, and skill-map integration.

## Workflow

1. Define the new domain clearly.
- Read [references/domain-expert-spec.md](references/domain-expert-spec.md).
- Choose the knowledgebase folder, skill name, expert title, domain mission, core lens, and first-pass handoffs.
- Keep the new expert narrow enough to be independently useful and broad enough to justify its own folder.

2. Scaffold the structure.
- Write a JSON spec that matches [references/domain-expert-spec.md](references/domain-expert-spec.md).
- Run `scripts/init_domain_expert.py --spec <spec.json> --update-agents`.
- This creates the knowledgebase folder, standalone specialist skill, expert brief stub, taxonomy stub, orchestrator card, registry entry, and specialist-skill-map entry.

3. Build the paper set.
- Read [references/build-workflow.md](references/build-workflow.md).
- Search locally first for overlap or adjacent literature already in `knowledgebase`.
- Browse for primary literature, official extension material, and other stable technical sources when the new folder is still thin.
- Download PDFs or save stable `.url` shortcuts plus local notes into the new knowledgebase folder.
- Integrate new sources into `knowledgebase/catalog.csv` and update `knowledgebase/README.md` when the domain meaningfully expands the paper set.

4. Finish the expert materials.
- Turn the scaffolded `references/expert-brief.md` into a real expert card for the specialist.
- Turn the scaffolded `references/taxonomy.md` into a retrieval map grounded in the actual downloaded/local sources.
- Add domain-specific resources such as process guides, matrices, seasonal checklists, or diagnostic notes when the domain benefits from them.

5. Integrate the new expert into the multi-agent stack.
- Confirm the new expert card appears in the orchestrator registry.
- Confirm the specialist skill appears in the specialist skill map.
- Update routing packs or orchestration references manually if the new domain should become part of default expert packs.

6. Validate.
- Run the skill validator on the new specialist skill.
- Forward-test the new specialist on at least one realistic question when the domain is important enough to justify it.
- Check that the expert can answer locally first, then browse outward only when the folder is thin.

## Working Rules

- Keep new experts local to `G:\My Drive\Home Docs\Garden`.
- Mirror the current specialist pattern instead of inventing a second architecture.
- Default to one specialist skill per domain, not one skill per paper or per micro-technique.
- Make the new expert independently callable with its own `SKILL.md`, `agents/openai.yaml`, `references/expert-brief.md`, and `references/taxonomy.md`.
- Treat the taxonomy as the specialist's own retrieval layer, not the orchestrator's.
- Make the specialist local-first and then web-enabled for additional scientific context when the local folder is thin, conflicting, incomplete, or missing a needed mechanism.
- Prefer primary literature and extension sources when browsing for new papers.
- Distinguish clearly between downloaded/local evidence and outside context in the final specialist outputs.

## Output Contract

- Create or update the standalone specialist skill and supporting files.
- Ensure the new expert can be called independently.
- Ensure the expert is integrated into orchestrator references.
- Suggest missing papers, weak evidence areas, and next resource additions when the new domain is still incomplete.
- Report the files created or changed.

## Resources

### scripts/
- `scripts/init_domain_expert.py`
  Scaffold a new local knowledge folder, specialist skill, taxonomy stub, expert brief stub, and orchestrator integration from a JSON spec.

### references/
- [references/domain-expert-spec.md](references/domain-expert-spec.md)
  JSON spec schema and example for new expert creation.
- [references/build-workflow.md](references/build-workflow.md)
  Research, discovery, download, taxonomy, and integration workflow for new domains.
