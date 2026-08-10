
import pytest

import json
import sys
from dataclasses import replace

import experiments.hippocampal_ordered_context as experiment_module
from experiments.hippocampal_ordered_context import (
    CHANNEL_TO_DEPTH,
    CONDITIONS,
    FINAL_SEEDS,
    GATE,
    QUICK_DEVELOPMENT_SEEDS,
    WORLD_TYPES,
    evaluate,
    generate_world,
    generic_soft_taper,
    learn_parameters,
    recurrent_solve,
    run_condition,
    sparse_context_cascade,
)

pytestmark = pytest.mark.historical


def _small_parameters():
    return learn_parameters(range(70000, 70020))


def test_learned_parameters_are_identity_free_and_recover_hierarchy() -> None:
    parameters = _small_parameters()

    assert len(parameters.evidence_resistance) == 4
    assert len(parameters.context_gains) == 4
    assert sorted(parameters.context_order) == [0, 1, 2, 3]
    assert [
        CHANNEL_TO_DEPTH[channel]
        for channel in parameters.context_order
    ] == [0, 1, 2, 3]

    assert set(parameters.to_dict()) == {
        "evidence_resistance",
        "context_gains",
        "context_order",
    }


def test_candidate_renaming_preserves_structure_and_behavior() -> None:
    parameters = _small_parameters()
    original = generate_world(71001, candidate_count=128)
    renamed = generate_world(
        71001,
        candidate_count=128,
        rename_seed=9_999_991,
    )

    assert [candidate.name for candidate in original.candidates] != [
        candidate.name for candidate in renamed.candidates
    ]
    assert [
        candidate.semantic_path
        for candidate in original.candidates
    ] == [
        candidate.semantic_path
        for candidate in renamed.candidates
    ]
    assert [
        candidate.context_tokens
        for candidate in original.candidates
    ] == [
        candidate.context_tokens
        for candidate in renamed.candidates
    ]
    assert [
        candidate.evidence
        for candidate in original.candidates
    ] == [
        candidate.evidence
        for candidate in renamed.candidates
    ]
    assert original.excitation == renamed.excitation
    assert original.inhibition == renamed.inhibition

    assert run_condition(
        original,
        parameters,
        "learned_order_sparse",
    ) == run_condition(
        renamed,
        parameters,
        "learned_order_sparse",
    )


def test_recurrent_solver_cannot_use_hidden_correct_index() -> None:
    parameters = _small_parameters()
    world = generate_world(71001, candidate_count=128)
    taper = sparse_context_cascade(
        world,
        parameters,
        world.initial_cue,
    )

    original = recurrent_solve(
        world,
        taper.activation,
        parameters,
        width=16,
    )
    relabeled_world = replace(
        world,
        correct_index=(
            world.correct_index + 11
        ) % len(world.candidates),
    )
    relabeled = recurrent_solve(
        relabeled_world,
        taper.activation,
        parameters,
        width=16,
    )

    assert relabeled == original


def test_hard_topk_cannot_reactivate_deleted_reversal_candidates() -> None:
    parameters = _small_parameters()
    suppressed = []

    for seed in range(71000, 71025):
        world = generate_world(seed, candidate_count=128)
        if world.world_type != "context_reversal":
            continue
        result = run_condition(world, parameters, "hard_topk")
        if result.initial_reversal_suppressed:
            suppressed.append(result)

    assert suppressed, "The reversal stressor must delete candidates."
    assert all(
        result.reversal_reactivated is False
        for result in suppressed
    )


def test_learned_sparse_cascade_reopens_after_context_reversal() -> None:
    parameters = _small_parameters()
    suppressed = []

    for seed in range(71000, 71025):
        world = generate_world(seed, candidate_count=128)
        if world.world_type != "context_reversal":
            continue
        result = run_condition(
            world,
            parameters,
            "learned_order_sparse",
        )
        if result.initial_reversal_suppressed:
            suppressed.append(result)

    assert suppressed, "The assay must exercise reversible suppression."
    assert any(
        result.reversal_reactivated is True
        for result in suppressed
    )


def test_sparse_order_uses_fewer_context_feature_evaluations_than_generic() -> None:
    parameters = _small_parameters()
    world = generate_world(71001, candidate_count=128)

    sparse = sparse_context_cascade(
        world,
        parameters,
        world.initial_cue,
    )
    generic = generic_soft_taper(
        world,
        parameters,
        world.initial_cue,
    )

    assert sparse.context_feature_evaluations > 0
    assert generic.context_feature_evaluations > 0
    assert (
        sparse.context_feature_evaluations
        < generic.context_feature_evaluations
    )


def test_development_evaluation_reports_every_condition_and_world_type() -> None:
    parameters = _small_parameters()
    result = evaluate(
        range(71000, 71010),
        parameters=parameters,
        candidate_count=128,
    )

    assert set(result["conditions"]) == set(CONDITIONS)
    assert set(result["by_world_type"]) == set(CONDITIONS)
    for condition in CONDITIONS:
        assert set(result["by_world_type"][condition]) == set(
            WORLD_TYPES
        )


def test_hct2_gate_and_final_split_are_frozen() -> None:
    assert GATE == {
        "learned_good_behavior_min": 0.90,
        "learned_final_survival_min": 0.95,
        "unresolved_commit_rate_max": 0.20,
        "reversal_suppression_cases_min": 10,
        "learned_reactivation_min": 0.80,
        "hard_reactivation_disadvantage_min": 0.30,
        "recurrent_cost_fraction_max": 0.10,
        "renaming_retention_min": 0.97,
        "generic_behavior_advantage_max": 0.03,
        "context_eval_fraction_vs_generic_max": 0.50,
        "learned_order_efficiency_advantage_min": 0.03,
    }

    assert FINAL_SEEDS.start == 72000
    assert FINAL_SEEDS.stop == 72300
    assert set(QUICK_DEVELOPMENT_SEEDS).isdisjoint(FINAL_SEEDS)


def test_cli_quick_uses_development_and_default_uses_final(
    monkeypatch,
    capsys,
) -> None:
    calls: list[str] = []

    def fake_run_assay(*, split: str = "final") -> dict[str, str]:
        calls.append(split)
        return {"split": split}

    monkeypatch.setattr(
        experiment_module,
        "run_assay",
        fake_run_assay,
    )

    monkeypatch.setattr(sys, "argv", ["hct2"])
    experiment_module.main()
    assert calls == ["final"]
    assert json.loads(capsys.readouterr().out) == {
        "split": "final"
    }

    calls.clear()
    monkeypatch.setattr(sys, "argv", ["hct2", "--quick"])
    experiment_module.main()
    assert calls == ["quick"]
    assert json.loads(capsys.readouterr().out) == {
        "split": "quick"
    }

    calls.clear()
    monkeypatch.setattr(
        sys,
        "argv",
        ["hct2", "--development"],
    )
    experiment_module.main()
    assert calls == ["development"]
    assert json.loads(capsys.readouterr().out) == {
        "split": "development"
    }
