# Cognitive Experiments

## Evidence Standard

The preferred experiment is a real stimulus applied through the running Synrheon organism.

Record:
- stimulus or action
- baseline behavior
- expected behavior
- observed UI/runtime output
- relevant internal state or trace
- interpretation

Automated tests may protect a discovered behavior but should not be treated as the only evidence that cognition works.

## E000 — Stage 0B Connected Organism Transport

Hypothesis: a browser-facing control/input request can cross into the real Python runtime, mutate Synrheon-owned session state, and return an observable snapshot without placing cognition in the UI or transport layer.

Implemented regression path:

```text
HTTP request
 ↓
interfaces.py
 ↓
SynrheonRuntime
 ↓
OrganismState
 ↓
snapshot
 ↓
HTTP response
```

Automated preview result: 4 focused tests passed, including the HTTP boundary test, distinct external/internal stimulus channels, one-step cycle behavior, and safe pre-start/empty-input failure.

Status: Integrated code path; human live-browser verification pending before Stage 0B is called Verified.

## E001 — Cognitive Substrate

Can Synrheon represent a tiny world of concepts and relationships and transform activation/state without stimulus-specific logic?

Status: Not Run

## E002 — Sequence Reconstruction

Can Synrheon identify what occurred immediately before or after another event?

Status: Future

## E003 — Temporal Retrieval

Can Synrheon restrict retrieval to a time region such as earlier today without searching all lifetime memories?

Status: Future

## E004 — Sparse Activation

Can a relevant cue activate a useful small region while unrelated concepts remain inactive?

Status: Future

## E005 — Three-Level Retrieval

Can Level 1 orientation narrow Level 2 candidates before Level 3 detailed retrieval?

Status: Future

## E006 — Problem / Trial Learning

After a failed trial, can Synrheon preserve why it failed and preferentially change the most likely causal variable?

Status: Future

## E007 — Route Learning

Can successful retrieval or reasoning trajectories become easier to select later without hardcoded stimulus rules?

Status: Future

## E008 — Recursive Thought

Can Synrheon solve a problem requiring several internal state transitions before producing an external response?

Status: Future

## E009 — Consolidation

Can repeated experiences produce a useful compressed representation while preserving evidence lineage?

Status: Future

## E010 — Autonomous Continuation

Can unresolved internal state produce useful S(t+1) without new external input while avoiding fixation?

Status: Future
