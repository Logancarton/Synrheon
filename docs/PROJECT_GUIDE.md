# Synrheon Project Guide — Plain English

This is the human-readable owner's manual for Synrheon. It explains what each important file owns, what is live now, and what is still planned.

Always distinguish **current real behavior** from **planned responsibility**.

# The New Mental Model

Synrheon is no longer trying to become intelligent by adding more hand-written rules for what to think next.

The new direction is:

```text
KNOWLEDGE
concepts
relations
experience
memory
tools
outside information
        ↓
CURRENT COGNITIVE STATE
        ↓
LEARNED COGNITIVE SKILL
focus
explore
retrieve
compare
check
predict
revise
stop
        ↓
NEXT COGNITIVE STATE
        ↓
checkpoint
        ↓
repeat only if useful
```

In plain English:

> **Teach Synrheon what kinds of mental actions are possible, then train her to learn when and how to use them instead of programming the route for every situation.**

# Current Real Flow

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
Stage 1P — Trainable Cognitive Policy    Designed, not implemented
```

The previous lexical-match → relation-spread → fixed Top-K cognition experiment has been removed from production.

That means Chat currently records experience again without pretending that a developer-selected graph heuristic is the final cognition.

# What Synrheon Can Do Now

Synrheon can currently:
- run through the browser/runtime UI;
- start, pause, continue, and step the observable harness;
- record external Chat as `observed` experience;
- record Internal Thought injection as `injected` experience;
- maintain current-episode time, sequence, elapsed time, and previous/next links;
- hold explicit concepts;
- hold typed world relations;
- hold open-ended organism-relative relations;
- keep injected and self-learned organism relations separate;
- keep activation representation separate from stored knowledge;
- expose live state and trace in the UI.

Synrheon currently **does not**:
- automatically decide which concepts should activate from text;
- choose cognitive actions through a trained model;
- perform checkpointed learned thought transitions;
- retrieve durable memory;
- reason recursively;
- generate natural-language answers;
- learn from live outcomes.

# What We Mean by “Train How to Think”

The initial trainable cognition system should learn transitions like:

```text
state A
 ↓ choose RETRIEVE
state B
 ↓ choose COMPARE
state C
 ↓ choose CHECK_EVIDENCE
state D
 ↓ choose PREDICT
state E
 ↓ choose STOP
```

The names of the operations may change. The important part is that Synrheon learns **which mental operation is useful from the state she is currently in**.

We do not want production code saying:

```text
if user asks about a name → retrieve
if relation is IS_A → expand
if concept is Daisy → follow dog
```

Those would be another version of the brittle system we intentionally removed.

# Designed Structure vs Learned Behavior

Some things must still be written in normal code.

## Normal software may define

```text
what state looks like
what an action interface looks like
how provenance is stored
how a checkpoint is recorded
maximum allowed cognitive steps
how outcomes/corrections enter training
how model weights are saved/loaded
safe validation
```

## Training should increasingly learn

```text
what deserves attention
which path is promising
which cognitive action should happen next
when to retrieve
what evidence to compare
what to predict
when to revise
which earlier step deserves credit or blame
when the thought process is done
```

A useful shorthand is:

> **We code the cognitive physics. Synrheon learns the cognitive skill.**

# One Cognitive Micro-Cycle

Instead of generating one huge hidden reasoning chain, Synrheon should operate in short steps:

```text
S0 — current state
 ↓
choose one mental action
 ↓
perform a bounded transition
 ↓
S1 — checkpoint
 ↓
look at where cognition is now
 ↓
choose another action or stop
```

The checkpoint is not a literal pause in seconds. It is an observable state boundary.

This matters because we can later answer:
- what state existed before the action;
- which action was chosen;
- what changed;
- what the model expected;
- what actually happened;
- whether that action deserved credit.

# The First Training Record

A useful training example should contain something like:

```text
state_before
available_actions
selected_action
short_transition_or_path
state_after
prediction
observed_outcome
error_or_correction
credit_assignment
```

Very important:

```text
selected path ≠ good path
```

Synrheon must not strengthen a route simply because she happened to choose it.

# The First Proof We Care About

The next experiment is not primarily:

> Can Synrheon answer a Daisy question?

It is:

> **Can Synrheon learn a thinking process on several small knowledge worlds and reuse that process with completely unfamiliar knowledge?**

```text
train on worlds A / B / C
          ↓
learn cognitive process
          ↓
run on unseen world D
          ↓
use useful mental operations above baseline
```

We will deliberately rename/permute concepts so the model cannot rely on familiar words.

If it works only on the training worlds, that is memorization or overfitting—not proof that Synrheon learned how to think.

# Root / Workflow Files

`README.md` — why Synrheon exists and the current research direction.

`AGENTS.md` — front door for coding agents.

`agent/ARCHITECTURE_STEWARD.md` — broad-to-narrow development, correct ownership, live-organism proof, thin runtime, honest status.

`.agents/skills/synrheon-development-workflow/SKILL.md` — canonical implementation workflow.

`pyproject.toml` — Python project/test configuration.

`.gitignore` — generated/local files Git should ignore.

# Project-Truth Documents

`docs/SCAFFOLD.md` — repository map and owner boundaries.

`docs/PROJECT_GUIDE.md` — this plain-English owner's manual.

`docs/SIGNAL_FLOW.md` — how information actually moves now and how the planned trainable loop should move.

`docs/ARCHITECTURE_PLAN.md` — intended dependency order and future mechanisms.

`docs/IMPLEMENTATION_STATUS.md` — what is Not Started, Designed, Built, Integrated, or Verified.

`docs/CURRENT_STAGE.md` — current development boundary and immediate success criteria.

`docs/DECISIONS.md` — durable architecture choices.

`docs/EXPERIMENTS.md` — preregistered and observed experiments, including anti-memorization transfer gates.

`docs/RESEARCH.md` — research ideas and prior-art leads, not implementation truth.

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

A concept should eventually be richer than a word. Neural representations may later learn similarity, function, context, prediction usefulness, and cross-modal grounding while the explicit concept identity remains available.

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

Important: **it is representation only.** Core does not decide which concepts should win.

A future learned cognition owner may update activation through an explicit interface, but the state container itself does not choose how to think.

### `CognitiveSubstrate`

Owns concepts, world relations, organism relations, and activation representation.

It validates stored state but does not choose cognitive routes.

### `learn_self_relation()`

This remains a narrow provenance-preserving storage update for one learned organism relation. It does not decide what thought path to follow and is not the cognitive policy.

### `OrganismState`

Top-level live state containing:
- session status/cycle;
- stimuli;
- trace;
- computational time;
- ordered experience thread;
- cognitive substrate.

## `src/synrheon/cognition.py`

**Plain English:** home for the trainable thinking policy.

Right now it deliberately contains **no production thinking algorithm**.

The next real implementation should eventually own:

```text
CognitiveState
        ↓
policy chooses cognitive action
        ↓
bounded cognitive transition
        ↓
next checkpoint
```

It should not own durable memory storage, HTTP/UI behavior, or outcome-learning persistence that belongs elsewhere.

## `src/synrheon/learning.py`

**Plain English:** future owner for learning from whether cognition actually helped.

Expected responsibilities include:

```text
prediction vs outcome
error / correction
credit assignment
policy update
transition-model update
route-usefulness learning
```

It must not mark world facts false merely because a reasoning route failed.

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

When learned cognition is added, runtime may sequence:

```text
state → cognition owner → checkpoint → next owner
```

but runtime must not choose the cognitive action itself.

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

`retrieval.py` — future Level 1 → Level 2 → Level 3 retrieval operation.

`scratchpad.py` — future active working state/checkpoints.

`problem_solving.py` — future problem/trial/outcome structure.

`consolidation.py` — future replay/pattern/compression.

`abstraction.py` — future higher-order concept formation.

`autonomy.py` — future decision to continue cognition without new input.

# Language / LLM Role

Language is not planned as the thinking owner.

```text
language / observation
 ↓
perception / grounding
 ↓
CognitiveState
 ↓
learned cognitive process
 ↓
reportable state
 ↓
language expression
```

A future LLM can be genuinely useful for interpretation, outside knowledge, simulation, concept proposals, and expression. But fluent output cannot substitute for the internal state/process being present.

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

Later it should display **observable cognitive checkpoints**, not hidden chain-of-thought text.

### Knowledge

Still allows manual developer scaffolding for:
- concepts;
- world relations;
- injected organism relations.

The organism-relation type remains free text.

### Inspector

Shows status, cycle, trace, experience, concept count, activation state, and complete backend state.

# Tests

## `tests/test_scaffold.py`

The current tests prove:
- UI/runtime transport remains connected;
- external/internal experience provenance remains distinct;
- temporal sequence and previous/next links remain correct;
- open-ended organism relation types remain data;
- injected/learned provenance remains separate;
- invalid state fails safely;
- Chat does **not** mutate knowledge/activation through a hand-written cognitive policy;
- HTTP still reaches the same real runtime and UI.

The next trainable-cognition tests should prove:
- model parameters actually learn;
- state/action/checkpoint traces are real;
- held-out knowledge transfers above baseline;
- renaming concepts does not destroy the learned strategy;
- some tasks require useful multi-step action sequences;
- no task-specific production branch exists;
- runtime remains thin.

# Developer Scripts

On Windows PowerShell:

```powershell
.\scripts\synrheon.ps1 setup
.\scripts\synrheon.ps1 run
.\scripts\synrheon.ps1 verify
.\scripts\synrheon.ps1 status
.\scripts\synrheon.ps1 context
```

On macOS, use `pwsh` for the PowerShell helper when PowerShell is installed, or invoke the underlying Python commands directly where appropriate.

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

# Planned Thinking Flow

```text
perceived / grounded state
        ↓
cognition.py
        ↓
choose one learned cognitive action
        ↓
bounded transition
        ↓
checkpoint
        ↓
learning.py later receives outcome/error/credit
        ↓
policy improves
```

# Maintenance Rule

Whenever meaningful code changes, keep this guide understandable to a non-programmer and explain what each owner does, what goes in/out, what state it owns, what calls it, what is live, and what is still planned.
