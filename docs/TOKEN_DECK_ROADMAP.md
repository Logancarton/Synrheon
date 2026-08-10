# Synrheon Token Deck Roadmap — Revision 6

**Parallel representation track**

The Token Deck is the production-facing representational layer that lets Synrheon preserve stable internal language units without collapsing words, meanings, concepts, entities, and experiences into the same thing.

It remains scientifically separate from MT-1. Token Deck work must not change frozen MT-1 conditions, channels, thresholds, or evaluation data unless a later experiment explicitly preregisters that integration.

## Core invariant

```text
surface form != token identity != sense != concept/entity != episode
```

Example:

```text
surface: "bank"
        ↓
stable token card
        ↓
possible senses:
    financial institution
    river edge
    aircraft turn
        ↓
context changes sense activation
        ↓
non-leading senses remain recoverable
```

D6 reinforces the general state principle used here: settled state is context-conditional. A weak sense in one context must not be permanently deleted merely because another sense currently dominates.

## What the Token Deck owns

```text
stable token IDs
surface forms and explicit aliases
open-ended morphology metadata
multiple possible senses
sense type metadata
optional links from senses to concepts/entities
provenance / evidence IDs
usage history
context-conditioned sense activation
reversible sense checkpoints
```

It does not own:

```text
truth
natural-language generation
world relations
memory truth
retrieval ranking
Ground 0 commitment
hidden LLM authority
a fixed semantic ontology
```

## Current status

```text
TD-0 stable token-card contract             BUILT
TD-1 multiple reversible senses             BUILT
TD-2 alias/morphology storage               BUILT — non-inferential
TD-3 exact surface segmentation             NEXT
TD-4 known/unknown acquisition              NOT STARTED
TD-5 contextual sense disambiguation        NOT STARTED
TD-6 concept/entity bridge                  CONTRACT BEGUN; BEHAVIOR NOT STARTED
TD-7 event/semantic-role composition        NOT STARTED
TD-8 durable Token Deck                     NOT STARTED
TD-9 candidate-source bridge                NOT STARTED
TD-10 learned vocabulary growth             NOT STARTED
```

Current owner:

```text
src/synrheon/token_deck.py
```

Current substrate integration:

```text
CognitiveSubstrate.token_deck
```

## TD-0 — stable token-card contract

Status: **BUILT**

Current behavior:

- repeated observations of the same normalized form reuse one stable token identity;
- original observed forms remain preserved;
- provenance is recorded;
- token identity remains distinct from sense/concept identity.

Current tests include case-variant reuse such as `Bank` / `bank`.

## TD-1 — multiple senses without destructive commitment

Status: **BUILT**

One token card may hold multiple candidate senses. Context may change support among them without deleting alternatives.

```text
BANK
  financial sense
  river sense

financial context
  financial ↑
  river ↓ but remains

river context
  river ↑
  financial ↓ but remains
```

Adding a newly discovered sense reopens the current sense inventory rather than assigning the new sense permanent zero support.

## TD-2 — alias and morphology storage

Status: **BUILT AS STORAGE ONLY**

Explicit related forms can share a token identity when registered with provenance.

Example:

```text
run / ran
```

Morphology metadata may be stored, but automatic lemmatization or morphological inference is not yet cognitive truth.

## TD-3 — exact surface segmentation

Status: **NEXT BUILD**

Goal:

Convert raw input into observable surface spans while preserving exact original text and character offsets.

Required output should include at least:

```text
original text
ordered surface spans
start/end character offsets
exact span text
normalized lookup form when applicable
surface category metadata only when mechanically observable
```

TD-3 must not decide meaning.

It must not:

```text
select a sense
fabricate a concept/entity
infer truth
force part of speech
call an LLM to decide what a span means
silently discard punctuation or offset provenance
```

First adversarial stimulus set should include:

```text
Daisy ran to the door.
Daisy's running.
Don't open the door.
The well-known doctor arrived at 8:30.
I paid $12.50.
Logan said, "Daisy isn't outside."
email@example.com
A/B testing improved 3.5%.
BANK Bank bank
```

Verification should prove that spans can be traced back to the exact source string.

The segmenter should be replaceable later without invalidating stable token/sense identities.

## TD-4 — known / unknown acquisition boundary

Status: **NOT STARTED**

After segmentation, each relevant surface form asks whether Synrheon already has a usable representation.

```text
surface span
    ↓
known token?
    ├─ yes -> retrieve existing senses / evidence
    └─ no  -> classify acquisition need
               ├─ likely name/entity
               ├─ morphology/variant candidate
               ├─ ordinary unknown word
               ├─ number/symbol/code
               └─ unresolved
```

Names/entities must not automatically be treated as dictionary words.

External dictionary/parser/LLM assistance may later propose candidates with provenance. Proposal is not truth.

## TD-5 — contextual sense disambiguation

Status: **NOT STARTED; SCIENTIFIC EXPERIMENT REQUIRED**

Goal:

Learn which visible contextual evidence changes support among known senses.

Required evaluation:

```text
simple frequency/default-sense baseline
held-out contexts
ambiguous cases where abstention is correct
context reversals
preservation/reactivation of initially suppressed senses
no answer identity in routing
raw per-case failures
```

A learned disambiguator should output evidence/support over senses, not overwrite the sense inventory.

Example families:

```text
I deposited money at the bank.
We sat beside the bank and watched the ducks.

The bat flew from the cave.
He swung the bat at the ball.

She booked a room.
I read the book.
```

## TD-6 — concept and entity bridge

Status: **CONTRACT BEGUN; BEHAVIOR NOT STARTED**

A sense may optionally point to a stable concept/entity identity without equating lexical identity with world identity.

```text
surface "Daisy"
    ↓
token card
    ↓
entity sense
    ↓
Concept / Entity: Daisy
```

Different words may eventually link to the same concept. One word may link to multiple concepts through different senses.

## TD-7 — event / semantic-role composition

Status: **NOT STARTED**

Goal:

Compose active token/sense evidence into structured event candidates such as:

```text
actor
action
object
destination
ownership / self relation
time
negation
modification
provenance
```

Do not hard-code one universal semantic representation. The first assay should compare explicit role/event structure against a simpler token/sense baseline on a task where event structure should matter.

## TD-8 — durable Token Deck

Status: **NOT STARTED**

Persist across sessions:

```text
token cards
surface forms / aliases
senses
provenance
morphology
concept links
usage statistics
learned sense evidence
```

Requirements include schema versioning, corruption/recovery tests, provenance separation, and safeguards against silent sense merging.

## TD-9 — candidate-source bridge

Status: **NOT STARTED**

This is where representation first directly feeds Ground 0 retrieval.

```text
stimulus
  ↓
Token Deck
  ↓
sense / event representation
  ↓
memory + concept retrieval
  ↓
legitimate broad candidate field
  ↓
ReversibleCandidateField
  ↓
Ground 0 cognition
```

Evaluate against a simpler lexical retrieval baseline. No hidden correct identity may enter candidate construction.

## TD-10 — learned vocabulary growth

Status: **NOT STARTED**

Allow Synrheon to propose and retain new representational distinctions only when they improve something measurable such as prediction, retrieval, compression, transfer, or repeated contextual discrimination.

Potential retained objects:

```text
new sense
new alias/morphology link
new concept link
new higher-order token/chunk
new relation between representations
```

Creation frequency is not evidence of usefulness.

## Development workflow for the Token Deck

Use progressively harder stimulus testing:

```text
build one representational capability
        ↓
feed explicit text stimuli
        ↓
inspect exact backend-owned representation
        ↓
locate failure in segmentation / identity / sense / provenance
        ↓
fix the process
        ↓
add failure as regression test
        ↓
advance to harder stimuli
```

Never fix one sentence by adding a sentence-specific branch.

## Relationship to MT-1

The tracks remain separate:

```text
GROUND 0 SCIENCE
D6 result -> MT-1 preregistration -> matched-compute stage test

REPRESENTATION
TD-0/1/2 -> TD-3 segmentation -> TD-4 acquisition -> TD-5 sense learning
```

Token Deck improvements must not be used to rescue or reinterpret MT-1 after its criteria are frozen.

## Near-term completion gate

The representation track moves past TD-3 only when:

- exact source text is preserved;
- spans and offsets are deterministic under the frozen segmenter version;
- punctuation/contractions/names/numbers/symbols have explicit tests;
- no meaning inference leaks into segmentation;
- failures from stimulus testing become regression tests;
- Token Deck identity remains stable independent of the segmenter's implementation details.
