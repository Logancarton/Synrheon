# Cognitive Experiments

## Evidence Standard

Use the evidence mode that matches the question being tested.

A controlled scientific assay may prove that a cognitive mechanism learns or transfers in isolation. It does **not** grant `Integrated` or `Verified` status.

A live-organism experiment is required when claiming that the real Synrheon runtime reaches and uses a mechanism. `Verified` additionally requires human observation of the intended live behavior and relevant state/trace.

Do not move pass criteria after seeing final results.

---

## E000 — Stage 0B Connected Organism Transport

Hypothesis: browser-facing actions can cross into the real Python runtime, mutate Synrheon-owned state, and return observable state/trace without placing cognition in the UI/transport layer.

Observed result: Start, Chat, Internal Thought, Step, Continue, Pause, Current State, and Trace were demonstrated through the real frontend/backend/runtime path.

Status: **Verified**

## E001 — World / Injected-Self / Learned-Self / Activation Separation

The initial Stage 1 substrate established separate world knowledge, organism-relative knowledge, learned organism-relative state, and activation representation.

Its first fixed self-vector representation was later superseded by E001A.

Status: **Superseded representation; provenance separation retained.**

## E001A — Open-Ended Organism Relation Space

Hypothesis: Synrheon can preserve injected-versus-self-learned provenance without hard-coding a closed list of organism-relative dimensions.

Observed automated behavior:
- arbitrary relation names remain data;
- injected and learned versions remain separate;
- learned evidence lineage remains explicit;
- world knowledge and current activation remain separate.

Status: **Built / integrated representation; bounded human live verification still separate.**

## E002 — Ordered Experience Thread

Hypothesis: meaningful external and explicitly injected internal events can receive episode coordinates and explicit before/after links without pretending current-episode experience is durable memory.

Observed automated behavior:
- Chat event is `origin = observed`;
- Internal Thought injection is `origin = injected`;
- sequence is monotonic;
- previous/next links agree;
- stimulus records link to experience event IDs;
- new session starts a new episode.

Status: **Integrated; not durable memory.**

## E003 — Temporal Retrieval

Can Synrheon restrict retrieval to a time region such as earlier today without searching all lifetime memories?

Status: **Future**

## E004 — Hand-Written Sparse Chat Activation

Historical experiment: lexical concept matching, relation spreading, salience, inhibition, fixed recurrence, and Top-K selection were wired through the live organism.

Interpretation: the integration path worked, but the cognition mechanics were developer-selected rather than learned.

Production status: **Removed / superseded by the trainable-cognition pivot.**

## E005 — Three-Level Retrieval

Can Level 1 orientation narrow Level 2 candidates before Level 3 detailed retrieval?

Status: **Future**

## E006 — Problem / Trial Learning

After a failed trial, can Synrheon preserve why it failed and preferentially change the most likely causal variable?

Status: **Future**

## E007 — Route Learning

Can successful retrieval or reasoning trajectories become easier to select later without hard-coded stimulus rules?

Status: **Future; likely absorbed into trainable cognitive-policy work.**

## E008 — Recursive Thought

Can Synrheon solve a problem requiring several internal state transitions before producing an external response?

Status: **Future**

## E009 — Consolidation

Can repeated experiences produce a useful compressed representation while preserving evidence lineage?

Status: **Future**

## E010 — Autonomous Continuation

Can unresolved internal state produce useful S(t+1) without new external input while avoiding fixation?

Status: **Future**

---

# E011 — Train the Cognitive Process, Test Transfer

## Research Question

Can a small model learn a reusable cognitive process over explicit state and transfer that process to generated knowledge it never trained on?

The governing principle is:

> **We code the cognitive physics. Synrheon learns the cognitive skill.**

E011 is split into two gates:

```text
E011-A — Controlled Process-Transfer Assay
prove a trainable policy learns reusable bounded search behavior

E011-B — Live Organism Integration
wire a proven artifact through cognition.py → thin runtime → state/trace/UI
```

Passing E011-A does not mean the mechanism is Integrated.

---

# E011-A — Controlled Process-Transfer Assay

## Frozen Experiment Version

```text
experiment_id: E011-A
experiment_version: e011a-v1
generator_version: e011a-v1
action_contract_version: e011a-actions-v1
state_contract_version: e011a-state-v1
hard_action_budget: 10
model_initialization_seeds: 11, 22, 33, 44, 55
```

Any material change to the generator, policy-visible features, action semantics, reward/training configuration, final seed split, or pass thresholds after inspecting final results creates a new experiment revision with a fresh untouched final split.

## Exact First Problem Family — Bounded Partial Graph Discovery

Each generated episode contains:

```text
10–14 opaque concept nodes
1 visible start node
1 hidden goal-marked node
1 unique shortest start→goal path of 3–5 edges
2–4 distractor branches
0–2 generated cross/back edges where valid
opaque per-world node identities
10-action hard budget
```

The start is revealed initially. Other nodes/edges remain hidden until expansion.

The goal marker is visible only after the goal node itself is legitimately revealed.

Success requires revealing the goal and selecting `STOP` within the fixed budget.

## Policy-Visible CognitiveState — Information Firewall

The policy may see only:

```text
checkpoint / action index
remaining hard action budget
revealed nodes only
revealed edges only
for each revealed node:
    opaque handle used only to execute a target
    known depth from start through revealed structure
    expanded / unexpanded
    reveal order / frontier status
    is_goal only after reveal
available valid operation + target candidates
previous selected operation + target summary
```

The trainable feature vector may not contain stable opaque-node identity embeddings.

The policy must never see:

```text
unrevealed nodes
unrevealed edges
hidden goal location before reveal
shortest path
shortest-path distance to goal
on-solution-path flags
correct next action
correct next target
future frontier structure
exhaustive solver output
scorer ranking
world seed as a predictive feature
```

The experiment harness may retain complete hidden truth for scoring and training evidence. Hidden truth remains structurally outside production cognition inputs.

## Frozen First Action Contract

### `EXPAND(target)`

Valid target: one currently revealed, unexpanded frontier node.

Deterministic effect:
- mark target expanded;
- reveal its outgoing local structure;
- update revealed graph/frontier;
- expose `is_goal` only if the goal itself became revealed;
- consume one cognitive action.

Python may enumerate valid targets. Python may not choose which target is preferable.

### `STOP`

Deterministic effect:
- terminate the episode;
- consume one cognitive action;
- succeed only if the goal marker is already revealed;
- otherwise record premature-stop failure.

No other cognitive operation is part of E011-A v1.

## Frozen Seed Splits

```text
TRAIN
1000–4999
4000 generated worlds/tasks

DEVELOPMENT VALIDATION
5000–5999
1000 worlds; may guide development but is not final evidence

FINAL LEVEL-1 HELD-OUT
10000–10999
1000 untouched worlds; not a tuning surface

PAIRED RENAMING / IDENTITY PERMUTATION
worlds 10000–10999
permutation seeds 20000–20999

FUTURE LEVEL-2 STRUCTURAL GATE
30000–30999
separately versioned topology distribution

MODEL INITIALIZATION/TRAINING SEEDS
11, 22, 33, 44, 55
```

All five model seeds must be reported.

## Baselines

E011-A compares:

```text
random-valid policy
matched untrained model
trained model
exhaustive all-reachable cost reference
```

A deterministic breadth-first diagnostic may be used outside production cognition for interpretation only.

## First Trainable Model

Production owner:

```text
src/synrheon/cognition.py
```

First architecture:

```text
e011a-linear-softmax-v1
```

The model scores valid `EXPAND(target)` / `STOP` candidates from revealed-state features only.

The initial feature family includes generic visible-state information such as target depth, target recency, frontier fraction, remaining budget, checkpoint progress, previous operation, and whether STOP is being considered after a revealed goal.

Opaque target handle strings are not trainable features.

## First Learning Mechanism

Production learning owner:

```text
src/synrheon/learning.py
```

The first learner is a small REINFORCE-style policy update using discounted outcome/cost returns and a running baseline.

The learner receives outcome evidence such as success, premature stop, newly revealed structure, goal reveal, dead end, action cost, and budget exhaustion.

It does not receive hidden route/goal-location/solver features.

The exact E011-A v1 training configuration is recorded in `data/e011a_v1_evidence.json` and is experiment configuration rather than permanent architecture truth.

## Training Record Direction

The broader checkpoint contract remains:

```text
state_before
available_actions_and_targets
selected_action
state_after
predicted_state_after        # future field until predictor exists
expected_value               # future field until value model exists
observed_outcome
compute_cost
error_or_correction
credit_assignment
alternative_action_estimates # future explicit counterfactual estimator
```

Selected does not mean useful. Credit derives from later outcome/cost evidence.

## Required Cost Measurements

Record:

```text
total cognitive actions
EXPAND count
STOP count
premature STOP count
invalid action count
invalid target count
stale target attempts
budget exhaustion
mean / median actions
fraction of hard budget consumed
exhaustive-reference action cost
successful cost / exhaustive cost
```

## Model Artifact / Development Lineage

Each meaningful policy artifact should preserve:

```text
model_id
parent_model_id
experiment/generator/state/action versions
model architecture id
model initialization seed
training seed range
training configuration hash
episodes_seen
parameter checksum
source Git commit
evaluation summary
strongest demonstrated generalization level
```

The recorded five-seed artifact is:

```text
data/e011a_v1_evidence.json
```

## Cognitive-Growth History Contract

Backend-owned evaluation evidence should preserve:

```text
training success
held-out success
renamed success
cognitive cost / efficiency
budget exhaustion
baselines
generalization level
model/version lineage
```

The UI may display this evidence. It must not calculate or invent the scientific result.

## Pre-Registered Failure Taxonomy

### Failed learning
Training performance does not improve meaningfully over matched untrained behavior.

### Memorization / overfit
Training succeeds while untouched held-out remains near random.

### Identity shortcut
Paired renaming causes material collapse.

### Structural overfit
Level 1 passes but later Level 2 changed-topology evaluation collapses.

### Inefficient cognition
Success depends on near-exhaustive exploration or near-total budget use.

### Insufficient / misleading representation
The permitted state omits necessary information or exposes a route shortcut.

### Answer leakage
Hidden graph, goal-location, shortest-path, correct-action, or solver-derived information reaches policy input/selection.

Any answer-leakage result is invalid regardless of score.

## Frozen Quantitative E011-A v1 Gate

All must hold:

1. parameters measurably change;
2. at least 4/5 seeds improve training success by at least 20 percentage points over their own untrained checkpoints;
3. median final Level-1 held-out success is at least 70%;
4. median held-out success is at least 20 points above both random-valid and matched-untrained baselines;
5. at least 4/5 seeds individually beat both final baselines by at least 15 points;
6. paired renaming retains at least 95% of unrenamed held-out success and median absolute drop is at most 5 points;
7. held-out success includes path depths 3, 4, and 5;
8. successful held-out mean action cost is at most 80% of exhaustive cost on the same worlds;
9. mean held-out hard-budget consumption is at most 80%;
10. no hidden-answer/hidden-route field reaches policy input;
11. no world/node/seed/correct-target production branch exists;
12. Python enumerates valid actions but does not choose the preferred target;
13. unrelated world/organism state is not mutated by policy inference;
14. all five frozen seed results are reported.

These thresholds are experiment settings, not permanent cognition constants.

## Stop-Tuning Rules

Revisit architecture instead of tuning locally when:
- materially different small models fit training but fail untouched transfer;
- renaming repeatedly collapses despite identity-agnostic design;
- success rises only by driving budget use above 85%;
- random/trained behavior is nearly indistinguishable because the task is badly scaled;
- success requires distance-to-goal, on-path status, correct-action truth, or another solver-derived feature;
- the proposed fix is a world-specific branch or hand-written target selector.

Final held-out data is not a development surface.

## Observed E011-A v1 Result

Recorded evidence:

```text
data/e011a_v1_evidence.json
```

Five frozen model seeds were trained for 8000 generated training episodes each under the recorded E011-A v1 configuration.

Observed controlled result:

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

All five trained model seeds reached 79.8% final held-out success in the recorded run.

Held-out success by shortest-path depth was approximately:

```text
depth 3    87.07%
depth 4    77.40%
depth 5    74.47%
```

The recorded numeric gate passed every frozen quantitative check.

Code-boundary inspection also confirms that:
- opaque handle identity is excluded from the feature vector;
- hidden goal location, shortest path, correct target, and world seed are absent from `CognitiveState` features;
- valid candidates are enumerated without a hand-written preferred-target selector;
- hidden generator/scorer truth remains in `experiments/e011a.py`, outside `src/synrheon/cognition.py`.

Interpretation:

```text
Level 1 — identity / instance transfer demonstrated in the controlled E011-A v1 family
```

Do **not** interpret this as Level 2 structural transfer, Level 3 compositional transfer, natural-language reasoning, or live runtime integration.

## E011-A Status

**Built — controlled E011-A v1 numeric gate passed; strongest supported claim: Level 1 identity / instance transfer.**

The policy is not yet Integrated into the live Synrheon organism.

---

# E011-B — Live Organism Integration Gate

E011-B is now the active next gate.

Required path:

```text
identified E011-A policy artifact
        ↓
legitimate live CognitiveState
        ↓
cognition.py
learned operation + target
        ↓
bounded transition / checkpoint
        ↓
thin runtime sequencing
        ↓
OrganismState / trace
        ↓
Organism UI
```

The hidden generated experiment scorer must remain outside the production cognition path.

E011-B must prove:

1. an exact recorded model artifact loads through the cognition owner;
2. runtime sequences but does not select the cognitive operation/target;
3. one learned action creates one explicit bounded checkpoint;
4. checkpoint and selected action reach live state/trace;
5. the Organism UI shows the specific integrated stage and backend-owned growth evidence;
6. malformed/mismatched state fails safely;
7. unrelated persistent state is not silently mutated;
8. focused and integration tests prove the real call path;
9. no hidden experiment scorer/solution metadata enters production cognition.

Only after this live gate may the policy be called **Integrated**.

Human testing through the running organism is still required before calling the live behavior **Verified**.
