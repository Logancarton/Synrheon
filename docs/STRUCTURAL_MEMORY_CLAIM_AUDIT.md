# Structural Memory Claim Audit

**Status:** pre-MRC-1 result claim cleanup

This document separates what Synrheon may reasonably claim now, what is only a design property, and what must be benchmarked.

## Claims to retract or narrow

### “Dense retrieval does not scale”

Retract. Modern approximate-nearest-neighbor systems such as HNSW and FAISS are specifically designed for large-scale non-exhaustive vector search, including billion-scale datasets. Synrheon should not position sparse structural routing as solving a scaling problem that ANN methods cannot solve.

### “RAG is flat single-shot nearest-neighbor retrieval”

Retract as a general statement. Many practical RAG pipelines are single-pass, but iterative, graph-based, and multi-hop retrieval systems exist. Synrheon may compare against a clearly specified single-pass RAG baseline, but not against “RAG” as though the whole category is one-shot.

### “Dense retrieval structurally cannot perform multi-hop reasoning”

Retract. Iterative retrieval systems can perform multi-hop evidence gathering. A valid Synrheon question is whether explicit structural traversal offers a cheaper, more controllable, more local, or better-calibrated route under matched tasks and compute.

### “No catastrophic forgetting by construction”

Narrow sharply. Structural insertion can preserve old stored records without overwriting them, but new memories can still reduce old-memory retrieval quality through collisions, interference, or changed routing competition. MRC-1 measures storage preservation and retrieval retention separately.

### “HNSW is O(log N)”

Use cautiously. The original HNSW work reports logarithmic complexity scaling behavior under its evaluated conditions; this should not be presented as a universal worst-case guarantee for every dataset or parameterization.

### “Product quantization compresses vectors 32x”

Do not use as a fixed claim. PQ compression depends on dimensionality, number of subquantizers, bits per code, metadata, and implementation choices.

## Claims that are established prior art, not Synrheon novelty

- external non-parametric memory can augment language models;
- retrieval can scale to very large corpora;
- selectivity-first / shortest-posting-first processing is a standard database/query-planning idea;
- iterative retrieval can gather multi-hop evidence;
- product quantization and ANN indexes can reduce vector-search memory/compute substantially.

Synrheon should treat these as baselines or borrowed engineering principles.

## Claims Synrheon can test directly

### Exact structural insertion

Does adding a new memory leave the serialized content of old memory records unchanged?

MRC-1 classification: specification invariant.

### Exact structural deletion and provenance

Can an individual stored memory be deleted from records and posting lists while unrelated records remain unchanged, and can every surviving retrieval ID resolve to the exact stored provenance?

MRC-1 classification: specification invariant.

### Old-memory retrieval retention under growth

Does partial-cue retrieval of old memories remain useful after thousands of new memories are inserted, especially under a crowded concept vocabulary?

MRC-1 classification: empirical synthetic benchmark.

### Query-work concentration

How many posting entries and membership checks are touched per query as the store grows, under selective versus crowded concept distributions?

MRC-1 classification: empirical/algorithmic benchmark. Operation counts are not equivalent to native ANN wall-clock time.

### Local continual routing updates

Can routing parameters be updated from newly stored memories or retrieval outcomes without global retraining, while preserving performance on old probes?

Status: not tested by MRC-1; requires a later learned-routing experiment.

### Structural multi-hop traversal

Can the same store answer held-out compositional queries by traversing stored relations, under matched compute and against iterative retrieval baselines?

Status: not tested by MRC-1; requires a later experiment with a genuinely competitive iterative baseline.

## Defensible current positioning

Synrheon is exploring a **structural, locally updatable memory and routing layer** that may complement a frozen language model. Its possible advantages must be demonstrated in explicit benchmarks for insertion/deletion semantics, provenance, retrieval retention under growth, routing work, local-update stability, compositional traversal, and abstention. It should not claim generic superiority to RAG, HNSW, FAISS, or modern dense retrieval without direct matched comparisons.

## Relevant prior work to cite in a future paper

- Malkov & Yashunin, *Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs*.
- Johnson et al., *Billion-scale similarity search with GPUs* / FAISS research foundations.
- Jégou et al., *Product Quantization for Nearest Neighbor Search*.
- Borgeaud et al., *Improving language models by retrieving from trillions of tokens* (RETRO).
- Modern iterative and multi-hop RAG literature should be included rather than treating RAG as a single flat method.
