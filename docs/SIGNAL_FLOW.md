# Synrheon Signal Flow

This document explains how information moves through Synrheon.

It must always separate:

```text
CURRENT REAL FLOW
from
INTENDED / PLANNED FLOW
```

A diagram here is not proof that the code already behaves that way. When runtime wiring changes, this document should change with it.

---

# 1. Current Real Flow — Stage 0B Scaffold

Synrheon does **not** yet have a live cognitive signal loop.

Current Python execution:

```text
PowerShell
.\scripts\synrheon.ps1 run
        ↓
python -m synrheon
        ↓
src/synrheon/__main__.py
        ↓
imports main() from runtime.py
        ↓
runtime.main()
        ↓
prints scaffold message
        ↓
process ends
```

That is the actual implemented organism path right now.

There is no persistent cognitive state yet, no thought loop, no memory/retrieval/learning path, and no UI-to-runtime connection.

---

# 2. Current UI Flow

Current `ui/index.html` is a static development scaffold.

```text
Browser opens ui/index.html
        ↓
shows development page
        ↓
Start             disabled
Think One Step    disabled
Continue          disabled
Pause             disabled
Stimulus           disabled
        ↓
Current State says "Not connected."
Trace says "No cognitive trace yet."
```

No signal currently leaves the UI. No Synrheon owner receives a UI command.

This is **Built as a visual scaffold**, not Integrated into the organism.

---

# 3. Developer Control Flow

The PowerShell control script is development infrastructure, not cognition.

```text
YOU
 ↓
scripts/synrheon.ps1
 ↓
command selector
 ├─ setup
 ├─ run
 ├─ verify
 ├─ status
 └─ context
```

## setup

```text
you
 ↓
synrheon.ps1 setup
 ↓
find/create .venv
 ↓
upgrade pip
 ↓
install Synrheon + dev tools
```

## run

```text
you
 ↓
synrheon.ps1 run
 ↓
python -m synrheon
 ↓
__main__.py
 ↓
runtime.main()
```

## verify

```text
you
 ↓
synrheon.ps1 verify
 ├─ pytest
 ├─ compileall
 ├─ git diff --check
 └─ git status
```

This protects engineering integrity. It is not the cognitive verification path.

## status

```text
you
 ↓
synrheon.ps1 status
 ↓
reads Git + CURRENT_STAGE
 ↓
prints project status
```

## context

```text
you
 ↓
synrheon.ps1 context
 ↓
scripts/context.ps1
 ↓
collects Git + project-truth state
 ↓
prints / copies / saves snapshot
 ↓
new AI chat
```

---

# 4. Stage 0B Target Flow

The first real organism flow should become:

```text
YOU
 ↓
Development UI
 ↓
command/stimulus boundary
 ↓
THIN RUNTIME
 ↓
current Synrheon state
 ↓
one allowed operation
 ↓
new Synrheon state
 ↓
trace + state snapshot
 ↓
runtime
 ↓
Development UI
 ↓
YOU inspect what actually happened
```

The exact browser-to-Python transport is not yet chosen.

Whatever transport is chosen, ownership must stay:

```text
UI
controls + displays

runtime
sequences + routes

cognitive owner
actually changes cognitive state
```

---

# 5. Target Stage 0B Control Signals

## Start

```text
UI Start
 ↓
runtime starts organism session
 ↓
initial state exists
 ↓
state/trace returned to UI
```

## Send Stimulus

```text
UI stimulus
 ↓
external input boundary
 ↓
runtime receives handoff
 ↓
appropriate owner(s) receive stimulus
 ↓
state changes
 ↓
trace returned
```

At Stage 0B, the cognitive transformation can still be minimal. The important thing is that the path is real and observable.

## Think One Step

```text
UI Think One Step
 ↓
runtime performs exactly one cognitive cycle
 ↓
owner state changes once
 ↓
runtime stops
 ↓
UI shows before/after state + trace
```

## Continue

```text
UI Continue
 ↓
runtime repeatedly advances cognitive cycles
 ↓
state evolves
 ↓
trace accumulates
 ↓
UI remains observable
```

## Pause

```text
UI Pause
 ↓
runtime stops future cycles
 ↓
current state remains inspectable
```

---

# 6. Future Cognitive Signal Flow — Conceptual

This is intended architecture, **not current implementation**. Sparse activation means not every owner participates in every cycle.

```text
EXTERNAL STIMULUS
        ↓
interfaces.py
outside-world boundary
        ↓
runtime.py
sequence / route
        ↓
time.py
assign when + sequence
        ↓
experience.py
record what happened
        ↓
core.py
update representational/activation state
        ↓
cognition.py
choose useful next cognitive operation
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
              ↓
 future route/weight/usefulness change
```

Longer-timescale flow:

```text
accumulated experience
        ↓
consolidation.py
        ↓
patterns / compressed structures
        ↓
abstraction.py
        ↓
higher-order concepts
        ↓
future cognition / retrieval / prediction
```

Autonomous continuation:

```text
unresolved internal state
        ↓
autonomy.py
continue?
        ↓ yes
runtime.py
        ↓
next cognitive cycle
        ↓
cognition.py
```

---

# 7. Ownership Flow in Plain English

`interfaces.py` — What came from outside, and what goes back outside?

`runtime.py` — Which owner acts now, and in what order?

`time.py` — When did this happen, and where is it in sequence?

`experience.py` — What happened?

`core.py` — What internal things, relationships, and activation currently exist?

`memory.py` — What has been retained?

`retrieval.py` — What retained information is relevant now?

`scratchpad.py` — What should remain immediately available in working thought?

`cognition.py` — What cognitive transformation should happen next?

`problem_solving.py` — What problem are we working on, what have we tried, and what variable should change next?

`learning.py` — What should future cognition do differently because of this outcome?

`consolidation.py` — What recurring experience should be replayed, compressed, or strengthened over time?

`abstraction.py` — What useful higher-level concept or structure can be formed from repeated evidence?

`autonomy.py` — Should cognition continue without another external prompt?

---

# 8. Memory / Retrieval Flow

Planned flow:

```text
current cue / problem
        ↓
retrieval.py
Level 1 coarse orientation
        ↓
small relevant region
        ↓
Level 2 situation / episode / concept cluster
        ↓
smaller relevant region
        ↓
Level 3 detailed evidence / relationships
        ↓
memory.py provides retained material
        ↓
scratchpad receives useful active packages
        ↓
cognition uses them
```

Important:

```text
retrieval chooses what to reactivate
memory owns what is retained
```

---

# 9. Problem-Solving Feedback Flow

Planned flow:

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
failure/success attribution
 ↓
learning.py
 ↓
change usefulness / future selection
 ↓
problem_solving.py
changes most likely causal variable
 ↓
new plan
```

The goal is not:

```text
trial failed → throw everything away
```

It is:

```text
trial failed
↓
identify most likely wrong variable
↓
change that variable first
↓
preserve useful parts of prior reasoning
```

---

# 10. Learning / Consolidation Timescales

Planned high-level flow:

```text
FAST
single thought / seconds
activation + working state
        ↓
SHORT
minutes / active problem
temporary route usefulness
        ↓
MEDIUM
hours / days
episode organization + repeated success/failure
        ↓
SLOW
days / weeks
consolidation + pattern discovery
        ↓
STRATEGIC
longer term
deeper model / representation training
```

Not every thought should rewrite the deepest model.

---

# 11. LLM / External Intelligence Flow

Planned boundary:

```text
Synrheon needs outside reasoning/language help
        ↓
interfaces.py
        ↓
LLM / external tool
        ↓
candidate interpretation / information / hypothesis
        ↓
interfaces.py
        ↓
Synrheon evaluates and stores it under its own rules
```

The LLM should not become Synrheon's persistent memory, identity owner, truth database, or only reasoning process.

---

# 12. Observable Trace Flow

As the UI grows, each meaningful cognitive cycle should expose enough to understand:

```text
what triggered the step
what owner acted
what information it received
what information it returned
what state changed
what memory/retrieval path was used
what uncertainty existed
what action/result occurred
what feedback came back
what learning changed
```

The trace should help answer "Why did Synrheon do that?" without placing the reasoning itself inside the UI.

---

# 13. Maintenance Rule

Update this file whenever a live call path changes, a new owner enters runtime, UI command types change, state/trace handoffs change, memory/retrieval wiring changes, learning feedback begins flowing, autonomous continuation is wired, or an LLM/tool becomes part of the real path.

For every change, keep **CURRENT REAL FLOW** separate from **PLANNED FLOW**.
