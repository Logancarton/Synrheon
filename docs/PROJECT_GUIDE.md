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
time.py + experience.py + core.py
 ↓
state / trace
 ↓
UI
```

The future learned thinking owner remains `cognition.py`, but it intentionally contains no hand-written thinking policy right now.

# Current Project Status

```text
Stage 0B — Observable Organism Harness   Verified
Stage 1  — Cognitive Substrate           Built / partially integrated
Stage 2  — Time + Experience             Integrated foundation
Pivot    — Trainable Cognitive Policy    Designed, not implemented
```

The previous lexical-match → relation-spread → fixed Top-K cognition experiment has been removed from production.

That means Chat currently records experience again without pretending that a developer-selected graph heuristic is the final cognition.

# What Synrheon Can Do Now

Synrheon can currently:
- run through the browser/runtime UI
- start, pause, continue, and step the observable harness
- record external Chat as `observed` experience
- record Internal Thought injection as `injected` experience
- maintain current-episode time, sequence, elapsed time, and previous/next links
- hold explicit concepts
- hold typed world relations
- hold open-ended organism-relative relations
- keep injected and self-learned organism relations separate
- keep activation representation separate from stored knowledge
- expose live state and trace in the UI

Synrheon currently **does not**:
- automatically decide which concepts should activate from text
- spread activation through a hand-written graph policy
- choose cognitive actions through a trained model
- retrieve durable memory
- reason recursively
- generate natural-language answers
- learn from live outcomes

# Root / Workflow Files

`README.md` — why Synrheon exists and the current pivot.

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

## `src/synrheon/core.py`

**Plain English:** owns basic explicit state, not the thinking strategy.

### `Concept`

One stable concept identity:

```text
concept_id
label
optional future world_vector
```

### `WorldRelation`

A stored relationship between known concepts, for example:

```text
daisy IS_A dog
```

The relation is data. Storing it does not mean production cognition automatically follows it.

### `OrganismRelation`

An open-ended relationship between Synrheon and a concept.

Important fields:

```text
relation_type
strength
confidence
origin
evidence_event_ids
```

`relation_type` remains free data rather than a fixed Python ontology.

### `SelfRelation`

Keeps two separate collections:

```text
injected_relations
learned_relations
```

What Synrheon was explicitly told cannot silently become what she learned herself.

### `ActivationState`

A container for current activation values.

Important change: **it is representation only.** Core no longer contains Top-K selection or atomic winner replacement for the retired heuristic.

A future learned cognition owner may update activation through an explicit interface, but the state container itself does not choose how to think.

### `CognitiveSubstrate`

Owns concepts, world relations, organism relations, and activation representation.

It validates stored state but does not choose cognitive routes.

### `learn_self_relation()`

This remains a narrow provenance-preserving storage update for one learned organism relation. It does not decide what thought path to follow and is not the new cognitive policy.

### `OrganismState`

Top-level live state containing:
- session status/cycle
- stimuli
- trace
- computational time
- ordered experience thread
- cognitive substrate

The retired `cognitive_frames` produced by the fixed activation heuristic are gone.

## `src/synrheon/cognition.py`

**Plain English:** reserved home for the trainable thinking policy.

Right now it deliberately contains **no production thinking algorithm**.

The removed experiment used:

```text
lexical matching
fixed relation spreading
fixed gains / decay
fixed inhibition
fixed Top-K
fixed recurrent rounds
```

Those rules were useful to prove live wiring but were too hand-designed to become Synrheon's long-term cognition.

The next implementation here should learn transformations such as:

```text
current cognitive state
 ↓
choose cognitive action
 ↓
short transition
 ↓
checkpoint
 ↓
new cognitive state
```

and train from outcome/error/credit evidence.

## `src/synrheon/time.py`

Owns when an experience occurs and where it sits in the current episode.

`TemporalCoordinate` stores sequence, timestamp, episode ID, and elapsed seconds.

## `src/synrheon/experience.py`

Owns the current autobiographical event thread.

`ExperienceEvent` contains event ID, external/internal kind, observed/injected provenance, exact text, temporal coordinate, previous event ID, and next event ID.

This is not durable memory across restart.

## `src/synrheon/runtime.py`

**Plain English:** thin traffic controller.

For Chat/Internal Thought it currently:

```text
records time
 ↓
records ordered experience
 ↓
records stimulus
 ↓
returns state / trace
```

It no longer calls a hand-written activation policy.

Runtime must remain thin when the learned cognitive policy arrives.

## `src/synrheon/interfaces.py`

Browser/API transport only.

Current endpoints remain:

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

## Other Cognitive Owners

`memory.py` — future durable memory.

`retrieval.py` — future Level 1 → Level 2 → Level 3 retrieval.

`scratchpad.py` — future active working state/checkpoints.

`problem_solving.py` — future problem/trial/outcome structure.

`learning.py` — future outcome/error/credit assignment and trainable policy updates.

`consolidation.py` — future replay/pattern/compression.

`abstraction.py` — future higher-order concept formation.

`autonomy.py` — future decision to continue cognition without new input.

# UI

## `ui/index.html`

The same three development views remain:

```text
Chat
Internal Thought
Knowledge
```

### Chat

Shows external text that was accepted and recorded as ordered observed experience.

It intentionally does **not** show fake cognitive activation or a fake answer while the learned policy is absent.

### Internal Thought

Shows the ordered experience thread and runtime trace.

### Knowledge

Still allows manual developer scaffolding for:
- concepts
- world relations
- injected organism relations

The organism-relation type remains free text.

### Inspector

Shows status, cycle, trace, experience, concept count, activation state, and complete backend state.

# Tests

## `tests/test_scaffold.py`

The high-value tests now prove:
- UI/runtime transport remains connected
- external/internal experience provenance remains distinct
- temporal sequence and previous/next links remain correct
- open-ended organism relation types remain data
- injected/learned provenance remains separate
- invalid state fails safely
- Chat does **not** mutate knowledge/activation through a hand-written cognitive policy
- HTTP still reaches the same real runtime and UI

The tests intentionally no longer prove lexical spreading or fixed Top-K because that production behavior was removed.

# Next Research Experiment

The next core test is not “Can Synrheon answer a Daisy question?”

It is:

```text
train cognitive process on worlds A/B/C
            ↓
learn state → action → next-state transitions
            ↓
run on unseen world D
            ↓
perform useful cognitive operations above baseline
```

If changing concept names destroys performance, the model likely learned knowledge/shortcuts instead of how to think.

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
       /       \
      ↓         ↓
 time.py   experience.py
      \         /
       OrganismState
            ↓
      snapshot / trace
            ↓
            UI
```

Knowledge injection separately reaches `core.py` through runtime.

`cognition.py` remains intentionally uninvoked until a genuine trainable policy exists.

# Maintenance Rule

Whenever meaningful code changes, keep this guide understandable to a non-programmer and explain what each owner does, what goes in/out, what state it owns, what calls it, what is live, and what is still planned.
