
import pytest

from experiments.hippocampal_settling import daisy_leash_scenario, settle, Candidate

pytestmark = pytest.mark.historical


def test_recurrence_can_overturn_initial_winner() -> None:
    result = daisy_leash_scenario(ambiguous=False)
    assert result.first_pass_winner == "Vet"
    assert result.settling.settled
    assert result.settling.winner == "Park"


def test_truth_probe_preserves_exception_possibility() -> None:
    result = daisy_leash_scenario(ambiguous=False)
    assert result.truth_probe.true_support > 0.7
    assert result.truth_probe.always_true_support == 0.0
    assert result.truth_probe.false_possible_support > 0.2


def test_ambiguous_state_requests_discriminator_and_refines() -> None:
    result = daisy_leash_scenario(ambiguous=True)
    assert result.clarification_needed
    assert result.clarification_question == "Did Daisy get into the car?"
    assert result.refined_settling is not None
    assert result.refined_settling.settled
    assert result.refined_settling.winner == "Vet"


def test_positive_resistance_required() -> None:
    bad = (
        Candidate("A", 0.5, (0.5,), 0.0),
        Candidate("B", 0.4, (0.4,), 1.0),
    )
    try:
        settle(bad)
    except ValueError as exc:
        assert "resistance" in str(exc).lower()
    else:
        raise AssertionError("Expected invalid resistance to be rejected")
