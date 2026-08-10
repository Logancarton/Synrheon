# MT-1.1 Preregistration — Equal-Budget Multi-Stage Settling Falsification

**Synrheon Ground 0**
**Status: DRAFT — awaiting explicit approval before freezing**
**Replaces:** `docs/MT1_PREREGISTRATION.md` (v1, `UNEXECUTED / DESIGN-INVALID`)
**Audit:** `docs/MT1_DESIGN_AUDIT.md`

No SciFact development nDCG result has been computed or inspected. The development split is
untouched and available to this experiment.

## Question

> Under an explicitly equal computational budget, does allocating part of the budget to an
> earlier partial-context settling/narrowing stage improve final retrieval quality compared
> with spending the same total budget on one full-context settling stage?

## What changed from v1, and why

v1 equalised *nominal sweeps* and then used measured cost as an admissibility gate. That
made `MULTI_STAGE_SUPPORTED` structurally unreachable. MT-1.1 makes equal compute a
**construction constraint** rather than an admissibility test: every result-bearing
condition receives the same hard per-query evaluation budget and may not exceed it.

Everything that was not the defect is carried over unchanged.

```text
CHANGED     compute rule: nominal sweeps + tolerance gate  ->  hard shared evaluation budget
UNCHANGED   material delta 0.010
UNCHANGED   paired bootstrap, 1000 resamples, seed 90210
UNCHANGED   minimum 30 transition-evaluable queries
UNCHANGED   primary metric mean nDCG@10
UNCHANGED   data boundary, channels, candidate field, learned parameters
UNCHANGED   no recurrence, no Token Deck input, no final split
```

The thresholds are deliberately not touched. They were not the defect, and moving them
here would be indistinguishable from threshold movement.

## Falsifier

If equal-budget multi-stage settling does not materially beat single-stage settling,
**multiple contextual settling stages are removed from Ground 0 as a required mechanism**,
and one full-context soft settling stage becomes the default architecture.

A negative MT-1.1 shrinks the architecture. It does not trigger threshold revision, and it
must not trigger changes to production cognition intended to make a re-run succeed.

## Frozen scope and data boundary

```text
dataset                      SciFact, development partition only
development queries          exactly 93 (reject otherwise)
candidate field              existing BM25 top-100 (CANDIDATE_DEPTH = 100)
channels                     existing four (CHANNEL_NAMES), unchanged
learned parameters           existing learn_parameters on development, shared by all conditions
recurrence                   forbidden
Token Deck output            forbidden in every condition
new channels / features      forbidden
reserved final split         must not be loaded, scored, or inspected
minimum transition queries   30
branch                       experiment/external-retrieval-cascade
```

## Compute budget — the core of this design

The compute unit is one **candidate x channel feature evaluation**, counted by the existing
`FeatureMeter`. Nominal sweep counts are not used for matching.

### Per-query budget

```text
B(q) = feature evaluations consumed by the frozen reference single-stage taper on q
     = cost of soft_taper(q, ...) with its existing TAPER_STAGE_CYCLES
```

`B(q)` is defined by the frozen reference implementation that D6 used as its condition B.
It is answer-independent: it depends only on the query, the candidate field, the learned
parameters, and the gate schedule. No qrel, relevance label, or outcome influences it.

### Budget enforcement

Every result-bearing condition runs under a budget-aware meter:

```text
before each channel cycle:
    if remaining_budget < |active set|:
        stop the stage
    else:
        spend |active set| evaluations and continue
```

The rule is deterministic and answer-independent. A condition that exhausts its budget
mid-schedule stops; it is never granted an overdraft.

### Budget allocation

```text
M1   may spend the entire B(q) on full-context settling
M3   spends at most floor(0.5 * B(q)) on the partial-context stage, including the cost of
     constructing the partial-cue prior, then at most the remainder on full-context settling
```

The 0.5 split is preregistered, not tuned. It is the symmetric default. Alternative splits
may be reported as exploratory with **no success criteria attached**, in the way D6 treated
its condition E.

Charging the partial-cue prior against the staged budget is the specific correction for the
v1 defect: in v1 that pass was free to the treatment and cost about 67% of the baseline's
entire budget.

## Conditions

All conditions rank the same frozen BM25 top-100 field for the same query with the same
learned parameters.

### M0 — retrieval anchor

BM25 top-100 order. No taper. Zero feature evaluations.

### M1 — single full-context settling **(primary baseline)**

Full context throughout, one stage, spending up to `B(q)`. By construction this is the
frozen reference taper, so `E(M1) = B(q)` exactly.

### M3 — equal-budget two-stage settling **(primary treatment)**

Stage 1: partial cue (`_reopen_cue`, first half of query tokens, requires >= 4 tokens),
starting from the cue prior, spending at most `floor(0.5 * B(q))` including prior
construction.
Transition: activation is reset to the full-query BM25 retrieval prior; stage 1's active
set is retained as a ceiling.
Stage 2: full context, restricted to the retained ceiling, spending at most the remaining
budget.

`E(M3) <= B(q) = E(M1)` by construction.

### M2 — equal-budget two-stage with naive carry **(pathology control)**

As M3, but stage 1's complete activation state is carried as the stage-2 prior and no
ceiling is applied. This is the transition mode D6 showed to be damaging. It is present to
confirm the pathology reproduces under a genuinely equal budget, not to be beaten.

### M4 — equal-budget two-stage with full reset **(wasted-stage control)**

As M3, but the active set is reset at the transition as well as the activation, so stage 1
contributes nothing to stage 2. M4 isolates how much of any M3 effect comes from retained
narrowing rather than from a shortened effective budget.

### M5 — reversed stage order **(order control)**

As M3, but stage 1 uses full context and stage 2 uses the partial cue. If M5 is
statistically indistinguishable from M3, the ordering of contextual information carries no
value even if M3 beats M1.

### M6 — equal-budget hard staged pruning **(reversibility control)**

As M3, but the transition hard-prunes the field to `RECURRENCE_WIDTH` candidates instead of
softly retaining the narrowed active set. Pruned candidates are removed, not damped, and
cannot be recovered by later evidence. Same budget rule.

This keeps reversibility separable from staging value. It does not substitute for the
primary comparison.

## Primary metric and comparison

```text
metric               mean nDCG@10
evaluation set       transition-evaluable development queries only
primary comparison   M3 - M1
uncertainty          paired_bootstrap, BOOTSTRAP_RESAMPLES = 1000, BOOTSTRAP_SEED = 90210
```

Queries with fewer than four tokens admit no partial cue. They are reported and included in
single-stage summary metrics, but excluded from all paired multi-stage comparisons.

## Frozen interpretation

Let `delta = M3 - M1`, `ci_low` its 95% lower bound, and `n` the number of
transition-evaluable queries.

### MULTI_STAGE_SUPPORTED

```text
n >= 30
delta >= 0.010
ci_low > 0
budget control intact
```

### MULTI_STAGE_IMMATERIAL

```text
n >= 30
ci_low > 0
delta < 0.010
budget control intact
```

A real but sub-threshold effect does not earn multiple stages a permanent role in Ground 0.

### MULTI_STAGE_NOT_SUPPORTED

```text
n >= 30
delta <= 0  OR  ci_low <= 0
```

Multiple contextual settling stages are removed from Ground 0 as a required mechanism.

### INCONCLUSIVE

```text
n < 30
```

### INVALID_BUDGET_CONTROL

```text
any condition exceeded its per-query budget
OR  E(M1) != B(q) on any query
OR  E(M3) > E(M1) on any query
```

An integrity failure, not a scientific outcome. The run is void and must be repaired before
reinterpretation.

**All five classifications are reachable by construction.** `E(M3) <= E(M1)` always holds,
so the budget rule can never block a positive result — which is exactly what v1 got wrong.

## Secondary comparisons — reported, never promoted

Report paired deltas and intervals for `M3 - M2`, `M3 - M4`, `M3 - M5`, `M3 - M6`, and
`M1 - M0`, under these frozen reading rules:

```text
M3 > M2   reproduces the D6 pathology under an equal budget.
          NOT evidence that staging beats single-stage settling.

M3 > M6   is evidence about reversibility, soft narrowing vs hard pruning.
          NOT evidence that multiple stages are necessary.

M3 ~ M5   stage ordering carries no information. Report the progressive-context
          claim as unsupported even if M3 > M1.

M3 ~ M4   retained narrowing contributed nothing, and any M3 advantage came from
          the shortened effective budget rather than from staging.

M1 > M0   confirms the taper preserves the retrieval anchor. Licenses nothing else.
```

No secondary comparison may be substituted for the primary comparison after results are
seen.

## Integrity requirements

MT-1.1 is invalid if any of the following occur:

- any reserved final-split query is loaded or evaluated;
- qrels, relevance labels, or correct identities influence candidate construction, active
  sets, transitions, pruning, stage order, the budget, or the stopping rule;
- recurrence is invoked in any condition;
- Token Deck / TD-3 / TD-4 output enters any condition;
- channels, learned parameters, candidate depth, temperature, dormant floor, relative gate,
  or minimum active width differ across conditions;
- any condition exceeds its per-query budget;
- the primary threshold, budget rule, split fraction, or comparison is changed after any
  result is observed;
- synthetic smoke output is described as evidence.

## Required raw output

```text
development query count
transition-evaluable query count
per-condition mean nDCG@10 on all development queries (M0, M1)
per-condition mean nDCG@10 on the paired transition-evaluable set (M0-M6)
paired deltas + 95% CI: M3-M1, M3-M2, M3-M4, M3-M5, M3-M6, M1-M0
per-query budget B(q)
per-condition mean and maximum feature evaluations
per-condition budget-exhaustion rate and mean stages completed
per-condition mean feature microseconds
per-query outcomes for every condition
frozen classification
```

Per-query outcomes must be preserved so unexpected behaviour can be inspected rather than
averaged away.

## Amendment policy

Any change to conditions, metric, threshold, budget rule, split fraction, or data boundary
must be recorded as an explicit versioned amendment (`MT-1.2`, ...) **before** any further
result is observed, with the reason stated. Amending after seeing a result to make the
outcome favourable invalidates the experiment.

## Scientific boundary

MT-1.1 can determine whether equal-budget multi-stage settling earns a role on the SciFact
development partition. It cannot establish held-out superiority, recurrence value, natural
language understanding, biological equivalence, or superiority to modern dense or
late-interaction retrieval.

## Open questions before freezing

These are flagged rather than silently resolved. They need a decision before this document
is frozen.

1. **The 0.5 split is a free parameter.** It is the symmetric default and is not tuned, but
   nothing establishes it as the right allocation. Alternatives: freeze 0.5 as primary and
   report others as exploratory without success criteria (current draft); or preregister a
   small fixed ladder such as {0.25, 0.5} with a Bonferroni-style correction; or derive the
   split from the frozen gate schedule rather than choosing it.

2. **The audit found the treatment's mechanism may be redundant.** M1 collapses to its
   active-set floor inside channel 0, so early narrowing is something the baseline already
   does more aggressively. Equal budget fixes the accounting defect, but it does not by
   itself give staging a mechanism the baseline lacks. MT-1.1 may therefore be a
   well-formed test of a mechanism that has no route to winning. Worth deciding whether
   that is acceptable — a clean negative is still a legitimate architectural simplification
   — or whether the treatment should first be given a genuinely differentiating mechanism,
   such as per-stage channel subsets, which would be a different experiment.

3. **`B(q)` is defined by the reference taper, so M1 is the budget.** That makes M1 exactly
   `B(q)` and M3 strictly bounded by it. This is deliberate and keeps SUPPORTED reachable,
   but it does mean the baseline can never be budget-starved while the treatment can be.
   The alternative — a fixed constant budget for all queries — would starve the baseline on
   large fields and is not obviously fairer.
