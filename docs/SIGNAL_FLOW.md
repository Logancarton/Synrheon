# Synrheon Signal Flow

This file shows only two things:

```text
CURRENT LIVE FLOW
TARGET GROUND 0 COGNITIVE FLOW
```

## Current Live Flow

```text
Chat / injected developer thought
        ↓
dev_server.py
        ↓
runtime.py
        ↓
temporal.py + experience.py
        ↓
state.py
        ↓
UI
```

Current truth:

- external Chat becomes ordered `observed` experience;
- developer Internal Thought becomes ordered `injected` experience;
- time, sequence, episode identity, and provenance are preserved;
- runtime sequences and routes;
- UI observes and controls;
- Ground 0 cognition is not yet called.

## Existing Trainable Policy Flow — Experimental Only

E011-A remains a useful controlled donor mechanism:

```text
revealed CognitiveState
        ↓
policy.py enumerates/scores valid operation + target candidates
        ↓
selected operation + target
        ↓
bounded experiment transition
        ↓
outcome / cost
        ↓
policy_learning.py update
```

Its narrow action set was:

```text
EXPAND(target)
STOP
```

This demonstrated transferable learned operation selection, not full Ground 0 cognition.

## Ground 0 Production Contract

`cognition.py` now owns the production-facing Ground 0 checkpoint vocabulary:

```text
broad_field
routing
tapering
recurrent_deliberation
evidence_assessment
complete
```

and dispositions:

```text
continue
commit
abstain
seek_evidence
reopen
```

This is a designed contract only. The real taper/recurrent mechanism is not live-integrated yet.

## Ground 0 Target Flow

```text
legitimate live state
        ↓
BROAD CANDIDATE / KNOWLEDGE FIELD
        ↓
learned context / operation routing
        ↓
REVERSIBLE SOFT TAPER
        ↓
Ground0Checkpoint
        ↓
SMALL SERIOUS-CANDIDATE FIELD
        ↓
STATE-DEPENDENT RECURRENCE
        ↓
Ground0Checkpoint
        ↓
EVIDENCE / UNCERTAINTY STATE
        ↓
COMMIT | ABSTAIN | SEEK EVIDENCE | REOPEN
        ↓
Ground0Checkpoint
        ↓
runtime sequences result
        ↓
state / trace
        ↓
UI
```

## Critical Separation

```text
Taper:
Which candidates still deserve serious compute?

Recurrence:
How do the surviving serious alternatives alter one another's support?

Commitment:
Is the evidence sufficient to act?
```

HCT-2 showed why this matters: removing recurrence reduced good behavior to 45% even though the correct candidate survived tapering 100% of the time.

## Reopening Flow

```text
initial context
        ↓
softly suppress candidate
        ↓
new / changed context arrives
        ↓
reopen broader preserved field
        ↓
rerun appropriate taper / deliberation
```

Hard Top-K is not the Ground 0 default because HCT-1 and HCT-2 both showed irreversible deletion failing context-reversal cases.

## Optional Reliability Flow

Historical evidence/pathway reliability may modify support when useful:

```text
source / pathway history
        ↓
learned reliability or resistance
        ↓
modulated evidence influence
```

This remains optional. HCT-2 did not require learned resistance for full good behavior.

## Ownership Rule

```text
cognition.py
    Ground 0 process/checkpoint owner

policy.py + policy_learning.py
    retained learned-routing donor mechanism

state.py
    explicit organism/cognitive substrate state

temporal.py + experience.py
    event position, sequence, provenance, ordered experience

runtime.py
    sequences handoffs only

dev_server.py
    local browser/API transport only

UI
    observation / control only

experiments
    hidden truth / scientific scoring only
```

The HCT generator, hidden correct identity, and frozen scientific scorer must never become production cognition inputs.
