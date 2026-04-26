# Direct Q&A Workflow

Use this when the user asks a direct question and expects the answer to reflect cross-topic connections.

## Procedure

1. Identify the actual decision behind the question.
2. Ground first using `orchestrator-grounding.md` whenever the question is system-level or interdisciplinary.
3. Route using `topic-routing.md`.
4. Load the relevant domain-expert cards.
5. If the question is meaningfully interdisciplinary, spawn parallel expert explorers.
6. Ask each domain expert for:
   - strongest answer from its folder
   - mechanism
   - practical implication
   - caveat
   - cross-topic dependencies
7. Run an interdependence scan using `iterative-orchestration.md`.
8. If needed, ask follow-up questions to the same or different experts, repeating until satisfied.
9. Integrate locally only after the main conflicts or dependencies have been tested.

## Synthesis Standard

The final answer should do more than stack summaries. It should say:

- which mechanism dominates
- which supporting mechanisms modify the recommendation
- which common interpretations are too narrow
- what the user should change in practice

## Typical Question Types

### Pest questions

Check:

- habitat and beneficials
- nutrient balance
- biological vigor
- plant stress or stalled growth
- climate timing

### Soil amendment questions

Check:

- decomposition and maturity
- microbial claims versus evidence
- interaction with irrigation, disease, or plant defense
- labor and repeatability

### Plant-selection questions

Check:

- zone-7 fit from the support inventories
- succession role
- companion or intercropping role
- pest and beneficial implications
- perennial or wild-integration opportunities

## What To Cite

Prefer local files from the knowledgebase. When the answer is synthetic, cite the most relevant files from each contributing topic rather than dumping the whole folder.
