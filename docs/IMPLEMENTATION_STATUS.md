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

## Immediate scientific boundary — MT-1 preregistration

MT-1 is now unblocked for specification, not for ad-hoc tuning.

Central question:

> After controlling transition-state persistence, does more than one soft contextual settling stage materially outperform one good soft stage under matched computation?

Conceptual controls to freeze precisely before result-bearing implementation:

```text
retrieval/no-taper anchor
single full-context soft
multi-soft with naive carry
multi-soft with controlled reset
scrambled/reversed context order
matched-compute hard staged pruning
```

Keep recurrence and Token Deck improvements outside the primary comparison unless explicitly preregistered before results.

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

Owner:

```text
src/synrheon/token_deck.py
```

Integrated storage owner:

```text
CognitiveSubstrate.token_deck in src/synrheon/state.py
```

Current status:

```text
TD-0 stable token identity                 Built
TD-1 multiple reversible senses            Built
TD-2 alias/morphology storage              Built, non-inferential
TD-3 exact surface segmentation            Not Started — next build
TD-4 known/unknown acquisition              Not Started
TD-5 contextual sense disambiguation       Not Started
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

The live chat path does not yet automatically segment input into Token Deck observations.

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
| Token Deck TD-0/1/2 | Built | Stored in substrate; not yet auto-fed by language |
| TD-3 segmentation | Not Started | Immediate representation build target |
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
temporal.py + experience.py
        ↓
state.py / trace
        ↓
UI
```

Token Deck storage exists inside state, but raw chat is not yet automatically segmented into token observations. Ground 0 contextual search is not yet in the live path.

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
