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

The architecture is grounded in the experimental sequence, including failures:

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

The purpose of future architecture is no longer to invent a cognitive route from scratch. It is to determine how to express, generalize, and train this reinforced process inside the persistent organism.

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

### 1. Candidate Field

Synrheon needs an explicit or representable field of currently plausible knowledge, memories, hypotheses, goals, or operations.

The field may be very large, but expensive reasoning should not operate over the whole field by default.

### 2. Learned Context Routing

Context should not be a permanently hand-written sequence.

The system should learn which contextual dimension is useful next from outcome evidence and state structure.

HCT-2 supports learned ordering as an efficiency mechanism when context is hierarchical and conditional.

### 3. Reversible Sparse Taper

Narrowing is provisional.

```text
suppressed ≠ deleted
```

A low-activation candidate may become important after new evidence or context change.

This principle is supported by HCT-1/HCT-2 reversal tests in which hard Top-K could not recover deleted correct candidates while reversible mechanisms could.

### 4. Recurrent Deliberation

Once the field is small enough, serious candidates may interact through recurrent excitation/inhibition or another state-dependent relational process.

HCT-2 showed that removing recurrence reduced good behavior to 45% even though correct-candidate survival remained 100%.

Therefore taper and recurrence should remain distinct architectural responsibilities.

### 5. Commitment

Ranking and knowledge are separate.

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

### 6. Optional Reliability Learning

Historical source/pathway reliability may modify evidence flow when a task actually benefits from it.

Do not make learned resistance universal by assumption. Future experiments should manipulate reliability directly and test whether the component earns its cost.

## Relationship to Existing E011 Work

E011-A proved a separate but compatible principle:

> A model can learn which valid cognitive operation/target to choose from visible state and transfer that preference across unseen and renamed worlds.

This remains useful for Ground 0 because learned context selection, taper selection, recurrence decisions, evidence seeking, and stopping can all eventually be represented as learnable cognitive operations.

However, E011-A's `EXPAND(target)` / `STOP` task is narrower than Ground 0.

Therefore the previous direct E011-B plan is not automatically the next step. Integration should first reconcile the learned policy surface with Ground 0.

## Next Live Architecture Slice

Build the smallest observable production path that contains the essential Ground 0 separation:

```text
live CognitiveState
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
OrganismState / trace
        ↓
UI
```

The first implementation does not need natural language semantics or the entire HCT synthetic mechanism. It must preserve the functional contracts and make every stage observable.

## Production Ownership

`core.py`  
Explicit organism/world state and substrate.

`cognition.py`  
Cognitive-state/action policy and future Ground 0 routing/taper/deliberation ownership unless real complexity justifies splitting owners.

`learning.py`  
Outcome/credit-driven changes to cognitive skill.

`memory.py`  
Future durable evidence store; existence remains separate from activation and route usefulness.

`retrieval.py`  
Future learned retrieval operations and leveled search.

`scratchpad.py`  
Future bounded working state/checkpoints.

`runtime.py`  
Thin sequencing only; never owns candidate preference or answer selection.

`interfaces.py`  
Transport only.

`ui/`  
Observation/control only.

`experiments/`  
Scientific generators, hidden truth, scoring, and falsification assays only.

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
recursive scratchpad cognition
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

Claims should continue to distinguish:

```text
Level 0 — training fit
Level 1 — identity / instance transfer
Level 2 — structural transfer
Level 3 — compositional transfer
```

HCT-1/HCT-2 provide controlled synthetic evidence for structural process properties, not natural-language or real-world general intelligence.

The next scientific extension should attack generality across changed world structures rather than simply enlarge HCT-2.
