# Synrheon Project Guide — Plain English

This is the human-readable owner's manual for Synrheon. It is written so the project can be understood without needing to be a programmer.

Use it to answer:

```text
What does this file do?
Why does it exist?
What are the important pieces inside it?
What calls it?
What does it call?
Is this real behavior yet or only planned?
```

Always distinguish **current real behavior** from **planned responsibility**.

---

# Quick Mental Model

```text
YOU
 ↓
Development UI
 ↓
Runtime
 ↓
Cognitive owners
 ↓
State changes
 ↓
Runtime
 ↓
UI / trace
 ↓
YOU
```

Think of the main layers this way:

```text
UI       = dashboard / microscope
runtime  = traffic controller
src/     = the parts intended to actually think, remember, retrieve, learn, etc.
docs/    = project truth and explanation
tests/   = regression protection
scripts/ = developer convenience
```

The UI should not think for Synrheon. The runtime should not think for Synrheon. Each cognitive responsibility should have a clear owner.

---

# A Few Coding Words

## Function
A named action. Example: `main()` means "run the instructions inside this action."

## Class
A blueprint for a kind of thing, such as a future `Concept`, `Memory`, or `CognitiveState`.

## Variable
A named place that holds information.

## Import
Means "use something owned by another file."

## Return
What a function gives back after it finishes.

## Test
Code that checks expected behavior. In Synrheon, tests protect contracts but do not by themselves prove the whole organism works.

---

# Current Project Status

Current stage:

```text
Stage 0B — Observable Organism Harness
```

Immediate goal:

```text
thin runtime
+
development UI
+
Start
+
Send Stimulus
+
Think One Step
+
Continue
+
Pause
+
Current State
+
Trace
```

Most cognitive source files are currently placeholders that define ownership but contain little or no executable cognition. That is intentional.

---

# Root Files

## `README.md`

**Plain English:** Why Synrheon exists and the long-term cognitive hypothesis.

Owns the big-picture vision: persistent cognition, time, memory, sparse activation, hierarchical retrieval, recursive thought, learning, abstraction, and eventual autonomous continuation.

Do not use it as a daily progress log.

## `AGENTS.md`

**Plain English:** Front-door sign for coding AIs.

It tells an agent what to read first and points it toward the Architecture Steward and canonical workflow.

Keep it short.

## `pyproject.toml`

**Plain English:** Python project setup.

Important sections:

- `[build-system]` — how Python builds/installs the project.
- `[project]` — project name, version, Python requirement, runtime dependencies.
- `[project.optional-dependencies] dev` — development tools such as pytest, ruff, mypy.
- `[tool.setuptools.packages.find]` — says Python code lives under `src/`.
- `[tool.pytest.ini_options]` — test configuration.
- `[tool.ruff]` — lint/code-style configuration.
- `[tool.mypy]` — type-checking configuration.

## `.gitignore`

**Plain English:** Tells Git what not to save.

Examples: `.venv`, caches, compiled Python files, local environment files, runtime/checkpoint/cache output.

---

# Agent / AI Workflow Files

## `agent/ARCHITECTURE_STEWARD.md`

**Plain English:** Defines how the main development AI should think about Synrheon.

Important sections:

- Canonical Repository — where Synrheon belongs.
- Primary Development Principle — bottom-up but observable from the beginning.
- Startup Sequence — what project truth to read before changes.
- Status Vocabulary — Not Started / Designed / Built / Integrated / Verified.
- Cognitive Effect — Infrastructure / Supporting cognition / Cognitive improvement.
- Broad-to-Narrow Review — find the underlying bottleneck instead of patching one example.
- UI-First Rule — build the running test organism before deep cognition.
- Runtime Principle — keep runtime thin.
- Documentation Synchronization — keep project truth current.

## `.agents/skills/synrheon-development-workflow/SKILL.md`

**Plain English:** The master work procedure.

The Architecture Steward says **how to think**. This skill says **how to execute**.

Its standard flow is roughly:

```text
read project truth
↓
identify real bottleneck
↓
compare mechanisms
↓
choose correct owner
↓
define live experiment
↓
observe baseline
↓
implement
↓
wire real runtime
↓
observe live behavior
↓
add regression tests
↓
update docs
↓
review diff
↓
commit/push verified work
```

## `.agents/skills/synrheon-development-workflow/openai.yaml`

**Plain English:** OpenAI/Codex discovery metadata for the canonical skill.

It contains the display name, short description, default prompt, and invocation policy. It does not own the workflow rules.

## `.claude/skills/synrheon-development-workflow.md`

**Plain English:** Thin Claude Code adapter.

It tells Claude to load the same canonical `SKILL.md` rather than inventing a separate Claude workflow.

---

# Project-Truth Documents

## `docs/SCAFFOLD.md`

**Plain English:** Repository map and ownership key — where everything is and what each major area owns.

## `docs/PROJECT_GUIDE.md`

**Plain English:** This file. The non-programmer owner's manual.

Update it when a meaningful file responsibility, class, function, command, UI control, or major section changes.

## `docs/SIGNAL_FLOW.md`

**Plain English:** How information moves through Synrheon.

It must always separate **CURRENT REAL FLOW** from **PLANNED / INTENDED FLOW**.

## `docs/ARCHITECTURE_PLAN.md`

**Plain English:** What major systems should eventually exist and what depends on what.

It is future architecture, not proof that the features are already live.

## `docs/IMPLEMENTATION_STATUS.md`

**Plain English:** Reality check.

Answers:

```text
What is only designed?
What has code?
What is connected to the live runtime?
What has actually been demonstrated?
```

Important rule:

```text
Built ≠ Integrated ≠ Verified
```

## `docs/CURRENT_STAGE.md`

**Plain English:** What we are working on right now.

Current focus is Stage 0B — the observable running organism.

## `docs/DECISIONS.md`

**Plain English:** Memory of architectural choices already made so they are not repeatedly reopened without new evidence.

## `docs/EXPERIMENTS.md`

**Plain English:** What we actually tried and what happened.

A useful experiment records hypothesis, baseline, stimulus, expected behavior, actual behavior, relevant state/trace, and interpretation.

## `docs/RESEARCH.md`

**Plain English:** Research notebook for papers, neuroscience ideas, math, donor mechanisms, prior art, and unresolved questions.

Research is not implementation truth.

## `docs/PROMPT_TEMPLATES.md`

**Plain English:** Prompt key for directing ChatGPT, Codex, Claude Code, or another agent without repeating the entire workflow every time.

---

# Actual Python Organism

Everything under `src/synrheon/` is intended to become the actual cognitive organism.

## `src/synrheon/__init__.py`

**Current real behavior:** Stores package identity and `__version__ = "0.0.1"`.

Keep it small.

## `src/synrheon/__main__.py`

**Current real behavior:** Entry point for:

```powershell
python -m synrheon
```

Important pieces:

- `from synrheon.runtime import main` — gets the startup function from `runtime.py`.
- `if __name__ == "__main__": main()` — runs that startup function when Synrheon is launched directly.

Current flow:

```text
python -m synrheon
↓
__main__.py
↓
runtime.main()
```

## `src/synrheon/runtime.py`

**Plain English:** Traffic controller / live integration layer.

**Current real behavior:** `main()` only prints a scaffold message and exits.

**Planned responsibility:** receive stimuli, sequence owners, advance one cognitive step, continue/pause recursion, expose state/trace.

Must not own memory, retrieval, learning, abstraction, or problem-solving intelligence.

## `src/synrheon/core.py`

**Plain English:** Lowest-level cognitive substrate owner.

**Current:** placeholder only.

**Planned:** concepts, connections, activation, cognitive state.

## `src/synrheon/time.py`

**Plain English:** Computational sense of when things happen.

**Current:** placeholder only.

**Planned:** absolute time, sequence number, relative/elapsed time, before/after, episode/day position, recent trajectory.

## `src/synrheon/experience.py`

**Plain English:** Synrheon's autobiography — what actually happened externally and internally.

**Current:** placeholder only.

**Planned:** external events, internal thought events, event ordering, episode membership, evidence lineage.

## `src/synrheon/memory.py`

**Plain English:** Durable retained knowledge and experience.

Important distinction:

```text
memory exists
≠
memory is strong
≠
memory is currently active
```

**Current:** placeholder only.

## `src/synrheon/retrieval.py`

**Plain English:** Decides what retained information is relevant now.

**Current:** placeholder only.

**Planned initial cascade:** Level 1 coarse orientation → Level 2 relevant situation/episode/concept region → Level 3 detailed reconstruction.

## `src/synrheon/scratchpad.py`

**Plain English:** Limited RAM-like working state.

**Current:** placeholder only.

**Planned initial bands:** current situation up to 3 packages; last hour up to 2; last day up to 3.

## `src/synrheon/cognition.py`

**Plain English:** Owns the transformation from current cognitive state toward the next state.

Conceptually:

```text
S(t) → S(t+1)
```

**Current:** placeholder only.

**Planned:** candidate cognitive operations, competition, uncertainty, next-state transformation.

## `src/synrheon/problem_solving.py`

**Plain English:** Keeps the problem, model, plan, prediction, trial, outcome, failure attribution, revised plan, solution, and lesson together.

**Current:** placeholder only.

Important rule: a failed route does not make every participating memory false.

## `src/synrheon/learning.py`

**Plain English:** What should future cognition do differently because something worked or failed?

**Current:** placeholder only.

**Planned:** prediction error, route usefulness, credit assignment, reinforcement/weakening, future adjustment.

## `src/synrheon/consolidation.py`

**Plain English:** Longer-timescale replay, pattern detection, and strategic compression while preserving evidence lineage.

**Current:** placeholder only.

## `src/synrheon/abstraction.py`

**Plain English:** Formation of useful higher-level concepts/structures from repeated evidence.

**Current:** placeholder only.

## `src/synrheon/autonomy.py`

**Plain English:** Decides whether Synrheon should keep thinking without another external prompt.

**Current:** placeholder only.

**Planned:** unresolved goals, continue/pause, resource limits, fixation prevention.

## `src/synrheon/interfaces.py`

**Plain English:** Border between Synrheon and outside systems such as users, LLMs, vision, audio, web, and code tools.

**Current:** placeholder only.

External systems may contribute information or reasoning but should not silently become Synrheon's persistent memory, identity, or learning owner.

---

# UI

## `ui/index.html`

**Current real behavior:** Static development scaffold only. Controls are disabled and not connected to Python.

Important visible pieces:

- Start
- Think One Step
- Continue
- Pause
- stimulus text area / Send
- Current State panel
- Trace panel

These are currently visual placeholders.

## `ui/README.md`

Explains the UI boundary: microscope/control panel, not cognition owner.

---

# Tests

## `tests/conftest.py`

Shared pytest setup location. Currently only documentation; no shared fixtures yet.

## `tests/test_scaffold.py`

**Current real behavior:** Imports every Synrheon module and checks version `0.0.1`.

This proves the scaffold imports. It does **not** prove cognition.

---

# Data

## `data/README.md`

Explains future non-code data ownership. Avoids creating unnecessary data folders before a mechanism actually needs them.

## `data/tiny_world.json`

Small deterministic pretend world for future early experiments. Contains sample concepts and relationships such as Logan, Daisy, person, dog, walk, leash, and door.

It is experiment data, not production cognition.

---

# Developer Scripts

## `scripts/synrheon.ps1`

**Plain English:** Main PowerShell control command.

Top command choices:

```text
help
setup
run
verify
status
context
```

Important pieces:

- `$RepoRoot` — local Synrheon directory.
- `$CanonicalRepo` — official GitHub repository.
- `$VenvPython` — Python inside `.venv`.
- `Get-PythonCommand` — finds the Python executable.
- `Test-GitRepo` — checks for the local Git repository.
- `Normalize-GitRemote` — treats equivalent GitHub remote forms consistently.
- `Test-HasCommit` — detects whether the branch has a commit yet.
- `Show-Help` — prints the menu.
- `Invoke-Setup` — creates `.venv` and installs development dependencies.
- `Invoke-Run` — runs `python -m synrheon`.
- `Invoke-Verify` — runs automated support checks.
- `Invoke-Status` — shows current stage and Git status.
- final `switch` — sends the command you typed to the correct function.

## `scripts/context.ps1`

**Plain English:** Creates a copy-paste repository snapshot for a new AI thread.

Important pieces:

- `-Copy` — copy snapshot to clipboard.
- `-OutFile` — save snapshot to a file.
- `Add-Section` — creates titled snapshot blocks.
- `Invoke-GitText` — runs Git commands and converts output to text.
- Git identity/status — branch, HEAD, origin, changes, recent commits.
- project-truth sections — current stage and implementation status.
- key-file check — verifies important project files exist.
- Python section — shows which Python environment is being used.

## `scripts/run.ps1`

Tiny shortcut for `scripts/synrheon.ps1 run`.

## `scripts/verify.ps1`

Tiny shortcut for `scripts/synrheon.ps1 verify`.

---

# How the Files Relate

```text
README                 WHY
ARCHITECTURE_PLAN      WHAT SHOULD EXIST
IMPLEMENTATION_STATUS  WHAT REALLY EXISTS
CURRENT_STAGE          WHAT WE ARE DOING NOW
DECISIONS              WHAT WE ALREADY DECIDED
EXPERIMENTS            WHAT WE ACTUALLY OBSERVED
RESEARCH               WHAT WE ARE STILL EXPLORING
SCAFFOLD               WHERE EVERYTHING IS
PROJECT_GUIDE          WHAT THE FILES/CODE MEAN IN PLAIN ENGLISH
SIGNAL_FLOW            HOW INFORMATION MOVES
ARCHITECTURE_STEWARD   HOW THE AI SHOULD THINK ABOUT CHANGES
CANONICAL SKILL        HOW THE AI SHOULD EXECUTE CHANGES
src/synrheon/          THE ACTUAL ORGANISM
runtime.py             SEQUENCES THE ORGANISM
ui/                    LETS YOU SEE/CONTROL IT
tests/                 PROTECT DISCOVERED CONTRACTS
scripts/               MAKES DAILY DEVELOPMENT EASIER
```

---

# Maintenance Rule

Whenever meaningful code is added, changed, split, or removed, update the relevant section here.

For implemented code, explain at minimum:

```text
what the file does
what each important class/function does
what information goes in
what information comes out
what state it owns
what calls it
what it calls
what is live
what is still planned
```

The goal is that this document remains understandable six months from now without first becoming a programmer.
