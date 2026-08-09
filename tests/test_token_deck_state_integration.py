"""Token Deck integration with explicit organism state, without live NLP behavior."""

from __future__ import annotations

from synrheon.state import CognitiveSubstrate, OrganismState


def test_cognitive_substrate_owns_observable_token_deck_state() -> None:
    substrate = CognitiveSubstrate()
    card = substrate.token_deck.observe("Daisy", evidence_id="experience-1")
    substrate.token_deck.add_sense(
        card.token_id,
        sense_key="daisy_entity",
        label="Daisy",
        sense_type="entity",
        concept_id="daisy",
        evidence_id="experience-1",
    )

    snapshot = substrate.snapshot()

    assert snapshot["token_deck"]["card_count"] == 1
    assert snapshot["token_deck"]["cards"][0]["token_id"] == card.token_id
    assert snapshot["token_deck"]["cards"][0]["senses"][0]["concept_id"] == "daisy"


def test_new_session_does_not_erase_process_local_token_identity() -> None:
    state = OrganismState()
    card = state.substrate.token_deck.observe("bank", evidence_id="experience-before-session")

    state.begin_session()

    resolved = state.substrate.token_deck.resolve_surface("BANK")
    assert resolved is not None
    assert resolved.token_id == card.token_id
    assert state.substrate.snapshot()["token_deck"]["card_count"] == 1
