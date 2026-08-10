"""TD-3 exact surface segmentation for Synrheon.

This owner converts raw text into ordered, offset-preserving surface spans. It is
deliberately mechanical: every decision is derivable from Unicode character classes
and adjacency in the original string.

It does not select a sense, fabricate a concept/entity, infer truth, assign a part of
speech, consult an LLM, create token identities, or discard punctuation. Those belong
to the Token Deck (identity), TD-4 (known/unknown routing), TD-5 (sense learning), and
later cognitive owners.

Two invariants make the segmenter replaceable without invalidating stable token/sense
identities:

    every character of the input belongs to exactly one span
    "".join(span.text for span in spans) == original text

Because the segmenter never assigns a token ID, a later segmenter version may change
span boundaries without disturbing any identity the Token Deck already owns.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal
import unicodedata

from synrheon.token_deck import normalize_surface

SEGMENTER_VERSION = "td3-exact-surface-v1"

SpanCategory = Literal[
    "alpha",
    "numeric",
    "alphanumeric",
    "whitespace",
    "punctuation",
    "symbol",
    "other",
]

#: Categories whose spans carry a normalized lookup form. Lookup eligibility is a
#: mechanical property of the characters, not a claim that the span is a known word.
LOOKUP_CATEGORIES: frozenset[str] = frozenset({"alpha", "numeric", "alphanumeric"})


@dataclass(frozen=True, slots=True)
class SurfaceMark:
    """A punctuation/symbol character observed *inside* a lexical span.

    A mark is absorbed only when it is directly flanked by lexical characters on both
    sides. Recording it preserves the observation without interpreting it: ``Daisy's``
    reports an internal apostrophe, it does not report a possessive.
    """

    offset: int
    char: str

    def to_dict(self) -> dict[str, object]:
        return {"offset": self.offset, "char": self.char}


@dataclass(frozen=True, slots=True)
class SurfaceSpan:
    """One contiguous observed surface unit with exact source coordinates."""

    index: int
    start: int
    end: int
    text: str
    category: SpanCategory
    normalized: str | None = None
    internal_marks: tuple[SurfaceMark, ...] = ()

    @property
    def is_lookup_candidate(self) -> bool:
        """Whether this span could be offered to identity lookup by a later stage."""

        return self.category in LOOKUP_CATEGORIES

    def to_dict(self) -> dict[str, object]:
        return {
            "index": self.index,
            "start": self.start,
            "end": self.end,
            "text": self.text,
            "category": self.category,
            "normalized": self.normalized,
            "is_lookup_candidate": self.is_lookup_candidate,
            "internal_marks": [mark.to_dict() for mark in self.internal_marks],
        }


@dataclass(frozen=True, slots=True)
class SurfaceSegmentation:
    """Complete, gap-free segmentation of one exact input string."""

    segmenter_version: str
    text: str
    spans: tuple[SurfaceSpan, ...]

    def __post_init__(self) -> None:
        _require_exact_coverage(self.text, self.spans)

    def reconstruct(self) -> str:
        """Rebuild the original text from spans alone."""

        return "".join(span.text for span in self.spans)

    def lookup_spans(self) -> tuple[SurfaceSpan, ...]:
        """Spans a later stage may offer to identity lookup; no lookup happens here."""

        return tuple(span for span in self.spans if span.is_lookup_candidate)

    def category_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for span in self.spans:
            counts[span.category] = counts.get(span.category, 0) + 1
        return dict(sorted(counts.items()))

    def to_dict(self) -> dict[str, object]:
        return {
            "segmenter_version": self.segmenter_version,
            "text": self.text,
            "span_count": len(self.spans),
            "lookup_span_count": len(self.lookup_spans()),
            "category_counts": self.category_counts(),
            "reconstructs_exactly": self.reconstruct() == self.text,
            "spans": [span.to_dict() for span in self.spans],
        }


def segment_surface(text: str) -> SurfaceSegmentation:
    """Segment raw text into exact ordered surface spans.

    Deterministic for a given ``SEGMENTER_VERSION``. Whitespace runs are preserved as
    spans so the original string is fully recoverable from the segmentation alone.
    """

    if not isinstance(text, str):
        raise TypeError("Surface segmentation requires a string.")

    spans: list[SurfaceSpan] = []
    length = len(text)
    position = 0
    index = 0

    while position < length:
        character = text[position]
        if _is_whitespace(character):
            end = _consume_whitespace_run(text, position)
            span = SurfaceSpan(
                index=index,
                start=position,
                end=end,
                text=text[position:end],
                category="whitespace",
            )
        elif _is_lexical(character):
            end, marks = _consume_lexical_run(text, position)
            body = text[position:end]
            category = _lexical_category(body)
            span = SurfaceSpan(
                index=index,
                start=position,
                end=end,
                text=body,
                category=category,
                normalized=_lookup_form(body) if category in LOOKUP_CATEGORIES else None,
                internal_marks=marks,
            )
        else:
            # One span per standalone mark character: maximal granularity keeps
            # punctuation provenance inspectable and requires no grouping judgement.
            end = position + 1
            span = SurfaceSpan(
                index=index,
                start=position,
                end=end,
                text=character,
                category=_mark_category(character),
            )

        spans.append(span)
        position = end
        index += 1

    return SurfaceSegmentation(
        segmenter_version=SEGMENTER_VERSION,
        text=text,
        spans=tuple(spans),
    )


def _consume_whitespace_run(text: str, start: int) -> int:
    position = start + 1
    while position < len(text) and _is_whitespace(text[position]):
        position += 1
    return position


def _consume_lexical_run(text: str, start: int) -> tuple[int, tuple[SurfaceMark, ...]]:
    """Consume letters/digits plus any mark directly flanked by lexical characters.

    The left flank is guaranteed by construction: the run begins on a lexical
    character and every absorbed mark is immediately followed by one.
    """

    length = len(text)
    position = start + 1
    marks: list[SurfaceMark] = []

    while position < length:
        character = text[position]
        if _is_lexical(character):
            position += 1
            continue
        if _is_whitespace(character):
            break
        if position + 1 < length and _is_lexical(text[position + 1]):
            marks.append(SurfaceMark(offset=position, char=character))
            position += 2
            continue
        break

    return position, tuple(marks)


def _is_whitespace(character: str) -> bool:
    return character.isspace()


def _is_lexical(character: str) -> bool:
    return character.isalnum() or unicodedata.category(character).startswith("M")


def _lexical_category(body: str) -> SpanCategory:
    has_alpha = any(character.isalpha() for character in body)
    has_number = any(unicodedata.category(character).startswith("N") for character in body)
    if has_alpha and has_number:
        return "alphanumeric"
    if has_alpha:
        return "alpha"
    if has_number:
        return "numeric"
    return "other"


def _mark_category(character: str) -> SpanCategory:
    category = unicodedata.category(character)
    if category.startswith("P"):
        return "punctuation"
    if category.startswith("S"):
        return "symbol"
    return "other"


def _lookup_form(body: str) -> str | None:
    normalized = normalize_surface(body)
    return normalized or None


def _require_exact_coverage(text: str, spans: tuple[SurfaceSpan, ...]) -> None:
    expected_start = 0
    for position, span in enumerate(spans):
        if span.index != position:
            raise ValueError(f"Span index {span.index} is out of order at position {position}.")
        if span.start != expected_start:
            raise ValueError(
                f"Span {span.index} starts at {span.start}; expected {expected_start}."
            )
        if span.end <= span.start:
            raise ValueError(f"Span {span.index} has a non-positive width.")
        if span.text != text[span.start : span.end]:
            raise ValueError(f"Span {span.index} text does not match its source offsets.")
        expected_start = span.end

    if expected_start != len(text):
        raise ValueError(
            f"Segmentation covers {expected_start} of {len(text)} characters; "
            "every character must belong to exactly one span."
        )


__all__ = [
    "LOOKUP_CATEGORIES",
    "SEGMENTER_VERSION",
    "SpanCategory",
    "SurfaceMark",
    "SurfaceSegmentation",
    "SurfaceSpan",
    "segment_surface",
]
