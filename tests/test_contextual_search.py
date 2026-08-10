from __future__ import annotations

import pytest

from synrheon.contextual_search import ReversibleCandidateField

pytestmark = pytest.mark.current


def test_soft_suppression_never_deletes_dormant_candidate_state() -> None:
    field = ReversibleCandidateField({"a": 0.6, "b": 0.3, "c": 0.1})
    field.replace_activation(
        {"a": 0.75, "b": 0.249, "c": 0.001},
        context_id="partial",
        transition="carry",
        active_ids=("a", "b"),
    )

    assert field.active == {"a", "b"}
    assert field.dormant == {"c"}
    assert "c" in field.activation
    assert field.activation["c"] > 0.0

    field.reactivate(("c",))
    assert field.active == {"a", "b", "c"}
    assert field.activation["c"] > 0.0


def test_reset_and_carry_return_distinct_transition_priors() -> None:
    field = ReversibleCandidateField({"a": 0.5, "b": 0.3, "c": 0.2})
    field.replace_activation(
        {"a": 0.1, "b": 0.2, "c": 0.7},
        context_id="partial",
        transition="carry",
    )

    assert field.prior_for("carry") == field.activation
    assert field.prior_for("residual") == field.activation
    assert field.prior_for("reset") == field.retrieval_prior
    assert field.prior_for("reset") != field.prior_for("carry")


def test_checkpoint_restore_recovers_activation_and_active_region() -> None:
    field = ReversibleCandidateField({"a": 0.6, "b": 0.25, "c": 0.15})
    first = field.replace_activation(
        {"a": 0.7, "b": 0.2, "c": 0.1},
        context_id="stage-1",
        transition="carry",
        active_ids=("a", "b"),
    )
    assert first is not None

    field.replace_activation(
        {"a": 0.1, "b": 0.2, "c": 0.7},
        context_id="stage-2",
        transition="residual",
        active_ids=("b", "c"),
    )
    field.restore(first.sequence)

    assert field.active == {"a", "b"}
    assert field.dormant == {"c"}
    assert field.activation == first.activation


def test_candidate_field_rejects_silent_hard_deletion() -> None:
    field = ReversibleCandidateField({"a": 0.5, "b": 0.5})

    with pytest.raises(ValueError, match="preserve the complete broad field"):
        field.replace_activation(
            {"a": 1.0},
            context_id="bad-stage",
            transition="carry",
        )


def test_snapshot_exposes_transition_provenance_without_truth_labels() -> None:
    field = ReversibleCandidateField({"x": 0.4, "y": 0.35, "z": 0.25})
    field.replace_activation(
        {"x": 0.15, "y": 0.75, "z": 0.10},
        context_id="identity-context",
        transition="residual",
        active_ids=("y", "z"),
    )

    snapshot = field.snapshot()
    checkpoint = snapshot["checkpoints"][0]
    assert snapshot["candidate_count"] == 3
    assert snapshot["dormant"] == ["x"]
    assert checkpoint["transition"] == "residual"
    assert "correct" not in checkpoint
    assert "qrel" not in checkpoint
