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

For a new human or coding-agent session:

```text
README.md
    ↓
docs/PROJECT_GUIDE.md      ← plain-English owner's manual
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

`docs/PROMPT_TEMPLATES.md` is optional human dispatch help; it is not workflow authority.

---

# Root Ownership

## `README.md`
Project purpose, cognitive vision, and long-term hypothesis.

## `AGENTS.md`
Short AI entry point that directs agents to the steward/workflow/project truth.

## `pyproject.toml`
Python package, dependency, testing, linting, and type-checking setup.

## `.gitignore`
Generated/local files Git should not save.

---

# Agent Ownership

## `agent/ARCHITECTURE_STEWARD.md`
How the primary development agent should think: broad-to-narrow, correct ownership, UI-first/live-organism proof, honest status.

## `.agents/skills/synrheon-development-workflow/SKILL.md`
Single canonical execution workflow for material Synrheon work.

## `.agents/skills/synrheon-development-workflow/openai.yaml`
OpenAI/Codex discovery metadata only.

## `.claude/skills/synrheon-development-workflow.md`
Thin Claude Code adapter pointing back to the canonical skill.

---

# Documentation Ownership

## `docs/PROJECT_GUIDE.md`
**Question:** What does every important file/piece mean in ordinary language?

Human-readable owner's manual. Update when file responsibility or meaningful internal structure changes.

## `docs/SIGNAL_FLOW.md`
**Question:** How does information actually move through Synrheon?

Owns current real flow plus clearly labeled planned flow. Update whenever runtime/UI/owner-to-owner wiring changes.

## `docs/ARCHITECTURE_PLAN.md`
**Question:** What should eventually exist and in what dependency order?

Current broad order:

```text
Architecture Stewardship
↓
Observable Runtime + Development UI
↓
Running Test Organism
↓
Cognitive Substrate
↓
Computational Time + Experience
↓
Memory + Sparse Activation
↓
Level 1 → Level 2 → Level 3 Retrieval
↓
Scratchpad + Recursive Cognition
↓
Problems + Trials + Solutions
↓
Learning + Plasticity
↓
Consolidation + Abstraction
↓
Multi-Layer Training
↓
Continuous Autonomous Cognition
↓
External Intelligence + Tools
```

## `docs/IMPLEMENTATION_STATUS.md`
**Question:** What actually exists and works?

Status vocabulary:

```text
Not Started
Designed
Built
Integrated
Verified
```

`Verified` requires real organism behavior/state/trace evidence, not tests alone.

## `docs/CURRENT_STAGE.md`
**Question:** What are we working on now?

Current: **Stage 0B — Observable Organism Harness**.

## `docs/DECISIONS.md`
Durable architecture choices already made.

## `docs/EXPERIMENTS.md`
Hypotheses, baseline, real stimulus/action, expected vs observed behavior, trace/state, interpretation.

## `docs/RESEARCH.md`
Outside ideas, math, neuroscience, donor mechanisms, prior art, open questions. Research is not implemented truth.

## `docs/PROMPT_TEMPLATES.md`
Human-facing prompt key for ChatGPT/Codex/Claude, including implementation, diagnosis, research, handoff, and manual Git prompts.

## `docs/SCAFFOLD.md`
This structural map and ownership key.

---

# Actual Organism Ownership

## `src/synrheon/runtime.py`
Thin sequencing/integration layer. May route and sequence; must not become primary cognition owner.

## `src/synrheon/core.py`
Lowest substrate: concepts, connections, activation, cognitive state.

## `src/synrheon/time.py`
Computational time/sequence owner.

## `src/synrheon/experience.py`
Autobiographical events and evidence lineage.

## `src/synrheon/memory.py`
Durable retained knowledge/experience. Keep existence, strength, and current activation separate.

## `src/synrheon/retrieval.py`
Level 1 → Level 2 → Level 3 relevance/reconstruction owner.

## `src/synrheon/scratchpad.py`
Limited RAM-like working context.

## `src/synrheon/cognition.py`
Current-state → next-state cognitive transformation owner.

## `src/synrheon/problem_solving.py`
Problem/model/plan/prediction/trial/outcome/failure-attribution/revised-plan/solution/lesson owner.

## `src/synrheon/learning.py`
Prediction error, route usefulness, credit assignment, future adaptation.

## `src/synrheon/consolidation.py`
Replay, repeated-pattern detection, strategic compression, evidence lineage.

## `src/synrheon/abstraction.py`
Useful higher-order representation formation.

## `src/synrheon/autonomy.py`
Whether/why cognition continues without new external input.

## `src/synrheon/interfaces.py`
Boundary to user/LLMs/tools/vision/audio/web/code. External systems contribute; they do not own persistent cognition.

## `src/synrheon/__main__.py`
Application/developer entry point; delegates to runtime.

## `src/synrheon/__init__.py`
Package identity/version. Keep small.

---

# UI Ownership

`ui/` is Synrheon's development microscope/control surface.

Initial Stage 0B targets:

```text
Start
Send Stimulus
Think One Step
Continue
Pause
Inspect Current State
Inspect Trace
```

The UI must not own cognition.

---

# Test Ownership

`tests/` protects discovered behavior/contracts.

Prefer meaningful owner behavior, cross-owner integration, runtime reachability, and live-organism evidence over large numbers of trivial tests.

---

# Data Ownership

`data/` holds non-code experiment/runtime data. Create deeper data folders only when a real mechanism needs them.

---

# Script Ownership

## `scripts/synrheon.ps1`
Main developer command:

```powershell
.\scripts\synrheon.ps1 setup
.\scripts\synrheon.ps1 run
.\scripts\synrheon.ps1 verify
.\scripts\synrheon.ps1 status
.\scripts\synrheon.ps1 context
```

## `scripts/context.ps1`
Generates a repository/context snapshot for a new AI thread; supports printing, `-Copy`, and `-OutFile`.

## `scripts/run.ps1`
Tiny wrapper for `synrheon.ps1 run`.

## `scripts/verify.ps1`
Tiny wrapper for `synrheon.ps1 verify`.

---

# Ownership Summary

```text
WHY THE PROJECT EXISTS
README.md

HOW THE AI SHOULD THINK
a gent/ARCHITECTURE_STEWARD.md

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

WHAT WE ARE INVESTIGATING
docs/RESEARCH.md

HUMAN PROMPT DISPATCH
docs/PROMPT_TEMPLATES.md

WHERE EVERYTHING IS
docs/SCAFFOLD.md

WHAT ACTUALLY THINKS
src/synrheon/*.py

WHAT SEQUENCES THE ORGANISM
src/synrheon/runtime.py

WHAT LETS YOU WATCH / CONTROL IT
ui/

WHAT COMMAND YOU USE LOCALLY
scripts/synrheon.ps1

WHAT CREATES A NEW-CHAT REPOSITORY SNAPSHOT
scripts/context.ps1
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
