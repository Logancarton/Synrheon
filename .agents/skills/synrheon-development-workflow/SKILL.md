---
name: synrheon-development-workflow
description: Use proactively for Synrheon architecture, cognitive implementation, repair, controlled experimentation, live integration, testing, learning, memory, retrieval, abstraction, autonomy, UI/runtime work, or documentation synchronization. Preserve preregistered experiment boundaries, put behavior in the correct owner, keep runtime thin, and distinguish controlled evidence from live integration.
---

# Synrheon Development Workflow

Canonical repository:

```text
Repository: https://github.com/Logancarton/Synrheon
Full name:  Logancarton/Synrheon
Branch:     main
```

This file owns the execution workflow for architecture review, experimentation, implementation, live integration, verification, documentation, Git hygiene, commit, and push.

# Current Priority

Stage 0B — the observable runtime/UI organism — already exists and is **Verified**.

E011-A v1 — the first controlled trainable-cognition assay — is now **Built**. Its frozen five-seed Level-1 numeric gate passed. It is not live-integrated.

The active target is:

```text
E011-B — Live Organism Integration

recorded E011-A artifact
        ↓
legitimate live CognitiveState
        ↓
cognition.py
learned operation + target
        ↓
bounded checkpoint
        ↓
thin runtime sequencing
        ↓
OrganismState / trace
        ↓
Organism UI
```

Do not rebuild or retune E011-A v1 against its already-inspected final seeds.

A material change to its model, visible state, action contract, reward/training configuration, generator, or final thresholds requires a new experiment revision with fresh untouched final worlds.

# Core Doctrine

Use this decision path:

```text
requested behavior
        ↓
inspect current project truth + full affected signal path
        ↓
identify the correct owner or coordinated owners
        ↓
implement the mechanism where it belongs
        ↓
wire owners through the real flow when integration is part of the stage
        ↓
observe behavior / outcome
        ↓
classify evidence honestly
```

Do not begin with a local patch simply because it is easy.

Prefer the cleanest correct organism-level change, even when it requires coordinated edits across existing owners.

# Status Vocabulary

Use status labels exactly:

```text
Not Started
Designed
Built
Integrated
Verified
```

- **Not Started** — no meaningful implementation exists.
- **Designed** — architecture/experiment contract exists; functional mechanism does not.
- **Built** — mechanism exists and works in isolation or controlled assay.
- **Integrated** — the live Synrheon runtime reaches and uses the mechanism.
- **Verified** — intended live behavior has been demonstrated through the running organism and relevant state/trace inspected.

Also classify cognitive effect:

```text
Infrastructure
Supporting cognition
Cognitive improvement
```

A controlled experiment may establish genuine cognitive improvement while still remaining only `Built` rather than `Integrated`.

# Project Truth To Read First

Before material work, inspect:

```text
README.md
docs/SCAFFOLD.md
docs/ARCHITECTURE_PLAN.md
docs/IMPLEMENTATION_STATUS.md
docs/CURRENT_STAGE.md
docs/EXPERIMENTS.md
docs/SIGNAL_FLOW.md
```

Also use:

- `docs/PROJECT_GUIDE.md` for the non-programmer owner's view;
- `docs/DECISIONS.md` for durable architecture choices;
- `docs/RESEARCH.md` only as research evidence, not implementation truth.

Then inspect the receiving production owners, call sites, state transitions, runtime sequence, and relevant tests before changing code.

# E011-A Frozen Truth

The controlled E011-A v1 result is recorded in:

```text
data/e011a_v1_evidence.json
```

The hidden scientific harness is:

```text
experiments/e011a.py
```

The production policy owner is:

```text
src/synrheon/cognition.py
```

The production learning owner is:

```text
src/synrheon/learning.py
```

E011-A uses:

```text
EXPAND(target)
STOP
```

and a 10-action budget over generated opaque partial-graph worlds.

The policy may consume revealed state only.

It must never receive:

```text
unrevealed graph
hidden goal location
shortest path
shortest-path distance
on-solution-path flags
correct next action / target
future frontier
solver / scorer output
world seed as predictive input
```

The generator/scorer may know those fields for scientific scoring, but that hidden truth must remain outside production cognition.

# E011-B Integration Rule

The next stage must integrate the learned mechanism without importing the controlled experiment's hidden world into the organism.

Before coding E011-B, identify what **legitimate live state** can satisfy the E011-A policy contract.

Do not solve this by:

- importing `experiments.e011a` into runtime;
- generating a hidden benchmark world inside production;
- feeding shortest-path/goal/scorer metadata to cognition;
- having runtime choose the target and asking the model only to approve it;
- adding a special UI demo that bypasses the real owner.

Runtime may:

- sequence cognition;
- route typed state/action/checkpoint handoffs;
- invoke one bounded step;
- return outcomes/feedback;
- expose backend-owned state to UI.

Runtime must not:

- rank candidate targets;
- own policy features or weights;
- duplicate learning;
- contain the hidden E011 solver;
- become the primary cognition owner.

# Runtime Principle

`src/synrheon/runtime.py` is an active but thin integration layer.

It may:

```text
start / pause / continue the organism
sequence owners
route typed handoffs
invoke live mechanisms
record externally visible trace events
return state and feedback
```

It must not become a parallel cognition, memory, retrieval, learning, abstraction, or action-selection subsystem.

# UI Principle

The UI is a microscope and behavioral laboratory.

It should show:

1. what stage/mechanism is actually integrated;
2. what that mechanism is doing now;
3. backend-owned evidence of learning/generalization over time.

The UI must not calculate scientific truth or choose cognitive actions.

For E011-A today, controlled learning metrics may be displayed as historical evidence while the stage remains explicitly **not live-integrated**.

For E011-B, the UI should eventually expose the loaded policy identity, current live CognitiveState summary, selected learned operation+target, resulting checkpoint, and growth evidence.

# Controlled Experiment vs Live Proof

Controlled scientific assays and live organism tests answer different questions.

## Controlled assay

Can show that a mechanism learns, transfers, or fails under isolated conditions.

This can support a `Built` cognitive-improvement claim.

## Live organism proof

Required for `Integrated` and `Verified` claims.

The real runtime path must reach the mechanism.

`Verified` additionally requires observing intended behavior through the running organism with relevant state/trace.

Automated tests support both modes but do not independently grant `Verified`.

# Implementation Workflow

## 1. Preserve current work

Before editing:

```powershell
git status --short -- Synrheon
git log -5 --oneline -- Synrheon
```

Never use:

```powershell
git add .
git clean
git reset --hard
```

Preserve unrelated or pre-existing dirty work.

## 2. Trace the full signal path

Inspect:

```text
input / trigger
        ↓
state owner
        ↓
cognition / other correct owner
        ↓
bounded state transition
        ↓
runtime sequencing
        ↓
trace / UI
        ↓
outcome / feedback
        ↓
learning owner when relevant
```

Do not patch a symptom before locating the correct owner.

## 3. Run the architecture gate

Answer:

1. What capability should Synrheon gain?
2. What mechanism currently blocks it?
3. What state must exist before and after?
4. Which owner should decide the behavior?
5. Which owner should only sequence it?
6. What information must remain hidden/unavailable?
7. What failure would falsify the approach?
8. What live evidence will prove integration?

If ownership or information boundaries are unclear, resolve them before coding.

## 4. Implement in the correct owner

Prefer existing owners.

Create a new production file only when no existing owner can cleanly hold the responsibility.

Avoid:

- phrase-specific rules;
- world-specific routes;
- fixed answer branches;
- hidden target selection;
- duplicate planners;
- duplicate memory stores;
- duplicate learning paths;
- UI-side cognition;
- runtime-owned cognition;
- compatibility wrappers that preserve a known-bad boundary.

## 5. Keep experiments outside production cognition

Scientific generators, hidden scorers, and benchmark-only truth belong outside the production cognition path.

A production policy may share reusable state/action/model classes with the assay, but it must not depend on hidden experiment answers.

## 6. Wire live behavior only through real owners

For an integration stage:

```text
correct owner
   ↓
runtime sequencing
   ↓
OrganismState / trace
   ↓
UI
```

Do not call a mechanism Integrated when only a unit test or experiment harness can reach it.

## 7. Add a small number of high-value tests

Tests should prove:

- valid input produces intended behavior;
- malformed/mismatched input fails safely;
- the intended live path reaches the owner when integration is claimed;
- unrelated state is not mutated;
- feedback reaches the correct owner;
- no duplicate authority or hidden shortcut exists.

Avoid excessive constructor/getter tests or repeated variations of the same behavior.

## 8. Test behavior and scientific gates

For E011-A regression work, preserve the frozen result; do not tune against final seeds.

For E011-B, prove:

```text
exact recorded artifact loaded
+
legitimate live state reaches cognition
+
policy selects operation + target
+
one bounded checkpoint occurs
+
runtime remains thin
+
UI/trace exposes the real result
```

Then run focused tests, integration tests, full active suite, compile, and any relevant engine/R4 gate.

## 9. Run repository gates

Use:

```powershell
python -m pytest
python -m compileall src tests experiments
git diff --check -- Synrheon
git status --short -- Synrheon
git diff -- Synrheon
```

Review the complete Synrheon-scoped diff before completion.

## 10. Synchronize project truth

Update only affected truth:

- `docs/ARCHITECTURE_PLAN.md` — intended architecture;
- `docs/IMPLEMENTATION_STATUS.md` — what really exists;
- `docs/CURRENT_STAGE.md` — active next boundary;
- `docs/DECISIONS.md` — durable architecture choices;
- `docs/EXPERIMENTS.md` — preregistration/results/failures;
- `docs/SCAFFOLD.md` — repository map/ownership;
- `docs/SIGNAL_FLOW.md` — current/planned signal path;
- `docs/PROJECT_GUIDE.md` — plain-English owner guide.

Documentation must distinguish controlled evidence from live integration.

## 11. Review the organism as one system

Before declaring completion, confirm:

- behavior is in the correct owner;
- runtime remains thin;
- hidden experiment truth is quarantined;
- UI is observational;
- real integration exists when claimed;
- tests prove behavior rather than structure only;
- no parallel subsystem was introduced;
- no world-specific target selector exists;
- documentation describes actual maturity accurately.

## 12. Commit and push

After relevant gates pass:

- stage every intended file explicitly;
- create a focused reversible commit;
- push the active branch;
- never force push or rewrite history unless explicitly requested.

# Definition of Done

A bounded change is complete only when:

- [ ] current truth was inspected first;
- [ ] full affected signal path was inspected;
- [ ] correct owners were identified;
- [ ] hidden information boundaries were preserved;
- [ ] mechanism is implemented where it belongs;
- [ ] runtime is thin;
- [ ] live path exists if `Integrated` is claimed;
- [ ] UI/trace exposes relevant backend-owned state when appropriate;
- [ ] focused/integration/full tests pass as relevant;
- [ ] compilation passes;
- [ ] `git diff --check` passes;
- [ ] complete Synrheon-scoped diff/status is reviewed;
- [ ] project-truth docs match reality;
- [ ] cognitive effect and status are not overstated;
- [ ] intended files are committed and pushed explicitly.
