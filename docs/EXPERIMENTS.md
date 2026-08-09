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

The initial Stage 1 substrate established separate world knowledge, organism-relative knowledge, learned organism-relative state, and activation representation.

Its first fixed 11-field self vector was later superseded by E001A.

Status: **Superseded representation; provenance separation retained.**

## E001A — Open-Ended Organism Relation Space

Hypothesis: Synrheon can preserve injected-versus-self-learned provenance without hard-coding a closed list of organism-relative dimensions.

Candidate result:
- arbitrary relation names were accepted as data
- injected and learned versions remained separate
- learned evidence lineage remained explicit
- world knowledge and current activation remained separate
- Stage 0B controls and ordered experience behavior remained intact

Status: **Built / integrated representation; human live verification still required for that bounded UI behavior.**

## E002 — Ordered Experience Thread

Hypothesis: every meaningful external or explicitly injected internal event can receive an episode coordinate and explicit before/after links without pretending current-episode experience is durable memory.

Expected result:
- Chat event is `origin = observed`
- Internal Thought injection is `origin = injected`
- sequence is monotonic
- previous/next links agree
- stimulus records link to experience event IDs
- new session starts a new episode
- no durable cross-process memory claim

Candidate automated result: current tests produced consistent observed/injected provenance, sequence, links, and stimulus-to-experience IDs.

Status: **Integrated; not durable memory.**

## E003 — Temporal Retrieval

Can Synrheon restrict retrieval to a time region such as earlier today without searching all lifetime memories?

Status: Future

## E004 — Hand-Written Sparse Chat Activation

Hypothesis tested: can Chat reach a state-changing cognition owner using generic lexical matching plus relation spreading, salience, inhibition, and Top-K selection without domain-specific phrase branches?

Historical candidate result:
- the live architecture was successfully wired from Chat/Internal Thought through runtime into `cognition.py`
- unrelated concept networks used the same algorithm
- fixed Top-K bounded the active region
- unknown cues failed safely
- world/organism knowledge was not rewritten

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

## E011 — Train the Cognitive Process, Test Transfer

### Hypothesis

A small trainable cognitive policy can learn **which cognitive operation to perform next** from abstract cognitive state and transfer that process to an unseen knowledge world whose concepts, relation labels, and answers were never used during training.

### Core Training Unit

```text
state before
candidate cognitive actions
selected action
short transition / path
checkpoint
state after
prediction
outcome
error
credit
```

A path is not rewarded merely because it was selected. Credit must depend on outcome, correction, prediction error, or another explicit usefulness signal.

### Training Worlds

Use at least three tiny unrelated worlds, for example:

```text
World A — arbitrary objects / relations
World B — different arbitrary objects / relations
World C — different arbitrary objects / relations
```

Names and relation labels should be randomized or permuted where practical so the policy cannot rely on semantic familiarity.

### Held-Out World

World D must contain:
- concept identities never used in training
- relation labels or encodings not tied to memorized answers
- the same abstract problem structure required for successful cognitive operations

### Baselines

At minimum compare against:
- random/untrained policy
- simple fixed heuristic where appropriate

### Pass Criteria

The experiment passes only if:

1. model parameters actually change through training;
2. decision quality or loss improves on training tasks;
3. held-out world performance exceeds the untrained/random baseline;
4. renaming concepts does not destroy the learned strategy;
5. success cannot be explained by memorized answer text or world-specific branches;
6. the learned policy can be invoked through the real Synrheon runtime boundary without moving cognition into the UI/runtime;
7. state/action/outcome/credit traces remain inspectable.

### Failure Criteria

The experiment fails if:
- performance collapses on unseen names despite identical abstract structure;
- the implementation embeds task answers or special-case routes;
- selected paths are reinforced without outcome evidence;
- runtime becomes the cognition owner;
- the model only reproduces training outputs rather than choosing useful cognitive operations.

### Current Status

**Pre-registered; implementation not started.**
