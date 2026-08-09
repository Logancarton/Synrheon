from experiments.hippocampal_learning import (
    CHANNEL_COUNT,
    evaluate,
    generate_episode,
    infer,
    train_resistance,
)


def test_learning_creates_expected_resistance_profile() -> None:
    learner = train_resistance(range(1000, 1120))
    frozen = learner.frozen()
    assert len(frozen) == CHANNEL_COUNT
    assert frozen[0] > 1.5
    assert all(value < 0.8 for value in frozen[1:])


def test_learned_resistance_beats_equal_resistance_on_unseen_worlds() -> None:
    learner = train_resistance(range(1000, 1120))
    frozen = learner.frozen()
    held_out = range(10000, 10200)
    baseline = evaluate(held_out, (1.0,) * CHANNEL_COUNT)
    trained = evaluate(held_out, frozen)
    assert trained.accuracy > 0.95
    assert trained.accuracy >= baseline.accuracy + 0.50


def test_candidate_renaming_does_not_change_transfer() -> None:
    learner = train_resistance(range(1000, 1120))
    frozen = learner.frozen()
    held_out = range(10000, 10200)
    original = evaluate(held_out, frozen)
    renamed = evaluate(held_out, frozen, rename_offset=700_000)
    assert renamed.accuracy == original.accuracy


def test_inference_does_not_mutate_frozen_resistance() -> None:
    learner = train_resistance(range(1000, 1020))
    frozen = learner.frozen()
    episode = generate_episode(10000)
    infer(episode, frozen)
    assert learner.frozen() == frozen
