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
- injected self `social = 0.8` remains injected organism-relative state
- self-learned state starts independently
- a trusted learning update changes only self-learned state
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

Interpretation: the provenance boundary is useful, but the initial fixed 11-field `SelfRelationVector` over-constrained what Synrheon could ever learn about how something relates to herself. E001A corrects that representation before sparse activation is built.

Status: **Superseded representation; provenance separation retained.**

## E001A — Open-Ended Organism Relation Space

Hypothesis: Synrheon can preserve injected-versus-self-learned provenance without hard-coding a closed list of organism-relative dimensions.

Baseline live/code behavior:
- `SelfRelationVector` contains exactly 11 Python fields
- the UI presents those same 11 values in a dropdown
- a new relation such as `protective_of`, `expects_help_from`, or `reminds_me_of` cannot exist without changing production code

Pre-registered live action:

```text
Start Synrheon
Add concept: daisy / Daisy
Inject self relation type: protective_of
Strength: 0.70
Confidence: 0.90
```

Expected post-change behavior:
- `protective_of` is accepted even though no Python constant or field names it
- the relation type is stored as data, not as a production-code dimension
- injected relation state remains explicitly injected
- self-learned relation state remains separately stored and cannot be directly injected
- a learning update for an arbitrary relation type changes only the learned representation for that type
- learning preserves evidence-event IDs
- world knowledge and current activation are unchanged
- blank relation types, unknown concepts, and out-of-range strengths/confidence fail safely
- no special case for `protective_of` exists in production code

State/trace to inspect:
- `cognitive_substrate.self_relations`
- injected and learned entries for the same concept/relation type
- `self_relation_injected` trace event

Must remain unchanged:
- Stage 0B controls and browser/backend path
- ordered experience thread
- world relation representation
- activation representation
- runtime remains a router rather than cognition owner

Candidate automated result:
- 8/8 focused/full preview tests passed after replacing the fixed vector
- Python compilation passed
- `protective_of`, `expects_help_from`, and `reminds_me_of_home` were accepted without any production-code declaration for those names
- HTTP integration accepted `protective_of` through the real API/runtime/substrate path
- injected `protective_of` remained unchanged while a learned `protective_of` updated independently
- learned evidence lineage remained attached to the learned relation
- blank relation type and out-of-range strength failed safely
- Stage 0B controls and ordered experience tests remained passing

Interpretation: the fixed cognitive ontology has been removed while the provenance boundary remains intact. This is a **Built** representation and an **Integrated** injection path, but not yet a cognitive sparse-activation mechanism.

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

## E004 — Sparse Chat Activation

Hypothesis: a Chat stimulus can enter the live cognition owner, seed known concepts through one generic lexical cue rule, spread activation through whatever world relations exist, weight already-reached concepts by arbitrary organism relations, inhibit weak competitors, and retain only a bounded Top-K active region without stimulus-specific branches.

Baseline before implementation:
- Chat becomes ordered observed experience
- `ActivationState` remains empty unless a developer mutates it directly
- `cognition.py` is a placeholder
- Chat shows no cognitive consequence

Pre-registered live setup:

```text
Concepts:
daisy / Daisy
dog / dog
animal / animal
violin / violin
music / music
volcano / volcano

World relations:
daisy IS_A dog
dog IS_A animal
violin PRODUCES music

Arbitrary injected organism relation:
dog personally_relevant_to_self 0.80 confidence 0.90
```

Live stimulus A:

```text
Daisy
```

Expected A:
- lexical cueing matches `daisy` generically by concept ID/label, not a Daisy-specific rule
- `daisy` is strongly active
- activation spreads `daisy → dog → animal`
- the arbitrary organism relation on `dog` can increase dog salience without cognition.py naming `personally_relevant_to_self`
- `violin`, `music`, and `volcano` do not survive the sparse winner set
- Chat and Internal Thought visibly expose the active winners and contributing paths

Live stimulus B:

```text
violin
```

Expected B:
- the exact same mechanism activates `violin → music`
- Daisy-network nodes do not survive merely because the first experiment used them
- no production branch contains `Daisy`, `violin`, or the organism-relation example names

Live stimulus C:

```text
quasar
```

Expected C:
- if no injected concept matches, Synrheon reports that no known concept cue matched
- current activation is cleared rather than falsely claiming understanding
- the observed experience is still retained in the ordered experience thread

Algorithm boundary:
- concept matching is a temporary generic lexical bootstrap, not semantic language understanding
- world-relation direction is respected
- outgoing spread is normalized so high-degree nodes do not gain unlimited activation merely from having many edges
- organism relation types are treated generically as salience evidence; no fixed ontology is reintroduced
- competition uses a floor + winner-relative threshold and bounded Top-K selection
- runtime only routes the observed event into `cognition.py`; cognition owns the state transformation

Must remain unchanged:
- injected / learned provenance separation
- world knowledge is not rewritten by activation
- organism relations are not rewritten by activation
- experience sequencing and before/after links
- UI remains observation/control only
- unknown concepts and malformed knowledge fail safely

Failure means the live Chat path still does not reach cognition, activation requires phrase-specific code, arbitrary organism relation types are enumerated, unrelated nodes remain broadly active, or cognition mutates stored knowledge while thinking.

Status: **Pre-registered; implementation pending.**

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
