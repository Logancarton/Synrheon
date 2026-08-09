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

## What `cognition.py` Owns Now

`cognition.py` remains the correct owner for future next-state cognitive transformation, but it intentionally contains no hand-written routing algorithm.

The target is a **trainable cognitive policy** that learns transformations such as:

```text
state before
+
available cognitive actions
        ↓
select cognitive action
        ↓
short transition / path
        ↓
checkpoint
        ↓
state after
        ↓
prediction / outcome / error / credit
```

The core question is not “Can the model memorize an answer?”

It is:

> Can a learned cognitive process transfer to concepts and knowledge worlds it never saw during training?

## Immediate Experimental Target

The next experiment should train on several tiny unrelated knowledge worlds and evaluate on a held-out world with new concept names and relations.

Pass/fail should focus on transfer:

```text
training worlds A/B/C
        ↓
learn cognitive process
        ↓
unseen world D
        ↓
select useful cognitive operations better than baseline
```

The model should not receive world-specific answers or concept-name shortcuts.

## What Is Still Missing

- trainable `CognitiveState` representation
- generic cognitive-action representation
- state → action policy
- short transition/checkpoint loop
- prediction-error / credit assignment
- transfer-training harness
- semantic language understanding
- durable memory
- Level 1 → Level 2 → Level 3 retrieval
- response generation
- recursive scratchpad cognition
- autonomous continuation

## Guardrail

Do not rebuild the removed heuristic under new names.

The design rule going forward is:

```text
hard-code the learning/process boundaries
learn the cognitive routing and useful transitions
```
