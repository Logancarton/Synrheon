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
interfaces.py
        ↓
runtime.py
        ↓
time.py + experience.py
        ↓
OrganismState / trace
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
valid cognitive action + target candidates
        ↓
trainable policy
        ↓
selected operation + target
        ↓
bounded transition
        ↓
outcome / cost
        ↓
learning update
```

Its narrow action set was:

```text
EXPAND(target)
STOP
```

This demonstrated transferable learned operation selection, not full Ground 0 cognition.

## Ground 0 Target Flow

The next live cognitive path should preserve these distinct stages:

```text
legitimate live CognitiveState
        ↓
BROAD CANDIDATE / KNOWLEDGE FIELD
        ↓
learned context / operation routing
        ↓
REVERSIBLE SOFT TAPER
        ↓
checkpoint: what remains strongly active?
        ↓
SMALL SERIOUS-CANDIDATE FIELD
        ↓
STATE-DEPENDENT RECURRENCE
        ↓
checkpoint: how did candidates change one another?
        ↓
EVIDENCE / UNCERTAINTY STATE
        ↓
COMMIT | ABSTAIN | SEEK EVIDENCE | REOPEN
        ↓
checkpoint
        ↓
runtime sequences result
        ↓
OrganismState / trace
        ↓
UI
```

## Critical Separation

Taper and recurrence are different jobs.

```text
Taper:
Which candidates still deserve serious compute?

Recurrence:
How do the surviving serious alternatives alter one another's support?

Commitment:
Is the evidence sufficient to act?
```

HCT-2 showed why this separation matters: removing recurrence reduced good behavior to 45% even though the correct candidate survived tapering 100% of the time.

## Reopening Flow

Suppression must remain reversible:

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

Hard Top-K is not the Ground 0 default because HCT-1 and HCT-2 both showed that irreversible deletion failed context-reversal cases.

## Optional Reliability Flow

Historical evidence/pathway reliability may modify support when useful:

```text
source / pathway history
        ↓
learned reliability or resistance
        ↓
modulated evidence influence
```

This is optional. HCT-2 did not require learned resistance for full good behavior.

## Ownership Rule

```text
cognition / learning owners
    choose and learn cognitive work

runtime
    sequences handoffs only

interfaces
    transport only

UI
    observation / control only

experiments
    hidden truth / scientific scoring only
```

The HCT generator, hidden correct identity, and frozen scientific scorer must never become production cognition inputs.
