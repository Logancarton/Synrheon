---
name: synrheon-development-workflow
description: Use proactively for Synrheon architecture, cognitive implementation, repair, experimentation, live-behavior testing, stage work, learning, memory, retrieval, abstraction, autonomy, UI/runtime integration, or documentation synchronization. Work broad-to-narrow, preserve preregistered experiment boundaries, prove controlled cognition scientifically before live integration when required, and prove Integrated/Verified status through the running organism.
---

# Synrheon Development Workflow

This is the canonical repo-local execution workflow for Synrheon.

It owns the procedure for architecture review, controlled experimentation, implementation, live-organism integration, test support, documentation synchronization, Git hygiene, commit, and push.

## Canonical Repository

```text
Repository: https://github.com/Logancarton/Synrheon
Full name:  Logancarton/Synrheon
Branch:     main
Clone:      https://github.com/Logancarton/Synrheon.git
```

Do not ask the user which repository to use.

Before pushing from a local checkout:
- verify `origin` points to the canonical repository;
- if no origin exists and the tree is clearly Synrheon, add the canonical origin;
- if origin points elsewhere, stop before push and report the mismatch.

## Current Priority

Stage 0B — the observable runtime/UI organism — already exists and is **Verified**.

The active implementation priority is:

```text
E011-A v1 controlled process-transfer assay
        ↓
implement the frozen scientific contract
        ↓
train / validate / untouched transfer / renaming / cost evaluation
        ↓
classify outcome honestly
        ↓
E011-B live cognition integration only after a suitable artifact exists
        ↓
cognition.py → thin runtime → OrganismState/trace → Organism UI
```

Do not restart runtime/UI foundation work merely because older instructions said it was the first priority.

## Core Doctrine

Synrheon is not built by accumulating stimulus-specific fixes.

Use this path:

```text
current project truth
        ↓
broad cognitive objective
        ↓
underlying bottleneck
        ↓
correct owner / experiment boundary
        ↓
pre-register exact evidence standard
        ↓
implement the smallest mechanism that tests the hypothesis
        ↓
measure outcome / failure class
        ↓
if promising, integrate through real runtime
        ↓
UI / trace observation
        ↓
documentation truth
```

The goal is not the smallest diff. The goal is the smallest coherent change that answers the current cognitive question without duplicate authority or hidden shortcuts.

## Controlled Experiment vs Live Integration

Two evidence modes are valid, but they prove different things.

### Controlled scientific assay

Use when isolating a learning mechanism is necessary to answer a causal question.

A controlled E011-A result may establish that a learned mechanism works experimentally.

It does **not** grant `Integrated` or `Verified` status.

### Live-organism proof

Required when claiming the live Synrheon organism reaches and uses the mechanism.

`Integrated` requires the real runtime path.

`Verified` requires observed behavior through the running organism with relevant state/trace inspected.

Automated tests support both modes but do not independently grant `Verified`.

## Project Truth Owners

Read before material work:

```text
README.md
        ↓
docs/SCAFFOLD.md
        ↓
docs/ARCHITECTURE_PLAN.md
        ↓
docs/IMPLEMENTATION_STATUS.md
        ↓
docs/CURRENT_STAGE.md
        ↓
docs/EXPERIMENTS.md
        ↓
docs/SIGNAL_FLOW.md
        ↓
affected production owners / tests
```

Also use:
- `docs/PROJECT_GUIDE.md` for human-readable project truth;
- `docs/DECISIONS.md` when durable architecture choices constrain work;
- `docs/RESEARCH.md` only for research evidence, not implementation truth.

## Status Rules

Use:

```text
Not Started
Designed
Built
Integrated
Verified
```

Definitions:
- `Not Started`: no meaningful implementation;
- `Designed`: intended mechanism or experiment contract defined;
- `Built`: implementation exists and works in isolation;
- `Integrated`: real Synrheon runtime reaches and uses it;
- `Verified`: intended live behavior demonstrated through the running organism with relevant state/trace inspected.

Also classify cognitive effect:

```text
Infrastructure
Supporting cognition
Cognitive improvement
```

Do not call controlled experimental evidence `Integrated`.

# Standard Workflow

## 0. Confirm project and preserve current work

Before editing:
- confirm the worktree is Synrheon;
- record branch and HEAD;
- inspect `git status --short`;
- inspect recent history;
- preserve unrelated dirty work;
- never use destructive cleanup to make the tree appear clean.

Never use:

```powershell
git add .
git clean
git reset --hard
```

Prefer:

```powershell
git status --short -- Synrheon
git diff --check -- Synrheon
git diff -- Synrheon
```

Stage changed files explicitly.

## 1. Read current project truth

Read the project truth owners listed above.

If documentation disagrees with reality, reconcile truth before adding cognition.

## 2. Run the architecture gate

Before choosing code, answer:

1. What capability are we trying to create?
2. Why is it the correct bottom-up capability now?
3. What broad bottleneck prevents it?
4. Which owner or coordinated owners should hold it?
5. What later systems depend on this choice?
6. What failure modes or shortcuts could fake success?
7. What observation would prove or falsify it?

Do not code if the owner, information boundary, or falsification condition is unclear.

## 3. Respect the active preregistered experiment

For E011-A v1, `docs/EXPERIMENTS.md` is binding experiment truth.

The first task is:

```text
bounded partial graph discovery
10–14 opaque nodes
1 visible start
1 hidden goal marker
unique shortest route 3–5 edges
2–4 distractor branches
0–2 cross/back edges
10-action hard budget
```

The first action vocabulary is exactly:

```text
EXPAND(target)
STOP
```

Do not add broader cognitive actions merely because the architecture may use them later.

The environment may enumerate valid action-target candidates. It must not choose the preferred target.

### E011-A policy firewall

Policy-visible state may contain only revealed information and valid candidate structure.

Never expose:

```text
unrevealed graph
hidden goal location
shortest path
shortest-path distance
on-solution-path flags
correct next action / target
future frontier
solver/scorer output
world seed as predictive input
```

If hidden truth reaches cognition, invalidate the result and repair the boundary.

### Frozen seed splits

```text
train                    1000–4999
development validation   5000–5999
final Level-1 held-out   10000–10999
paired renaming          20000–20999
future Level-2           30000–30999
model seeds              11, 22, 33, 44, 55
```

Final held-out data is not a tuning surface.

Once final results are inspected, any material model/state/action/reward/generator change creates a new experiment revision and requires a fresh untouched final split.

Do not move quantitative pass thresholds after seeing results.

## 4. Inspect the full affected signal path

For E011-A inspect:

```text
generator hidden world
        ↓
revealed-state adapter
        ↓
CognitiveState
        ↓
cognition owner / policy
        ↓
operation + target
        ↓
bounded transition
        ↓
checkpoint / outcome / cost
        ↓
learning owner
        ↓
model artifact / evaluation history
```

The hidden scorer belongs outside production cognition.

For E011-B later inspect:

```text
live state
        ↓
cognition.py
        ↓
learned action + target
        ↓
checkpoint
        ↓
runtime sequencing
        ↓
OrganismState / trace
        ↓
UI
```

Runtime stays thin.

## 5. Implement in the correct owner

Prefer existing owners whenever they can cleanly hold the behavior.

Likely E011 responsibilities:

```text
cognition.py
    CognitiveState / action representation / policy inference / bounded cognition-owned transition interface

learning.py
    outcome/error/credit/parameter-update ownership

experiment support outside production cognition
    deterministic generated worlds
    hidden scorer
    seed splits
    evaluation harness
```

Do not put hidden generated truth into production cognition.

Create a new production file only when no existing owner can hold the responsibility cleanly.

Do not add:
- phrase-specific cognition;
- known-world branches;
- solver-derived policy features;
- hand-written preferred-target routing;
- fake success flags;
- UI-side cognition;
- parallel planners/learning paths/memory stores.

## 6. Add the minimum high-value tests

For E011-A prioritize tests proving:
- deterministic generator behavior;
- train/validation/final seed disjointness;
- hidden truth is absent from policy-visible state;
- action semantics and 10-step budget are exact;
- malformed/mismatched action output fails safely;
- unrelated state is not mutated;
- model parameters actually change during training;
- evaluation reports all frozen seeds and baselines;
- renaming/permutation leaves no identity shortcut;
- no production world-specific branch is required.

Avoid large batteries of trivial construction/getter tests.

## 7. Run the controlled E011-A evidence gate

Report all frozen model seeds.

At minimum compare:

```text
random-valid policy
matched untrained model
trained model
exhaustive all-reachable cost reference
```

Use development validation for iteration.

Use final held-out worlds only after final configuration is frozen.

Apply the preregistered quantitative thresholds exactly as documented.

## 8. Classify failure before changing code

Use the predefined taxonomy:

```text
failed learning
memorization / overfit
identity shortcut
structural overfit
inefficient cognition
insufficient / misleading representation
answer leakage
```

Do not patch a single failed world.

Stop local tuning and revisit architecture when multiple models fit training but fail untouched transfer, renaming repeatedly collapses, gains require nearly all compute, the task cannot distinguish trained from random behavior, or success requires hidden solver-derived features.

A failed experiment is useful evidence and remains documented.

## 9. Preserve model lineage and growth history

Meaningful checkpoints should preserve:

```text
model_id
parent_model_id
experiment / generator / state / action versions
model architecture id
model seed
training split
configuration hash
episodes_seen
checkpoint index
parameter checksum
source Git commit
evaluation summary
strongest demonstrated generalization level
```

Preserve immutable evaluation records for training, held-out, renaming, cost, budget, and baselines.

Backend-owned summary metrics may later feed the Organism UI. The UI must not manufacture the result.

## 10. E011-B live integration gate

Only after a suitable E011-A artifact exists, integrate through the real organism.

Required path:

```text
legitimate live CognitiveState
        ↓
cognition.py
        ↓
learned operation + target
        ↓
bounded checkpoint
        ↓
runtime sequences only
        ↓
OrganismState / trace
        ↓
Organism UI
```

The generated experiment's hidden graph/scorer/solution must not enter the live production path.

A cognitive mechanism is not `Integrated` until runtime reaches it.

## 11. Run live organism proof before declaring Verified

For E011-B:
- start Synrheon through the supported entry point;
- exercise the mechanism through the real path;
- inspect visible behavior;
- inspect current state/checkpoints/trace;
- confirm the Organism UI shows the actual integrated stage and backend-owned growth evidence;
- confirm unrelated state is not mutated;
- repeat after any cleanup/integration change that could alter behavior.

Automated tests alone cannot grant `Verified`.

## 12. Run verification gates

After the relevant controlled/live behavior is correct:
- run focused tests;
- run integration tests;
- run the full active suite when broad state/runtime/cognition changed;
- run any relevant engine/R4 gate;
- compile;
- run `git diff --check`;
- review the full Synrheon-scoped diff;
- review Synrheon-scoped status.

## 13. Synchronize project truth

Update only affected documents:

- `docs/ARCHITECTURE_PLAN.md`
- `docs/IMPLEMENTATION_STATUS.md`
- `docs/CURRENT_STAGE.md`
- `docs/DECISIONS.md`
- `docs/EXPERIMENTS.md`
- `docs/RESEARCH.md`
- `docs/SCAFFOLD.md`
- `docs/SIGNAL_FLOW.md`
- `docs/PROJECT_GUIDE.md`

Do not let documentation claim cognition the experiment or live organism has not demonstrated.

## 14. Review the whole change as one organism

Before completion confirm:
- behavior is in the correct owner;
- hidden truth cannot reach the policy;
- runtime remains thin;
- UI remains observational;
- no duplicate subsystem exists;
- tests prove behavior rather than manufacture it;
- experiment thresholds were not moved post-result;
- documentation matches reality;
- cognitive effect/status is honest;
- no unrelated files are included.

## 15. Commit and push

After the relevant gates pass:
- stage every intended file explicitly;
- create a focused reversible commit;
- push the active branch to the canonical repository.

Do not force-push, rewrite history, or include unrelated files.

# Definition of Done

A bounded Synrheon change is complete only when:

- [ ] Current project truth was read first.
- [ ] The architecture gate identified the correct bottleneck and owner.
- [ ] The active experiment contract was respected.
- [ ] Hidden-answer boundaries were audited.
- [ ] Implementation lives in the correct owner.
- [ ] High-value behavioral tests protect the contract.
- [ ] Controlled evidence was run for E011-A when applicable.
- [ ] Failure was classified rather than patched.
- [ ] Runtime integration exists before claiming Integrated.
- [ ] Live organism behavior was observed before claiming Verified.
- [ ] Full relevant tests/compile/gates pass.
- [ ] `git diff --check` passes.
- [ ] Complete Synrheon diff/status were reviewed.
- [ ] Documentation states implemented truth.
- [ ] Cognitive effect is described honestly.
- [ ] Completed work is committed and pushed to `Logancarton/Synrheon`.
