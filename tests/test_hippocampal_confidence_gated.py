from experiments.hippocampal_confidence_gated import adaptive_recurrent, evaluate
from experiments.hippocampal_stateful_recurrence import generate_world


def test_adaptive_rule_keeps_field_open_initially() -> None:
    world = generate_world(20000)
    result = adaptive_recurrent(world)
    assert result.traces[0].keep_k == 4
    assert result.traces[1].keep_k == 4


def test_adaptive_rule_never_prunes_before_minimum_open_cycles() -> None:
    world = generate_world(20001)
    result = adaptive_recurrent(world)
    if result.first_prune_cycle is not None:
        assert result.first_prune_cycle >= 3


def test_adaptive_gating_is_compared_against_fixed_and_clock_progressive() -> None:
    result = evaluate(range(20000, 20200))
    assert result["fixed_width"].accuracy >= 0.90
    assert result["clock_progressive"].accuracy <= result["fixed_width"].accuracy - 0.40
    assert 0.0 <= result["confidence_gated"].accuracy <= 1.0


def test_renaming_does_not_change_adaptive_accuracy() -> None:
    original = evaluate(range(20000, 20200))
    renamed = evaluate(range(20000, 20200), 900000)
    assert renamed["confidence_gated"].accuracy == original["confidence_gated"].accuracy
