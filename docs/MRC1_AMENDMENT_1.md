# MRC-1 Amendment 1 — Crowded-regime collision strength

**Status:** FROZEN BEFORE IMPLEMENTATION OUTPUT OR BENCHMARK RESULTS

The original preregistration set the crowded-regime vocabulary to 512 concepts. A pre-result analytical check shows that this is too sparse to exercise meaningful three-concept cue collisions over the frozen growth range.

With 6 concepts per memory and a 3-concept exact cue, a rough independent approximation for another memory matching all three cue concepts is `(6/V)^3`. At `V=512` and `N=30,000`, the expected number of accidental three-concept matches remains far below one, so the crowded condition would likely remain at a ceiling and would not test retrieval interference.

Therefore, before implementation output is inspected:

```text
crowded vocabulary size: 512 -> 64
```

At `V=64`, the same rough approximation predicts materially more exact-cue collisions at the larger checkpoints, making degradation possible rather than guaranteed absent.

No success threshold is added. All other MRC-1 conditions, metrics, controls, and interpretation boundaries remain unchanged.
