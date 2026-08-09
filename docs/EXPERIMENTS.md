# Cognitive Experiments

## Evidence Standard

The preferred final integration evidence is a real stimulus applied through the running Synrheon organism.

For controlled learning experiments, a scientific assay may run before live-organism integration when isolating the mechanism is necessary to answer the research question. Such a result is **experimental evidence**, not `Integrated` or `Verified` live cognition.

Record stimulus/action, baseline, expected behavior, observed output, relevant state/trace, interpretation, experiment version, seed split, and model artifact identity.

Automated tests protect discovered behavior but are not enough to call cognition `Verified`.

## E000 — Stage 0B Connected Organism Transport

Hypothesis: browser-facing actions can cross into the real Python runtime, mutate Synrheon-owned state, and return observable state/trace without placing cognition in the UI/transport layer.

Observed result: the user ran the supported application and confirmed Start, Chat, Internal Thought, Step, Continue, Pause, Current State, and Trace through the real frontend/backend/runtime path.

Status: **Verified**

## E001 — World / Injected-Self / Learned-Self / Activation Separation

The initial Stage 1 substrate established separate world knowledge, organism-relative knowledge, learned organism-relative state, and activation representation.

Its first fixed 11-field self vector was later superseded by E001A.

Status: **Superseded representation; provenance separation retained.**

## E001A — Open-Ended Organism Relation Space

Hypothesis: Synrheon can preserve injected-versus-self-learned provenance without hard-coding a closed list of organism-relative dimensions.

Candidate result:
- arbitrary relation names were accepted as data;
- injected and learned versions remained separate;
- learned evidence lineage remained explicit;
- world knowledge and current activation remained separate;
- Stage 0B controls and ordered experience behavior remained intact.

Status: **Built / integrated representation; human live verification still required for that bounded UI behavior.**

## E002 — Ordered Experience Thread

Hypothesis: every meaningful external or explicitly injected internal event can receive an episode coordinate and explicit before/after links without pretending current-episode experience is durable memory.

Expected result:
- Chat event is `origin = observed`;
- Internal Thought injection is `origin = injected`;
- sequence is monotonic;
- previous/next links agree;
- stimulus records link to experience event IDs;
- new session starts a new episode;
- no durable cross-process memory claim.

Candidate automated result: current tests produced consistent observed/injected provenance, sequence, links, and stimulus-to-experience IDs.

Status: **Integrated; not durable memory.**

## E003 — Temporal Retrieval

Can Synrheon restrict retrieval to a time region such as earlier today without searching all lifetime memories?

Status: Future

## E004 — Hand-Written Sparse Chat Activation

Hypothesis tested: can Chat reach a state-changing cognition owner using generic lexical matching plus relation spreading, salience, inhibition, and Top-K selection without domain-specific phrase branches?

Historical candidate result:
- the live architecture was successfully wired from Chat/Internal Thought through runtime into `cognition.py`;
- unrelated concept networks used the same algorithm;
- fixed Top-K bounded the active region;
- unknown cues failed safely;
- world/organism knowledge was not rewritten.

Important interpretation after review:

The experiment proved the **integration path**, but the actual decision policy still depended on developer-selected cognition mechanics:

```text
lexical matcher
fixed spread gain
fixed decay
fixed salience gain
fixed inhibition threshold
fixed Top-K
fixed recurrence count
```

Those mechanics are no longer considered the intended cognition architecture.

Production implementation status: **Removed / superseded by the trainable-cognition pivot.**

Historical Git evidence remains useful as a failure lesson: a mechanism can be generic across examples and still be too hand-designed to qualify as the long-term learned cognition policy.

## E005 — Three-Level Retrieval

Can Level 1 orientation narrow Level 2 candidates before Level 3 detailed retrieval?

Status: Future

## E006 — Problem / Trial Learning

After a failed trial, can Synrheon preserve why it failed and preferentially change the most likely causal variable?

Status: Future

## E007 — Route Learning

Can successful retrieval or reasoning trajectories become easier to select later without hardcoded stimulus rules?

Status: Future; likely absorbed into the trainable cognitive-policy direction.

## E008 — Recursive Thought

Can Synrheon solve a problem requiring several internal state transitions before producing an external response?

Status: Future

## E009 — Consolidation

Can repeated experiences produce a useful compressed representation while preserving evidence lineage?

Status: Future

## E010 — Autonomous Continuation

Can unresolved internal state produce useful S(t+1) without new external input while avoiding fixation?

Status: Future

# E011 — Train the Cognitive Process, Test Transfer

## Research Question

Can a small model learn a reusable cognitive process over explicit state and transfer that process to generated knowledge it never trained on?

The experiment is intentionally not natural-language question answering. Natural-language fluency would make it too easy to mistake pretrained or memorized knowledge for learned cognition.

The governing principle is:

> **We code the cognitive physics. Synrheon learns the cognitive skill.**

E011 is divided into two gates so scientific evidence is not confused with live integration:

```text
E011-A — Controlled Process-Transfer Assay
prove a trainable policy learns reusable bounded search behavior

E011-B — Live Organism Integration
wire the proven policy through cognition.py → thin runtime → state/trace/UI
```

Passing E011-A does **not** mean the mechanism is Integrated. E011-B is required for that claim.

# E011-A — Controlled Process-Transfer Assay

## Frozen Experiment Version

```text
experiment_id: E011-A
generator_version: e011a-v1
action_contract_version: e011a-actions-v1
state_contract_version: e011a-state-v1
hard_action_budget: 10
model_initialization_seeds: 11, 22, 33, 44, 55
```

Any material change to the task generator, policy-visible features, action semantics, final seed split, or pass thresholds creates a new experiment version. It must not be silently treated as the same preregistered result.

## Exact First Problem Family — Bounded Partial Graph Discovery

The first test deliberately asks Synrheon to learn a small reusable search process rather than language semantics.

Each generated episode contains:

```text
10–14 opaque concept nodes
1 visible start node
1 hidden goal-marked node
1 unique shortest start→goal path of 3–5 edges
2–4 distractor branches
0–2 generated cross/back edges where valid
opaque per-world node identities
no natural-language labels with useful meaning
```

The start node is revealed at episode start. Other nodes and edges are hidden until a cognitive action reveals them.

The goal is not identified by a meaningful word. When the goal node itself becomes revealed, its terminal `is_goal` marker becomes legitimate observable state. Before reveal, the policy receives no goal-location information.

The task is successful only when the policy reveals the goal and chooses `STOP` within the fixed 10-action budget.

The task is intentionally multi-step: the goal cannot be initially visible, and the unique shortest route requires at least three edge transitions.

## Why This Task Exists

This is not intended to prove general intelligence. It tests a narrower causal question:

> Can training produce a reusable policy for where to spend limited cognitive expansion next, rather than merely memorizing node identities or developer-authored routes?

A useful learned process should increasingly avoid wasteful deep distractor exploration, preserve budget, reveal the goal, and stop when appropriate on unfamiliar generated worlds.

## Policy-Visible CognitiveState — Information Firewall

The policy may receive only information legitimately available from the revealed episode state.

### Policy may see

```text
checkpoint / action index
remaining hard action budget
revealed nodes only
revealed edges only
for each revealed node:
    candidate slot / opaque handle
    depth from revealed start through known structure
    expanded / unexpanded state
    reveal order / frontier status
    is_goal only if that node has already been revealed
available valid operation + target candidates
previous selected operation + target summary
```

Opaque concept handles exist only so the chosen target can be executed. E011-A must not learn a persistent embedding keyed to stable concept identity. Candidate slots are generated from current revealed state rather than a global vocabulary.

### Policy must never see

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
scorer rankings
world seed as a predictive feature
```

### Scorer / experiment harness may see

The experiment harness may retain the complete generated graph, hidden goal, shortest route, reference costs, and success truth for evaluation and training signal.

That hidden information must remain structurally outside production cognition inputs.

Conceptually:

```text
GENERATOR / SCORER
full hidden graph ───────────────→ scoring / training evidence
      │
      │ revealed state only
      ↓
CognitiveState
      ↓
cognition policy
      ↓
operation + target
      ↓
bounded environment transition
      ↓
next revealed CognitiveState
```

If any hidden field enters policy features, the E011-A result is invalid regardless of score.

## Frozen First Action Contract

E011-A deliberately begins with the smallest action vocabulary that can test learned target selection and stopping.

### `EXPAND(target)`

Valid target: one currently revealed, unexpanded frontier node.

Deterministic effect:
- mark that target as expanded;
- reveal its currently hidden outgoing edges and newly reached nodes;
- update the revealed graph/frontier;
- expose `is_goal` only for newly revealed nodes that actually are the generated goal;
- consume exactly 1 cognitive action.

Python may enumerate which `EXPAND(target)` actions are currently valid. Python may **not** choose which target is cognitively preferable.

### `STOP`

Deterministic effect:
- terminate the episode;
- consume exactly 1 cognitive action;
- success only if the goal marker has already been revealed;
- otherwise record premature-stop failure.

No other operation is part of E011-A v1. `FOCUS`, `RETRIEVE`, `COMPARE`, `CHECK_EVIDENCE`, `PREDICT`, `REVISE`, and richer parameterization remain later expansions after the first transfer mechanism is understood.

This narrow first vocabulary is intentional: the causal question is whether **learned operation/target selection under bounded compute** transfers at all.

## Seed Splits — Frozen Before Training

World-generation seeds are disjoint:

```text
TRAIN
1000–4999
4000 generated worlds/tasks

DEVELOPMENT VALIDATION
5000–5999
1000 generated worlds/tasks
may be used for architecture/training development
must not be reported as final transfer evidence

FINAL LEVEL-1 HELD-OUT
10000–10999
1000 generated worlds/tasks
must not be used for tuning

RENAMING / IDENTITY-PERMUTATION CONTROL
same held-out world seeds 10000–10999
paired independent permutation seeds 20000–20999

FUTURE LEVEL-2 STRUCTURAL GATE
30000–30999
1000 worlds from a separately versioned topology-distribution change
not part of the initial E011-A pass
```

The five model initialization/training seeds are frozen as:

```text
11
22
33
44
55
```

Final claims report all five runs, not only the best seed.

Once the final held-out split has been inspected, any model, feature, reward, generator, or hyperparameter change intended to improve that result creates a new experiment revision with a fresh untouched final split. The old result remains recorded.

## Baselines

E011-A must report at least four references:

### Random-valid policy

Uniformly choose among currently valid `EXPAND(target)` actions plus `STOP`.

This estimates chance behavior under the same action contract and budget.

### Matched untrained model

Evaluate the exact trainable architecture before optimization for each frozen model seed.

This proves that any gain is not merely an architectural prior or favorable initialization.

### Trained model

The learned policy after the documented training configuration.

### Exhaustive all-reachable reference

A non-learning experiment-only reference that expands every reachable node needed to fully expose the generated world and then stops.

This reference is not production cognition and is not a competitor the trained policy must imitate. It provides a cost ceiling for how much work brute-force discovery requires.

A separate deterministic breadth-first diagnostic may be recorded for interpretation, but it is not a production policy and must not be copied into `cognition.py`.

## Training Record Contract

Each cognitive checkpoint preserves at least:

```text
state_before
available_actions_and_targets
selected_action
state_after
predicted_state_after        # when prediction is implemented
expected_value               # when value is implemented
observed_outcome
compute_cost
error_or_correction
credit_assignment
alternative_action_estimates # may initially be deferred/null, but field remains available
```

Selected does not mean useful. Credit must derive from outcome/evidence rather than from having appeared in a successful episode.

## Required Cost Measurements

Record:

```text
total cognitive actions
EXPAND count
STOP count
premature STOP count
invalid decoded action count
invalid target count
repeated / stale target attempt count
budget exhaustion count
mean and median actions on successful episodes
mean fraction of 10-step budget consumed
exhaustive-reference action cost on the same world
```

If the model succeeds only by approaching exhaustive cost, that is not useful sparse cognition.

## Model Artifact / Development Lineage Contract

Every saved policy checkpoint intended for comparison must preserve:

```text
model_id
parent_model_id
experiment_id + experiment_version
generator_version
state_contract_version
action_contract_version
model architecture identifier
model initialization seed
training world seed range
optimizer / training configuration hash
episodes_seen
checkpoint index
parameter checksum
source Git commit
created timestamp
evaluation summary
strongest demonstrated generalization level
```

This allows Synrheon's cognitive development to be compared across actual parameter generations rather than by filename or memory.

## Cognitive-Growth History Contract

Evaluation history should preserve immutable records containing at least:

```text
model_id
checkpoint / episodes_seen
evaluation split
world seed range
success rate
mean / median cognitive actions
budget exhaustion rate
premature STOP rate
invalid action / target rate
exhaustive-cost ratio
random-valid baseline
matched-untrained baseline
renaming-paired result where applicable
strongest demonstrated generalization level
experiment/config hash
```

For the existing Organism UI, a backend-owned summary may expose fields such as:

```text
learning_metrics:
    model_version
    training_episode
    training_success
    held_out_success
    renamed_success
    cognitive_efficiency
    strongest_generalization_level
    verdict
    detail
```

The UI displays this evidence. It must not calculate or invent the scientific truth itself.

## Pre-Registered Failure Taxonomy

A poor result should be classified rather than patched locally.

### Failed learning

Training performance does not improve at least 10 percentage points over the matched untrained model.

Interpretation: optimization/model capacity/training signal may be inadequate before any transfer claim is considered.

### Memorization / training overfit

Training success reaches at least 70%, but final held-out success is less than 10 percentage points above random-valid behavior.

Interpretation: the policy fit the training distribution without learning a reusable process.

### Identity shortcut

Paired renaming causes more than a 10-percentage-point absolute drop in held-out success.

Interpretation: concept identity leaked into behavior despite the intended opaque representation.

### Structural overfit

Level 1 passes but later Level-2 structural evaluation drops more than 20 percentage points and falls near baseline.

Interpretation: the policy learned a process tied to the original topology distribution, not a broader structural skill.

### Inefficient cognition

Success thresholds pass, but successful held-out episodes consume more than 90% of the exhaustive all-reachable reference cost on average or more than 85% of the hard budget.

Interpretation: the policy found answers mainly through brute-force exploration.

### Insufficient / misleading representation

Multiple model configurations fail while inspection shows the permitted state omits information necessary for any policy to improve, or exposes a feature that directly encodes the route.

Interpretation: revisit `CognitiveState` rather than tuning around a broken information boundary.

### Answer leakage

Any hidden graph, goal-location, shortest-path, correct-action, or solver-derived feature reaches policy input or target selection.

Interpretation: invalidate the result and fix the boundary before continuing.

## Frozen Quantitative E011-A Pass Gate

E011-A v1 is promising only if **all** of the following are true:

1. Parameters change measurably from the matched untrained checkpoints and parameter checksums differ.
2. At least 4 of 5 model seeds improve training success by **20 percentage points or more** over their own untrained checkpoints.
3. Median final Level-1 held-out success across the five model seeds is at least **70%**.
4. Median final Level-1 held-out success is at least **20 percentage points above both** the random-valid baseline and matched-untrained baseline.
5. At least 4 of 5 model seeds individually beat both final baselines by at least **15 percentage points**.
6. Paired renaming retains at least **95% of unrenamed held-out success** and causes no more than a **5-percentage-point median absolute drop**.
7. Held-out success includes tasks whose shortest path is 3, 4, and 5 edges; no success claim may come only from the easiest depth subset.
8. On successful held-out episodes, mean cognitive action cost is at most **80% of the exhaustive all-reachable reference cost** on the same worlds.
9. Mean hard-budget consumption on held-out episodes is at most **80%** while maintaining the success thresholds above.
10. No hidden-answer or hidden-route field reaches policy input.
11. No production branch names a world, node identity, seed, expected route, or correct target.
12. Python enumerates valid actions but does not choose the cognitively preferred target.
13. Unrelated world/organism state is not mutated by policy inference.
14. Results for all five frozen seeds are reported, including failures.

These are experiment thresholds, not permanent architecture constants.

If a threshold is changed after seeing final results, the changed run is a new experiment revision and cannot retroactively pass E011-A v1.

## Architecture-Reconsideration / Stop-Tuning Rules

Do not endlessly tune a failing benchmark.

Revisit the state/action/task architecture rather than continuing local hyperparameter changes when any of the following occurs:

- two materially different small model configurations each reach at least 80% training success but remain less than 10 percentage points above random on untouched Level-1 validation;
- concept-renaming repeatedly loses more than 10 percentage points despite no intended identity feature;
- improvements in success occur only by driving mean budget use above 85%;
- random-valid and trained behavior remain nearly indistinguishable because the generated task is too easy, too hard, or underdetermined;
- a useful result requires adding a feature that encodes distance-to-goal, on-path status, the correct next action, or another solver-derived shortcut;
- the only apparent fix is a world-specific branch or special-case target selector.

Development validation may guide iteration. Final held-out data must not become a tuning surface.

## Generalization Levels

Every result must be classified at the strongest demonstrated level:

```text
Level 0 — Training memorization
same training distribution only

Level 1 — Identity / instance transfer
unseen generated worlds with unseen opaque identities from the same experiment family
plus paired identity permutation control

Level 2 — Structural transfer
new concepts + separately versioned topology / relation arrangement distribution

Level 3 — Compositional transfer
new knowledge + new structure + novel combinations of cognitive demands
```

Do not summarize Level-1 success as unrestricted “learned how to think.”

## E011-A Status

**Fully preregistered / implementation not started.**

The task, information firewall, action semantics, budgets, seed ranges, baselines, failure taxonomy, artifact lineage, growth-history fields, stop-tuning rules, and quantitative first gate are frozen for `E011-A v1` before model implementation.

# E011-B — Live Organism Integration Gate

E011-B begins only after an E011-A artifact satisfies the preregistered gate or is explicitly carried forward as a clearly labeled experimental exception.

The integration path must be:

```text
legitimate live CognitiveState
        ↓
cognition.py
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
UI behavioral evidence + growth history
```

The generated experiment's hidden world/scorer must remain outside the live production cognition path.

E011-B must prove:

1. the exact identified model artifact loads through the intended cognition owner;
2. runtime sequences but does not select cognitive actions or targets;
3. live checkpoints reach explicit state/trace;
4. the Organism UI shows the specific integrated stage and backend-owned learning/generalization evidence;
5. the same policy behavior remains available after model reload/restart when persistence is enabled;
6. malformed/mismatched state fails safely;
7. unrelated persistent state is not silently mutated;
8. focused and integration tests prove the real call path;
9. no hidden experiment scorer or solution metadata enters production cognition.

Only after this live gate may the policy be called **Integrated**. Human testing through the running organism is still required for **Verified**.
