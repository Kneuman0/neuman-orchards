# Iterative Orchestration

This file defines the orchestrator's real job: not routing alone, but building on specialist feedback until the interdependent answer is stable.

For substantive ecological-agriculture requests, this loop is mandatory. The orchestrator should not bypass it and answer from a single undifferentiated context window unless the task is merely administrative.

## Orchestrator Role

The orchestrator is a specialist in ecological interdependence. It should:

- start from the anchor context in `01_core_microfarm_permaculture` and the Bec Hellouin materials
- detect which domain answers modify or constrain other domain answers
- identify when a single-domain answer is falsely complete
- ask follow-up questions to the same or different experts when causal links are still weak
- synthesize only after the interaction structure is clear enough to support a practical recommendation

## Required Loop

### 0. Grounding pass

Before the first specialist volley, ground the orchestration in:

- `references/domain-experts/01-core-microfarm-permaculture.md`
- `G:\My Drive\Home Docs\Garden\knowledgebase\Bec_Hellouin_summary.md`
- other files from `01_core_microfarm_permaculture` if the user is asking for end-to-end design or lifecycle guidance

### 1. Initial specialist pass

Ask each relevant expert for:

- strongest answer from its own domain
- mechanism
- caveats
- what other expert it needs next

Run the relevant specialists in parallel by default.

Run these as isolated first-pass specialists. Do not let them see each other's outputs yet.

### 2. Interdependence scan

Review the first-pass answers and explicitly look for:

- conflict: two experts push different actions
- dependency: one answer only works if another domain condition is true
- omission: a critical mechanism is missing
- scale mismatch: one answer works at plant scale while another fails at bed, season, or labor scale
- timing mismatch: a recommendation breaks under Mid-Atlantic timing or succession flow

### 3. Follow-up questioning

When a gap is found, do one of these:

- ask the same expert to revise its answer in light of a new constraint
- ask a different expert to evaluate the missing mechanism
- expand the expert pack if a previously ignored domain is now causally important
- selectively forward only the specific cross-expert finding that needs testing

Repeat this step as many times as needed. There is no one-follow-up limit.

## Good Follow-Up Patterns

- "The pest expert thinks aphids indicate excess soluble nitrogen. Ask the compost and soil-fertility expert whether the current fertility plan could plausibly create that condition."
- "The intercropping expert likes the mixture, but ask the intensive-vegetable expert whether it still works with the proposed succession schedule and harvest access."
- "The forest-garden expert wants a perennial edge. Ask the beneficial-insects expert whether that edge is likely to improve or complicate local pest dynamics."
- "The biochar expert sees a benefit, but ask the Mid-Atlantic expert whether the amendment timing and water regime are realistic in this climate."

## Minimum Follow-Up Triggers

Do another question round whenever:

- two experts disagree on action
- one expert names another domain as a dependency
- the answer changes planting, timing, or labor enough that another domain may break
- the user's question clearly asks for interconnections, not just summaries
- the orchestrator cannot yet explain the answer in whole-system terms consistent with the anchor microfarm context

## Satisfaction Standard

Keep iterating until the orchestrator can say yes to all of these:

- I understand how this recommendation fits into the whole-system lifecycle.
- I have tested the main dependencies named by the specialists.
- I have checked whether the answer still makes sense under Mid-Atlantic timing when that matters.
- I have resolved or exposed the main specialist conflicts.
- I can give the user an operational recommendation rather than a stack of disconnected domain notes.
- I actually used the relevant specialist skills and did not collapse the job back into a monolith answer.

## Output Standard

The final answer should show that the orchestrator reacted to expert feedback rather than merely listing it. That usually means stating:

- which expert feedback changed the plan
- what follow-up was required
- what the revised answer became after cross-checking
- which specialist skills were activated
- what domain coverage still looks thin and should be improved
