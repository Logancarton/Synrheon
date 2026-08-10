# Synrheon Scaffold — Revision 6

This is the compact structural map for the active repository.

Rule:

> **A planned capability does not earn a production source file until real implementation exists and its responsibility is clear.**

## Active production source

```text
src/synrheon/
├── __init__.py
├── __main__.py
├── state.py
├── cognition.py
├── contextual_search.py
├── token_deck.py
├── policy.py
├── policy_learning.py
├── learning.py          # temporary E011-A compatibility export only
├── experience.py
├── temporal.py
├── runtime.py
└── dev_server.py
```

## Ownership

```text
state.py
    explicit organism/substrate state
    owns concepts, world/self relations, activation storage, TokenDeck container

cognition.py
    Ground 0 public cognitive-cycle/checkpoint boundary

contextual_search.py
    complete reversible candidate field
    active/dormant regions
    carry/reset/residual transition provenance
    checkpoint / restore / reopen

token_deck.py
    stable token identity
    surface forms / explicit aliases
    provenance
    multiple recoverable senses
    non-inferential morphology metadata
    context-conditioned reversible sense activation

policy.py
    retained E011-A trainable operation/target donor mechanism

policy_learning.py
    retained E011-A outcome-driven policy learning

learning.py
    temporary compatibility shim for frozen E011-A imports

experience.py
    ordered current-episode autobiographical experience + provenance

temporal.py
    episode/time/sequence coordinates

runtime.py
    thin sequencing only

dev_server.py
    local browser/API transport only
```

## Scientific source

```text
experiments/
├── external_retrieval_cascade.py
├── ext2_diagnostics.py
└── d6_transition_persistence.py
```

Current science continues from D6 into MT-1 specification. MT-1 does not yet earn a source file until its preregistration is frozen.

## Current working architecture

```text
raw stimulus
    ↓
Token Deck representation path            # beginning now
    ↓
concept/entity/event structure             # future
    ↓
durable memory + legitimate retrieval     # future
    ↓
ReversibleCandidateField
    ↓
question-guided context selection
    ↓
explicit context transition
    ↓
reversible settling
    ↓
evidence sufficiency
    ↓
commit | abstain | seek evidence | reopen
```

Multiple contextual stages and recurrence are not guaranteed components. MT-1 and later assays must earn them.

## Current evidence-driven invariants

```text
surface form != token identity != sense != concept/entity != episode
suppressed != deleted
settled activation is context-conditional
winner != sufficient evidence
hidden experimental truth stays outside production cognition
runtime sequences; owners decide
UI observes; it does not choose
```

## Dual-track development map

```text
TRACK A — SCIENCE
D6 completed
    ↓
MT-1 preregistration
    ↓
matched-compute stage-necessity experiment

TRACK B — REPRESENTATION
TD-0/1/2 built
    ↓
TD-3 exact surface segmentation
    ↓
TD-4 known/unknown acquisition
    ↓
TD-5 contextual sense learning
```

Do not let Track B improvements alter Track A after MT-1 is frozen unless a new versioned experiment explicitly combines them.

## Future capabilities without owners yet

These remain planned until real implementation earns an owner:

```text
surface segmenter                    TD-3 next
known/unknown acquisition            TD-4
learned contextual sense selector    TD-5
entity/event composition             later
durable memory                       later
learned retrieval                    later
question/unresolved-state controller later
production multi-taper controller    blocked on MT-1 evidence
production recurrence                must earn task-specific role
commitment calibration               must earn role
problem/trial learning               later
consolidation / abstraction          later
autonomy                             later
```

Do not recreate empty placeholder modules for them.

## Scientific separation

```text
src/synrheon/
    reusable production state/process owners only

experiments/
    benchmark/synthetic harnesses, hidden truth, qrels, scoring, falsification

tests/
    invariant, regression, integration, and scientific-integrity checks

ui/
    observation/control only
```

Hidden experiment truth must never become production cognition input.

## Structural rule

```text
one clear responsibility
        ↓
one understandable owner
        ↓
real complexity appears
        ↓
split only when justified
```

And for new cognitive mechanisms:

```text
claim + falsifier
        ↓
preregister when scientific
        ↓
build smallest reusable owner
        ↓
test behavior
        ↓
keep only what earns its role
```
