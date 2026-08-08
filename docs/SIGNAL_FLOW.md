# Synrheon Signal Flow

This document separates **CURRENT REAL FLOW** from **PLANNED / INTENDED FLOW**.

# 1. Current Real Application Flow

```text
.\scripts\synrheon.ps1 run
        ↓
python -m synrheon
        ↓
runtime.main()
        ↓
SynrheonRuntime
        ↓
interfaces.run_development_server(runtime)
        ↓
local HTTP server
        ↓
browser
```

The UI controls/injects explicit scaffolding and observes. It does not own cognition.

# 2. Current External Experience Flow

```text
Chat
 ↓
POST /api/stimulus
 ↓
interfaces.py
 ↓
runtime.send_external_stimulus()
 ↓
time.py → next TemporalCoordinate
 ↓
experience.py → ExperienceEvent(origin="observed")
 ↓
previous / next links
 ↓
StimulusRecord → experience_event_id
 ↓
state → UI
```

Each event receives episode ID, monotonic experience sequence, timestamp, elapsed episode time, and before/after links.

# 3. Current Injected Internal Experience Flow

```text
Internal Thought
 ↓
POST /api/thought
 ↓
runtime.inject_internal_thought()
 ↓
time.py
 ↓
experience.py → ExperienceEvent(origin="injected")
 ↓
ordered current-episode thread
 ↓
UI
```

Injected thought remains explicitly injected. It is not self-generated cognition or self-learned knowledge.

# 4. Current Knowledge Injection Flow

## Concept

```text
Knowledge UI → /api/concept → runtime.define_concept()
             → CognitiveSubstrate.add_concept()
```

## World Relation

```text
Knowledge UI → /api/world-relation → runtime.define_world_relation()
             → CognitiveSubstrate.add_world_relation()
             → WorldRelation(origin="injected")
```

## Injected Organism Relation

```text
Knowledge UI
  relation_type = arbitrary non-empty text
  strength = 0..1
  confidence = 0..1
        ↓
POST /api/self-relation
        ↓
runtime.define_self_relation()
        ↓
CognitiveSubstrate.set_injected_self_relation()
        ↓
SelfRelation.injected_relations[relation_type]
```

No production-code list decides which organism relation types are allowed.

Generic world knowledge, injected organism relations, self-learned organism relations, and current activation are separate state.

# 5. Current Substrate Ownership

```text
core.py
├─ Concept
├─ WorldRelation
├─ OrganismRelation
├─ SelfRelation
│  ├─ injected_relations: arbitrary typed relations
│  └─ learned_relations: arbitrary typed relations
├─ ActivationState
├─ CognitiveSubstrate
└─ OrganismState

time.py
├─ TemporalCoordinate
└─ ComputationalTime

experience.py
├─ ExperienceEvent
└─ ExperienceThread

runtime.py     sequencing / routing only
interfaces.py  HTTP / browser transport only
ui/            explicit injection + observation only
```

# 6. Current Self-Learning Mechanism — Built, Not Live-Integrated

`CognitiveSubstrate.learn_self_relation()` accepts an arbitrary relation type and implements:

```text
learned_new
=
learned_old
+
(learning_rate × trust)
×
(observed_strength - learned_old)
```

It:
- creates the learned relation type if it does not already exist
- updates only the learned relation with that type
- leaves the injected relation of the same type unchanged
- leaves world relations unchanged
- increases learned confidence gradually
- records supporting experience-event IDs

There is not yet a live outcome/feedback owner that decides when this mechanism should run or what relation type an experience implies.

# 7. Current Activation State — Representation Only

`ActivationState` exists separately from stored concept/world/organism knowledge.

There is not yet a live activation equation, spreading activation, competition, inhibition, decay, or Top-K sparse selection.

# 8. Current Episode Boundary

Starting a fresh session creates a new episode, resets experience sequence/thread, and clears current activation.

Injected concepts/world relations/injected organism relations and any learned organism relations remain for the life of the current process.

Process restart still loses all of this because durable memory/persistence is not implemented.

# 9. Planned Sparse Activation Flow

```text
stimulus / active context
        ↓
concept candidates
        ↓
world relation support
+
context-compatible injected organism relations
+
context-compatible learned organism relations
+
current goal / recent context
        ↓
recurrent activation update
        ↓
competition + inhibition + decay
        ↓
Top-K sparse active region
        ↓
Internal Thought observation
```

The activation mechanism should operate over whatever organism relation types exist rather than enumerating a closed relation ontology in code.

# 10. Planned Retrieval Flow

```text
active sparse region
        ↓
Level 1 coarse orientation
        ↓
Level 2 relevant situation / episode / concept region
        ↓
Level 3 detailed evidence / relationships
        ↓
scratchpad
        ↓
cognition
```

# 11. Planned Durable Memory Flow

The current `ExperienceThread` is not durable memory.

```text
ordered ExperienceEvent thread
        ↓
memory owner
        ↓
persistent episodes/events
        ↓
retrieval
        ↓
reconstructed sequence / evidence
```

# 12. Planned Neural Training Flow

```text
explicit experience
        ↓
explicit world/injected-organism/learned-organism provenance
        ↓
trusted learning trace
        ↓
optional neural training
        ↓
weights improve
```

Training must not erase the explicit record of what was injected, observed, inferred, or learned, nor collapse injected and self-learned organism relations into one opaque representation.
