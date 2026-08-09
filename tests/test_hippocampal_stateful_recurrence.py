from experiments.hippocampal_stateful_recurrence import (
    evaluate,
    generate_world,
    one_pass,
    recurrent,
)


def test_one_pass_is_lured_by_initial_activation() -> None:
    world = generate_world(20000)
    result = one_pass(world)
    assert result.winner != world.correct_name


def test_stateful_recurrence_can_overturn_lure() -> None:
    world = generate_world(20000)
    result = recurrent(world)
    assert result.winner == world.correct_name
    assert len(result.cycles) > 2


def test_recurrence_materially_beats_one_pass_on_unseen_worlds() -> None:
    result = evaluate(range(20000, 20200))
    one = result["one_pass"]
    rec = result["recurrent_progressive"]
    assert rec.accuracy >= 0.80
    assert rec.accuracy >= one.accuracy + 0.25


def test_candidate_renaming_preserves_result() -> None:
    original = evaluate(range(20000, 20200))
    renamed = evaluate(range(20000, 20200), rename_offset=900_000)
    assert renamed["recurrent_progressive"].accuracy == original["recurrent_progressive"].accuracy
    assert renamed["one_pass"].accuracy == original["one_pass"].accuracy
