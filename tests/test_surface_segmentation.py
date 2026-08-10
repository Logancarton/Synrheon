"""TD-3 exact surface segmentation invariants and adversarial stimulus regressions.

Every case here tests a *process* property — exact recovery, offset provenance,
mechanical categorisation, absence of meaning inference — rather than a preferred
answer for one sentence.
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

from synrheon.dev_server import create_development_server
from synrheon.runtime import SynrheonRuntime
from synrheon.surface_segmentation import (
    SEGMENTER_VERSION,
    SurfaceSegmentation,
    SurfaceSpan,
    segment_surface,
)

pytestmark = pytest.mark.current

ROADMAP_STIMULI = (
    "Daisy ran to the door.",
    "Daisy's running.",
    "Don't open the door.",
    "The well-known doctor arrived at 8:30.",
    "I paid $12.50.",
    'Logan said, "Daisy isn\'t outside."',
    "email@example.com",
    "A/B testing improved 3.5%.",
    "BANK Bank bank",
)

HARDER_STIMULI = (
    "",
    "   ",
    "  leading and trailing  ",
    "line one\nline two\r\ntab\there",
    "The dogs' bowls.",
    "Wait... really?",
    "well--known and well—known",
    "The U.S. economy",
    "1,000,000 and 1.000,50",
    "https://example.com/path?q=1&r=2",
    "café vs café",
    "ﬁne ＡＢＣ",
    "Daisy \U0001f415 barked \U0001f44d\U0001f3fd",
    "İstanbul",
    "non breaking space",
    "​zero width",
    "3½ cups",
    "coöperate re‑enter",
    "@handle #tag $TICKER",
    "a1b2c3 X-15 COVID-19",
)


def texts(segmentation: SurfaceSegmentation) -> list[str]:
    return [span.text for span in segmentation.spans]


def visible(segmentation: SurfaceSegmentation) -> list[str]:
    return [span.text for span in segmentation.spans if span.category != "whitespace"]


def marks(span: SurfaceSpan) -> str:
    return "".join(mark.char for mark in span.internal_marks)


def find(segmentation: SurfaceSegmentation, text: str) -> SurfaceSpan:
    for span in segmentation.spans:
        if span.text == text:
            return span
    raise AssertionError(f"No span with text {text!r} in {texts(segmentation)}")


@pytest.mark.parametrize("text", ROADMAP_STIMULI + HARDER_STIMULI)
def test_every_span_traces_back_to_the_exact_source_string(text: str) -> None:
    segmentation = segment_surface(text)

    assert segmentation.reconstruct() == text
    assert segmentation.to_dict()["reconstructs_exactly"] is True
    assert segmentation.segmenter_version == SEGMENTER_VERSION

    cursor = 0
    for position, span in enumerate(segmentation.spans):
        assert span.index == position
        assert span.start == cursor
        assert span.end > span.start
        assert span.text == text[span.start : span.end]
        cursor = span.end
    assert cursor == len(text)


@pytest.mark.parametrize("text", ROADMAP_STIMULI + HARDER_STIMULI)
def test_segmentation_is_deterministic_and_idempotent(text: str) -> None:
    first = segment_surface(text)
    second = segment_surface(text)

    assert first == second
    assert segment_surface(first.reconstruct()) == first


def test_empty_text_produces_an_empty_but_valid_segmentation() -> None:
    segmentation = segment_surface("")

    assert segmentation.spans == ()
    assert segmentation.reconstruct() == ""
    assert segmentation.lookup_spans() == ()


def test_sentence_punctuation_is_separated_rather_than_discarded() -> None:
    segmentation = segment_surface("Daisy ran to the door.")

    assert visible(segmentation) == ["Daisy", "ran", "to", "the", "door", "."]
    assert find(segmentation, ".").category == "punctuation"
    assert find(segmentation, ".").normalized is None
    assert find(segmentation, "door").end == 21


def test_contractions_and_possessives_stay_one_span_with_an_observable_apostrophe() -> None:
    for text, expected in (
        ("Daisy's running.", "Daisy's"),
        ("Don't open the door.", "Don't"),
        ('Logan said, "Daisy isn\'t outside."', "isn't"),
    ):
        span = find(segment_surface(text), expected)
        assert span.category == "alpha"
        assert marks(span) == "'"
        # The apostrophe is reported as an observed internal mark, never as a
        # possessive/negation claim, and the clitic is not stripped from the form.
        assert span.normalized == expected.casefold()


def test_trailing_apostrophe_is_not_absorbed_into_the_word() -> None:
    segmentation = segment_surface("The dogs' bowls.")

    assert visible(segmentation) == ["The", "dogs", "'", "bowls", "."]
    assert find(segmentation, "dogs").internal_marks == ()
    assert find(segmentation, "'").category == "punctuation"


def test_a_mark_joins_a_span_only_when_flanked_by_lexical_characters() -> None:
    single = segment_surface("The well-known doctor")
    doubled = segment_surface("well--known")

    joined = find(single, "well-known")
    assert joined.category == "alpha"
    assert marks(joined) == "-"

    assert visible(doubled) == ["well", "-", "-", "known"]


def test_times_and_decimals_are_numeric_compounds_not_interpreted_values() -> None:
    time_span = find(segment_surface("The well-known doctor arrived at 8:30."), "8:30")
    decimal_span = find(segment_surface("A/B testing improved 3.5%."), "3.5")

    assert time_span.category == "numeric"
    assert marks(time_span) == ":"
    assert decimal_span.category == "numeric"
    assert marks(decimal_span) == "."
    # No field claims "time" or "percentage"; category metadata stays mechanical.
    assert set(time_span.to_dict()) == {
        "index",
        "start",
        "end",
        "text",
        "category",
        "normalized",
        "is_lookup_candidate",
        "internal_marks",
    }


def test_currency_symbol_is_kept_separate_from_its_number() -> None:
    segmentation = segment_surface("I paid $12.50.")

    assert visible(segmentation) == ["I", "paid", "$", "12.50", "."]
    assert find(segmentation, "$").category == "symbol"
    assert find(segmentation, "12.50").category == "numeric"
    assert find(segmentation, "12.50").start == 8


def test_quotes_and_commas_survive_as_distinct_punctuation_spans() -> None:
    segmentation = segment_surface('Logan said, "Daisy isn\'t outside."')

    assert visible(segmentation) == [
        "Logan",
        "said",
        ",",
        '"',
        "Daisy",
        "isn't",
        "outside",
        ".",
        '"',
    ]
    assert [span.category for span in segmentation.spans if span.text == '"'] == [
        "punctuation",
        "punctuation",
    ]


def test_case_variants_share_a_lookup_form_while_keeping_distinct_offsets() -> None:
    segmentation = segment_surface("BANK Bank bank")
    lookups = segmentation.lookup_spans()

    assert [span.text for span in lookups] == ["BANK", "Bank", "bank"]
    assert {span.normalized for span in lookups} == {"bank"}
    assert [(span.start, span.end) for span in lookups] == [(0, 4), (5, 9), (10, 14)]


def test_letter_and_digit_mixtures_are_reported_as_alphanumeric() -> None:
    segmentation = segment_surface("a1b2c3 X-15 COVID-19")

    assert [span.category for span in segmentation.lookup_spans()] == [
        "alphanumeric",
        "alphanumeric",
        "alphanumeric",
    ]
    assert marks(find(segmentation, "COVID-19")) == "-"


def test_whitespace_runs_are_preserved_so_layout_is_recoverable() -> None:
    segmentation = segment_surface("line one\nline two\r\ntab\there")
    whitespace = [span.text for span in segmentation.spans if span.category == "whitespace"]

    assert whitespace == [" ", "\n", " ", "\r\n", "\t"]
    assert all(span.normalized is None for span in segmentation.spans if span.category == "whitespace")


def test_leading_and_trailing_whitespace_is_not_trimmed_away() -> None:
    segmentation = segment_surface("  leading and trailing  ")

    assert segmentation.spans[0].text == "  "
    assert segmentation.spans[-1].text == "  "
    assert segmentation.reconstruct() == "  leading and trailing  "


def test_compatibility_normalization_never_moves_character_offsets() -> None:
    # NFKC changes length ("ﬁ" -> "fi", "½" -> "1⁄2"); offsets must stay on the source.
    ligature = find(segment_surface("ﬁne ＡＢＣ"), "ﬁne")
    fraction = find(segment_surface("3½ cups"), "3½")

    assert ligature.normalized == "fine"
    assert (ligature.start, ligature.end) == (0, 3)
    assert len(ligature.normalized) != ligature.end - ligature.start

    assert fraction.category == "numeric"
    assert (fraction.start, fraction.end) == (0, 2)


def test_invisible_characters_are_not_silently_discarded() -> None:
    leading = segment_surface("​zero width")
    embedded = segment_surface("wo​rd")

    assert leading.spans[0].text == "​"
    assert leading.reconstruct() == "​zero width"

    # A zero-width character between letters is absorbed but stays reportable.
    joined = find(embedded, "wo​rd")
    assert marks(joined) == "​"


def test_emoji_and_non_ascii_letters_round_trip_without_loss() -> None:
    segmentation = segment_surface("Daisy \U0001f415 barked")

    assert find(segmentation, "\U0001f415").category == "symbol"
    assert find(segmentation, "\U0001f415").normalized is None
    assert segmentation.reconstruct() == "Daisy \U0001f415 barked"
    assert find(segment_surface("café vs café"), "café").category == "alpha"


def test_lookup_candidates_exclude_whitespace_symbols_and_punctuation() -> None:
    segmentation = segment_surface("I paid $12.50.")

    assert [span.text for span in segmentation.lookup_spans()] == ["I", "paid", "12.50"]
    assert segmentation.category_counts() == {
        "alpha": 2,
        "numeric": 1,
        "punctuation": 1,
        "symbol": 1,
        "whitespace": 2,
    }


def test_segmentation_records_no_token_sense_or_concept_identity() -> None:
    # TD-3 stops at observation. Identity stays with the Token Deck so the segmenter
    # can be replaced later without invalidating any stable token or sense.
    span_fields = set(find(segment_surface("bank"), "bank").to_dict())

    assert not span_fields & {"token_id", "sense_id", "concept_id", "sense", "meaning"}
    assert set(segment_surface("bank").to_dict()) == {
        "segmenter_version",
        "text",
        "span_count",
        "lookup_span_count",
        "category_counts",
        "reconstructs_exactly",
        "spans",
    }


def test_compound_marks_are_recorded_rather_than_split_by_convention() -> None:
    # Frozen consequence of the flanking rule: mark-joined compounds stay whole and
    # every absorbed mark is reported, so a later stage can re-split without the
    # segmenter guessing that a span is an address, a URL, or an abbreviation.
    email = find(segment_surface("email@example.com"), "email@example.com")
    abbreviation = find(segment_surface("The U.S. economy"), "U.S")

    assert marks(email) == "@."
    assert email.category == "alpha"
    assert marks(abbreviation) == "."
    assert visible(segment_surface("The U.S. economy")) == ["The", "U.S", ".", "economy"]


@pytest.mark.parametrize(
    ("spans", "problem"),
    (
        ((SurfaceSpan(index=0, start=0, end=2, text="ab", category="alpha"),), "of 4 characters"),
        (
            (
                SurfaceSpan(index=0, start=0, end=2, text="ab", category="alpha"),
                SurfaceSpan(index=1, start=3, end=4, text="d", category="alpha"),
            ),
            "expected 2",
        ),
        ((SurfaceSpan(index=0, start=0, end=4, text="abXd", category="alpha"),), "does not match"),
    ),
)
def test_incomplete_or_mismatched_coverage_is_rejected(
    spans: tuple[SurfaceSpan, ...], problem: str
) -> None:
    with pytest.raises(ValueError, match=problem):
        SurfaceSegmentation(segmenter_version=SEGMENTER_VERSION, text="abcd", spans=spans)


def test_non_string_input_is_rejected() -> None:
    with pytest.raises(TypeError, match="requires a string"):
        segment_surface(None)  # type: ignore[arg-type]


def test_live_stimulus_exposes_its_segmentation_without_creating_identity() -> None:
    runtime = SynrheonRuntime(cycle_interval_seconds=10.0)
    try:
        runtime.start()
        substrate_before = runtime.snapshot()["cognitive_substrate"]

        state = runtime.send_external_stimulus("Daisy's at the door.")
        stimulus = state["stimuli"][-1]
        segmentation = stimulus["segmentation"]

        assert segmentation["segmenter_version"] == SEGMENTER_VERSION
        assert segmentation["reconstructs_exactly"] is True
        assert [span["text"] for span in segmentation["spans"] if span["is_lookup_candidate"]] == [
            "Daisy's",
            "at",
            "the",
            "door",
        ]
        assert any(event["event"] == "surface_segmented" for event in state["trace"])

        # Observation must not become identity: no token card, sense, or concept.
        assert state["cognitive_substrate"] == substrate_before
        assert state["cognitive_substrate"]["token_deck"]["card_count"] == 0
    finally:
        runtime.close()


def test_inspecting_a_stimulus_does_not_record_it() -> None:
    runtime = SynrheonRuntime(cycle_interval_seconds=10.0)
    try:
        runtime.start()
        before = runtime.snapshot()

        inspected = runtime.inspect_segmentation("BANK Bank bank")

        assert inspected["lookup_span_count"] == 3
        assert runtime.snapshot() == before
    finally:
        runtime.close()


def test_http_segment_endpoint_returns_the_observation_only() -> None:
    runtime = SynrheonRuntime(cycle_interval_seconds=10.0)
    server = create_development_server(runtime, port=0)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address[:2]

    try:
        request = Request(
            f"http://{host}:{port}/api/segment",
            data=json.dumps({"text": "I paid $12.50."}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=5) as response:
            payload = json.load(response)

        assert payload["ok"] is True
        assert "state" not in payload
        assert payload["segmentation"]["reconstructs_exactly"] is True
        assert [span["text"] for span in payload["segmentation"]["spans"]] == [
            "I",
            " ",
            "paid",
            " ",
            "$",
            "12.50",
            ".",
        ]
        assert runtime.snapshot()["stimuli"] == []
    finally:
        server.shutdown()
        server.server_close()
        runtime.close()


def test_segment_subcommand_prints_the_exact_observation() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "synrheon", "segment", "The well-known doctor arrived at 8:30."],
        capture_output=True,
        text=True,
        check=True,
        cwd=Path(__file__).resolve().parents[1],
        env={**os.environ, "PYTHONPATH": str(Path(__file__).resolve().parents[1] / "src")},
    )
    payload = json.loads(completed.stdout)

    assert payload["segmenter_version"] == SEGMENTER_VERSION
    assert payload["reconstructs_exactly"] is True
    assert payload["text"] == "The well-known doctor arrived at 8:30."
