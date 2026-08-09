from dataclasses import replace

from experiments.hippocampal_contextual_taper_full_system import (
    CONDITIONS,
    GATE,
    WORLD_TYPES,
    evaluate,
    generate_world,
    learn_parameters,
    recurrent_solve,
    run_condition,
    soft_context_cascade,
    verdict,
)


def test_learned_parameters_are_identity_free_and_nonuniform() -> None:
    parameters = learn_parameters(range(60000, 60080))

    assert len(parameters.evidence_resistance) == 4
    assert sorted(parameters.taper_order) == [0, 1, 2, 3]
    assert len(parameters.taper_gains) == 4
    assert max(parameters.evidence_resistance) > min(parameters.evidence_resistance)
    assert max(parameters.taper_gains) > min(parameters.taper_gains)

    payload = parameters.to_dict()
    assert set(payload) == {
        "evidence_resistance",
        "taper_order",
        "taper_gains",
    }


def test_candidate_renaming_preserves_structure_and_behavior() -> None:
    parameters = learn_parameters(range(60000, 60080))
    original = generate_world(61004)
    renamed = generate_world(61004, rename_seed=9_999_991)

    assert [candidate.name for candidate in original.candidates] != [
        candidate.name for candidate in renamed.candidates
    ]
    assert [candidate.context_path for candidate in original.candidates] == [
        candidate.context_path for candidate in renamed.candidates
    ]
    assert [candidate.evidence for candidate in original.candidates] == [
        candidate.evidence for candidate in renamed.candidates
    ]
    assert original.excitation == renamed.excitation
    assert original.inhibition == renamed.inhibition

    original_result = run_condition(
        original,
        parameters,
        "context_specific_cascade",
    )
    renamed_result = run_condition(
        renamed,
        parameters,
        "context_specific_cascade",
    )

    assert original_result == renamed_result


def test_recurrent_solver_cannot_use_hidden_correct_index() -> None:
    parameters = learn_parameters(range(60000, 60080))
    world = generate_world(61001)
    activation, _, _ = soft_context_cascade(
        world,
        parameters,
        world.initial_cue,
    )

    original = recurrent_solve(world, activation, parameters, width=12)
    falsified_label = replace(
        world,
        correct_index=(world.correct_index + 7) % len(world.candidates),
    )
    relabeled = recurrent_solve(
        falsified_label,
        activation,
        parameters,
        width=12,
    )

    assert relabeled == original


def test_hard_topk_cannot_reactivate_a_candidate_it_deleted() -> None:
    parameters = learn_parameters(range(60000, 60080))
    suppressed = []

    for seed in range(61000, 61100):
        world = generate_world(seed)
        if world.world_type != "context_reversal":
            continue
        result = run_condition(world, parameters, "hard_topk")
        if result.initial_reversal_suppressed:
            suppressed.append(result)

    assert suppressed, "The assay must exercise hard-pruned reversal cases."
    assert all(result.reversal_reactivated is False for result in suppressed)


def test_context_specific_cascade_exercises_reopening_after_context_reversal() -> None:
    parameters = learn_parameters(range(60000, 60080))
    suppressed = []

    for seed in range(61000, 61100):
        world = generate_world(seed)
        if world.world_type != "context_reversal":
            continue
        result = run_condition(world, parameters, "context_specific_cascade")
        if result.initial_reversal_suppressed:
            suppressed.append(result)

    assert suppressed, "The assay must exercise soft-suppressed reversal cases."
    assert any(result.reversal_reactivated is True for result in suppressed)


def test_full_assay_reports_every_world_type_and_matched_control() -> None:
    parameters = learn_parameters(range(60000, 60080))
    result = evaluate(
        range(61000, 61025),
        parameters=parameters,
        candidate_count=128,
    )

    assert set(result["conditions"]) == set(CONDITIONS)
    assert set(result["by_world_type"]) == set(CONDITIONS)
    for condition in CONDITIONS:
        assert set(result["by_world_type"][condition]) == set(WORLD_TYPES)

    cascade = result["conditions"]["context_specific_cascade"]
    no_taper = result["conditions"]["no_taper"]
    assert cascade["mean_recurrent_candidate_cycles"] < no_taper[
        "mean_recurrent_candidate_cycles"
    ]
    assert cascade["mean_taper_candidate_evaluations"] > 0


def test_hct1_gate_is_frozen_and_scientifically_falsifiable() -> None:
    assert GATE == {
        "cascade_good_behavior_min": 0.85,
        "cascade_final_survival_min": 0.90,
        "unresolved_commit_rate_max": 0.25,
        "reversal_suppression_cases_min": 5,
        "cascade_reactivation_min": 0.75,
        "hard_reactivation_disadvantage_min": 0.20,
        "cascade_recurrent_cost_fraction_max": 0.50,
        "renaming_retention_min": 0.97,
        "generic_advantage_max": 0.03,
    }


def test_scientific_verdict_can_reinforce_discount_or_be_inconclusive() -> None:
    parameters = learn_parameters(range(60000, 60080))
    held = evaluate(range(61000, 61100), parameters=parameters)
    renamed = evaluate(
        range(61000, 61100),
        parameters=parameters,
        rename_offset=1_700_000,
    )

    decision, checks = verdict(held, renamed)

    assert decision.startswith(("REINFORCED:", "DISCOUNTED:", "INCONCLUSIVE:"))
    assert any(key.endswith("_pass") for key in checks)
