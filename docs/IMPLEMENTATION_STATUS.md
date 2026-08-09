# Synrheon Implementation Status

This file records what actually exists and what level of evidence supports it.

## Status meanings

- **Historical synthetic evidence** — observed in a controlled self-authored world; useful but not external validation.
- **External test pending** — a stronger confirmatory assay is frozen but its final external result is not yet observed.
- **Built** — implementation exists in isolation.
- **Integrated** — live runtime reaches it.
- **Verified** — intended behavior was observed through the running organism.

## Ground 0

```text
large candidate / knowledge field
    ↓
learned routing
    ↓
reversible contextual tapering
    ↓
serious-candidate field
    ↓
state-dependent recurrence
    ↓
evidence / uncertainty
    ↓
commit | abstain | seek evidence | reopen
```

A post-HCT code review found design vulnerabilities that weaken the strongest HCT-2 causal interpretations. HCT-1/HCT-2 remain part of the scientific history, but the recurrence, ordering, and efficiency claims are now **provisional pending EXT-1**.

| Component | Current evidence status |
|---|---|
| Reversible soft narrowing | Strong synthetic support; external C2 pending |
| Context-driven reopening | Strong synthetic support; external C2 pending |
| Learned context ordering | HCT-2 historical efficiency result; clean external C1 pending |
| State-dependent recurrence | Large HCT-2 ablation effect, but answer-bearing graph weakens causal interpretation; EXT-1 ablation pending |
| Commitment separate from winner | Synthetic support; external C3 pending |
| Opaque-identity transfer | Supported in earlier synthetic controls |
| Learned pathway resistance | Promising earlier; not necessary in HCT-2; optional |

Historical HCT-2 measurements remain recorded in the theory paper, but the old `7.14%`, `5.49%`, `3.125%`, and `100% → 45%` figures must not be described as externally settled mechanisms.

## EXT-1 status

```text
Branch: experiment/external-retrieval-cascade
Status: preregistered / implementation built / final external split NOT YET RUN
Primary dataset: BEIR SciFact
Secondary preregistered dataset: BEIR NFCorpus
```

EXT-1 closes the main HCT review vulnerabilities by construction:

```text
external qrels; no planted answer index
answer-independent document relation graph
document-id tie breaking
symmetric per-condition feature caching
measured feature evaluations + timing
order learned from utility / measured cost
published BM25 sanity anchor
paired confidence intervals
synthetic runs forced to NOT EVIDENCE
partial final runs forbidden
```

C1, C2, and C3 are reported independently. Fewer than 30 paired reopening cases makes C2 inconclusive without hiding a failure in C1 or C3.

See `docs/EXT1_PREREGISTRATION.md`.

## Live organism

| Capability | Status | Current truth |
|---|---|---|
| Observable runtime + development UI | Verified | Browser/API/runtime/state path works live |
| Cognitive substrate | Built | Concepts, relations, activation representation |
| Computational time | Integrated | Episode, sequence, timestamp, elapsed time |
| Ordered experience + provenance | Integrated | Observed/injected experience thread exists in-process |
| E011-A trainable operation/target policy | Built experimentally | Historical controlled transfer result |
| Ground 0 checkpoint contract | Built | `Ground0Checkpoint` defines phase/disposition boundaries |
| Ground 0 tapering | Research only | Not live-integrated |
| Ground 0 recurrence | Research only | Not live-integrated |
| Ground 0 commit/abstain/reopen behavior | Research only | Contract exists; behavior not live-integrated |
| Durable memory | Not started | Current experience is process-local |
| Learned retrieval | Not started | Future architecture only |
| Recursive autonomous cognition | Not started | Future architecture only |

## Current production source ownership

```text
state.py             explicit organism/substrate state
cognition.py         Ground 0 checkpoint/cognitive-cycle contract
policy.py            retained E011-A operation/target policy
policy_learning.py   retained E011-A policy learning
learning.py          temporary E011 compatibility export
experience.py        ordered current-episode experience
temporal.py          time / sequence / episode coordinates
runtime.py           thin sequencing
dev_server.py        local HTTP/UI transport
```

Placeholder-only future modules were removed. Planned capabilities do not receive source files until implementation exists.

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

Ground 0 cognition is not yet in this live path.

## Next scientific boundary

The immediate research gate is **EXT-1**, not another synthetic HCT expansion.

Before any production Ground 0 integration is treated as justified, we need to learn which of these survive external data:

```text
C1: ordered reversible tapering earns measured feature cost
C2: reversibility recovers externally relevant candidates after suppression
C3: abstention improves external calibration
plus: recurrence adds value when the relation graph is answer-independent
```

A negative EXT-1 result should simplify Ground 0 rather than trigger threshold tuning.

## Scientific boundary

Neither the HCT series nor EXT-1 currently establishes natural-language understanding, learned semantics, biological equivalence, general intelligence, modern-retrieval superiority, end-to-end wall-clock superiority, autonomous cognition, or production integration.
