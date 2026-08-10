# Synrheon Implementation Status — Revision 6

This file records what actually exists and what level of evidence supports it.

## Status meanings

Scientific evidence:

- **Historical synthetic evidence** — controlled self-authored worlds; useful but not external validation.
- **External development evidence** — public benchmark/development data; stronger than synthetic evidence but not final confirmation.
- **Confirmatory held-out evidence** — untouched evaluation used according to a preregistered boundary.

Implementation maturity:

- **Not Started** — no meaningful implementation.
- **Designed** — contract exists; mechanism does not yet operate.
- **Built** — mechanism exists and passes relevant isolated/controlled tests.
- **Integrated** — the live runtime reaches and uses it.
- **Verified** — intended live behavior was observed through the running organism with relevant state/trace inspected.

## Authoritative continuation

```text
Current scientific branch:
experiment/external-retrieval-cascade

Historical synthetic branch:
experiment/hippocampal-sparse-settling
```

Current authority begins with:

```text
docs/REV6_CONTINUATION_STATE.md
docs/CURRENT_STAGE.md
```

Older Revision 4/5 theory and HCT/E011 records remain historical evidence and frozen experiment history.

## Revision 6 evidence ledger

### Supported / strengthened

- Reversible suppression has strong synthetic support.
- One full-context soft taper approximately preserves the SciFact BM25 development anchor.
- BM25 top-100 retains meaningful oracle reranking headroom.
- D6 supports inappropriate carried activation as a major contributor to the partial-to-full failure on SciFact development.
- Explicit context-transition provenance, reset/re-anchor, restore, and reopen are justified as reusable architecture.
- E011-A remains controlled evidence that operation/target preferences can transfer across unseen and renamed synthetic worlds.

### Discounted / falsified in the current implementation

- EXT-1 C1/C2/C3 were not validated as originally hoped.
- Current four hand-designed lexical channels are not established as useful residual discriminators.
- Current static recurrence harmed SciFact development ranking.
- Current commitment calibration is not established.
- HCT-2 does not establish external recurrence necessity because identified synthetic confounds weaken that interpretation.
- Hard pruning losing is not sufficient evidence for multiple-soft-stage necessity.

### Open / untested

- Whether controlled multi-soft stages outperform a single soft stage under matched compute.
- Question-guided contextual divergence with richer context.
- Trajectory-relative recurrence.
- External recovery value of reopening on a suitable changing-context task.
- Calibrated commitment beyond strong baselines.
- Token/sense/event state as a useful retrieval/context signal.

## D6 — completed external-development diagnostic

Frozen source:

```text
docs/D6_PREREGISTRATION.md
experiments/d6_transition_persistence.py
tests/test_d6_transition_persistence.py
```

Observed SciFact development result:

```text
development queries:                 93
transition-evaluable queries:        92
reset control integrity:             PASS
max reset activation difference:     2.220446049250313e-16
R_reset:                             1.0
frozen verdict:                      MAJOR_PERSISTENCE_CONTRIBUTION_SUPPORTED
reserved final split:                untouched by D6
```

Interpretation:

> The carried settled state is a major contributor to the observed partial-to-full degradation under the frozen D6 implementation.

The result does not establish that multiple stages are useful. D6-E residual refinement remains diagnostic/mixed and had no preregistered success threshold.

## Immediate scientific boundary — MT-1 implementation

Frozen source:

```text
docs/MT1_PREREGISTRATION.md
```

Status: **v1 UNEXECUTED / DESIGN-INVALID; MT-1.1 replacement awaiting approval**

A pre-result implementation audit found that the v1 treatment condition cannot satisfy the
experiment's own matched-compute admissibility rule (`E(M3) ~= 2.285 * E(M1)` against a
1.10 tolerance), making `MULTI_STAGE_SUPPORTED` structurally unreachable. The v1
preregistration is retained unedited as frozen historical design evidence.

```text
docs/MT1_DESIGN_AUDIT.md      what was found and what was deliberately not done
docs/MT11_PREREGISTRATION.md  equal-budget replacement, draft, awaiting approval
```

No SciFact development nDCG was computed or inspected. The development split is untouched.

Central question:

> After controlling transition-state persistence, does more than one soft contextual settling stage materially outperform one good soft stage under matched computation?

Frozen conditions:

```text
M0 retrieval anchor
M1 single full-context soft                  primary baseline
M2 multi-soft with naive carry               pathology control
M3 multi-soft, reset + retained narrowing    primary treatment
M4 multi-soft with full reset                wasted-stage sanity control
M5 reversed stage order                      order control
M6 matched-compute hard staged pruning       reversibility control
```

Frozen compute rule: one candidate x channel feature evaluation is the unit; every
condition receives eight nominal channel-cycle sweeps; `E(M3) <= 1.10 * E(M1)` gates any
supportive reading. Frozen material effect: `M3 - M1 >= 0.010` nDCG@10 with a positive
95% paired bootstrap lower bound over at least 30 transition-evaluable queries.

Recurrence and Token Deck output are excluded from every condition. Thresholds may now
move only through an explicit versioned amendment recorded before further results.

## Production-facing contextual search

Owner:

```text
src/synrheon/contextual_search.py
```

Status: **Built, not Integrated**

Current invariant/mechanics:

```text
complete broad-field prior
complete activation state
active vs dormant compute region
soft suppression without deletion
carry / reset / residual transition provenance
checkpoints
restore
reactivate
reopen-all
```

D6 used this same transition-state contract. The live runtime still lacks a legitimate broad candidate source, so contextual search must not be wired with fabricated candidates merely to claim integration.

## Token Deck

Owners:

```text
src/synrheon/token_deck.py            token/sense identity and reversible sense state
src/synrheon/surface_segmentation.py  TD-3 exact surface observation
```

Integrated storage owners:

```text
CognitiveSubstrate.token_deck in src/synrheon/state.py    identity
StimulusRecord.segmentation in src/synrheon/state.py      per-stimulus observation
```

Current status:

```text
TD-0 stable token identity                 Built
TD-1 multiple reversible senses            Built
TD-2 alias/morphology storage              Built, non-inferential
TD-3 exact surface segmentation            Built + Integrated, not Verified
TD-4 known/unknown acquisition              Built + Integrated, not Verified
TD-5 contextual sense disambiguation       Not Started — preregistration next
TD-6 concept/entity bridge                  Contract begun; behavior pending
TD-7 event/role composition                 Not Started
TD-8 durable Token Deck                     Not Started
TD-9 candidate-source bridge                Not Started
TD-10 learned vocabulary growth             Not Started
```

Current Token Deck cognitive-physics invariants:

```text
surface form != token identity != sense != concept/entity != episode
multiple senses remain recoverable
context-conditioned sense activation is reversible
newly discovered senses reopen the inventory rather than inheriting permanent zero support
provenance remains inspectable
```

TD-3 invariants, enforced at construction rather than only tested:

```text
every character of the input belongs to exactly one span
spans rejoin into the exact original string
offsets always index the original text, never a normalized form
the segmenter assigns no token, sense, or concept identity
```

Frozen segmenter version: `td3-exact-surface-v1`.

The live chat path now segments each stimulus and records the observation on the stimulus,
but it still creates **no** token cards. The cognitive substrate is unchanged by chat, and
a regression test asserts that. Turning an observed span into an identity is TD-4's
decision.

Stimulus inspection paths:

```text
python3 -m synrheon segment "<text>"       JSON observation; no session, no state change
python3 -m synrheon route "<text>"          TD-4 routing against a fresh empty deck
POST /api/segment {"text": ...}             inspection only; records nothing
POST /api/acquisition {"text": ...}         TD-4 routing against the live deck
POST /api/acquire {"text": ..., "needs": [...]}   explicit acquisition; the only mutation
state.stimuli[].segmentation                observation attached to each live stimulus
state.stimuli[].acquisition                 routing attached to each live stimulus
trace events "surface_segmented" / "acquisition_routed" / "tokens_acquired"
```

## Live organism status

| Capability | Maturity | Current truth |
|---|---|---|
| Observable runtime + development UI | Verified | Browser/API/runtime/state path works live |
| Computational time | Integrated | Episode/sequence/time coordinates are live |
| Ordered experience + provenance | Integrated | Observed/injected current-episode thread is live |
| Cognitive substrate | Built | Concepts, relations, activation, TokenDeck representation |
| E011-A operation/target policy | Built experimentally | Historical controlled transfer donor mechanism |
| Ground 0 checkpoint contract | Built | Public phase/disposition contract exists |
| Reversible candidate field | Built | Not live-integrated; no legitimate broad source yet |
| Token Deck TD-0/1/2 | Built | Stored in substrate; identity still not auto-created |
| TD-3 segmentation | Built + Integrated | Live stimuli observed exactly; awaiting human stimulus verification |
| TD-4 acquisition routing | Built + Integrated | Read-only known/unknown routing; acquisition stays explicit |
| TD-5 sense disambiguation | Not Started | First serious language-learning experiment; preregister first |
| Learned context selection | Not Started | Must be earned/tested |
| Production multi-taper controller | Not Started | Blocked on MT-1 evidence |
| Production recurrence | Not Started | Must earn task-specific role |
| Commitment calibration | Not Started | Current external signal discounted |
| Durable memory | Not Started | Current experience remains process-local |
| Learned retrieval | Not Started | Candidate-source dependency remains open |
| Recursive autonomous cognition | Not Started | Future only |

## Current production source ownership

```text
state.py               explicit organism/substrate state; contains TokenDeck
cognition.py           Ground 0 public cognitive contracts
contextual_search.py   reversible candidate field / context-transition checkpoints
token_deck.py          stable token/sense identity + reversible sense state
surface_segmentation.py  TD-3 exact surface observation; assigns no identity
acquisition_routing.py   TD-4 known/unknown routing; read-only, acquires only when called
policy.py              retained E011-A operation/target donor policy
policy_learning.py     retained E011-A learning
learning.py            temporary E011 compatibility export
experience.py          ordered current-episode experience + provenance
temporal.py            computational time / sequence
runtime.py             thin sequencing
dev_server.py          local HTTP/UI transport
experiments/           scientific harnesses, qrels, hidden evaluation/scoring
ui/                    observation and control only
```

## Current live flow

```text
Chat / injected developer thought
        ↓
dev_server.py
        ↓
runtime.py
        ↓
temporal.py + experience.py + surface_segmentation.py
        ↓
state.py / trace
        ↓
UI
```

Raw chat is now segmented into exact surface observations, but no identity is created from
it. Ground 0 contextual search is still not in the live path, and no legitimate broad
candidate source exists yet.

## Development rule

Synrheon now advances through two independent loops:

```text
SCIENTIFIC
preregister -> implement -> integrity/smoke -> allowed evidence run -> frozen classification -> update theory

ARCHITECTURE
build one invariant -> stimulus test -> inspect state -> fix process -> regression test -> integrate only with legitimate inputs
```

Negative evidence should simplify Ground 0 rather than trigger threshold tuning. Token Deck improvements must not alter MT-1 after its boundary is frozen unless a new versioned experiment explicitly combines them.

## Scientific boundary

Current work does not establish biological hippocampal equivalence, a new law of cognition, natural-language understanding, general intelligence, superiority to modern dense/late-interaction retrieval, end-to-end wall-clock superiority, autonomous cognition, or production-ready intelligence.
