# Cognitive Experiments

## Evidence Standard

The preferred experiment is a real stimulus applied through the running Synrheon organism.

Record stimulus/action, baseline, expected behavior, observed UI/runtime output, relevant internal state/trace, and interpretation.

Automated tests protect discovered behavior but are not enough to call cognition `Verified`.

## E000 — Stage 0B Connected Organism Transport

Hypothesis: browser-facing actions can cross into the real Python runtime, mutate Synrheon-owned state, and return observable state/trace without placing cognition in the UI/transport layer.

Observed result: the user ran the supported application and confirmed Start, Chat, Internal Thought, Step, Continue, Pause, Current State, and Trace through the real frontend/backend/runtime path.

Status: **Verified**

## E001 — World / Injected-Self / Learned-Self / Activation Separation

Hypothesis: Synrheon can keep generic world knowledge, explicitly injected organism-relative knowledge, self-learned organism-relative knowledge, and current activation separate so later sparse activation can combine them without losing provenance.

Pre-registered setup:

```text
Concepts:
Daisy
dog

Injected world relation:
Daisy IS_A dog

Injected self relation:
Daisy.social = 0.8

Current activation:
Daisy = 1.0
```

Baseline: Stage 0B had no concept substrate, world/self distinction, explicit self-learning representation, or activation state.

Expected result:
- `Daisy IS_A dog` remains injected world knowledge
- injected self `social = 0.8` remains in `injected_vector`
- `learned_vector` starts independently
- a trusted learning update changes only `learned_vector`
- learning preserves evidence-event IDs and learned confidence
- injected self state and world relation remain unchanged
- activation remains separate from all stored knowledge
- malformed references fail without unrelated mutation

Candidate automated result:
- 7/7 current focused/full tests passed in the isolated preview
- Python compilation passed
- HTTP integration reached concept/world/injected-self injection through the real runtime/API
- unknown-concept relation failed safely with HTTP 400
- learned-vector test changed learned `experience/social/prediction` while injected `social` and world knowledge remained unchanged

Interpretation: the representation boundary is **Built**; explicit concept/world/injected-self injection is **Integrated**; self-learning mathematics is **Built** but not invoked from live outcome feedback.

Status: **Not Verified until human live UI/state inspection.**

## E002 — Ordered Experience Thread

Hypothesis: every meaningful external or explicitly injected internal event can receive an episode coordinate and explicit before/after links without pretending current-episode experience is durable memory.

Pre-registered live stimulus:

```text
Start
Chat: "Daisy came to the door"
Internal Thought injection: "Consider whether Daisy expects a walk"
```

Expected result:
- Chat event is `origin = observed`
- Internal Thought injection is `origin = injected`
- experience sequence is exactly `1 → 2`
- event 1 points forward to event 2
- event 2 points back to event 1
- both stimulus records link to their experience event IDs
- Internal Thought/state exposes the thread
- restarting a session begins a new episode thread
- no durable cross-process memory claim

Candidate automated result: tests produced `observed → injected`, exact sequence `1 → 2`, consistent forward/back links, stimulus-to-experience IDs, and experience sequence 2. HTTP integration reached the same owners through the real backend.

Interpretation: this is an **Integrated** current-process autobiographical thread, not durable memory.

Status: **Not Verified until human live UI/state inspection.**

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
