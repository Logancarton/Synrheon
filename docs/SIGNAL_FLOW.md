# Synrheon Signal Flow — Revision 6

This file distinguishes what is live now from what is being built and what remains a scientific target.

## Current live flow

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
- injected Internal Thought becomes ordered `injected` experience;
- time, sequence, episode identity, and provenance are preserved;
- `CognitiveSubstrate` now contains a `TokenDeck`;
- runtime sequences and routes;
- UI observes and controls;
- raw chat is not yet automatically segmented into Token Deck observations;
- Ground 0 contextual search is not yet live-integrated.

## Representation path being built

Current built representation:

```text
explicit TokenDeck API
        ↓
stable token identity
        ↓
surface forms / aliases / provenance
        ↓
multiple candidate senses
        ↓
reversible context-conditioned sense activation
```

Immediate next path — TD-3:

```text
raw text
        ↓
exact surface segmenter
        ↓
spans + character offsets + normalized lookup forms
        ↓
TokenDeck observe/reuse
```

TD-3 is intentionally surface-only. It must not choose meaning, sense, concept, or answer.

Future representation path:

```text
surface segments
        ↓
known / unknown acquisition boundary
        ↓
possible senses
        ↓
contextual sense evidence
        ↓
concept / entity links
        ↓
event / semantic-role candidates
        ↓
durable memory
```

## Candidate-source path

The reversible candidate field is already built but cannot be declared live until a legitimate broad source exists.

Target path:

```text
question / current cognitive need
        ↓
Token/sense/event representation
        ↓
memory + concept retrieval
        ↓
opaque candidate IDs + provenance + initial support
        ↓
ReversibleCandidateField
```

Do not insert planted correct identities or experiment qrels into this production handoff.

## Reversible candidate-state flow

Owner:

```text
contextual_search.py
```

Mechanics:

```text
broad retrieval prior
        ↓
complete candidate activation field
        ↓
active expensive-compute region
+ dormant recoverable region
        ↓
context transition checkpoint
        ↓
carry | reset/re-anchor | residual/transform | reopen
        ↓
new complete reversible state
```

D6 adds a critical rule:

> The previous settled state is not automatically the correct prior for changed context.

The transition mode must be explicit and later learned/tested rather than silently defaulting to carry.

## Ground 0 target cognitive flow

```text
QUESTION / UNRESOLVED STATE
        ↓
LEGITIMATE BROAD CANDIDATE FIELD
        ↓
which context operation could discriminate what remains unresolved?
        ↓
EXPLICIT CONTEXT TRANSITION
        ↓
REVERSIBLE CONTEXTUAL SETTLING
        ↓
what remains unresolved now?
        ↓
more refinement worth compute?
  ├─ no  -> evidence sufficiency
  └─ yes -> another earned context operation
        ↓
optional recurrence only if separately earned
        ↓
EVIDENCE SUFFICIENCY
        ↓
COMMIT | ABSTAIN | SEEK EVIDENCE | REOPEN
        ↓
runtime sequences result
        ↓
state / trace
        ↓
UI
```

Multiple contextual stages are not assumed. MT-1 must determine whether more than one soft stage adds value over one good soft stage once transition-state persistence is controlled.

## D6 scientific flow — completed

```text
A  BM25/full-query anchor
B  one full-context soft taper
C  partial -> full with carried activation
D  partial -> full with reset
E  partial -> full residual refinement
```

Observed frozen outcome:

```text
92/93 transition-evaluable
reset integrity PASS
R_reset = 1.0
MAJOR_PERSISTENCE_CONTRIBUTION_SUPPORTED
```

D6 establishes a transition diagnosis, not multi-stage necessity.

## MT-1 scientific target flow

Before result-bearing implementation:

```text
write/freeze MT-1 preregistration
        ↓
implement exact frozen conditions
        ↓
integrity tests
        ↓
synthetic smoke = not evidence
        ↓
allowed development assay
        ↓
paired/matched-compute interpretation
```

Conceptual comparisons:

```text
retrieval/no-taper anchor
single soft
multi-soft naive carry          # pathology control
multi-soft controlled reset
scrambled/reversed order
matched-compute hard stages
```

Recurrence and Token Deck features stay outside the primary MT-1 comparison unless explicitly frozen into the experiment before results.

## Historical E011 donor flow

E011-A remains a useful controlled donor mechanism:

```text
revealed CognitiveState
        ↓
policy.py scores valid operation + target candidates
        ↓
selected operation + target
        ↓
bounded controlled transition
        ↓
outcome / cost
        ↓
policy_learning.py update
```

This is historical evidence that action preference can be learned. It is not the active live integration target and does not define current Ground 0.

## Ownership rule

```text
token_deck.py
    lexical/sense identity + reversible sense state

contextual_search.py
    reversible broad candidate field + context transitions

cognition.py
    Ground 0 public cognitive contracts

state.py
    explicit organism/substrate state

temporal.py + experience.py
    time, sequence, provenance, ordered experience

policy.py + policy_learning.py
    historical E011 donor mechanism

runtime.py
    sequences handoffs only

dev_server.py
    transport only

UI
    observation/control only

experiments/
    qrels / hidden truth / scientific scoring only
```

## Development feedback loop

```text
stimulus or experiment
        ↓
observable state / raw metrics
        ↓
where did the process fail?
        ↓
fix correct owner / transition / representation
        ↓
add regression or falsification record
        ↓
repeat with harder case
```

The UI should expose state and failures; it must not choose the cognitive solution.
