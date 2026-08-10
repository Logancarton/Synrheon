"""CPN-1 implementation and integrity tests.

These verify the experiment executes exactly as frozen in `docs/CPN1_PREREGISTRATION.md`
and `docs/CPN1_1_AMENDMENT.md`, and that its classifier behaves. They do **not** assert
that contextual pre-narrowing works. No SciFact development ranking or nDCG is computed
here; every fixture is synthetic.
"""

from __future__ import annotations

import inspect
from dataclasses import replace

import pytest

import experiments.cpn1_equal_budget_prenarrowing as cpn1
from experiments.ext2_diagnostics import make_hard_corpus
from experiments.external_retrieval_cascade import (
    CANDIDATE_DEPTH,
    RECURRENCE_WIDTH,
    TAPER_STAGE_CYCLES,
    _initial_activation,
    _reopen_cue,
    build_environment,
    learn_parameters,
    queries_for_split,
)
from experiments.cpn1_equal_budget_prenarrowing import (
    CONDITIONS,
    MATERIAL_DELTA,
    MIN_TRANSITION_QUERIES,
    classify_cpn1,
    new_trajectory,
    run_a1,
    run_cpn1,
    run_prenarrowed,
    run_query,
    run_stage,
)

pytestmark = pytest.mark.scientific


@pytest.fixture(scope="module")
def environment():
    dataset = make_hard_corpus(seed=31, clusters=14, queries=48, informative_features=True)
    index, bank = build_environment(dataset)
    development = queries_for_split(dataset, "development")
    parameters = learn_parameters(dataset, bank, index, development=development)
    query = next(q for q in development if _reopen_cue(q) is not None
                 and index.top_candidates(q.tokens, CANDIDATE_DEPTH))
    candidates = index.top_candidates(query.tokens, CANDIDATE_DEPTH)
    return dataset, index, bank, parameters, development, query, candidates


@pytest.fixture()
def trajectories(environment):
    """Every condition for one query, built exactly as the runner builds them."""
    dataset, index, bank, parameters, development, query, candidates = environment
    prior = _initial_activation(candidates)
    cue = _reopen_cue(query)
    a1 = run_a1(query, bank, parameters, prior)
    budget = a1.evaluations
    made = {"A1": a1}
    for name, plan in (
        ("T", dict(stage1_cue=cue, stage2_cue=None)),
        ("C_carry", dict(stage1_cue=cue, stage2_cue=None, carry=True)),
        ("C_reversed", dict(stage1_cue=None, stage2_cue=cue)),
        ("C_hard", dict(stage1_cue=cue, stage2_cue=None, hard_prune=True)),
    ):
        made[name] = run_prenarrowed(
            name, query, bank, parameters, prior, cue, budget, **plan
        )
    return made, budget, prior, query, candidates, parameters, bank


# --- 1-7: starting state, retrieval, and context placement --------------------------

def test_1_candidate_field_is_identical_across_all_conditions(trajectories) -> None:
    made, _, _, _, candidates, _, _ = trajectories
    expected = {doc_id for doc_id, _ in candidates}

    for name in ("A1", "T", "C_carry", "C_reversed"):
        assert set(made[name].activation) == expected, name
    # C-hard is the only condition permitted to shrink the field.
    assert set(made["C_hard"].activation) < expected


def test_2_treatment_starts_from_the_full_query_prior(trajectories) -> None:
    made, budget, prior, query, candidates, parameters, bank = trajectories

    trajectory = new_trajectory(bank, prior)
    assert trajectory.activation == prior
    assert trajectory.update_region == set(prior)


def test_3_no_cue_prior_call_exists_anywhere_in_cpn1() -> None:
    source = inspect.getsource(cpn1)

    assert "_cue_prior" not in source
    assert "cue_prior" not in source


def test_4_partial_cue_enters_only_the_intended_feature_context(trajectories) -> None:
    made, _, _, query, _, parameters, _ = trajectories
    cue = _reopen_cue(query)
    order = parameters.channel_order

    stage1, stage2 = made["T"].stages
    assert stage1.cue_used is True and stage1.channels == order[:1]
    assert stage2.cue_used is False and stage2.channels == order[1:]
    assert cue != query.tokens


def test_5_baseline_uses_channel_one_under_full_context(trajectories) -> None:
    made, _, _, _, _, parameters, _ = trajectories
    (stage,) = made["A1"].stages

    assert stage.channels == parameters.channel_order
    assert stage.cue_used is False


def test_6_treatment_uses_channel_one_under_partial_context(trajectories) -> None:
    made, _, _, _, _, parameters, _ = trajectories
    assert made["T"].stages[0].channels == parameters.channel_order[:1]
    assert made["T"].stages[0].cue_used is True


def test_7_treatment_stage_two_uses_remaining_channels_under_full_context(
    trajectories,
) -> None:
    made, _, _, _, _, parameters, _ = trajectories
    assert made["T"].stages[1].channels == parameters.channel_order[1:]
    assert made["T"].stages[1].cue_used is False


# --- 8-12: suppressed != deleted ----------------------------------------------------

def test_8_transition_preserves_every_candidate_identity(trajectories) -> None:
    made, _, prior, _, _, _, _ = trajectories
    assert set(made["T"].activation) == set(prior)


def test_9_outside_ceiling_candidates_remain_but_receive_no_stage_two_update(
    trajectories,
) -> None:
    made, _, prior, query, _, parameters, bank = trajectories
    treatment = made["T"]
    outside = set(treatment.activation) - set(treatment.update_ceiling)
    assert outside, "fixture must produce a non-empty dormant region"

    # Present in state.
    assert outside <= set(treatment.activation)
    # A normalized reset prior rescales dormant candidates uniformly, so their
    # relative order is untouched by stage 2 -- no feature update reached them.
    ordered = [d for d in treatment.ranking if d in outside]
    baseline = [d for d, _ in sorted(prior.items(), key=lambda kv: (-kv[1], kv[0]))
                if d in outside]
    assert ordered == baseline


def test_10_final_ranking_is_built_from_the_complete_activation_map(trajectories) -> None:
    made, _, _, _, candidates, _, _ = trajectories
    treatment = made["T"]

    assert len(treatment.ranking) == len(candidates)
    assert set(treatment.ranking) == set(treatment.activation)
    assert len(treatment.ranking) > len(treatment.update_ceiling)


def test_11_hard_pruning_physically_removes_outside_candidates(trajectories) -> None:
    made, _, _, _, candidates, _, _ = trajectories
    hard = made["C_hard"]

    assert len(hard.activation) == RECURRENCE_WIDTH
    assert len(hard.ranking) == RECURRENCE_WIDTH
    assert hard.removed_candidates
    for doc_id in hard.removed_candidates:
        assert doc_id not in hard.activation
        assert doc_id not in hard.ranking


def test_12_candidate_lost_to_hard_pruning_survives_in_the_treatment(trajectories) -> None:
    """The reversibility distinction, stated as a concrete recoverable candidate."""

    made, _, _, _, _, _, _ = trajectories
    treatment, hard = made["T"], made["C_hard"]

    lost = set(hard.removed_candidates)
    assert lost, "fixture must actually prune something"
    # Every candidate destroyed by hard pruning is still present and rankable in T.
    assert lost <= set(treatment.activation)
    assert lost <= set(treatment.ranking)
    # And T is not accidentally equivalent to C-hard.
    assert set(treatment.ranking) != set(hard.ranking)


# --- 13-14: control semantics -------------------------------------------------------

def test_13_carry_differs_from_treatment_only_in_transition_activation(
    trajectories,
) -> None:
    made, _, _, _, _, _, _ = trajectories
    treatment, carry = made["T"], made["C_carry"]

    # Identical ceiling semantics and identical stage structure.
    assert carry.update_ceiling == treatment.update_ceiling
    assert [s.channels for s in carry.stages] == [s.channels for s in treatment.stages]
    assert [s.cue_used for s in carry.stages] == [s.cue_used for s in treatment.stages]
    assert set(carry.activation) == set(treatment.activation)
    # Same candidate width means the isolated difference is reset vs carry.
    assert carry.activation != treatment.activation


def test_14_reversed_control_cannot_affect_the_primary_classifier() -> None:
    signature = inspect.signature(classify_cpn1)

    assert set(signature.parameters) == {
        "transition_queries", "delta", "ci_low", "budget_control_ok",
    }
    # No C-reversed quantity can reach the classifier at all.
    assert "reversed" not in inspect.getsource(classify_cpn1).lower()


# --- 15-17: cache isolation ---------------------------------------------------------

def test_15_every_condition_gets_a_distinct_meter_with_an_empty_cache(
    trajectories,
) -> None:
    made, _, prior, _, _, _, bank = trajectories

    first = new_trajectory(bank, prior)
    second = new_trajectory(bank, prior)
    assert first.meter is not second.meter
    assert first.meter._cache == {} and second.meter._cache == {}
    assert first.meter.evaluations == 0 and first.meter.requests == 0
    assert first.evaluated_keys == set()


def test_16_baseline_cache_entries_are_not_visible_to_the_treatment(
    environment,
) -> None:
    dataset, index, bank, parameters, development, query, candidates = environment
    prior = _initial_activation(candidates)
    cue = _reopen_cue(query)

    a1_trajectory = new_trajectory(bank, prior)
    run_stage(a1_trajectory, query, parameters, channels=parameters.channel_order, cue=None)
    assert a1_trajectory.meter.evaluations > 0

    treatment = new_trajectory(bank, prior)
    assert treatment.meter._cache == {}
    run_stage(treatment, query, parameters, channels=parameters.channel_order[:1], cue=cue,
              budget=a1_trajectory.meter.evaluations)
    # The treatment paid for its own features; nothing was inherited.
    assert treatment.meter.evaluations > 0
    assert treatment.meter._cache.keys() != a1_trajectory.meter._cache.keys()
    assert len(treatment.evaluated_keys) == treatment.meter.evaluations


def test_17_only_the_scalar_budget_crosses_a_condition_boundary() -> None:
    signature = inspect.signature(run_prenarrowed)

    assert signature.parameters["budget"].annotation == "int"
    source = inspect.getsource(cpn1.run_query)
    # The budget is read off A1 as a plain integer; no meter is passed onward.
    assert "budget = a1.evaluations" in source
    assert "meter=" not in source


# --- 18-20: budget enforcement ------------------------------------------------------

def test_18_no_condition_exceeds_the_budget(trajectories) -> None:
    made, budget, _, _, _, _, _ = trajectories

    for name in ("T", "C_carry", "C_reversed", "C_hard"):
        assert made[name].evaluations <= budget, name
    assert made["A1"].evaluations == budget


def test_19_stage_one_is_always_executable_on_the_fixture(environment) -> None:
    dataset, index, bank, parameters, development, _, _ = environment

    checked = 0
    for query in development:
        candidates = index.top_candidates(query.tokens, CANDIDATE_DEPTH)
        cue = _reopen_cue(query)
        if not candidates or cue is None:
            continue
        prior = _initial_activation(candidates)
        budget = run_a1(query, bank, parameters, prior).evaluations
        trajectory = new_trajectory(bank, prior)
        trace = run_stage(trajectory, query, parameters,
                          channels=parameters.channel_order[:1], cue=cue, budget=budget)
        assert trace.truncated is False
        assert trace.channels_completed == 1
        checked += 1
    assert checked > 0


def test_20_budget_exhaustion_stops_before_a_cycle_never_halfway(environment) -> None:
    dataset, index, bank, parameters, development, query, candidates = environment
    prior = _initial_activation(candidates)

    trajectory = new_trajectory(bank, prior)
    # A budget too small for even the first cycle.
    trace = run_stage(trajectory, query, parameters,
                      channels=parameters.channel_order, cue=None, budget=1)

    assert trace.truncated is True
    assert trace.cycles_completed == 0
    assert trajectory.meter.evaluations == 0
    assert trajectory.activation == prior
    assert trajectory.activation_updates == 0


def test_20b_partial_budget_completes_only_whole_cycles(environment) -> None:
    dataset, index, bank, parameters, development, query, candidates = environment
    prior = _initial_activation(candidates)
    full = run_a1(query, bank, parameters, prior).evaluations

    trajectory = new_trajectory(bank, prior)
    run_stage(trajectory, query, parameters, channels=parameters.channel_order,
              cue=None, budget=full // 2)

    assert trajectory.meter.evaluations <= full // 2
    assert len(trajectory.evaluated_keys) == trajectory.meter.evaluations


# --- 21-22: classifier ---------------------------------------------------------------

def test_21_every_frozen_classification_is_reachable() -> None:
    base = dict(transition_queries=50, delta=0.05, ci_low=0.01, budget_control_ok=True)

    assert classify_cpn1(**base) == "CONTEXTUAL_PRENARROWING_SUPPORTED"
    assert classify_cpn1(**{**base, "delta": 0.005}) == "CONTEXTUAL_PRENARROWING_IMMATERIAL"
    assert classify_cpn1(**{**base, "delta": -0.01}) == "CONTEXTUAL_PRENARROWING_NOT_SUPPORTED"
    assert classify_cpn1(**{**base, "ci_low": -0.001}) == "CONTEXTUAL_PRENARROWING_NOT_SUPPORTED"
    assert classify_cpn1(**{**base, "transition_queries": 5}) == "INCONCLUSIVE"
    assert classify_cpn1(**{**base, "budget_control_ok": False}) == "INVALID_BUDGET_CONTROL"


def test_22_secondary_reversed_outcome_does_not_modify_the_primary_classification() -> None:
    dataset = make_hard_corpus(seed=17, clusters=10, queries=36, informative_features=True)
    report = run_cpn1(dataset)
    primary = report["classification"]

    # The reported secondary effect exists but carries no threshold and no gate.
    assert "T_minus_C_reversed" in report["secondary_effects"]
    assert report["classification"] == primary
    assert classify_cpn1(
        transition_queries=report["transition_evaluable_queries"],
        delta=report["primary_effect"]["delta"],
        ci_low=report["primary_effect"]["ci_low"],
        budget_control_ok=report["budget_control_ok"],
    ) == primary
    assert "may change, veto, promote, or replace" in report["secondary_note"]


def _rename_candidates(dataset):
    """Replace every document identity with an opaque, order-preserving label.

    Order preservation keeps BM25 tie-breaks identical, so any surviving difference is
    attributable to identity rather than to ranking noise.
    """

    ordered = sorted(dataset.documents, key=lambda document: document.doc_id)
    mapping = {document.doc_id: f"cand{index:06d}" for index, document in enumerate(ordered)}
    documents = tuple(replace(document, doc_id=mapping[document.doc_id])
                      for document in dataset.documents)
    qrels = {
        query_id: {mapping[doc_id]: value for doc_id, value in judged.items()}
        for query_id, judged in dataset.qrels.items()
    }
    return replace(dataset, documents=documents, qrels=qrels)


def test_23_renaming_candidates_preserves_compute_accounting_and_classification() -> None:
    original = make_hard_corpus(seed=23, clusters=10, queries=36, informative_features=True)
    renamed = _rename_candidates(original)

    assert {d.doc_id for d in original.documents} != {d.doc_id for d in renamed.documents}

    first, second = run_cpn1(original), run_cpn1(renamed)

    assert first["classification"] == second["classification"]
    assert first["mean_budget"] == second["mean_budget"]
    assert first["primary_effect"]["delta"] == second["primary_effect"]["delta"]

    # Wall-clock is a diagnostic and cannot be deterministic; every counted quantity is.
    def counted(report):
        return {
            condition: {k: v for k, v in stats.items() if k != "mean_nanoseconds"}
            for condition, stats in report["paired_compute"].items()
        }

    assert counted(first) == counted(second)


# --- 24-25: leakage and data boundary -----------------------------------------------

def test_24_no_answer_information_reaches_any_frozen_decision() -> None:
    for function in (cpn1.run_stage, cpn1.run_prenarrowed, cpn1.run_a1, cpn1.classify_cpn1):
        source = inspect.getsource(function)
        assert "qrels" not in source
        assert "judged" not in source
        assert "ndcg" not in source.lower()

    # Scoring is the only place judgments are read, and it is gated.
    run_query_source = inspect.getsource(cpn1.run_query)
    assert "if score else {}" in run_query_source


def test_25_reserved_final_split_cannot_be_invoked(environment) -> None:
    source = inspect.getsource(cpn1.run_cpn1)

    assert '"development"' in source
    assert '"final"' not in source
    # And the runner actively rejects any stray non-development query id.
    assert "Reserved final-split queries reached CPN-1" in source


def test_evidence_run_is_gated_off_by_default() -> None:
    dataset = make_hard_corpus(seed=5, clusters=6, queries=20, informative_features=True)
    external = type(dataset)(
        name="scifact", synthetic=False,
        documents=dataset.documents, queries=dataset.queries, qrels=dataset.qrels,
    )

    with pytest.raises(RuntimeError, match="evidence_run=True"):
        run_cpn1(external)


def test_synthetic_report_is_labelled_not_evidence_and_preserves_raw_output() -> None:
    dataset = make_hard_corpus(seed=31, clusters=10, queries=36, informative_features=True)
    report = run_cpn1(dataset)

    assert report["synthetic"] is True
    assert report["verdict"].startswith("NOT EVIDENCE")
    assert report["preregistration"] == "docs/CPN1_PREREGISTRATION.md"
    assert report["amendment"] == "docs/CPN1_1_AMENDMENT.md"
    assert report["budget_control_ok"] is True
    assert len(report["per_query"]) == report["development_queries"]
    assert set(report["paired_transition_ndcg10"]) == set(CONDITIONS)
    assert report["material_delta"] == MATERIAL_DELTA
    assert report["minimum_transition_queries"] == MIN_TRANSITION_QUERIES


def test_frozen_constants_and_dynamics_are_unchanged() -> None:
    assert MATERIAL_DELTA == 0.010
    assert MIN_TRANSITION_QUERIES == 30
    assert TAPER_STAGE_CYCLES == 2
