# Synrheon Scaffold

This is the structural map and ownership key for the Synrheon repository.

Keep the repository compact. Add files/folders only when real architecture or implementation needs them.

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
│   ├── e011a_v1_evidence.json
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
├── experiments/
│   ├── __init__.py
│   └── e011a.py
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
│   ├── test_e011_trainable_cognition.py
│   └── test_scaffold.py
├── ui/
│   ├── README.md
│   └── index.html
├── .gitignore
├── AGENTS.md
├── pyproject.toml
└── README.md
```

# Fast Orientation

```text
README.md
    ↓
docs/PROJECT_GUIDE.md
    ↓
docs/IMPLEMENTATION_STATUS.md
    ↓
docs/CURRENT_STAGE.md
    ↓
docs/EXPERIMENTS.md
    ↓
docs/SIGNAL_FLOW.md
    ↓
affected owners / experiment / tests
```

# Current Stage Truth

```text
Stage 0B   Observable organism harness      Verified
Stage 1    Cognitive substrate              Built
Stage 2    Time + experience                Integrated
E011-A     Controlled trainable policy      Built; Level-1 numeric gate passed
E011-B     Live policy integration          Not Started / next gate
```

E011-A is controlled scientific evidence. It is not live integration.

# Production Ownership

## `src/synrheon/cognition.py`

Owns trainable current-state → cognitive-action/target policy inference.

Current first implementation:

```text
CognitiveState
RevealedNode
CognitiveAction
LinearCognitivePolicy
```

The first E011-A action vocabulary is `EXPAND(target)` + `STOP`.

Opaque node identity is execution data only; it is not a trainable feature.

## `src/synrheon/learning.py`

Owns outcome-driven cognitive-policy updates.

Current first implementation:

```text
PolicyDecisionTrace
ReinforceLearner
```

It consumes policy decision evidence plus rewards/costs. It must not consume hidden E011 route/goal truth.

## `src/synrheon/core.py`

Owns basic explicit organism substrate:
- concepts;
- world relations;
- open-ended organism relations;
- activation representation;
- top-level live organism state.

Core stores/validates state. It does not choose cognitive routes.

## `src/synrheon/runtime.py`

Thin sequencing/integration layer.

Current Chat/Internal Thought flow still records ordered experience only. Runtime does **not** invoke the E011-A policy yet.

E011-B must add only the sequencing needed to reach cognition without moving target selection into runtime.

## Other owners

`time.py` — computational time / event coordinates.

`experience.py` — ordered current-episode autobiographical experience.

`memory.py` — future durable memory.

`retrieval.py` — future Level 1 → 2 → 3 retrieval.

`scratchpad.py` — future working-state/checkpoint owner.

`problem_solving.py` — future problem/trial/outcome structure.

`consolidation.py` — future replay/pattern/compression.

`abstraction.py` — future higher-order representation formation.

`autonomy.py` — future continuation decision owner.

`interfaces.py` — browser/API transport only.

# Controlled Experiment Ownership

## `experiments/e011a.py`

Non-production scientific harness for E011-A.

Owns:

```text
deterministic generated hidden worlds
partial revealed-state environment
hidden goal / shortest-route truth
random/untrained/trained/exhaustive references
training execution
evaluation
frozen numeric gate calculation
backend-ready learning summary
```

This separation is intentional.

Hidden generator/scorer truth must not migrate into `src/synrheon/cognition.py`, runtime, or UI.

# Data Ownership

## `data/e011a_v1_evidence.json`

Checked-in immutable summary of the recorded E011-A v1 five-seed result.

Contains:
- model lineage;
- parameter checksums;
- learned weights;
- training/untrained/held-out/renaming results;
- cognitive-cost evidence;
- frozen gate result.

## `data/tiny_world.json`

Human-readable debug/UI fixture only.

Never use it as E011 training data or transfer evidence.

# Test Ownership

## `tests/test_e011_trainable_cognition.py`

Protects high-value E011 contracts:
- opaque identity is not a policy feature;
- generated world size/depth contract;
- action-target validation;
- quick five-seed learning/transfer/renaming gate.

## `tests/test_scaffold.py`

Protects existing runtime/UI/substrate/time/experience behavior and proves Chat does not silently regain the removed hand-written cognitive policy.

# UI Ownership

`ui/` remains the development microscope/control surface.

It may display backend-owned learning evidence and live checkpoints as E011-B is integrated.

It must not own action selection, hidden scoring, training truth, or cognition.

# Documentation Ownership

`PROJECT_GUIDE.md` — plain-English owner's manual.

`SIGNAL_FLOW.md` — current and planned information flow.

`ARCHITECTURE_PLAN.md` — architecture and dependency order.

`IMPLEMENTATION_STATUS.md` — what actually exists.

`CURRENT_STAGE.md` — immediate active boundary.

`DECISIONS.md` — durable architecture choices.

`EXPERIMENTS.md` — preregistration + observed scientific evidence.

`RESEARCH.md` — outside ideas only.

# Structural Rule

Prefer:

```text
one clear responsibility
↓
one understandable owner
↓
real complexity appears
↓
split only when justified
```

Avoid parallel cognition, memory, learning, runtime, or experiment authorities.
