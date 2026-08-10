"""Current invariants for the retained E011-A donor mechanism.

The E011-A *assay* is historical evidence (see `test_e011_historical_assay.py`), but
`policy.py` and `policy_learning.py` remain production owners. These tests cover the live
contract only: the action contract, the no-opaque-identity feature invariant, and the rule
that runtime exposes recorded evidence without silently activating cognition.

A failure here is a defect in current production code.
"""

from __future__ import annotations

import pytest

from synrheon.policy import CognitiveAction, CognitiveState, LinearCognitivePolicy, RevealedNode
from synrheon.runtime import SynrheonRuntime

pytestmark = pytest.mark.current


def _state(prefix: str) -> CognitiveState:
    return CognitiveState(
        checkpoint_index=2,
        remaining_budget=8,
        hard_budget=10,
        nodes=(
            RevealedNode(f"{prefix}a", 0, True, 0, False, False),
            RevealedNode(f"{prefix}b", 1, False, 1, True, False),
            RevealedNode(f"{prefix}c", 1, False, 2, True, False),
        ),
        revealed_edges=((f"{prefix}a", f"{prefix}b"), (f"{prefix}a", f"{prefix}c")),
        previous_action=CognitiveAction("EXPAND", f"{prefix}a"),
    )


def test_policy_does_not_use_opaque_identity_as_feature() -> None:
    policy = LinearCognitivePolicy(seed=11)
    left = policy.evaluate(_state("x"))
    right = policy.evaluate(_state("z"))

    assert [item.features for item in left] == [item.features for item in right]
    assert [item.score for item in left] == [item.score for item in right]


def test_stop_requires_no_target_and_expand_requires_target() -> None:
    try:
        CognitiveAction("STOP", "x")
    except ValueError:
        pass
    else:
        raise AssertionError("STOP accepted a target")

    try:
        CognitiveAction("EXPAND")
    except ValueError:
        pass
    else:
        raise AssertionError("EXPAND accepted no target")


def test_runtime_exposes_recorded_growth_evidence_without_invoking_policy() -> None:
    runtime = SynrheonRuntime(cycle_interval_seconds=10.0)
    try:
        before = runtime.snapshot()
        metrics = before["learning_metrics"]
        assert metrics["verdict"] == "E011-A v1 numeric gate passed"
        assert metrics["training_success"] == 0.81
        assert metrics["held_out_success"] == 0.798
        assert metrics["renamed_success"] == 0.798
        assert metrics["strongest_generalization_level"] == "Level 1"

        started = runtime.start()
        assert started["learning_metrics"] == metrics
        assert not any(event["event"] == "cognition_activated" for event in started["trace"])
    finally:
        runtime.close()
