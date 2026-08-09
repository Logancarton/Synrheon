# Synrheon Implementation Status

This document records implemented truth, not future intention.

## Status Definitions

- **Not Started** — no meaningful implementation exists.
- **Designed** — architecture is defined, but functional implementation does not yet exist.
- **Built** — the mechanism exists and works in isolation.
- **Integrated** — the live Synrheon runtime reaches and uses the mechanism.
- **Verified** — intended live behavior has been demonstrated through the running organism and relevant state/trace inspected.

## Cognitive Effect

- **Infrastructure**
- **Supporting cognition**
- **Cognitive improvement**

| Stage | Capability | Status | Cognitive Effect | Evidence |
|---|---|---|---|---|
| 0A | Architecture Stewardship | Designed | Infrastructure | Agent + canonical workflow |
| 0B | Observable Runtime + Development UI | Verified | Infrastructure | Connected browser/API/runtime/state path; prior live browser verification |
| 0B.1 | Organism stage/evidence dashboard | Built | Infrastructure | UI renders backend-owned stage/experience/substrate/provenance/activation surfaces |
| 1 | Cognitive Substrate | Built | Supporting cognition | Concepts, world relations, open-ended organism relations, activation representation |
| 1P | Trainable Cognitive Policy | Built experimentally | Cognitive improvement | E011-A policy exists and controlled Level-1 transfer gate passed; not live-integrated |
| 1P.A | E011-A v1 controlled process-transfer assay | Built / controlled gate passed | Cognitive improvement | Five frozen model seeds, untouched held-out worlds, paired renaming, cost gate |
| 1P.B | E011-B live organism integration | Designed | Supporting cognition | `cognition.py → thin runtime → state/trace/UI` contract; implementation still absent |
| 1P.1 | CognitiveState feature representation | Built | Supporting cognition | Explicit revealed-only `CognitiveState` + `RevealedNode`; hidden solver state excluded |
| 1P.2 | Parameterized cognitive-action representation | Built | Supporting cognition | `EXPAND(target)` + `STOP` with validation |
| 1P.3 | State → cognitive-action/target policy | Built | Cognitive improvement | Trainable linear softmax policy chooses operation/target from visible features |
| 1P.4 | One-action → checkpoint transition loop | Built in controlled assay | Cognitive improvement | `PartialGraphEpisode` produces bounded revealed-state transitions; not runtime-integrated |
| 1P.5 | Transition / next-state prediction | Designed | Supporting cognition | `F(S,a) → S'` boundary only; learned predictor absent |
| 1P.6 | Expected cognitive value | Designed | Supporting cognition | `V(S,a)` boundary only; learned value estimator absent |
| 1P.7 | Outcome/error/credit update | Built, first narrow slice | Cognitive improvement | `ReinforceLearner` updates policy from outcome/cost returns; full future trace schema still broader |
| 1P.8 | Generated world/task curriculum | Built | Supporting cognition | Deterministic `e011a-v1` generated partial-graph worlds |
| 1P.9 | Transfer harness | Built / Level-1 gate passed | Cognitive improvement | Frozen train/final/renaming/model seeds evaluated |
| 1P.10 | Cognitive-cost evaluation | Built | Supporting cognition | Budget use + exhaustive-reference ratio recorded |
| 1P.11 | Counterfactual / alternative-action credit | Designed | Supporting cognition | Candidate probabilities are available during learning; explicit counterfactual estimator not built |
| 1P.12 | Live runtime invocation of learned policy | Not Started | Cognitive improvement | E011-B next |
| 2 | Computational Time + Experience | Integrated | Supporting cognition | Current-episode timestamp, elapsed time, sequence, provenance, previous/next links live |
| 3A | Hand-written Sparse Activation experiment | Removed / superseded | Experimental cognition | Fixed lexical/spreading/Top-K path removed |
| 3B | Durable Memory | Not Started | Cognitive improvement | Current experience remains process-local |
| 4 | Level 1→2→3 Retrieval | Not Started | Cognitive improvement | |
| 5 | Scratchpad + Recursive Loop | Not Started | Cognitive improvement | |
| 6 | Problems + Trials + Solutions | Not Started | Cognitive improvement | |
| 7 | Broader Learning + Plasticity | Not Started | Cognitive improvement | E011-A has a narrow policy learner only; organism-wide learning is not integrated |
| 8 | Consolidation + Abstraction | Not Started | Cognitive improvement | |
| 9 | Multi-Layer Training | Not Started | Cognitive improvement | |
| 10 | Continuous Autonomous Cognition | Not Started | Cognitive improvement | |
| 11 | External Intelligence + Tools | Not Started | Supporting cognition | |

## Current E011-A v1 Evidence

Evidence artifact:

```text
data/e011a_v1_evidence.json
```

Source implementation commit recorded by the artifact:

```text
f73f0c043cd2fb1c7015c55df312b4397effd252
```

Controlled result:

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

All five frozen model seeds are recorded. Held-out success is present on shortest-path depths 3, 4, and 5.

The recorded numeric gate passed every frozen quantitative check.

## What Was Actually Learned

The policy feature vector contains no opaque node identity embedding and no hidden shortest-path/goal-location feature.

Training changed the policy from behavior that was near-total failure into a reusable preference over visible cognitive structure:

```text
revealed state
    ↓
score valid EXPAND(target) / STOP candidates
    ↓
choose target based on learned visible-state features
    ↓
observe transition outcome + cognitive cost
    ↓
update policy weights
```

This is **Level 1 — identity / instance transfer** only.

It is not yet evidence of:

```text
Level 2 structural transfer
Level 3 compositional transfer
semantic reasoning
language understanding
durable memory
recursive autonomous thought
```

## Information-Firewall Truth

Policy-visible:

```text
checkpoint/action index
remaining budget
revealed nodes and edges
known revealed depth
frontier / expanded state
reveal order
is_goal only after reveal
available valid actions + targets
previous action summary
```

Hidden from policy:

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

The hidden generator/scorer lives outside production cognition in `experiments/e011a.py`.

## Current Cognition Truth

```text
Hand-written lexical concept matching                 Removed
Hand-written relation spreading                       Removed
Fixed spread/decay/salience gains                     Removed
Fixed recurrence count                                Removed
Fixed Top-K cognitive policy                          Removed
Chat → ordered observed experience                    Integrated
Internal Thought → ordered injected experience        Integrated
Organism UI backend-evidence surface                  Built
E011-A CognitiveState                                 Built
E011-A action/target representation                   Built
E011-A trainable policy                               Built
E011-A outcome-driven weight update                   Built
E011-A generated curriculum/scorer                    Built outside production cognition
E011-A controlled Level-1 transfer gate               Passed
E011-B live runtime invocation                        Not Started
Transition prediction model                           Not Started
Expected cognitive value model                        Not Started
Semantic language understanding                       Not Started
Natural-language response generation                  Not Started
Durable retrieval                                     Not Started
Autonomous recursive thought                          Not Started
```

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
Durable cross-process memory                          Not Started
```

## Current Experimental Gate

**E011-A v1 is complete as a controlled Built experiment.**

The next gate is E011-B:

```text
identified trained artifact
        ↓
legitimate live CognitiveState
        ↓
cognition.py policy inference
        ↓
bounded transition/checkpoint
        ↓
thin runtime sequencing
        ↓
OrganismState / trace
        ↓
Organism UI
```

The hidden E011 generator/scorer must not enter that production path.

Until E011-B exists, the trained policy must not be called **Integrated**.

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

`Think One Step` and `Continue` still advance harness cycles only. They do not yet invoke the E011-A policy.
