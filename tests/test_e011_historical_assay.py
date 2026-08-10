"""Historical reproduction — E011-A first trainable cognition assay.

Superseded research generation. Revision 6 classifies E011-A as historical controlled
evidence: it remains the donor result behind `policy.py`, but it is no longer the active
architecture target. These tests verify that the preserved result is still reproduced;
they do not make "the old hypothesis must pass" the meaning of pytest success.

Live `policy.py` / `runtime.py` invariants live in `test_e011_policy_invariants.py`.

Preserved outcome, `full_assay(quick=True)`:

```text
median_held_out_success        0.785
median_renamed_success         0.785
median_renaming_retention      1.000
median_renaming_absolute_drop  0.000
median_untrained_success       0.000
random_valid_success           0.065
frozen numeric gate            PASSED (all nine checks true)
```

Recorded conclusion: operation/target preferences were learned and transferred to unseen
and renamed synthetic worlds without an opaque-identity shortcut. This is a *positive*
historical result, preserved the same way as the negative ones — by recording the
observations and the frozen classifier's verdict rather than asserting the hypothesis.
"""

from __future__ import annotations

import pytest

from experiments.e011a import assess_pass_gate, full_assay, generate_world

pytestmark = pytest.mark.historical

#: Frozen numeric-gate thresholds from the E011-A preregistration, preserved verbatim.
PREREGISTERED_MINIMUM_HELD_OUT_SUCCESS = 0.70


def test_generated_world_respects_frozen_size_and_depth() -> None:
    for seed in range(1000, 1030):
        world = generate_world(seed)
        assert 10 <= len(world.handles) <= 14
        assert 3 <= world.shortest_path_edges <= 5
        assert world.shortest_path[0] == world.start
        assert world.shortest_path[-1] == world.goal
        for source, target in zip(world.shortest_path, world.shortest_path[1:]):
            assert target in world.adjacency[source]


def test_quick_assay_reproduces_its_preserved_observations() -> None:
    """Reproduce the recorded measurements, independent of the gate's conclusion."""

    gate = assess_pass_gate(full_assay(quick=True))

    assert gate["median_held_out_success"] == pytest.approx(0.785)
    assert gate["median_renamed_success"] == pytest.approx(0.785)
    assert gate["median_renaming_retention"] == pytest.approx(1.0)
    assert gate["median_renaming_absolute_drop"] == pytest.approx(0.0)
    assert gate["median_untrained_success"] == pytest.approx(0.0)
    assert gate["random_valid_success"] == pytest.approx(0.065)


def test_frozen_numeric_gate_still_returns_its_preserved_verdict() -> None:
    """Lock observation, threshold, and frozen classifier together."""

    gate = assess_pass_gate(full_assay(quick=True))

    # The preserved conclusion: this assay's gate passed.
    assert gate["passed_numeric_gate"] is True
    assert all(gate["checks"].values())

    # The thresholds that produced it, preserved beside the observations.
    assert gate["median_held_out_success"] >= PREREGISTERED_MINIMUM_HELD_OUT_SUCCESS
    assert gate["median_renamed_success"] == gate["median_held_out_success"]
    assert gate["random_valid_success"] < gate["median_held_out_success"]
