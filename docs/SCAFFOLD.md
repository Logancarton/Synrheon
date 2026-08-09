# Synrheon Scaffold

This is the structural map and ownership key for the Synrheon repository.

Use it to answer:

```text
What files exist?
Where are they?
What does each major surface own?
Where should a new behavior or document go?
```

Keep the repository compact. Add files/folders only when real architecture or implementation needs them.

---

# Repository Map

```text
Synrheon/
├── .agents/
│   └── skills/
│       └── synrheon-development-workflow/
│           ├── SKILL.md
│           └── openai.yaml
├── .claude/
│   └── skills/
│       └── synrheon-development-workflow.md
├── agent/
│   └── ARCHITECTURE_STEWARD.md
├── data/
│   ├── README.md
│   └── tiny_world.json
├── docs/
│   ├── ARCHITECTURE_PLAN.md
│   ├── CURRENT_STAGE.md
│   ├── DECISIONS.md
│   ├── EXPERIMENTS.md
│   ├── IMPLEMENTATION_STATUS.md
│   ├── PROJECT_GUIDE.md
│   ├── PROMPT_TEMPLATES.md
│   ├── RESEARCH.md
│   ├── SCAFFOLD.md
│   └── SIGNAL_FLOW.md
├── scripts/
│   ├── context.ps1
│   ├── run.ps1
│   ├── synrheon.ps1
│   └── verify.ps1
├── src/
│   └── synrheon/
│       ├── __init__.py
│       ├── __main__.py
│       ├── abstraction.py
│       ├── autonomy.py
│       ├── cognition.py
│       ├── consolidation.py
│       ├── core.py
│       ├── experience.py
│       ├── interfaces.py
│       ├── learning.py
│       ├── memory.py
│       ├── problem_solving.py
│       ├── retrieval.py
│       ├── runtime.py
│       ├── scratchpad.py
│       └── time.py
├── tests/
│   ├── conftest.py
│   └── test_scaffold.py
├── ui/
│   ├── README.md
│   └── index.html
├── .gitignore
├── AGENTS.md
├── pyproject.toml
└── README.md
```

---

# Fast Orientation

```text
README.md
    ↓
docs/PROJECT_GUIDE.md
    ↓
AGENTS.md
    ↓
agent/ARCHITECTURE_STEWARD.md
    ↓
.agents/skills/synrheon-development-workflow/SKILL.md
    ↓
docs/SCAFFOLD.md
    ↓
docs/ARCHITECTURE_PLAN.md
    ↓
docs/IMPLEMENTATION_STATUS.md
    ↓
docs/CURRENT_STAGE.md
    ↓
docs/SIGNAL_FLOW.md when live wiring is involved
    ↓
affected source files
    ↓
relevant tests / live organism
```

---

# Documentation Ownership

`docs/PROJECT_GUIDE.md` — plain-English owner's manual.

`docs/SIGNAL_FLOW.md` — current real information flow plus clearly labeled planned flow.

`docs/ARCHITECTURE_PLAN.md` — future architecture and cognitive dependency order.

`docs/IMPLEMENTATION_STATUS.md` — what actually exists and works.

`docs/CURRENT_STAGE.md` — current active boundary.

Current: **Stage 1 — Trainable Cognition Pivot**.

`docs/DECISIONS.md` — durable architecture choices.

`docs/EXPERIMENTS.md` — hypotheses, baselines, observed results, failures, and preregistered tests.

`docs/RESEARCH.md` — outside ideas/research only.

`docs/PROMPT_TEMPLATES.md` — human-facing dispatch prompts.

---

# Actual Organism Ownership

## `src/synrheon/runtime.py`

Thin sequencing/integration layer.

Current textual stimulus flow:

```text
record time
 ↓
record ordered experience
 ↓
record stimulus / trace
 ↓
return state
```

Runtime does **not** currently invoke a hand-written cognitive policy.

## `src/synrheon/core.py`

Lowest substrate representations:
- concepts
- world relations
- open-ended organism relations
- activation representation
- top-level organism state

Core stores/validates state. It does not choose cognitive routes.

## `src/synrheon/cognition.py`

Reserved owner for future current-state → next-state cognitive transformation.

Current status:

```text
trainable cognitive policy owner
implementation intentionally absent
```

The previous lexical matching / fixed spreading / decay / inhibition / Top-K mechanism was experimental and has been removed from production.

Future cognition should learn useful state/action transitions rather than rebuild those fixed rules.

## `src/synrheon/time.py`
Computational time/sequence owner.

## `src/synrheon/experience.py`
Autobiographical events, ordering, and evidence lineage.

## `src/synrheon/memory.py`
Future durable retained knowledge/experience.

## `src/synrheon/retrieval.py`
Future Level 1 → Level 2 → Level 3 retrieval owner.

## `src/synrheon/scratchpad.py`
Future limited RAM-like working context/checkpoints.

## `src/synrheon/problem_solving.py`
Future problem/model/plan/prediction/trial/outcome/revision owner.

## `src/synrheon/learning.py`
Future prediction error, route usefulness, credit assignment, and trainable cognitive-policy updates.

## `src/synrheon/consolidation.py`
Future replay, pattern detection, strategic compression.

## `src/synrheon/abstraction.py`
Future higher-order representation formation.

## `src/synrheon/autonomy.py`
Future decision whether/why cognition continues without new external input.

## `src/synrheon/interfaces.py`
Browser/outside-world transport only.

---

# UI Ownership

`ui/` remains Synrheon's development microscope/control surface.

Current live surfaces:

```text
Start / Step / Continue / Pause
Chat stimulus
Internal Thought injection
Knowledge injection
Experience thread
Current state / trace
```

The UI must not own cognition.

A future learned cognitive policy may expose explicit checkpoints/state transitions here, but JavaScript must only display backend-owned state.

---

# Test Ownership

`tests/` protects discovered behavior/contracts.

Current regression priorities:
- Stage 0B transport remains connected
- observed/injected experience provenance remains distinct
- temporal sequence and links remain correct
- open-ended organism relation representation stays non-hardcoded
- invalid knowledge fails safely
- Chat does not mutate cognitive state through a hand-written thinking policy
- UI/API still reaches the real runtime

Future trainable-policy tests must prove transfer to unseen knowledge worlds, not merely training-set accuracy.

---

# Data Ownership

`data/` holds non-code experiment/runtime data. Create deeper data folders only when a real mechanism needs them.

---

# Script Ownership

```powershell
.\scripts\synrheon.ps1 setup
.\scripts\synrheon.ps1 run
.\scripts\synrheon.ps1 verify
.\scripts\synrheon.ps1 status
.\scripts\synrheon.ps1 context
```

`verify` runs pytest, compileall, `git diff --check`, and Git status. Live cognitive verification still requires observing the organism.

---

# Ownership Summary

```text
WHY THE PROJECT EXISTS
README.md

HOW THE AI SHOULD THINK
agent/ARCHITECTURE_STEWARD.md

HOW WORK SHOULD BE EXECUTED
.agents/skills/synrheon-development-workflow/SKILL.md

PLAIN-ENGLISH CODE / FILE GUIDE
docs/PROJECT_GUIDE.md

HOW INFORMATION MOVES
docs/SIGNAL_FLOW.md

WHAT SHOULD EXIST
docs/ARCHITECTURE_PLAN.md

WHAT REALLY EXISTS
docs/IMPLEMENTATION_STATUS.md

WHAT WE ARE DOING NOW
docs/CURRENT_STAGE.md

WHAT WE DECIDED
docs/DECISIONS.md

WHAT WE OBSERVED
docs/EXPERIMENTS.md

WHERE EVERYTHING IS
docs/SCAFFOLD.md

FUTURE TRAINABLE THINKING OWNER
src/synrheon/cognition.py

BASIC COGNITIVE STATE
src/synrheon/core.py

SEQUENCING
src/synrheon/runtime.py

OBSERVATION / CONTROL
ui/
```

---

# Structural Rule

Prefer:

```text
one clear responsibility
↓
one understandable file
↓
real complexity appears
↓
split only when justified
```

Avoid creating files/folders merely because they may be useful someday.
