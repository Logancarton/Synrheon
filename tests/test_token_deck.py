"""Token Deck TD-0/1/2 representation invariants."""

from __future__ import annotations

import pytest

from synrheon.token_deck import TokenDeck

pytestmark = pytest.mark.current


def test_repeated_surface_observation_reuses_stable_token_identity() -> None:
    deck = TokenDeck()

    first = deck.observe("Bank", evidence_id="event-1")
    second = deck.observe("bank", evidence_id="event-2")

    assert first is second
    assert first.token_id == second.token_id
    assert first.canonical_form == "Bank"
    assert first.normalized_form == "bank"
    assert first.surface_forms == {"Bank", "bank"}
    assert first.usage_count == 2
    assert [item.evidence_id for item in first.evidence] == ["event-1", "event-2"]


def test_explicit_alias_and_morphology_share_token_without_inference() -> None:
    deck = TokenDeck()
    card = deck.observe(
        "run",
        evidence_id="event-run",
        morphology={"lemma": "run", "form": "base"},
    )

    deck.add_alias(
        card.token_id,
        "ran",
        evidence_id="event-ran",
        morphology={"lemma": "run", "tense": "past"},
    )

    assert deck.resolve_surface("ran") is card
    assert deck.resolve_surface("RUN") is card
    assert card.morphology_by_form["ran"] == {"lemma": "run", "tense": "past"}


def test_one_token_retains_multiple_senses_distinct_from_concept_identity() -> None:
    deck = TokenDeck()
    card = deck.observe("bank", evidence_id="event-1")

    financial = deck.add_sense(
        card.token_id,
        sense_key="financial_institution",
        label="financial institution",
        sense_type="concept",
        concept_id="concept:financial-bank",
        evidence_id="sense-evidence-1",
    )
    river = deck.add_sense(
        card.token_id,
        sense_key="river_edge",
        label="river edge",
        sense_type="concept",
        concept_id="concept:river-bank",
        evidence_id="sense-evidence-2",
    )

    assert financial.sense_id != river.sense_id
    assert financial.sense_id != card.token_id
    assert financial.concept_id != card.token_id
    assert set(card.senses) == {financial.sense_id, river.sense_id}
    assert card.sense_activation[financial.sense_id] == pytest.approx(0.5)
    assert card.sense_activation[river.sense_id] == pytest.approx(0.5)


def test_context_can_reverse_leading_sense_without_deleting_alternative() -> None:
    deck = TokenDeck()
    card = deck.observe("bank", evidence_id="event-1")
    financial = deck.add_sense(
        card.token_id,
        sense_key="financial",
        label="financial institution",
        sense_type="concept",
    )
    river = deck.add_sense(
        card.token_id,
        sense_key="river",
        label="river edge",
        sense_type="concept",
    )

    first = deck.set_context_activation(
        card.token_id,
        context_id="deposit-money",
        support={financial.sense_id: 0.9, river.sense_id: 0.1},
    )
    assert deck.ranked_senses(card.token_id)[0][0].sense_id == financial.sense_id

    second = deck.set_context_activation(
        card.token_id,
        context_id="ducks-by-water",
        support={financial.sense_id: 0.05, river.sense_id: 0.95},
    )
    assert second.sequence == 2
    assert deck.ranked_senses(card.token_id)[0][0].sense_id == river.sense_id
    assert set(card.sense_activation) == {financial.sense_id, river.sense_id}
    assert card.sense_activation[financial.sense_id] > 0.0

    restored = deck.restore_context(card.token_id, first.sequence)
    assert restored.context_id == "deposit-money"
    assert deck.ranked_senses(card.token_id)[0][0].sense_id == financial.sense_id


def test_newly_discovered_sense_reopens_previous_settled_inventory() -> None:
    deck = TokenDeck()
    card = deck.observe("bank", evidence_id="event-1")
    financial = deck.add_sense(
        card.token_id,
        sense_key="financial",
        label="financial institution",
        sense_type="concept",
    )
    river = deck.add_sense(
        card.token_id,
        sense_key="river",
        label="river edge",
        sense_type="concept",
    )
    checkpoint = deck.set_context_activation(
        card.token_id,
        context_id="money",
        support={financial.sense_id: 0.99, river.sense_id: 0.01},
    )

    aircraft = deck.add_sense(
        card.token_id,
        sense_key="aircraft_turn",
        label="aircraft turn",
        sense_type="action",
    )

    assert card.current_context_id is None
    assert set(card.sense_activation) == {
        financial.sense_id,
        river.sense_id,
        aircraft.sense_id,
    }
    assert all(value == pytest.approx(1.0 / 3.0) for value in card.sense_activation.values())

    with pytest.raises(ValueError, match="current sense inventory"):
        deck.restore_context(card.token_id, checkpoint.sequence)


def test_context_update_cannot_silently_drop_a_known_sense() -> None:
    deck = TokenDeck()
    card = deck.observe("bank", evidence_id="event-1")
    financial = deck.add_sense(
        card.token_id,
        sense_key="financial",
        label="financial institution",
        sense_type="concept",
    )
    deck.add_sense(
        card.token_id,
        sense_key="river",
        label="river edge",
        sense_type="concept",
    )

    with pytest.raises(ValueError, match="complete sense inventory"):
        deck.set_context_activation(
            card.token_id,
            context_id="money",
            support={financial.sense_id: 1.0},
        )


def test_snapshot_preserves_provenance_forms_senses_and_context_history() -> None:
    deck = TokenDeck()
    card = deck.observe("Daisy", evidence_id="experience-7", context_id="episode-1")
    entity = deck.add_sense(
        card.token_id,
        sense_key="daisy_entity",
        label="Daisy",
        sense_type="entity",
        concept_id="daisy",
        evidence_id="experience-7",
    )
    deck.set_context_activation(
        card.token_id,
        context_id="episode-1",
        support={entity.sense_id: 1.0},
    )

    snapshot = deck.snapshot()
    stored = snapshot["cards"][0]

    assert snapshot["card_count"] == 1
    assert stored["evidence"][0]["evidence_id"] == "experience-7"
    assert stored["senses"][0]["concept_id"] == "daisy"
    assert stored["context_checkpoints"][0]["context_id"] == "episode-1"
