# Domain Expert Spec

Use this JSON spec with `scripts/init_domain_expert.py`.

## Required Fields

```json
{
  "folder": "14_seed_saving_selection",
  "skill_name": "ecoag-seed-saving",
  "display_name": "EcoAg Seed Saving",
  "short_description": "Seed saving and selection",
  "expert_name": "Seed Saving Expert",
  "focus": "seed saving, pollination biology, isolation, selection, and home-scale breeding logic",
  "mission": "Own seed saving, variety maintenance, isolation, roguing, selection pressure, and breeding decisions for ecological garden systems.",
  "core_lens": "This expert thinks in genetics, pollination biology, isolation distance, population maintenance, and adaptation over time rather than one-season yield alone.",
  "when_to_use": [
    "the question is about saving seed, maintaining varietal purity, or home-scale selection",
    "the answer depends on pollination biology, population size, or isolation logic"
  ]
}
```

- `folder`: Knowledgebase folder name under `knowledgebase`.
- `skill_name`: Standalone specialist skill name under `.codex/skills`.
- `display_name`: Human-facing specialist skill title.
- `short_description`: Short UI blurb for `agents/openai.yaml`.
- `expert_name`: Domain expert title used in registry/card files.
- `focus`: Short focus phrase for the skill description.
- `mission`: Domain mission used in expert-brief and registry text.
- `core_lens`: How this expert thinks differently from neighboring domains.
- `when_to_use`: List of trigger situations for the specialist.

## Optional Fields

```json
{
  "default_handoffs": [
    "02_intensive_vegetable_systems when crop handling or seasonal occupancy matters",
    "09_mid_atlantic_priority when regional timing or overwintering matters"
  ],
  "discovery_queries": [
    "seed saving isolation distance peer reviewed",
    "home garden seed saving pollination biology extension"
  ],
  "anchor_files": [
    "G:\\My Drive\\Home Docs\\Garden\\knowledgebase\\Bec_Hellouin_summary.md"
  ],
  "update_agents": true
}
```

- `default_handoffs`: Optional neighboring experts to name in the brief and card.
- `discovery_queries`: Optional starter search queries seeded into the taxonomy stub.
- `anchor_files`: Optional high-priority local files relevant to the new domain.
- `update_agents`: Optional boolean. If true, the scaffold script also updates `AGENTS.md`.

## Output Created By The Scaffold Script

- `knowledgebase/<folder>/`
- `.codex/skills/<skill_name>/SKILL.md`
- `.codex/skills/<skill_name>/agents/openai.yaml`
- `.codex/skills/<skill_name>/references/expert-brief.md`
- `.codex/skills/<skill_name>/references/taxonomy.md`
- `.codex/skills/ecological-agriculture-orchestrator/references/domain-experts/<folder-slug>.md`
- `.codex/skills/ecological-agriculture-orchestrator/references/domain-expert-registry.md`
- `.codex/skills/ecological-agriculture-orchestrator/references/specialist-skill-map.md`

## Example Command

```powershell
python .codex\skills\ecoag-domain-expert-builder\scripts\init_domain_expert.py `
  --spec G:\My Drive\Home Docs\Garden\my-domain-spec.json `
  --update-agents
```
