from dataclasses import replace

import pytest

from experiments.hct2_retrospective_audit import (
    ALL_ORDERS,
    RELATION_VARIANTS,
    answer_independent_selectivity_order,
    relation_variant_world,
    run_hct2_retrospective_audit,
    shifted_relation_world,
)
from experiments.hippocampal_ordered_context import generate_world

pytestmark = pytest.mark.audit


@pytest.fixture(scope="module")
def small_report() -> dict[str, object]:
    return run_hct2_retrospective_audit(
        training_seeds=range(70000, 70020),
        evaluation_seeds=range(71000, 71008),
        split_label="test_slice",
    )


def test_audit_is_retrospective_and_cannot_upgrade_hct2(
    small_report: dict[str, object],
) -> None:
    report = small_report

    assert report["artifact_class"] == "RETROSPECTIVE_AUDIT"
    assert report["can_upgrade_hct2"] is False
    assert report["hct2_v1_modified"] is False
    assert report["split"] == "test_slice"


def test_order_landscape_exhausts_all_24_channel_permutations(
    small_report: dict[str, object],
) -> None:
    landscape = small_report["order_landscape"]

    observed = {tuple(row["order"]) for row in landscape}
    assert len(landscape) == 24
    assert observed == set(ALL_ORDERS)


def test_answer_independent_selectivity_order_ignores_correct_index() -> None:
    worlds = tuple(generate_world(seed) for seed in range(70000, 70008))
    relabeled = tuple(
        replace(
            world,
            correct_index=(world.correct_index + 17) % len(world.candidates),
        )
        for world in worlds
    )

    original = answer_independent_selectivity_order(worlds)
    changed_truth = answer_independent_selectivity_order(relabeled)

    assert changed_truth == original


def test_shifted_relations_preserve_graph_structure_and_weights() -> None:
    world = generate_world(71003)
    shifted = shifted_relation_world(world)

    assert shifted.candidates == world.candidates
    assert shifted.initial_cue == world.initial_cue
    assert shifted.late_cue == world.late_cue
    assert shifted.correct_index == world.correct_index

    assert len(shifted.excitation) == len(world.excitation)
    assert len(shifted.inhibition) == len(world.inhibition)
    assert sorted(weight for _, _, weight in shifted.excitation) == sorted(
        weight for _, _, weight in world.excitation
    )
    assert sorted(weight for _, _, weight in shifted.inhibition) == sorted(
        weight for _, _, weight in world.inhibition
    )
    assert {(source, target) for source, target, _ in shifted.excitation} != {
        (source, target) for source, target, _ in world.excitation
    }


def test_relation_variants_change_only_relation_structure() -> None:
    world = generate_world(71004)

    for variant in RELATION_VARIANTS:
        changed = relation_variant_world(world, variant)
        assert changed.candidates == world.candidates
        assert changed.initial_cue == world.initial_cue
        assert changed.late_cue == world.late_cue
        assert changed.correct_index == world.correct_index

    none = relation_variant_world(world, "no_relations")
    assert none.excitation == tuple()
    assert none.inhibition == tuple()


def test_relation_audit_holds_taper_survival_and_context_cost_constant(
    small_report: dict[str, object],
) -> None:
    metrics = small_report["relation_alignment"]

    assert {row["variant"] for row in metrics} == set(RELATION_VARIANTS)
    survival = {row["final_survival_rate"] for row in metrics}
    context_cost = {row["mean_context_feature_evaluations"] for row in metrics}

    assert len(survival) == 1
    assert len(context_cost) == 1


def test_audit_reports_learned_and_answer_independent_orders_without_outcome_gate(
    small_report: dict[str, object],
) -> None:
    summary = small_report["order_summary"]

    assert sorted(summary["learned_order"]) == [0, 1, 2, 3]
    assert sorted(summary["answer_independent_selectivity_order"]) == [0, 1, 2, 3]
    assert len(summary["training_mean_matching_fraction_by_channel"]) == 4
    assert 1 <= summary["orders_with_identical_learned_good_behavior"] <= 24
    rank = summary["learned_eval_rank_among_identical_behavior_orders"]
    assert rank is None or 1 <= rank <= 24
