# Hippocampal Learned-Resistance Assay

This is the second controlled experiment on the hippocampal sparse-settling branch.

The first assay proved that a hand-specified broad → recurrent → sparse settling field can overturn a misleading first-pass winner and can preserve ambiguity for clarification.

This assay removes the hand-specified channel preference.

## Question

Can repeated outcomes teach the settling system which evidence channels should become easy or hard to traverse, then transfer that learned resistance profile to unseen anonymous candidates after learning is frozen?

## Signal flow

```text
training episode
    ↓
broad anonymous candidate field
    ↓
outcome becomes known
    ↓
compare correct support vs strongest wrong support per evidence channel
    ↓
reliable channel → resistance decreases
misleading channel → resistance increases
    ↓
repeat over many unrelated anonymous episodes
    ↓
FREEZE resistances
    ↓
held-out unseen candidate identities
    ↓
recurrent sparse settling using frozen resistance
```

The update is:

```text
delta_R_j = learning_rate * (strongest_wrong_support_j - correct_support_j)
R_j <- clamp(R_j + delta_R_j)
```

At inference, resistance is converted to conductance:

```text
G_j = 1 / R_j
```

and normalized conductance weights scale the evidence entering the same recurrent settling operator from the first assay.

## Synthetic world family

Every episode contains three anonymous candidates and four anonymous evidence channels.

Channel 0 is deliberately seductive but historically misleading. Wrong candidates tend to have strong evidence there and often have the strongest initial activation.

Channels 1–3 are individually less dramatic but jointly reliable for the successful candidate.

The learner is not told this rule. It starts with equal resistance on every channel.

Candidate names never become model parameters.

## Baselines and transfer

The held-out comparison is:

```text
Equal resistance recurrent settling
vs
Learned frozen resistance recurrent settling
```

A second held-out pass independently renames every candidate. Performance should remain unchanged if identity is not being memorized.

## Run

Quick assay:

```bash
python3 -m experiments.hippocampal_learning --quick
```

Full assay:

```bash
python3 -m experiments.hippocampal_learning
```

Tests:

```bash
python3 -m pytest -q tests/test_hippocampal_learning.py
```

## Required interpretation boundary

A positive result would demonstrate learned structural resistance transfer inside this generated family.

It would not yet prove language understanding, autonomous generation of clarification questions, biological equivalence to the hippocampus, or production Synrheon integration.

The next stronger experiment would vary the structural family itself: change the number of candidates, reliability distribution, evidence-channel count, and conflict topology while preserving only the abstract principle that distributed consensus should outperform a seductive single cue.
