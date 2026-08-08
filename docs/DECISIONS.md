# Architectural Decisions

Keep durable architectural choices here until this file becomes large enough to justify separate ADR files.

## D001 — Bottom-Up Development

Synrheon will be developed from substrate upward rather than by patching individual conversational failures.

## D002 — Strict Initial Retrieval Cascade

Normal retrieval begins with:

```text
Level 1 → Level 2 → Level 3
```

Additional levels may be added later only if evidence supports them.

## D003 — Limited Temporal Scratchpad

The initial scratchpad uses:
- current situation: up to 3 condensed packages
- last hour: up to 2
- last day: up to 3

The scratchpad is RAM-like working state, not a full-day memory store.

## D004 — Time Is Foundational

Meaningful external and internal events receive temporal position and sequence information.

## D005 — Memory Existence, Strength, and Activation Are Separate

A memory may exist durably without being currently active.

## D006 — Failed Reasoning Does Not Make Participating Memories False

Synrheon should learn route usefulness and failure attribution separately from factual memory truth.

## D007 — External LLMs May Participate but Do Not Own Persistent Cognition

LLMs may help with interpretation, semantic inference, language, and outside knowledge while Synrheon owns persistent state, autobiographical sequence, memory lineage, and durable learning effects.

## D008 — Major Cognitive Owners Begin as Files, Not Packages

Start with a small number of high-context source files.

Split a file into a package only when the implementation demonstrates multiple independent owners or the file becomes meaningfully difficult to understand.

## D009 — Live Organism Before Deep Cognition

Before Stage 1 cognitive mechanisms are treated as the primary implementation target, establish a running Synrheon runtime and development UI.

The live organism is the primary testing laboratory.

Automated tests are regression support and cannot by themselves grant `Verified` status.

## D010 — UI Is an Observation and Control Surface

The development UI may stimulate, step, continue, pause, and inspect Synrheon.

It must not own cognitive interpretation, retrieval, memory, learning, abstraction, or problem-solving behavior.

## D011 — Canonical Repository

Synrheon's canonical repository is:

```text
https://github.com/Logancarton/Synrheon
```

Agents should use this repository without asking the user to provide it again.
