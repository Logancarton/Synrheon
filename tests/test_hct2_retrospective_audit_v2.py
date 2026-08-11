from __future__ import annotations

import pytest

from experiments.hct2_retrospective_audit_v2 import (
    RELATION_VARIANTS_V2,
    audit_difficulty_sweep,
    audit_order_equivalence,
    audit_relation_variants_detailed,
    random_relation_world,
)
from experiments.hct2_retrospective_audit_runner import learn_parameters_from_worlds
from experiments.hippocampal_ordered_context import generate_world

pytestmark = pytest.mark.audit


def test_order_learning_equivalence_is_classified_as_specification() -> None:
    report = audit_order_equivalence(
        training_blocks=(
            tuple(range(70000, 70006)),
            tuple(range(70006, 70012)),
        )
    )

    assert report["classification"] == "SPECIFICATION_EQUIVALENCE"
    assert report["all_blocks_identical"] is True
    for row in report["blocks"]:
        assert row["correct_matches_every_channel"] is True
        assert row["orders_identical"] is True


def test_random_relations_preserve_counts_weights_and_nonrelation_inputs() -> None:
    world = generate_world(71003)
    randomized = random_relation_world(world)

    assert randomized.candidates == world.candidates
    assert randomized.initial_cue == world.initial_cue
    assert randomized.late_cue == world.late_cue
    assert randomized.correct_index == world.correct_index

    assert len(randomized.excitation) == len(world.excitation)
    assert len(randomized.inhibition) == len(world.inhibition)
    assert sorted(weight for _, _, weight in randomized.excitation) == sorted(
        weight for _, _, weight in world.excitation
    )
    assert sorted(weight for _, _, weight in randomized.inhibition) == sorted(
        weight for _, _, weight in world.inhibition
    )
    assert {(s, t) for s, t, _ in randomized.excitation} != {
        (s, t) for s, t, _ in world.excitation
    }


def test_relation_audit_v2_reports_four_variants_and_failure_overlap() -> None:
    training_worlds = tuple(generate_world(seed) for seed in range(70000, 70008))
    parameters = learn_parameters_from_worlds(training_worlds)
    worlds = tuple(generate_world(seed) for seed in range(71000, 71004))

    metrics, detail = audit_relation_variants_detailed(
        worlds,
        parameters,
        progress=False,
    )

    assert {metric.variant for metric in metrics} == set(RELATION_VARIANTS_V2)
    assert len(detail["per_world_rows"]) == 4
    assert len(detail["failure_overlap"]) == 3

    survival_rates = {metric.final_survival_rate for metric in metrics}
    context_costs = {metric.mean_context_feature_evaluations for metric in metrics}
    assert len(survival_rates) == 1
    assert len(context_costs) == 1


def test_difficulty_sweep_never_requires_behavioral_difference() -> None:
    training_worlds = tuple(generate_world(seed) for seed in range(70000, 70008))
    parameters = learn_parameters_from_worlds(training_worlds)

    metrics = audit_difficulty_sweep(
        parameters,
        evaluation_seeds=(71000, 71001),
        candidate_counts=(512, 640),
        progress=False,
    )

    assert [metric.candidate_count for metric in metrics] == [512, 640]
    for metric in metrics:
        assert metric.evaluation_worlds == 2
        assert 0.0 <= metric.worst_good_behavior_rate <= 1.0
        assert 0.0 <= metric.best_good_behavior_rate <= 1.0
        assert metric.worst_good_behavior_rate <= metric.best_good_behavior_rate
        assert metric.distinct_good_behavior_rates >= 1
        assert isinstance(metric.behavior_has_resolution, bool)
