# Synrheon Signal Flow

This document separates **CURRENT REAL FLOW** from **PLANNED / INTENDED FLOW**.

# 1. Current Real Flow — Stage 0B

Synrheon now has a connected development-organism path in code.

Startup:

```text
PowerShell
.\scripts\synrheon.ps1 run
        ↓
python -m synrheon
        ↓
src/synrheon/__main__.py
        ↓
runtime.main()
        ↓
SynrheonRuntime created
        ↓
interfaces.run_development_server(runtime)
        ↓
local HTTP server
        ↓
browser opens http://127.0.0.1:8765
```

Browser command path:

```text
Browser control / input
        ↓
HTTP endpoint in interfaces.py
        ↓
SynrheonRuntime method
        ↓
OrganismState changes
        ↓
JSON state snapshot + trace
        ↓
interfaces.py
        ↓
Browser renders returned state
```

JavaScript does not own the organism state.

# 2. Current State Ownership

`core.py` currently owns the minimal Stage 0B `OrganismState`.

It contains:

```text
session_id
status: off / paused / running
cycle
event_sequence
external/internal stimulus records
trace events
```

This is in-memory session state only. It is not durable memory and does not survive process restart.

# 3. Current Chat Flow

```text
Chat tab
 ↓
POST /api/stimulus
 ↓
interfaces.py validates transport
 ↓
runtime.send_external_stimulus()
 ↓
StimulusRecord(kind="external")
 ↓
OrganismState
 ↓
snapshot
 ↓
Chat tab
```

No semantic interpretation or reply generation occurs yet.

# 4. Current Internal Thought Flow

```text
Internal Thought tab
 ↓
user explicitly injects thought
 ↓
POST /api/thought
 ↓
interfaces.py validates transport
 ↓
runtime.inject_internal_thought()
 ↓
StimulusRecord(kind="internal")
 ↓
OrganismState + trace
 ↓
snapshot
 ↓
Internal Thought tab
```

An injected thought is not presented as self-generated Synrheon cognition.

The Internal Thought view also shows runtime trace events. Future structured cognitive activity can use the same observation surface.

# 5. Current Control Flow

## Start

```text
UI Start
 ↓
POST /api/start
 ↓
runtime.start()
 ↓
fresh OrganismState session
status = paused
cycle = 0
 ↓
session_started trace
 ↓
snapshot → UI
```

## Think One Step

```text
UI Think One Step
 ↓
POST /api/step
 ↓
runtime.think_one_step()
 ↓
cycle += 1 exactly once
 ↓
cycle_advanced trace
 ↓
snapshot → UI
```

This is an observable harness cycle, not real cognition yet.

## Continue

```text
UI Continue
 ↓
POST /api/continue
 ↓
status = running
 ↓
background runtime worker
 ↓
repeated observable cycle advancement
 ↓
browser polls /api/state
 ↓
updated cycle + trace visible
```

## Pause

```text
UI Pause
 ↓
POST /api/pause
 ↓
status = paused
 ↓
background worker stops advancing cycles
 ↓
current state remains inspectable
```

# 6. Current Ownership Boundary

```text
UI
controls + displays

interfaces.py
HTTP/browser transport

runtime.py
session sequencing + control routing

core.py
minimal Synrheon-owned observable state
```

There is still no implemented memory, retrieval, semantic understanding, learning, abstraction, or autonomous cognition.

# 7. Planned Cognitive Flow

This remains intended architecture, not current implementation.

```text
EXTERNAL STIMULUS
        ↓
interfaces.py
        ↓
runtime.py
        ↓
time.py
        ↓
experience.py
        ↓
core.py
        ↓
cognition.py
        ↓
   ┌────┴─────────────────────┐
   ↓                          ↓
retrieval.py          problem_solving.py
   ↓                          ↓
memory.py                  prediction /
   ↓                       trial / model
scratchpad.py                 ↓
   └──────────┬───────────────┘
              ↓
         new cognitive state
              ↓
           runtime
              ↓
      interfaces / UI output
              ↓
        OUTCOME / FEEDBACK
              ↓
        experience.py
              ↓
         learning.py
```

Longer timescales:

```text
accumulated experience
        ↓
consolidation.py
        ↓
patterns / compression
        ↓
abstraction.py
        ↓
future cognition / retrieval / prediction
```

Autonomous continuation later becomes:

```text
unresolved internal state
        ↓
autonomy.py
continue?
        ↓ yes
runtime.py
        ↓
next real cognitive cycle
        ↓
cognition.py
```

Stage 0B Continue must not be confused with this future autonomous decision.

# 8. Planned Retrieval Flow

```text
current cue / problem
        ↓
retrieval.py
Level 1 coarse orientation
        ↓
Level 2 relevant situation / episode / concept region
        ↓
Level 3 detailed evidence / relationships
        ↓
memory.py retained material
        ↓
scratchpad active packages
        ↓
cognition.py
```

# 9. Planned Learning Flow

```text
problem
 ↓
model
 ↓
plan
 ↓
prediction
 ↓
trial
 ↓
outcome
 ↓
prediction error
 ↓
causal attribution
 ↓
learning.py
 ↓
future usefulness / selection changes
```

Failed reasoning must not automatically mark all participating memories false.

# 10. Planned LLM / External Intelligence Flow

```text
Synrheon needs outside help
        ↓
interfaces.py
        ↓
LLM / tool
        ↓
candidate interpretation / information / hypothesis
        ↓
interfaces.py
        ↓
Synrheon evaluates and retains it under Synrheon-owned rules
```

External intelligence may participate without becoming the sole persistent cognition owner.

# 11. Trace Boundary

The Stage 0B trace currently records observable harness events such as session start, inputs, pause/continue, and cycle advancement.

Later trace should expose enough structured state to understand owner handoffs and behavior without moving cognition into the UI.

# 12. Maintenance Rule

Update CURRENT REAL FLOW whenever the live call path changes. Keep future architecture under PLANNED / INTENDED FLOW until the real runtime reaches it.
