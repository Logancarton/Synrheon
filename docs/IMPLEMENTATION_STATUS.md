# Synrheon Implementation Status

This document records implemented truth, not future intention.

## Status Definitions

- **Not Started** — no meaningful implementation exists.
- **Designed** — architecture is defined, but functional implementation does not yet exist.
- **Built** — the mechanism exists and works in isolation.
- **Integrated** — the live Synrheon runtime reaches and uses the mechanism.
- **Verified** — intended behavior has been demonstrated through the running organism and relevant state/trace inspected. Automated tests alone cannot grant this status.

## Cognitive Effect

- **Infrastructure**
- **Supporting cognition**
- **Cognitive improvement**

| Stage | Capability | Status | Cognitive Effect | Evidence |
|---|---|---|---|---|
| 0A | Architecture Stewardship | Designed | Infrastructure | Agent + canonical development workflow |
| 0B | Observable Runtime + Development UI | Verified | Infrastructure | Connected browser/API/runtime/state path; live browser verification |
| 0B.1 | Organism stage/evidence dashboard | Built | Infrastructure | UI renders backend-owned stage evidence, experience, substrate, provenance, activation, and reserved learning metrics |
| 1 | Cognitive Substrate | Built | Supporting cognition | Concepts, world relations, open-ended organism relations, activation representation |
| 1P | Trainable Cognitive Policy architecture | Designed | Supporting cognition | State/action/checkpoint/transfer contract documented; no production policy yet |
| 1P.A | E011-A v1 controlled process-transfer assay | Designed / preregistered | Supporting cognition | Exact generated task, information firewall, actions, seeds, baselines, costs, failure taxonomy, numeric gate frozen before implementation |
| 1P.B | E011-B live organism integration gate | Designed | Supporting cognition | Live cognition.py → thin runtime → state/trace/UI contract documented; implementation absent |
| 1P.1 | CognitiveState feature representation | Not Started | Cognitive improvement | E011-A visible/hidden field contract frozen; code absent |
| 1P.2 | Parameterized cognitive-action representation | Designed | Supporting cognition | E011-A v1 fixed to `EXPAND(target)` + `STOP`; implementation absent |
| 1P.3 | State → cognitive-action/target policy | Not Started | Cognitive improvement | |
| 1P.4 | One-action → checkpoint transition loop | Not Started | Cognitive improvement | |
| 1P.5 | Transition / next-state prediction | Designed | Supporting cognition | `F(S,a) → S'` boundary documented; model absent and not required for first E011-A policy-only slice |
| 1P.6 | Expected cognitive value | Designed | Supporting cognition | `V(S,a)` kept distinct from transition prediction; model absent and not required for first E011-A policy-only slice |
| 1P.7 | Outcome/error/credit training trace | Designed | Supporting cognition | Trace contract includes outcome, cost, alternatives, and future prediction/value fields |
| 1P.8 | Generated world/task curriculum | Designed / preregistered | Supporting cognition | `e011a-v1`: 10–14 opaque-node partial graphs, hidden goal, distractors, fixed budget and frozen seed ranges |
| 1P.9 | Transfer harness | Designed / preregistered | Supporting cognition | Frozen train/validation/final/renaming/model seeds and quantitative Level-1 gate |
| 1P.10 | Cognitive-cost evaluation | Designed / preregistered | Supporting cognition | 10-action ceiling; step/expand/stop/budget/exhaustive-reference measurements and pass thresholds fixed |
| 1P.11 | Counterfactual / alternative-action credit | Designed | Supporting cognition | Alternative action field preserved; estimator may be deferred in first slice |
| 1P.12 | Live runtime invocation of learned policy | Not Started | Cognitive improvement | E011-B only after controlled policy artifact exists |
| 2 | Computational Time + Experience | Integrated | Supporting cognition | Current-episode timestamp, elapsed time, sequence, provenance, previous/next links live |
| 3A | Hand-written Sparse Activation experiment | Removed / superseded | Experimental cognition | Lexical matching, fixed spreading, decay, inhibition, Top-K, and fixed recurrence removed from production |
| 3B | Durable Memory | Not Started | Cognitive improvement | Current experience remains process-local |
| 4 | Level 1→2→3 Retrieval | Not Started | Cognitive improvement | |
| 5 | Scratchpad + Recursive Loop | Not Started | Cognitive improvement | |
| 6 | Problems + Trials + Solutions | Not Started | Cognitive improvement | |
| 7 | Learning + Plasticity | Not Started | Cognitive improvement | Narrow organism-relation storage update exists; no live outcome credit assignment |
| 8 | Consolidation + Abstraction | Not Started | Cognitive improvement | |
| 9 | Multi-Layer Training | Not Started | Cognitive improvement | |
| 10 | Continuous Autonomous Cognition | Not Started | Cognitive improvement | |
| 11 | External Intelligence + Tools | Not Started | Supporting cognition | |

## Current Cognition Truth

```text
Hand-written lexical concept matching                 Removed
Hand-written relation spreading                       Removed
Fixed spread/decay/salience gains                     Removed
Fixed recurrence count                                Removed
Winner-relative inhibition heuristic                  Removed
Fixed Top-K cognitive policy                          Removed
Cognitive activation frames from that heuristic       Removed
Chat → ordered observed experience                    Integrated
Internal Thought → ordered injected experience        Integrated
Organism UI backend-evidence surface                  Built
Cognition.py owner retained for trainable policy      Designed
Cognitive physics vs learned-skill boundary           Designed
Micro-cycle / checkpoint contract                     Designed
Parameterized action/target contract                  Designed
E011-A exact task family                              Designed / preregistered
E011-A policy-visible information firewall            Designed / preregistered
E011-A 10-action hard budget                          Designed / preregistered
E011-A frozen seed splits                             Designed / preregistered
E011-A numeric pass/failure gates                     Designed / preregistered
Model lineage / cognitive-growth record contract      Designed
E011-B live integration gate                          Designed
Trainable state → action → next-state policy          Not Started
Semantic language understanding                       Not Started
Natural-language response generation                  Not Started
Durable retrieval                                     Not Started
Autonomous recursive thought                          Not Started
```

The important pivot is intentional: the runtime no longer mutates activation merely because a text string happens to match a concept label or because a fixed graph rule says where activation should spread.

## E011-A v1 Preregistered Truth

### First generated problem family

```text
bounded partial graph discovery
10–14 opaque nodes
1 visible start
1 hidden goal marker
unique shortest route 3–5 edges
2–4 distractor branches
0–2 cross/back edges
10-action hard ceiling
```

### First action contract

```text
EXPAND(target)
STOP
```

The environment may enumerate valid `EXPAND(target)` candidates. It may not choose which target is preferable.

### Policy-visible state

```text
checkpoint / action index
remaining budget
revealed nodes and edges
known depth from start
frontier / expanded state
reveal order
is_goal only after reveal
available valid action + target candidates
previous action summary
```

### Hidden from policy

```text
unrevealed graph
hidden goal location
shortest path
shortest-path distance
on-solution-path flags
correct next action / target
future frontier
scorer / solver output
world seed as predictive input
```

### Frozen world/model seeds

```text
train                    1000–4999
development validation   5000–5999
final Level-1 held-out   10000–10999
paired renaming          20000–20999
future Level-2           30000–30999
model seeds              11, 22, 33, 44, 55
```

### Frozen first gate

```text
4/5 seeds improve training success by ≥20 percentage points
median final held-out success ≥70%
median held-out gain ≥20 points over random and untrained
4/5 seeds individually beat both baselines by ≥15 points
paired renaming retains ≥95% of held-out success
median renaming drop ≤5 points
successful mean cost ≤80% of exhaustive all-reachable reference
mean held-out hard-budget use ≤80%
no hidden-answer leakage
no hand-written preferred-target selection
all five seed results reported
```

These are experiment settings, not permanent architecture constants.

## Predefined Failure Taxonomy

```text
Failed learning
    training fails to improve meaningfully

Memorization / training overfit
    training works, untouched transfer stays near random

Identity shortcut
    renaming causes material collapse

Structural overfit
    Level 1 works, later changed topology collapses

Inefficient cognition
    success depends on near-exhaustive exploration

Insufficient / misleading representation
    permitted state is missing necessary information or contains route leakage

Answer leakage
    hidden graph/goal/path/solver data reaches cognition
```

Failure classification should guide which owner or representation is revisited. It should not trigger benchmark-specific patch branches.

## Stop-Tuning Rule

Architecture review is required instead of continued local tuning when multiple materially different small models fit training but fail untouched transfer, renaming repeatedly collapses, success rises only by exhausting the hard budget, the task is too easy/hard to distinguish trained from random behavior, or a proposed fix requires solver-derived features or hand-written target routing.

Final held-out data is not a development surface. Once inspected, material changes create a new experiment revision with a fresh untouched final split.

## Model Lineage / Growth History Contract

A meaningful policy artifact should preserve:

```text
model_id
parent_model_id
experiment/generator/state/action versions
model architecture id
model seed
training seed range
configuration hash
episodes_seen
checkpoint index
parameter checksum
source Git commit
evaluation summary
strongest demonstrated generalization level
```

Historical evaluation records should preserve training, held-out, renaming, cognitive cost, budget use, baseline comparisons, and generalization level.

The Organism UI may display backend-owned summaries such as:

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

The UI does not own or invent these metrics.

## E011-B Integration Truth

A controlled E011-A result is not `Integrated`.

The live gate must eventually be:

```text
legitimate live CognitiveState
        ↓
cognition.py
learned operation + target
        ↓
bounded transition / checkpoint
        ↓
thin runtime
        ↓
OrganismState + trace
        ↓
Organism UI
```

The hidden experiment generator/scorer must not enter this production path.

## Stage 1 Representation Truth

```text
Concept identity                                      Built
WorldRelation representation                          Built
Open-ended OrganismRelation representation            Built
Injected/learned organism-relation separation         Built
Arbitrary relation type stored as data                Built
Explicit concept/world/injected-self injection        Integrated
Free-form organism relation UI/API path               Integrated
Confidence-weighted learned-relation storage update   Built
Learned evidence lineage                              Built
ActivationState representation                        Built
Automatic relation discovery from live experience     Not Started
Automatic self-learning from live outcomes            Not Started
```

The existing learned organism-relation update remains a narrow provenance-preserving storage mechanism; it is **not** a routing/thinking policy.

## Current Temporal / Experience Foundation

```text
Episode ID                                            Integrated
Absolute event timestamp                              Integrated
Elapsed episode time                                  Integrated
Monotonic experience sequence                         Integrated
Observed vs injected provenance                       Integrated
Previous / next event links                           Integrated
Experience event linked from stimulus                 Integrated
Internal Thought thread visualization                 Integrated
Organism live experience evidence view                Built
Durable cross-process memory                          Not Started
Day membership / temporal context                     Not Started
Recent trajectory model                               Not Started
```

The current thread is autobiographical **current-process experience**, not durable memory.

## Current Experimental Gate

The next code to build is E011-A v1. It must first demonstrate controlled learned process transfer under the frozen contract above.

Only after that evidence exists should E011-B wire the resulting policy through the live runtime and UI.

A successful training-world result without untouched transfer is **not** a cognitive improvement claim.

## Stage 0B Component Truth

```text
Modern development UI shell                           Verified
Browser → Python HTTP boundary                         Verified
Start / Step / Continue / Pause                        Verified
External Chat stimulus channel                         Verified
Internal thought injection channel                     Verified
In-memory session state + trace                        Verified
Human live-browser inspection                          Verified
Organism stage/evidence dashboard                     Built
```

`Think One Step` and `Continue` still advance harness cycles only. They do not yet invoke a trainable cognitive policy.
