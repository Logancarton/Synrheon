# Current Stage

## Active Stage

**Stage 1 — Cognitive Substrate**

## Stage 0B Closure

Stage 0B — Observable Organism Harness is **Verified** and remains the live laboratory for all later work.

## Current Stage 1 Boundary

The first Stage 1 increment uses four separable substrate layers:

```text
Layer 1 — Concept Identity
Layer 2 — World Relations
Layer 3 — Current Activation / Situation
Layer 4 — Organism Relations
```

Layer 4 is now deliberately **open-ended**. Synrheon is not limited to a hard-coded list such as ownership, social, trust, or prediction.

For each concept, organism-relative relations are stored as arbitrary typed data, for example:

```text
protective_of
expects_help_from
reminds_me_of_home
trusted_source
```

Production code does not need to know those relation types in advance.

Injected and self-learned organism relations remain permanently separate:

```text
injected relations
≠
self-learned relations
```

Injected scaffolding can create only injected relations. Experience-based learning can create or update only learned relations. Later sparse activation may combine their relevance without losing provenance.

## Sequencing Foundation Pulled Forward

Because computational time is foundational and the design needs a memory thread, Stage 1 also uses a narrow Stage 2 foundation:

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

- `Concept`, `WorldRelation`, `OrganismRelation`, `SelfRelation`, and `ActivationState`
- open-ended organism relation types stored as data rather than Python fields
- separate generic world state, injected organism-relative state, self-learned state, and current activation
- confidence-weighted update of one arbitrary **learned** relation type
- learned evidence-event lineage and learned confidence
- Knowledge UI for explicit concept/world/injected-self scaffolding
- free-form organism relation type input in the UI/API
- computational episode time and monotonic experience sequence
- ordered `ExperienceThread` with previous/next links
- Chat recorded as `observed`
- Internal Thought injection recorded as `injected`
- experience thread visible in Internal Thought and raw state

## What Is Still Missing

Stage 1 is not complete. There is still no implemented:

- automatic language-to-concept interpretation
- automatic discovery/naming of new relation types from experience
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
relevant injected organism relations
+
relevant self-learned organism relations
-
competition
-
decay
```

and exposes the winning active concepts and contributing relation paths through Internal Thought.
