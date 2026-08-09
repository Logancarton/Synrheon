# D6 Preregistration — Transition Persistence Diagnostic

**Synrheon Ground 0**  
**Frozen before the SciFact development run**

## Question

Does carrying a context-settled activation state from an under-specified partial cue into later full context cause a substantial portion of the observed partial -> full degradation?

D6 is an isolation diagnostic. It does not test the reserved final split and it does not validate MT-1.

## Frozen scope

Use exactly the current external-validation machinery on the SciFact development partition:

```text
same 93 development queries
same BM25 top-100 candidate field
same current four channels
same learned parameters
no recurrence
no new semantic channels
no threshold tuning
no final split
```

The current branch is:

```text
experiment/external-retrieval-cascade
```

## Conditions

### A — BM25 full-query anchor

Rank the frozen top-100 candidate field by the existing BM25 retrieval score.

### B — one full-context soft taper

Run the existing `soft_taper` once from the normal full-query BM25 activation prior. No recurrence.

### C — partial -> full with carried activation

1. Build the same full-query BM25 top-100 field.
2. Construct the same under-specified cue used by EXT-1 reopening: the first half of query tokens when the query contains at least four tokens.
3. Create the partial-cue prior with the existing channel-0 cue-prior mechanism.
4. Run the existing soft taper under the partial cue.
5. Carry the resulting complete activation state into a second existing soft taper under full context.
6. Rank directly from the resulting activation. Do not run recurrence.

Queries that do not admit the frozen partial cue remain in A/B summary metrics but are excluded from C/D/E paired transition diagnostics. D6 must report the number of transition-evaluable queries.

### D — partial -> full with reset

Run the same partial stage as C, but before full-context tapering restore the original full-query BM25 activation prior. Then run exactly the same full-context soft taper as B. No other state is allowed to carry from the partial stage into the full stage.

This is intentionally a strong isolation control. If D and B are not numerically equivalent apart from metering/timing noise, the implementation has an uncontrolled path dependency and D6 must be considered invalid until that discrepancy is explained.

### E — partial -> full residual refinement

Run the same partial stage as C and retain its complete reversible activation state. During the second stage, do **not** apply the full-context feature value as though no earlier context had been processed. Instead, for each candidate and channel use the answer-independent feature residual:

```text
residual_value = feature(full_context) - feature(partial_context)
```

The existing stage decay, temperature, channel gains, active-set gate, stage order, stage-cycle count, dormant floor, and minimum active width remain unchanged. Only the stage-two feature term changes from the full value to the residual value.

Negative residuals are preserved. They are evidence that later context reduced support. No qrel, correct identity, relevance label, or outcome may be used to clip or select residuals.

E is diagnostic. No success threshold for E is declared in D6; its raw behavior will inform the later MT-1 design if D6 is valid.

## Primary quantities

Let `A`, `B`, `C`, `D`, and `E` denote mean nDCG@10 on the same transition-evaluable query set for the respective conditions.

Observed sequential damage:

```text
Delta_damage = B - C
```

Reset recovery fraction:

```text
R_reset = (D - C) / (B - C)
```

If `B - C <= 0`, the presumed partial -> full damage is not reproduced and the persistence diagnosis loses its premise. In that case do not interpret `R_reset` as supportive.

## Frozen statistical comparison

Compute paired query-level bootstrap intervals using the existing EXT-1 bootstrap procedure and frozen resample count/seed.

The primary paired effect is:

```text
D - C
```

Report its mean delta and 95% bootstrap interval.

Also report `B - C`, `E - C`, and `E - B` with paired intervals for diagnosis, without creating post-hoc pass criteria for E.

## Frozen interpretation

### Major persistence contribution supported

Only if all are true:

```text
B - C > 0
D - C > 0
95% paired CI for D - C excludes zero on the positive side
R_reset >= 0.50
```

### Partial support

```text
B - C > 0
0.25 <= R_reset < 0.50
```

### Persistence insufficient

```text
B - C > 0
R_reset < 0.25
```

### Inconclusive

Use `INCONCLUSIVE` rather than upgrading the claim if the magnitude criterion appears large but the paired interval for `D - C` includes zero, or if too few queries admit the frozen partial cue for a stable paired interpretation.

### Damage not reproduced

If `B - C <= 0`, report `DAMAGE_NOT_REPRODUCED`. Do not tune the cue, channels, decay, gain, temperature, gate, or thresholds to force the expected degradation to appear.

## Integrity requirements

D6 is invalid if any of the following occur:

- any final-split query is evaluated;
- qrels affect candidate transitions, routing, residual construction, or recurrence;
- recurrence is invoked;
- B and D differ because reset failed to restore the original full-query activation state;
- the channel set or learned parameters differ across conditions;
- a threshold is changed after observing D6;
- synthetic smoke data are described as evidence.

## Required raw output

Report:

```text
number of SciFact development queries
number of transition-evaluable queries
A/B nDCG@10 on all development queries
A/B/C/D/E nDCG@10 on the paired transition-evaluable set
B-C paired delta + CI
D-C paired delta + CI
E-C paired delta + CI
E-B paired delta + CI
R_reset
per-condition feature evaluations
per-condition measured feature time
frozen verdict
```

Preserve per-query outcomes so unexpected failures can be inspected rather than averaged away.

## Scientific boundary

D6 can identify whether carried activation is a major contributor to the current transition failure. It cannot establish that multiple contextual tapers are useful, that residual refinement is correct, or that recurrence should return. MT-1 remains blocked until D6 is interpreted under these frozen rules.
