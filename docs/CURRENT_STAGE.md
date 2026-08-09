# Current Stage

## Active Stage

**Stage 1 — Trainable Cognition Pivot**

Stage 0B — Observable Organism Harness remains **Verified** and continues to be the live laboratory.

## Why the Pivot Happened

The first sparse-activation experiment proved that Chat could reach a real state-changing owner, but the mechanism still depended on developer-selected cognition rules:

```text
lexical concept matching
fixed spreading gain
fixed decay
fixed organism salience gain
fixed inhibition threshold
fixed Top-K
fixed recurrence rounds
```

Those rules were useful scaffolding, but keeping them would turn Synrheon into a hand-designed graph reasoner rather than a system that learns **how to think**.

The production implementation has therefore removed that policy instead of extending it.

## Current Live Boundary

The live organism still preserves:

```text
Chat / Internal Thought
        ↓
interfaces.py
        ↓
runtime.py
        ↓
computational time
        ↓
ordered ExperienceEvent
        ↓
StimulusRecord + provenance + trace
        ↓
state / UI
```

Knowledge scaffolding also remains live:

```text
concepts
world relations
open-ended organism relations
activation representation
```

But **no hand-written thinking policy currently turns a stimulus into activation winners.**

## What Was Removed

The following are no longer production cognition:

```text
concept-label lexical matcher
relation traversal policy
spread = 0.62
decay = 0.30
organism gain = 0.35
inhibition fraction = 0.10
activation floor = 0.05
Top-K = 5
three recurrent rounds
```

No `CognitiveFrame` is manufactured from those heuristics now.

## New Development Rule: Cognitive Physics vs Cognitive Skill

Synrheon still needs designed software boundaries. The pivot does **not** mean that every line of code should be learned.

### Designed / fixed infrastructure may define

```text
what a CognitiveState can contain
how provenance is represented
what a cognitive-action interface looks like
how one checkpoint is recorded
maximum compute / step budgets
how training examples are serialized
how outcomes and corrections enter learning
safe validation and failure behavior
```

### Learned behavior should increasingly determine

```text
which concepts / regions deserve attention
which path is worth exploring
which cognitive action should happen next
when retrieval is useful
what evidence should be compared
what prediction is reasonable
when to revise
which earlier transition deserves credit / blame
when a thought process is complete
```

The architecture provides the **physics of cognition**. Training should learn the **skill of cognition**.

## What `cognition.py` Owns Now

`cognition.py` remains the correct owner for future next-state cognitive transformation, but it intentionally contains no hand-written routing algorithm.

The target is a **trainable cognitive policy** that operates through short observable micro-cycles:

```text
S0 — current cognitive state
 ↓
choose one cognitive action
 ↓
perform a bounded transition
 ↓
S1 — checkpoint
 ↓
inspect uncertainty / evidence / prediction
 ↓
choose next action
 ↓
S2 — checkpoint
 ↓
...
 ↓
stop / predict / act / answer
```

A checkpoint is computational state, not a literal wall-clock pause.

## Initial Cognitive Action Vocabulary

The first experiment may use a small action vocabulary such as:

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

These are **operations**, not answers or domain knowledge. The vocabulary is experimental and may later be learned, expanded, compressed, or replaced if evidence supports it.

Production code must not contain rules such as:

```text
if the user asks about a name → RETRIEVE
if relation == IS_A → EXPAND
if concept == Daisy → follow dog
```

The useful sequencing of cognitive actions is the thing to be learned.

## Training Record Contract

One useful training trace should preserve at least:

```text
state_before
available_actions
selected_action
short_transition_or_path
state_after
prediction
observed_outcome
error_or_correction
credit_assignment
```

Selection alone is **not** evidence that a path was useful. Synrheon must not reinforce a route merely because it chose that route.

## Knowledge Is Not the Main Training Target

The first cognitive-policy experiment should deliberately separate:

```text
WHAT SYN RHEON KNOWS
concepts / relations / experience / memory / external sources

from

WHAT SYN RHEON LEARNS TO DO
focus / explore / retrieve / compare / test / predict / revise / stop
```

Concept representations may themselves become trainable later, but knowledge content must not be allowed to masquerade as cognitive skill.

Language also remains outside the central thinking policy:

```text
language / observation
        ↓
perception / grounding
        ↓
CognitiveState
        ↓
learned cognitive process
        ↓
state result
        ↓
optional language expression
```

## Immediate Experimental Target

The next implementation should be the smallest trainable vertical slice capable of answering one research question:

> **Can a model learn a reusable cognitive-action policy that transfers to an unseen knowledge world?**

Training should use several small worlds with different content. Evaluation must include a held-out world with unseen concepts and preferably a different arrangement of relations.

```text
training worlds A / B / C
        ↓
learn cognitive-action policy
        ↓
unseen world D
        ↓
select useful cognitive operations better than baseline
```

### Anti-memorization controls

At minimum:

```text
opaque or randomized concept names
held-out concept identities
renaming / permutation test
no answer text in policy features
no production world-specific branches
untrained/random baseline
```

A stronger follow-up should also vary world topology so the policy cannot simply memorize one graph shape.

## First-Pass Success Criteria

The trainable slice is promising only if:

1. model parameters actually change through training;
2. training decision quality improves;
3. held-out-world performance exceeds an untrained/random baseline;
4. renaming concepts does not materially destroy the strategy;
5. the policy produces more than one useful cognitive action when the task requires several steps;
6. intermediate checkpoints remain observable;
7. training preserves outcome/error/credit evidence;
8. runtime only sequences the policy and does not contain the learned reasoning logic;
9. no answer-, concept-, relation-, or phrase-specific production branch is required.

## What Is Still Missing

- trainable `CognitiveState` feature representation
- generic cognitive-action representation
- state → action policy
- short transition/checkpoint loop
- transition / next-state prediction
- prediction-error / credit assignment
- transfer-training harness
- learned concept organization / routing
- semantic language grounding
- durable memory
- Level 1 → Level 2 → Level 3 retrieval
- response generation
- recursive scratchpad cognition
- autonomous continuation

## Guardrail

Do not rebuild the removed heuristic under new names.

The design rule going forward is:

```text
hard-code representations, interfaces, budgets, provenance, and learning boundaries

learn concept organization, cognitive routing, action selection, transition usefulness,
and eventually the process that turns one cognitive state into the next
```
