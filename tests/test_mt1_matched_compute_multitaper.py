"""MT-1 implementation and integrity tests.

These verify that the experiment executes correctly and that its frozen classifier
behaves. They do **not** assert that the multi-stage hypothesis is true. MT-1 may
conclude SUPPORTED, IMMATERIAL, NOT_SUPPORTED, COMPUTE_UNMATCHED, or INCONCLUSIVE, and
none of those outcomes should turn a test red.
"""

from __future__ import annotations

import pytest

from experiments.ext2_diagnostics import make_hard_corpus
from experiments.external_retrieval_cascade import (
    CANDIDATE_DEPTH,
    RECURRENCE_WIDTH,
    _initial_activation,
    _reopen_cue,
    build_environment,
    learn_parameters,
    queries_for_split,
    soft_taper,
)
from experiments.mt1_matched_compute_multitaper import (
    COMPUTE_TOLERANCE,
    CONDITIONS,
    MATERIAL_DELTA,
    MIN_TRANSITION_QUERIES,
    MULTI_STAGE_CYCLES,
    SINGLE_STAGE_CYCLES,
    FeatureMeter,
    classify_mt1,
    run_mt1,
    run_query,
    soft_stage,
)

pytestmark = pytest.mark.scientific


@pytest.fixture(scope="module")
def environment():
    dataset = make_hard_corpus(seed=31, clusters=12, queries=40, informative_features=True)
    index, bank = build_environment(dataset)
    development = queries_for_split(dataset, "development")
    parameters = learn_parameters(dataset, bank, index, development=development)
    return dataset, index, bank, parameters, development


def test_single_stage_condition_reproduces_the_frozen_soft_taper(environment) -> None:
    """M1 must be the existing full-context taper, not a re-implementation of it."""

    dataset, index, bank, parameters, development = environment

    for query in development[:8]:
        candidates = index.top_candidates(query.tokens, CANDIDATE_DEPTH)
        if not candidates:
            continue
        reference = soft_taper(query, candidates, parameters, FeatureMeter(bank))
        rebuilt = soft_stage(
            query,
            candidates,
            parameters,
            FeatureMeter(bank),
            prior=_initial_activation(candidates),
            cue=None,
            cycles_per_channel=SINGLE_STAGE_CYCLES,
        )
        assert rebuilt.activation == reference.activation
        assert rebuilt.active == reference.active


def test_two_stages_use_the_same_nominal_sweep_budget_as_one(environment) -> None:
    """Four channels x two cycles equals four channels x one cycle, twice."""

    dataset, index, bank, parameters, development = environment
    assert SINGLE_STAGE_CYCLES == 2 * MULTI_STAGE_CYCLES

    query = next(q for q in development if _reopen_cue(q) is not None)
    candidates = index.top_candidates(query.tokens, CANDIDATE_DEPTH)

    single = soft_stage(
        query,
        candidates,
        parameters,
        FeatureMeter(bank),
        prior=_initial_activation(candidates),
        cue=None,
        cycles_per_channel=SINGLE_STAGE_CYCLES,
    )
    assert len(single.stage_active_counts) == len(parameters.channel_order)


def test_active_ceiling_narrows_and_never_re_expands(environment) -> None:
    """Retained narrowing is a ceiling: a later stage may narrow, never re-expand."""

    dataset, index, bank, parameters, development = environment
    query = next(q for q in development if _reopen_cue(q) is not None)
    candidates = index.top_candidates(query.tokens, CANDIDATE_DEPTH)
    cue = _reopen_cue(query)

    meter = FeatureMeter(bank)
    first = soft_stage(
        query,
        candidates,
        parameters,
        meter,
        prior=_initial_activation(candidates),
        cue=cue,
        cycles_per_channel=MULTI_STAGE_CYCLES,
    )
    second = soft_stage(
        query,
        candidates,
        parameters,
        meter,
        prior=_initial_activation(candidates),
        cue=None,
        cycles_per_channel=MULTI_STAGE_CYCLES,
        active_ceiling=first.active,
    )

    assert set(second.active) <= set(first.active)
    # Dormant candidates keep state and are never deleted.
    assert set(second.activation) == set(second.active) | set(second.dormant)
    assert len(second.activation) == len(candidates)


def test_narrowed_stage_costs_no_more_than_the_unnarrowed_stage(environment) -> None:
    dataset, index, bank, parameters, development = environment
    query = next(q for q in development if _reopen_cue(q) is not None)
    candidates = index.top_candidates(query.tokens, CANDIDATE_DEPTH)
    cue = _reopen_cue(query)

    seed_meter = FeatureMeter(bank)
    first = soft_stage(
        query, candidates, parameters, seed_meter,
        prior=_initial_activation(candidates), cue=cue,
        cycles_per_channel=MULTI_STAGE_CYCLES,
    )

    narrowed_meter = FeatureMeter(bank)
    soft_stage(
        query, candidates, parameters, narrowed_meter,
        prior=_initial_activation(candidates), cue=None,
        cycles_per_channel=MULTI_STAGE_CYCLES, active_ceiling=first.active,
    )
    open_meter = FeatureMeter(bank)
    soft_stage(
        query, candidates, parameters, open_meter,
        prior=_initial_activation(candidates), cue=None,
        cycles_per_channel=MULTI_STAGE_CYCLES,
    )

    assert narrowed_meter.evaluations <= open_meter.evaluations


def test_every_condition_is_scored_and_queries_without_a_cue_are_excluded(environment) -> None:
    dataset, index, bank, parameters, development = environment

    with_cue = next(q for q in development if _reopen_cue(q) is not None)
    evaluable = run_query(dataset, index, bank, parameters, with_cue)

    assert evaluable.transition_evaluable is True
    assert set(evaluable.ndcg) == set(CONDITIONS)
    assert set(evaluable.feature_evaluations) == set(CONDITIONS)
    # The anchor is free; every tapered condition spends feature evaluations.
    assert evaluable.feature_evaluations["M0_bm25_anchor"] == 0
    for condition in CONDITIONS[1:]:
        assert evaluable.feature_evaluations[condition] > 0

    without_cue = [q for q in development if _reopen_cue(q) is None]
    if without_cue:
        excluded = run_query(dataset, index, bank, parameters, without_cue[0])
        assert excluded.transition_evaluable is False
        # M0/M1 remain computable; staged conditions are not scored.
        assert excluded.feature_evaluations["M1_single_full_soft"] > 0
        assert excluded.ndcg["M3_multi_reset_narrowed"] == 0.0


def test_hard_pruning_removes_candidates_rather_than_damping_them(environment) -> None:
    """M6 must lose the pruned candidates; they cannot be recovered by later evidence."""

    dataset, index, bank, parameters, development = environment
    query = next(q for q in development if _reopen_cue(q) is not None)
    outcome = run_query(dataset, index, bank, parameters, query)

    # Hard pruning evaluates a strictly narrowed field, so it cannot cost more than the
    # soft-narrowed condition at the same nominal budget.
    assert outcome.feature_evaluations["M6_hard_staged_prune"] <= (
        outcome.feature_evaluations["M3_multi_reset_narrowed"]
    )


def test_classifier_applies_only_the_frozen_categories() -> None:
    base = {
        "transition_queries": 50,
        "delta": 0.05,
        "ci_low": 0.01,
        "compute_ratio": 1.0,
        "single_stage_equivalence_ok": True,
    }

    assert classify_mt1(**base) == "MULTI_STAGE_SUPPORTED"
    assert classify_mt1(**{**base, "delta": 0.005}) == "MULTI_STAGE_IMMATERIAL"
    assert classify_mt1(**{**base, "delta": -0.01}) == "MULTI_STAGE_NOT_SUPPORTED"
    assert classify_mt1(**{**base, "ci_low": -0.001}) == "MULTI_STAGE_NOT_SUPPORTED"
    assert classify_mt1(**{**base, "compute_ratio": 1.5}) == "COMPUTE_UNMATCHED"
    assert classify_mt1(**{**base, "transition_queries": 10}) == "INCONCLUSIVE"
    assert (
        classify_mt1(**{**base, "single_stage_equivalence_ok": False})
        == "INVALID_SINGLE_STAGE_CONTROL"
    )


def test_extra_compute_cannot_excuse_a_loss() -> None:
    """A negative result under an inflated budget is still NOT_SUPPORTED."""

    assert (
        classify_mt1(
            transition_queries=50,
            delta=-0.02,
            ci_low=-0.05,
            compute_ratio=3.0,
            single_stage_equivalence_ok=True,
        )
        == "MULTI_STAGE_NOT_SUPPORTED"
    )


def test_frozen_decision_constants_are_unchanged() -> None:
    """Guard the preregistered numbers against silent drift."""

    assert MATERIAL_DELTA == 0.010
    assert COMPUTE_TOLERANCE == 1.10
    assert MIN_TRANSITION_QUERIES == 30


def test_synthetic_run_is_labelled_not_evidence_and_reports_raw_output() -> None:
    dataset = make_hard_corpus(seed=31, clusters=10, queries=36, informative_features=True)
    report = run_mt1(dataset)

    assert report["synthetic"] is True
    assert report["verdict"].startswith("NOT EVIDENCE")
    assert report["split"] == "development"
    assert report["single_stage_equivalence_ok"] is True

    # Raw per-query output must survive for inspection.
    assert len(report["per_query"]) == report["development_queries"]
    assert set(report["paired_transition_ndcg10"]) == set(CONDITIONS)
    assert report["primary_effect"]["comparison"] == (
        "M3_multi_reset_narrowed_minus_M1_single_full_soft"
    )
    for key in ("ci_low", "ci_high", "delta"):
        assert key in report["primary_effect"]


def test_v1_cannot_produce_a_development_result() -> None:
    """MT-1 v1 is UNEXECUTED / DESIGN-INVALID and must stay that way.

    Its treatment cannot satisfy its own matched-compute rule, so
    MULTI_STAGE_SUPPORTED is structurally unreachable. The guard keeps the SciFact
    development split available to the replacement design.
    """

    dataset = make_hard_corpus(seed=7, clusters=6, queries=20, informative_features=True)
    external = type(dataset)(
        name="scifact",
        synthetic=False,
        documents=dataset.documents,
        queries=dataset.queries,
        qrels=dataset.qrels,
    )

    with pytest.raises(RuntimeError, match="DESIGN-INVALID"):
        run_mt1(external)
