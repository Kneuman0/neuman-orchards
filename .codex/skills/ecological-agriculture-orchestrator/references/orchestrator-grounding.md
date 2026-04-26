# Orchestrator Grounding

This file defines what the orchestrator itself must know before it starts synthesizing specialist answers.

## Anchor Knowledge

The orchestrator should be intimately familiar with:

- `01_core_microfarm_permaculture`
- `G:\My Drive\Home Docs\Garden\knowledgebase\Bec_Hellouin_summary.md`
- `Bec-Hellouin-Farm-Profitability-study.pdf`
- the Morel microfarm thesis and related microfarm-viability papers in `01_core_microfarm_permaculture`

These sources provide the best end-to-end lifecycle context in the knowledgebase for how ecological production systems actually function over time.

## Why This Grounding Comes First

The specialist agents are narrower by design. The orchestrator needs the anchor context first so it can frame better questions for the specialists and recognize when a specialist answer is locally true but systemically incomplete.

The anchor context should shape the orchestrator's thinking about:

- season-spanning workflow, not isolated interventions
- labor realism and management burden
- ecological maturity and whole-system dependencies
- protected cultivation, bed design, and manual intensification
- short-cycle crops, market fit, and throughput
- the fact that the intensive nucleus depends on wider ecological support systems

## When Grounding Is Mandatory

Ground in `01_core_microfarm_permaculture` and Bec Hellouin before synthesis whenever the user asks for:

- a garden or farm plan
- a yearly timeline or weekly operating schedule
- end-to-end practice design
- integrated questions spanning multiple domains
- questions about whether a practice fits into a coherent ecological production system

## When Grounding Can Be Lighter

If the question is extremely narrow and technical, the orchestrator may use lighter grounding, but it should still remember that the final answer may need to reconnect to the whole-system context if the user broadens the scope.

## What The Orchestrator Should Extract Before Querying Specialists

Before the first specialist volley, identify:

- the likely system scale
- the likely labor and management intensity
- whether the user is implicitly asking about annual-bed intensification, perennial structure, or both
- whether the practice depends on wider ecological support functions
- which lifecycle stage of the system is most relevant: establishment, intensification, turnover, harvest flow, or long-horizon maturation

## Grounding Effect On Specialist Questions

The orchestrator should use the anchor context to ask better specialist questions. Examples:

- ask the pest expert not just "what controls this pest?" but "what does this pest imply about the stability of the production system described here?"
- ask the intensive-vegetable expert not just "does this planting fit?" but "does it fit the turnover and labor rhythm implied by the system?"
- ask the soil experts not just "does this amendment help?" but "does it improve the long-run ecological function of the system or only solve a narrow short-term issue?"
