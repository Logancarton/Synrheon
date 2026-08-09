# Hippocampal Sparse-Settling E3 — One-Pass Equivalence Test

## Why this test exists

The previous assay showed that learned channel resistance can improve held-out inference and transfer across renamed candidate identities.

That does **not** prove that recurrent settling is doing useful work.

The current operator uses fixed evidence anchors across all six cycles. If the same winner can be obtained from the exact first recurrent update, then the extra cycles and progressive sparsity are not yet justified by the evidence.

This experiment is therefore designed to falsify the recurrent claim.

## Question

```text
same learned resistance
same visible evidence
same initial activation
same consensus rule
same contradiction rule

one exact first-cycle pass
             versus
six recurrent settling cycles
```

Does recurrence improve held-out decisions?

## Conditions

The assay trains channel resistance exactly as `hippocampal_learning.py` does, freezes it, and evaluates unseen worlds under three inference conditions.

### A. Exact one-pass control

This reproduces cycle 1 of `settle()` exactly and stops.

It therefore receives the same:

```text
conductance-weighted support
initial activation
consensus count
contradiction penalty
```

but no repeated state evolution and no multi-cycle Top-K contraction.

### B. Recurrent progressive sparsity

```text
cycles = 6
K = (3, 3, 3, 2, 2, 2)
```

### C. Recurrent fixed sparsity

```text
cycles = 6
K = (3, 3, 3, 3, 3, 3)
```

This separates repeated recurrence from progressive field contraction.

## Predeclared interpretation

If one-pass/recurrent agreement is at least 98% and recurrent accuracy advantage is below 1 percentage point:

```text
CURRENT RECURRENCE NOT YET NECESSARY
```

The learned resistance result remains valid, but the present world family does not demonstrate independent value from recurrence.

If recurrent accuracy exceeds one-pass accuracy by at least 3 percentage points:

```text
EVIDENCE FOR RECURRENT VALUE
```

Otherwise:

```text
MIXED RESULT
```

No code or threshold should be changed merely to obtain the desired verdict.

## What a negative result would mean

A negative result is scientifically useful.

It would tell us that the current recurrence is mathematically too shallow because evidence is static across cycles. The next recurrence design would need state-dependent interaction such as:

```text
candidate-to-candidate excitation/inhibition
changing evidence support as competitors disappear
reconstructed pattern feeding back into the next cycle
cycle-dependent contradiction
new evidence arriving between cycles
attractor-state transitions
```

That would create an actual dynamical computation rather than repeating nearly the same weighted score.

## Run

```bash
python3 -m experiments.hippocampal_equivalence --quick
python3 -m pytest -q tests/test_hippocampal_equivalence.py
```

## Scientific boundary

This test addresses only whether recurrence is necessary in the current synthetic world family. It does not yet test changed world structure, natural language, learned representations, or biological equivalence.
