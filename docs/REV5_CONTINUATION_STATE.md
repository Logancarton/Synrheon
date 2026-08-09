# Synrheon Ground 0 — Revision 5 Continuation State

**Authoritative continuation note — August 9, 2026**

This document records the current scientific continuation state for the Ground 0 contextual-tapering research program. It supersedes the older continuation boundary in `docs/CONTEXT_SETTLED_TAPERING_THEORY.md` Revision 4 where that document still says EXT-1 is the immediate next gate.

## Current branch lineage

```text
Historical synthetic research branch:
experiment/hippocampal-sparse-settling

Current external-validation branch:
experiment/external-retrieval-cascade
```

`experiment/external-retrieval-cascade` is a strict descendant of the historical hippocampal branch and is the branch from which scientific work should continue. Preserve the historical branch; do not silently move or rewrite it.

Current external branch head at the time of this revision:

```text
85c3d780eb192114a32ae6c492289174eb54cc64
Test EXT-2 diagnostic integrity
```

Current external-validation source includes:

```text
experiments/external_retrieval_cascade.py
experiments/ext2_diagnostics.py
tests/test_external_retrieval_cascade.py
tests/test_ext2_diagnostics.py
```

## Current evidence ledger

### Supported

- Reversible suppression has strong synthetic evidence.
- A one-pass full-context soft taper approximately preserves the BM25 SciFact development anchor.
- Meaningful oracle headroom remains on development data.

### Falsified or discounted in the current external implementation

- EXT-1 C1/C2/C3 are not validated as originally hoped in the current implementation.
- Current static recurrence is not beneficial on SciFact development; removing recurrence improved development nDCG from approximately `0.5081` to `0.5415`.
- The current four hand-designed channels are not established as useful residual discriminators.
- Current commitment calibration is not established.

### Partially supported / open

- External value of reopening remains open.
- Contextual state persistence is a plausible cause of the partial-context -> full-context degradation but is not yet established.

### Untested

- Question-guided contextual divergence.
- Trajectory-based recurrence.
- Residual-guided tapering.
- The matched-compute multiple-soft-taper hypothesis.

## Why D6 must come before the major multi-taper experiment

The current external implementation already contains a sequential process in which a partial cue creates a taper state and a later full-context taper may receive that previous activation as its prior.

Current diagnostics indicate that a single full-context soft taper is approximately harmless relative to BM25, while the partial -> full sequential pathway deteriorates sharply. Therefore, adding more sequential taper stages before understanding this transition could amplify a state-persistence pathology and falsely attribute the damage or recovery to multi-taper architecture.

The immediate scientific gate is therefore **D6 only**.

## D6 — Transition Persistence Diagnostic

Keep everything else frozen:

- same 93 SciFact development queries;
- same BM25 candidate field;
- same current channels;
- same learned parameters;
- no final split;
- no recurrence;
- no new semantic channels;
- no threshold tuning.

Conditions:

```text
A — BM25 / full-query anchor
B — one full-context soft taper
C — partial -> full with carried activation, no recurrence
D — partial -> full, reset before the full-context stage
E — partial -> full where stage two acts only on the unresolved residual
```

Define observed transition damage:

```text
Delta_damage = B - C
```

Define reset recovery fraction:

```text
R_reset = (D - C) / (B - C)
```

Interpretation thresholds are frozen before observing D6:

- **Major persistence contribution supported:** `D > C` with paired 95% CI excluding zero and reset restores at least 50% of the B -> C damage.
- **Persistence insufficient:** reset restores less than 25% of B -> C damage.
- **Partial support:** reset restores 25% to <50% of B -> C damage.

Do not lower or reinterpret these thresholds after observing D6.

## MT-1 — Matched-Compute Multi-Taper Falsification

MT-1 is blocked until D6 resolves the transition-state question.

The primary comparison must separate the actual hypotheses:

```text
single full-context soft taper
vs
multiple context-settled soft tapers
vs
matched-compute hard staged pruning
```

Also include:

```text
multi-stage reset condition
scrambled-order multi-stage condition
clock-driven Top-K as negative control only
```

The major success criterion is asymmetric:

> **Hard pruning losing is not sufficient evidence for multi-taper necessity.**

Multi-taper necessity is supported only if multi-soft materially outperforms single-soft under matched computation.

If multi-soft and single-soft are equivalent while hard pruning loses reactivation, the correct conclusion is:

```text
reversibility supported
multiple contextual settling stages not supported
```

## Synthetic isolation requirements for MT-1

Freeze these controls before running the assay:

- unseen-world evaluation;
- unseen-identity evaluation;
- opaque/randomized candidate IDs;
- final worlds untouched during design/tuning;
- qrels/target identity forbidden from routing or relation construction;
- candidate renaming must not materially change performance.

Report separately rather than compressing into one efficiency score:

- top-1 quality;
- correct-candidate survival;
- suppressed-correct reactivation;
- unresolved-world commitment;
- feature evaluations;
- candidate-update operations;
- recurrence work;
- measured runtime.

## Scientific rule for continuation

Do not optimize the architecture toward the current preferred theory. Optimize experiments toward discovering where the theory is wrong.

Negative results should narrow or simplify Ground 0 rather than trigger threshold tuning.

The current strongest defensible claim is not that the old cascade is validated. It is a narrower contextual-divergence hypothesis:

> **Reversible contextual state transitions may preserve useful alternatives, but the necessity of multiple contextual settling stages remains unproven and must be tested only after transition-state persistence is isolated.**
