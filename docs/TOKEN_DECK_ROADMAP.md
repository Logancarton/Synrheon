# Synrheon Token Deck Roadmap

**Parallel architecture track — Revision 5**

The Token Deck is the production-facing representational layer that will let Synrheon preserve stable internal language units without collapsing words, meanings, concepts, entities, and experiences into the same thing.

It is deliberately separate from the D6 / MT-1 retrieval experiments. Token Deck work must not change the frozen retrieval conditions, channels, thresholds, or evaluation data unless a later experiment explicitly preregisters that integration.

## Core invariant

```text
surface form != token identity != sense != concept/entity != episode
```

Example:

```text
surface: "bank"
        ↓
stable token card: BANK
        ↓
possible senses:
    financial institution
    river edge
    aircraft turn
        ↓
context may change activation among senses
        ↓
non-selected senses remain recoverable
```

The Token Deck should apply the same general lesson now supported by D6: a settled state is conditional on its context. A sense that is weak in one context must not be permanently deleted merely because another sense currently dominates.

## What the Token Deck owns

The Token Deck may own:

```text
stable token IDs
surface forms and aliases
open-ended morphology metadata
multiple possible senses
sense type metadata
optional links from senses to concepts/entities
provenance / evidence event IDs
usage history
context-conditioned sense activation
reversible sense checkpoints
```

It does **not** own:

```text
truth
natural-language generation
LLM reasoning
a hard-coded semantic ontology
forced part-of-speech decisions
world relations
memory truth
retrieval ranking
Ground 0 commitment
```

## Build philosophy

The Token Deck should begin as cognitive physics, not as a hand-written English expert.

```text
we provide stable representational rules
        ↓
Synrheon later learns / acquires linguistic skill
```

A dictionary, thesaurus, parser, or LLM may eventually provide bounded evidence, but external helpers must not silently become the owner of token identity, sense truth, or cognition.

## TD-0 — Stable token-card contract

Status: **BEGIN NOW**

Goal:

- repeated observation of the same normalized surface form reuses one stable token identity;
- original surface forms remain preserved;
- each observation preserves provenance;
- token identity remains distinct from any concept or sense identity.

Pass examples:

```text
"Bank" + "bank" -> same stable token card
same surface observed later -> same token ID
provenance events remain inspectable
```

Failure:

- duplicate token identities for the same registered form without an explicit split;
- token ID being treated as a concept ID;
- loss of the original observed form or evidence event.

## TD-1 — Multiple senses without destructive commitment

Status: **BEGIN NOW**

Goal:

One token card may hold several candidate senses. Context can alter their activation without deleting alternatives.

Required behavior:

```text
BANK
  financial sense
  river-edge sense

financial context
  financial ↑
  river ↓ but preserved

river context
  river ↑
  financial ↓ but preserved
```

Adding a newly discovered sense must not silently assign it permanent zero probability because an earlier context settled before that sense existed.

## TD-2 — Alias and morphology storage

Status: **BEGIN NOW AS STORAGE ONLY**

Goal:

Represent related observed forms without pretending Synrheon already knows how to infer morphology.

Examples:

```text
run / runs / ran / running
child / children
```

The first implementation may store explicit morphology metadata and aliases. Automatic lemmatization or morphological inference must be tested separately before becoming cognitive behavior.

## TD-3 — Surface segmentation

Status: **NOT STARTED**

Goal:

Convert raw input into observable surface spans while preserving exact input and offsets.

Requirements:

- punctuation and whitespace handling must be explicit;
- segmentation must not decide meaning;
- exact original text must remain available;
- contractions, hyphenation, numbers, symbols, and names need tests.

The system should be able to replace the first segmenter later without invalidating stable token/sense identity.

## TD-4 — Known / unknown acquisition boundary

Status: **NOT STARTED**

Goal:

For each surface form, determine whether Synrheon already has a usable token/sense representation before asking an outside source.

Possible flow:

```text
surface form
    ↓
known token?
    yes -> retrieve existing senses
    no  -> classify acquisition need
              ↓
          possible entity/name
          morphology/variant
          ordinary unknown word
          symbol/code/number
```

Names/entities should not automatically be sent through a dictionary-definition pathway. External dictionary/LLM assistance may later propose candidates, but proposals must retain source provenance and remain distinguishable from Synrheon-learned structure.

## TD-5 — Contextual sense disambiguation

Status: **NOT STARTED**

Goal:

Learn which visible contextual evidence changes support among known senses.

This is where the Token Deck begins connecting to the broader contextual-settling research.

Scientific requirement:

- compare against simple frequency/default-sense baselines;
- use held-out contexts;
- include ambiguous cases where abstention is correct;
- include context reversals;
- preserve initially suppressed senses;
- do not use answer identity in routing.

A learned disambiguator should output evidence/activation over senses, not overwrite the sense inventory.

## TD-6 — Concept and entity bridge

Status: **CONTRACT BEGINS IN TD-0/1; BEHAVIOR NOT STARTED**

Goal:

Allow a sense to point to a stable `Concept` or entity identity without making lexical identity and world identity equivalent.

Example:

```text
surface "Daisy"
    ↓
token card
    ↓
entity sense
    ↓
concept/entity ID for Daisy
```

Different words may link to the same concept; one word may link to multiple concepts/senses.

## TD-7 — Event / semantic-role composition

Status: **NOT STARTED**

Goal:

Compose active token senses into structured event candidates such as:

```text
actor
action
object
destination
ownership/self relation
time
negation
modification
provenance
```

Do not hard-code this as the only possible semantic representation. The first assay should test whether explicit role structure improves recall/prediction over a bag of token senses.

## TD-8 — Durable Token Deck

Status: **NOT STARTED**

Goal:

Persist token cards, senses, provenance, morphology, concept links, and learned use statistics across sessions.

Requirements:

- schema versioning;
- injected vs observed vs learned provenance remains separate;
- no session reset deletes durable token identity;
- corruption/recovery tests;
- consolidation cannot silently merge distinct senses.

## TD-9 — Candidate-source bridge

Status: **NOT STARTED**

Goal:

Use token/sense/event state as one legitimate source of query/context representation for memory retrieval and the `ReversibleCandidateField`.

```text
stimulus
  ↓
Token Deck
  ↓
active sense / event candidates
  ↓
memory + concept retrieval
  ↓
broad candidate field
  ↓
Ground 0 contextual cognition
```

This is the first point where Token Deck output should directly influence broad retrieval. It must be evaluated against a simpler lexical retrieval baseline.

## TD-10 — Learned vocabulary growth

Status: **NOT STARTED**

Goal:

Let Synrheon propose and retain new internal distinctions only when they improve prediction, retrieval, compression, transfer, or repeated contextual discrimination.

Potential retained objects:

```text
new sense
new alias/morphology link
new concept link
new higher-order token/chunk
new relation between representations
```

Creation frequency alone is not evidence that a representation is useful.

## First implementation slice

Build only TD-0 through the non-inferential portions of TD-2:

```text
TokenDeck
  ↓
stable token cards
  ↓
surface aliases
  ↓
provenance
  ↓
multiple sense records
  ↓
optional concept links
  ↓
context-conditioned reversible sense activation
  ↓
checkpoint / restore
```

Do not automatically tokenize incoming chat yet. The runtime should not pretend to understand language until a segmentation/acquisition path has its own tests.

## First verification set

The first unit tests should establish:

1. repeated surface observations reuse stable token identity;
2. alias forms can map to the same token explicitly;
3. one token can retain multiple senses;
4. context can reverse the leading sense without deleting the alternative;
5. restoring a checkpoint restores the earlier sense state;
6. adding a new sense after prior settling reopens the sense field rather than assigning the new sense permanent zero support;
7. concept links remain optional and distinct from token identity;
8. provenance remains inspectable.

## Parallel relationship to MT-1

Token Deck development can proceed while MT-1 is designed, but the tracks remain scientifically separate:

```text
Ground 0 track:
D6 result -> MT-1 preregistration -> matched-compute multi-taper test

Representation track:
TD-0/1/2 -> segmentation -> acquisition -> contextual sense learning
```

A later experiment may deliberately connect them. Until then, Token Deck improvements must not be used to rescue or reinterpret MT-1.