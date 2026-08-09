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

Example:

```text
Daisy IS_A dog
```

is world knowledge, while organism-relative relations describe what Daisy means to Synrheon.

The two may later influence the same learned cognitive state, but one must not overwrite or silently become the other.

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

## D014 — Organism Relations Are Open-Ended Data, Not a Fixed Cognitive Ontology

Synrheon must not be limited to a hard-coded list of ways that something can matter to her.

Organism-relative relation types are stored as data. A relation type not known when the software was written must be representable without changing production code.

For each concept, injected and self-learned organism relations remain permanently separate collections:

```text
injected_relations
≠
learned_relations
```

Injected developer scaffolding may write only `injected_relations`.

Experience-based learning may create or update only `learned_relations`.

The existing learned-relation update is a narrow provenance-preserving storage mechanism, not a thinking policy.

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

## D016 — The First Hand-Written Sparse Activation Policy Was Experimental and Is Retired

A temporary experiment used:

```text
lexical concept matching
fixed graph spreading
fixed decay / salience gains
fixed inhibition
fixed Top-K
fixed recurrence rounds
```

It proved that the live Chat/runtime path could reach a state-changing cognition owner and expose the result in the UI.

It did **not** prove that those developer-selected mechanics were the correct long-term cognition policy.

That production logic has been removed. Historical experiment evidence may remain in Git history/docs, but future agents must not treat the retired heuristic as current architecture.

## D017 — Train the Cognitive Process Instead of Hand-Coding Cognitive Routes

Synrheon's next core hypothesis is that the system should learn **how to transform cognitive state** rather than primarily memorize input→output mappings or follow developer-authored reasoning routes.

The preferred training unit is:

```text
state before
candidate cognitive actions
selected action
short transition / path
checkpoint
state after
prediction
outcome
error
credit
```

The architecture may define general process boundaries, representations, safety constraints, compute limits, and learning mechanics.

It should not encode world-specific answers, stimulus-specific branches, or permanent rules saying which relation/path to follow for a given phrase.

A selected path is not automatically rewarded. Learning should depend on outcome, correction, prediction error, or other evidence that the transition was useful.

The required research test is **transfer**:

```text
train on unrelated knowledge worlds A/B/C
        ↓
learn cognitive-action policy
        ↓
evaluate on unseen world D
```

If the policy only works because it remembers concept names, relation labels, exact prompts, or answers from training, the experiment fails.
