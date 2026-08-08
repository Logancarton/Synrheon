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

The development UI may stimulate, step, continue, pause, inject explicit developer scaffolding, and inspect Synrheon.

It must not own cognitive interpretation, retrieval, memory, learning, abstraction, or problem-solving behavior.

## D011 — Canonical Repository

Synrheon's canonical repository is:

```text
https://github.com/Logancarton/Synrheon
```

Agents should use this repository without asking the user to provide it again.

## D012 — World Knowledge and Organism Knowledge Stay Separate

Generic world relationships and Synrheon-relative relationships are different state.

Examples:

```text
Daisy IS_A dog
```

is world knowledge, while:

```text
Daisy.social = 0.8
Daisy.experience = 0.9
```

is organism-relative knowledge.

The two may influence the same future activation calculation but one must not overwrite or silently become the other.

## D013 — Injected, Observed, Inferred, and Learned Provenance Is Preserved

Knowledge and experience must retain how they entered the organism.

Initial provenance categories are:

```text
injected
observed
inferred
learned
```

Injected developer scaffolding must never be relabeled as self-learned merely because it is stored or later used.

If neural training later absorbs a pattern, the explicit source/evidence representation remains outside model weights.

## D014 — Self-Learned Representation Remains Explicit Outside Neural Weights

Synrheon may later train neural components from experience, but the authoritative record of organism-learned relevance remains explicit and inspectable.

The initial self relation vector contains:

```text
ownership
experience
social
goal
history
knowledge
trust
prediction
consequence
preference
uncertainty
```

The initial online update is:

```text
s_new = s_old + (learning_rate × trust) × (observation - s_old)
```

Each learned update preserves supporting experience-event IDs.

## D015 — Experience Thread Is Ordered but Is Not Yet Durable Memory

Meaningful current-process events receive:
- episode ID
- monotonic experience sequence
- absolute timestamp
- elapsed episode time
- previous/next event links
- observed vs injected provenance

This creates an autobiographical thread for live cognition.

It does not become durable memory until a later memory owner persists and retrieves it across process restart.
