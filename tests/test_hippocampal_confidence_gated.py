"""Historical reproduction — confidence-gated adaptive sparsity assay.

Superseded research generation. These tests verify that the preserved historical result is
still reproduced; they do not assert that the original hypothesis is true.

Preserved outcome on seeds 30000-30500:

```text
adaptive accuracy                   0.850
fixed-width accuracy                0.852
active state savings vs fixed       0.0761  <- fails its own >= 0.10 criterion
frozen verdict                      MIXED RESULT
```

Recorded conclusion: adaptive gating preserved accuracy but did not deliver the
preregistered efficiency benefit. The hypothesis failed on cost, not on correctness. Do
not retune the gate to reach 0.10.
"""

from __future__ import annotations

import pytest

from experiments.hippocampal_confidence_gated import (
    WORLD_TYPES,
    adaptive_recurrent,
    evaluate,
    generate_mixed_world,
    verdict,
)

pytestmark = pytest.mark.historical

#: Frozen efficiency criterion from the original preregistration, preserved verbatim.
PREREGISTERED_MINIMUM_STATE_SAVINGS = 0.10


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


def test_adaptive_gating_preserved_accuracy_but_failed_its_efficiency_criterion() -> None:
    """Reproduce the recorded outcome: accuracy held, the efficiency gate did not."""

    result = evaluate(range(30000, 30500))
    adaptive = result["confidence_gated"]
    fixed = result["fixed_width"]
    savings = result["active_state_savings_vs_fixed"]

    # The half of the hypothesis that held.
    assert adaptive.accuracy >= fixed.accuracy - 0.05
    assert adaptive.accuracy == pytest.approx(0.85)
    assert fixed.accuracy == pytest.approx(0.852)

    # The half that failed, with the preregistered threshold preserved beside it.
    assert savings == pytest.approx(0.07611111111111113, abs=1e-9)
    assert savings < PREREGISTERED_MINIMUM_STATE_SAVINGS

    assert verdict(result) == "MIXED RESULT"


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
