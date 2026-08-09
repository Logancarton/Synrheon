# HCT-2 Preregistration: Ordered Conditional Context Settling

**Synrheon Experimental Research Program**  
**Frozen before final HCT-2 held-out evaluation**  
**Date:** August 9, 2026  
**Branch:** `experiment/hippocampal-sparse-settling`

## 1. Why HCT-2 exists

HCT-1 reinforced a narrower claim than the full contextual-settling theory originally proposed. In its final 200-world assay, reversible soft tapering preserved uncertainty, survived opaque renaming, sharply reduced recurrent-field size, and recovered from context reversal where irreversible Top-K pruning failed. However, the generic soft control matched the context-specific cascade on correct-or-abstain behavior and reactivation while using fewer taper evaluations.

Therefore HCT-2 does **not** retest whether reversible soft narrowing works. Its purpose is to test the unresolved stronger claim:

> Does a learned order of context-specific settling become useful when context channels are hierarchically aliased and later context is cheaper or safer to evaluate only after earlier context has narrowed the active field?

The primary HCT-2 claim is an **efficiency-with-preserved-behavior** claim, not an accuracy-superiority claim.

## 2. HCT-2 hypothesis

### HCT-2 — Learned Ordered Conditional Sparse Settling

A learned ordering of reversible sparse context stages will preserve high correct-or-abstain behavior and correct-candidate survival in hierarchically aliased worlds while using substantially fewer context-feature evaluations than a strong simultaneous learned generic-soft control. The learned order should also be more evaluation-efficient than the same sparse mechanism run in a fixed anonymous channel order.

The hypothesis is weakened if the generic soft control matches behavior at similar context-evaluation cost, if the learned order provides no measurable efficiency benefit over fixed order, if correct candidates fail to survive sparse settling, or if reversibility is lost.

## 3. What changes from HCT-1

HCT-1 used 256 opaque candidates and evaluated every candidate at every contextual taper stage. That proved reversibility but made the multi-stage cascade itself expensive.

HCT-2 introduces:

- 512 opaque candidates per world;
- hierarchical context paths with parent-conditioned token encoding;
- anonymous context channels presented out of semantic-depth order;
- alias competitors that can match deep context tokens while belonging to the wrong broad context;
- reversible sparse eligibility, where low-activation candidates become dormant rather than deleted;
- a learned context order derived only from training outcomes;
- a strong simultaneous generic-soft control using the same learned context gains;
- a fixed anonymous-order sparse control;
- explicit no-resistance and no-recurrence ablations;
- separate accounting for context-feature evaluations and recurrent candidate-cycles;
- a reserved final split that is never used by `--quick`, development tests, parameter selection, or tuning.

## 4. Conditional context construction

Each candidate has a four-level latent semantic path. Deeper raw context tokens are encoded by deterministic prefix-specific codebooks. Therefore the same observed deep token can occur under different broad contexts.

The observed context channels are intentionally anonymous and scrambled:

```text
channel 0 -> semantic depth 2
channel 1 -> semantic depth 0
channel 2 -> semantic depth 3
channel 3 -> semantic depth 1
```

The learner is not handed the semantic order. It learns evidence resistance, context gains, and a global context-channel order from the training split.

The principal stressor is contextual aliasing: many wrong-broad-context candidates share two or three deep raw tokens with the correct path. In context-reversal worlds, the initial cue deliberately establishes a strong wrong basin; later context changes to the true basin. Reversible mechanisms may reopen from the broad field. Hard Top-K may only rescore candidates it retained.

## 5. Conditions

HCT-2 compares seven conditions:

```text
1. no_taper
2. hard_topk
3. generic_soft
4. fixed_order_sparse
5. learned_order_sparse
6. learned_order_no_resistance
7. learned_order_no_recurrence
```

### No taper

Runs recurrence over all 512 candidates.

### Hard Top-K

Scores the broad field using the learned context gains, keeps only 16 candidates, and permanently excludes the rest for that inference episode. Later context may rescore only the retained set.

### Generic soft

Uses all learned context gains simultaneously across the full candidate field for up to eight settling cycles. It is deliberately a strong control and is allowed to spend more context-feature evaluations than the sparse cascade.

### Fixed-order sparse

Uses the same reversible sparse stage mechanism and learned gains as the proposed model, but evaluates anonymous channels in fixed numerical order `(0, 1, 2, 3)`.

### Learned-order sparse

Uses the learned channel order. After each stage, only candidates above the reversible eligibility gate continue to receive expensive context-feature evaluation. Dormant candidates retain activation state and are not deleted. A context reversal may reopen from the broad field and rerun the cascade.

### No-resistance ablation

Uses the learned ordered sparse cascade but equalizes recurrent evidence resistance.

### No-recurrence ablation

Uses the learned ordered sparse cascade but replaces downstream recurrent interaction with a static final ranking/commitment calculation.

The ablations are diagnostic. They are **not forced to fail** by the primary frozen HCT-2 gate.

## 6. World types

Each split contains five equally cycling world classes:

```text
clear_hierarchy
alias_conflict
misleading_deep
unresolved_branch
context_reversal
```

`clear_hierarchy` tests ordinary conditional narrowing.

`alias_conflict` increases evidence favoring candidates that match deeper tokens while belonging to the wrong broad context.

`misleading_deep` makes deep evidence especially seductive.

`unresolved_branch` creates a nearly symmetric rival and should usually produce abstention rather than forced commitment.

`context_reversal` begins inside a strong wrong contextual basin and later changes to the true basin, testing whether suppressed candidates can re-enter.

## 7. Information firewall

The generator may use hidden truth to construct a scoreable synthetic world and explicit relation structure. Held-out inference may receive only the generated candidate evidence, context tokens, current cue, learned global parameters, and explicit excitation/inhibition relations.

The recurrent solver must not consult `correct_index`.

The hidden correct index may be used only for:

```text
training updates after outcomes are known
post-inference scoring
survival measurement
suppression/reactivation measurement
```

Candidate names are opaque and may be regenerated independently without changing the world structure.

## 8. Seed firewall

The splits are frozen as:

```text
TRAINING
70000-70499
500 worlds

DEVELOPMENT
71000-71149
150 worlds

QUICK DEVELOPMENT
71000-71049
50 worlds

FINAL HELD-OUT
72000-72299
300 worlds
```

`--quick` uses only the 50-world development subset. It does not touch final seeds.

`--development` uses the complete development split.

The default command uses the 300-world final split.

No final HCT-2 seed is to be used for tuning, gate changes, parameter selection, threshold changes, or debugging.

## 9. Frozen HCT-2 interpretation gate

HCT-2 v1 is reinforced only if all primary criteria hold on the untouched 300-world final split:

```text
learned-order sparse good behavior >= 90%
correct-candidate survival >= 95%
unresolved commitment <= 20%
at least 10 genuine reversal-suppression cases
learned-order reversal reactivation >= 80%
hard Top-K reactivation at least 30 percentage points worse
learned-order recurrent cost <= 10% of no-taper recurrent cost
candidate-renaming retention >= 97%
generic-soft behavior advantage <= 3 percentage points
learned-order context-feature evaluations <= 50% of generic soft
learned-order context-evaluation efficiency >= 3% better than fixed-order sparse
learned channel order must recover semantic depth order 0 -> 1 -> 2 -> 3
```

If too few reversal cases are actually exercised, the final assay is inconclusive.

If any other frozen primary criterion fails, HCT-2 is discounted on that criterion. Thresholds are not to be moved after final results are observed.

## 10. Cost interpretation

HCT-2 reports two distinct operation counts:

```text
context-feature evaluations
recurrent candidate-cycles
```

A context-feature evaluation means one candidate/context-channel compatibility check.

A recurrent candidate-cycle means one candidate processed for one recurrent cycle.

These counts are not assumed to have equal hardware cost. HCT-2 therefore does not make a wall-clock or energy-efficiency claim unless a later experiment introduces and justifies an explicit calibrated cost model.

## 11. Development calibration already permitted

Development-only runs are allowed before the gate is frozen in order to verify that the generator exercises the intended mechanisms, that the learned order is recoverable, and that the code is scientifically testable.

The final 72000-72299 split remains the confirmatory test.

Once this preregistration and the corresponding experiment are committed, any material mechanism or threshold change requires a new HCT-2 version and a new untouched final split.

## 12. Possible interpretations

If learned-order sparse matches generic behavior but uses substantially fewer context-feature evaluations, HCT-2 supports **ordered sparse contextual efficiency**, not accuracy superiority.

If learned-order sparse also outperforms fixed-order sparse on evaluation efficiency, it supports the proposition that learned stage ordering matters under hierarchical aliasing.

If generic soft matches both behavior and context-evaluation cost, the stronger ordered-stage claim is weakened.

If fixed-order sparse matches or beats learned order, the learned-order claim is weakened.

If no-resistance or no-recurrence ablations match the full mechanism, the corresponding learned-resistance or recurrent component is not necessary in this HCT-2 world family.

If hard Top-K again fails after context reversal while reversible methods recover, that replicates HCT-1's reversibility result under a new generator.

## 13. Scientific boundary

Even a successful HCT-2 would remain controlled synthetic evidence. It would not establish:

- biological hippocampal equivalence;
- semantic understanding;
- natural-language reasoning;
- general intelligence;
- superiority to transformers, attention, associative retrieval, mixture-of-experts, or modern learned routing;
- total compute superiority without a calibrated cost model;
- production readiness.

A successful HCT-2 would strengthen a narrower computational case: a large hypothesis field can be narrowed through learned ordered reversible context stages, with later context evaluation concentrated on a progressively smaller active field while dormant alternatives remain recoverable.
