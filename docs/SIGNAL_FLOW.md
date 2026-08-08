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

# 2. Current External Chat → Cognition Flow

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
runtime invokes cognition.py
 ↓
activate_from_text(substrate, text, experience_event_id)
 ↓
generic lexical cue match against existing concept IDs / labels
 ↓
bounded recurrent sparse activation
 ↓
CognitiveFrame linked to same experience_event_id
 ↓
ActivationState replaced with current Top-K winners
 ↓
snapshot + trace
 ↓
Chat activation card + Internal Thought + inspector
```

No natural-language reply is generated yet. The visible result is a real cognitive-state transition, not a fabricated chatbot answer.

# 3. Current Internal Thought Injection → Cognition Flow

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
runtime invokes the same cognition.py mechanism
 ↓
CognitiveFrame
 ↓
ActivationState + UI
```

Injected thought remains explicitly injected. It is not self-generated cognition or self-learned knowledge.

# 4. Current Sparse Activation Transformation

Owned by `src/synrheon/cognition.py`.

For each textual experience:

```text
text
 ↓
known concept cue(s)
 ↓
seed activation = 1.0
 ↓
3 bounded recurrent rounds
```

Each round performs:

```text
current activation × decay
+
normalized outgoing world-relation support
+
organism-relation salience for already-reached concepts
+
re-seeded current stimulus concepts
 ↓
clip to 0..1
 ↓
activation floor + winner-relative inhibition threshold
 ↓
Top-K sparse survivors
```

Initial parameters:

```text
decay               0.30
spread gain         0.62
organism gain       0.35
inhibition fraction 0.10
activation floor    0.05
Top-K               5
rounds              3
```

Outgoing world-relation influence is normalized by the source concept's total outgoing confidence. This prevents a high-degree source from sending unlimited total activation merely because it has many edges.

# 5. Current Organism-Relation Contribution

For a concept already reached by the current cue/world spread:

```text
relation salience = strength × confidence
```

Injected and learned organism relations are both eligible to contribute, but remain separately stored and separately labeled in the observable contribution path.

The relation type itself is open-ended data. `cognition.py` does not enumerate or special-case relation names.

Organism relations do **not** independently seed unrelated concepts in this first mechanism.

# 6. Current Lexical Cue Boundary

The current text-to-concept bridge is intentionally small:

```text
normalized text tokens
       ↓
match existing concept ID or label phrase
       ↓
seed matching concept
```

This is a temporary lexical bootstrap, not semantic language understanding.

If no known concept matches:

```text
experience remains recorded
+
CognitiveFrame(status="unmatched")
+
current activation cleared
```

# 7. Current Knowledge Injection Flow

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

# 8. Current Ownership

```text
core.py
├─ Concept
├─ WorldRelation
├─ OrganismRelation
├─ SelfRelation
├─ ActivationState
├─ ActivationContribution
├─ CognitiveFrame
├─ CognitiveSubstrate
└─ OrganismState

cognition.py
├─ ActivationConfig
├─ generic lexical cue matching
├─ recurrent world-relation spreading
├─ organism salience
├─ inhibition / Top-K competition
└─ current activation transformation

time.py
├─ TemporalCoordinate
└─ ComputationalTime

experience.py
├─ ExperienceEvent
└─ ExperienceThread

runtime.py     sequence owners / route typed handoffs
interfaces.py  HTTP / browser transport only
ui/            explicit injection + observation only
```

# 9. Current Self-Learning Mechanism — Built, Not Live Outcome-Integrated

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

It creates/updates only the learned relation and preserves evidence-event IDs. There is still no live outcome/feedback owner deciding when or why to call it.

# 10. Current Episode Boundary

Starting a fresh session:

```text
new session / episode
 ↓
experience sequence reset
 ↓
experience thread cleared
 ↓
cognitive frames cleared
 ↓
current activation cleared
```

Injected concepts/world relations/injected organism relations and learned organism relations remain for the life of the running Python process.

Process restart still loses all of this because durable persistence is not implemented.

# 11. Planned Retrieval Flow

```text
sparse active region
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

# 12. Planned Durable Memory Flow

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

# 13. Planned Learned Language / Perception Flow

The current lexical cue matcher should eventually become only one low-cost route inside a richer perception layer:

```text
text / observation
        ↓
learned language/perception mechanism
        ↓
candidate concepts / senses + confidence
        ↓
existing cognition.py sparse activation owner
```

A future LLM/neural encoder may own part of this perception step without erasing Synrheon's explicit state/provenance.

# 14. Planned Neural Training Flow

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

Training must not erase what was injected, observed, inferred, or learned, nor collapse explicit organism relations into opaque weights.
