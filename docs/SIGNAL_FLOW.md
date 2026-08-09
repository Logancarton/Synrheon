# Synrheon Signal Flow

This document separates **CURRENT REAL FLOW**, **E011-A CONTROLLED EXPERIMENT FLOW**, and **E011-B PLANNED LIVE COGNITION FLOW**.

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

# 5. Current Organism UI Evidence Flow

```text
backend OrganismState
        ↓
GET /api/state
        ↓
ui/index.html
        ↓
Organism tab
        ├─ live experience thread
        ├─ concepts
        ├─ world relations
        ├─ injected vs learned organism relations
        ├─ activation
        ├─ cycle / counts
        └─ stage-specific evidence
```

The UI also has a reserved growth surface that may later display backend-owned learning/generalization metrics.

Until a learning owner actually produces those values, the UI must say that cognitive growth is not measured.

# 6. Current Ownership

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

# 7. Removed Experimental Cognition

The following flow was tried and deliberately removed from production:

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

The experiment demonstrated end-to-end state-changing wiring, but its decision mechanics were developer-selected rather than learned. It must not be rebuilt inside runtime, retrieval, memory, learning, or UI.

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

# 9. E011-A v1 — Controlled Process-Transfer Assay

E011-A is the next implementation target.

It is a controlled scientific assay, not yet the live organism cognition path.

## 9.1 Generated world flow

```text
seed
 ↓
e011a-v1 generator
 ↓
complete hidden 10–14 node graph
 ├─ visible start
 ├─ hidden goal marker
 ├─ unique shortest route 3–5 edges
 ├─ 2–4 distractor branches
 └─ 0–2 cross/back edges
```

The generator/scorer may retain the complete graph.

The policy may not.

## 9.2 Hidden-truth firewall

```text
                ┌────────────────────────────┐
                │ generator / scorer         │
                │ full graph                 │
                │ hidden goal location       │
                │ shortest path / cost       │
                │ success truth              │
                └─────────────┬──────────────┘
                              │
                 scoring / training evidence
                              │
                              │ NEVER policy input
                              │
revealed state only           ↓
        ┌────────────────────────────┐
        │ CognitiveState             │
        │ revealed nodes / edges     │
        │ frontier / expanded state  │
        │ known depth / reveal order │
        │ remaining budget           │
        │ goal marker only if seen   │
        │ valid actions + targets    │
        └─────────────┬──────────────┘
                      ↓
                 learned policy
```

Forbidden policy inputs include:

```text
unrevealed nodes / edges
hidden goal location
shortest path
shortest-path distance
on-solution-path flags
correct next action / target
future frontier
solver output
world seed as a predictive feature
```

If hidden truth crosses this boundary, the experiment is invalid.

# 10. E011-A v1 — Cognitive Micro-Cycle

The first action vocabulary is intentionally only:

```text
EXPAND(target)
STOP
```

The flow is:

```text
revealed CognitiveState S(t)
        ↓
enumerate valid candidates
        ├─ EXPAND(frontier target A)
        ├─ EXPAND(frontier target B)
        ├─ ...
        └─ STOP
        ↓
policy selects operation + target
        ↓
execute deterministic action
        ↓
consume 1 of 10 cognitive actions
        ↓
revealed CognitiveState S(t+1)
        ↓
record checkpoint / outcome / cost
        ↓
goal revealed + STOP? ── yes ──→ success
        │
        no
        ↓
budget left? ── yes ──→ next policy step
        │
        no
        ↓
fail by budget exhaustion
```

Python may define which actions are valid. Python must not choose the preferred frontier target.

# 11. E011-A v1 — Training / Evaluation Flow

```text
TRAIN worlds 1000–4999
        ↓
optimize model seeds 11 / 22 / 33 / 44 / 55
        ↓
DEVELOPMENT VALIDATION 5000–5999
        ↓
freeze final configuration
        ↓
FINAL LEVEL-1 HELD-OUT 10000–10999
        ↓
paired identity permutation 20000–20999
        ↓
compare all five trained runs against:
        ├─ random-valid policy
        ├─ matched untrained model
        └─ exhaustive all-reachable cost reference
```

Future Level-2 structural worlds use 30000–30999 under a separately versioned topology distribution.

Final held-out data is not a tuning surface.

# 12. E011-A v1 — Checkpoint / Credit Record

```text
state_before
+
available_actions_and_targets
        ↓
selected_action
        ↓
state_after
        ↓
observed_outcome
+
compute_cost
        ↓
error_or_correction
        ↓
credit_assignment
```

The record shape also reserves:

```text
predicted_state_after
expected_value
alternative_action_estimates
```

These may be deferred/null in the first policy-only slice, but the architecture must not later confuse selection with usefulness.

# 13. E011-A v1 — Cognitive Cost Flow

```text
checkpoint
 ↓
record EXPAND / STOP / invalid / stale-target / budget use
 ↓
world outcome
 ↓
compare successful action cost against exhaustive reference
 ↓
report efficiency with success
```

The hard budget is exactly 10 actions for E011-A v1.

The first pass requires successful mean cost at or below 80% of the exhaustive all-reachable reference and mean hard-budget use at or below 80% while meeting the success thresholds.

# 14. E011-A v1 — Failure Classification Flow

```text
result
 ↓
classify first
 ├─ failed learning
 ├─ memorization / overfit
 ├─ identity shortcut
 ├─ structural overfit
 ├─ inefficient cognition
 ├─ insufficient / misleading state
 └─ answer leakage
 ↓
inspect correct owner / representation
 ↓
new experiment revision if material contract changes
```

Do not jump from a failed example directly to a world-specific code patch.

# 15. E011-A v1 — Model Lineage / Growth Flow

```text
trained checkpoint
 ↓
model artifact metadata
 ├─ model + parent ID
 ├─ experiment / generator / state / action versions
 ├─ model seed / training split
 ├─ config hash
 ├─ episodes seen
 ├─ parameter checksum
 ├─ Git commit
 └─ evaluation summary
 ↓
immutable evaluation history
 ↓
backend learning_metrics summary
 ↓
Organism UI growth surface
```

The UI displays backend-owned evidence. It does not compute the scientific result itself.

# 16. E011-B — Planned Live Cognition Flow

Only after a controlled E011-A artifact is ready for integration:

```text
live legitimate CognitiveState
        ↓
cognition.py
        ↓
learned operation + target
        ↓
bounded transition
        ↓
checkpoint
        ↓
runtime.py sequences only
        ↓
OrganismState + trace
        ↓
interfaces.py
        ↓
Organism UI
```

The generated experiment's hidden scorer, full graph, hidden goal, and solution path are not production dependencies.

Runtime may invoke the cognition owner and route its output. Runtime must not reimplement target choice, learning, memory, or policy scoring.

# 17. Broader Planned Policy / Transition / Value Boundary

The long-term cognitive architecture still distinguishes:

```text
POLICY
P(a | S)
Which operation + target should happen next?

TRANSITION
F(S, a) → predicted S'
What should that action change?

VALUE
V(S, a)
How useful should that action be from here?
```

E011-A v1 may begin with the policy question only. Prediction and value remain distinct future trainable quantities rather than hand-written scores.

# 18. Planned Perception → Cognition Boundary

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

# 19. Planned Knowledge / Skill Separation

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

# 20. Planned Retrieval Flow

```text
current CognitiveState
        ↓
policy selects RETRIEVE(target, region, depth)
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

# 21. Planned Durable Memory Flow

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

# 22. Planned Language Expression Flow

Expression happens after cognition has produced enough state to communicate:

```text
resolved / reportable cognitive state
        ↓
language expression owner / model
        ↓
external response
```

Fluent text must never be used as proof that the internal cognitive process occurred.

# 23. Planned Autonomous Continuation

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
