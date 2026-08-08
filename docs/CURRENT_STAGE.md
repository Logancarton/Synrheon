# Current Stage

## Active Stage

**Stage 1 — Cognitive Substrate**

## Stage 0B Closure

Stage 0B — Observable Organism Harness is **Verified** and remains the live laboratory for all later work.

## Current Stage 1 Boundary

The first Stage 1 increment now targets four separable substrate layers:

```text
Layer 1 — Concept Identity
Layer 2 — World Relations
Layer 3 — Current Activation / Situation
Layer 4 — Organism Relation
```

Layer 4 is not one blended personal score. Each concept has two permanently separate organism-relative vectors:

```text
injected_self_vector
self_learned_vector
```

Both use these initial dimensions:

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

Injected self scaffolding may seed the first vector. Only experience-based learning may update the second. Later activation can combine both without losing their provenance.

## Sequencing Foundation Pulled Forward

Because computational time is foundational and the design needs a memory thread, this Stage 1 increment also introduces a narrow Stage 2 foundation:

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

This does **not** mean Stage 2 is complete. The current thread is in-memory only and does not survive process restart.

## Implemented in the Current Candidate

- `Concept`, `WorldRelation`, `SelfRelation`, `SelfRelationVector`, and `ActivationState`
- separate generic world state, injected self state, self-learned state, and current activation
- confidence-weighted update of the **learned** self vector only
- learned evidence-event lineage and learned confidence
- Knowledge UI for explicit concept/world/self injection
- computational episode time and monotonic experience sequence
- ordered `ExperienceThread` with previous/next links
- Chat recorded as `observed`
- Internal Thought injection recorded as `injected`
- experience thread visible in Internal Thought and raw state

## What Is Still Missing

Stage 1 is not complete. There is still no implemented:

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

After this candidate is live-verified, the next Stage 1 mechanism should be sparse activation that combines:

```text
world relation support
+
current context
+
injected self relevance
+
self-learned relevance
-
competition
-
decay
```

and exposes the winning active concepts through Internal Thought.
