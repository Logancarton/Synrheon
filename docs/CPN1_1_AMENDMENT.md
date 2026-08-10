# CPN-1.1 Pre-Result Clarification Amendment

```text
Status:                                              FROZEN before result-bearing implementation
Parent preregistration:                              docs/CPN1_PREREGISTRATION.md
Parent frozen commit:                                afea37c
Scientific thresholds changed:                       NO
Conditions changed:                                  NO
Primary comparison changed:                          NO
Compute budget changed:                              NO
Development ranking/nDCG inspected before amendment: NO
```

This amendment resolves **four implementation ambiguities only**. It adds no condition,
moves no threshold, and changes no scientific claim. The parent preregistration is preserved
unedited as frozen evidence.

---

## Clarification 1 — exact starting state

All CPN-1 conditions begin from the same candidate retrieval:

```text
candidates = full-query BM25 top-100
```

**Candidate retrieval is never performed from the partial cue.**

For `A1`, `T`, `C-carry`, `C-reversed`, and `C-hard` the initial ranking activation is:

```text
full_query_prior = _initial_activation(candidates)
```

derived from the full-query BM25 candidate scores. It is **not** `_cue_prior(...)`, not a
partial-query BM25 retrieval, not a second BM25 retrieval, and not an independently computed
partial-context prior.

For `T` specifically:

```text
Stage 1 starts from full_query_prior.

The PARTIAL CUE affects only the feature context supplied to channel 1's
FeatureMeter.value(...) calls.
```

The manipulation is therefore exactly:

```text
same candidates
same starting BM25 activation
different context for channel 1 feature computation
```

Frozen statement:

> **No `_cue_prior()` call exists anywhere in CPN-1.**

The partial cue must not perform a hidden second broad retrieval or hidden prior
construction. `C-carry`, `C-reversed`, and `C-hard` follow the starting-state semantics
required by their frozen comparison and may not introduce a different retrieval prior.

---

## Clarification 2 — reversible ceiling vs hard pruning

After `T` stage 1:

```text
stage1_active = the active set produced by the frozen taper gate
```

At the transition, ranking activation is reset to `full_query_prior`, **but every original
candidate identity remains represented in the activation map.**

The stage-1 active set is an **update ceiling, not a deletion boundary.**

During `T` stage 2:

```text
only candidates inside stage1_active receive new channel feature updates
```

Candidates outside `stage1_active`:

```text
remain represented
remain in the complete activation field
receive no new stage-2 feature update
are dormant / suppressed, not deleted
```

They must not disappear from the state merely because they fall outside the update ceiling.
The final `T` ranking is generated from the **complete candidate activation field**,
including dormant candidates.

This is the exact invariant:

```text
suppressed != deleted
```

The same complete-field semantics apply to `C-carry`.

`C-hard` must be genuinely different. After its stage 1, hard pruning **physically removes**
candidates outside the frozen hard-pruned retained set from the result-bearing activation
field. Those removed candidates receive no later updates, do not appear in the final
ranking, and cannot recover in that trajectory.

```text
T       = reversible suppression, dormant alternatives preserved
C-hard  = destructive removal
```

Tests must fail if `T` and `C-hard` accidentally become equivalent because both discard
outside-ceiling candidates. `RECURRENCE_WIDTH` and every other threshold stay unchanged; the
difference must come from the mechanism, not from a retuned constant.

---

## Clarification 3 — C-reversed cannot override the primary verdict

This supersedes wording in the parent preregistration that implied
`T ~ C-reversed => primary CPN-1 becomes unsupported`.

The **only** primary scientific classifier for CPN-1 is:

```text
T - A1
```

using the already frozen mean nDCG@10, delta threshold 0.010, paired bootstrap, 1000
resamples, seed 90210, minimum n = 30.

`C-reversed` is **secondary mechanistic evidence**. The `T - C-reversed` result must not
change, veto, promote, or replace the formal primary classification.

```text
T - A1 answers:
    Does contextual pre-narrowing earn a Ground 0 role under this task and
    compute model?

T - C-reversed answers:
    Does the evidence demonstrate that the placement/order of partial versus
    full context matters?
```

Report the `T - C-reversed` mean paired delta and its paired 95% bootstrap interval. **Do
not invent a post-hoc threshold for this secondary comparison.**

A valid result may therefore read:

```text
primary CPN-1:            CONTEXTUAL_PRENARROWING_SUPPORTED
context-order specificity: not demonstrated / unresolved by secondary comparison
```

That is not a contradiction. No secondary comparison may replace the frozen `T - A1`
classifier.

---

## Clarification 4 — strict cache isolation

For every query, `A1` receives a newly constructed empty `FeatureMeter(bank)`. That isolated
meter yields:

```text
B(q) = A1.evaluations
```

After `A1` finishes, **only the scalar integer `B(q)`** may be transferred to another
condition. `T`, `C-carry`, `C-reversed`, and `C-hard` each receive their own newly
constructed empty `FeatureMeter(bank)`.

No condition may inherit from any other:

```text
FeatureMeter._cache
requests
evaluations
per_channel counts
nanoseconds
feature values
```

Shared immutable/calibrated objects may remain shared where scientifically legitimate:

```text
candidate field
ChannelBank configuration
BM25 index
LearnedParameters
channel order / gains
```

But **feature cache state must never cross a condition boundary.**

Frozen rule:

> `B(q)` is experimental evaluation machinery. It is a scalar budget derived from the
> separate `A1` control trajectory. Running `A1` is **not** part of `T`'s live cognitive
> operation.

CPN-1 tests equal-cost algorithms experimentally. It does **not** claim that a production
Synrheon instance must first execute `A1` to discover `T`'s runtime budget.

---

## Amendment integrity

This amendment does **not** change:

```text
scientific question
primary T-A1 comparison
0.010 materiality threshold
bootstrap method
bootstrap seed
minimum sample size
candidate field
channel order
channel gains
stage cycles
compute metric
B(q) definition
no-overdraft rule
CPN-1 conditions
data boundary
```

It only removes implementation ambiguity before any result-bearing run.
