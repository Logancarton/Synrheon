# Synrheon Signal Flow

This document separates:

```text
CURRENT LIVE ORGANISM FLOW
CONTROLLED E011-A SCIENTIFIC FLOW
PLANNED E011-B LIVE COGNITION FLOW
```

# 1. Current Real Application Flow

```text
synrheon.ps1 run / python -m synrheon
        ↓
SynrheonRuntime
        ↓
interfaces.py
        ↓
local HTTP server
        ↓
browser UI
```

The UI controls and observes. It does not own cognition.

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
time.py → TemporalCoordinate
 ↓
experience.py → ExperienceEvent(origin="observed")
 ↓
StimulusRecord + trace
 ↓
OrganismState snapshot
 ↓
UI
```

Chat currently records ordered experience.

It does **not** yet invoke the E011-A learned policy.

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

Injected thought remains explicitly injected. It is not self-generated cognition.

# 4. Current Knowledge Injection Flow

## Concept

```text
Knowledge UI
 ↓
/api/concept
 ↓
runtime.define_concept()
 ↓
CognitiveSubstrate.add_concept()
```

## World Relation

```text
Knowledge UI
 ↓
/api/world-relation
 ↓
runtime.define_world_relation()
 ↓
CognitiveSubstrate.add_world_relation()
```

## Organism Relation

```text
Knowledge UI
 ↓
/api/self-relation
 ↓
runtime.define_self_relation()
 ↓
CognitiveSubstrate.set_injected_self_relation()
```

The relation type remains open-ended data.

# 5. Current Production Ownership

```text
core.py
├─ explicit concepts / relations
├─ activation representation
└─ OrganismState

cognition.py
├─ CognitiveState
├─ RevealedNode
├─ CognitiveAction
└─ LinearCognitivePolicy

learning.py
├─ PolicyDecisionTrace
└─ ReinforceLearner

time.py
└─ computational event coordinates

experience.py
└─ ordered current-episode experience

runtime.py
└─ thin sequencing / routing only

interfaces.py
└─ browser / HTTP transport only

ui/
└─ observation / control only
```

The E011-A policy/learner exist in production owners, but the live runtime does not call them yet.

# 6. Removed Historical Cognition

The following path is no longer production cognition:

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

Do not rebuild this behavior inside runtime, memory, retrieval, learning, or UI.

---

# 7. Current Controlled E011-A Flow — Built

The hidden experiment environment lives outside production cognition:

```text
experiments/e011a.py
```

Real E011-A flow:

```text
seeded hidden generated graph
        │
        ├──────────────→ hidden scorer / reference truth
        │
        │ reveal only legitimate local state
        ↓
CognitiveState
        ↓
src/synrheon/cognition.py
LinearCognitivePolicy
        ↓
score every valid EXPAND(target) / STOP candidate
        ↓
learned operation + target
        ↓
experiments/e011a.py applies one deterministic bounded transition
        ↓
new revealed CognitiveState
        ↓
observable outcome + cognitive cost
        ↓
src/synrheon/learning.py
ReinforceLearner
        ↓
policy weights update
```

Critical separation:

```text
hidden graph / hidden goal / shortest path / correct target
        └──────── experiment harness only

revealed state / valid candidates
        └──────── policy-visible
```

# 8. E011-A Inference Flow

At one checkpoint:

```text
CognitiveState
        ↓
valid action enumeration
        ↓
for each candidate:
    build visible-state feature vector
        ↓
linear candidate score
        ↓
softmax probability
        ↓
choose operation + target
```

The opaque target handle is used to execute the selected target.

The handle identity itself is not a trainable feature.

# 9. E011-A Learning Flow

```text
candidate evaluations
+
selected candidate
        ↓
transition occurs
        ↓
outcome / cost reward
        ↓
discounted return
        ↓
running baseline
        ↓
policy-gradient credit
        ↓
weights change
```

The learning owner receives outcome/cost evidence, not hidden route truth.

# 10. E011-A Evidence Flow

```text
training worlds 1000–4999
        ↓
trained policies for seeds 11 / 22 / 33 / 44 / 55
        ↓
untouched held-out worlds 10000–10999
        ↓
paired renaming 20000–20999
        ↓
random + matched-untrained + exhaustive references
        ↓
frozen numeric gate
        ↓
data/e011a_v1_evidence.json
```

Recorded controlled result supports Level 1 identity/instance transfer.

This path is **Built** but not live-runtime Integrated.

---

# 11. Planned E011-B Live Integration Flow — Next

The next correct path is:

```text
identified recorded policy artifact
        ↓
legitimate live CognitiveState source / adapter
        ↓
cognition.py
learned policy inference
        ↓
operation + target
        ↓
bounded cognition-owned transition
        ↓
explicit checkpoint
        ↓
runtime.py sequences handoff
        ↓
OrganismState / trace
        ↓
Organism UI
```

Runtime may:
- sequence the owner;
- route state/action/checkpoint handoffs;
- expose outcomes and feedback.

Runtime must not:
- score candidates;
- choose the preferred target;
- contain the hidden experiment solver;
- duplicate policy/learning logic.

# 12. E011-B UI Evidence Flow

When live integration exists:

```text
backend-owned live policy state
        ↓
OrganismState / API
        ↓
UI
```

The UI should display:

```text
loaded model/artifact identity
current live CognitiveState summary
selected learned operation + target
resulting checkpoint
live stage status
recorded backend-owned growth evidence
```

The UI must not calculate the scientific pass result or make cognitive decisions.

# 13. Future Policy / Transition / Value Boundary

The broader architecture still separates:

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

E011-A v1 implemented the first policy slice only.

# 14. Future Retrieval Flow

```text
current CognitiveState
        ↓
policy selects RETRIEVE(target, region, depth)
        ↓
Level 1 orientation
        ↓
Level 2 relevant region
        ↓
Level 3 detailed evidence
        ↓
new checkpoint
```

Retrieval remains future work.

# 15. Future Durable Memory Flow

```text
ordered ExperienceEvent thread
        ↓
memory owner
        ↓
persistent episodes/events
        ↓
learned retrieval
        ↓
CognitiveState checkpoint
```

Durable memory is not implemented yet.

# 16. Future Expression Flow

```text
reportable cognitive state
        ↓
language expression owner / model
        ↓
external response
```

Fluent text must never be used as proof that internal cognition occurred.

# 17. Future Autonomous Continuation

Only after bounded live cognitive steps prove useful:

```text
checkpoint
 ↓
unresolved state + expected value of more cognition
 ↓
autonomy owner permits continuation
 ↓
runtime sequences cognition again
```

A hard safety/resource ceiling remains infrastructure even if continuation preference later becomes learned.
