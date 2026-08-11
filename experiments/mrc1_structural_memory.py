"""MRC-1 structural-memory scaling and retention benchmark.

This experiment measures a simple opaque concept -> memory posting-list store.
It deliberately does not claim superiority to optimized ANN/RAG systems.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import hashlib
import json
import math
import random
from statistics import mean
from typing import Iterable, Sequence

EXPERIMENT_ID = "mrc1-structural-memory-v1"
MEMORY_COUNTS = (1_000, 3_000, 10_000, 30_000)
SEEDS = (81001, 81002, 81003, 81004, 81005)
CONCEPTS_PER_MEMORY = 6
CUE_SIZE = 3
OLD_PROBE_COUNT = 200
QUERY_PROBE_COUNT = 100
CROWDED_VOCABULARY = 64


@dataclass(frozen=True, slots=True)
class MemoryRecord:
    memory_id: str
    concepts: tuple[str, ...]
    provenance: str
    insertion_sequence: int


@dataclass(frozen=True, slots=True)
class RetrievalResult:
    ranked_ids: tuple[str, ...]
    posting_entries_read: int
    candidate_score_updates: int
    intersection_membership_checks: int
    candidates_scored: int


@dataclass(frozen=True, slots=True)
class CheckpointMetric:
    regime: str
    seed: int
    memory_count: int
    vocabulary_size: int
    hit_at_1: float
    hit_at_32: float
    mean_reciprocal_rank: float
    mean_candidates_scored: float
    mean_posting_entries_read: float
    mean_candidate_score_updates: float
    mean_intersection_membership_checks: float
    full_scan_concept_checks_per_query: int
    mean_work_fraction_vs_full_scan_checks: float
    frozen_record_digest_preserved: bool

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class StructuralMemoryIndex:
    def __init__(self) -> None:
        self.records: dict[str, MemoryRecord] = {}
        self.postings: dict[str, set[str]] = {}

    def insert(self, record: MemoryRecord) -> None:
        if record.memory_id in self.records:
            raise ValueError(f"duplicate memory_id: {record.memory_id}")
        self.records[record.memory_id] = record
        for concept in record.concepts:
            self.postings.setdefault(concept, set()).add(record.memory_id)

    def delete(self, memory_id: str) -> MemoryRecord:
        record = self.records.pop(memory_id)
        for concept in record.concepts:
            posting = self.postings[concept]
            posting.remove(memory_id)
            if not posting:
                del self.postings[concept]
        return record

    def provenance(self, memory_id: str) -> str:
        return self.records[memory_id].provenance

    def retrieve(
        self,
        cue: Sequence[str],
        *,
        order: str = "selectivity_first",
    ) -> RetrievalResult:
        if not cue:
            return RetrievalResult(tuple(), 0, 0, 0, 0)

        cue_unique = tuple(dict.fromkeys(cue))
        posting_rows = [
            (concept, self.postings.get(concept, set())) for concept in cue_unique
        ]
        if order == "selectivity_first":
            posting_rows.sort(key=lambda row: (len(row[1]), row[0]))
        elif order == "reverse_selectivity":
            posting_rows.sort(key=lambda row: (-len(row[1]), row[0]))
        else:
            raise ValueError(f"unknown order: {order}")

        first = posting_rows[0][1]
        posting_entries_read = len(first)
        candidates = set(first)
        membership_checks = 0

        for _, posting in posting_rows[1:]:
            next_candidates: set[str] = set()
            for memory_id in candidates:
                membership_checks += 1
                if memory_id in posting:
                    next_candidates.add(memory_id)
            candidates = next_candidates
            if not candidates:
                break

        # Every surviving candidate contains every cue concept. The explicit overlap
        # score is retained so the benchmark's ranking rule matches the full-scan
        # correctness control rather than relying on insertion order.
        scored: list[tuple[int, str]] = []
        candidate_score_updates = 0
        cue_set = set(cue_unique)
        for memory_id in candidates:
            overlap = 0
            record = self.records[memory_id]
            record_set = set(record.concepts)
            for concept in cue_set:
                candidate_score_updates += 1
                if concept in record_set:
                    overlap += 1
            scored.append((overlap, memory_id))

        scored.sort(key=lambda item: (-item[0], item[1]))
        return RetrievalResult(
            ranked_ids=tuple(memory_id for _, memory_id in scored),
            posting_entries_read=posting_entries_read,
            candidate_score_updates=candidate_score_updates,
            intersection_membership_checks=membership_checks,
            candidates_scored=len(scored),
        )

    def full_scan(self, cue: Sequence[str]) -> RetrievalResult:
        cue_unique = tuple(dict.fromkeys(cue))
        cue_set = set(cue_unique)
        scored: list[tuple[int, str]] = []
        checks = 0
        for memory_id, record in self.records.items():
            record_set = set(record.concepts)
            overlap = 0
            for concept in cue_set:
                checks += 1
                if concept in record_set:
                    overlap += 1
            scored.append((overlap, memory_id))
        scored.sort(key=lambda item: (-item[0], item[1]))
        return RetrievalResult(
            ranked_ids=tuple(memory_id for _, memory_id in scored),
            posting_entries_read=0,
            candidate_score_updates=checks,
            intersection_membership_checks=0,
            candidates_scored=len(scored),
        )


def _record_digest(records: Iterable[MemoryRecord]) -> str:
    rows = [
        {
            "memory_id": record.memory_id,
            "concepts": list(record.concepts),
            "provenance": record.provenance,
            "insertion_sequence": record.insertion_sequence,
        }
        for record in sorted(records, key=lambda record: record.memory_id)
    ]
    payload = json.dumps(rows, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _opaque_memory_ids(seed: int, count: int) -> list[str]:
    rng = random.Random(seed + 4_700_003)
    values = rng.sample(range(10_000_000_000, 99_999_999_999), count)
    return [f"m{value}" for value in values]


def _vocabulary_size(regime: str, checkpoint: int) -> int:
    if regime == "crowded":
        return CROWDED_VOCABULARY
    if regime == "selective":
        return max(256, round(CONCEPTS_PER_MEMORY * math.sqrt(checkpoint) * 8))
    raise ValueError(f"unknown regime: {regime}")


def _concept_pool(size: int) -> tuple[str, ...]:
    return tuple(f"c{index:06d}" for index in range(size))


def _generate_growth_records(
    *,
    seed: int,
    regime: str,
    checkpoints: Sequence[int] = MEMORY_COUNTS,
) -> list[MemoryRecord]:
    max_count = max(checkpoints)
    ids = _opaque_memory_ids(seed, max_count)
    rng = random.Random(seed)
    records: list[MemoryRecord] = []
    previous = 0

    for checkpoint in checkpoints:
        vocabulary_size = _vocabulary_size(regime, checkpoint)
        pool = _concept_pool(vocabulary_size)
        for sequence in range(previous, checkpoint):
            concepts = tuple(sorted(rng.sample(pool, CONCEPTS_PER_MEMORY)))
            records.append(
                MemoryRecord(
                    memory_id=ids[sequence],
                    concepts=concepts,
                    provenance=f"seed={seed};regime={regime};sequence={sequence}",
                    insertion_sequence=sequence,
                )
            )
        previous = checkpoint

    return records


def _probe_cues(records: Sequence[MemoryRecord]) -> dict[str, tuple[str, ...]]:
    probes = records[: min(QUERY_PROBE_COUNT, len(records))]
    return {
        record.memory_id: tuple(record.concepts[:CUE_SIZE])
        for record in probes
    }


def _rank_of(memory_id: str, ranked_ids: Sequence[str]) -> int | None:
    try:
        return ranked_ids.index(memory_id) + 1
    except ValueError:
        return None


def _evaluate_checkpoint(
    *,
    index: StructuralMemoryIndex,
    regime: str,
    seed: int,
    memory_count: int,
    probe_cues: dict[str, tuple[str, ...]],
    frozen_digest: str,
) -> CheckpointMetric:
    ranks: list[int | None] = []
    candidates_scored: list[int] = []
    posting_entries: list[int] = []
    candidate_updates: list[int] = []
    membership_checks: list[int] = []
    work_fractions: list[float] = []

    for memory_id, cue in probe_cues.items():
        result = index.retrieve(cue, order="selectivity_first")
        rank = _rank_of(memory_id, result.ranked_ids)
        ranks.append(rank)
        candidates_scored.append(result.candidates_scored)
        posting_entries.append(result.posting_entries_read)
        candidate_updates.append(result.candidate_score_updates)
        membership_checks.append(result.intersection_membership_checks)

        full_checks = memory_count * len(cue)
        route_work = (
            result.posting_entries_read
            + result.candidate_score_updates
            + result.intersection_membership_checks
        )
        work_fractions.append(route_work / full_checks if full_checks else 0.0)

    frozen_records = [
        record
        for record in index.records.values()
        if record.insertion_sequence < OLD_PROBE_COUNT
    ]
    current_digest = _record_digest(frozen_records)

    reciprocal = [0.0 if rank is None else 1.0 / rank for rank in ranks]
    return CheckpointMetric(
        regime=regime,
        seed=seed,
        memory_count=memory_count,
        vocabulary_size=_vocabulary_size(regime, memory_count),
        hit_at_1=mean(1.0 if rank == 1 else 0.0 for rank in ranks),
        hit_at_32=mean(
            1.0 if rank is not None and rank <= 32 else 0.0 for rank in ranks
        ),
        mean_reciprocal_rank=mean(reciprocal),
        mean_candidates_scored=mean(candidates_scored),
        mean_posting_entries_read=mean(posting_entries),
        mean_candidate_score_updates=mean(candidate_updates),
        mean_intersection_membership_checks=mean(membership_checks),
        full_scan_concept_checks_per_query=memory_count * CUE_SIZE,
        mean_work_fraction_vs_full_scan_checks=mean(work_fractions),
        frozen_record_digest_preserved=current_digest == frozen_digest,
    )


def _deletion_integrity(index: StructuralMemoryIndex) -> dict[str, object]:
    records_by_sequence = sorted(index.records.values(), key=lambda record: record.insertion_sequence)
    if len(records_by_sequence) <= OLD_PROBE_COUNT + 1:
        raise ValueError("index too small for deletion integrity check")

    frozen_before = _record_digest(records_by_sequence[:OLD_PROBE_COUNT])
    victim = records_by_sequence[OLD_PROBE_COUNT + 1]
    victim_provenance = victim.provenance
    unrelated = records_by_sequence[0]
    unrelated_provenance = unrelated.provenance

    removed = index.delete(victim.memory_id)
    absent_from_records = victim.memory_id not in index.records
    absent_from_postings = all(
        victim.memory_id not in posting for posting in index.postings.values()
    )
    frozen_after = _record_digest(
        sorted(index.records.values(), key=lambda record: record.insertion_sequence)[:OLD_PROBE_COUNT]
    )

    return {
        "deleted_id": victim.memory_id,
        "deleted_record_round_trip": removed == victim,
        "deleted_provenance_round_trip": removed.provenance == victim_provenance,
        "absent_from_records": absent_from_records,
        "absent_from_all_postings": absent_from_postings,
        "unrelated_provenance_unchanged": index.provenance(unrelated.memory_id) == unrelated_provenance,
        "frozen_digest_unchanged": frozen_before == frozen_after,
    }


def _order_work_control(index: StructuralMemoryIndex, probe_cues: dict[str, tuple[str, ...]]) -> dict[str, float | bool]:
    selective_work: list[int] = []
    reverse_work: list[int] = []
    same_rankings = True

    for cue in probe_cues.values():
        selective = index.retrieve(cue, order="selectivity_first")
        reverse = index.retrieve(cue, order="reverse_selectivity")
        selective_work.append(
            selective.posting_entries_read
            + selective.candidate_score_updates
            + selective.intersection_membership_checks
        )
        reverse_work.append(
            reverse.posting_entries_read
            + reverse.candidate_score_updates
            + reverse.intersection_membership_checks
        )
        same_rankings = same_rankings and selective.ranked_ids == reverse.ranked_ids

    return {
        "same_rankings": same_rankings,
        "mean_selectivity_first_work": mean(selective_work),
        "mean_reverse_selectivity_work": mean(reverse_work),
        "selectivity_first_not_more_work": mean(selective_work) <= mean(reverse_work),
    }


def run_seed(seed: int, regime: str) -> dict[str, object]:
    records = _generate_growth_records(seed=seed, regime=regime)
    probe_cues = _probe_cues(records)
    index = StructuralMemoryIndex()

    first_old = records[:OLD_PROBE_COUNT]
    frozen_digest = _record_digest(first_old)
    checkpoint_metrics: list[CheckpointMetric] = []
    inserted = 0

    for checkpoint in MEMORY_COUNTS:
        for record in records[inserted:checkpoint]:
            index.insert(record)
        inserted = checkpoint
        checkpoint_metrics.append(
            _evaluate_checkpoint(
                index=index,
                regime=regime,
                seed=seed,
                memory_count=checkpoint,
                probe_cues=probe_cues,
                frozen_digest=frozen_digest,
            )
        )

    order_control = _order_work_control(index, probe_cues)
    deletion = _deletion_integrity(index)

    # A small correctness spot-check verifies that the posting-list route and full scan
    # agree on the target rank whenever the target matches all cue concepts.
    correctness_rows: list[dict[str, object]] = []
    for memory_id, cue in list(probe_cues.items())[:10]:
        routed = index.retrieve(cue, order="selectivity_first")
        full = index.full_scan(cue)
        routed_rank = _rank_of(memory_id, routed.ranked_ids)
        full_rank = _rank_of(memory_id, full.ranked_ids)
        correctness_rows.append(
            {
                "memory_id": memory_id,
                "routed_rank": routed_rank,
                "full_scan_rank": full_rank,
                "rank_matches": routed_rank == full_rank,
            }
        )

    return {
        "seed": seed,
        "regime": regime,
        "checkpoints": [metric.to_dict() for metric in checkpoint_metrics],
        "order_control": order_control,
        "deletion_integrity": deletion,
        "full_scan_correctness_spotcheck": correctness_rows,
    }


def _aggregate(seed_reports: Sequence[dict[str, object]], regime: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for checkpoint in MEMORY_COUNTS:
        checkpoint_rows = []
        for report in seed_reports:
            metrics = report["checkpoints"]
            assert isinstance(metrics, list)
            checkpoint_rows.append(
                next(row for row in metrics if row["memory_count"] == checkpoint)
            )

        rows.append(
            {
                "regime": regime,
                "memory_count": checkpoint,
                "mean_hit_at_1": mean(float(row["hit_at_1"]) for row in checkpoint_rows),
                "mean_hit_at_32": mean(float(row["hit_at_32"]) for row in checkpoint_rows),
                "mean_mrr": mean(float(row["mean_reciprocal_rank"]) for row in checkpoint_rows),
                "mean_candidates_scored": mean(float(row["mean_candidates_scored"]) for row in checkpoint_rows),
                "mean_work_fraction_vs_full_scan_checks": mean(
                    float(row["mean_work_fraction_vs_full_scan_checks"])
                    for row in checkpoint_rows
                ),
                "all_frozen_record_digests_preserved": all(
                    bool(row["frozen_record_digest_preserved"])
                    for row in checkpoint_rows
                ),
            }
        )
    return rows


def run_benchmark(*, seeds: Sequence[int] = SEEDS) -> dict[str, object]:
    regime_reports: dict[str, list[dict[str, object]]] = {}
    aggregate: dict[str, list[dict[str, object]]] = {}

    for regime in ("selective", "crowded"):
        reports = [run_seed(seed, regime) for seed in seeds]
        regime_reports[regime] = reports
        aggregate[regime] = _aggregate(reports, regime)

    all_deletion_pass = all(
        all(bool(value) for key, value in report["deletion_integrity"].items() if key != "deleted_id")
        for reports in regime_reports.values()
        for report in reports
    )
    all_rank_spotchecks_pass = all(
        all(bool(row["rank_matches"]) for row in report["full_scan_correctness_spotcheck"])
        for reports in regime_reports.values()
        for report in reports
    )
    all_order_controls_pass = all(
        bool(report["order_control"]["same_rankings"])
        and bool(report["order_control"]["selectivity_first_not_more_work"])
        for reports in regime_reports.values()
        for report in reports
    )

    return {
        "experiment": EXPERIMENT_ID,
        "artifact_class": "SYNTHETIC_SYSTEMS_BENCHMARK",
        "preregistration": "docs/MRC1_STRUCTURAL_MEMORY_PREREGISTRATION.md",
        "amendment": "docs/MRC1_AMENDMENT_1.md",
        "claims": {
            "record_preservation": "SPECIFICATION_INVARIANT",
            "deletion_and_provenance": "SPECIFICATION_INVARIANT",
            "old_memory_retrieval_retention": "EMPIRICAL_SYNTHETIC",
            "query_work_scaling": "EMPIRICAL_ALGORITHMIC",
            "selectivity_first": "ENGINEERING_BASELINE",
        },
        "aggregate": aggregate,
        "integrity": {
            "all_deletion_checks_pass": all_deletion_pass,
            "all_routed_vs_full_scan_rank_spotchecks_pass": all_rank_spotchecks_pass,
            "all_selectivity_order_controls_pass": all_order_controls_pass,
        },
        "per_seed": regime_reports,
        "interpretation_boundary": {
            "no_ann_superiority_claim": True,
            "no_rag_superiority_claim": True,
            "record_preservation_does_not_imply_retrieval_preservation": True,
            "operation_counts_are_not_wall_clock_or_flops": True,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run MRC-1 structural memory benchmark")
    parser.add_argument("--quick", action="store_true", help="run two seeds instead of five")
    args = parser.parse_args()
    seeds = SEEDS[:2] if args.quick else SEEDS
    print(json.dumps(run_benchmark(seeds=seeds), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
