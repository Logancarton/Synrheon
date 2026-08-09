# Current Stage

## Active Stage

**Stage 1 — Trainable Cognition Pivot**

Stage 0B — Observable Organism Harness remains **Verified** and continues to be the live laboratory.

The immediate coding target is now narrower and fully preregistered:

```text
E011-A v1 — Controlled Process-Transfer Assay
```

No trainable cognitive policy is implemented yet.

## Why the Pivot Happened

The first sparse-activation experiment proved that Chat could reach a real state-changing owner, but the mechanism still depended on developer-selected cognition rules:

```text
lexical concept matching
fixed spreading gain
fixed decay
fixed organism salience gain
fixed inhibition threshold
fixed Top-K
fixed recurrent rounds
```

Those rules were useful scaffolding, but keeping them would turn Synrheon into a hand-designed graph reasoner rather than a system that learns **how to think**.

The production implementation therefore removed that policy instead of extending it.

## Current Live Boundary

The live organism currently preserves:

```text
Chat / Internal Thought
        ↓
interfaces.py
        ↓
runtime.py
        ↓
computational time
        ↓
ordered ExperienceEvent
        ↓
StimulusRecord + provenance + trace
        ↓
state / Organism UI
```

Knowledge scaffolding also remains live:

```text
concepts
world relations
open-ended organism relations
activation representation
```

But **no hand-written thinking policy currently turns a stimulus into activation winners.**

The Organism UI now exposes backend-owned evidence from these integrated foundations and has a reserved growth surface for future backend learning metrics. It does not invent a smartness score while learning is absent.

## New Development Rule: Cognitive Physics vs Cognitive Skill

Synrheon still needs designed software boundaries. The pivot does **not** mean that every line of code should be learned.

### Designed / fixed infrastructure may define

```text
what a CognitiveState can contain
how provenance is represented
what a cognitive-action interface looks like
how one checkpoint is recorded
maximum compute / step budgets
how valid action candidates are enumerated
how training examples are serialized
how outcomes and corrections enter learning
safe validation and failure behavior
```

### Learned behavior should increasingly determine

```text
which concepts / regions deserve attention
which path is worth exploring
which cognitive action should happen next
what target / scope that action uses
when retrieval is useful
what evidence should be compared
what prediction is reasonable
when to revise
which earlier transition deserves credit / blame
when a thought process is complete
```

The architecture provides the **physics of cognition**. Training should learn the **skill of cognition**.

## What `cognition.py` Owns Now

`cognition.py` remains the correct owner for future next-state cognitive transformation, but it intentionally contains no hand-written routing algorithm.

The target architecture is:

```text
S0 — current cognitive state
 ↓
choose one cognitive action + target
 ↓
perform a bounded transition
 ↓
S1 — checkpoint
 ↓
continue / redirect / stop
```

A checkpoint is computational state, not a literal wall-clock pause.

## Frozen E011-A v1 Problem

The first trainable experiment is now fixed before implementation.

### Generated world

```text
10–14 opaque concept nodes
1 visible start node
1 hidden goal-marked node
unique shortest start→goal path of 3–5 edges
2–4 distractor branches
0–2 cross/back edges
10-action hard budget
```

All concept identities are opaque and world-local. No natural-language semantics are required.

The policy begins with only the revealed start and progressively reveals structure through cognitive actions.

## Frozen First Action Vocabulary

E011-A v1 uses exactly:

```text
EXPAND(target)
STOP
```

`EXPAND(target)` selects one currently revealed, unexpanded frontier target and reveals its outgoing local structure. It costs one cognitive action.

`STOP` ends the episode and costs one cognitive action. It succeeds only after the goal marker has legitimately become visible.

The broader operation families — FOCUS, RETRIEVE, COMPARE, CHECK_EVIDENCE, PREDICT, REVISE, and others — remain future additions. They are intentionally excluded from the first causal test.

## Policy Information Firewall

The policy may see only revealed state:

```text
checkpoint/action index
remaining budget
revealed nodes and edges
known depth from start
frontier / expanded status
reveal order
is_goal only after reveal
available valid actions + targets
previous action summary
```

The policy must never see:

```text
unrevealed graph structure
hidden goal location
shortest path
shortest-path distance
on-solution-path flags
correct next action or target
future frontier
scorer/solver output
world seed as a predictive feature
```

The experiment harness may know hidden truth for scoring. `cognition.py` may not.

## Frozen Training / Evaluation Splits

```text
TRAIN
1000–4999

DEVELOPMENT VALIDATION
5000–5999

FINAL LEVEL-1 HELD-OUT
10000–10999

PAIRED RENAMING SEEDS
20000–20999
paired 1:1 with final held-out worlds

FUTURE LEVEL-2 STRUCTURAL WORLDS
30000–30999

MODEL SEEDS
11, 22, 33, 44, 55
```

Final held-out worlds cannot become a tuning surface. Any material change after inspecting final results creates a new experiment revision and fresh untouched final split.

## Baselines

E011-A must compare:

```text
random-valid policy
matched untrained model
trained model
exhaustive all-reachable cost reference
```

A deterministic breadth-first diagnostic may be used for interpretation outside production cognition, but it must not become a hand-written production policy.

## Training Record Contract

One useful cognitive checkpoint should preserve:

```text
state_before
available_actions_and_targets
selected_action
state_after
predicted_state_after
expected_value
observed_outcome
compute_cost
error_or_correction
credit_assignment
alternative_action_estimates
```

Some future-facing fields may initially be null, but the record shape must preserve the distinction between what was selected and what later proved useful.

## Frozen E011-A v1 Pass Gate

The full gate lives in `docs/EXPERIMENTS.md`. The key thresholds are:

```text
real parameter change
4/5 model seeds improve training success by ≥20 percentage points
median final held-out success ≥70%
median held-out gain ≥20 points over random and untrained
4/5 seeds beat both baselines by ≥15 points
paired renaming retains ≥95% of held-out success
median renaming drop ≤5 percentage points
successful mean cost ≤80% of exhaustive reference
mean hard-budget use ≤80%
no hidden-answer leakage
no hand-written preferred-target selection
all five model seeds reported
```

These are **experiment configuration**, not permanent cognition constants.

## Failure Categories Are Predefined

A failed result should be classified before changing code:

```text
failed learning
memorization / training overfit
identity shortcut
structural overfit
inefficient brute-force cognition
insufficient or misleading representation
answer leakage
```

The purpose is to repair the correct owner or representation rather than patch the benchmark.

## Stop-Tuning Rule

Revisit architecture instead of continuing local tuning when:

- multiple small models fit training but fail untouched transfer;
- renaming repeatedly collapses despite an identity-agnostic contract;
- success rises only by consuming nearly all cognitive budget;
- random and trained behavior are nearly indistinguishable because the task is underdetermined or badly scaled;
- success requires a feature derived from shortest path, hidden goal location, or correct-next-action truth;
- the proposed fix is a world-specific branch or hand-written target selector.

## Model Lineage and Growth History

Every meaningful trained checkpoint should preserve:

```text
model ID + parent model ID
experiment/generator/state/action versions
model seed + training split
configuration hash
episodes seen
parameter checksum
source Git commit
evaluation summary
strongest demonstrated generalization level
```

Evaluation history should preserve training, held-out, renaming, cost, budget use, and baseline evidence over time so the Organism UI can later show actual cognitive development rather than a one-time score.

## E011-A vs E011-B

E011-A is the controlled scientific test.

E011-B is the live integration gate:

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

A successful E011-A artifact is **not Integrated** until this live path exists and is tested.

The hidden E011 generator/scorer must never be part of production cognition.

## Policy / Transition / Value Boundary

The design still keeps three questions distinct:

```text
P(a | S)       What should I do?
F(S,a) → S'    What do I expect it to change?
V(S,a)         Is it worth doing from here?
```

E011-A may initially train only the action/target policy while preserving trace fields for later transition/value learning. That is a deliberately narrow experiment, not a rejection of the broader architecture.

## Generalization Ladder

Results must be classified by the strongest demonstrated level:

```text
Level 0 — Training memorization
Level 1 — Identity / instance transfer
Level 2 — Structural transfer
Level 3 — Compositional transfer
```

Do not describe Level-1 success as unrestricted “learned how to think.”

## What Is Still Missing

- E011-A generated world/task implementation;
- trainable `CognitiveState` feature representation;
- parameterized action-target representation;
- state → action/target policy;
- bounded transition/checkpoint loop;
- training objective / credit mechanism;
- artifact persistence and growth-history writer;
- transfer-training/evaluation harness;
- E011-B runtime invocation;
- later transition / next-state prediction;
- later expected cognitive value estimate;
- later counterfactual/alternative-action estimator;
- learned concept organization / routing;
- semantic language grounding;
- durable memory;
- Level 1 → Level 2 → Level 3 retrieval;
- response generation;
- recursive scratchpad cognition;
- autonomous continuation.

## Guardrail

Do not rebuild the removed heuristic under new names.

The design rule going forward is:

```text
hard-code representations, interfaces, budgets, provenance, candidate validity, and learning boundaries

learn concept organization, cognitive routing, action/target selection, transition usefulness,
expected cognitive value, and eventually the process that turns one cognitive state into the next
```
