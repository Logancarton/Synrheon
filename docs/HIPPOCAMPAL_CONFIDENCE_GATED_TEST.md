# Confidence-Gated Adaptive Sparsity Test

## Hypothesis

Keep the candidate field broad while the top alternatives are close or the field is still moving. Collapse only when the leading state is both clearly ahead and stable.

The tested gate is:

```text
minimum open cycles = 3
leader gap >= 0.18
L1 state-change <= 0.10
then collapse to K = 2
```

## Why this test follows the prior result

The stateful recurrence assay found:

```text
one pass                  0.0%
clock-driven progressive 25.5%
fixed-width recurrence   98.0%
```

This showed that recurrence can matter while scheduled pruning can destroy useful states before a coherent recurrent pattern forms.

## Controls

The new assay compares four conditions on the same unseen worlds:

1. one-pass initial evidence;
2. clock-driven progressive sparsity;
3. fixed-width stateful recurrence;
4. confidence-gated stateful recurrence.

Candidate renaming is repeated as an identity control.

## Predeclared interpretation

The revised hypothesis is reinforced if confidence-gated inference:

```text
accuracy >= 90%
within 5 percentage points of fixed-width recurrence
at least 40 percentage points above clock-driven pruning
```

It is discounted if adaptive pruning falls at least 20 percentage points below fixed-width recurrence.

It is inconclusive if the gate almost never activates, because that would merely reproduce fixed-width recurrence.

## Important scientific point

This is not a test designed to make the theory pass. A failure means the proposed clear-and-stable gate still prunes too early or uses the wrong observable. A non-triggering gate means the rule has not added anything. A positive result would support the narrower claim that sparsification should be driven by state evidence rather than elapsed recurrent cycles.

## Run

```bash
python3 -m experiments.hippocampal_confidence_gated --quick
python3 -m pytest -q tests/test_hippocampal_confidence_gated.py
```

## Observed result — recorded 2026-08-09

Reproduced by `tests/test_hippocampal_confidence_gated.py` (marked `historical`).

```text
seeds                           30000-30500
adaptive accuracy               0.850
fixed-width accuracy            0.852
active state savings vs fixed   0.0761
preregistered minimum savings   0.10
frozen verdict                  MIXED RESULT
```

### Standing conclusion

Adaptive gating preserved accuracy and **failed** its preregistered efficiency criterion.
The hypothesis failed on cost, not on correctness. Do not retune the gate to reach 0.10.
