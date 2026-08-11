"""Progress-visible, computation-reduced runner for the frozen HCT-2 retrospective audit.

This runner does not change HCT-2 v1 or the audit questions. It removes duplicate world
construction, reuses relation-independent taper results across relation variants, and
prints progress to stderr so a long development audit cannot look hung.

Smoke mode is an engineering check only. Quick/development remain retrospective audits.
"""

from __future__ import annotations

from dataclasses import asdict
from statistics import mean, median
from typing import Iterable, Sequence
import argparse
import json
import sys

from experiments.hct2_retrospective_audit import (
    ALL_ORDERS,
    AUDIT_ID,
    RELATION_VARIANTS,
    OrderMetric,
    RelationMetric,
    _good_behavior,
    _run_order_world,
    _summarize_order,
    answer_independent_selectivity_order,
    relation_variant_world,
)
from experiments.hippocampal_ordered_context import (
    CHANNEL_TO_DEPTH,
    DEFAULT_RECURRENCE_WIDTH,
    DEVELOPMENT_SEEDS,
    QUICK_DEVELOPMENT_SEEDS,
    TRAIN_SEEDS,
    ContextWorld,
    LearnedParameters,
    generate_world,
    learn_parameters,
    recurrent_solve,
    sparse_context_cascade,
)

SMOKE_TRAIN_SEEDS = range(70000, 70020)
SMOKE_EVALUATION_SEEDS = range(71000, 71008)


def _progress(message: str, *, enabled: bool) -> None:
    if enabled:
        print(message, file=sys.stderr, flush=True)


def learn_parameters_from_worlds(worlds: Sequence[ContextWorld]) -> LearnedParameters:
    """Exact audit-local reproduction of the frozen HCT-2 learner over cached worlds."""

    if not worlds:
        raise ValueError("At least one training world is required.")

    resistance = [1.0, 1.0, 1.0, 1.0]
    utility_sums = [0.0, 0.0, 0.0, 0.0]

    for world in worlds:
        final_cue = world.late_cue or world.initial_cue
        for channel in range(4):
            correct_support = world.candidates[world.correct_index].evidence[channel]
            strongest_wrong = max(
                candidate.evidence[channel]
                for index, candidate in enumerate(world.candidates)
                if index != world.correct_index
            )
            updated = resistance[channel] + 0.025 * (
                strongest_wrong - correct_support
            )
            resistance[channel] = min(3.0, max(0.25, updated))

            matches = [
                1.0 if candidate.context_tokens[channel] == final_cue[channel] else 0.0
                for candidate in world.candidates
            ]
            utility_sums[channel] += matches[world.correct_index] - mean(matches)

    utility = [value / len(worlds) for value in utility_sums]
    average_utility = mean(utility)
    if average_utility <= 0.0:
        raise ValueError("Training did not produce positive context utility.")

    gains = tuple(value / average_utility for value in utility)
    order = tuple(
        sorted(range(4), key=lambda channel: utility[channel], reverse=True)
    )
    return LearnedParameters(
        evidence_resistance=tuple(resistance),
        context_gains=gains,
        context_order=order,
    )


def verify_cached_learner_equivalence() -> bool:
    """Check the cache-based learner against frozen v1 on a small identical seed slice."""

    seeds = range(70000, 70012)
    worlds = tuple(generate_world(seed) for seed in seeds)
    cached = learn_parameters_from_worlds(worlds)
    frozen = learn_parameters(seeds)
    return cached == frozen


def _order_landscape(
    worlds: Sequence[ContextWorld],
    parameters: LearnedParameters,
    *,
    progress: bool,
) -> tuple[list[OrderMetric], dict[str, object]]:
    metrics: list[OrderMetric] = []
    total = len(ALL_ORDERS)
    for number, order in enumerate(ALL_ORDERS, start=1):
        _progress(
            f"[order {number:02d}/{total}] evaluating {order}",
            enabled=progress,
        )
        rows = [_run_order_world(world, parameters, order) for world in worlds]
        metrics.append(_summarize_order(order, rows))

    by_order = {metric.order: metric for metric in metrics}
    learned = by_order[parameters.context_order]
    fixed = by_order[(0, 1, 2, 3)]
    same_behavior = [
        metric
        for metric in metrics
        if abs(metric.good_behavior_rate - learned.good_behavior_rate) <= 1e-12
    ]
    same_behavior_sorted = sorted(
        same_behavior,
        key=lambda metric: (metric.mean_context_feature_evaluations, metric.order),
    )
    learned_rank = same_behavior_sorted.index(learned) + 1
    eval_values = [metric.mean_context_feature_evaluations for metric in metrics]

    return metrics, {
        "learned_order": list(parameters.context_order),
        "learned_depth_order": [
            CHANNEL_TO_DEPTH[channel] for channel in parameters.context_order
        ],
        "original_fixed_order": [0, 1, 2, 3],
        "learned_good_behavior_rate": learned.good_behavior_rate,
        "learned_mean_context_feature_evaluations": learned.mean_context_feature_evaluations,
        "fixed_good_behavior_rate": fixed.good_behavior_rate,
        "fixed_mean_context_feature_evaluations": fixed.mean_context_feature_evaluations,
        "orders_with_identical_learned_good_behavior": len(same_behavior),
        "learned_eval_rank_among_identical_behavior_orders": learned_rank,
        "best_mean_context_feature_evaluations": min(eval_values),
        "median_mean_context_feature_evaluations": median(eval_values),
        "worst_mean_context_feature_evaluations": max(eval_values),
    }


def _relation_alignment_cached(
    worlds: Sequence[ContextWorld],
    parameters: LearnedParameters,
    *,
    progress: bool,
) -> list[RelationMetric]:
    """Reuse taper outputs because relation variants alter only relation endpoints."""

    rows_by_variant: dict[str, list[dict[str, object]]] = {
        variant: [] for variant in RELATION_VARIANTS
    }

    for world_number, world in enumerate(worlds, start=1):
        if progress and (world_number == 1 or world_number % 25 == 0):
            _progress(
                f"[relations] prepared {world_number}/{len(worlds)} worlds",
                enabled=True,
            )

        initial_taper = sparse_context_cascade(
            world,
            parameters,
            world.initial_cue,
            order=parameters.context_order,
        )
        final_taper = initial_taper
        context_evaluations = initial_taper.context_feature_evaluations
        if world.late_cue is not None:
            final_taper = sparse_context_cascade(
                world,
                parameters,
                world.late_cue,
                order=parameters.context_order,
            )
            context_evaluations += final_taper.context_feature_evaluations

        for variant in RELATION_VARIANTS:
            relation_world = relation_variant_world(world, variant)
            final = recurrent_solve(
                relation_world,
                final_taper.activation,
                parameters,
                width=DEFAULT_RECURRENCE_WIDTH,
            )
            rows_by_variant[variant].append(
                {
                    "good_behavior": _good_behavior(relation_world, final),
                    "correct": final.winner_index == relation_world.correct_index,
                    "committed": final.committed,
                    "final_survival": relation_world.correct_index in final.selected,
                    "context_feature_evaluations": context_evaluations,
                }
            )

    metrics: list[RelationMetric] = []
    for variant in RELATION_VARIANTS:
        rows = rows_by_variant[variant]
        metrics.append(
            RelationMetric(
                variant=variant,
                episodes=len(rows),
                good_behavior_rate=mean(
                    1.0 if bool(row["good_behavior"]) else 0.0 for row in rows
                ),
                correct_rate=mean(
                    1.0 if bool(row["correct"]) else 0.0 for row in rows
                ),
                commit_rate=mean(
                    1.0 if bool(row["committed"]) else 0.0 for row in rows
                ),
                final_survival_rate=mean(
                    1.0 if bool(row["final_survival"]) else 0.0 for row in rows
                ),
                mean_context_feature_evaluations=mean(
                    int(row["context_feature_evaluations"]) for row in rows
                ),
            )
        )
    return metrics


def run_visible_audit(
    *,
    training_seeds: Iterable[int],
    evaluation_seeds: Iterable[int],
    split_label: str,
    progress: bool = True,
) -> dict[str, object]:
    training_seed_tuple = tuple(training_seeds)
    evaluation_seed_tuple = tuple(evaluation_seeds)

    _progress(
        f"[1/5] generating {len(training_seed_tuple)} training worlds",
        enabled=progress,
    )
    training_worlds = tuple(generate_world(seed) for seed in training_seed_tuple)

    _progress("[2/5] learning frozen HCT-2 parameters from cached worlds", enabled=progress)
    parameters = learn_parameters_from_worlds(training_worlds)
    selectivity_order, selectivity_fractions = answer_independent_selectivity_order(
        training_worlds
    )

    _progress(
        f"[3/5] generating {len(evaluation_seed_tuple)} evaluation worlds",
        enabled=progress,
    )
    evaluation_worlds = tuple(generate_world(seed) for seed in evaluation_seed_tuple)

    _progress("[4/5] evaluating all 24 channel orders", enabled=progress)
    order_metrics, order_summary = _order_landscape(
        evaluation_worlds,
        parameters,
        progress=progress,
    )
    by_order = {metric.order: metric for metric in order_metrics}
    selectivity_metric = by_order[selectivity_order]
    order_summary.update(
        {
            "answer_independent_selectivity_order": list(selectivity_order),
            "answer_independent_selectivity_depth_order": [
                CHANNEL_TO_DEPTH[channel] for channel in selectivity_order
            ],
            "training_mean_matching_fraction_by_channel": list(selectivity_fractions),
            "selectivity_order_matches_supervised_order": (
                selectivity_order == parameters.context_order
            ),
            "selectivity_good_behavior_rate": selectivity_metric.good_behavior_rate,
            "selectivity_mean_context_feature_evaluations": (
                selectivity_metric.mean_context_feature_evaluations
            ),
        }
    )

    _progress("[5/5] auditing relation alignment with cached taper outputs", enabled=progress)
    relation_metrics = _relation_alignment_cached(
        evaluation_worlds,
        parameters,
        progress=progress,
    )

    return {
        "audit": AUDIT_ID,
        "runner": "hct2-retrospective-audit-visible-v1",
        "artifact_class": "RETROSPECTIVE_AUDIT",
        "evidence_level": "diagnostic analysis of already-observed synthetic HCT-2",
        "can_upgrade_hct2": False,
        "hct2_v1_modified": False,
        "split": split_label,
        "evaluation_worlds": len(evaluation_worlds),
        "training_worlds": len(training_worlds),
        "learned_parameters": parameters.to_dict(),
        "order_summary": order_summary,
        "order_landscape": [metric.to_dict() for metric in order_metrics],
        "relation_alignment": [metric.to_dict() for metric in relation_metrics],
        "interpretation_boundary": {
            "smoke": "engineering execution check only; never interpret scientifically",
            "audit": "retrospective only; cannot upgrade historical HCT-2 evidence",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run HCT-2 audit with visible progress")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--smoke", action="store_true")
    mode.add_argument("--quick", action="store_true")
    mode.add_argument("--development", action="store_true")
    args = parser.parse_args()

    if args.smoke:
        train = SMOKE_TRAIN_SEEDS
        evaluate = SMOKE_EVALUATION_SEEDS
        label = "smoke_engineering_only"
    elif args.quick:
        train = TRAIN_SEEDS
        evaluate = QUICK_DEVELOPMENT_SEEDS
        label = "quick_development"
    else:
        train = TRAIN_SEEDS
        evaluate = DEVELOPMENT_SEEDS
        label = "development"

    report = run_visible_audit(
        training_seeds=train,
        evaluation_seeds=evaluate,
        split_label=label,
        progress=True,
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
