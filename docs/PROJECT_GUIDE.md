# Synrheon Project Guide — Plain English

This is the human-readable owner's manual for Synrheon. It explains what each important file owns, what is live now, and what is still planned.

Always distinguish **current real behavior** from **planned responsibility**.

# Quick Mental Model

```text
YOU
 ↓
Development UI
 ↓
HTTP / browser boundary
 ↓
Thin runtime
 ↓
Synrheon-owned state
 ↓
state change + trace
 ↓
runtime
 ↓
HTTP boundary
 ↓
UI
 ↓
YOU
```

Stage 0B established and live-verified this organism shell. Stage 1 now begins adding the first real cognitive substrate inside that observable path.

```text
UI          = dashboard / microscope
interfaces  = outside-world transport boundary
runtime     = traffic controller / sequencer
core        = current Synrheon-owned observable state and likely Stage 1 substrate owner
cognition   = future next-state cognitive transformation
docs        = project truth
tests       = regression protection
scripts     = developer convenience
```

The UI does not think. The HTTP layer does not think. The runtime does not interpret language. Cognitive owners must produce cognitive behavior and expose it through these verified boundaries.

# Current Project Status

Current stage:

```text
Stage 1 — Cognitive Substrate
```

Stage 0B — Observable Organism Harness is **Verified**.

The live frontend/backend/runtime path is:

```text
Browser
 ↓
interfaces.py HTTP API
 ↓
SynrheonRuntime
 ↓
OrganismState
 ↓
snapshot + trace
 ↓
Browser
```

The live UI provides:

- Chat tab for external user stimuli
- Internal Thought tab for runtime trace and explicit internal-thought injection
- Start / Restart Session
- Think One Step
- Continue
- Pause
- current status, session, cycle, event and input counts
- raw state inspection

The user ran the supported local application and confirmed the real UI workflow worked. That verifies Stage 0B as **Infrastructure**.

Stage 1 is the first planned **Cognitive improvement** stage, but no Stage 1 cognitive mechanism is implemented yet. There is still no language understanding, durable memory, retrieval, learning, abstraction, or autonomous cognition.

# Root Files

## `README.md`
Why Synrheon exists and the long-term cognitive hypothesis.

## `AGENTS.md`
Front door for coding agents. Points them to the architecture steward, canonical workflow, and project truth.

## `pyproject.toml`
Python project configuration and development dependencies.

## `.gitignore`
Prevents generated/local files from being committed.

# Agent / Workflow Files

## `agent/ARCHITECTURE_STEWARD.md`
Defines how development decisions should be made: broad-to-narrow, correct ownership, live-organism proof, thin runtime, honest status.

## `.agents/skills/synrheon-development-workflow/SKILL.md`
Canonical execution workflow for implementation, live proof, tests, documentation, Git review, commit, and push.

## `.agents/skills/synrheon-development-workflow/openai.yaml`
OpenAI/Codex discovery metadata for the canonical workflow.

## `.claude/skills/synrheon-development-workflow.md`
Thin Claude adapter pointing to the same workflow.

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
What actually exists: Not Started, Designed, Built, Integrated, or Verified.

## `docs/CURRENT_STAGE.md`
What Synrheon is working on now.

## `docs/DECISIONS.md`
Durable architectural choices.

## `docs/EXPERIMENTS.md`
What was actually tested or observed.

## `docs/RESEARCH.md`
Ideas, papers, mechanisms, and unresolved questions that are not implementation truth.

## `docs/PROMPT_TEMPLATES.md`
Human-facing prompts for common development tasks.

# Actual Python Organism

## `src/synrheon/__init__.py`
Package identity and version.

## `src/synrheon/__main__.py`
Application entry point.

```text
python -m synrheon
 ↓
runtime.main()
```

## `src/synrheon/core.py`

**Plain English:** owns the smallest real Synrheon state used by the verified Stage 0B organism.

### `OrganismState`
Holds the current in-memory session state:

- session ID
- off / paused / running status
- cycle count
- monotonic event sequence
- received stimuli
- observable trace

`begin_session()` creates a fresh session. `snapshot()` returns a detached JSON-safe view for the UI.

This state lasts for the running process. It is **not durable memory across restart**.

### `StimulusRecord`
Represents one received input.

`kind="external"` means user/chat input.

`kind="internal"` means an explicitly injected internal stimulus.

These channels are intentionally separate so future cognition can treat them differently.

### `TraceEvent`
Records what the observable harness actually did. Trace is observation data, not hidden reasoning.

### `utc_now()`
Provides timestamps for observable events.

Stage 1 is expected to add the minimum substrate required for concepts, connections, activation, cognitive state, and basic state transitions. The exact mechanism must still pass the architecture gate and live experiment before implementation.

## `src/synrheon/runtime.py`

**Plain English:** thin traffic controller for the live organism.

### `SynrheonRuntime`
Owns sequencing around one `OrganismState`.

Important methods:

- `start()` — creates a fresh session in paused mode
- `pause()` — stops future automatic cycles
- `continue_thinking()` — enables repeated cycles
- `think_one_step()` — advances exactly one cycle while paused
- `send_external_stimulus()` — records Chat input on the external channel
- `inject_internal_thought()` — records an injected thought on the internal channel
- `snapshot()` — returns current observable state
- `close()` — stops the background runtime worker

The background worker only advances the Stage 0B cycle counter while status is running. It does not manufacture thoughts.

### `main()`
Creates the runtime and hands it to the development HTTP server.

Runtime does not own language understanding, memory, retrieval, learning, abstraction, or problem-solving.

## `src/synrheon/interfaces.py`

**Plain English:** connection between the browser and Synrheon.

### `DevelopmentRequestHandler`
Translates browser HTTP requests into runtime commands.

Live endpoints:

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
```

It validates transport input and returns JSON snapshots. It does not interpret the meaning of a stimulus.

### `create_development_server()`
Wraps an existing `SynrheonRuntime` in the local HTTP server. Tests use this to exercise the real transport boundary.

### `run_development_server()`
Starts the local development server at `http://127.0.0.1:8765`, opens the browser, and serves until stopped.

Future LLM, tool, vision, audio, web, or code interfaces may also enter through this outside-world boundary, but persistent cognition remains Synrheon-owned.

## `src/synrheon/time.py`
Placeholder for computational time and sequence ownership beyond the minimal Stage 0B trace timestamps.

## `src/synrheon/experience.py`
Placeholder for autobiographical event and evidence-lineage ownership.

## `src/synrheon/memory.py`
Placeholder for durable memory.

```text
memory exists
≠
memory strength
≠
current activation
```

## `src/synrheon/retrieval.py`
Placeholder for Level 1 → Level 2 → Level 3 retrieval and sparse relevance selection.

## `src/synrheon/scratchpad.py`
Placeholder for limited RAM-like working context.

## `src/synrheon/cognition.py`
Placeholder for real cognitive transformation:

```text
S(t) → S(t+1)
```

## `src/synrheon/problem_solving.py`
Placeholder for problem/model/plan/prediction/trial/outcome/failure-attribution/revision.

## `src/synrheon/learning.py`
Placeholder for prediction error, route usefulness, credit assignment, and adaptation.

## `src/synrheon/consolidation.py`
Placeholder for replay, repeated-pattern detection, and strategic compression.

## `src/synrheon/abstraction.py`
Placeholder for useful higher-order concept/structure formation.

## `src/synrheon/autonomy.py`
Placeholder for deciding whether unresolved internal state merits another cognitive cycle. Stage 0B Continue is only runtime cycling; it is not autonomous cognition.

# UI

## `ui/index.html`

**Plain English:** the verified development product shell and microscope.

### Chat
Shows external user stimuli sent to `/api/stimulus`.

The current harness does not fabricate Synrheon replies. Future language/output cognition can populate this conversation through the real organism path.

### Internal Thought
Shows Stage 0B trace plus explicit thoughts injected through `/api/thought`.

Injected thoughts are clearly identified as injections. They are not presented as self-generated Synrheon thought.

Future cognitive owners can expose structured internal activity here: active concepts, activation, retrieval paths, scratchpad state, predictions, uncertainty, learning changes, and autonomous thought.

### Organism controls
Start, Think One Step, Continue, and Pause all call the Python backend. JavaScript does not own the state change.

### State inspector
Shows status, cycle, event count, input count, and the complete returned state snapshot.

The browser polls `/api/state` so continued runtime cycles remain visible.

## `ui/README.md`
Documents the UI ownership boundary and current controls.

# Tests

## `tests/conftest.py`
Shared pytest setup location. No special fixtures yet.

## `tests/test_scaffold.py`
Contains the scaffold import check plus a small number of high-value Stage 0B tests.

The tests prove:

- the package still imports
- Start creates a real paused session
- external Chat and internal Thought remain distinct channels
- Think One Step advances exactly one cycle
- controls fail safely before Start
- empty stimuli do not mutate state
- the HTTP boundary reaches the actual runtime
- the backend serves the connected UI

These regression tests are now accompanied by successful human live-browser verification of the Stage 0B workflow.

# Data

## `data/README.md`
Explains future non-code runtime/experiment data ownership.

## `data/tiny_world.json`
Small deterministic future experiment world. It is not production cognition.

# Developer Scripts

## `scripts/synrheon.ps1`
Main PowerShell developer command.

```powershell
.\scripts\synrheon.ps1 setup
.\scripts\synrheon.ps1 run
.\scripts\synrheon.ps1 verify
.\scripts\synrheon.ps1 status
.\scripts\synrheon.ps1 context
```

`run` enters the verified Stage 0B development application through `python -m synrheon`.

## `scripts/context.ps1`
Creates a repository/context snapshot for a new AI thread.

## `scripts/run.ps1`
Shortcut for `synrheon.ps1 run`.

## `scripts/verify.ps1`
Shortcut for `synrheon.ps1 verify`.

# Current Information Flow

```text
Browser Chat ---------------------┐
                                 │
Browser Inject Thought -----------┤
                                 ↓
                           interfaces.py
                                 ↓
                           runtime.py
                                 ↓
                              core.py
                       OrganismState changes
                                 ↓
                         snapshot + trace
                                 ↓
                           interfaces.py
                                 ↓
                               Browser
```

This flow is live and verified as infrastructure. Deep cognitive owners still do not exist. As Stage 1 and later owners are implemented, runtime should route signals to them rather than absorbing their responsibilities.

# Maintenance Rule

Whenever meaningful code changes, keep this guide understandable to a non-programmer and explain:

```text
what the file does
what each important class/function does
what goes in
what comes out
what state it owns
what calls it
what it calls
what is live
what is still planned
```
