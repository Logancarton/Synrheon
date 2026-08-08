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

Implemented path:

```text
Browser action
 ↓
HTTP request
 ↓
interfaces.py
 ↓
SynrheonRuntime
 ↓
OrganismState
 ↓
snapshot + trace
 ↓
HTTP response
 ↓
Browser
```

Automated regression evidence: 4 focused tests passed, including the HTTP boundary test, distinct external/internal stimulus channels, one-step cycle behavior, and safe pre-start/empty-input failure.

Live action set:

```text
Start
Chat stimulus
Internal Thought injection
Think One Step
Continue
Pause
inspect Current State
inspect Trace
```

Observed result: the user ran the supported local Synrheon application and confirmed the UI workflow worked. The real frontend/backend/runtime path was therefore observed through the running organism rather than inferred from tests alone.

Interpretation: Stage 0B successfully provides the observable development organism required for later cognitive experiments. This verifies infrastructure only; it does not demonstrate semantic understanding or cognition.

Status: **Verified**

## E001 — World / Self / Activation Separation

Hypothesis: Synrheon can represent generic world knowledge, organism-relative knowledge, and current activation as separate state so later sparse activation can use self relevance without rewriting world truth.

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

Baseline: before this change `core.py` has only Stage 0B session/stimulus/trace state. There is no concept substrate, world/self distinction, explicit self vector, or activation state.

Expected result:
- `Daisy IS_A dog` remains world knowledge with `origin = injected`
- `Daisy.social` remains a separate self relation with `origin = injected`
- activation is stored separately from both
- later self-learning may update a self vector from evidence without mutating the injected world relation
- malformed references fail without mutating unrelated state

Failure means world/self provenance is merged, activation overwrites stored knowledge, or self-learning rewrites generic world truth.

Candidate verification: 7/7 focused/full current tests passed in the isolated preview and Python compilation passed.

Automated candidate result: the substrate separation and self-learning tests passed. The HTTP integration test also reached concept/world/self injection through the real runtime/API and confirmed malformed unknown-concept relations fail with HTTP 400.

Interpretation: the representation boundary is Built, and explicit concept/world/self injection is Integrated through the live backend/UI path. The confidence-weighted self-learning method is Built but not yet invoked by live outcome feedback.

Status: **Built / Integrated candidate; human live UI inspection pending before any Stage 1 capability is called Verified.**

## E002 — Ordered Experience Thread

Hypothesis: every meaningful external or explicitly injected internal event can receive an episode coordinate and explicit before/after links without pretending that current-episode experience is durable memory.

Pre-registered live stimulus:

```text
Start
Chat: "Daisy came to the door"
Internal Thought injection: "Consider whether Daisy expects a walk"
```

Baseline: Stage 0B records stimuli and trace events, but there is no separate autobiographical event thread, episode sequence, elapsed time, or previous/next event linkage.

Expected result:
- Chat event is recorded as `origin = observed`
- Internal Thought injection is recorded as `origin = injected`
- experience sequence is exactly `1 → 2`
- event 1 points forward to event 2
- event 2 points back to event 1
- both stimulus records link to their experience event IDs
- the Internal Thought/UI state exposes the thread
- restarting a session begins a new episode thread
- no claim of durable cross-process memory is made

Failure means provenance collapses, ordering is ambiguous, links disagree, or the thread is created only in JavaScript/tests.

Automated candidate result: the ordered-experience test produced `observed → injected` provenance, exact sequence `1 → 2`, consistent forward/back links, stimulus-to-experience IDs, and an experience sequence of 2. The HTTP integration test reached the same path through the real backend, and the UI candidate renders the thread in Internal Thought.

Interpretation: the current-process experience thread is Integrated candidate behavior. It supplies sequencing and an autobiographical thread without falsely claiming durable memory.

Status: **Integrated candidate; human live UI inspection pending before this bounded behavior is called Verified.**

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
