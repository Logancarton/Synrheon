# EXT-1 Preregistration — Ground 0 Against External Retrieval Baselines

**Synrheon Experimental Research Program**  
**Frozen before any external final-split evaluation**  
**Date:** August 9, 2026  
**Branch:** `experiment/external-retrieval-cascade`

## 1. Why EXT-1 exists

HCT-1 and HCT-2 were useful synthetic experiments, but they share a limitation that preregistration alone cannot remove: the generator, mechanism, controls, and interpretation were created inside the same research loop.

A post-HCT code review identified six ways HCT-2 could overstate the strength of its conclusions:

1. the correct candidate occupied a privileged position and stable sorting could resolve ties toward it;
2. the synthetic excitation graph included correctness-dependent structure, so recurrence was not fully answer-independent;
3. the generic-soft control recomputed invariant feature values across cycles, inflating the reported context-evaluation advantage;
4. the 3.125% recurrent-load figure was determined by configured widths/cycles rather than measured computational work;
5. channel order was entangled with the synthetic hierarchy/branching structure, so the experiment did not cleanly prove discovery of a semantic hierarchy;
6. some synthetic baselines were much weaker than a strong real-world retrieval baseline.

These findings do not erase the historical HCT results. They change their evidentiary status: HCT-2 remains evidence about behavior inside its own synthetic family, while its stronger recurrence, ordering, and efficiency interpretations are **provisional pending external validation**.

EXT-1 moves the mechanism to a corpus, queries, relevance judgments, and published baseline that Synrheon did not author.

## 2. Independent claims

EXT-1 tests three claims independently. One claim may be reinforced, discounted, or inconclusive without masking the others.

### C1 — Staged narrowing at matched feature budget

Learned ordered reversible tapering should:

- exceed BM25 on nDCG@10 with a paired-bootstrap 95% interval above zero;
- remain within 0.01 nDCG@10 of a fully evaluated cached rerank control;
- use at most 50% of the full rerank's measured feature evaluations;
- show at least a 3% feature-evaluation advantage over the same sparse mechanism in fixed channel order.

### C2 — Reversibility earns its keep

On queries where **both** soft and hard cascades initially suppress every relevant document under the same under-specified cue, the reversible cascade should recover a relevant document into the top 10 at least **10 percentage points** more often than hard deletion, with a paired-bootstrap interval above zero.

At least 30 common suppression cases are required. Fewer than 30 makes **C2 only** inconclusive.

### C3 — Explicit abstention improves calibration

For the learned-order cascade:

- committed-query precision minus forced-commitment precision should be at least 5 percentage points, with a bootstrap interval above zero;
- at least 50% of queries whose BM25 top-100 field contains no relevant document should be abstained on.

Commit rate/coverage is reported alongside precision so abstention cannot be interpreted without its coverage cost.

## 3. External data and anchors

Primary dataset: **BEIR SciFact**.  
Secondary, declared before the primary final run: **BEIR NFCorpus**.

Published BM25 nDCG@10 anchors used as retrieval sanity checks:

```text
SciFact   0.665
NFCorpus  0.325
```

The local BM25 implementation uses the same k1=0.9 and b=0.4 parameters but different tokenization from Anserini/Lucene. It therefore is not expected to reproduce the published values exactly.

Before any downstream EXT-1 result is interpretable, local BM25 must reach at least 90% of the published anchor. An unrecognized dataset name has no anchor and cannot satisfy C1.

If the anchor fails, the correct action is to repair or replace the retrieval baseline and create a new EXT version if the frozen mechanism changes. The anchor threshold must not be lowered after seeing the final result.

## 4. Conditions

Every condition receives the same BM25 top-100 candidate field retrieved from the full query.

```text
1. bm25_only
2. full_rerank
3. hard_cascade
4. fixed_order_taper
5. learned_order_taper
6. learned_order_no_recurrence
7. learned_order_no_reopen
```

All applicable conditions face the same information arrival: first an under-specified cue, then the full query.

The reopening probe deliberately holds the retrieved candidate field fixed. Only starting activation is misled by the first half of the query. This isolates taper/reopening from the retriever. It is therefore a narrower test than a true two-turn retrieval scenario.

## 5. Feature channels

Four hand-designed channels are used:

```text
0 lexical_core
1 rare_term_coverage
2 proximity_window
3 char_ngram_semantic
```

Each condition requests features through its own `FeatureMeter`. The meter caches by `(document id, channel, exact token tuple)`.

A feature is charged only on a cache miss. Re-requesting an invariant across recurrence/settling cycles is free within that condition. Cross-condition cache sharing is impossible.

Both feature-evaluation count and elapsed nanoseconds around cache misses are recorded. **Feature evaluations are the frozen primary compute gate; nanoseconds are reported as a secondary measured-cost calibration because runtime timing is machine/noise dependent.**

## 6. Learned parameters

Only the development split may influence:

- feature normalization/calibration;
- channel gains;
- per-channel measured unit cost;
- learned channel order;
- commitment margin.

Channel order is learned from discriminative utility per unit of measured development cost. It is not read from a branching-factor constant or semantic depth label.

The final split is never used for calibration, stage-order learning, threshold selection, debugging, or partial inspection.

## 7. Firewalls

### Split firewall

Query assignment is deterministic from `sha256(query_id)`: approximately 30% development and 70% final.

`--limit` is development-only. The program refuses partial final runs.

### Information firewall

Relevance judgments are used only for:

1. learning parameters on the development split;
2. post-hoc evaluation/scoring.

Inference does not receive qrels. Candidate relations are derived from document/document rare-term overlap. A regression test empties every qrel and requires the relation field to remain unchanged.

Ties are broken by document id rather than input position.

### Reopening firewall

Soft tapering retains dormant activation and later reopening resumes from that retained state. It does not discard the taper and restart from the front end.

Hard cascade deletes candidates and cannot recreate them.

### Synthetic-evidence firewall

The smoke corpus exists only for code-path tests. `verdict()` must return `NOT EVIDENCE` for every dataset marked synthetic regardless of score.

## 8. Frozen gate

```text
local BM25 nDCG@10 >= 90% of published anchor

C1:
learned-order minus BM25 nDCG@10: point delta >= 0 and CI low > 0
learned-order minus full-rerank nDCG@10: CI low >= -0.01
learned-order mean feature evaluations <= 50% of full rerank
learned-vs-full feature-evaluation difference CI high < 0
learned-order feature-evaluation advantage over fixed order >= 3%
fixed-minus-learned feature-evaluation CI low > 0

C2:
at least 30 common initial-suppression cases
soft-minus-hard recovery advantage >= 10 percentage points
paired-bootstrap recovery interval low > 0

C3:
committed precision minus forced precision >= 5 percentage points
bootstrap precision-gain interval low > 0
empty-field abstain rate >= 50%
```

The earlier draft contained an internal C2 wording mismatch: one paragraph specified 10 points while the gate paragraph said 30. The code, test constant, and claim definition all used 10 points. **Before any external final evaluation, this preregistration freezes C2 at 10 points.** This is a pre-final correction, not a response to SciFact performance.

## 9. Statistical reporting

All primary comparative deltas use 1,000 deterministic paired-bootstrap resamples and report a 95% interval.

C2 uses only common suppression cases, preserving query pairing between soft and hard conditions.

C3 bootstraps the query-level committed-precision-minus-forced-precision statistic.

A point estimate that clears its threshold while the required interval crosses zero does not pass.

## 10. Verdict logic

C1, C2, and C3 receive independent statuses:

```text
REINFORCED
DISCOUNTED
INCONCLUSIVE
```

Overall reporting is conservative:

- any `DISCOUNTED` claim -> overall `DISCOUNTED`;
- otherwise any `INCONCLUSIVE` claim -> overall `INCONCLUSIVE`;
- all three `REINFORCED` -> overall `REINFORCED`;
- any synthetic dataset -> `NOT EVIDENCE` regardless of the internal checks.

Too few C2 cases may not hide a negative C1 or C3 result.

## 11. What negative results mean

A negative C1 would mean the staged cascade does not earn its feature-evaluation cost against straightforward real retrieval/reranking under this implementation. That would materially weaken the HCT-2 efficiency interpretation.

A negative C2 would mean the HCT reversibility advantage did not transfer to this retrieval setting. An inconclusive C2 would mean the chosen corpus/probe did not exercise enough genuine suppression cases; it must not be converted into a pass by lowering the case threshold.

A negative C3 would mean the current commitment margin does not improve calibration enough to justify explicit abstention in this setting.

A negative recurrence ablation on external data would directly weaken the strongest mechanistic interpretation currently drawn from HCT-2, because HCT-2's relation graph was not fully answer-independent.

## 12. Scientific boundary

Even a successful EXT-1 would establish only a narrow result: with one public retrieval benchmark and four hand-designed features, a learned ordered reversible cascade can preserve or improve retrieval behavior at lower measured feature cost, recover some candidates after under-specified context, and/or improve commitment calibration.

It would not establish biological hippocampal equivalence, learned semantic representations, general reasoning, superiority to modern dense/late-interaction retrieval, lower total end-to-end wall-clock cost, autonomous cognition, or production readiness.

## 13. Run order

First, code-path verification only:

```bash
python3 -m pytest -q tests/test_external_retrieval_cascade.py
python3 -m experiments.external_retrieval_cascade --smoke
```

Then download SciFact once and inspect **development only**:

```bash
python3 -m experiments.external_retrieval_cascade \
  --data datasets/scifact \
  --development
```

Only after the implementation, tests, preregistration, and development diagnostics are frozen should the confirmatory final split be run:

```bash
python3 -m experiments.external_retrieval_cascade --data datasets/scifact
```

Once the external final split is observed, material mechanism/gate changes require a new EXT version rather than rewriting EXT-1.
