from __future__ import annotations

import json

import pytest

from experiments.r0_exact_match_envelope_v2 import run_corrected_exact_match_report

pytestmark = pytest.mark.specification


def test_corrected_report_is_classified_as_specification() -> None:
    report = run_corrected_exact_match_report(seed=1701)

    assert report["artifact_class"] == "SPECIFICATION"
    assert report["scientific_finding"] == "NONE"
    assert report["mechanism_changed_from_v1"] is False
    assert report["verdict"] == "SPECIFICATION_INTEGRITY_VALID"


def test_zero_support_is_one_deterministic_field_not_random_chance() -> None:
    report = run_corrected_exact_match_report(seed=1701)

    for baseline in report["zero_support_baseline"]:
        assert baseline["baseline_kind"] == "ZERO_SUPPORT_DETERMINISTIC_PREFIX"
        assert baseline["all_candidate_scores_tied"] is True
        assert baseline["tie_break"] == "memory_id_ascending"
        assert baseline["query_invariant_field"] is True
        assert baseline["unique_returned_fields"] == 1
        assert baseline["equals_first_sorted_memory_ids"] is True
        assert baseline["aggregate_hit_at_32"] == pytest.approx(32 / 128)


def test_alias_and_near_id_rates_are_named_as_zero_support_prefix_rates() -> None:
    report = run_corrected_exact_match_report(seed=1701)

    for metric in report["route_metrics"]:
        assert "near_id_hit_at_32" not in metric
        assert "alias_hit_at_32" not in metric
        assert metric["near_id_zero_support_prefix_hit_at_32"] == pytest.approx(32 / 128)
        assert metric["alias_zero_support_prefix_hit_at_32"] == pytest.approx(32 / 128)
        assert metric["metric_class"] == "DERIVED_SPECIFICATION_CHECK"


def test_corrected_report_does_not_describe_zero_support_as_chance() -> None:
    report = run_corrected_exact_match_report(seed=1701)
    rendered = json.dumps(report).lower()

    assert "chance" not in rendered


def test_v1_baseline_numbers_are_preserved_without_reinterpretation() -> None:
    report = run_corrected_exact_match_report(seed=1701)

    assert len(report["field_sweep"]) == 20
    assert len(report["route_metrics"]) == 4
    assert [item["route_group_size"] for item in report["route_metrics"]] == [8, 16, 32, 64]
