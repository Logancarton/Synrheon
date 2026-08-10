"""Historical reproduction — state-dependent recurrent settling assay (E4).

Superseded research generation. These tests verify that the preserved historical result is
still reproduced; they do not assert that the original hypothesis is true.

Preserved outcome on seeds 20000-20200:

```text
one_pass                            0.000
recurrent, progressive sparsity     0.255   <- fails its own >= 0.80 gate
recurrent, sparsity disabled        0.980
progressive advantage over fixed   -0.725
frozen verdict                      MIXED RESULT
```

Recorded conclusion: state-dependent recurrence works; the clock-driven hard-pruning
schedule is what fails. `keep_k` drops to 2 at step 6 and zeroes one member of a
mutually-excitatory triad, which removes its excitation, flips the ranking, and zeroes a
different member next cycle. The field enters a limit cycle instead of settling, so the
reported winner is an artifact of the stopping cycle.

This is historical evidence for `suppressed != deleted`. Do not repair the schedule to
make the original threshold pass.
"""

from __future__ import annotations

import pytest

from experiments.hippocampal_stateful_recurrence import (
    evaluate,
    generate_world,
    one_pass,
    recurrent,
)

pytestmark = pytest.mark.historical

#: Frozen thresholds from the original preregistration, preserved verbatim.
PREREGISTERED_MINIMUM_ACCURACY = 0.80
PREREGISTERED_MINIMUM_ADVANTAGE = 0.25


def test_one_pass_is_lured_by_initial_activation() -> None:
    world = generate_world(20000)
    result = one_pass(world)
    assert result.winner != world.correct_name


def test_hard_pruning_still_prevents_recurrence_from_settling() -> None:
    """Reproduce the recorded failure: the frozen default does not overturn the lure."""

    world = generate_world(20000)
    pruned = recurrent(world)
    unpruned = recurrent(world, progressive_sparsity=False)

    # The historical negative result: with the frozen pruning schedule the correct
    # candidate does not win.
    assert pruned.winner != world.correct_name
    assert len(pruned.cycles) > 2

    # And the diagnosis it produced: the same mechanism succeeds without hard pruning.
    assert unpruned.winner == world.correct_name


def test_progressive_sparsity_reproduces_its_failed_preregistered_gate() -> None:
    """Reproduce the recorded accuracies and the failure of the original criterion."""

    result = evaluate(range(20000, 20200))
    one = result["one_pass"]
    progressive = result["recurrent_progressive"]
    fixed = result["recurrent_fixed"]

    assert one.accuracy == pytest.approx(0.0)
    assert progressive.accuracy == pytest.approx(0.255)
    assert fixed.accuracy == pytest.approx(0.98)
    assert result["progressive_advantage_over_fixed"] == pytest.approx(-0.725)

    # The preregistered gate is preserved and still fails on accuracy.
    assert progressive.accuracy < PREREGISTERED_MINIMUM_ACCURACY
    assert progressive.accuracy >= one.accuracy + PREREGISTERED_MINIMUM_ADVANTAGE

    # Without hard pruning the same gate would have passed. That contrast is the finding.
    assert fixed.accuracy >= PREREGISTERED_MINIMUM_ACCURACY
    assert fixed.accuracy >= one.accuracy + PREREGISTERED_MINIMUM_ADVANTAGE


def test_candidate_renaming_preserves_result() -> None:
    original = evaluate(range(20000, 20200))
    renamed = evaluate(range(20000, 20200), rename_offset=900_000)
    assert renamed["recurrent_progressive"].accuracy == original["recurrent_progressive"].accuracy
    assert renamed["one_pass"].accuracy == original["one_pass"].accuracy
