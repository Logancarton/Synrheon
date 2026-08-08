# Synrheon Project Guide — Plain English

This is the human-readable owner's manual for Synrheon. It explains what each important file owns, what is live now, and what is still planned.

Always distinguish **current real behavior** from **planned responsibility**.

# Quick Mental Model

```text
YOU
 ↓
Development UI
 ↓
interfaces.py
 ↓
runtime.py
 ↓
correct Synrheon owner
 ↓
state change
 ↓
snapshot / trace
 ↓
UI
```

Current cognitive/data owners:

```text
core.py        concepts, world relations, organism relations, activation state/frames
cognition.py   current stimulus → sparse active concept region
time.py        episode time + experience sequence
experience.py  ordered autobiographical thread
runtime.py     sequencing/routing only
interfaces.py  browser/API transport only
ui/            explicit injection + observation only
```

# Current Project Status

```text
Stage 0B — Observable Organism Harness    Verified
Stage 1  — Cognitive Substrate            Integrated candidate
Stage 3A — First Sparse Activation slice  Integrated candidate
```

Human live browser/state inspection is still required before the new cognition is called `Verified`.

Current Synrheon can now:
- hold explicitly injected concept identities
- hold typed world relations
- hold open-ended organism-relative relations
- keep injected and self-learned organism relations separate
- keep current activation separate from stored knowledge
- record ordered current-process experience
- send Chat/Internal Thought text through the real cognition owner
- generically cue already-known concepts by concept ID/label
- spread activation through directed world relations
- let already-reached concepts gain organism-relative salience
- inhibit weak candidates and keep a bounded Top-K active region
- expose the winning concepts and activation paths in the UI/state

There is still no semantic language understanding, durable memory, retrieval, response generation, automatic relation discovery, outcome-driven learning, or autonomous thought.

# Root / Workflow Files

`README.md` — why Synrheon exists and the current implementation boundary.

`AGENTS.md` — front door for coding agents.

`agent/ARCHITECTURE_STEWARD.md` — broad-to-narrow development, correct ownership, live-organism proof, thin runtime, honest status.

`.agents/skills/synrheon-development-workflow/SKILL.md` — canonical implementation workflow.

`pyproject.toml` — Python project/test configuration.

`.gitignore` — generated/local files Git should ignore.

# Project-Truth Documents

`docs/SCAFFOLD.md` — repository map and owner boundaries.

`docs/PROJECT_GUIDE.md` — this plain-English owner's manual.

`docs/SIGNAL_FLOW.md` — how information actually moves now.

`docs/ARCHITECTURE_PLAN.md` — intended dependency order and future mechanisms.

`docs/IMPLEMENTATION_STATUS.md` — what is Not Started, Designed, Built, Integrated, or Verified.

`docs/CURRENT_STAGE.md` — current development boundary.

`docs/DECISIONS.md` — durable architecture choices.

`docs/EXPERIMENTS.md` — preregistered and observed experiments.

`docs/RESEARCH.md` — research ideas, not implementation truth.

`docs/PROMPT_TEMPLATES.md` — human-facing dispatch prompts.

# Actual Python Organism

## `src/synrheon/__init__.py`

Package identity/version.

## `src/synrheon/__main__.py`

Application entry point:

```text
python -m synrheon
 ↓
runtime.main()
```

## `src/synrheon/core.py`

**Plain English:** owns Synrheon's basic internal representations and the top-level live state. It does not decide how activation should spread; that decision now belongs to `cognition.py`.

### `Concept`

One stable concept identity.

Important fields:
- `concept_id` — stable internal key
- `label` — human-readable name
- `world_vector` — reserved for later generic/vector representation

### `WorldRelation`

One directed world relationship between two known concepts.

Example:

```text
daisy IS_A dog
```

It stores source, relation type, target, provenance, confidence, and evidence lineage.

### `OrganismRelation`

One open-ended relation between Synrheon and a concept.

Fields:

```text
relation_type
strength
confidence
origin
evidence_event_ids
```

The critical rule is that `relation_type` is data, not an enum. New relation types can exist without editing production code.

### `SelfRelation`

Groups one concept's organism relations into two permanent collections:

```text
injected_relations
learned_relations
```

Injected information never silently becomes self-learned information.

### `ActivationState`

The small set of concepts that are active **right now**.

It is separate from whether a concept exists or whether a relation is stored.

`replace()` lets the cognition owner atomically replace the current active region after one bounded cognitive transition.

### `ActivationContribution`

One inspectable contribution to activation.

Examples:

```text
seed: Daisy +1.0
world: daisy —IS_A→ dog +0.62
organism: self —personally_relevant_to_self→ dog +0.14
```

This is observable state-transition evidence, not private chain-of-thought.

### `CognitiveFrame`

One observable result of processing one experience.

Stores:
- source experience event ID
- exact stimulus text
- `activated` or `unmatched`
- concepts directly matched by the lexical bootstrap
- final sparse active concepts
- activation contributions

### `CognitiveSubstrate`

Owns concepts, world relations, organism relations, and current activation.

Important methods:

`add_concept()` — creates a stable concept identity.

`add_world_relation()` — adds a world edge when both concepts exist.

`set_injected_self_relation()` — accepts any non-empty organism relation type and writes only injected state.

`learn_self_relation()` — updates only the learned relation of one arbitrary type using:

```text
learned_new
=
learned_old
+
(learning_rate × trust)
×
(observed_strength - learned_old)
```

`set_activation()` — direct low-level activation setter used mainly for substrate/testing support.

### `StimulusRecord`

Transport-facing record of an accepted Chat/Internal Thought input. Links to its `experience_event_id`.

### `TraceEvent`

Observable runtime event. It is not hidden reasoning.

### `OrganismState`

Top-level live state containing:
- session status/cycle
- stimuli
- runtime trace
- cognitive frames
- computational time
- experience thread
- cognitive substrate

A new session clears current experience, cognitive frames, and current activation. Injected/learned substrate knowledge remains only for the lifetime of the current Python process.

## `src/synrheon/cognition.py`

**Plain English:** this is now the first real next-state cognition owner.

### `ActivationConfig`

Contains the initial general activation hyperparameters:

```text
seed_strength       1.00
decay               0.30
spread_gain         0.62
organism_gain       0.35
inhibition_fraction 0.10
activation_floor    0.05
top_k               5
rounds              3
```

These values are starting mechanics to test, not semantic facts and not claimed optimal.

### `activate_from_text()`

Current live transformation:

```text
textual experience
 ↓
match already-known concept IDs/labels
 ↓
seed matching concepts
 ↓
recurrently spread through directed world relations
 ↓
add organism salience to concepts already reached
 ↓
decay + inhibition
 ↓
keep Top-K winners
 ↓
replace ActivationState
 ↓
return CognitiveFrame
```

There are no Daisy-, dog-, violin-, or phrase-specific branches.

### Lexical cue matcher

The first language bridge lowercases/tokenizes text and matches existing concept ID/label phrases.

This lets injected concept knowledge participate in cognition before a learned language model exists.

It is **not semantic understanding**. Unknown wording that does not match a known concept produces an `unmatched` frame and clears stale activation.

### World spreading

Activation follows the stored direction of `WorldRelation` edges.

Outgoing confidence is normalized per source concept so a node cannot send unlimited total activation merely because it has many outgoing edges.

### Organism salience

For a concept already reached by the cue/world spread, arbitrary injected/learned organism relations contribute generic salience based on:

```text
strength × confidence
```

The cognition code does not care what the relation type is called.

A highly self-relevant but unrelated concept does not activate by itself in this first mechanism.

### Competition

After each recurrent round, activation below the floor/winner-relative threshold is suppressed and only the strongest `Top-K` concepts survive.

## `src/synrheon/time.py`

Owns when an experience occurs and where it sits in the current episode.

`TemporalCoordinate` stores sequence, timestamp, episode ID, and elapsed seconds.

`ComputationalTime.begin_episode()` starts a new episode.

`ComputationalTime.next_coordinate()` creates the next temporal coordinate.

## `src/synrheon/experience.py`

Owns the current autobiographical event thread.

`ExperienceEvent` contains event ID, external/internal kind, observed/injected provenance, exact text, temporal coordinate, previous event ID, and next event ID.

`ExperienceThread.append()` maintains backward/forward sequence links.

This is not durable memory across restart.

## `src/synrheon/runtime.py`

**Plain English:** thin traffic controller.

Runtime sequences owners; it does not perform activation math itself.

For each Chat/Internal Thought event it:

```text
records time
 ↓
records ordered experience
 ↓
records stimulus
 ↓
invokes cognition.activate_from_text()
 ↓
stores returned CognitiveFrame
 ↓
returns snapshot
```

`define_concept()` routes concept scaffolding.

`define_world_relation()` routes world-knowledge scaffolding.

`define_self_relation()` routes arbitrary injected organism relations.

`Think One Step` / `Continue` still advance harness cycles only. They do not yet produce stimulus-free recursive cognition.

## `src/synrheon/interfaces.py`

Browser/API transport only.

Current endpoints:

```text
GET  /
GET  /api/state
GET  /health
POST /api/start
POST /api/pause
POST /api/continue
POST /api/step
POST /api/stimulus
POST /api/thought
POST /api/concept
POST /api/world-relation
POST /api/self-relation
```

It validates request shape and calls runtime. It does not interpret language or relations.

## Other cognitive owners

`memory.py` — future durable memory across restart.

`retrieval.py` — future Level 1 → Level 2 → Level 3 retrieval.

`scratchpad.py` — future limited active working state.

`problem_solving.py` — future problem/model/plan/prediction/trial/outcome/revision.

`learning.py` — future broader credit assignment and adaptation.

`consolidation.py` — future replay, pattern detection, compression.

`abstraction.py` — future higher-order concept formation.

`autonomy.py` — future decision to continue cognition without a new external/internal stimulus.

# UI

## `ui/index.html`

The development microscope has three views.

### Chat

Chat now shows both:

```text
user stimulus
+
Cognitive activation card
```

If a known concept matches, the card shows the sparse active winners.

If nothing matches, the card explicitly says no known concept cue matched. This prevents a silent/dead-looking Chat while avoiding a fake conversational reply.

### Internal Thought

Displays:
- ordered experience thread
- full cognitive activation frames
- recent relation-path contributions
- runtime trace

### Knowledge

Manual scaffolding for:
- concept
- world relation
- injected organism relation

The organism relation type remains free text, not a fixed dropdown.

### Inspector

Shows status, cycle, trace count, experience count, concept count, active concept count, and complete backend state.

JavaScript never owns authoritative cognition.

# Tests

## `tests/test_scaffold.py`

The current high-value suite now proves:
- Stage 0B controls still work
- observed/injected experience channels remain distinct
- previous/next experience links remain consistent
- arbitrary organism relation types remain data
- injected/learned relation provenance remains separate
- learning does not mutate world/injected state
- `Daisy → dog → animal` activates through general world edges
- a separate `violin → music` network uses the same mechanism
- unrelated concepts do not survive simply because another network was activated first
- an arbitrary organism relation increases only an already-reached concept's salience
- Top-K actually bounds the active region
- unknown cue clears stale activation without deleting the experience
- Chat reaches cognition through the real runtime path
- HTTP reaches the same runtime/cognition owners

Candidate reconstructed branch result: **12/12 passed**.

# Developer Scripts

```powershell
.\scripts\synrheon.ps1 setup
.\scripts\synrheon.ps1 run
.\scripts\synrheon.ps1 verify
.\scripts\synrheon.ps1 status
.\scripts\synrheon.ps1 context
```

# Current Information Flow

```text
Chat / Internal Thought
          ↓
     interfaces.py
          ↓
      runtime.py
       /   |    \
      ↓    ↓     ↓
 time.py experience.py cognition.py
                    ↓
                  core.py
          (ActivationState + CognitiveFrame)
                    ↓
             snapshot / trace
                    ↓
                   UI
```

# Important Truth

Current Synrheon now does more than store Chat text. A recognized cue produces a bounded internal state transition through general graph/salience mathematics.

But current cognition is still narrow:

```text
known lexical cue
→ sparse association activation
```

not:

```text
full language understanding
→ retrieval
→ reasoning
→ answer
```

That distinction must remain explicit so future development improves the real organism instead of hiding missing cognition behind fluent output.

# Maintenance Rule

Whenever meaningful code changes, keep this guide understandable to a non-programmer and explain what each owner does, what goes in/out, what state it owns, what calls it, what is live, and what is still planned.
