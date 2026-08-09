# Hippocampal Sparse-Settling Experiment

Status: experimental only. Not production cognition.

## Question

Can an input open a broad possibility field, then use repeated recurrent cycles to settle toward a smaller mutually compatible sparse state rather than choosing the strongest first-pass association?

The experiment also tests whether an unresolved field can ask for the next discriminating fact and run the same settling equation again.

## Core Update

For candidate `i`:

```text
recurrent_i = sum(support_ij * anchor_j) / resistance_i
raw_i = alpha * previous_i + beta * recurrent_i + gamma * initial_i
raw_i *= 1 + consensus_weight * consensus_i
raw_i -= contradiction_weight * contradiction_i
```

After each cycle the field is normalized and progressively Top-K sparsified.

Interpretation:

```text
initial activation  = what looks plausible immediately
support             = how well broad evidence supports the candidate
resistance          = how difficult the learned pathway is to traverse
consensus           = how many broad evidence dimensions agree
contradiction       = evidence pushing against the candidate
progressive sparsity= fewer candidate paths survive over time
```

## Transparent Scenario

Input:

```text
Logan + Daisy + leash + ? + happy
```

Candidates:

```text
Park
Vet
Neighborhood
```

`Vet` deliberately has the strongest initial activation. The experiment passes the first qualitative hypothesis only if recurrent settling can still select `Park` when its total support, consensus, and lower resistance make it the more coherent pathway.

A second ambiguous version deliberately leaves the first field unresolved. It then asks:

```text
Did Daisy get into the car?
```

The answer becomes another broad input dimension and the same settling operator runs again. The refined state is expected to settle on `Vet`.

## Truth / Exception Probe

The experiment separately represents:

```text
Is it supported as true?
Is it always true?
Can it be false?
```

These are not collapsed into one confidence number. A frequent relationship can therefore remain strongly predictive without becoming a universal rule.

## Run

```text
python -m experiments.hippocampal_settling
```

Tests:

```text
python -m pytest -q tests/test_hippocampal_settling.py
```

## What This Does NOT Prove

This is a hand-constructed mathematical assay. Sensible support and resistance values are supplied deliberately. It demonstrates that the proposed dynamics are computationally coherent and observable; it does not prove that Synrheon can learn those values from experience.

The next scientific gate is therefore:

```text
experience only
    ↓
learn support + resistance
    ↓
unseen ambiguous world
    ↓
settle correctly without hand-set pathway values
```

That is the point where the architecture starts becoming evidence for learned cognitive dynamics rather than a designed demonstration.
