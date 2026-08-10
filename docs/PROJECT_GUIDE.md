# Synrheon Project Guide — Revision 6 Plain English

This is the owner's short map of what Synrheon is, what has actually been learned, what is built, and what should happen next.

Always separate:

```text
scientific evidence
from
implementation maturity
```

A mechanism can have meaningful scientific evidence while still being only `Built`, not live.

## What Synrheon is trying to become

Synrheon is exploring whether a persistent cognitive system can:

```text
keep a very large field of possible knowledge available
        ↓
focus computation where the current question needs more detail
        ↓
preserve weaker alternatives instead of deleting them
        ↓
change or reopen internal state when context changes
        ↓
learn which cognitive operations are worth using
        ↓
remember experiences with provenance
        ↓
stop only when evidence is sufficient
```

The architecture is not treated as proven. Each major piece must earn its place.

## The most important new result — D6

Revision 5 suspected that Synrheon was damaging retrieval because a partial-context state was being carried too strongly into later full context.

D6 tested that directly on the frozen SciFact development partition.

Observed:

```text
93 development queries
92 transition-evaluable
reset control integrity: PASS
R_reset = 1.0
verdict: MAJOR_PERSISTENCE_CONTRIBUTION_SUPPORTED
```

Plain English:

> When Synrheon first settled under incomplete context and blindly carried that settled state forward, performance could collapse. Resetting/re-anchoring before processing the changed context recovered the measured transition damage under the frozen diagnostic.

The lesson is **not** "always reset." The lesson is that previous settled state is conditional on the context that produced it. The future system needs to learn/test when to carry, reset, transform, or reopen.

D6 does not prove that several taper stages are useful. That is what MT-1 must test next.

## Current Ground 0 working idea

```text
question / unresolved need
        ↓
broad legitimate candidate field
        ↓
choose context that may discriminate the remaining alternatives
        ↓
explicit transition of prior state
        ↓
reversible contextual settling
        ↓
what is still unresolved?
        ↓
optional more refinement / optional recurrence if it earns value
        ↓
evidence sufficient?
        ↓
commit | abstain | seek evidence | reopen
```

Ground 0 is a research program, not a completed production cognition engine.

## Current two-track workflow

Synrheon now develops on two tracks at the same time.

### Track A — scientific cognition testing

```text
D6 completed
    ↓
MT-1 preregistration
    ↓
MT-1 matched-compute experiment
```

MT-1 asks a very specific question:

> Once the known carry-state problem is controlled, do multiple soft contextual settling stages actually outperform one good soft stage?

If the answer is no, we remove multi-stage necessity from the architecture. Hard pruning losing is not enough to save multi-stage tapering.

### Track B — representation / Token Deck

```text
TD-0 stable token identity          Built
TD-1 multiple reversible senses     Built
TD-2 morphology/alias storage       Built
TD-3 surface segmentation           Next
TD-4 known/unknown routing          Later
TD-5 contextual sense learning      Later experiment
```

The Token Deck gives Synrheon stable internal pieces to eventually think with.

Core separation:

```text
surface word != token != sense != concept/entity != memory episode
```

For example, `bank` can be one stable token card while keeping financial-bank and river-bank as different possible senses. Context can change which sense is stronger without deleting the other.

## Why a Token Deck matters

Raw text is not a good long-term cognitive substrate. Synrheon needs stable reusable identities so language can later connect to concepts, entities, events, memory, and retrieval.

The intended path is:

```text
raw language
   ↓
surface segmentation
   ↓
Token Deck
   ↓
possible senses
   ↓
concepts / entities / event structure
   ↓
durable memory
   ↓
retrieval
   ↓
broad candidate field
   ↓
Ground 0 cognition
```

The Token Deck itself is not language understanding. It is the representational foundation for later learning/testing.

## What exists today

```text
observable runtime + development UI       Verified
computational time                        Integrated
ordered experience + provenance           Integrated
cognitive substrate                       Built
Token Deck TD-0/1/2                       Built
reversible candidate field                Built
E011-A learned action policy              Built experimentally / historical donor
TD-3 segmenter                            Not Started
Ground 0 live contextual cognition        Not Integrated
Durable memory                            Not Started
Learned retrieval                         Not Started
Recursive autonomous cognition            Not Started
```

## Current live flow

```text
Chat / injected internal thought
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

The Token Deck is stored inside the cognitive substrate, but normal chat does not yet automatically pass through a real surface segmenter into token observations.

The reversible candidate field is also not live-integrated because Synrheon does not yet have a legitimate broad memory/retrieval source to feed it.

## Source ownership

```text
state.py
    organism/substrate state; contains TokenDeck

cognition.py
    Ground 0 public cognitive contracts

contextual_search.py
    reversible candidate field and context-transition checkpoints

token_deck.py
    stable token identity, senses, provenance, reversible sense state

policy.py / policy_learning.py
    retained E011-A donor mechanism and learning

experience.py
    ordered current-episode experience + provenance

temporal.py
    computational time and sequence

runtime.py
    traffic controller only

dev_server.py
    browser/API transport only

experiments/
    scientific laboratory; hidden qrels/scorers stay here

ui/
    microscope / controls only
```

## How development should work now

For science:

```text
question
  ↓
state what would falsify it
  ↓
preregister controls/metrics/thresholds
  ↓
commit preregistration
  ↓
build
  ↓
integrity/smoke test
  ↓
allowed evidence run
  ↓
apply frozen interpretation
  ↓
change architecture if needed
```

For organism capabilities:

```text
build one capability
  ↓
give Synrheon explicit stimuli
  ↓
inspect exact internal state
  ↓
find where the process failed
  ↓
fix the process, not the phrase
  ↓
add regression test
  ↓
try harder stimuli
```

This is the main workflow going forward.

## Immediate next work

### Scientific

Write and freeze MT-1 before building result-bearing MT-1 behavior.

The conceptual comparison should include:

```text
retrieval/no-taper anchor
single soft
multi-soft with naive carry
multi-soft with controlled reset
scrambled/reversed order
matched-compute hard stages
```

Recurrence and Token Deck features should stay out of the primary MT-1 test unless explicitly frozen into a new version before results.

### Architecture

Build TD-3 exact surface segmentation.

The first version should preserve:

```text
exact raw text
surface spans
character offsets
normalized lookup forms
```

It should **not** decide meaning yet.

Test with things like:

```text
Daisy ran to the door.
Daisy's running.
Don't open the door.
The well-known doctor arrived at 8:30.
I paid $12.50.
Logan said, "Daisy isn't outside."
```

Then inspect the actual spans/offsets and turn every failure into a process-level regression test.

## Important scientific guardrails

1. Never change a frozen pass criterion after seeing the result just to make a mechanism win.
2. Preserve failed experiments and unexpected cases.
3. Hidden correct answers/qrels may exist in `experiments/` for scoring but must not enter production cognition.
4. Match compute when claiming a mechanism is better or more efficient.
5. Do not describe development-set findings as untouched final confirmation.
6. Do not claim a mechanism is live because an isolated test passes.
7. Do not patch individual phrases when the general process is wrong.
8. Keep Token Deck work independent from MT-1 until an experiment intentionally combines them.

## Documents to read first

Current truth:

```text
REV6_CONTINUATION_STATE.md
CURRENT_STAGE.md
IMPLEMENTATION_STATUS.md
ARCHITECTURE_PLAN.md
TOKEN_DECK_ROADMAP.md
```

Plain-English and signal maps:

```text
PROJECT_GUIDE.md
SIGNAL_FLOW.md
SCAFFOLD.md
```

Frozen/historical scientific records remain useful, but older Revision 4/5 theory does not override Revision 6 continuation state.
