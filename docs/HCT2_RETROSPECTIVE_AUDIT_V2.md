# HCT-2 Retrospective Audit v2

**Status:** frozen retrospective diagnostic before v2 outputs are inspected  
**Historical target:** HCT-2 v1 remains unchanged  
**Evidence class:** retrospective audit only; cannot upgrade HCT-2

## Why v2 exists

The first 8-world smoke audit exposed three unresolved issues:

1. all 24 channel orders achieved identical good behavior, so behavioral order sensitivity was unresolvable at that difficulty;
2. the supervised learned order exactly matched an answer-independent selectivity order;
3. original, removed, and shifted relation graphs changed commitment behavior while leaving winner identity unchanged on the smoke slice.

The smoke run is engineering-only and is not scientific evidence. v2 sharpens the audit before any larger run.

## Audit A — order-learning equivalence

HCT-2 v1 learns channel utility as:

```text
utility(channel) = mean_worlds(correct_match - candidate_mean_match)
```

For the HCT-2 generator, training uses the final true cue and the designated correct candidate carries the true context tokens. Therefore:

```text
correct_match = 1 for every channel in every training world
utility(channel) = 1 - mean_matching_fraction(channel)
```

Thus descending supervised utility and ascending answer-independent selectivity are the same ordering, except for possible tie-breaking.

This is a **specification consequence**, not evidence that the learner discovered semantic depth. v2 must report and regression-test this equivalence across multiple disjoint training blocks only as an implementation check.

## Audit B — behavioral-resolution sweep

The original 8-world smoke slice had a behavioral ceiling: every one of the 24 orders achieved good behavior 1.0. More worlds at the same difficulty cannot make order informative if the task remains at ceiling.

Before a 50-world order comparison, v2 sweeps field size while holding the frozen HCT-2 learner and solver fixed:

```text
candidate_count in {512, 768, 1024, 1536}
```

The sweep uses a fixed retrospective development slice and evaluates all 24 orders at every field size.

Report for each field size:

- best / median / worst good-behavior rate across orders;
- number of distinct good-behavior rates;
- best / median / worst context-feature evaluations;
- whether the behavioral metric has resolution (`max_good > min_good`);
- learned-order behavior and cost;
- best-cost order among orders with learned-order behavior.

No supportive threshold is imposed. If every order remains behaviorally identical, order remains a compute-only claim in this generator family at the tested sizes.

This sweep is exploratory retrospective stress testing, not confirmation.

## Audit C — relation-generation provenance

The HCT-2 generator constructs its relation graph using hidden designated answer identity:

```text
coherent = {correct, allies...}
```

and gives additional incoming excitation to the correct candidate outside unresolved worlds. Therefore original relation alignment is truth-shaped by construction.

v2 records this as a generator provenance fact. A relation perturbation cannot convert the historical recurrence result into independent evidence of discovering useful relations.

## Audit D — four relation variants

Use the exact same frozen taper output for every relation variant so candidate evidence, cue, taper, field survival, and context-feature cost are held fixed.

Variants:

```text
original
no_relations
shifted_relations
random_relations
```

`shifted_relations` cyclically relabels endpoints while preserving graph topology and weights.

`random_relations` preserves the number of excitation/inhibition edges and each edge-weight multiset but samples new unique endpoints deterministically, destroying the original topology/alignment.

Report per variant:

- winner correctness;
- commit rate;
- good behavior;
- final target survival;
- context-feature evaluations.

## Audit E — per-world failure overlap

Aggregate equality is insufficient. v2 must retain the failing world seeds for each relation variant and report pairwise overlap for:

```text
no_relations vs shifted_relations
no_relations vs random_relations
shifted_relations vs random_relations
```

For each pair report intersection, union, Jaccard overlap, and exact-set equality.

Interpretation:

- similar aggregate rates with different failure sets means the mechanisms are not equivalent;
- shifted ≈ random ≈ none in both rates and failure identity suggests graph-to-answer alignment, rather than topology, carries most of the observed benefit;
- shifted differing from random suggests topology has an effect independent of original candidate alignment.

## Scientific boundary

This is a retrospective audit of a synthetic result whose historical outcomes are already known. It may downgrade or narrow HCT-2 interpretation. It cannot produce new confirmatory support for HCT-2.

Do not modify HCT-2 v1 generator, learner, taper, recurrence, or historical verdict to improve audit outcomes.
