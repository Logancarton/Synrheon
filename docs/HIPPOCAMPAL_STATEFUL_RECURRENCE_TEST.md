# Hippocampal Sparse-Settling E4 — Stateful Recurrence Test

## Why this test exists

The previous one-pass equivalence assay showed that static-anchor recurrence improved accuracy only slightly and progressive sparsity did not outperform fixed K.

That means the earlier recurrence was not yet doing enough state-dependent computation.

This experiment changes the mathematics so the state at cycle `t` changes what evidence is received at cycle `t+1`.

## Core question

Can a recurrent field solve unseen relational configurations that a matched one-pass initial scorer cannot?

## Construction

Four candidates are active.

Candidates 0-2 form a coherent triad:

```text
A ↔ B
↕   ↕
C ↔ A
```

They moderately excite one another.

Candidate 3 is a lure:

```text
D
```

It begins with the strongest initial activation, but it conflicts with two members of the coherent triad.

The correct candidate is one member of the triad and receives a small structural advantage from the other two members.

The one-pass condition sees only the initial field and therefore tends to choose the lure.

The recurrent condition allows support and conflict to circulate through the field for multiple cycles.

## Recurrent equation

For candidate `i`:

```text
u_i(t+1)
  = p * a_i(t)
  + e * sum_j excitation[j,i] * a_j(t)
  - h * sum_j inhibition[j,i] * a_j(t)
  + g * initial_i
```

Then:

```text
a(t+1) = Normalize(max(0, u(t+1)))
```

Optional progressive sparsity contracts the field from four active candidates to three and finally two.

The important distinction from the previous assay is:

```text
a_j(t) changes every cycle
```

so the recurrent input itself changes.

## Conditions

### A. One-pass control

Chooses from normalized initial activations only.

### B. Stateful recurrence + progressive sparsity

Eight recurrent cycles with candidate-to-candidate excitation and inhibition.

### C. Stateful recurrence without progressive sparsity

Same recurrence, but all four candidates remain active.

This separates recurrent value from the added contribution of progressive sparsity.

## Predeclared interpretation

If recurrent accuracy exceeds one-pass accuracy by at least 25 percentage points and recurrent accuracy is at least 80%:

```text
EVIDENCE FOR STATE-DEPENDENT RECURRENT VALUE
```

If the advantage is below 5 percentage points:

```text
STATE-DEPENDENT RECURRENCE NOT YET SUPPORTED
```

Otherwise:

```text
MIXED RESULT
```

These thresholds should not be changed merely to obtain a desired outcome.

## What a positive result would mean

A positive result would demonstrate that multiple cycles are computationally useful when later evidence depends on the current state.

It would not yet prove general intelligence, biological fidelity, or superiority to all alternative graph/recurrent models.

## What a negative result would mean

A negative result would suggest that the present excitation/inhibition design is still too weak, too easily approximated, or poorly matched to the task.

The next step would then be to test learned recurrent edges, attractor reconstruction, or dynamic evidence arrival rather than tuning thresholds to force success.

## Run

```bash
python3 -m experiments.hippocampal_stateful_recurrence --quick
python3 -m pytest -q tests/test_hippocampal_stateful_recurrence.py
```

## Scientific boundary

The generator intentionally contains relational structure that recurrence can exploit. Therefore a positive result establishes only that state-dependent recurrence can add value under controlled conditions. Later experiments must test changed graph families, learned recurrent relations, noise, reversal, and simpler equivalent baselines.
