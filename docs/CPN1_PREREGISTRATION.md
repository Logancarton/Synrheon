# CPN-1 Preregistration — Equal-Budget Contextual Pre-Narrowing

**Synrheon Ground 0**
**Experiment ID:** `cpn-1-equal-budget-contextual-prenarrowing-v1`
**Status: FROZEN before result-bearing implementation**

**Chronology:** occupies the MT-1.1 slot. Supersedes the withdrawn MT-1.1 draft and replaces
MT-1 v1 (`UNEXECUTED / DESIGN-INVALID`, see `docs/MT1_DESIGN_AUDIT.md`). The "multi-taper"
framing is **retired**: this experiment does not test general multi-stage settling.

No SciFact development ranking or nDCG result has been computed or inspected. The
development split is untouched.

## Question

> Does spending the one affordable broad feature pass under partial context, using that
> pass to create a reversible active ceiling, and then spending the remaining channel
> computation under full context, improve retrieval quality relative to the same frozen
> channel schedule performed entirely under full context?

## Falsifier, and its deliberate narrowness

A negative result means:

> **Contextual pre-narrowing is not supported as a required Ground 0 mechanism under this
> task and compute model.**

It must **not** be read as:

> ~~Multiple contextual stages or iterative settling in general are disproven.~~

A general multi-stage / iterative-settling question stays open and separate. It may only be
tested once a computationally legitimate mechanism exists for it — one that does not require
re-evaluating the broad field under a second context, which this compute model cannot
afford. Do not reuse a CPN-1 negative to close that question.

## Why the scope narrowed

The audit of MT-1 v1 established that the candidate field admits exactly **one** affordable
broad feature pass. Re-evaluating the field under a second context costs about 67% of the
entire baseline budget on its own. Any honest equal-budget design therefore cannot run two
broad contextual passes, so "multiple settling stages" is not testable here. What *is*
testable is where the single broad pass is spent.

This experiment has one broad pass and one narrowed pass, exactly as the baseline does. The
manipulation is which context each pass uses.

## Frozen scope and data boundary

```text
dataset                      SciFact, development partition only
development queries          exactly 93 (reject otherwise)
candidate field              existing BM25 top-100 (CANDIDATE_DEPTH = 100)
channel order                frozen learned order (1, 2, 0, 3)
channel gains                existing learn_parameters on development, shared by all conditions
stage dynamics               existing TAPER_STAGE_CYCLES = 2, unchanged
recurrence                   forbidden
Token Deck output            forbidden in every condition
new channels / features      forbidden
reserved final split         must not be loaded, scored, or inspected
minimum transition queries   30
branch                       experiment/external-retrieval-cascade
```

## Compute rule

### Primary hard constraint

```text
unique FeatureMeter.evaluations
```

This counts actual `ChannelBank.compute()` executions and therefore captures the major cost
introduced by changing context. It is the only pass/fail compute gate.

```text
B(q) = evaluations consumed by the frozen reference single-stage taper on q
       (soft_taper with its existing TAPER_STAGE_CYCLES; this is D6 condition B)

required, per query, for every tapered condition:   evaluations <= B(q)
```

**No overdraft.** Before each channel cycle a condition counts how many of its active
candidates would miss the feature cache for that `(doc, channel, context)`. If spending them
would exceed `B(q)`, the stage stops. The rule is deterministic and answer-independent: no
qrel, label, or outcome influences it.

### Secondary compute diagnostics

Reported, **never** hypothesis pass/fail gates unless an independent pre-result reason
establishes a threshold:

```text
FeatureMeter.requests
activation-update count
normalization work
per-channel evaluations
feature nanoseconds
wall-clock if useful
```

Requests are explicitly *not* a gate. Within a fixed context the second cycle of a channel is
entirely cache hits, so requests charge work that is not performed; gating on them would
credit the baseline with cost it does not pay.

### Why evaluations, and what asymmetry that encodes

Under a fixed context a feature value is constant, so repeated cycles evolve the activation
state at no feature cost — the update reads the current activation, which changed after the
previous normalization. Every new context invalidates the cache. Charging by evaluations
therefore encodes a real algorithmic property: **single-context settling is cheap to iterate;
changing context is not.** That is the honest cost of the manipulation under test.

## Conditions

All conditions rank the same frozen BM25 top-100 field with the same learned parameters and
the same stage dynamics.

### A0 — retrieval anchor

BM25 top-100 order. No taper. Zero feature evaluations.

### A1 — full-context baseline **(primary baseline; defines B(q))**

Frozen channel order `(1, 2, 0, 3)`, all channels under full context, two-cycle dynamics.
Channel 1 pays the broad pass over the field; the gate narrows; channels 2, 0, 3 run on the
narrowed set. `E(A1) = B(q)` by construction.

### T — contextual pre-narrowing **(primary treatment)**

```text
stage 1     channel 1 under the PARTIAL CUE across the broad field, two-cycle dynamics
            the resulting active set becomes a reversible ceiling
transition  reset ranking activation to the full-query BM25 prior
            retain the active ceiling only
stage 2     channels 2, 0, 3 under FULL context, restricted to the ceiling
            stop before any operation that would exceed B(q)
```

There is **no separate `_cue_prior()` pass.** The first partial-context channel pass *is* the
contextual pre-narrowing operation. Eliminating that surcharge is what makes the treatment
affordable, and it is the specific correction for the MT-1 v1 defect.

Partial cue is the existing frozen `_reopen_cue`: the first half of query tokens, requiring at
least four tokens.

### C-carry — transition-mode control **(D6 pathology)**

Identical to T except the transition **carries** stage 1's activation instead of resetting it.
The ceiling is retained in both, so this varies only the transition mode. This is a stricter
isolation of the D6 pathology than MT-1 v1 achieved, which confounded transition mode with
narrowing.

### C-reversed — context-placement control

Stage 1 is channel 1 under **full** context; stage 2 is channels 2, 0, 3 under the **partial
cue**, restricted to the resulting ceiling. If C-reversed is indistinguishable from T, the
placement of partial context carries no value even if T beats A1.

### C-hard — reversibility control

Identical to T except the transition **hard-prunes** the field to `RECURRENCE_WIDTH`
candidates. Pruned candidates are removed, not damped, and cannot be recovered. Same
evaluation budget and same accounting.

### Condition deliberately excluded, and why

A "staging without a retained ceiling" ablation is **not runnable** under equal compute.
Verified mechanically: with stage 1 spending the broad pass, the remaining budget is about 48
evaluations, while an unnarrowed full-context channel pass needs about 100. Stage 2 is
truncated on 100% of queries and never executes.

This is itself a structural finding worth recording: **the reversible ceiling is not an
optional design choice, it is the precondition that makes staging affordable at all.** Carrying
a condition that cannot execute would repeat the MT-1 v1 error, so it is excluded rather than
frozen as a dead arm.

## The experimental manipulation, stated plainly

```text
A1  receives channel 1 under FULL context
T   receives channel 1 under PARTIAL context instead
```

Both then spend the remainder of the same budget on channels 2, 0, 3 under full context. That
information trade is the entire manipulation. T is not given extra compute, extra channels, or
extra cycles.

## Pre-freeze mechanical verification

Cost accounting only. No ranking produced, no nDCG computed, no qrels consulted.

```text
                                   min     median    mean      max
B(q) frozen A1 evaluations       148.0     148.0    148.5    158.0
T evaluations                    134.0     148.0    147.9    158.0
C-hard evaluations               148.0     148.0    148.0    148.0
C-carry evaluations                                 147.8
C-reversed evaluations                              148.4
stage-1 ceiling width             16.0      16.0     16.6     48.0

T never exceeds B(q)                     PASS    overruns 0/92
stage 1 fully executable                 PASS    92/92
C-hard obeys same accounting             PASS    overruns 0/92
compute gate cannot block support        PASS    max(E(T) - B(q)) = 0
E(T)/B(q)                                0.9965
E(C-hard)/B(q)                           0.9970
```

T completes a mean of 3.96 of 4 channel passes. Its stage 2 is truncated on **3 of 92
queries (3.3%)**, and C-carry on the same 3. This is reported as a known cost of equal
budget. **The budget must not be enlarged to rescue it.**

## Primary metric and comparison

```text
metric               mean nDCG@10
evaluation set       transition-evaluable development queries only
primary comparison   T - A1
uncertainty          paired_bootstrap, BOOTSTRAP_RESAMPLES = 1000, BOOTSTRAP_SEED = 90210
```

Queries with fewer than four tokens admit no partial cue. They are reported and included in
A0/A1 summary metrics but excluded from all paired comparisons.

## Frozen interpretation

Let `delta = T - A1`, `ci_low` its 95% lower bound, `n` the transition-evaluable count.

### CONTEXTUAL_PRENARROWING_SUPPORTED

```text
n >= 30
delta >= 0.010
ci_low > 0
budget control intact
```

### CONTEXTUAL_PRENARROWING_IMMATERIAL

```text
n >= 30
ci_low > 0
delta < 0.010
budget control intact
```

A real but sub-threshold effect does not earn the mechanism a permanent Ground 0 role.

### CONTEXTUAL_PRENARROWING_NOT_SUPPORTED

```text
n >= 30
delta <= 0  OR  ci_low <= 0
```

Contextual pre-narrowing is removed as a required Ground 0 mechanism. This does **not**
close the general iterative-settling question.

### INCONCLUSIVE

```text
n < 30
```

### INVALID_BUDGET_CONTROL

```text
any condition exceeded B(q) on any query
OR  E(A1) != B(q) on any query
```

Integrity failure, not a scientific outcome. The run is void until repaired.

All five classifications are reachable: `E(T) <= B(q) = E(A1)` holds by construction and was
verified with zero overruns, so the compute gate can never block a positive result.

The 0.010 materiality threshold and the bootstrap procedure are carried over unchanged from
MT-1 v1. They were not the defect, and no independent mathematical reason to alter them was
identified.

## Secondary comparisons — reported, never promoted

```text
T - C-carry     reproduces the D6 pathology with narrowing held constant.
                NOT evidence that pre-narrowing beats the full-context baseline.

T - C-hard      evidence about reversibility, soft ceiling vs hard pruning.
                NOT evidence that pre-narrowing is necessary.

T - C-reversed  if indistinguishable, the placement of partial context carries no
                value; report the pre-narrowing claim as unsupported even if T > A1.

A1 - A0         confirms the taper preserves the retrieval anchor. Licenses nothing else.
```

No secondary comparison may be substituted for the primary comparison after results are seen.

## Integrity requirements

Invalid if any of the following occur:

- any reserved final-split query is loaded or evaluated;
- qrels, relevance labels, or correct identities influence candidate construction, active
  sets, the ceiling, transitions, pruning, channel order, the budget, or the stopping rule;
- recurrence is invoked;
- Token Deck / TD-3 / TD-4 output enters any condition;
- channel order, gains, candidate depth, temperature, dormant floor, relative gate, minimum
  active width, or stage cycles differ across conditions;
- any condition exceeds `B(q)`;
- the budget is enlarged to reduce truncation;
- the threshold, budget rule, conditions, or comparison change after any result is observed;
- synthetic smoke output is described as evidence.

## Required raw output

```text
development query count
transition-evaluable query count
per-condition mean nDCG@10 on all development queries (A0, A1)
per-condition mean nDCG@10 on the paired transition-evaluable set (all conditions)
paired deltas + 95% CI: T-A1, T-C-carry, T-C-hard, T-C-reversed, A1-A0
per-query B(q)
per-condition mean and maximum evaluations, and overrun count
per-condition truncation rate and mean channel passes completed
secondary diagnostics: requests, activation updates, normalization work,
    per-channel evaluations, feature nanoseconds
per-query outcomes for every condition
frozen classification
```

Per-query outcomes must be preserved so unexpected behaviour can be inspected rather than
averaged away.

## Amendment policy

Any change to conditions, metric, threshold, budget rule, or data boundary must be recorded
as an explicit versioned amendment (`CPN-1.1`, ...) **before** any further result is
observed, with the reason stated. Amending after seeing a result to make the outcome
favourable invalidates the experiment.

## Scientific boundary

CPN-1 can determine whether equal-budget contextual pre-narrowing earns a role on the SciFact
development partition under this compute model. It cannot establish held-out superiority,
recurrence value, general multi-stage or iterative-settling value, natural language
understanding, biological equivalence, or superiority to modern dense or late-interaction
retrieval.
