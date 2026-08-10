
import pytest

from experiments.hippocampal_equivalence import (
    compare_episode,
    evaluate_equivalence,
    exact_one_pass,
    interpret,
)
from experiments.hippocampal_learning import (
    CHANNEL_COUNT,
    candidates_from_episode,
    generate_episode,
    train_resistance,
)
from experiments.hippocampal_settling import settle

pytestmark = pytest.mark.historical


def test_exact_one_pass_matches_first_cycle_winner() -> None:
    learner = train_resistance(range(1000, 1040))
    episode = generate_episode(10000)
    candidates = candidates_from_episode(episode, learner.frozen())
    one_pass = exact_one_pass(candidates)
    recurrent = settle(
        candidates,
        cycles=1,
        sparsity_schedule=(3,),
        settle_gap=0.0,
    )
    assert recurrent.winner == one_pass.winner


def test_comparison_uses_frozen_resistance_without_mutation() -> None:
    learner = train_resistance(range(1000, 1040))
    frozen = learner.frozen()
    episode = generate_episode(10001)
    compare_episode(episode, frozen)
    assert learner.frozen() == frozen
    assert len(frozen) == CHANNEL_COUNT


def test_equivalence_assay_survives_candidate_renaming() -> None:
    learner = train_resistance(range(1000, 1120))
    frozen = learner.frozen()
    held_out = range(10000, 10100)
    original = evaluate_equivalence(held_out, frozen)
    renamed = evaluate_equivalence(held_out, frozen, rename_offset=900_000)
    assert renamed.one_pass_accuracy == original.one_pass_accuracy
    assert renamed.recurrent_progressive_accuracy == original.recurrent_progressive_accuracy
    assert renamed.one_pass_recurrent_agreement == original.one_pass_recurrent_agreement


def test_interpretation_reports_one_of_predeclared_outcomes() -> None:
    learner = train_resistance(range(1000, 1120))
    summary = evaluate_equivalence(range(10000, 10200), learner.frozen())
    verdict = interpret(summary)
    assert verdict.startswith((
        "CURRENT RECURRENCE NOT YET NECESSARY",
        "EVIDENCE FOR RECURRENT VALUE",
        "MIXED RESULT",
    ))
