# Build Workflow

Use this workflow after scaffolding the new domain expert.

## 1. Scope The Domain

- Make sure the new domain is not already adequately covered by an existing expert.
- Define what this expert owns that neighboring experts do not.
- Define the first-pass handoffs for questions that spill into adjacent domains.

## 2. Search Local First

- Search `knowledgebase` for overlapping papers, notes, and references.
- Search `knowledgebase/catalog.csv` for adjacent topics that should be copied or cross-linked.
- Search the existing specialist taxonomies for overlap or reusable source clusters.

## 3. Browse For New Papers

- Use web search only after checking local sources.
- Prefer:
  - peer-reviewed primary literature
  - official extension publications
  - USDA, SARE, or other stable technical institutions
- Save PDFs directly into the new knowledge folder when possible.
- If direct PDF capture is blocked, save a `.url` shortcut plus a short local `.md` note.

## 4. Integrate New Sources

- Add new sources to `knowledgebase/catalog.csv`.
- Update `knowledgebase/README.md` when the new folder meaningfully changes the knowledgebase map.
- Keep filenames stable and descriptive.

## 5. Build The Specialist Materials

- Update `references/expert-brief.md` with real mission, lens, handoffs, and indexed resources.
- Update `references/taxonomy.md` so it reflects the actual local files, not just placeholders.
- Add domain-specific resources when they materially improve retrieval:
  - process guides
  - crop matrices
  - diagnostic tables
  - annual timelines
  - troubleshooting maps

## 6. Integrate The Expert

- Confirm the new domain expert card exists under the orchestrator `references/domain-experts`.
- Confirm the new expert appears in:
  - `references/domain-expert-registry.md`
  - `references/specialist-skill-map.md`
- Update broader routing docs manually if the new expert should join default packs or default handoff logic.

## 7. Validate

- Run the skill validator on the new specialist skill.
- Ask at least one realistic domain question to ensure:
  - the specialist starts from its own local folder
  - the taxonomy routes correctly
  - outside browsing happens only after the local pass
  - the expert names the right neighboring handoffs

## 8. Improve The Domain

- Suggest missing papers when the expert is still weak.
- Suggest missing domain resources when paper coverage exists but retrieval is poor.
- Suggest skill refinements when the expert scope is too broad, too narrow, or too dependent on neighboring domains.
