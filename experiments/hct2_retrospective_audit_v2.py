"""HCT-2 retrospective audit v2.

This audit cannot upgrade historical HCT-2 evidence. It sharpens the retrospective
questions after the v1 smoke run without modifying HCT-2's frozen generator, learner,
taper, recurrent solver, or historical verdict.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from statistics import mean, median
from typing import Iterable, Sequence
import argparse
import json
import random
import sys

from experiments.hct2_retrospective_audit import (
    ALL_ORDERS,
    _run_order_world,
    _summarize_order,
    answer_independent_selectivity_order,
    relation_variant_world,
)
from experiments.hct2_retrospective_audit_runner import learn_parameters_from_worlds
from experiments.hippocampal_ordered_context import (
    DEFAULT_RECURRENCE_WIDTH,
    ContextWorld,
    LearnedParameters,
    generate_world,
    recurrent_solve,
    sparse_context_cascade,
)

AUDIT_ID = "hct2-retrospective-audit-v2"
CANDIDATE_COUNT_SWEEP = (512, 768, 1024, 1536)
RESOLUTION_EVALUATION_SEEDS = tuple(range(71000, 71008))
RELATION_VARIANTS_V2 = (
    "original",
    "no_relations",
    "shifted_relations",
    "random_relations",
)
EQUIVALENCE_TRAINING_BLOCKS = tuple(
    tuple(range(start, start + 20)) for start in range(70000, 70120, 20)
)


@dataclass(frozen=True, slots=True)
class DifficultyMetric:
    candidate_count: int
    evaluation_worlds: int
    best_good_behavior_rate: float
    median_good_behavior_rate: float
    worst_good_behavior_rate: float
    distinct_good_behavior_rates: int
    behavior_has_resolution: bool
    learned_order_good_behavior_rate: float
    learned_order_mean_context_feature_evaluations: float
    best_cost_at_learned_behavior: float
    best_mean_context_feature_evaluations: float
    median_mean_context_feature_evaluations: float
    worst_mean_context_feature_evaluations: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class RelationVariantMetric:
    variant: str
    episodes: int
    correct_rate: float
    commit_rate: float
    good_behavior_rate: float
    final_survival_rate: float
    mean_context_feature_evaluations: float
    failing_world_seeds: tuple[int, ...]

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["failing_world_seeds"] = list(self.failing_world_seeds)
        return data


def _progress(message: str, *, enabled: bool) -> None:
    if enabled:
        print(message, file=sys.stderr, flush=True)


def _random_unique_edges(
    *,
    count: int,
    weights: Sequence[float],
    seed: int,
) -> tuple[tuple[int, int, float], ...]:
    """Assign the frozen weight multiset to unique random directed endpoints."""

    if len(weights) > count * count:
        raise ValueError("Too many edges for unique random endpoints.")
    rng = random.Random(seed)
    codes = rng.sample(range(count * count), len(weights))
    return tuple(
        (code // count, code % count, weight)
        for code, weight in zip(codes, weights, strict=True)
    )


def random_relation_world(world: ContextWorld) -> ContextWorld:
    """Destroy relation topology/alignment while preserving edge counts and weights."""

    count = len(world.candidates)
    excitation = _random_unique_edges(
        count=count,
        weights=tuple(weight for _, _, weight in world.excitation),
        seed=world.seed * 17 + 91_001,
    )
    inhibition = _random_unique_edges(
        count=count,
        weights=tuple(weight for _, _, weight in world.inhibition),
        seed=world.seed * 31 + 193_003,
    )
    return replace(world, excitation=excitation, inhibition=inhibition)


def relation_variant_world_v2(world: ContextWorld, variant: str) -> ContextWorld:
    if variant == "random_relations":
        return random_relation_world(world)
    return relation_variant_world(world, variant)


def _good_behavior(world: ContextWorld, *, winner: int, committed: bool) -> bool:
    if world.world_type == "unresolved_branch":
        return not committed
    return committed and winner == world.correct_index


def audit_order_equivalence(
    training_blocks: Sequence[Sequence[int]] = EQUIVALENCE_TRAINING_BLOCKS,
) -> dict[str, object]:
    """Verify the specification-level identity between learned utility and selectivity."""

    rows: list[dict[str, object]] = []
    for block_index, seeds in enumerate(training_blocks):
        worlds = tuple(generate_world(seed) for seed in seeds)
        parameters = learn_parameters_from_worlds(worlds)
        selectivity_order, fractions = answer_independent_selectivity_order(worlds)

        correct_matches_all_channels = all(
            all(
                world.candidates[world.correct_index].context_tokens[channel]
                == (world.late_cue or world.initial_cue)[channel]
                for channel in range(4)
            )
            for world in worlds
        )
        derived_utilities = tuple(1.0 - fraction for fraction in fractions)
        derived_order = tuple(
            sorted(
                range(4),
                key=lambda channel: (-derived_utilities[channel], channel),
            )
        )

        rows.append(
            {
                "block_index": block_index,
                "seed_start": min(seeds),
                "seed_end": max(seeds),
                "worlds": len(worlds),
                "correct_matches_every_channel": correct_matches_all_channels,
                "learned_order": list(parameters.context_order),
                "answer_independent_selectivity_order": list(selectivity_order),
                "derived_order_from_1_minus_match_fraction": list(derived_order),
                "mean_matching_fraction_by_channel": list(fractions),
                "orders_identical": (
                    parameters.context_order == selectivity_order == derived_order
                ),
            }
        )

    return {
        "classification": "SPECIFICATION_EQUIVALENCE",
        "identity": "utility(channel) = 1 - mean_matching_fraction(channel)",
        "blocks": rows,
        "all_blocks_identical": all(bool(row["orders_identical"]) for row in rows),
    }


def audit_difficulty_sweep(
    parameters: LearnedParameters,
    *,
    evaluation_seeds: Sequence[int] = RESOLUTION_EVALUATION_SEEDS,
    candidate_counts: Sequence[int] = CANDIDATE_COUNT_SWEEP,
    progress: bool = True,
) -> list[DifficultyMetric]:
    """Find whether order behavior becomes measurable as the candidate field grows."""

    metrics: list[DifficultyMetric] = []
    total_counts = len(candidate_counts)
    for count_number, candidate_count in enumerate(candidate_counts, start=1):
        _progress(
            f"[difficulty {count_number}/{total_counts}] generating "
            f"{len(evaluation_seeds)} worlds at candidate_count={candidate_count}",
            enabled=progress,
        )
        worlds = tuple(
            generate_world(seed, candidate_count=candidate_count)
            for seed in evaluation_seeds
        )

        order_metrics = []
        for order_number, order in enumerate(ALL_ORDERS, start=1):
            _progress(
                f"  [order {order_number:02d}/24] {order}",
                enabled=progress,
            )
            outcomes = [_run_order_world(world, parameters, order) for world in worlds]
            order_metrics.append(_summarize_order(order, outcomes))

        learned = next(
            metric for metric in order_metrics if metric.order == parameters.context_order
        )
        good_values = [metric.good_behavior_rate for metric in order_metrics]
        eval_values = [metric.mean_context_feature_evaluations for metric in order_metrics]
        same_learned_behavior = [
            metric
            for metric in order_metrics
            if abs(metric.good_behavior_rate - learned.good_behavior_rate) <= 1e-12
        ]

        metrics.append(
            DifficultyMetric(
                candidate_count=candidate_count,
                evaluation_worlds=len(worlds),
                best_good_behavior_rate=max(good_values),
                median_good_behavior_rate=median(good_values),
                worst_good_behavior_rate=min(good_values),
                distinct_good_behavior_rates=len(set(good_values)),
                behavior_has_resolution=max(good_values) > min(good_values),
                learned_order_good_behavior_rate=learned.good_behavior_rate,
                learned_order_mean_context_feature_evaluations=(
                    learned.mean_context_feature_evaluations
                ),
                best_cost_at_learned_behavior=min(
                    metric.mean_context_feature_evaluations
                    for metric in same_learned_behavior
                ),
                best_mean_context_feature_evaluations=min(eval_values),
                median_mean_context_feature_evaluations=median(eval_values),
                worst_mean_context_feature_evaluations=max(eval_values),
            )
        )
    return metrics


def audit_relation_variants_detailed(
    worlds: Sequence[ContextWorld],
    parameters: LearnedParameters,
    *,
    progress: bool = True,
) -> tuple[list[RelationVariantMetric], dict[str, object]]:
    """Hold taper fixed and compare alignment/topology with per-world failure identity."""

    rows: dict[str, list[dict[str, object]]] = {
        variant: [] for variant in RELATION_VARIANTS_V2
    }

    for world_number, world in enumerate(worlds, start=1):
        if progress:
            _progress(
                f"[relations {world_number}/{len(worlds)}] seed={world.seed}",
                enabled=True,
            )

        taper = sparse_context_cascade(
            world,
            parameters,
            world.initial_cue,
            order=parameters.context_order,
        )
        context_evaluations = taper.context_feature_evaluations
        if world.late_cue is not None:
            taper = sparse_context_cascade(
                world,
                parameters,
                world.late_cue,
                order=parameters.context_order,
            )
            context_evaluations += taper.context_feature_evaluations

        for variant in RELATION_VARIANTS_V2:
            relation_world = relation_variant_world_v2(world, variant)
            result = recurrent_solve(
                relation_world,
                taper.activation,
                parameters,
                width=DEFAULT_RECURRENCE_WIDTH,
            )
            good = _good_behavior(
                relation_world,
                winner=result.winner_index,
                committed=result.committed,
            )
            rows[variant].append(
                {
                    "seed": world.seed,
                    "world_type": world.world_type,
                    "correct": result.winner_index == world.correct_index,
                    "committed": result.committed,
                    "good_behavior": good,
                    "final_survival": world.correct_index in result.selected,
                    "context_feature_evaluations": context_evaluations,
                }
            )

    metrics: list[RelationVariantMetric] = []
    failure_sets: dict[str, set[int]] = {}
    for variant in RELATION_VARIANTS_V2:
        variant_rows = rows[variant]
        failures = {
            int(row["seed"])
            for row in variant_rows
            if not bool(row["good_behavior"])
        }
        failure_sets[variant] = failures
        metrics.append(
            RelationVariantMetric(
                variant=variant,
                episodes=len(variant_rows),
                correct_rate=mean(
                    1.0 if bool(row["correct"]) else 0.0 for row in variant_rows
                ),
                commit_rate=mean(
                    1.0 if bool(row["committed"]) else 0.0 for row in variant_rows
                ),
                good_behavior_rate=mean(
                    1.0 if bool(row["good_behavior"]) else 0.0 for row in variant_rows
                ),
                final_survival_rate=mean(
                    1.0 if bool(row["final_survival"]) else 0.0 for row in variant_rows
                ),
                mean_context_feature_evaluations=mean(
                    int(row["context_feature_evaluations"]) for row in variant_rows
                ),
                failing_world_seeds=tuple(sorted(failures)),
            )
        )

    pairs = (
        ("no_relations", "shifted_relations"),
        ("no_relations", "random_relations"),
        ("shifted_relations", "random_relations"),
    )
    overlap_rows: list[dict[str, object]] = []
    for left_name, right_name in pairs:
        left = failure_sets[left_name]
        right = failure_sets[right_name]
        union = left | right
        intersection = left & right
        overlap_rows.append(
            {
                "left": left_name,
                "right": right_name,
                "left_failures": len(left),
                "right_failures": len(right),
                "intersection": len(intersection),
                "union": len(union),
                "jaccard": len(intersection) / len(union) if union else 1.0,
                "exact_same_failure_set": left == right,
                "intersection_seeds": sorted(intersection),
            }
        )

    return metrics, {
        "per_world_rows": rows,
        "failure_overlap": overlap_rows,
    }


def run_audit_v2(*, progress: bool = True) -> dict[str, object]:
    _progress("[1/4] checking order-learning specification equivalence", enabled=progress)
    equivalence = audit_order_equivalence()

    _progress("[2/4] learning original HCT-2 parameters", enabled=progress)
    training_worlds = tuple(generate_world(seed) for seed in range(70000, 70500))
    parameters = learn_parameters_from_worlds(training_worlds)

    _progress("[3/4] running behavioral-resolution field-size sweep", enabled=progress)
    difficulty = audit_difficulty_sweep(parameters, progress=progress)

    _progress("[4/4] running detailed relation audit at original field size", enabled=progress)
    relation_worlds = tuple(
        generate_world(seed, candidate_count=512)
        for seed in RESOLUTION_EVALUATION_SEEDS
    )
    relation_metrics, relation_detail = audit_relation_variants_detailed(
        relation_worlds,
        parameters,
        progress=progress,
    )

    resolved_counts = [
        metric.candidate_count for metric in difficulty if metric.behavior_has_resolution
    ]

    return {
        "audit": AUDIT_ID,
        "artifact_class": "RETROSPECTIVE_AUDIT",
        "can_upgrade_hct2": False,
        "hct2_v1_modified": False,
        "evaluation_status": "EXPLORATORY_RETROSPECTIVE",
        "order_learning_equivalence": equivalence,
        "difficulty_sweep": [metric.to_dict() for metric in difficulty],
        "first_behaviorally_resolved_candidate_count": (
            min(resolved_counts) if resolved_counts else None
        ),
        "relation_generation_provenance": {
            "uses_designated_correct_identity": True,
            "correct_receives_extra_excitation_outside_unresolved_worlds": True,
            "classification": "TRUTH_SHAPED_SYNTHETIC_RELATIONS",
        },
        "relation_variants": [metric.to_dict() for metric in relation_metrics],
        "relation_detail": relation_detail,
        "interpretation_boundary": {
            "order_equivalence": "specification consequence of HCT-2 learner/generator",
            "difficulty_sweep": "retrospective stress test; no confirmatory threshold",
            "relation_audit": "diagnoses dependence on synthetic relation alignment/topology",
            "historical_hct2": "unchanged; v2 may only narrow or downgrade interpretation",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run HCT-2 retrospective audit v2")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run_audit_v2(progress=not args.quiet), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
