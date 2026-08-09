from experiments.hippocampal_confidence_gated import generate_mixed_world
from experiments.hippocampal_consensus_trials import (
    consensus_trials,
    evaluate,
    perturb_world,
)


def test_perturbation_preserves_identity_and_answer_contract() -> None:
    _, world = generate_mixed_world(40000)
    sampled = perturb_world(world, seed=12345)
    assert sampled.names == world.names
    assert sampled.correct_index == world.correct_index
    assert sampled.initial != world.initial


def test_consensus_retains_counterfactual_losers_when_it_commits() -> None:
    _, world = generate_mixed_world(40000)
    result = consensus_trials(world, trial_seed=999)
    if result.committed:
        assert result.winner is not None
        assert len(result.retained_alternatives) >= 1
        assert all(name != result.winner for name, _ in result.retained_alternatives)


def test_mixed_assay_exercises_resolvable_and_unresolved_behavior() -> None:
    result = evaluate(range(40000, 40250))
    resolvable = result["resolvable"]
    unresolved = result["unresolved_close"]
    assert 0.0 <= resolvable.committed_rate <= 1.0
    assert 0.0 <= unresolved.committed_rate <= 1.0
    assert resolvable.early_stop_rate > 0.0 or unresolved.max_trial_rate > 0.0


def test_consensus_does_not_materially_underperform_fixed_recurrence_on_resolvable_worlds() -> None:
    result = evaluate(range(40000, 40250))
    resolvable = result["resolvable"]
    baseline = result["deterministic_fixed_recurrent"]
    assert resolvable.committed_accuracy >= float(baseline["resolvable_accuracy"]) - 0.05


def test_unresolved_worlds_are_not_forced_to_commit_most_of_the_time() -> None:
    result = evaluate(range(40000, 40250))
    unresolved = result["unresolved_close"]
    assert unresolved.committed_rate <= 0.50


def test_candidate_renaming_preserves_population_behavior() -> None:
    original = evaluate(range(40000, 40250))
    renamed = evaluate(range(40000, 40250), rename_offset=1_300_000)
    original_resolvable = original["resolvable"]
    renamed_resolvable = renamed["resolvable"]
    original_unresolved = original["unresolved_close"]
    renamed_unresolved = renamed["unresolved_close"]
    assert renamed_resolvable.committed_accuracy == original_resolvable.committed_accuracy
    assert renamed_resolvable.committed_rate == original_resolvable.committed_rate
    assert renamed_unresolved.committed_rate == original_unresolved.committed_rate
