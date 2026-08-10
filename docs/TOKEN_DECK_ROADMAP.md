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
TD-3 exact surface segmentation             BUILT + INTEGRATED — not yet Verified
TD-4 known/unknown acquisition              BUILT + INTEGRATED — not yet Verified
TD-5 contextual sense disambiguation        NEXT — SCIENTIFIC EXPERIMENT
TD-6 concept/entity bridge                  CONTRACT BEGUN; BEHAVIOR NOT STARTED
TD-7 event/semantic-role composition        NOT STARTED
TD-8 durable Token Deck                     NOT STARTED
TD-9 candidate-source bridge                NOT STARTED
TD-10 learned vocabulary growth             NOT STARTED
```

Current owners:

```text
src/synrheon/token_deck.py            token/sense identity and reversible sense state
src/synrheon/surface_segmentation.py  TD-3 exact surface observation
src/synrheon/acquisition_routing.py   TD-4 known/unknown routing; read-only
```

Current substrate integration:

```text
CognitiveSubstrate.token_deck         identity storage
StimulusRecord.segmentation           TD-3 observation of each live stimulus
StimulusRecord.acquisition            TD-4 routing of each live stimulus
```

Identity and observation are deliberately separate owners: the segmenter assigns no token
ID, so it can be replaced without invalidating anything the Token Deck already owns.

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

Status: **BUILT + INTEGRATED — not Verified**

Owner:

```text
src/synrheon/surface_segmentation.py
```

Frozen segmenter version:

```text
td3-exact-surface-v1
```

### Structural invariants

Both are enforced at construction time, not only in tests:

```text
every character of the input belongs to exactly one span
"".join(span.text for span in spans) == original text
```

A segmentation whose spans have a gap, an overlap, or text that disagrees with its own
offsets cannot be constructed.

### Output per span

```text
index                ordinal position
start / end          character offsets into the exact original string
text                 exact source slice
category             alpha | numeric | alphanumeric | whitespace | punctuation | symbol | other
normalized           lookup form for lexical spans only; None otherwise
is_lookup_candidate  mechanical eligibility, not a claim of being a known word
internal_marks       punctuation/symbol characters absorbed inside the span, with offsets
```

Categories come from Unicode character classes alone. `%` reports as punctuation and `$`
as symbol because that is what Unicode says, not because of what they mean.

### Segmentation rules

```text
whitespace runs      one span (layout stays recoverable)
lexical runs         letters/digits/combining marks
standalone marks     one span per character (no grouping judgement required)
internal marks       a mark joins a lexical span only when directly flanked by
                     lexical characters on both sides
```

The flanking rule is the whole of the joining policy. It is purely positional, so it
requires no list of "word-forming" characters — such a list would be a linguistic
judgement, which TD-3 is not allowed to make.

### What TD-3 still does not do

```text
select a sense
fabricate a concept/entity
infer truth
force part of speech
call an LLM to decide what a span means
create a token card or any stable identity
strip clitics, expand abbreviations, or lemmatize
silently discard punctuation, whitespace, invisible characters, or offset provenance
```

`Daisy's` reports an internal apostrophe. It does not report a possessive.

### Frozen consequences of the flanking rule

These are documented and locked by regression tests so a later change is visible rather
than silent:

```text
Daisy's / Don't / isn't      one span, internal apostrophe recorded
dogs'                        word and apostrophe split (no right-hand lexical flank)
well-known                   one span; well--known splits into four
8:30 / 3.5 / 12.50           numeric compounds; no time or percentage is claimed
$12.50                       symbol span separate from the numeric span
U.S.                         "U.S" + "."  (no abbreviation inference)
email@example.com            one span, marks "@." recorded
https://example.com/path?q=1 "https" ":" "/" "/" then one long compound span
```

The last case is the rule at its least flattering, and it is kept deliberately. Splitting
a URL into components is structure recognition, which belongs to TD-4 and later, and every
absorbed mark is recorded so a later stage can re-split without re-reading the source.

### Known limitations of `td3-exact-surface-v1`

```text
no UAX-29 grapheme clustering: emoji modifier and ZWJ sequences split into
several symbol spans (reconstruction still exact)
NFKC lookup forms may differ in length from the source ("3½" -> "31⁄2");
offsets always index the original string, never the normalized form
```

### Exposure for stimulus testing

```text
python3 -m synrheon segment "<text>"    exact observation as JSON, no session, no state
POST /api/segment {"text": ...}          inspection only; records nothing
StimulusRecord.segmentation              every live stimulus carries its own observation
trace event "surface_segmented"          span and lookup counts per stimulus
```

Live stimuli are segmented but create **no** token cards. The cognitive substrate is
byte-identical before and after a stimulus, and a test asserts it.

### Remaining gate to Verified

Automated tests grant `Built` and `Integrated` only. `Verified` requires observing the
intended behaviour through the running organism on your own stimuli.

## TD-4 — known / unknown acquisition boundary

Status: **BUILT + INTEGRATED — not Verified**

Owner:

```text
src/synrheon/acquisition_routing.py
```

Frozen router version:

```text
td4-acquisition-routing-v1
```

After segmentation, each lookup span asks whether Synrheon already has a usable representation.

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

### Routing is read-only

`route_segmentation(segmentation, deck)` creates no token card, no sense, and no concept,
and it mutates nothing. `acquire_route(deck, route, evidence_id=...)` is the only path from
observation to identity, and it must be called explicitly.

This keeps the earned invariant intact: observing language never silently becomes identity.
A live stimulus is segmented and routed, and the cognitive substrate is unchanged.

### Proposal, not truth

Each route carries every mechanical signal observed for the span, including signals that
did not decide the proposed need:

```text
known_form / unknown_form         deck resolution
surface_category                  TD-3 category
contains_digits                   numeric or alphanumeric
contains_known_part               a mark-delimited part resolves in the deck
mark_delimited_structure          internal marks present, no part known
capitalised                       with sentence-initial or interior position
uninformative_capital             sentence-initial: the capital carries no name evidence
all_capitals                      acronym, emphasis, and name are not distinguished
```

Recording the non-deciding signals is deliberate: a learned router can later be compared
against this one on identical observations.

### Decision order

```text
known                                            -> none
has digits                                       -> number_symbol_or_code
mark-delimited part resolves in the deck         -> variant_candidate
internal marks but no known part                 -> unresolved
capitalised, interior position, not all-capitals -> likely_name_or_entity
capitalised, sentence-initial or all-capitals    -> unresolved
lowercase alpha                                  -> ordinary_unknown_word
otherwise                                        -> unresolved
```

Names and entities never fall through to `ordinary_unknown_word`.

### The router abstains where orthography is uninformative

```text
"Logan said, ..."        Logan     unresolved      sentence-initial capital
'"Rex isn't outside."'   Rex       unresolved      opening quote is skipped, still initial
"I met BANK yesterday."  BANK      unresolved      all-capitals
"I met Bank yesterday."  Bank      likely_name_or_entity
```

A capital at the start of a sentence carries no information about whether a form is a name,
so the router refuses to guess there. Abstaining is cheap; a confident wrong class would
propagate into identity.

`SENTENCE_FINAL_MARKS` is the one orthographic convention hard-coded here. It is a frozen,
inspectable set, and the asymmetry is safe: widening it only widens abstention.

### Containment is not morphology

`variant_candidate` reports that a mark-delimited part of an unknown form resolves in the
deck — `Daisy's` contains a known `Daisy`. It asserts no lemma, stem, inflection, or
possessive relationship. TD-2 remains storage-only, and automatic morphological inference
is still not cognitive truth.

### Acquisition creates identity, never meaning

`acquire_route` calls `TokenDeck.observe` with provenance and creates **no sense**.
Deciding what a token can mean is TD-5's job. External dictionary/parser/LLM assistance may
later propose candidates with provenance. Proposal is not truth.

### Exposure for stimulus testing

```text
python3 -m synrheon route "<text>"        routing against a fresh empty deck
POST /api/acquisition {"text": ...}        routing against the live deck; acquires nothing
StimulusRecord.acquisition                 routing of each live stimulus at that moment
trace event "acquisition_routed"           known/unknown counts and need histogram
```

### Driving acquisition explicitly

```text
POST /api/acquire {"text": ..., "needs": [...]}   admit routed unknown forms
runtime.acquire_from_text(text, needs=...)         same, in process
trace event "tokens_acquired"                      exactly what was admitted
```

`needs` optionally restricts which acquisition classes are admitted, so `unresolved` forms
can be left out of identity entirely. Nothing on the stimulus path calls this.

## TD-5 — contextual sense disambiguation

Status: **NEXT; SCIENTIFIC EXPERIMENT REQUIRED — preregister before results**

This is the first serious language-learning experiment, so it is preregistered like MT-1
rather than built like TD-3/TD-4.

Prerequisites now satisfied: exact spans with provenance (TD-3), known/unknown resolution
against stable identity (TD-4), and a reversible multi-sense inventory that a learned
disambiguator can supply support over without deleting alternatives (TD-1).

Still missing before it can run: a sense-annotated data source, and a frozen decision about
which contexts are held out.

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
D6 result -> MT-1 preregistration FROZEN -> matched-compute stage test

REPRESENTATION
TD-0/1/2 -> TD-3 segmentation BUILT -> TD-4 acquisition BUILT -> TD-5 sense learning
```

`docs/MT1_PREREGISTRATION.md` explicitly forbids Token Deck output from entering any MT-1
condition. Token Deck improvements must not be used to rescue or reinterpret MT-1 after
its criteria are frozen.

## Near-term completion gate

The representation track moves past TD-3 when:

- [x] exact source text is preserved — enforced at construction, not only tested;
- [x] spans and offsets are deterministic under the frozen segmenter version;
- [x] punctuation/contractions/names/numbers/symbols have explicit tests;
- [x] no meaning inference leaks into segmentation;
- [x] Token Deck identity remains stable independent of the segmenter's implementation details;
- [ ] failures from your own stimulus testing become regression tests.

The last item is open by construction: it stays open until TD-3 has been driven with
stimuli that were not chosen by the person who wrote it.
