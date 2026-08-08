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
core.py        concept/world/organism-relation/activation substrate
time.py        episode time + experience sequence
experience.py  ordered autobiographical thread
runtime.py     sequencing/routing only
interfaces.py  browser/API transport only
ui/            explicit injection + observation only
```

# Current Project Status

```text
Stage 0B — Observable Organism Harness    Verified
Stage 1  — Cognitive Substrate            Active
```

The current Stage 1 candidate provides:
- concept identities
- world relations
- open-ended organism-relative relation types
- permanent separation between injected and self-learned organism relations
- activation state as separate state
- explicit injected/observed/inferred/learned provenance
- a confidence-weighted learned-relation update with evidence lineage
- ordered current-episode experience sequence and before/after links
- a Knowledge UI for manual scaffolding

There is still no spreading activation, automatic relation discovery, retrieval, durable memory, language understanding, or autonomous cognition.

# Root / Workflow Files

## `README.md`
Why Synrheon exists and the long-term cognitive hypothesis.

## `AGENTS.md`
Front door for coding agents. Points them to the Architecture Steward, canonical workflow, and project truth.

## `agent/ARCHITECTURE_STEWARD.md`
Defines broad-to-narrow development, correct ownership, live-organism proof, thin runtime, and honest status.

## `.agents/skills/synrheon-development-workflow/SKILL.md`
Canonical implementation workflow.

## `pyproject.toml`
Python project configuration and development dependencies.

## `.gitignore`
Prevents generated/local files from being committed.

# Project-Truth Documents

`docs/SCAFFOLD.md` — where files belong and what each area owns.

`docs/PROJECT_GUIDE.md` — this plain-English owner's manual.

`docs/SIGNAL_FLOW.md` — how information currently moves through Synrheon.

`docs/ARCHITECTURE_PLAN.md` — intended cognitive dependency order.

`docs/IMPLEMENTATION_STATUS.md` — what is Not Started, Designed, Built, Integrated, or Verified.

`docs/CURRENT_STAGE.md` — active implementation boundary.

`docs/DECISIONS.md` — durable architecture decisions.

`docs/EXPERIMENTS.md` — preregistered and observed experiments.

`docs/RESEARCH.md` — research that is not implementation truth.

`docs/PROMPT_TEMPLATES.md` — human-facing dispatch prompts.

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

One stable concept identity with:
- `concept_id` — stable internal identifier
- `label` — human-readable name
- `world_vector` — optional future generic/vector representation

Concept identity is separate from word forms and from Synrheon's relationship to the concept.

### `WorldRelation`

One generic relationship between concepts, for example:

```text
daisy IS_A dog
```

It stores source concept, relation type, target concept, provenance, confidence, and later evidence lineage.

### `OrganismRelation`

One typed relationship between Synrheon and a concept.

Important fields:
- `relation_type` — arbitrary non-empty text such as `protective_of`
- `strength` — current strength from 0 to 1
- `confidence` — confidence from 0 to 1
- `origin` — `injected` or `learned`
- `evidence_event_ids` — evidence lineage for learned relations

The important design rule is that `relation_type` is **data**, not a Python field or enum. Synrheon can therefore hold a future relation type that the developers did not anticipate when the code was written.

### `SelfRelation`

Groups organism-relative relations for one concept into two permanently separate collections:

```text
injected_relations
learned_relations
```

An injected relation means Synrheon was explicitly told that a concept relates to her in that way.

A learned relation means trusted experience updated that relation through the learning mechanism.

The same relation type may exist in both collections without either overwriting the other.

### `ActivationState`

Stores current concept activation separately from concept existence, world truth, injected organism relations, and learned organism relations.

It can currently store and rank activation values; recurrent sparse activation is not implemented yet.

### `CognitiveSubstrate`

Owns concepts, world relations, organism relations, and activation.

Important methods:

`add_concept()` — adds a stable concept identity.

`add_world_relation()` — adds a world relationship only when both concepts exist.

`set_injected_self_relation()` — accepts any non-empty relation type and writes only the injected collection.

`learn_self_relation()` — accepts any non-empty relation type and changes only the learned collection using:

```text
learned_new
=
learned_old
+
(learning_rate × trust)
×
(observed_strength - learned_old)
```

It preserves injected organism relations, world knowledge, learned confidence, and supporting experience-event IDs.

`set_activation()` — stores current activation without changing stored knowledge.

### `StimulusRecord`

Record of an accepted Chat or Internal Thought input. It links directly to its corresponding `experience_event_id`.

### `TraceEvent`

Records observable runtime actions. Trace is not hidden reasoning.

### `OrganismState`

Top-level live state containing session status/cycle, stimuli, trace, computational time, experience thread, and cognitive substrate.

A new session resets the current episode and activation. Injected concepts/world/organism relations and learned organism relations remain for the life of the current Python process.

Nothing here survives process restart yet.

## `src/synrheon/time.py`

**Plain English:** owns when an experience occurs and where it sits in the current episode.

`TemporalCoordinate` stores monotonic experience sequence, timestamp, episode ID, and elapsed seconds.

`ComputationalTime.begin_episode()` starts a new episode.

`ComputationalTime.next_coordinate()` creates the next temporal coordinate.

## `src/synrheon/experience.py`

**Plain English:** owns the current autobiographical event thread.

`ExperienceEvent` contains event ID, external/internal kind, `observed` or `injected` provenance, exact text, temporal coordinate, previous event ID, and next event ID.

`ExperienceThread.append()` adds the event and keeps forward/backward links consistent.

This is a **memory thread**, but not durable memory across restart.

## `src/synrheon/runtime.py`

**Plain English:** thin traffic controller.

Runtime sequences owners and routes commands; it does not own semantic interpretation, memory, learning, retrieval, abstraction, or problem solving.

`start()` starts a new episode/session.

`send_external_stimulus()` routes Chat into time + experience as `observed`.

`inject_internal_thought()` routes explicit Internal Thought injection into time + experience as `injected`.

`define_concept()` routes explicit concept injection to the substrate.

`define_world_relation()` routes injected world knowledge.

`define_self_relation()` passes an arbitrary relation type, strength, and confidence to the substrate's injected organism-relation collection. Runtime does not decide which relation types are valid meanings.

`think_one_step()`, `continue_thinking()`, and `pause()` preserve the verified harness controls. They still advance harness cycles only, not real recursive cognition.

## `src/synrheon/interfaces.py`

**Plain English:** browser/outside-world transport.

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

`/api/self-relation` accepts:

```text
concept_id
relation_type
strength
confidence
```

It validates transport shape and calls runtime methods. It does not decide what relation types mean.

## Other cognitive owners

`cognition.py` — future next-state cognitive transformation.

`memory.py` — future durable memory across restart.

`retrieval.py` — future Level 1 → Level 2 → Level 3 retrieval.

`scratchpad.py` — future limited active working state.

`problem_solving.py` — future problem/model/plan/prediction/trial/outcome/revision.

`learning.py` — future broader learning/credit assignment. The narrow arbitrary relation-strength update currently stays with the organism-relation representation because it mutates only that owner; broader learning should move/cooperate with `learning.py` when it exists.

`consolidation.py` — future replay, pattern detection, compression.

`abstraction.py` — future higher-order concept formation.

`autonomy.py` — future decision to continue cognition without new external input.

# UI

## `ui/index.html`

The development microscope has three views.

### Chat

Accepted external text becomes a `StimulusRecord`, an `ExperienceEvent(origin="observed")`, and part of the ordered experience thread.

### Internal Thought

Explicit injected internal text becomes `ExperienceEvent(origin="injected")`.

The view also displays experience number, observed vs injected provenance, previous/next links, elapsed episode time, and runtime trace.

### Knowledge

Manual developer scaffolding for:
- concept
- world relation
- injected organism relation

The organism-relation form uses a free-text `relation_type` rather than a fixed dropdown. It can inject a relation such as `protective_of` without any production-code change.

There is intentionally no UI control that directly creates learned organism relations.

### Inspector

Shows status, cycle, trace count, experience count, concept count, and complete backend state. JavaScript never owns the authoritative state.

## `ui/README.md`
Documents UI boundaries and current views.

# Tests

## `tests/test_scaffold.py`

High-value regression tests prove:
- Stage 0B controls remain functional
- external/internal channels stay distinct
- observed/injected experience provenance stays distinct
- experience sequence is monotonic
- previous/next links agree
- stimuli link to experience events
- arbitrary organism relation types are accepted as data
- injected and learned versions of the same relation type remain separate
- learned relation updates do not mutate injected organism state or world knowledge
- malformed/blank relation types and out-of-range values fail safely
- the HTTP boundary accepts a relation type that production code never named
- the Knowledge UI is served by the backend

Tests protect contracts; live UI observation is still required for `Verified`.

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

Current Synrheon can distinguish:

```text
what was injected
what was observed
what is generic world knowledge
what is injected organism-relative knowledge
what is self-learned organism-relative knowledge
what is currently active
what happened first / next
```

And the software no longer decides in advance the complete list of ways something may relate to Synrheon.

It still cannot automatically discover relation meanings from language/experience, spread activation, retrieve durable memory, or learn from live outcomes on its own.

# Maintenance Rule

Whenever meaningful code changes, keep this guide understandable to a non-programmer and explain what each owner does, what goes in/out, what state it owns, what calls it, what is live, and what is still planned.
