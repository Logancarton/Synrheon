# Hippocampal Sparse-Settling — Stochastic Consensus Trial

## Question

Can repeated perturbed recurrent trials produce a population-level winner that is more trustworthy than a single trajectory, while refusing to force a decision when the population remains split?

## Core hypothesis

The same relational field is rerun many times with small controlled perturbations to uncertain activations and relation strengths. Each run uses fixed-width state-dependent recurrence. The experiment records which candidate wins each trial.

After a minimum number of trials, the system may commit only when both conditions are met:

```text
winner share >= 0.58
winner share - runner-up share >= 0.34
```

If those conditions are not met, sampling continues until a maximum of 51 trials. If the field is still split at that point, the result remains unresolved rather than forcing a winner.

## Why perturb the trials?

Repeating a deterministic calculation would add no information. Perturbations simulate uncertainty in the evidence and test whether the same attractor remains dominant across plausible nearby states.

The perturbation never changes candidate identity or the hidden correct answer. It only slightly changes initial activation and existing excitation/inhibition strengths.

## Counterfactual preservation

When the system commits, it retains strong losing hypotheses rather than deleting them. A losing candidate is retained when its empirical win share is at least 20% of the winner's share. The runner-up is always retained so every commitment has at least one explicit counterfactual available for later analysis.

## World families

The assay reuses the five mixed relational regimes:

```text
easy_clear
delayed_clear
persistent_close
misleading_early
unresolved_close
```

The first four are treated as resolvable. The final type is intentionally designed to remain close enough that abstention is often the correct system behavior.

## Controls

The assay also reports deterministic fixed-width recurrent accuracy on the same worlds. This matters because repeated trials should not receive credit merely for spending more computation.

## Predeclared interpretation

The theory is discounted if any of the following occur:

- committed accuracy on resolvable worlds falls more than 5 percentage points below deterministic fixed recurrence;
- fewer than 65% of resolvable worlds reach commitment;
- more than 35% of unresolved-close worlds are forced into commitment;
- misleading-early committed accuracy falls below 85%;
- the system fails to retain explicit losing counterfactuals.

The result is inconclusive if resolvable worlds rarely reach early consensus or if unresolved worlds rarely require the full trial budget, because then the assay has not exercised both sides of the hypothesis.

A reinforced result requires stable population consensus on resolvable worlds, meaningful abstention on unresolved worlds, and preserved counterfactual losers.

## What this can prove

A positive result would support the claim that confidence should be estimated from repeated plausible recurrent trajectories rather than from one trajectory's internal gap alone.

It would not prove that the chosen thresholds are optimal, that the method is biologically hippocampal, or that it improves language models.

## Run

```bash
python3 -m experiments.hippocampal_consensus_trials --quick
python3 -m pytest -q tests/test_hippocampal_consensus_trials.py
```

## Observed result — recorded 2026-08-09

Reproduced by `tests/test_hippocampal_consensus_trials.py` (marked `historical`).

```text
seeds                                        40000-40250
unresolved_close committed_rate              0.78
preregistered maximum committed_rate         0.50
unresolved_close correct_or_abstain_rate     0.22
frozen verdict                               DISCOUNTED
```

### Standing conclusion

Population consensus manufactured agreement on worlds built to be genuinely unresolvable.
This is part of why `winner != sufficient evidence` survived into the current architecture.
Do not adjust the consensus mechanism to force abstention here.
