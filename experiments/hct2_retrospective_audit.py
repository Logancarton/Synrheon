"""Retrospective audit of the already-observed HCT-2 v1 synthetic result.

This module does not modify HCT-2 v1. It imports the frozen generator, taper,
learner, and recurrent solver and asks two diagnostic questions:

1. Where does the learned context order sit among all 24 possible orders?
2. How sensitive is the recurrence result to answer-aligned relation structure?

The output is retrospective diagnostic evidence only. It cannot upgrade HCT-2.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from itertools import permutations
from statistics import mean, median
from typing import Iterable, Sequence
import argparse
import json

from experiments.hippocampal_ordered_context import (
    CHANNEL_TO_DEPTH,
    DEFAULT_RECURRENCE_WIDTH,
    DEVELOPMENT_SEEDS,
    FINAL_SEEDS,
    QUICK_DEVELOPMENT_SEEDS,
    TRAIN_SEEDS,
    ContextWorld,
    LearnedParameters,
    SolveResult,
    generate_world,
    learn_parameters,
    recurrent_solve,
    sparse_context_cascade,
)

AUDIT_ID = "hct2-retrospective-audit-v1"
RELATION_VARIANTS = ("original", "no_relations", "shifted_relations")
ALL_ORDERS = tuple(permutations(range(4)))


@dataclass(frozen=True, slots=True)
class OrderWorldOutcome:
    good_behavior: bool
    correct: bool
    committed: bool
    final_survival: bool
    context_feature_evaluations: int
    initial_reversal_suppressed: bool | None
    reversal_reactivated: bool | None


@dataclass(frozen=True, slots=True)
class OrderMetric:
    order: tuple[int, ...]
    depth_order: tuple[int, ...]
    episodes: int
    good_behavior_rate: float
    correct_rate: float
    commit_rate: float
    final_survival_rate: float
    mean_context_feature_evaluations: float
    reversal_suppression_cases: int
    reversal_reactivation_rate: float | None

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["order"] = list(self.order)
        data["depth_order"] = list(self.depth_order)
        return data


@dataclass(frozen=True, slots=True)
class RelationWorldOutcome:
    good_behavior: bool
    correct: bool
    committed: bool
    final_survival: bool
    context_feature_evaluations: int


@dataclass(frozen=True, slots=True)
class RelationMetric:
    variant: str
    episodes: int
    good_behavior_rate: float
    correct_rate: float
    commit_rate: float
    final_survival_rate: float
    mean_context_feature_evaluations: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def answer_independent_selectivity_order(
    worlds: Sequence[ContextWorld],
) -> tuple[tuple[int, ...], tuple[float, ...]]:
    """Order channels by average cue selectivity without using outcome identity.

    Lower matching fraction means the channel narrows the candidate field more strongly.
    The function deliberately never reads ``correct_index``.
    """

    if not worlds:
        raise ValueError("At least one world is required.")

    fractions: list[list[float]] = [[] for _ in range(4)]
    for world in worlds:
        cue = world.late_cue or world.initial_cue
        candidate_count = len(world.candidates)
        for channel in range(4):
            matching = sum(
                1
                for candidate in world.candidates
                if candidate.context_tokens[channel] == cue[channel]
            )
            fractions[channel].append(matching / candidate_count)

    averages = tuple(mean(values) for values in fractions)
    order = tuple(sorted(range(4), key=lambda channel: (averages[channel], channel)))
    return order, averages


def shifted_relation_world(world: ContextWorld) -> ContextWorld:
    """Cyclically relabel relation endpoints while preserving graph topology/weights."""

    count = len(world.candidates)
    if count < 2:
        raise ValueError("Shifted relations require at least two candidates.")
    shift = (world.seed % (count - 1)) + 1

    excitation = tuple(
        ((source + shift) % count, (target + shift) % count, weight)
        for source, target, weight in world.excitation
    )
    inhibition = tuple(
        ((source + shift) % count, (target + shift) % count, weight)
        for source, target, weight in world.inhibition
    )
    return replace(world, excitation=excitation, inhibition=inhibition)


def relation_variant_world(world: ContextWorld, variant: str) -> ContextWorld:
    if variant == "original":
        return world
    if variant == "no_relations":
        return replace(world, excitation=tuple(), inhibition=tuple())
    if variant == "shifted_relations":
        return shifted_relation_world(world)
    raise ValueError(f"Unknown relation variant: {variant}")


def _good_behavior(world: ContextWorld, result: SolveResult) -> bool:
    if world.world_type == "unresolved_branch":
        return not result.committed
    return result.committed and result.winner_index == world.correct_index


def _run_order_world(
    world: ContextWorld,
    parameters: LearnedParameters,
    order: tuple[int, ...],
) -> OrderWorldOutcome:
    initial_taper = sparse_context_cascade(
        world,
        parameters,
        world.initial_cue,
        order=order,
    )
    context_evaluations = initial_taper.context_feature_evaluations
    initial = recurrent_solve(
        world,
        initial_taper.activation,
        parameters,
        width=DEFAULT_RECURRENCE_WIDTH,
    )
    final = initial
    initial_suppressed: bool | None = None
    reactivated: bool | None = None

    if world.late_cue is not None:
        initial_suppressed = world.correct_index not in initial.selected
        reopened = sparse_context_cascade(
            world,
            parameters,
            world.late_cue,
            order=order,
        )
        context_evaluations += reopened.context_feature_evaluations
        final = recurrent_solve(
            world,
            reopened.activation,
            parameters,
            width=DEFAULT_RECURRENCE_WIDTH,
        )
        if initial_suppressed:
            reactivated = (
                world.correct_index in final.selected
                and final.winner_index == world.correct_index
            )

    return OrderWorldOutcome(
        good_behavior=_good_behavior(world, final),
        correct=final.winner_index == world.correct_index,
        committed=final.committed,
        final_survival=world.correct_index in final.selected,
        context_feature_evaluations=context_evaluations,
        initial_reversal_suppressed=initial_suppressed,
        reversal_reactivated=reactivated,
    )


def _summarize_order(
    order: tuple[int, ...],
    rows: Sequence[OrderWorldOutcome],
) -> OrderMetric:
    suppression_rows = [row for row in rows if row.initial_reversal_suppressed is True]
    reactivation_rows = [
        row for row in suppression_rows if row.reversal_reactivated is not None
    ]
    return OrderMetric(
        order=order,
        depth_order=tuple(CHANNEL_TO_DEPTH[channel] for channel in order),
        episodes=len(rows),
        good_behavior_rate=_bool_mean(rows, "good_behavior"),
        correct_rate=_bool_mean(rows, "correct"),
        commit_rate=_bool_mean(rows, "committed"),
        final_survival_rate=_bool_mean(rows, "final_survival"),
        mean_context_feature_evaluations=mean(
            row.context_feature_evaluations for row in rows
        ),
        reversal_suppression_cases=len(suppression_rows),
        reversal_reactivation_rate=(
            mean(1.0 if row.reversal_reactivated else 0.0 for row in reactivation_rows)
            if reactivation_rows
            else None
        ),
    )


def _run_relation_world(
    world: ContextWorld,
    parameters: LearnedParameters,
    variant: str,
) -> RelationWorldOutcome:
    relation_world = relation_variant_world(world, variant)

    initial_taper = sparse_context_cascade(
        relation_world,
        parameters,
        relation_world.initial_cue,
        order=parameters.context_order,
    )
    context_evaluations = initial_taper.context_feature_evaluations
    final = recurrent_solve(
        relation_world,
        initial_taper.activation,
        parameters,
        width=DEFAULT_RECURRENCE_WIDTH,
    )

    if relation_world.late_cue is not None:
        reopened = sparse_context_cascade(
            relation_world,
            parameters,
            relation_world.late_cue,
            order=parameters.context_order,
        )
        context_evaluations += reopened.context_feature_evaluations
        final = recurrent_solve(
            relation_world,
            reopened.activation,
            parameters,
            width=DEFAULT_RECURRENCE_WIDTH,
        )

    return RelationWorldOutcome(
        good_behavior=_good_behavior(relation_world, final),
        correct=final.winner_index == relation_world.correct_index,
        committed=final.committed,
        final_survival=relation_world.correct_index in final.selected,
        context_feature_evaluations=context_evaluations,
    )


def _summarize_relation(
    variant: str,
    rows: Sequence[RelationWorldOutcome],
) -> RelationMetric:
    return RelationMetric(
        variant=variant,
        episodes=len(rows),
        good_behavior_rate=_bool_mean(rows, "good_behavior"),
        correct_rate=_bool_mean(rows, "correct"),
        commit_rate=_bool_mean(rows, "committed"),
        final_survival_rate=_bool_mean(rows, "final_survival"),
        mean_context_feature_evaluations=mean(
            row.context_feature_evaluations for row in rows
        ),
    )


def _bool_mean(rows: Sequence[object], attribute: str) -> float:
    if not rows:
        return 0.0
    return mean(1.0 if bool(getattr(row, attribute)) else 0.0 for row in rows)


def audit_order_landscape(
    worlds: Sequence[ContextWorld],
    parameters: LearnedParameters,
) -> tuple[list[OrderMetric], dict[str, object]]:
    metrics: list[OrderMetric] = []
    for order in ALL_ORDERS:
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
    learned_rank_same_behavior = (
        same_behavior_sorted.index(learned) + 1 if learned in same_behavior_sorted else None
    )

    all_eval_values = [metric.mean_context_feature_evaluations for metric in metrics]
    summary = {
        "learned_order": list(parameters.context_order),
        "learned_depth_order": [
            CHANNEL_TO_DEPTH[channel] for channel in parameters.context_order
        ],
        "original_fixed_order": [0, 1, 2, 3],
        "learned_good_behavior_rate": learned.good_behavior_rate,
        "learned_mean_context_feature_evaluations": (
            learned.mean_context_feature_evaluations
        ),
        "fixed_good_behavior_rate": fixed.good_behavior_rate,
        "fixed_mean_context_feature_evaluations": fixed.mean_context_feature_evaluations,
        "orders_with_identical_learned_good_behavior": len(same_behavior),
        "learned_eval_rank_among_identical_behavior_orders": learned_rank_same_behavior,
        "best_mean_context_feature_evaluations": min(all_eval_values),
        "median_mean_context_feature_evaluations": median(all_eval_values),
        "worst_mean_context_feature_evaluations": max(all_eval_values),
    }
    return metrics, summary


def audit_relation_alignment(
    worlds: Sequence[ContextWorld],
    parameters: LearnedParameters,
) -> list[RelationMetric]:
    metrics: list[RelationMetric] = []
    for variant in RELATION_VARIANTS:
        rows = [_run_relation_world(world, parameters, variant) for world in worlds]
        metrics.append(_summarize_relation(variant, rows))
    return metrics


def run_hct2_retrospective_audit(
    *,
    evaluation_seeds: Iterable[int] = DEVELOPMENT_SEEDS,
    training_seeds: Iterable[int] = TRAIN_SEEDS,
    split_label: str = "development",
) -> dict[str, object]:
    training_worlds = tuple(generate_world(seed) for seed in training_seeds)
    evaluation_worlds = tuple(generate_world(seed) for seed in evaluation_seeds)
    if not training_worlds:
        raise ValueError("Training seed set is empty.")
    if not evaluation_worlds:
        raise ValueError("Evaluation seed set is empty.")

    parameters = learn_parameters(world.seed for world in training_worlds)
    selectivity_order, selectivity_fractions = answer_independent_selectivity_order(
        training_worlds
    )

    order_metrics, order_summary = audit_order_landscape(evaluation_worlds, parameters)
    relation_metrics = audit_relation_alignment(evaluation_worlds, parameters)

    order_by_tuple = {metric.order: metric for metric in order_metrics}
    selectivity_metric = order_by_tuple[selectivity_order]
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

    return {
        "audit": AUDIT_ID,
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
            "order_audit": (
                "describes where the historical learned order sits among all 24 orders"
            ),
            "selectivity_comparator": (
                "uses cue/candidate match frequency only; no correct identity"
            ),
            "relation_audit": (
                "tests dependence on graph-to-candidate alignment; shifted graph is not a "
                "realistic-world model"
            ),
            "historical_final": (
                "if selected, remains retrospective because HCT-2 final results were "
                "already observed"
            ),
        },
    }


def _select_seeds(args: argparse.Namespace) -> tuple[Iterable[int], str]:
    if args.quick:
        return QUICK_DEVELOPMENT_SEEDS, "quick_development"
    if args.historical_final:
        return FINAL_SEEDS, "historical_final_retrospective"
    return DEVELOPMENT_SEEDS, "development"


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit historical HCT-2 v1")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--quick", action="store_true")
    mode.add_argument("--development", action="store_true")
    mode.add_argument("--historical-final", action="store_true")
    args = parser.parse_args()

    evaluation_seeds, split_label = _select_seeds(args)
    report = run_hct2_retrospective_audit(
        evaluation_seeds=evaluation_seeds,
        training_seeds=TRAIN_SEEDS,
        split_label=split_label,
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
