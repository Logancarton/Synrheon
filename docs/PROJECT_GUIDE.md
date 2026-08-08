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
core.py        concept/world/self/activation substrate
time.py        episode time + experience sequence
experience.py  ordered autobiographical thread
runtime.py     sequencing/routing only
interfaces.py  browser/API transport only
ui/            injection + observation only
```

# Current Project Status

```text
Stage 0B — Observable Organism Harness    Verified
Stage 1  — Cognitive Substrate            Active
```

The current Stage 1 candidate adds:
- concept identities
- world relations
- separate organism/self relation vectors
- activation state as separate state
- explicit injected/observed/inferred/learned provenance
- a confidence-weighted self-vector learning method
- ordered current-episode experience sequence and before/after links
- a Knowledge UI for manual scaffolding

There is still no spreading activation, retrieval, durable memory, language understanding, or autonomous cognition.

# Root / Workflow Files

## `README.md`
Why Synrheon exists and the long-term cognitive hypothesis.

## `AGENTS.md`
Front door for coding agents. Points them to the Architecture Steward, canonical workflow, and project truth.

## `agent/ARCHITECTURE_STEWARD.md`
Defines how development decisions should be made: broad-to-narrow, correct ownership, live-organism proof, thin runtime, honest status.

## `.agents/skills/synrheon-development-workflow/SKILL.md`
Canonical implementation workflow.

## `pyproject.toml`
Python project configuration and development dependencies.

## `.gitignore`
Prevents generated/local files from being committed.

# Project-Truth Documents

## `docs/SCAFFOLD.md`
Where files belong and what each major area owns.

## `docs/PROJECT_GUIDE.md`
This plain-English owner's manual.

## `docs/SIGNAL_FLOW.md`
How information currently moves through Synrheon, with planned flow kept separate.

## `docs/ARCHITECTURE_PLAN.md`
What should eventually exist and in what dependency order.

## `docs/IMPLEMENTATION_STATUS.md`
What is Not Started, Designed, Built, Integrated, or Verified.

## `docs/CURRENT_STAGE.md`
The active implementation boundary.

## `docs/DECISIONS.md`
Durable architectural decisions.

## `docs/EXPERIMENTS.md`
Pre-registered and observed live experiments.

## `docs/RESEARCH.md`
Research ideas that are not implementation truth.

## `docs/PROMPT_TEMPLATES.md`
Human-facing dispatch prompts.

# Actual Python Organism

## `src/synrheon/__init__.py`
Package identity and version.

## `src/synrheon/__main__.py`

Application entry point:

```text
python -m synrheon
 ↓
runtime.main()
```

## `src/synrheon/core.py`

**Plain English:** owns the first real cognitive substrate and the top-level live organism state.

### `Concept`

One stable concept identity.

Current fields:
- `concept_id` — stable internal identifier
- `label` — human-readable name
- `world_vector` — optional future generic/vector representation

The concept identity is separate from word forms and from Synrheon's personal relationship to the concept.

### `WorldRelation`

One generic relationship between concepts.

Example:

```text
daisy IS_A dog
```

Fields include:
- source concept
- relation type
- target concept
- provenance/origin
- confidence
- supporting evidence-event IDs

Injected world knowledge remains marked `injected`.

### `SelfRelationVector`

How a concept relates to Synrheon.

Initial dimensions:

```text
ownership
experience
social
goal
history
knowledge
trust
prediction
consequence
preference
uncertainty
```

This is deliberately separate from generic world meaning.

### `SelfRelation`

Wraps one concept's organism-relative vector with:
- provenance
- confidence
- evidence-event lineage

Injected self scaffolding stays `injected`.

Learned self state is marked `learned`.

### `ActivationState`

Stores current concept activation separately from concept existence and stored relation truth.

Current implementation can store/top-rank activation values, but the recurrent sparse activation equation is not implemented yet.

### `CognitiveSubstrate`

Owns:
- concepts
- world relations
- self relations
- activation state

Important methods:

`add_concept()`
Adds a stable concept identity.

`add_world_relation()`
Adds a world relation only when both concepts already exist.

`set_injected_self_relation()`
Sets one self dimension from explicit developer scaffolding without pretending Synrheon learned it.

`learn_self_relation()`
Updates the explicit self vector using:

```text
s_new = s_old + (learning_rate × trust) × (observation - s_old)
```

It stores the evidence event ID and does not rewrite world knowledge.

`set_activation()`
Stores current activation without changing concept/world/self knowledge.

### `StimulusRecord`

Transport-facing record of an accepted Chat or Internal Thought input.

It now links directly to its corresponding `experience_event_id`.

### `TraceEvent`

Records observable runtime actions. Trace is not hidden reasoning.

### `OrganismState`

Top-level live state.

Contains:
- session status/cycle
- stimuli
- trace
- computational time
- experience thread
- cognitive substrate

A new session resets the current experience episode and activation, while injected concept/world/self scaffolding remains for the life of the running process.

Nothing here is durable across process restart yet.

## `src/synrheon/time.py`

**Plain English:** owns when an experience occurs and where it sits in the current episode.

### `TemporalCoordinate`

Contains:
- monotonic experience sequence
- absolute timestamp
- episode ID
- elapsed seconds since episode start

### `ComputationalTime`

`begin_episode()`
Starts a new episode and resets experience sequence.

`next_coordinate()`
Creates the next temporal coordinate.

`snapshot()`
Exposes current temporal state to the UI.

## `src/synrheon/experience.py`

**Plain English:** owns the current autobiographical event thread.

### `ExperienceEvent`

One meaningful external or injected internal event.

Contains:
- event ID
- external/internal kind
- `observed` or `injected` provenance
- exact text
- temporal coordinate
- previous event ID
- next event ID

### `ExperienceThread`

`begin_episode()`
Starts a fresh thread for a new session.

`append()`
Adds one event, links it backward to the previous event, and updates the previous event's forward link.

`snapshot()`
Returns the ordered thread for the UI/API.

This is a **memory thread**, but not durable memory yet.

## `src/synrheon/runtime.py`

**Plain English:** thin traffic controller.

Runtime may sequence owners and route commands.

It does not own semantic interpretation, memory, learning, retrieval, abstraction, or problem solving.

Important methods:

`start()`
Starts a new episode/session.

`send_external_stimulus()`
Routes Chat input into computational time and the experience owner as `observed`.

`inject_internal_thought()`
Routes explicit Internal Thought injection into the experience owner as `injected`.

`define_concept()`
Routes explicit concept injection to `CognitiveSubstrate`.

`define_world_relation()`
Routes world knowledge to the substrate with `origin = injected`.

`define_self_relation()`
Routes one injected organism-relative dimension to the self vector.

`think_one_step()`, `continue_thinking()`, `pause()`
Keep the verified control surface working. They still advance harness cycles only, not real recursive cognition.

## `src/synrheon/interfaces.py`

**Plain English:** outside-world/browser transport.

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

It validates transport input and calls runtime methods.

It does not decide what words mean.

## `src/synrheon/cognition.py`
Placeholder for future real next-state cognitive transformation.

## `src/synrheon/memory.py`
Placeholder for durable memory across restart.

## `src/synrheon/retrieval.py`
Placeholder for Level 1 → Level 2 → Level 3 retrieval.

## `src/synrheon/scratchpad.py`
Placeholder for limited active working state.

## `src/synrheon/problem_solving.py`
Placeholder for problem/model/plan/prediction/trial/outcome/revision.

## `src/synrheon/learning.py`
Placeholder for broader learning/credit assignment. The narrow explicit self-vector update currently lives with the self-relation substrate because it only mutates that representation; if learning grows beyond that boundary, ownership should move/cooperate with `learning.py`.

## `src/synrheon/consolidation.py`
Placeholder for replay, pattern detection, and compression.

## `src/synrheon/abstraction.py`
Placeholder for higher-order concept formation.

## `src/synrheon/autonomy.py`
Placeholder for deciding whether unresolved internal state warrants another cognitive cycle.

# UI

## `ui/index.html`

The development microscope now has three views.

### Chat

External input.

Accepted text becomes:
- a `StimulusRecord`
- an `ExperienceEvent(origin="observed")`
- part of the ordered experience thread

### Internal Thought

Explicit injected internal input plus observation.

Injected text becomes:

```text
ExperienceEvent(origin="injected")
```

The view also displays the current memory thread:
- experience number
- observed vs injected
- previous/next links
- elapsed episode time
- runtime trace

### Knowledge

Manual developer scaffolding for early Synrheon construction.

Allows injection of:
- concept
- world relation
- self relation dimension

This is intentionally explicit because no language-to-concept interpreter exists yet.

### Inspector

Shows:
- status
- cycle
- trace event count
- experience count
- concept count
- complete backend state

JavaScript never owns the authoritative organism state.

## `ui/README.md`
Documents the UI boundary and current views.

# Tests

## `tests/test_scaffold.py`

High-value regression tests now prove:
- Stage 0B controls remain functional
- external and internal channels remain distinct
- observed and injected experience provenance remain distinct
- experience sequence is monotonic
- previous/next links agree
- stimuli link to experience events
- world/self/activation state remain separate
- self-vector learning does not mutate world knowledge
- malformed relation references fail safely
- the HTTP boundary reaches the real runtime/substrate
- the Knowledge UI is served by the backend

Tests protect contracts; live UI observation is still required for `Verified`.

# Developer Scripts

## `scripts/synrheon.ps1`

Main PowerShell command:

```powershell
.\scripts\synrheon.ps1 setup
.\scripts\synrheon.ps1 run
.\scripts\synrheon.ps1 verify
.\scripts\synrheon.ps1 status
.\scripts\synrheon.ps1 context
```

## `scripts/context.ps1`
Creates a project/context snapshot.

## `scripts/run.ps1`
Run shortcut.

## `scripts/verify.ps1`
Verification shortcut.

# Current Information Flow

```text
Chat ----------------------┐
Internal Thought ----------┤
Knowledge injection -------┤
                           ↓
                     interfaces.py
                           ↓
                      runtime.py
                    /      |      \
                   ↓       ↓       ↓
               time.py  core.py  experience.py
                   \       |       /
                    \      |      /
                     OrganismState
                           ↓
                    snapshot + trace
                           ↓
                         Browser
```

# Important Truth

Current Synrheon can now distinguish:

```text
what was injected
what was observed
what is world knowledge
what is organism-relative knowledge
what is currently active
what happened first / next
```

It still cannot yet automatically understand language, spread activation, retrieve memory, or learn from live outcomes on its own.

# Maintenance Rule

Whenever meaningful code changes, keep this guide understandable to a non-programmer and explain:
- what the file does
- what each important class/function does
- what goes in
- what comes out
- what state it owns
- what calls it
- what it calls
- what is live
- what is still planned
