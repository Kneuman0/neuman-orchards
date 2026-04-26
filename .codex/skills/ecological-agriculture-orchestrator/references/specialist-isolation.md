# Specialist Isolation

This file defines how the specialist experts should be run as isolated agents.

## Purpose

The point of the specialist agents is not just topical organization. It is to let each expert think from its own domain without being prematurely biased by the other experts.

## Default Runtime Model

For a cross-domain question:

1. The orchestrator grounds itself in `01_core_microfarm_permaculture` and the Bec Hellouin materials.
2. The orchestrator identifies the needed specialists.
3. It spawns those specialists as separate isolated agents using `spawn_agent` with `fork_context=false`.
4. Each isolated specialist researches its own folder and returns its own answer.
5. The orchestrator compares the answers and decides what follow-up questions are needed.
6. Only then does it selectively reveal cross-expert findings where necessary.

For any substantive ecological-agriculture question, this isolated parallel specialist model is the default, not a special case.

## What Each Isolated Specialist Gets

- the user question
- the orchestrator's narrowed question for that domain
- the local specialist skill for that domain
- the expert card for that domain if it is needed as an extra brief
- the corresponding knowledgebase folder path
- support inventory data only if required

## What Each Isolated Specialist Should Not Get On First Pass

- other specialists' answers
- other specialists' mechanisms
- the orchestrator's preferred answer
- prior synthesis notes
- the full multi-domain context dump

## Why Isolation Matters

Isolation helps preserve:

- genuine domain-specific reasoning
- disagreement detection
- cleaner causal testing
- better follow-up questions from the orchestrator

If every specialist sees everyone else's answer too early, you lose the main benefit of specialization.

## When Cross-Expert Sharing Is Allowed

Cross-expert sharing is allowed only after the first pass, and only for one of these reasons:

- testing whether one specialist's condition invalidates another specialist's recommendation
- resolving disagreement
- checking a causal dependency
- checking whether a plan still works at a different scale, phase, or climate constraint

## Orchestrator Responsibility

The orchestrator should explicitly decide:

- which findings are worth forwarding
- which specialist should receive them
- what exact question the forwarded finding is supposed to test

Do not broadcast all results to all specialists.

Do not skip specialist spawning and answer from the orchestrator alone unless the task is purely administrative.
