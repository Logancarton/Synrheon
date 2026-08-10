from __future__ import annotations

import pytest

from experiments.d6_transition_persistence import (
    CONDITIONS,
    classify_d6,
    run_d6,
    run_query,
)
from experiments.ext2_diagnostics import make_hard_corpus
from experiments.external_retrieval_cascade import (
    Dataset,
    build_environment,
    learn_parameters,
    queries_for_split,
)

pytestmark = pytest.mark.scientific


def test_d6_reset_control_returns_to_the_same_full_context_state_as_B() -> None:
    dataset = make_hard_corpus(seed=41, clusters=18, queries=80, informative_features=True)
    index, bank = build_environment(dataset)
    development = queries_for_split(dataset, "development")
    parameters = learn_parameters(dataset, bank, index, development=development)
    query = next(query for query in development if len(query.tokens) >= 4)

    outcome = run_query(dataset, index, bank, parameters, query)

    assert outcome.transition_evaluable is True
    assert outcome.reset_state_max_abs_diff is not None
    assert outcome.reset_state_max_abs_diff <= 1e-12
    assert outcome.ndcg["D_reset"] == pytest.approx(outcome.ndcg["B_full_soft"])


def test_d6_smoke_exercises_all_conditions_but_cannot_be_evidence() -> None:
    dataset = make_hard_corpus(seed=43, clusters=20, queries=90, informative_features=True)
    report = run_d6(dataset)

    assert report["synthetic"] is True
    assert report["split"] == "development"
    assert report["verdict"].startswith("NOT EVIDENCE")
    assert set(report["paired_transition_ndcg10"]) == set(CONDITIONS)
    assert report["reset_control_integrity_ok"] is True
    assert report["transition_evaluable_queries"] > 0
    assert set(report["paired_effects"]) == {
        "B_minus_C",
        "D_minus_C",
        "E_minus_C",
        "E_minus_B",
    }


def test_d6_frozen_classification_boundaries_do_not_move() -> None:
    positive_ci = {"delta": 0.06, "ci_low": 0.01, "ci_high": 0.10, "p_greater": 0.99}
    crossing_ci = {"delta": 0.06, "ci_low": -0.01, "ci_high": 0.11, "p_greater": 0.90}

    assert classify_d6(
        transition_queries=40,
        damage=0.10,
        reset_effect=positive_ci,
        reset_recovery_fraction=0.60,
        reset_integrity_ok=True,
    ) == "MAJOR_PERSISTENCE_CONTRIBUTION_SUPPORTED"

    assert classify_d6(
        transition_queries=40,
        damage=0.10,
        reset_effect=positive_ci,
        reset_recovery_fraction=0.30,
        reset_integrity_ok=True,
    ) == "PARTIAL_SUPPORT"

    assert classify_d6(
        transition_queries=40,
        damage=0.10,
        reset_effect=positive_ci,
        reset_recovery_fraction=0.20,
        reset_integrity_ok=True,
    ) == "PERSISTENCE_INSUFFICIENT"

    assert classify_d6(
        transition_queries=40,
        damage=0.10,
        reset_effect=crossing_ci,
        reset_recovery_fraction=0.60,
        reset_integrity_ok=True,
    ) == "INCONCLUSIVE"

    assert classify_d6(
        transition_queries=29,
        damage=0.10,
        reset_effect=positive_ci,
        reset_recovery_fraction=0.60,
        reset_integrity_ok=True,
    ) == "INCONCLUSIVE"

    assert classify_d6(
        transition_queries=40,
        damage=0.0,
        reset_effect=positive_ci,
        reset_recovery_fraction=None,
        reset_integrity_ok=True,
    ) == "DAMAGE_NOT_REPRODUCED"

    assert classify_d6(
        transition_queries=40,
        damage=0.10,
        reset_effect=positive_ci,
        reset_recovery_fraction=0.60,
        reset_integrity_ok=False,
    ) == "INVALID_RESET_CONTROL"


def test_d6_rejects_external_datasets_other_than_frozen_scifact() -> None:
    dataset = Dataset(
        name="nfcorpus",
        synthetic=False,
        documents=(),
        queries=(),
        qrels={},
    )
    with pytest.raises(ValueError, match="SciFact"):
        run_d6(dataset)
