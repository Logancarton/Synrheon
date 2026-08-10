# MT-1 Preregistration — Matched-Compute Multi-Taper Falsification

**Synrheon Ground 0**
**Status: FROZEN before result-bearing implementation**
**Unlocked by:** `docs/D6_RESULT.md`

## Question

> After controlling the known transition-state persistence pathology, does more than one
> soft contextual settling stage materially outperform one good soft settling stage
> **under matched computation**?

MT-1 isolates *stage necessity*. It does not test recurrence, residual refinement,
commitment calibration, new context channels, or Token Deck representation.

## Why this test exists now

D6 established that blindly carrying a state settled under partial context into changed
context causes major path-dependent damage (`R_reset = 1.0`,
`MAJOR_PERSISTENCE_CONTRIBUTION_SUPPORTED`).

D6 did **not** hold compute constant. Its two-stage conditions spent roughly twice the
per-query feature budget of its single-stage condition. So D6 answered "is carrying
harmful?" and left "is staging worth its cost?" open. MT-1 closes exactly that gap.

## Falsifier

If multi-stage soft settling does not materially beat single-stage soft settling under
the frozen matched-compute rule, **multiple contextual settling stages are removed from
Ground 0 as a required mechanism**, and one full-context soft settling stage becomes the
default architecture.

A negative MT-1 shrinks the architecture. It does not trigger threshold revision.

## Frozen scope and data boundary

```text
dataset:                     SciFact, development partition only
development queries:         exactly 93 (reject otherwise)
candidate field:             existing BM25 top-100 (CANDIDATE_DEPTH = 100)
channels:                    existing four (CHANNEL_NAMES), unchanged
learned parameters:          existing learn_parameters on development, shared by all conditions
recurrence:                  forbidden
new channels / features:     forbidden
reserved final split:        must not be loaded, scored, or inspected
minimum transition queries:  30
branch:                      experiment/external-retrieval-cascade
```

Token Deck work (TD-3 and later) is outside MT-1. No segmentation output, sense state, or
token identity may enter any MT-1 condition.

## Context partition

Stage contexts reuse the existing frozen cue machinery. No new partition is invented.

```text
partial context = _reopen_cue(query)      # first half of query tokens, requires >= 4 tokens
full context    = the complete query
```

Queries with fewer than four tokens admit no partial cue. They are reported and included
in single-stage summary metrics, but excluded from all paired multi-stage comparisons.
The count of transition-evaluable queries must be reported.

## Compute budget

The frozen compute unit is one **candidate x channel feature evaluation**, counted by the
existing `FeatureMeter`. Measured feature time (nanoseconds) is reported alongside but is
not the gate.

Every condition receives the same nominal **eight channel-cycle update sweeps** over the
frozen channel order:

```text
single stage:   4 channels x 2 cycles                    = 8 sweeps
two stages:     4 channels x 1 cycle, twice (stage 1, 2)  = 8 sweeps
```

Because the active-set gate narrows differently across conditions, nominal sweeps do not
guarantee equal cost. Actual mean feature evaluations per query are therefore measured and
gated (see Interpretation).

## Conditions

All conditions rank the same frozen BM25 top-100 field for the same query with the same
learned parameters.

### M0 — retrieval anchor

BM25 top-100 order. No taper.

### M1 — single full-context soft settling **(primary baseline)**

The existing `soft_taper` from the full-query BM25 activation prior: one stage, two cycles
per channel, full context throughout. Identical to D6 condition B.

### M2 — multi-soft with naive carry **(pathology control)**

Stage 1: one cycle per channel under the partial cue, from the cue prior.
Stage 2: one cycle per channel under full context, **carrying stage 1's complete
activation state as the stage-2 prior**.

This is the transition mode D6 showed to be damaging. It is present to confirm the
pathology reproduces under matched compute, not to be beaten.

### M3 — multi-soft with controlled reset and retained narrowing **(primary treatment)**

Stage 1: one cycle per channel under the partial cue, from the cue prior.
Transition: **activation is reset to the original full-query BM25 retrieval prior, while
stage 1's active set is retained.**
Stage 2: one cycle per channel under full context, restricted to the retained active set.

This is the only condition in which early context is allowed to contribute *compute
narrowing* without contributing *ranking state*. It is the mechanism multiple stages must
justify: early partial context decides where later full context is allowed to look.

### M4 — multi-soft with full reset **(wasted-stage sanity control)**

As M3, but the active set is reset at the transition as well as the activation. Stage 1
then contributes nothing to stage 2, so M4 is definitionally a half-budget M1.

M4 exists to make the accounting explicit. It is expected to lose. Its losing is not
evidence for anything.

### M5 — reversed stage order **(order control)**

As M3, but the stage contexts are reversed: stage 1 uses full context, stage 2 uses the
partial cue.

If M5 is statistically indistinguishable from M3, the ordering of contextual information
carries no value and the progressive-context claim is unsupported even if M3 beats M1.

### M6 — matched-compute hard staged pruning **(reversibility control)**

As M3, but the transition hard-prunes the field to `RECURRENCE_WIDTH` candidates instead
of softly retaining the narrowed active set. Pruned candidates are removed, not damped.

## Primary metric and comparison

```text
metric:               mean nDCG@10
evaluation set:       transition-evaluable development queries only
primary comparison:   M3 - M1
```

Paired query-level uncertainty uses the existing frozen procedure:

```text
paired_bootstrap, BOOTSTRAP_RESAMPLES = 1000, BOOTSTRAP_SEED = 90210
```

Report mean delta and 95% paired bootstrap interval.

## Frozen interpretation

Let `delta = M3 - M1`, `ci_low` its 95% lower bound, `E(x)` the mean feature evaluations
per query for condition `x`, and `n` the number of transition-evaluable queries.

### MULTI_STAGE_SUPPORTED

Only if **all** hold:

```text
n >= 30
delta >= 0.010
ci_low > 0
E(M3) <= 1.10 * E(M1)
```

### MULTI_STAGE_IMMATERIAL

```text
n >= 30
ci_low > 0
delta < 0.010
E(M3) <= 1.10 * E(M1)
```

A real but sub-threshold effect does **not** earn multiple stages a permanent role in
Ground 0. It is recorded as a measured but immaterial effect.

### MULTI_STAGE_NOT_SUPPORTED

```text
n >= 30
delta <= 0  OR  ci_low <= 0
```

Multiple contextual settling stages are removed from Ground 0 as a required mechanism.

### COMPUTE_UNMATCHED

```text
E(M3) > 1.10 * E(M1)  AND  delta > 0
```

The comparison cannot support multiple stages. A negative result under an *inflated* M3
budget still counts as `MULTI_STAGE_NOT_SUPPORTED`, because extra compute cannot excuse a
loss.

### INCONCLUSIVE

```text
n < 30
```

## Secondary comparisons — reported, never promoted

Report paired deltas and intervals for `M3 - M2`, `M3 - M4`, `M3 - M5`, `M3 - M6`, and
`M1 - M0`, under these frozen reading rules:

```text
M3 > M2   reproduces the D6 pathology under matched compute.
          It is NOT evidence that staging beats single-stage settling.

M3 > M6   is evidence about reversibility (soft narrowing vs hard pruning).
          It is NOT evidence that multiple stages are necessary.

M3 ~ M5   means stage ordering carries no information.
          Report the progressive-context claim as unsupported even if M3 > M1.

M3 ~ M4   means retained narrowing contributed nothing, and any M3 advantage
          came from the shorter effective budget rather than from staging.

M1 > M0   confirms the taper preserves the retrieval anchor. It licenses nothing else.
```

No secondary comparison may be substituted for the primary comparison after results are
seen.

## Integrity requirements

MT-1 is invalid if any of the following occur:

- any reserved final-split query is loaded or evaluated;
- qrels, relevance labels, or correct identities influence candidate construction, active
  sets, transitions, pruning, stage order, or the compute budget;
- recurrence is invoked in any condition;
- channels, learned parameters, candidate depth, temperature, dormant floor, relative
  gate, or minimum active width differ across conditions;
- the primary threshold, compute tolerance, or comparison is changed after any result is
  observed;
- Token Deck / TD-3 output enters any condition;
- synthetic smoke output is described as evidence.

## Required raw output

```text
development query count
transition-evaluable query count
per-condition mean nDCG@10 on all development queries (M0, M1)
per-condition mean nDCG@10 on the paired transition-evaluable set (M0-M6)
paired deltas + 95% CI: M3-M1, M3-M2, M3-M4, M3-M5, M3-M6, M1-M0
per-condition mean feature evaluations
per-condition mean feature microseconds
E(M3) / E(M1) compute ratio
per-query outcomes for every condition
frozen classification
```

Per-query outcomes must be preserved so unexpected behaviour can be inspected rather than
averaged away.

## Amendment policy

Any change to conditions, metric, threshold, compute rule, or data boundary must be
recorded as an explicit versioned amendment (`MT-1.1`, `MT-1.2`, ...) **before** any
further result is observed, with the reason stated. Amending this document after seeing a
result to make the outcome favourable invalidates the experiment.

## Scientific boundary

MT-1 can determine whether multiple soft contextual settling stages earn a role on the
SciFact development partition under matched compute. It cannot establish held-out
superiority, recurrence value, natural-language understanding, biological equivalence, or
superiority to modern dense or late-interaction retrieval.
