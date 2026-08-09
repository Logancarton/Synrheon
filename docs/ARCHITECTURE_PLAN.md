# Synrheon Architecture Plan

## Ground 0 — Architectural Baseline

Ground 0 is the current experimentally reinforced computational process that future Synrheon cognition should implement, challenge, or improve.

```text
VERY LARGE KNOWLEDGE / CANDIDATE FIELD
        ↓
learned context routing
        ↓
ordered reversible soft tapering
        ↓
TRACTABLE SERIOUS-CANDIDATE FIELD
        ↓
state-dependent recurrent deliberation
        ↓
evidence + uncertainty
        ↓
COMMIT | ABSTAIN | SEEK EVIDENCE | REOPEN
```

Learned pathway resistance is an optional modifier, not a required Ground 0 component. It produced strong earlier synthetic results but was unnecessary in HCT-2.

Ground 0 is a **research foundation**, not a claim that this path is already live-integrated.

## Why This Is Ground 0

```text
clock-driven progressive Top-K     failed
confidence-only narrowing          limited
stochastic consensus               produced false certainty
hard irreversible deletion         failed context reversal
reversible soft taper              reinforced
learned ordered sparse taper       efficiency advantage reinforced
state-dependent recurrence         strongly supported by ablation
explicit abstention / reopening    reinforced
```

The purpose of future architecture is no longer to invent a cognitive route from scratch. It is to express, generalize, train, and falsify this reinforced process inside the persistent organism.

## Core Architectural Principle

> **We code the cognitive physics. Synrheon learns the cognitive skill.**

Designed cognitive physics may define:

```text
state and candidate schemas
valid cognitive operation interfaces
reversible suppression mechanics
recurrent transition mechanics
hard resource / safety ceilings
checkpoint and provenance formats
commit / abstain / reopen interfaces
validation and persistence boundaries
```

Learned cognitive skill should increasingly determine:

```text
which context matters
which context to evaluate next
stage order
stage gain / selectivity
candidate-region preference
which cognitive operation + target to choose
when recurrence is worth more compute
when evidence is sufficient
when to seek more evidence
when to reopen broader context
```

## Ground 0 Computational Responsibilities

### Candidate field

Synrheon needs an explicit or representable field of currently plausible knowledge, memories, hypotheses, goals, or operations. Expensive reasoning should not operate over the whole field by default.

### Learned context routing

Context should not be a permanently hand-written sequence. HCT-2 supports learning a useful order as an efficiency mechanism when context is hierarchical and conditional.

### Reversible sparse taper

```text
suppressed ≠ deleted
```

A low-activation candidate may become important after new evidence or context change. HCT-1/HCT-2 reversal tests support this over hard deletion.

### Recurrent deliberation

Once the field is small enough, serious candidates may interact through recurrent excitation/inhibition or another state-dependent relational process. HCT-2 showed that removing recurrence reduced good behavior to 45% even though correct-candidate survival remained 100%.

Taper and recurrence therefore remain separate architectural responsibilities.

### Commitment

```text
winner ≠ sufficient evidence
```

Commitment must allow at least:

```text
COMMIT
ABSTAIN
SEEK DISCRIMINATING EVIDENCE
REOPEN BROADER CONTEXT
```

### Optional reliability learning

Historical source/pathway reliability may modify evidence flow when a task actually benefits from it. Do not make learned resistance universal by assumption.

## Relationship to Existing E011 Work

E011-A proved a separate but compatible principle: a model can learn which valid cognitive operation/target to choose from visible state and transfer that preference across unseen and renamed worlds.

Its implementation now lives in:

```text
policy.py
policy_learning.py
```

Its `EXPAND(target)` / `STOP` task is narrower than Ground 0, so it is a donor mechanism rather than the architecture itself.

## Production Ownership Now

The source tree should contain real implementation, not roadmap placeholders.

`state.py`  
Explicit organism/world state, concepts, relations, activation, stimuli, and trace records.

`cognition.py`  
Ground 0 cognitive-cycle contract and future production cognition owner. It currently defines observable process checkpoints; the actual HCT mechanism is not yet integrated.

`policy.py`  
Retained E011-A trainable operation/target policy primitives.

`policy_learning.py`  
Outcome-driven updates for the retained policy.

`temporal.py`  
Computational time and event coordinates.

`experience.py`  
Ordered current-episode autobiographical experience and provenance.

`runtime.py`  
Thin sequencing only; never owns candidate preference or answer selection.

`dev_server.py`  
Local browser/API transport only.

`ui/`  
Observation/control only.

`experiments/`  
Scientific generators, hidden truth, scoring, and falsification assays only.

A small compatibility export remains in `learning.py` for the frozen E011-A experiment. New code should use `policy_learning.py` directly. `cognition.py` also temporarily re-exports the E011 policy classes so the frozen experiment remains reproducible while the real ownership has moved to `policy.py`.

## Future Capabilities Do Not Get Empty Source Files

Durable memory, retrieval, scratchpad cognition, problem/trial learning, consolidation, abstraction, and autonomy remain planned architecture. Their former placeholder-only source files were removed.

A new source owner should be created only when implementation exists and its responsibility is clear.

```text
planned capability
        ↓
architecture / experiment proves need
        ↓
real implementation appears
        ↓
source owner earns a file
```

## Next Live Architecture Slice

Build the smallest observable production path that contains the essential Ground 0 separation:

```text
live state
        ↓
construct legitimate broad candidate field
        ↓
select context / operation from visible state
        ↓
reversible taper checkpoint
        ↓
small recurrent field
        ↓
one or more bounded recurrent transitions
        ↓
commit / abstain / reopen checkpoint
        ↓
runtime sequences handoff
        ↓
state / trace
        ↓
UI
```

The first implementation does not need natural-language semantics or the entire HCT synthetic mechanism. It must preserve the functional contracts and make every stage observable.

## Development Dependency Order From Ground 0

```text
Ground 0 integration contract
        ↓
observable candidate/taper/recurrent/commit checkpoints
        ↓
live learned routing
        ↓
durable memory
        ↓
learned sparse retrieval
        ↓
recursive working-state cognition
        ↓
problem / trial / revision learning
        ↓
consolidation + abstraction
        ↓
broader multi-layer training
        ↓
autonomous continuation
        ↓
external tools / intelligence
```

The order may change if experiments show a missing prerequisite.

## Scientific Development Rule

Every major mechanism should have:

```text
hypothesis
baseline / control
frozen evaluation boundary
failure condition
ablation where possible
identity/leakage safeguards
observable production boundary if integrated
```

Do not preserve a mechanism because it is elegant. Preserve it because it repeatedly earns a role.

## Generalization Ladder

```text
Level 0 — training fit
Level 1 — identity / instance transfer
Level 2 — structural transfer
Level 3 — compositional transfer
```

HCT-1/HCT-2 provide controlled synthetic evidence for structural process properties, not natural-language or real-world general intelligence.

The next scientific extension should attack generality across changed world structures rather than simply enlarge HCT-2.
