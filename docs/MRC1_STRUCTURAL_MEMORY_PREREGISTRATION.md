# MRC-1 Preregistration: Structural Memory Scaling and Retention

**Synrheon Experimental Research Program**  
**Status:** FROZEN BEFORE RESULT INSPECTION  
**Branch:** `experiment/external-retrieval-cascade`

## Question

Can a simple structural memory store with concept posting lists support exact inserts/deletes, preserve previously stored records, and retain useful partial-cue retrieval as the store grows, while query work is concentrated on touched posting lists rather than a full memory scan?

This is deliberately narrower than a claim that Synrheon is superior to modern RAG, HNSW, FAISS, or dense retrieval. MRC-1 does not test language quality, embedding quality, wall-clock superiority to optimized native ANN libraries, or general intelligence.

## Claims separated before testing

### S1 — record preservation

Appending new memories does not mutate the serialized representation of existing memories.

Classification if it passes: **SPECIFICATION / DATA-STRUCTURE INVARIANT**. It is not evidence that retrieval quality is preserved.

### S2 — exact deletion and provenance

Deleting a memory removes its record and its posting-list memberships while leaving unrelated records unchanged. A returned memory ID resolves to its exact stored provenance record.

Classification if it passes: **SPECIFICATION / DATA-STRUCTURE INVARIANT**.

### E1 — old-memory retrieval retention

After adding increasingly many new memories, partial-cue retrieval of a frozen set of old memories remains measurably useful. This may fail because new memories can create collisions even though old records are not overwritten.

Classification: **EMPIRICAL SYNTHETIC BENCHMARK**.

### E2 — query-work scaling

Posting-list routing should avoid a full scan when cue concepts are selective, but no universal sublinear claim is preregistered. Two regimes are required:

1. **selective regime** — vocabulary grows with memory count, keeping posting lists relatively sparse;
2. **crowded regime** — vocabulary is fixed while memory count grows, causing posting lists to grow.

The benchmark reports posting entries touched and candidate score updates per query. It does not equate these operations to FLOPs or wall-clock cost of optimized ANN systems.

Classification: **EMPIRICAL/ALGORITHMIC BENCHMARK**, interpreted separately by regime.

### E3 — selectivity-first routing

For the same cue and same index, intersecting/processing shortest posting lists first should use no more candidate-set intersection work than longest-first ordering. Because this follows standard set-processing logic, it is treated primarily as an engineering baseline, not a novel scientific discovery.

## Store

Each memory contains:

- opaque `memory_id`;
- a fixed set of opaque concept IDs;
- immutable provenance text;
- insertion sequence.

The index contains:

- `records[memory_id] -> MemoryRecord`;
- `postings[concept_id] -> set[memory_id]`.

No vectors, embeddings, language model, hidden answer bonus, learned relation graph, or target identity is available to retrieval.

## Retrieval

A query is a set of observed concept IDs. For each cue concept, retrieve its posting list. Candidate memories are scored by exact cue overlap. Ties are broken by opaque memory ID only after scoring.

The retriever reports explicit work counters:

- posting entries read;
- candidate score updates;
- intersection membership checks;
- number of candidates scored.

No claim is made that one Python operation equals one native ANN distance operation.

## Synthetic data

Each memory contains 6 concepts. Each retrieval cue contains 3 concepts sampled from the target memory.

Memory counts:

`1,000; 3,000; 10,000; 30,000`

Two data regimes:

- **selective:** vocabulary size = max(256, round(6 * sqrt(N) * 8));
- **crowded:** vocabulary size = 512.

For each N, generate 5 independent seeds. For each seed, freeze the first 200 memories as the old-memory probe set and query up to 100 of them.

The same old probe identities are evaluated after each growth checkpoint within a seed.

## Metrics

For old-memory probes:

- Hit@1;
- Hit@32;
- mean reciprocal rank within scored candidates;
- mean candidates scored;
- mean posting entries read;
- mean candidate score updates;
- mean intersection membership checks.

Record preservation:

- SHA-256 digest of the frozen first-200 record serialization before and after growth.

Deletion/provenance integrity:

- deleted ID absent from records and all postings;
- unrelated frozen-record digest unchanged;
- provenance returned for surviving IDs exactly equals stored provenance.

## Controls

1. **full-scan exact overlap** — same overlap score over every memory; correctness reference, not a speed competitor.
2. **posting-list route, selectivity-first** — proposed structural route.
3. **posting-list route, reverse-selectivity** — same information and score, intentionally poor posting order for work comparison.

A future external benchmark may add FAISS/HNSW/BM25 using native libraries. MRC-1 does not substitute a Python reimplementation and call it a fair ANN comparison.

## Advancement / falsification

MRC-1 may support only the following narrow statements:

- structural insertion preserves old stored records if S1 passes;
- exact structural deletion/provenance works if S2 passes;
- partial-cue old-memory retrieval remains useful over the tested growth range if E1 remains strong;
- selective posting-list routing touches materially less of the store than a full scan in the selective regime if observed;
- no universal sublinear claim is permitted if crowded-regime work grows approximately with N.

The claim **“new inserts cannot hurt old-memory retrieval” is falsified** by any meaningful decline in old-memory retrieval metrics, even if record digests are unchanged.

The claim **“Synrheon beats RAG/HNSW/FAISS” cannot be supported by MRC-1** under any result.

## Scientific boundary

This is a synthetic systems benchmark. It does not establish language understanding, semantic alias resolution, external-memory superiority, hardware efficiency, continual-learning superiority to all parametric methods, or production readiness.
