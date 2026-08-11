"""R0-SR1D: map the operating envelope of frozen exact single-route retrieval.

This diagnostic imports and reuses the validated R0-SR1 world and retriever unchanged.
It adds no vectors, similarity, learning, multi-route merge, or target-aware routing.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from statistics import mean
from typing import Sequence
import argparse
import json

from experiments.r0_single_route_access import (
    FIELD_SIZE,
    MEMORY_COUNT,
    LabeledProbe,
    MemoryRecord,
    ProbeOutcome,
    RetrievalCue,
    SingleRouteRetriever,
    SingleRouteWorld,
    make_family_a_world,
    make_probe,
    score_probe,
)

EXPERIMENT_ID = "r0-exact-match-envelope-v1"
FIELD_SIZES = (4, 8, 16, 32, 64)
UNBOUND_NOISE_COUNTS = (1, 4, 16, 64)


@dataclass(frozen=True, slots=True)
class FieldSweepMetric:
    route_index: int
    route_group_size: int
    field_size: int
    partial_hit: float
    expected_partial_hit: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class RouteEnvelopeMetric:
    route_index: int
    route_group_size: int
    detail_only_top1: float
    detail_only_hit_at_32: float
    same_group_conflict_target_top1: float
    same_group_conflict_target_hit_at_32: float
    same_group_conflict_competitor_top1: float
    foreign_group_conflict_target_hit_at_32: float
    foreign_group_conflict_mean_target_rank_when_hit: float | None
    near_id_hit_at_32: float
    alias_hit_at_32: float
    unbound_noise_hit_at_32: dict[str, float]
    partial_reference_hit_at_32: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def run_exact_match_envelope(
    *,
    seed: int = 1701,
) -> dict[str, object]:
    """Run the frozen exact-match operating-envelope diagnostic."""

    world = make_family_a_world(seed=seed)
    retriever = SingleRouteRetriever(world)

    field_sweep: list[FieldSweepMetric] = []
    route_metrics: list[RouteEnvelopeMetric] = []

    for route_index, group_size in enumerate(world.route_group_sizes):
        # A. Capacity/ambiguity sweep.
        for field_size in FIELD_SIZES:
            outcomes = [
                score_probe(
                    retriever,
                    make_probe(
                        world,
                        memory,
                        route_index=route_index,
                        condition="partial",
                    ),
                    field_size=field_size,
                )
                for memory in world.memories
            ]
            field_sweep.append(
                FieldSweepMetric(
                    route_index=route_index,
                    route_group_size=group_size,
                    field_size=field_size,
                    partial_hit=_bool_rate(outcomes, "hit_at_field"),
                    expected_partial_hit=min(1.0, field_size / group_size),
                )
            )

        partial_reference = _custom_hit_rate(
            retriever,
            world,
            route_index,
            cues=[
                RetrievalCue((memory.binding(route_index).anchor_concept_id,))
                for memory in world.memories
            ],
            field_size=FIELD_SIZE,
        )

        # B. Unique exact detail survives without its shared anchor.
        detail_cues = [
            RetrievalCue((memory.binding(route_index).detail_concept_id,))
            for memory in world.memories
        ]
        detail_outcomes = _custom_outcomes(
            retriever,
            world,
            route_index,
            detail_cues,
            field_size=FIELD_SIZE,
            label="detail_only",
        )

        # C. Unbound distractors scale scores but should not change ranking.
        unbound_noise: dict[str, float] = {}
        for noise_count in UNBOUND_NOISE_COUNTS:
            cues = [
                RetrievalCue(
                    (
                        memory.binding(route_index).anchor_concept_id,
                        *tuple(
                            f"unbound:{seed}:{route_index}:{memory.memory_id}:{noise_index}"
                            for noise_index in range(noise_count)
                        ),
                    )
                )
                for memory in world.memories
            ]
            unbound_noise[str(noise_count)] = _custom_hit_rate(
                retriever,
                world,
                route_index,
                cues=cues,
                field_size=FIELD_SIZE,
            )

        # D. Correct shared anchor + another same-group memory's exact detail.
        same_group_cues: list[RetrievalCue] = []
        same_group_competitors: list[str] = []
        for memory in world.memories:
            competitor = _same_group_competitor(world, memory, route_index)
            binding = memory.binding(route_index)
            same_group_cues.append(
                RetrievalCue(
                    (
                        binding.anchor_concept_id,
                        competitor.binding(route_index).detail_concept_id,
                    )
                )
            )
            same_group_competitors.append(competitor.memory_id)
        same_group_outcomes = _custom_outcomes(
            retriever,
            world,
            route_index,
            same_group_cues,
            field_size=FIELD_SIZE,
            label="same_group_conflict",
        )
        same_group_competitor_top1 = _competitor_top1_rate(
            retriever,
            route_index,
            same_group_cues,
            same_group_competitors,
        )

        # E. Correct shared anchor + exact detail from another group.
        foreign_group_cues: list[RetrievalCue] = []
        for memory in world.memories:
            competitor = _foreign_group_competitor(world, memory, route_index)
            binding = memory.binding(route_index)
            foreign_group_cues.append(
                RetrievalCue(
                    (
                        binding.anchor_concept_id,
                        competitor.binding(route_index).detail_concept_id,
                    )
                )
            )
        foreign_group_outcomes = _custom_outcomes(
            retriever,
            world,
            route_index,
            foreign_group_cues,
            field_size=FIELD_SIZE,
            label="foreign_group_conflict",
        )
        foreign_ranks = [
            outcome.target_rank
            for outcome in foreign_group_outcomes
            if outcome.target_rank is not None
        ]

        # F. Unequal concept identity: deterministic one-character-like suffix mutation.
        near_id_cues = [
            RetrievalCue((f"{memory.binding(route_index).detail_concept_id}~",))
            for memory in world.memories
        ]
        near_id_hit = _custom_hit_rate(
            retriever,
            world,
            route_index,
            cues=near_id_cues,
            field_size=FIELD_SIZE,
        )

        # G. Experiment-known alias that is never installed into memory bindings.
        alias_cues = [
            RetrievalCue((f"alias:{seed}:{route_index}:{memory.memory_id}",))
            for memory in world.memories
        ]
        alias_hit = _custom_hit_rate(
            retriever,
            world,
            route_index,
            cues=alias_cues,
            field_size=FIELD_SIZE,
        )

        route_metrics.append(
            RouteEnvelopeMetric(
                route_index=route_index,
                route_group_size=group_size,
                detail_only_top1=_bool_rate(detail_outcomes, "top1"),
                detail_only_hit_at_32=_bool_rate(detail_outcomes, "hit_at_field"),
                same_group_conflict_target_top1=_bool_rate(
                    same_group_outcomes, "top1"
                ),
                same_group_conflict_target_hit_at_32=_bool_rate(
                    same_group_outcomes, "hit_at_field"
                ),
                same_group_conflict_competitor_top1=same_group_competitor_top1,
                foreign_group_conflict_target_hit_at_32=_bool_rate(
                    foreign_group_outcomes, "hit_at_field"
                ),
                foreign_group_conflict_mean_target_rank_when_hit=(
                    mean(foreign_ranks) if foreign_ranks else None
                ),
                near_id_hit_at_32=near_id_hit,
                alias_hit_at_32=alias_hit,
                unbound_noise_hit_at_32=unbound_noise,
                partial_reference_hit_at_32=partial_reference,
            )
        )

    integrity = _diagnostic_integrity(field_sweep, route_metrics)
    return {
        "experiment": EXPERIMENT_ID,
        "evidence_level": "exact-match mechanism envelope; not vector evidence",
        "generator_family": "A",
        "seed": seed,
        "memory_count": len(world.memories),
        "field_sizes": list(FIELD_SIZES),
        "route_group_sizes": list(world.route_group_sizes),
        "unbound_noise_counts": list(UNBOUND_NOISE_COUNTS),
        "field_sweep": [metric.to_dict() for metric in field_sweep],
        "route_metrics": [metric.to_dict() for metric in route_metrics],
        "verdict": (
            "EXACT_MATCH_ENVELOPE_VALID"
            if integrity
            else "EXACT_MATCH_DIAGNOSTIC_INVALID"
        ),
    }


def _custom_outcomes(
    retriever: SingleRouteRetriever,
    world: SingleRouteWorld,
    route_index: int,
    cues: Sequence[RetrievalCue],
    *,
    field_size: int,
    label: str,
) -> list[ProbeOutcome]:
    if len(cues) != len(world.memories):
        raise ValueError("Custom cues must align one-to-one with world memories.")
    outcomes: list[ProbeOutcome] = []
    for memory, cue in zip(world.memories, cues, strict=True):
        probe = LabeledProbe(
            probe_id=f"{label}:{route_index}:{memory.memory_id}",
            route_index=route_index,
            condition="partial",
            cue=cue,
            target_memory_id=memory.memory_id,
        )
        outcomes.append(score_probe(retriever, probe, field_size=field_size))
    return outcomes


def _custom_hit_rate(
    retriever: SingleRouteRetriever,
    world: SingleRouteWorld,
    route_index: int,
    *,
    cues: Sequence[RetrievalCue],
    field_size: int,
) -> float:
    outcomes = _custom_outcomes(
        retriever,
        world,
        route_index,
        cues,
        field_size=field_size,
        label="custom",
    )
    return _bool_rate(outcomes, "hit_at_field")


def _bool_rate(outcomes: Sequence[ProbeOutcome], attribute: str) -> float:
    if not outcomes:
        return 0.0
    return sum(1.0 if bool(getattr(outcome, attribute)) else 0.0 for outcome in outcomes) / len(
        outcomes
    )


def _same_group_competitor(
    world: SingleRouteWorld,
    target: MemoryRecord,
    route_index: int,
) -> MemoryRecord:
    target_anchor = target.binding(route_index).anchor_concept_id
    candidates = [
        memory
        for memory in world.memories
        if memory.memory_id != target.memory_id
        and memory.binding(route_index).anchor_concept_id == target_anchor
    ]
    if not candidates:
        raise RuntimeError("Same-group conflict requires route groups larger than one.")
    return min(candidates, key=lambda memory: memory.memory_id)


def _foreign_group_competitor(
    world: SingleRouteWorld,
    target: MemoryRecord,
    route_index: int,
) -> MemoryRecord:
    target_anchor = target.binding(route_index).anchor_concept_id
    candidates = [
        memory
        for memory in world.memories
        if memory.binding(route_index).anchor_concept_id != target_anchor
    ]
    if not candidates:
        raise RuntimeError("Foreign-group conflict requires at least two anchor groups.")
    return min(candidates, key=lambda memory: memory.memory_id)


def _competitor_top1_rate(
    retriever: SingleRouteRetriever,
    route_index: int,
    cues: Sequence[RetrievalCue],
    competitor_ids: Sequence[str],
) -> float:
    if len(cues) != len(competitor_ids):
        raise ValueError("Competitor identities must align with cues.")
    wins = 0
    for cue, competitor_id in zip(cues, competitor_ids, strict=True):
        field = retriever.rank(cue, route_index=route_index, field_size=1)
        if field[0].memory_id == competitor_id:
            wins += 1
    return wins / len(cues) if cues else 0.0


def _diagnostic_integrity(
    field_sweep: Sequence[FieldSweepMetric],
    route_metrics: Sequence[RouteEnvelopeMetric],
    *,
    tolerance: float = 1e-12,
) -> bool:
    chance = FIELD_SIZE / MEMORY_COUNT
    for metric in field_sweep:
        if abs(metric.partial_hit - metric.expected_partial_hit) > tolerance:
            return False
    for metric in route_metrics:
        if abs(metric.detail_only_top1 - 1.0) > tolerance:
            return False
        if abs(metric.detail_only_hit_at_32 - 1.0) > tolerance:
            return False
        if abs(metric.same_group_conflict_target_top1 - 0.0) > tolerance:
            return False
        if abs(metric.same_group_conflict_competitor_top1 - 1.0) > tolerance:
            return False
        if abs(metric.near_id_hit_at_32 - chance) > tolerance:
            return False
        if abs(metric.alias_hit_at_32 - chance) > tolerance:
            return False
        for hit in metric.unbound_noise_hit_at_32.values():
            if abs(hit - metric.partial_reference_hit_at_32) > tolerance:
                return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Run R0 exact-match operating-envelope diagnostic")
    parser.add_argument("--seed", type=int, default=1701)
    args = parser.parse_args()
    print(json.dumps(run_exact_match_envelope(seed=args.seed), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
