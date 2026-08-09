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

# 2. Current External Chat Flow

```text
Chat text
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
previous / next event links updated
 ↓
StimulusRecord links to experience_event_id
 ↓
state + trace
 ↓
UI
```

The message is retained as experience. No hand-written cognitive policy currently interprets it, spreads activation from it, or manufactures a response.

# 3. Current Internal Thought Injection Flow

```text
Internal Thought text
 ↓
POST /api/thought
 ↓
runtime.inject_internal_thought()
 ↓
time.py
 ↓
ExperienceEvent(origin="injected")
 ↓
ordered current-episode thread
 ↓
state + trace
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

# 5. Current Ownership

```text
core.py
├─ Concept
├─ WorldRelation
├─ OrganismRelation
├─ SelfRelation
├─ ActivationState           representation only
├─ CognitiveSubstrate
└─ OrganismState

cognition.py
└─ reserved owner for future trainable cognitive policy
   (no hand-written thinking algorithm)

time.py
├─ TemporalCoordinate
└─ ComputationalTime

experience.py
├─ ExperienceEvent
└─ ExperienceThread

runtime.py     sequence owners / route commands only
interfaces.py  HTTP / browser transport only
ui/            explicit injection + observation only
```

# 6. Removed Experimental Cognition

The following flow was tried and then deliberately removed from production:

```text
text
 ↓
lexical concept match
 ↓
fixed relation spreading
 ↓
fixed salience / decay / inhibition
 ↓
fixed Top-K winners
```

The experiment demonstrated end-to-end state-changing wiring, but its decision mechanics were developer-selected rather than learned. It must not be silently rebuilt inside runtime, retrieval, memory, or UI.

# 7. Current Self-Learning Storage Mechanism — Built, Not Live Outcome-Integrated

`CognitiveSubstrate.learn_self_relation()` accepts an arbitrary relation type and updates only its learned representation while preserving injected/world state and evidence IDs.

This remains a narrow storage update. It does **not** decide which cognitive path to take and is not the trainable thinking policy.

There is still no live outcome/feedback owner deciding when or why to call it.

# 8. Current Episode Boundary

Starting a fresh session:

```text
new session / episode
 ↓
experience sequence reset
 ↓
experience thread cleared
 ↓
current activation cleared
```

Injected concepts/world relations/injected organism relations and learned organism relations remain for the life of the running Python process.

Process restart still loses all of this because durable persistence is not implemented.

# 9. Planned Trainable Cognitive Policy Flow

```text
experience / current state
        ↓
CognitiveState representation
        ↓
available generic cognitive actions
        ↓
trainable policy P(action | state)
        ↓
selected cognitive action
        ↓
short state transition / path
        ↓
checkpoint
        ↓
state after
        ↓
prediction / outcome / error
        ↓
credit assignment
        ↓
policy / transition learning
```

The central requirement is **transfer**: a policy trained on knowledge worlds A/B/C should remain useful in unseen world D without concept-name or answer-specific rules.

# 10. Planned Retrieval Flow

```text
current cognitive state
        ↓
learned decision to retrieve
        ↓
Level 1 coarse orientation
        ↓
Level 2 relevant situation / episode / concept region
        ↓
Level 3 detailed evidence / relationships
        ↓
checkpoint / next cognitive action
```

Retrieval should become one cognitive operation available to the learned policy rather than a response to hard-coded phrases.

# 11. Planned Durable Memory Flow

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

# 12. Planned Language / Perception Flow

Language should not be the cognition owner.

```text
text / observation
        ↓
perception / concept grounding
        ↓
cognitive state
        ↓
trainable cognitive policy
        ↓
state result
        ↓
optional language expression
```

A neural encoder or LLM may later participate in perception/expression without owning Synrheon's persistent autobiographical state or learned cognitive process.

# 13. Planned Training Trace

A useful training unit should preserve at least:

```text
state before
candidate cognitive actions
selected action
short path / transition
state after
prediction
outcome
error
credit
```

Training should reward useful process/outcome evidence, not merely reinforce a path because it happened to be selected.
