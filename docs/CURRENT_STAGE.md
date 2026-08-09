# Current Stage

## Active Stage

**Stage 1 — Trainable Cognition Pivot**

Stage 0B — Observable Organism Harness remains **Verified**.

The first controlled trainable-cognition slice is now **Built** and has passed the frozen E011-A v1 numeric transfer gate. It is **not yet Integrated** into the live Synrheon runtime.

The immediate target is now:

```text
E011-B — Live Organism Integration
```

## What Was Actually Built

`src/synrheon/cognition.py` now owns the first explicit trainable policy surface:

```text
CognitiveState
+
RevealedNode
+
CognitiveAction
+
LinearCognitivePolicy
```

The first policy chooses among the frozen E011-A v1 actions:

```text
EXPAND(target)
STOP
```

Python enumerates valid candidates. The learned policy scores and chooses the preferred operation/target. Opaque node identity is not part of the trainable feature vector.

`src/synrheon/learning.py` now owns the first outcome-driven policy update:

```text
policy decision evidence
+
outcome rewards/costs
+
discounted return
+
REINFORCE credit update
        ↓
future policy weights change
```

The learner receives outcomes. It does not receive the hidden generated graph, shortest path, hidden goal location, or correct target.

The hidden E011 generator/scorer lives outside production cognition in:

```text
experiments/e011a.py
```

## E011-A v1 Controlled Result

The checked-in evidence artifact is:

```text
data/e011a_v1_evidence.json
```

Frozen five-model-seed result:

```text
training success, median          81.0%
final held-out success, median    79.8%
random-valid baseline              6.1%
matched untrained, median          0.0%
paired renaming success           79.8%
renaming retention               100.0%
mean held-out budget use          78.02%
success cost / exhaustive cost    57.18%
```

All five trained model seeds reached 79.8% held-out success in the recorded run. Held-out success remained present on shortest-path depths 3, 4, and 5.

The frozen numeric gate therefore passed.

This is evidence of **Level 1 — identity / instance transfer** only. It is not evidence of unrestricted general reasoning, Level 2 structural transfer, or Level 3 compositional transfer.

## Information Firewall Remains Binding

The policy may see only revealed state:

```text
checkpoint/action index
remaining budget
revealed nodes and edges
known revealed depth
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
correct next action / target
future frontier
solver / scorer output
world seed as predictive input
```

Any future change that violates this boundary invalidates the experiment result.

## What The Result Means

The first model learned a reusable bounded search preference from outcome/cost evidence rather than using opaque node identity or a hard-coded correct-target selector.

The result is meaningful cognitive evidence because:

```text
untrained behavior ≈ fails
        ↓
training changes parameters
        ↓
training behavior improves
        ↓
unseen generated worlds remain strong
        ↓
renaming does not collapse behavior
```

But the result is still a controlled assay.

It does **not** mean Chat now thinks differently, durable memory exists, or the live runtime uses the trained policy.

## E011-B — Immediate Integration Gate

The next live path must be:

```text
legitimate live CognitiveState
        ↓
cognition.py
identified trained policy artifact
        ↓
learned operation + target
        ↓
bounded cognitive transition
        ↓
checkpoint
        ↓
thin runtime sequencing
        ↓
OrganismState / trace
        ↓
Organism UI
```

The hidden E011 generator/scorer must remain outside production cognition.

Runtime may sequence the owner and return state/feedback. Runtime must not choose the cognitive action or target.

## What E011-B Must Prove

Before the first policy is called **Integrated**:

1. an exact recorded E011-A model artifact loads through the cognition owner;
2. a legitimate live CognitiveState reaches the policy through the real runtime path;
3. runtime does not rank or choose operation/target candidates;
4. one policy choice produces one bounded checkpoint;
5. checkpoint state and selected action reach state/trace;
6. the Organism UI exposes the specific live stage and backend-owned growth evidence;
7. malformed/mismatched state fails safely;
8. unrelated world/organism state is not silently mutated;
9. focused and integration tests prove the actual call path;
10. the hidden experiment scorer never enters the production path.

Human testing through the running organism is still required before calling the live behavior **Verified**.

## Current Live Boundary

The existing browser/runtime organism still preserves:

```text
Chat / Internal Thought
        ↓
interfaces.py
        ↓
runtime.py
        ↓
computational time + ordered experience
        ↓
state / trace / Organism UI
```

Knowledge scaffolding remains live:

```text
concepts
world relations
open-ended organism relations
activation representation
```

Chat still does not invoke the E011-A policy yet. This is intentional until E011-B is implemented cleanly.

## Policy / Transition / Value Boundary

The broader design still distinguishes:

```text
P(a | S)       What cognitive action/target should I choose?
F(S,a) → S'    What state change should I expect?
V(S,a)         How useful should this action be?
```

E011-A v1 implemented only the first learned policy slice. Transition prediction and expected cognitive value remain future work.

## What Is Still Missing

Immediate:

- E011-B live CognitiveState source / adapter;
- exact artifact loading through the cognition owner;
- runtime sequencing of one learned cognitive transition;
- checkpoint representation in live OrganismState/trace;
- UI exposure of the live E011-B transition and recorded growth evidence;
- live integration tests and human verification.

Later:

- learned transition prediction;
- learned expected cognitive value;
- counterfactual/alternative-action estimator;
- Level 2 structural transfer;
- learned concept organization / routing;
- semantic language grounding;
- durable memory;
- Level 1 → Level 2 → Level 3 retrieval;
- recursive scratchpad cognition;
- response generation;
- autonomous continuation.

## Guardrail

Do not tune E011-A v1 against the already-inspected final seeds.

If the model/state/action/reward/generator is materially changed to improve transfer, create a new experiment revision with a fresh untouched final split.

Do not rebuild the removed hand-written lexical/spreading/Top-K cognition under new names.
