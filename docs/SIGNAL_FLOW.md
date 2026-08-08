# Synrheon Signal Flow

This document separates **CURRENT REAL FLOW** from **PLANNED / INTENDED FLOW**.

# 1. Current Real Application Flow

```text
PowerShell
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

The UI remains a control/observation surface.

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
experience.py → append ExperienceEvent(origin="observed")
 ↓
previous / next event links updated
 ↓
StimulusRecord links to experience_event_id
 ↓
OrganismState snapshot
 ↓
UI
```

The event receives:
- episode ID
- monotonic experience sequence
- absolute timestamp
- elapsed episode time
- previous/next event links

# 3. Current Injected Internal Experience Flow

```text
Internal Thought composer
 ↓
POST /api/thought
 ↓
interfaces.py
 ↓
runtime.inject_internal_thought()
 ↓
time.py → next TemporalCoordinate
 ↓
experience.py → append ExperienceEvent(origin="injected")
 ↓
ordered experience thread
 ↓
state + trace
 ↓
Internal Thought view
```

An injected thought remains explicitly **injected**. It is not presented as self-generated cognition or self-learned knowledge.

# 4. Current Knowledge Injection Flow

The Knowledge tab provides explicit developer scaffolding.

## Concept

```text
Knowledge UI
 ↓
POST /api/concept
 ↓
runtime.define_concept()
 ↓
core.CognitiveSubstrate.add_concept()
 ↓
Concept stored
 ↓
snapshot → UI
```

## World Relation

```text
Knowledge UI
 ↓
POST /api/world-relation
 ↓
runtime.define_world_relation()
 ↓
core.CognitiveSubstrate.add_world_relation()
 ↓
WorldRelation(origin="injected")
 ↓
snapshot → UI
```

## Self Relation

```text
Knowledge UI
 ↓
POST /api/self-relation
 ↓
runtime.define_self_relation()
 ↓
core.CognitiveSubstrate.set_injected_self_relation()
 ↓
SelfRelation(origin="injected")
 ↓
snapshot → UI
```

Generic world knowledge and organism-relative knowledge are separate state.

# 5. Current Substrate Ownership

```text
core.py
├─ Concept
├─ WorldRelation
├─ SelfRelationVector
├─ SelfRelation
├─ ActivationState
├─ CognitiveSubstrate
└─ OrganismState

time.py
├─ TemporalCoordinate
└─ ComputationalTime

experience.py
├─ ExperienceEvent
└─ ExperienceThread

runtime.py
└─ sequencing / routing only

interfaces.py
└─ HTTP / browser transport only

ui/
└─ injection + observation only
```

# 6. Current Self-Learning Mechanism — Built, Not Live-Integrated

`CognitiveSubstrate.learn_self_relation()` implements:

```text
s_new
=
s_old
+
(learning_rate × trust)
×
(observation - s_old)
```

It:
- updates only the explicit self relation vector
- sets provenance to `learned`
- increases confidence gradually
- records evidence event IDs
- does not rewrite world relations

There is not yet a live outcome/feedback owner that decides when to call this mechanism.

# 7. Current Activation State — Representation Only

`ActivationState` exists and remains separate from stored concept/world/self knowledge.

There is not yet a live activation equation, spreading activation, competition, inhibition, decay, or Top-K sparse selection.

# 8. Current Episode Boundary

Starting a fresh session:

```text
Start
 ↓
new session ID
 ↓
new computational-time episode
 ↓
experience sequence = 0
 ↓
new empty ExperienceThread
 ↓
activation cleared
```

Injected concepts/world/self relations remain in the running process when a session is restarted.

Everything is still in-memory. Process restart loses the current substrate and experience thread.

# 9. Planned Sparse Activation Flow

This is intended architecture, not current implementation.

```text
stimulus / active context
        ↓
concept candidates
        ↓
world relation support
        +
organism-relative relevance
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

Later:

```text
ordered ExperienceEvent thread
        ↓
memory owner
        ↓
persistent episode / event storage
        ↓
retrieval
        ↓
reconstructed sequence / evidence
```

# 12. Planned Neural Training Flow

```text
explicit experience
        ↓
explicit self/world provenance
        ↓
trusted learning trace
        ↓
optional neural training
        ↓
weights improve
```

Training must not erase the explicit record of:
- what was injected
- what was observed
- what was inferred
- what was learned
- which evidence supported the learning
