"""Historical reproduction — stochastic multi-trial consensus assay.

Superseded research generation. These tests verify that the preserved historical result is
still reproduced; they do not assert that the original hypothesis is true.

Preserved outcome on seeds 40000-40250, `unresolved_close` worlds:

```text
committed_rate                      0.78   <- preregistered criterion is <= 0.35
max_trial_rate                      0.22
overall_correct_or_abstain_rate     0.22
frozen verdict                      DISCOUNTED
```

Two preregistered criteria fail. The classifier reports the sampling-exercise criterion
first (`max_trial_rate < 0.50`), so that is the verdict string returned; the commitment
criterion (`committed_rate > 0.35`) fails independently and is asserted separately here.

Recorded conclusion: population consensus manufactured agreement on worlds built to be
genuinely unresolvable. This is part of why `winner != sufficient evidence` survived into
the current architecture. Do not adjust the consensus mechanism to force abstention here.
"""

from __future__ import annotations

import pytest

from experiments.hippocampal_confidence_gated import generate_mixed_world
from experiments.hippocampal_consensus_trials import (
    consensus_trials,
    evaluate,
    perturb_world,
    verdict,
)

pytestmark = pytest.mark.historical

#: Frozen abstention criterion from the original preregistration, preserved verbatim:
#: "more than 35% of unresolved-close worlds are forced into commitment" discounts the
#: hypothesis. This matches the `> 0.35` branch in the frozen `verdict()` classifier.
PREREGISTERED_MAXIMUM_UNRESOLVED_COMMITMENT = 0.35

#: The sampling-exercise criterion the classifier checks first.
PREREGISTERED_MINIMUM_UNRESOLVED_MAX_TRIAL_RATE = 0.50


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


def test_unresolved_worlds_still_reproduce_the_false_consensus_failure() -> None:
    """Reproduce the recorded outcome: consensus commits where it should abstain."""

    result = evaluate(range(40000, 40250))
    unresolved = result["unresolved_close"]

    assert unresolved.committed_rate == pytest.approx(0.78)
    assert unresolved.max_trial_rate == pytest.approx(0.22)
    assert unresolved.overall_correct_or_abstain_rate == pytest.approx(0.22)

    # Both preregistered criteria are preserved and both still fail.
    assert unresolved.committed_rate > PREREGISTERED_MAXIMUM_UNRESOLVED_COMMITMENT
    assert unresolved.max_trial_rate < PREREGISTERED_MINIMUM_UNRESOLVED_MAX_TRIAL_RATE

    # The classifier reports the sampling-exercise criterion, which it checks first.
    assert verdict(result) == (
        "DISCOUNTED: genuinely unresolved worlds too often produced a false population consensus."
    )


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
