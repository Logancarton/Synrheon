# Current Stage

## Active Stage

**Stage 1 — Cognitive Substrate**

## Stage 0B Closure

Stage 0B — Observable Organism Harness is **Verified** and remains the live laboratory for all later work.

## Current Stage 1 Boundary

The first Stage 1 increment now targets four separable substrate layers:

```text
Layer 1 — Concept Identity
What is this?

Layer 2 — World Relations
How can things relate in general?

Layer 3 — Current Activation / Situation
What is active now?

Layer 4 — Organism Relation
What does this mean to Synrheon?
```

The organism-relative layer is intentionally distinct from generic world knowledge.

Initial self-relation dimensions:

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

Every world/self relation preserves provenance such as:

```text
injected
observed
inferred
learned
```

Injected information must never silently become "learned."

## Sequencing Foundation Pulled Forward

Because computational time is foundational and the current design needs a memory thread, the current Stage 1 work also introduces a narrow Stage 2 foundation:

```text
meaningful event
 ↓
episode coordinate
 ↓
monotonic experience sequence
 ↓
previous / next event links
 ↓
current-episode experience thread
```

This does **not** mean Stage 2 is complete.

The current thread is in-memory only and does not survive process restart.

## Implemented in the Current Candidate

- `Concept`, `WorldRelation`, `SelfRelation`, `SelfRelationVector`, and `ActivationState`
- explicit separation of world knowledge, self-relative knowledge, and activation
- confidence-weighted self-vector update equation with evidence lineage
- Knowledge UI for explicit concept/world/self injection
- computational episode time and monotonic experience sequence
- ordered `ExperienceThread` with previous/next links
- Chat recorded as `observed`
- Internal Thought injection recorded as `injected`
- experience thread visible in Internal Thought and raw state

## What Is Still Missing

Stage 1 is not complete.

There is still no implemented:

- automatic language-to-concept interpretation
- recurrent spreading activation
- competition / inhibition
- Top-K sparse activation
- context gating
- automatic self-learning from live outcomes
- retrieval
- durable memory
- semantic response generation
- autonomous cognition

## Immediate Next Cognitive Boundary

After this candidate is live-verified, the next Stage 1 mechanism should be the sparse activation update that combines:

```text
world relation support
+
current context
+
organism-relative relevance
-
competition
-
decay
```

and exposes the winning active concepts through the verified Internal Thought surface.
