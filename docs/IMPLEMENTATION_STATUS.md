# Synrheon Implementation Status

This file records what actually exists and what level of evidence supports it.

## Status meanings

- **Historical synthetic evidence** — observed in a controlled self-authored world; useful but not external validation.
- **External development evidence** — observed on public data/development split; stronger than synthetic evidence but not a final held-out claim.
- **Built** — implementation exists in isolation.
- **Integrated** — live runtime reaches it.
- **Verified** — intended behavior was observed through the running organism.

## Authoritative research branch

```text
Historical synthetic branch:
experiment/hippocampal-sparse-settling

Current external-validation branch:
experiment/external-retrieval-cascade
```

Scientific continuation must proceed from `experiment/external-retrieval-cascade`. The historical hippocampal branch should remain preserved as the synthetic research record.

At Revision 5, the external branch is a strict descendant of the historical branch and contains the current retrieval-cascade and EXT-2 diagnostic implementation.

See:

```text
docs/REV5_CONTINUATION_STATE.md
```

for the current continuation protocol. Where the older Revision 4 theory document still says EXT-1 is the immediate next gate, the Revision 5 continuation note supersedes that boundary.

## Ground 0

```text
large candidate / knowledge field
    ↓
learned routing / context selection
    ↓
reversible contextual tapering
    ↓
serious-candidate field
    ↓
optional recurrence if it earns value
    ↓
evidence / uncertainty
    ↓
commit | abstain | seek evidence | reopen
```

The architecture is being simplified whenever stronger external evidence fails to support a mechanism.

| Component | Current evidence status |
|---|---|
| Reversible soft narrowing | Strong synthetic support; external value remains open |
| Context-driven reopening | Strong synthetic support; external value remains open |
| Multiple ordered context stages | Not established; MT-1 blocked until D6 |
| State-dependent recurrence | Synthetic support in selected families; current static recurrence discounted on SciFact development |
| Commitment separate from winner | Conceptually retained; current external calibration discounted |
| Opaque-identity transfer | Supported in earlier synthetic controls |
| Learned pathway resistance | Promising earlier; optional / task-dependent |

Historical HCT measurements remain part of the research record, but the old ordering, recurrence, and efficiency figures must not be described as externally settled mechanisms.

## External-validation status

Current source includes:

```text
experiments/external_retrieval_cascade.py
experiments/ext2_diagnostics.py
tests/test_external_retrieval_cascade.py
tests/test_ext2_diagnostics.py
```

The current external evidence ledger is:

### Supported

- Reversible suppression has strong synthetic evidence.
- A single full-context soft taper approximately preserves the BM25 SciFact development anchor.
- Meaningful oracle headroom remains on development data.

### Falsified / discounted in the current implementation

- EXT-1 C1/C2/C3 are not validated as originally hoped in the current implementation.
- Current static recurrence is not beneficial on SciFact development; removing recurrence improved development nDCG from approximately `0.5081` to `0.5415`.
- The current four hand-designed channels are not established as useful residual discriminators.
- Current commitment calibration is not established.

### Partially supported / open

- External value of reopening.
- Contextual state persistence as a possible cause of the partial-context -> full-context collapse.

### Untested

- Question-guided contextual divergence.
- Trajectory-based recurrence.
- Residual-guided tapering.
- Matched-compute multiple-soft-taper necessity.

## Immediate scientific boundary — D6 only

The immediate research gate is **D6: Transition Persistence Diagnostic**.

Do not proceed directly to a large multi-taper experiment because the current sequential partial -> full process may already contain a transition-state persistence pathology.

Freeze:

```text
same 93 SciFact development queries
same BM25 candidate field
same current channels
same learned parameters
no final split
no recurrence
no new semantic channels
no threshold tuning
```

Conditions:

```text
A — BM25 / full-query anchor
B — one full-context soft taper
C — partial -> full with carried activation, no recurrence
D — partial -> full, reset before full-context stage
E — partial -> full, stage two acts only on unresolved residual
```

Diagnostic quantities:

```text
Delta_damage = B - C
R_reset = (D - C) / (B - C)
```

Frozen interpretation:

- `D > C` with paired 95% CI excluding zero and `R_reset >= 0.50` -> inappropriate persistence supported as a major contributor.
- `R_reset < 0.25` -> persistence is not a sufficient explanation.
- `0.25 <= R_reset < 0.50` -> partial support.

## Next major experiment — MT-1, blocked on D6

After D6, specify **MT-1: Matched-Compute Multi-Taper Falsification**.

Primary comparison:

```text
single full-context soft taper
vs
multiple context-settled soft tapers
vs
matched-compute hard staged pruning
```

Also include multi-stage reset, scrambled-order, and clock-driven Top-K as a negative control.

Critical interpretation rule:

> Hard pruning losing is not sufficient evidence for multiple contextual settling stages.

Multi-taper necessity is supported only if multi-soft materially outperforms single-soft under matched computation.

If multi-soft ~= single-soft while hard pruning loses reactivation, conclude:

```text
reversibility supported
multiple contextual settling stages not supported
```

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

Placeholder-only future modules remain excluded until implementation exists.

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

## Scientific rule

Do not optimize the architecture toward the current preferred theory. Optimize experiments toward discovering where the theory is wrong.

A negative result should simplify Ground 0 rather than trigger threshold tuning.

## Scientific boundary

Neither the HCT series nor current external-development work establishes natural-language understanding, learned semantics, biological equivalence, general intelligence, modern-retrieval superiority, end-to-end wall-clock superiority, autonomous cognition, or production integration.
