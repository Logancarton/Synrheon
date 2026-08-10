"""TD-4 known/unknown acquisition routing invariants and stimulus regressions.

The router proposes an acquisition need from mechanical evidence and abstains when the
evidence does not isolate a class. These tests target that process, not preferred answers
for individual sentences.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from threading import Thread
from urllib.request import Request, urlopen

import pytest

from synrheon.acquisition_routing import (
    ROUTER_VERSION,
    AcquisitionReport,
    SpanRoute,
    acquire_route,
    route_segmentation,
)
from synrheon.dev_server import create_development_server
from synrheon.runtime import SynrheonRuntime
from synrheon.surface_segmentation import SEGMENTER_VERSION, segment_surface
from synrheon.token_deck import TokenDeck

pytestmark = pytest.mark.current

SEED_FORMS = ("door", "the", "ran", "to", "Daisy", "well", "open", "paid", "testing")


@pytest.fixture()
def deck() -> TokenDeck:
    seeded = TokenDeck()
    for form in SEED_FORMS:
        seeded.observe(form, evidence_id=f"seed-{form}")
    return seeded


def report_for(text: str, deck: TokenDeck) -> AcquisitionReport:
    return route_segmentation(segment_surface(text), deck)


def route_for(text: str, surface: str, deck: TokenDeck) -> SpanRoute:
    for route in report_for(text, deck).routes:
        if route.surface == surface:
            return route
    raise AssertionError(f"No route for {surface!r} in {text!r}")


def signals(route: SpanRoute) -> list[str]:
    return [item.signal for item in route.evidence]


def test_routing_never_mutates_the_deck(deck: TokenDeck) -> None:
    before = deck.snapshot()

    for text in (
        "Daisy ran to the door.",
        "Logan said, \"Daisy isn't outside.\"",
        "A/B testing improved 3.5%.",
    ):
        report_for(text, deck)

    assert deck.snapshot() == before


def test_known_form_returns_its_identity_and_needs_no_acquisition(deck: TokenDeck) -> None:
    card = deck.resolve_surface("door")
    assert card is not None
    deck.add_sense(card.token_id, sense_key="entry", label="entry", sense_type="concept")

    route = route_for("Daisy ran to the door.", "door", deck)

    assert route.status == "known"
    assert route.acquisition_need == "none"
    assert route.token_id == card.token_id
    assert route.known_sense_ids == tuple(sorted(card.senses))
    assert signals(route) == ["known_form"]


def test_case_variant_of_a_known_form_is_already_known(deck: TokenDeck) -> None:
    # Token identity is case-insensitive, so routing must not re-acquire "The".
    route = route_for("The well-known doctor arrived at 8:30.", "The", deck)

    assert route.status == "known"
    assert route.normalized == "the"


def test_unknown_lowercase_word_routes_to_ordinary_unknown(deck: TokenDeck) -> None:
    route = route_for("The well-known doctor arrived at 8:30.", "doctor", deck)

    assert route.status == "unknown"
    assert route.acquisition_need == "ordinary_unknown_word"
    assert route.token_id is None
    assert route.known_sense_ids == ()


def test_interior_capital_proposes_a_name_rather_than_a_dictionary_word(deck: TokenDeck) -> None:
    route = route_for("BANK Bank bank", "Bank", deck)

    assert route.acquisition_need == "likely_name_or_entity"
    assert "capitalised" in signals(route)
    assert "uninformative_capital" not in signals(route)


def test_sentence_initial_capital_is_treated_as_uninformative(deck: TokenDeck) -> None:
    route = route_for("Logan said, \"Daisy isn't outside.\"", "Logan", deck)

    assert route.acquisition_need == "unresolved"
    assert "uninformative_capital" in signals(route)


def test_sentence_boundary_is_detected_so_position_is_not_guessed(deck: TokenDeck) -> None:
    text = "I met Bank yesterday. BANK is loud."

    interior = route_for(text, "Bank", deck)
    after_full_stop = route_for(text, "BANK", deck)

    assert interior.acquisition_need == "likely_name_or_entity"
    assert "uninformative_capital" in signals(after_full_stop)


def test_opening_quote_does_not_make_a_word_look_interior(deck: TokenDeck) -> None:
    # The first word inside a quotation is orthographically sentence-initial.
    route = route_for('"Rex isn\'t outside."', "Rex", deck)

    assert route.acquisition_need == "unresolved"
    assert "uninformative_capital" in signals(route)


def test_all_capital_form_does_not_claim_to_be_a_name(deck: TokenDeck) -> None:
    route = route_for("I met BANK yesterday.", "BANK", deck)

    assert route.acquisition_need == "unresolved"
    assert "all_capitals" in signals(route)
    assert "uninformative_capital" not in signals(route)


@pytest.mark.parametrize(
    ("text", "surface"),
    (
        ("The well-known doctor arrived at 8:30.", "8:30"),
        ("I paid $12.50.", "12.50"),
        ("A/B testing improved 3.5%.", "3.5"),
        ("The X-15 flew.", "X-15"),
    ),
)
def test_digit_bearing_forms_route_to_number_symbol_or_code(
    text: str, surface: str, deck: TokenDeck
) -> None:
    route = route_for(text, surface, deck)

    assert route.acquisition_need == "number_symbol_or_code"
    assert "contains_digits" in signals(route)


@pytest.mark.parametrize(
    ("text", "surface", "known_part"),
    (
        ("Daisy's running.", "Daisy's", "Daisy"),
        ("The well-known doctor arrived.", "well-known", "well"),
    ),
)
def test_mark_delimited_part_that_is_known_proposes_a_variant(
    text: str, surface: str, known_part: str, deck: TokenDeck
) -> None:
    route = route_for(text, surface, deck)

    assert route.acquisition_need == "variant_candidate"
    assert any(
        item.signal == "contains_known_part" and known_part in item.detail
        for item in route.evidence
    )


def test_variant_evidence_asserts_containment_not_a_lemma(deck: TokenDeck) -> None:
    # "Daisy's" contains a known "Daisy". TD-4 reports that and nothing more: no
    # possessive, stem, or inflection relationship is stored anywhere.
    route = route_for("Daisy's running.", "Daisy's", deck)

    assert route.normalized == "daisy's"
    assert route.token_id is None
    detail = " ".join(item.detail for item in route.evidence).lower()
    assert "possessive" not in detail
    assert "lemma" not in detail


@pytest.mark.parametrize(
    ("text", "surface"),
    (
        ("email@example.com", "email@example.com"),
        ("Logan said, \"Daisy isn't outside.\"", "isn't"),
        ("A/B testing improved.", "A/B"),
    ),
)
def test_mark_structure_without_a_known_part_abstains(
    text: str, surface: str, deck: TokenDeck
) -> None:
    # Structurally complex forms are not ordinary dictionary words, and nothing
    # observable says what they are instead.
    route = route_for(text, surface, deck)

    assert route.acquisition_need == "unresolved"
    assert route.status == "unknown"


def test_evidence_records_every_observed_signal_not_only_the_deciding_one(
    deck: TokenDeck,
) -> None:
    route = route_for("Daisy's running.", "Daisy's", deck)

    # The need is decided by containment, but the capitalisation observations survive.
    assert route.acquisition_need == "variant_candidate"
    assert set(signals(route)) >= {
        "unknown_form",
        "surface_category",
        "contains_known_part",
        "capitalised",
    }


def test_only_lookup_spans_are_routed_and_offsets_still_reference_the_source(
    deck: TokenDeck,
) -> None:
    text = "I paid $12.50."
    segmentation = segment_surface(text)
    report = route_segmentation(segmentation, deck)

    assert [route.surface for route in report.routes] == ["I", "paid", "12.50"]
    for route in report.routes:
        assert text[route.start : route.end] == route.surface
        assert segmentation.spans[route.span_index].text == route.surface


def test_empty_deck_marks_every_lookup_span_unknown() -> None:
    report = report_for("Daisy ran to the door.", TokenDeck())

    assert report.known() == ()
    assert len(report.unknown()) == 5
    assert report.need_counts()["ordinary_unknown_word"] == 4


def test_report_shape_is_stable_and_versioned(deck: TokenDeck) -> None:
    payload = report_for("BANK Bank bank", deck).to_dict()

    assert payload["router_version"] == ROUTER_VERSION
    assert payload["segmenter_version"] == SEGMENTER_VERSION
    assert set(payload) == {
        "router_version",
        "segmenter_version",
        "text",
        "routed_span_count",
        "known_count",
        "unknown_count",
        "need_counts",
        "routes",
    }


def test_acquisition_is_explicit_and_flips_the_route(deck: TokenDeck) -> None:
    text = "The well-known doctor arrived."
    before = route_for(text, "doctor", deck)
    assert before.status == "unknown"

    card = acquire_route(deck, before, evidence_id="experience-1", context_id="episode-1")
    after = route_for(text, "doctor", deck)

    assert after.status == "known"
    assert after.token_id == card.token_id
    assert card.canonical_form == "doctor"
    assert [item.evidence_id for item in card.evidence] == ["experience-1"]
    assert card.evidence[0].context_id == "episode-1"


def test_acquiring_a_name_does_not_make_it_a_dictionary_word(deck: TokenDeck) -> None:
    route = route_for("I met Rex yesterday.", "Rex", deck)
    assert route.acquisition_need == "likely_name_or_entity"

    card = acquire_route(deck, route, evidence_id="experience-2")

    # Identity exists; meaning does not. Deciding what a token can mean is TD-5's job.
    assert card.senses == {}
    assert card.sense_activation == {}
    assert card.surface_forms == {"Rex"}


def test_acquisition_preserves_the_original_surface_form(deck: TokenDeck) -> None:
    route = route_for("I met Rex yesterday.", "Rex", deck)
    card = acquire_route(deck, route, evidence_id="experience-3")

    assert card.canonical_form == "Rex"
    assert card.normalized_form == "rex"
    assert deck.resolve_surface("REX") is card


def test_live_stimulus_exposes_routing_without_acquiring_anything() -> None:
    runtime = SynrheonRuntime(cycle_interval_seconds=10.0)
    try:
        runtime.start()
        substrate_before = runtime.snapshot()["cognitive_substrate"]

        state = runtime.send_external_stimulus("Daisy ran to the door.")
        acquisition = state["stimuli"][-1]["acquisition"]

        assert acquisition["router_version"] == ROUTER_VERSION
        assert acquisition["known_count"] == 0
        assert acquisition["unknown_count"] == 5
        assert any(event["event"] == "acquisition_routed" for event in state["trace"])

        # Observing language must not create identity on its own.
        assert state["cognitive_substrate"] == substrate_before
        assert state["cognitive_substrate"]["token_deck"]["card_count"] == 0
    finally:
        runtime.close()


def test_inspecting_acquisition_does_not_record_or_acquire() -> None:
    runtime = SynrheonRuntime(cycle_interval_seconds=10.0)
    try:
        runtime.start()
        before = runtime.snapshot()

        inspected = runtime.inspect_acquisition("BANK Bank bank")

        assert inspected["need_counts"]["likely_name_or_entity"] == 1
        assert runtime.snapshot() == before
    finally:
        runtime.close()


def test_http_acquisition_endpoint_returns_the_routing_only() -> None:
    runtime = SynrheonRuntime(cycle_interval_seconds=10.0)
    server = create_development_server(runtime, port=0)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address[:2]

    try:
        request = Request(
            f"http://{host}:{port}/api/acquisition",
            data=json.dumps({"text": "I met Rex yesterday."}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=5) as response:
            payload = json.load(response)

        assert payload["ok"] is True
        assert "state" not in payload
        needs = {route["surface"]: route["acquisition_need"] for route in payload["acquisition"]["routes"]}
        assert needs["Rex"] == "likely_name_or_entity"
        assert runtime.snapshot()["cognitive_substrate"]["token_deck"]["card_count"] == 0
    finally:
        server.shutdown()
        server.server_close()
        runtime.close()


def test_explicit_acquisition_is_the_only_thing_that_changes_the_substrate() -> None:
    runtime = SynrheonRuntime(cycle_interval_seconds=10.0)
    try:
        runtime.start()
        text = "Daisy ran to the door."

        stimulus_state = runtime.send_external_stimulus(text)
        assert stimulus_state["cognitive_substrate"]["token_deck"]["card_count"] == 0

        acquired_state = runtime.acquire_from_text(text)
        assert acquired_state["cognitive_substrate"]["token_deck"]["card_count"] == 5
        assert any(event["event"] == "tokens_acquired" for event in acquired_state["trace"])

        # The same stimulus now routes as fully known.
        again = runtime.send_external_stimulus(text)
        assert again["stimuli"][-1]["acquisition"]["known_count"] == 5
        assert again["stimuli"][-1]["acquisition"]["unknown_count"] == 0
    finally:
        runtime.close()


def test_acquisition_can_admit_only_chosen_needs() -> None:
    runtime = SynrheonRuntime(cycle_interval_seconds=10.0)
    try:
        runtime.start()
        text = "I met Rex yesterday."

        runtime.acquire_from_text(text, needs=["likely_name_or_entity"])
        routed = runtime.inspect_acquisition(text)
        needs = {route["surface"]: route["acquisition_need"] for route in routed["routes"]}

        assert routed["known_count"] == 1
        assert needs["Rex"] == "none"
        assert needs["yesterday"] == "ordinary_unknown_word"
        assert needs["I"] == "unresolved"
    finally:
        runtime.close()


def test_acquired_tokens_carry_provenance_and_no_senses() -> None:
    runtime = SynrheonRuntime(cycle_interval_seconds=10.0)
    try:
        runtime.start()
        state = runtime.acquire_from_text("I met Rex yesterday.", needs=["likely_name_or_entity"])
        cards = state["cognitive_substrate"]["token_deck"]["cards"]

        assert len(cards) == 1
        assert cards[0]["canonical_form"] == "Rex"
        assert cards[0]["senses"] == []
        assert cards[0]["evidence"][0]["origin"] == "observed"
        assert cards[0]["evidence"][0]["context_id"] == state["session_id"]
    finally:
        runtime.close()


def test_route_subcommand_prints_the_routing_against_an_empty_deck() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "synrheon", "route", "I met Rex yesterday."],
        capture_output=True,
        text=True,
        check=True,
        cwd=Path(__file__).resolve().parents[1],
        env={**os.environ, "PYTHONPATH": str(Path(__file__).resolve().parents[1] / "src")},
    )
    payload = json.loads(completed.stdout)

    assert payload["router_version"] == ROUTER_VERSION
    assert payload["known_count"] == 0
    needs = {route["surface"]: route["acquisition_need"] for route in payload["routes"]}
    assert needs["Rex"] == "likely_name_or_entity"
