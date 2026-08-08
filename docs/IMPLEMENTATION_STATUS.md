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
| 1 | Cognitive Substrate + activation handoff | Integrated | Cognitive improvement | Concepts/world/open organism relations/current activation plus Chat/Internal Thought routed through cognition owner |
| 2 | Computational Time + Experience | Integrated | Supporting cognition | Current-episode timestamp, elapsed time, sequence, provenance, previous/next links live; partial Stage 2 |
| 3A | Sparse Activation slice | Integrated | Cognitive improvement | Generic lexical seed → directed relation spread → organism salience → competition/Top-K is reached by live stimulus path |
| 3B | Durable Memory | Not Started | Cognitive improvement | Current experience/activation is still process-local |
| 4 | Level 1→2→3 Retrieval | Not Started | Cognitive improvement | |
| 5 | Scratchpad + Recursive Loop | Not Started | Cognitive improvement | |
| 6 | Problems + Trials + Solutions | Not Started | Cognitive improvement | |
| 7 | Learning + Plasticity | Not Started | Cognitive improvement | Narrow organism-relation update exists, but live outcome credit assignment does not |
| 8 | Consolidation + Abstraction | Not Started | Cognitive improvement | |
| 9 | Multi-Layer Training | Not Started | Cognitive improvement | |
| 10 | Continuous Autonomous Cognition | Not Started | Cognitive improvement | |
| 11 | External Intelligence + Tools | Not Started | Supporting cognition | |

## Current Cognitive Activation Truth

```text
Generic concept ID/label lexical cue matching          Integrated
Semantic language understanding                       Not Started
Directed world-relation spreading                      Integrated
Outgoing fan-out normalization                         Integrated
Open-ended organism-relation salience                  Integrated
Organism salience limited to already-reached concepts  Integrated
Activation decay                                       Integrated
Winner-relative inhibition threshold                   Integrated
Bounded Top-K sparse active region                     Integrated
Observable cognitive activation frames                 Integrated
Chat → cognition owner                                 Integrated
Internal Thought injection → cognition owner           Integrated
Natural-language response generation                   Not Started
Retrieval from durable memory                          Not Started
Autonomous recursive thought                           Not Started
```

The first activation configuration is general mechanism data, not stimulus-specific rules:

```text
seed strength       1.00
decay               0.30
spread gain         0.62
organism gain       0.35
inhibition fraction 0.10
activation floor    0.05
Top-K               5
recurrent rounds    3
```

These are initial hyperparameters to test and learn from later. They are not semantic facts.

The lexical matcher is a temporary bootstrap. It only recognizes concept IDs/labels that already exist in the injected substrate and should not be described as language understanding.

An unmatched stimulus still becomes observed/injected experience, produces an observable `unmatched` cognitive frame, and clears stale activation rather than pretending it understood the text.

## Stage 1 Representation Truth

```text
Concept identity                                      Built
WorldRelation representation                          Built
Open-ended OrganismRelation representation            Built
Injected/learned organism-relation separation         Built
Arbitrary relation type stored as data                Built
Explicit concept/world/injected-self injection        Integrated
Free-form organism relation UI/API path               Integrated
Confidence-weighted learned-relation update           Built
Learned evidence lineage                              Built
Automatic relation discovery from live experience     Not Started
Automatic self-learning from live outcomes            Not Started
ActivationState representation                        Integrated
```

The learned-relation update remains:

```text
learned_new
=
learned_old
+
(learning_rate × trust)
×
(observed_strength - learned_old)
```

It changes only the learned relation collection for that arbitrary relation type. It does not mutate injected organism relations or world knowledge.

## Current Temporal / Experience Foundation

```text
Episode ID                                        Integrated
Absolute event timestamp                           Integrated
Elapsed episode time                               Integrated
Monotonic experience sequence                      Integrated
Observed vs injected provenance                    Integrated
Previous / next event links                        Integrated
Experience event linked from stimulus              Integrated
Internal Thought thread visualization              Integrated
Cognitive frame linked to experience               Integrated
Durable cross-process memory                       Not Started
Day membership / temporal context                  Not Started
Recent trajectory model                            Not Started
```

The current thread is autobiographical **current-process experience**, not durable memory.

## Candidate Verification Evidence

The Stage 1 sparse-activation candidate was exercised in an isolated local reconstruction of the exact candidate Python sources because direct GitHub cloning is unavailable in the execution sandbox.

Results:

```text
Focused activation preview     Passed
Runtime live-path preview      Passed
HTTP/API integration preview   Passed
Current test suite             12/12 passed
Python compileall              Passed
```

Human live browser/state inspection is still required before the new cognitive behavior is called **Verified**.

## Stage 0B Component Truth

```text
Modern development UI shell                       Verified
Browser → Python HTTP boundary                     Verified
Start / Step / Continue / Pause                    Verified
External Chat stimulus channel                     Verified
Internal thought injection channel                 Verified
In-memory session state + trace                    Verified
Human live-browser inspection                      Verified
```

`Think One Step` and `Continue` still advance harness cycles only. The new cognition currently runs when a textual external/internal experience arrives; this is not autonomous continuation.
