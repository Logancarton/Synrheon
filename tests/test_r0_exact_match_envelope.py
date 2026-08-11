from __future__ import annotations

import pytest

from experiments.r0_exact_match_envelope import (
    FIELD_SIZES,
    UNBOUND_NOISE_COUNTS,
    run_exact_match_envelope,
)

pytestmark = pytest.mark.scientific


def test_exact_match_envelope_is_valid() -> None:
    report = run_exact_match_envelope(seed=1701)

    assert report["verdict"] == "EXACT_MATCH_ENVELOPE_VALID"


def test_field_capacity_matches_ambiguity_exactly() -> None:
    report = run_exact_match_envelope(seed=1701)

    for metric in report["field_sweep"]:
        assert metric["field_size"] in FIELD_SIZES
        assert metric["partial_hit"] == pytest.approx(metric["expected_partial_hit"])


def test_unique_exact_detail_retrieves_perfectly() -> None:
    report = run_exact_match_envelope(seed=1701)

    for metric in report["route_metrics"]:
        assert metric["detail_only_top1"] == pytest.approx(1.0)
        assert metric["detail_only_hit_at_32"] == pytest.approx(1.0)


def test_unbound_noise_does_not_reorder_exact_partial_retrieval() -> None:
    report = run_exact_match_envelope(seed=1701)

    for metric in report["route_metrics"]:
        reference = metric["partial_reference_hit_at_32"]
        assert set(metric["unbound_noise_hit_at_32"]) == {
            str(count) for count in UNBOUND_NOISE_COUNTS
        }
        for hit in metric["unbound_noise_hit_at_32"].values():
            assert hit == pytest.approx(reference)


def test_same_group_wrong_exact_detail_beats_target_for_top1() -> None:
    report = run_exact_match_envelope(seed=1701)

    for metric in report["route_metrics"]:
        assert metric["same_group_conflict_target_top1"] == pytest.approx(0.0)
        assert metric["same_group_conflict_competitor_top1"] == pytest.approx(1.0)


def test_near_identity_and_unstored_alias_fall_to_chance() -> None:
    report = run_exact_match_envelope(seed=1701)
    chance = 32 / 128

    for metric in report["route_metrics"]:
        assert metric["near_id_hit_at_32"] == pytest.approx(chance)
        assert metric["alias_hit_at_32"] == pytest.approx(chance)


def test_foreign_exact_conflict_is_reported_without_posthoc_gate() -> None:
    report = run_exact_match_envelope(seed=1701)

    for metric in report["route_metrics"]:
        assert 0.0 <= metric["foreign_group_conflict_target_hit_at_32"] <= 1.0
        rank = metric["foreign_group_conflict_mean_target_rank_when_hit"]
        if rank is not None:
            assert 1.0 <= rank <= 32.0
