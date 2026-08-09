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
└─ reserved owner for trainable cognitive-state transformation
   (no hand-written thinking policy today)

learning.py
└─ future outcome / error / credit / parameter-update owner

time.py
├─ TemporalCoordinate
└─ ComputationalTime

experience.py
├─ ExperienceEvent
└─ ExperienceThread

runtime.py     sequence owners / route typed handoffs only
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

The experiment demonstrated end-to-end state-changing wiring, but its decision mechanics were developer-selected rather than learned. It must not be silently rebuilt inside runtime, retrieval, memory, learning, or UI.

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

# 9. Planned Perception → Cognition Boundary

Language should not be the cognition owner.

```text
text / observation
        ↓
perception / grounding
        ↓
CognitiveState seed
        ↓
trainable cognition
```

Tokenization, embeddings, an LLM, vision encoder, or other perception system may later help construct a state seed. Those mechanisms must not decide the complete thought process merely because they recognized the input.

# 10. Planned Cognitive Micro-Cycle

One cognitive step should produce one observable checkpoint:

```text
CognitiveState S(t)
        ↓
expose available cognitive operations
        ↓
cognition.py policy chooses a(t)
        ↓
execute one bounded cognitive operation
        ↓
CognitiveState S(t+1)
        ↓
record checkpoint / trace
        ↓
resolved? ── yes ──→ stop / predict / act / express
   │
   no
   ↓
next micro-cycle
```

A checkpoint is computational state, not a wall-clock sleep.

The runtime may sequence this loop, but it must not select the cognitive action itself.

# 11. Planned Cognitive Action Flow

Initial experimental action vocabulary may include:

```text
FOCUS
EXPAND
RETRIEVE
COMPARE
CHECK_SEQUENCE
CHECK_EVIDENCE
PREDICT
REVISE
STOP
```

The action names describe generic operations. Production code must not contain mappings such as:

```text
phrase X → RETRIEVE
relation IS_A → EXPAND
concept Daisy → follow dog
```

The policy should learn when each operation is useful from state and outcome evidence.

# 12. Planned Training / Credit Flow

```text
state_before
+
available_actions
        ↓
selected_action
        ↓
short transition
        ↓
state_after checkpoint
        ↓
prediction / task consequence
        ↓
observed outcome / correction
        ↓
error
        ↓
learning.py assigns credit / blame
        ↓
policy / transition model parameters update
```

Critical rule:

```text
selected path ≠ successful path
```

No route is strengthened merely because the model chose it.

# 13. Planned Knowledge / Skill Separation

```text
KNOWLEDGE SOURCES
concepts
relations
experience
memory
tools
outside knowledge
        │
        ↓
CognitiveState
        │
        ↓
COGNITIVE SKILL
focus
explore
retrieve
compare
check
predict
revise
stop
```

This allows the same learned process to be evaluated with knowledge it never trained on.

# 14. Planned Transfer Experiment Flow

```text
training worlds A / B / C
        ↓
create task-specific CognitiveStates
        ↓
train cognitive-action policy
        ↓
freeze evaluation configuration
        ↓
unseen world D
        ↓
run policy
        ↓
measure task success + action sequence + checkpoints
        ↓
rename / permute concept identities
        ↓
run again
        ↓
compare against random / untrained baseline
```

The experiment is not passed by training-world accuracy alone.

# 15. Planned Retrieval Flow

```text
current CognitiveState
        ↓
policy selects RETRIEVE
        ↓
Level 1 coarse orientation
        ↓
Level 2 relevant situation / episode / concept region
        ↓
Level 3 detailed evidence / relationships
        ↓
new checkpoint
        ↓
policy chooses next cognitive action
```

Retrieval levels constrain search cost. They do not encode which answer is correct.

# 16. Planned Durable Memory Flow

```text
ordered ExperienceEvent thread
        ↓
memory owner
        ↓
persistent episodes/events
        ↓
retrieval operation
        ↓
reconstructed sequence / evidence
        ↓
CognitiveState checkpoint
```

# 17. Planned Language Expression Flow

Expression happens after cognition has produced enough state to communicate:

```text
resolved / reportable cognitive state
        ↓
language expression owner / model
        ↓
external response
```

Fluent text must never be used as proof that the internal cognitive process occurred.

# 18. Planned Autonomous Continuation

Only after bounded micro-cycles are useful under direct stimulation:

```text
checkpoint
 ↓
unresolved + expected value of more cognition
 ↓
autonomy owner permits another cycle
 ↓
runtime sequences cognition owner again
```

A hard resource ceiling remains infrastructure even if the preference to continue/stop becomes learned.
