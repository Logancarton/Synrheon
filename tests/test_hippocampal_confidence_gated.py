from experiments.hippocampal_confidence_gated import (
    WORLD_TYPES,
    adaptive_recurrent,
    evaluate,
    generate_mixed_world,
    verdict,
)


def test_stability_compares_to_immediately_prior_state() -> None:
    _, world = generate_mixed_world(30000)
    result = adaptive_recurrent(world)
    assert len(result.traces) == 8
    assert all(trace.stability_delta >= 0.0 for trace in result.traces)


def test_mixed_generator_exercises_all_world_types() -> None:
    seen = {generate_mixed_world(seed)[0] for seed in range(30000, 30025)}
    assert seen == set(WORLD_TYPES)


def test_adaptive_gating_exercises_both_prune_and_keep_open_behavior() -> None:
    result = evaluate(range(30000, 30500))
    adaptive = result["confidence_gated"]
    assert 0.20 <= adaptive.prune_rate <= 0.80
    assert 0.20 <= adaptive.never_pruned_rate <= 0.80


def test_clear_worlds_prune_more_than_unresolved_close_worlds() -> None:
    result = evaluate(range(30000, 30500))
    by_type = result["by_world_type"]
    assert by_type["easy_clear"].prune_rate >= 0.60
    assert by_type["unresolved_close"].never_pruned_rate >= 0.60


def test_misleading_early_worlds_rarely_false_prune() -> None:
    result = evaluate(range(30000, 30500))
    misleading = result["by_world_type"]["misleading_early"]
    assert misleading.false_prune_rate <= 0.10


def test_adaptive_gating_preserves_accuracy_and_saves_state_cost() -> None:
    result = evaluate(range(30000, 30500))
    adaptive = result["confidence_gated"]
    fixed = result["fixed_width"]
    assert adaptive.accuracy >= fixed.accuracy - 0.05
    assert result["active_state_savings_vs_fixed"] >= 0.10


def test_renaming_does_not_change_adaptive_summary() -> None:
    original = evaluate(range(30000, 30500))
    renamed = evaluate(range(30000, 30500), 1_200_000)
    assert renamed["confidence_gated"].accuracy == original["confidence_gated"].accuracy
    assert renamed["confidence_gated"].prune_rate == original["confidence_gated"].prune_rate


def test_verdict_cannot_reinforce_if_gate_never_exercises() -> None:
    result = evaluate(range(30000, 30500))
    text = verdict(result)
    if result["confidence_gated"].prune_rate < 0.20 or result["confidence_gated"].prune_rate > 0.80:
        assert text.startswith("INCONCLUSIVE")
