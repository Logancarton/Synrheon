from __future__ import annotations

import pytest

from experiments.r0_single_route_access import (
    FIELD_SIZE,
    MEMORY_COUNT,
    ROUTE_GROUP_SIZES,
    LabeledProbe,
    RetrievalCue,
    SingleRouteRetriever,
    make_family_a_world,
    make_probe,
    run_single_route_assay,
)

pytestmark = pytest.mark.specification


def test_frozen_single_route_integrity_verdict_passes() -> None:
    result = run_single_route_assay(seed=1701)

    assert result["experiment"] == "r0-single-route-access-v1"
    assert result["generator_family"] == "A"
    assert result["memory_count"] == MEMORY_COUNT
    assert result["field_size"] == FIELD_SIZE
    assert result["route_group_sizes"] == list(ROUTE_GROUP_SIZES)
    assert result["verdict"] == "SINGLE_ROUTE_INSTRUMENT_VALID"


def test_full_cue_recovers_every_memory_top1_in_every_isolated_route() -> None:
    world = make_family_a_world(seed=1701)
    retriever = SingleRouteRetriever(world)

    for route_index in range(world.route_count):
        for memory in world.memories:
            probe = make_probe(world, memory, route_index=route_index, condition="full")
            field = retriever.rank(probe.cue, route_index=route_index)
            assert len(field) == FIELD_SIZE
            assert field[0].memory_id == memory.memory_id
            assert field[0].score == pytest.approx(1.0)


def test_partial_hit_at_32_is_exactly_limited_by_route_ambiguity() -> None:
    result = run_single_route_assay(seed=1701)
    metrics = result["route_metrics"]

    expected = {
        8: 1.0,
        16: 1.0,
        32: 1.0,
        64: 0.5,
    }
    for row in metrics:
        group_size = row["route_group_size"]
        assert row["partial_hit_at_32"] == pytest.approx(expected[group_size])
        assert row["partial_hit_at_32"] == pytest.approx(row["expected_partial_hit_at_32"])


def test_missing_cue_has_only_deterministic_zero_support_prefix_coverage() -> None:
    result = run_single_route_assay(seed=1701)
    expected_prefix_coverage = FIELD_SIZE / MEMORY_COUNT

    for row in result["route_metrics"]:
        assert row["missing_hit_at_32"] == pytest.approx(expected_prefix_coverage)
        assert row["expected_missing_hit_at_32"] == pytest.approx(expected_prefix_coverage)


def test_wrong_route_cue_cannot_borrow_evidence_from_another_route() -> None:
    world = make_family_a_world(seed=1701)
    retriever = SingleRouteRetriever(world)
    target = world.memories[0]

    probe = make_probe(world, target, route_index=0, condition="wrong_route")
    field = retriever.rank(probe.cue, route_index=0)

    assert len(field) == FIELD_SIZE
    assert all(candidate.score == 0.0 for candidate in field)

    result = run_single_route_assay(seed=1701)
    expected_prefix_coverage = FIELD_SIZE / MEMORY_COUNT
    for row in result["route_metrics"]:
        assert row["wrong_route_hit_at_32"] == pytest.approx(expected_prefix_coverage)


def test_foreign_route_concepts_do_not_change_single_route_ranking_order() -> None:
    world = make_family_a_world(seed=1701)
    retriever = SingleRouteRetriever(world)
    target = world.memories[17]

    route_zero = target.binding(0)
    route_one = target.binding(1)
    route_zero_only = RetrievalCue(
        (route_zero.anchor_concept_id, route_zero.detail_concept_id)
    )
    mixed_cue = RetrievalCue(
        (
            route_zero.anchor_concept_id,
            route_zero.detail_concept_id,
            route_one.anchor_concept_id,
            route_one.detail_concept_id,
        )
    )

    base = retriever.rank(route_zero_only, route_index=0)
    mixed = retriever.rank(mixed_cue, route_index=0)

    assert [item.memory_id for item in mixed] == [item.memory_id for item in base]


def test_target_label_is_not_a_retrieval_input() -> None:
    world = make_family_a_world(seed=1701)
    retriever = SingleRouteRetriever(world)
    first = world.memories[0]
    second = world.memories[1]
    binding = first.binding(0)
    cue = RetrievalCue((binding.anchor_concept_id, binding.detail_concept_id))

    true_label = LabeledProbe(
        probe_id="truth-a",
        route_index=0,
        condition="full",
        cue=cue,
        target_memory_id=first.memory_id,
    )
    false_label = LabeledProbe(
        probe_id="truth-b",
        route_index=0,
        condition="full",
        cue=cue,
        target_memory_id=second.memory_id,
    )

    first_ranking = retriever.rank(true_label.cue, route_index=true_label.route_index)
    second_ranking = retriever.rank(false_label.cue, route_index=false_label.route_index)

    assert first_ranking == second_ranking
    assert first_ranking[0].memory_id == first.memory_id


def test_family_a_seed_is_deterministic_but_not_a_transfer_family() -> None:
    first = make_family_a_world(seed=1701)
    repeated = make_family_a_world(seed=1701)
    different_seed = make_family_a_world(seed=1702)

    assert first == repeated
    assert first != different_seed


def test_every_probe_returns_exactly_the_frozen_field_size() -> None:
    result = run_single_route_assay(seed=1701)

    assert result["outcomes"]
    assert all(outcome["field_size"] == FIELD_SIZE for outcome in result["outcomes"])
