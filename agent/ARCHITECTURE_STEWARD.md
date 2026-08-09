# Synrheon Architecture Steward

## Canonical Repository

```text
https://github.com/Logancarton/Synrheon
```

Repository full name: `Logancarton/Synrheon`

Default branch: `main`

Do not ask the user which repository Synrheon belongs in.

When working locally, verify `origin` points to the canonical repository before pushing. If no `origin` exists and the tree is clearly Synrheon, add it. If `origin` points elsewhere, stop before push and report the mismatch rather than silently replacing it.

## Primary Development Principle

Synrheon is developed bottom-up with observable state and explicit ownership.

Stage 0B — the runtime/UI organism — already exists and is **Verified**. Do not treat runtime/UI construction as the current first priority anymore.

The active scientific target is now **E011-A v1**, a fully preregistered controlled process-transfer assay. Its purpose is to test whether a small learned policy can acquire reusable bounded cognitive search behavior without hidden-answer leakage or developer-selected target routing.

A controlled experiment may be built and evaluated before live runtime integration when isolation is necessary to answer the causal research question. Such a result is **experimental evidence only**.

It becomes `Integrated` only through **E011-B**, where the real live path reaches the learned owner:

```text
legitimate live CognitiveState
        ↓
cognition.py
learned operation + target
        ↓
bounded checkpoint
        ↓
thin runtime
        ↓
OrganismState / trace
        ↓
Organism UI
```

The UI is a microscope for cognition. It must not become the owner of cognition or scientific scoring truth.

## Startup Sequence

Before material work, read and reconcile:

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
```

Read `docs/PROJECT_GUIDE.md` for the human-readable project map and keep it synchronized when meaningful responsibility or structure changes.

Then load and follow:

```text
.agents/skills/synrheon-development-workflow/SKILL.md
```

Only after current truth is understood should implementation begin.

## Status Vocabulary

Use:

- **Not Started** — no meaningful implementation exists.
- **Designed** — architecture/experiment contract exists, but functional implementation does not.
- **Built** — mechanism exists and works in isolation.
- **Integrated** — the real Synrheon runtime reaches and uses it.
- **Verified** — intended live behavior has been demonstrated through the running organism with relevant state/trace inspected.

Keep cognitive effect separate:

- **Infrastructure**
- **Supporting cognition**
- **Cognitive improvement**

A successful controlled E011-A model may represent experimental cognitive improvement, but it is not `Integrated` until E011-B.

## Broad-to-Narrow Review

For each proposed change identify:

1. Cognitive objective.
2. Current bottleneck.
3. Affected owners/state/signal path.
4. Candidate mechanisms.
5. System effects.
6. Failure modes.
7. Correct owner or coordinated owners.
8. The observation that would prove or falsify the mechanism.

Prefer changes that improve an underlying mechanism and solve a class of problems.

Do not begin with:
- stimulus-specific patches;
- hardcoded phrase recognition;
- world-specific routes;
- arbitrary score changes;
- scripted answers;
- test-only production behavior;
- UI-side cognitive shortcuts.

## E011-A v1 Frozen Scientific Contract

Before E011-A implementation, treat `docs/EXPERIMENTS.md` as binding experiment truth.

The first problem family is:

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

The environment may enumerate valid action-target candidates. It must not choose which target is cognitively preferable.

Policy-visible state is limited to revealed information. It must never receive:

```text
unrevealed graph structure
hidden goal location
shortest path
shortest-path distance
on-solution-path labels
correct next action / target
future frontier
solver/scorer output
world seed as predictive input
```

Frozen world/model seeds are:

```text
train                    1000–4999
development validation   5000–5999
final Level-1 held-out   10000–10999
paired renaming          20000–20999
future Level-2           30000–30999
model seeds              11, 22, 33, 44, 55
```

Do not tune against the final held-out split. Once final results are inspected, a material model/feature/reward/generator change requires a new experiment revision and fresh untouched final split.

Do not move pass thresholds after seeing the result.

## E011-A Failure Discipline

Classify failure before changing the mechanism:

```text
failed learning
memorization / overfit
identity shortcut
structural overfit
inefficient cognition
insufficient / misleading representation
answer leakage
```

If multiple small models fit training but fail untouched transfer, if renaming repeatedly collapses, if gains require near-total budget use, or if success requires solver-derived features, stop local tuning and revisit the state/action/task architecture.

Never make the benchmark pass by adding:
- distance-to-goal;
- on-solution-path labels;
- correct-action hints;
- a hidden target router;
- special branches for known seeds/worlds.

## Runtime Principle

`src/synrheon/runtime.py` is the thin live integration layer.

Runtime may:
- start/stop/pause/step the organism;
- sequence owners;
- route typed handoffs;
- accept stimuli;
- invoke a learned cognition owner during E011-B;
- expose observable state;
- return outcomes/feedback.

Runtime must not:
- become the primary cognition owner;
- choose preferred E011 targets;
- duplicate learning, memory, retrieval, abstraction, or autonomy;
- contain hidden experiment solver logic.

## UI Principle

The Organism UI should show:
- what stage is actually integrated;
- what state/evidence that stage owns right now;
- later backend-owned learning/generalization history.

It must not manufacture cognition or calculate the scientific result itself.

## Documentation Synchronization

After meaningful work, update only affected truth owners:

- `docs/IMPLEMENTATION_STATUS.md`
- `docs/CURRENT_STAGE.md`
- `docs/ARCHITECTURE_PLAN.md`
- `docs/DECISIONS.md`
- `docs/EXPERIMENTS.md`
- `docs/SCAFFOLD.md`
- `docs/SIGNAL_FLOW.md`
- `docs/PROJECT_GUIDE.md`

Documentation must describe observed and implemented truth, not hoped-for behavior.

## Definition of Architectural Success

Before calling a stage complete, confirm:

```text
correct owner
+
no duplicate cognitive authority
+
no hidden answer leakage
+
real behavior/evidence
+
honest status
+
reproducible experiment or live stimulus
+
thin runtime when integration occurs
+
UI/trace observation when live
```
