# Current Stage

## Active Stage

**Stage 1 — Cognitive Substrate + First Sparse Activation**

Stage 0B — Observable Organism Harness remains **Verified** and is still the live laboratory.

## Current Live Boundary

Synrheon now has four separable substrate layers:

```text
Layer 1 — Concept Identity
Layer 2 — World Relations
Layer 3 — Current Activation / Situation
Layer 4 — Open-Ended Organism Relations
```

And the candidate live stimulus path is now:

```text
Chat / Internal Thought text
        ↓
ordered experience
        ↓
generic known-concept lexical cueing
        ↓
cognition.py
        ↓
directed world-relation spread
        +
organism-relative salience
        +
decay
        -
competition
        ↓
Top-K sparse active region
        ↓
observable cognitive frame
        ↓
Chat + Internal Thought + raw state
```

This is the first implemented state transformation that changes which concepts are cognitively active based on current input and relationship structure.

## Important Non-Hardcoded Boundary

The production mechanism does **not** contain rules for Daisy, dog, violin, walk, or any specific organism relation name.

Concept cues are matched generically against already-existing concept IDs/labels. World relations are traversed from stored data. Organism relation types remain arbitrary strings stored as data.

A second unrelated concept network therefore uses the same activation algorithm as the first.

## Current Activation Mechanics

The first bounded recurrence uses:

```text
seed known concepts
      ↓
retain a decayed fraction of current activation
      +
normalized directed world-relation spread
      +
open-ended organism salience on already-reached concepts
      ↓
clip to valid activation range
      ↓
winner-relative inhibition threshold
      ↓
Top-K = 5
```

Initial recurrence count: **3 rounds per textual experience**.

These are starting hyperparameters, not claimed optimal values.

## What Organism Relations Do Right Now

Organism relation names are intentionally not interpreted by a fixed ontology.

For an already-reached concept, any injected or learned organism relation contributes generic personal salience based on:

```text
strength × confidence
```

This can make a personally relevant concept more competitive without globally activating unrelated personal concepts.

Later cognition can learn context-specific meanings/valence for relation types. That is not implemented yet.

## Current Text Understanding Boundary

The lexical cue layer is deliberately minimal:

```text
"Daisy" → existing concept ID/label `daisy`
```

It is case-insensitive and supports generic multi-token concept labels, but it is **not semantic language understanding**.

If no known concept matches:
- the experience is still recorded
- a cognitive frame reports `unmatched`
- stale activation is cleared
- Synrheon does not pretend it understood the text

## Sequencing Foundation

Every Chat/Internal Thought event still receives:
- episode ID
- timestamp
- monotonic experience sequence
- elapsed episode time
- previous/next links
- observed vs injected provenance

The cognitive frame is linked back to the same experience event ID.

This thread is still in-memory only and does not survive process restart.

## Candidate Evidence

```text
Focused activation preview     Passed
Runtime live-path preview      Passed
HTTP/API integration preview   Passed
Current test suite             12/12 passed
Python compileall              Passed
```

Human browser/state inspection remains required before this candidate is called **Verified**.

## What Is Still Missing

There is still no implemented:

- semantic language understanding / learned encoder
- automatic concept creation from unknown language
- automatic discovery/naming of organism relation types
- durable memory across restart
- Level 1 → Level 2 → Level 3 retrieval
- context-specific interpretation of organism relation meanings
- outcome-driven live self-learning
- natural-language response generation
- scratchpad recursion
- problem solving
- autonomous continuation

## Immediate Next Boundary After Live Verification

Do **not** add a fake response generator.

Once the user verifies that Chat visibly changes the intended sparse activation state, the next architectural decision should be whether to deepen:

```text
language → concept/sense perception
```

or

```text
active concepts → temporal/durable retrieval
```

based on what the live stimulus tests reveal.
