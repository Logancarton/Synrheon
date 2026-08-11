from __future__ import annotations

import pytest

from experiments.hct2_retrospective_audit import audit_relation_alignment
from experiments.hct2_retrospective_audit_runner import (
    _relation_alignment_cached,
    learn_parameters_from_worlds,
    run_visible_audit,
    verify_cached_learner_equivalence,
)
from experiments.hippocampal_ordered_context import generate_world, learn_parameters

pytestmark = pytest.mark.audit


def test_cached_learner_matches_frozen_hct2_learner() -> None:
    assert verify_cached_learner_equivalence() is True


def test_cached_learner_matches_frozen_on_test_slice() -> None:
    seeds = range(70000, 70008)
    worlds = tuple(generate_world(seed) for seed in seeds)

    assert learn_parameters_from_worlds(worlds) == learn_parameters(seeds)


def test_cached_relation_audit_matches_original_relation_audit() -> None:
    training_seeds = range(70000, 70008)
    evaluation_seeds = range(71000, 71004)
    training_worlds = tuple(generate_world(seed) for seed in training_seeds)
    evaluation_worlds = tuple(generate_world(seed) for seed in evaluation_seeds)
    parameters = learn_parameters_from_worlds(training_worlds)

    original = audit_relation_alignment(evaluation_worlds, parameters)
    cached = _relation_alignment_cached(
        evaluation_worlds,
        parameters,
        progress=False,
    )

    assert cached == original


def test_smoke_runner_remains_retrospective_and_exhausts_orders() -> None:
    report = run_visible_audit(
        training_seeds=range(70000, 70006),
        evaluation_seeds=range(71000, 71003),
        split_label="test_smoke",
        progress=False,
    )

    assert report["artifact_class"] == "RETROSPECTIVE_AUDIT"
    assert report["can_upgrade_hct2"] is False
    assert report["hct2_v1_modified"] is False
    assert len(report["order_landscape"]) == 24
    assert len(report["relation_alignment"]) == 3
