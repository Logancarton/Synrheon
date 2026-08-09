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
| 1 | Cognitive Substrate | Built | Supporting cognition | Concepts, world relations, open-ended organism relations, activation representation |
| 1P | Trainable Cognitive Policy | Designed | Cognitive improvement | Architecture pivot defined; production thinking policy intentionally not implemented yet |
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
Fixed spread/decay/salience gains                      Removed
Fixed recurrence count                                Removed
Winner-relative inhibition heuristic                  Removed
Fixed Top-K cognitive policy                          Removed
Cognitive activation frames from that heuristic       Removed
Chat → ordered observed experience                    Integrated
Internal Thought → ordered injected experience        Integrated
Cognition.py owner retained for trainable policy      Designed
Trainable state → action → next-state policy          Not Started
Transfer training on unseen knowledge worlds          Not Started
Semantic language understanding                       Not Started
Natural-language response generation                  Not Started
Durable retrieval                                     Not Started
Autonomous recursive thought                          Not Started
```

The important pivot is intentional: the runtime no longer mutates activation merely because a text string happens to match a concept label or because a fixed graph rule says where activation should spread.

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
Episode ID                                        Integrated
Absolute event timestamp                           Integrated
Elapsed episode time                               Integrated
Monotonic experience sequence                      Integrated
Observed vs injected provenance                    Integrated
Previous / next event links                        Integrated
Experience event linked from stimulus              Integrated
Internal Thought thread visualization              Integrated
Durable cross-process memory                       Not Started
Day membership / temporal context                  Not Started
Recent trajectory model                            Not Started
```

The current thread is autobiographical **current-process experience**, not durable memory.

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

`Think One Step` and `Continue` still advance harness cycles only. They do not yet invoke a trainable cognitive policy.
