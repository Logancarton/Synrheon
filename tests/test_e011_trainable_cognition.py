"""High-value scientific regression tests for the first trainable cognition assay."""

from __future__ import annotations

from experiments.e011a import assess_pass_gate, full_assay, generate_world
from synrheon.cognition import CognitiveAction, CognitiveState, LinearCognitivePolicy, RevealedNode
from synrheon.runtime import SynrheonRuntime


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


def test_generated_world_respects_frozen_size_and_depth() -> None:
    for seed in range(1000, 1030):
        world = generate_world(seed)
        assert 10 <= len(world.handles) <= 14
        assert 3 <= world.shortest_path_edges <= 5
        assert world.shortest_path[0] == world.start
        assert world.shortest_path[-1] == world.goal
        for source, target in zip(world.shortest_path, world.shortest_path[1:]):
            assert target in world.adjacency[source]


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


def test_quick_assay_learns_and_transfers_without_identity_shortcut() -> None:
    report = full_assay(quick=True)
    gate = assess_pass_gate(report)

    assert gate["passed_numeric_gate"] is True
    assert gate["median_held_out_success"] >= 0.70
    assert gate["median_renamed_success"] == gate["median_held_out_success"]
    assert gate["random_valid_success"] < gate["median_held_out_success"]


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
