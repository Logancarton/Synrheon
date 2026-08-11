from __future__ import annotations

import pytest

from experiments.r0_exact_match_envelope import (
    FIELD_SIZES,
    UNBOUND_NOISE_COUNTS,
    run_exact_match_envelope,
)

pytestmark = pytest.mark.specification


def test_exact_match_envelope_implementation_matches_specification() -> None:
    report = run_exact_match_envelope(seed=1701)

    assert report["verdict"] == "EXACT_MATCH_ENVELOPE_VALID"


def test_field_capacity_matches_derived_ambiguity_formula() -> None:
    report = run_exact_match_envelope(seed=1701)

    for metric in report["field_sweep"]:
        assert metric["field_size"] in FIELD_SIZES
        assert metric["partial_hit"] == pytest.approx(metric["expected_partial_hit"])


def test_unique_exact_detail_matches_constructed_unique_identity() -> None:
    report = run_exact_match_envelope(seed=1701)

    for metric in report["route_metrics"]:
        assert metric["detail_only_top1"] == pytest.approx(1.0)
        assert metric["detail_only_hit_at_32"] == pytest.approx(1.0)


def test_unbound_noise_preserves_ranking_by_algebraic_construction() -> None:
    report = run_exact_match_envelope(seed=1701)

    for metric in report["route_metrics"]:
        reference = metric["partial_reference_hit_at_32"]
        assert set(metric["unbound_noise_hit_at_32"]) == {
            str(count) for count in UNBOUND_NOISE_COUNTS
        }
        for hit in metric["unbound_noise_hit_at_32"].values():
            assert hit == pytest.approx(reference)


def test_same_group_wrong_exact_detail_has_more_overlap_than_target() -> None:
    report = run_exact_match_envelope(seed=1701)

    for metric in report["route_metrics"]:
        assert metric["same_group_conflict_target_top1"] == pytest.approx(0.0)
        assert metric["same_group_conflict_competitor_top1"] == pytest.approx(1.0)


def test_near_identity_and_unstored_alias_have_zero_support_aggregate_prefix_rate() -> None:
    report = run_exact_match_envelope(seed=1701)
    deterministic_prefix_rate = 32 / 128

    for metric in report["route_metrics"]:
        assert metric["near_id_hit_at_32"] == pytest.approx(deterministic_prefix_rate)
        assert metric["alias_hit_at_32"] == pytest.approx(deterministic_prefix_rate)


def test_foreign_exact_conflict_is_reported_without_posthoc_gate() -> None:
    report = run_exact_match_envelope(seed=1701)

    for metric in report["route_metrics"]:
        assert 0.0 <= metric["foreign_group_conflict_target_hit_at_32"] <= 1.0
        rank = metric["foreign_group_conflict_mean_target_rank_when_hit"]
        if rank is not None:
            assert 1.0 <= rank <= 32.0
