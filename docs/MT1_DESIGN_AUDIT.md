# MT-1 v1 Design Audit — pre-result implementation audit

**Status: `UNEXECUTED / DESIGN-INVALID`**
**Not scientifically failed. The experiment was never run on evidence data.**

Frozen design under audit:

```text
docs/MT1_PREREGISTRATION.md          retained unedited as frozen historical design evidence
experiments/mt1_matched_compute_multitaper.py   v1 implementation, guarded against evidence runs
```

The v1 preregistration was **not** amended to rescue its treatment condition. It stands as
the record of what was frozen and what the audit found wrong with it.

## What the audit found

MT-1 v1 asked whether multi-stage settling helps under matched compute, and made matched
compute an *admissibility rule* rather than a construction constraint:

```text
stated question              does multi-stage settling help under matched compute?
frozen admissibility rule    E(M3) <= 1.10 * E(M1)   (required for MULTI_STAGE_SUPPORTED)
measured engineering cost    E(M3) ~= 2.285 * E(M1)
```

The implemented treatment therefore could not satisfy the experiment's own matched-compute
condition. Under the frozen classifier, `MULTI_STAGE_SUPPORTED` was **structurally
unreachable**: the only attainable outcomes were `MULTI_STAGE_NOT_SUPPORTED`,
`COMPUTE_UNMATCHED`, and `INCONCLUSIVE`.

An experiment that cannot return one of its own headline classifications is not a test of
its stated question.

## Measured cost, SciFact development, 92 transition-evaluable queries

Feature-evaluation cost only. No ranking was produced and no nDCG was computed.

```text
mean candidate x channel feature evaluations per query

  M1  single full-context soft      148.5    ratio 1.000
  M2  multi, naive carry            413.1    ratio 2.783
  M3  multi, reset + narrowing      339.2    ratio 2.285   <- treatment
  M4  multi, full reset             413.1    ratio 2.783
  M5  reversed stage order          297.5    ratio 2.004
  M6  hard staged pruning           327.9    ratio 2.209

  frozen tolerance                             1.10
```

## Root causes

Two independent structural defects, both in the compute model rather than in the code:

### 1. The nominal budget was not the real budget

v1 equalised *nominal channel-cycle sweeps* (eight per condition) and then measured actual
cost. Nominal equality does not produce cost equality, because the active-set gate narrows
at different points in each schedule. The v1 document anticipated this and chose to measure
and gate rather than to constrain construction — which is precisely what made one
classification unreachable.

### 2. The baseline already performs the treatment's mechanism, more aggressively

M3's intended contribution was early narrowing that reduces later compute. The baseline
obtains that narrowing for free inside its own first channel:

```text
candidate field width                       100.0
M1 active width per channel        [16.3, 16.1, 16.1, 16.1]
M3 stage-1 ceiling handed to stage 2        27.2
```

M1 collapses to its floor inside channel 0 and stays there. The "retained narrowing" M3
hands to its second stage is **wider** than the active set M1 uses internally (27.2 vs
16.3). Staging therefore adds a partial-cue prior pass (100.0 evaluations, about 67% of
M1's entire budget) and a redundant narrowing pass, and hands the second stage a wider
field than the baseline uses.

The treatment is not merely disadvantaged on cost accounting. Its mechanism is redundant
with the baseline.

## Evidence boundary — development split untouched

```text
development nDCG computed        NO
development nDCG inspected       NO
ranking produced on development  NO
reserved final split loaded      NO
```

Precise statement: the audit called `learn_parameters`, which internally reads development
qrels to fit channel gains. That is the protocol-sanctioned learning step, identical to the
one D6 used, and it produces channel gains rather than an outcome. No `ndcg_at_k` call was
made on development data, no ranking was scored, and no development result was displayed.

The SciFact development partition therefore remains available to the replacement
experiment, and the reserved final split was never loaded.

## Non-evidentiary engineering information

A synthetic smoke run (`make_hard_corpus`, explicitly not evidence) produced identical
nDCG for M3 and M4, suggesting that retained narrowing may not change the top of the
ranking. This is recorded as engineering information only.

It was **not** used to design, tune, or select any part of the replacement experiment. It
did not use protected development-result inspection.

## What was deliberately not done

To keep the replacement design honest, none of the following were performed:

```text
raising the 1.10 tolerance
excluding cue-prior cost to make M3 admissible
tuning treatment details against the smoke-run M3/M4 comparison
inspecting development outcomes before a replacement design was frozen
editing the v1 preregistration to make the treatment fit
```

Selecting a new rule because it is favourable to the treatment is the same failure mode as
moving a threshold after seeing a result.

## Replacement

```text
docs/CPN1_PREREGISTRATION.md
```

CPN-1 replaces admissibility-by-tolerance with an **explicit hard per-query evaluation
budget**, so equal compute is enforced by construction and every classification stays
reachable. A first MT-1.1 draft was withdrawn before freezing: its 0.5 stage split was
mechanically impossible on 92/92 queries, because the separate cue-prior pass costs 100
evaluations against a maximum allowance of 79. The frozen replacement removes that pass
entirely and narrows the claim to contextual pre-narrowing.

The v1 decision thresholds are carried into CPN-1 unchanged — material delta 0.010, 95%
paired bootstrap with 1000 resamples at seed 90210, minimum 30 transition-evaluable
queries — because they were not the defect. Changing them here would be indistinguishable
from threshold movement.
