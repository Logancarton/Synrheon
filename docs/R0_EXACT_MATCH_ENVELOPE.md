# R0-SR1D — Exact-Match Operating Envelope

**Synrheon relational cognition track**  
**Status: frozen diagnostic extension after R0-SR1 instrument validation, before vector/similarity work**

## Question

Now that the single-route exact-match instrument is valid, where does exact symbolic overlap succeed, degrade, and fail under controlled cue ambiguity and corruption?

This diagnostic does not change `R0_SINGLE_ROUTE_PREREGISTRATION.md` and does not reinterpret R0-SR1. It reuses the validated family-A world and frozen exact-overlap retriever without changing its scoring rule.

## Why this comes before vectors

A vector/similarity mechanism should only be introduced for failures that exact structure cannot solve. Before adding that complexity, map the operating envelope of exact matching itself.

The diagnostic distinguishes three kinds of perturbation:

```text
irrelevant unbound noise       concept is bound to no memory in the tested route
competitive bound noise        concept exactly belongs to another memory/group
identity corruption            concept is intended as an alias/near form but is not the same ID
```

Those perturbations should not be conflated.

## Frozen mechanism

Use the already validated R0-SR1 family-A world and `SingleRouteRetriever` unchanged:

```text
memories:              128
route group sizes:      8, 16, 32, 64
route identity:         oracle-isolated, one route at a time
matching:               exact concept ID only
similarity:             none
learning:               none
vectors:                none
multi-route merge:      none
```

The scoring rule remains exactly the R0-SR1 overlap rule. This diagnostic may vary the candidate-field size and cue construction, but may not alter the retriever.

## Diagnostic axes

### A. Field-size × ambiguity sweep

For each route group size `G in {8,16,32,64}`, evaluate anchor-only partial cues at field sizes:

```text
F in {4, 8, 16, 32, 64}
```

Expected aggregate target access:

```text
Hit@F = min(1, F / G)
```

This maps the exact capacity boundary directly.

### B. Detail-only exact cue

Use only the target memory's unique detail concept.

Expected:

```text
Top1 = 1.00
Hit@F = 1.00 for every F >= 1
```

This establishes that exact matching is excellent when a unique exact identifier survives.

### C. Unbound-noise load

Use the correct anchor plus `n` concepts that occur nowhere in the tested route, for:

```text
n in {1, 4, 16, 64}
```

Because all candidates share the same cue denominator and unbound concepts match no candidate, ranking should be identical to the anchor-only partial cue.

Expected:

```text
Hit@32(unbound noise n) = Hit@32(anchor only)
```

This is a useful success boundary: irrelevant unknown noise should scale scores but not reorder candidates.

### D. Same-group conflicting detail

Use the target anchor plus the unique detail belonging to another memory in the same anchor group.

The competitor receives two exact matches while the target receives only the anchor match.

Expected:

```text
competitor rank = 1
subject target Top1 = 0
```

Target Hit@32 remains diagnostic because it depends on group size and tie ordering after the competitor.

This isolates competitive exact evidence: exact matching trusts a wrong exact detail more than an ambiguous correct anchor.

### E. Foreign-group conflicting detail

Use the target anchor plus a detail from a memory in another anchor group.

The target group receives anchor support and the foreign memory receives detail support. Neither receives both.

Expected behavior is competition between two exact sources rather than semantic resolution. Report target Hit@32 and target rank distribution without imposing a supportive threshold.

### F. Identity corruption / near-ID cue

Take the target's unique detail concept ID and deterministically alter one character so that it is not equal to any stored concept ID.

Important: this is **not** a claim that opaque hash strings carry semantic edit distance. It is an instrument demonstration of exact identity discontinuity: one unequal ID is simply unequal.

Expected:

```text
corrupted-detail-only Hit@32 = 32 / 128 = 0.25
```

This is the clean failure boundary that a future alias/similarity mechanism would need to address.

### G. Explicit alias cue

Create a fresh opaque alias token paired only by the experiment with the target detail, but do not add that alias to stored bindings.

Expected:

```text
alias-only Hit@32 = 0.25
```

This proves exact matching cannot infer equivalence that has not been explicitly represented.

## Report

The diagnostic must report:

```text
field-size × ambiguity matrix
exact detail-only Top1/Hit
unbound-noise invariance by noise count
same-group conflict target Top1/Hit and competitor Top1
foreign-group conflict target Hit/rank summary
near-ID Hit
alias-only Hit
```

## Interpretation

Expected exact-match strengths:

- perfect retrieval from surviving unique exact detail;
- mathematically predictable broadening from a shared exact anchor;
- graceful capacity loss as ambiguity exceeds the fixed field;
- immunity to arbitrarily many unbound distractor concepts because they do not reorder candidates;
- strict route isolation.

Expected exact-match failures:

- no recovery from unseen aliases or changed identities;
- no graded similarity for partially corrupted identity;
- no principled resolution when two incompatible but exact pieces of evidence compete;
- ambiguity cannot be reduced without additional exact structure.

These failures do not automatically justify vectors. They identify the cases a next mechanism must beat while preserving the exact mechanism's strengths and hidden-information firewall.

## Advancement rule

Do not add vector similarity merely because near-ID/alias conditions fail; those failures are expected by construction. First confirm the complete operating envelope and preserve it as a regression baseline. A future similarity mechanism must improve a preregistered failure condition without degrading exact full/detail retrieval, route isolation, or chance controls.
