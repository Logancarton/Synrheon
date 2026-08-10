"""TD-4 known/unknown acquisition routing for Synrheon.

This owner sits between TD-3 observation and Token Deck identity. For each lookup span
it answers two questions:

    does Synrheon already hold a usable representation for this form?
    if not, what kind of acquisition would be needed?

Routing is **read-only**. It never creates a token card, a sense, or a concept, and it
never mutates the deck. Acquisition is a separate explicit call, so observing language can
never silently become identity.

The acquisition need is a *proposal carrying its evidence*, not truth. Every mechanical
signal observed for a span is recorded, including signals that did not determine the
proposed need, so a later learned router can be compared against this one on the same
observations.

Where orthography is genuinely uninformative the router abstains with ``unresolved``
rather than guessing. Sentence-initial capitalisation is the main such case: in English a
capital there carries no information about whether the form is a name.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from synrheon.surface_segmentation import SurfaceSegmentation, SurfaceSpan
from synrheon.token_deck import TokenCard, TokenDeck, TokenOrigin, normalize_surface

ROUTER_VERSION = "td4-acquisition-routing-v1"

#: Marks treated as sentence-final when deciding whether a capital is uninformative.
#: Widening this set only widens abstention, so an omission makes the router more
#: confident and an addition makes it more cautious. It is deliberately small.
SENTENCE_FINAL_MARKS: frozenset[str] = frozenset(".!?…。！？")

RouteStatus = Literal["known", "unknown"]

AcquisitionNeed = Literal[
    "none",
    "likely_name_or_entity",
    "variant_candidate",
    "ordinary_unknown_word",
    "number_symbol_or_code",
    "unresolved",
]


@dataclass(frozen=True, slots=True)
class RouteEvidence:
    """One mechanical observation about a span, recorded whether or not it decided the route."""

    signal: str
    detail: str

    def to_dict(self) -> dict[str, object]:
        return {"signal": self.signal, "detail": self.detail}


@dataclass(frozen=True, slots=True)
class SpanRoute:
    """The routing outcome for one lookup span, with full source coordinates."""

    span_index: int
    start: int
    end: int
    surface: str
    normalized: str
    status: RouteStatus
    acquisition_need: AcquisitionNeed
    token_id: str | None = None
    known_sense_ids: tuple[str, ...] = ()
    evidence: tuple[RouteEvidence, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "span_index": self.span_index,
            "start": self.start,
            "end": self.end,
            "surface": self.surface,
            "normalized": self.normalized,
            "status": self.status,
            "acquisition_need": self.acquisition_need,
            "token_id": self.token_id,
            "known_sense_ids": list(self.known_sense_ids),
            "evidence": [item.to_dict() for item in self.evidence],
        }


@dataclass(frozen=True, slots=True)
class AcquisitionReport:
    """Complete routing of one segmentation against one deck at one moment."""

    router_version: str
    segmenter_version: str
    text: str
    routes: tuple[SpanRoute, ...]

    def known(self) -> tuple[SpanRoute, ...]:
        return tuple(route for route in self.routes if route.status == "known")

    def unknown(self) -> tuple[SpanRoute, ...]:
        return tuple(route for route in self.routes if route.status == "unknown")

    def with_need(self, need: AcquisitionNeed) -> tuple[SpanRoute, ...]:
        return tuple(route for route in self.routes if route.acquisition_need == need)

    def need_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for route in self.routes:
            counts[route.acquisition_need] = counts.get(route.acquisition_need, 0) + 1
        return dict(sorted(counts.items()))

    def to_dict(self) -> dict[str, object]:
        return {
            "router_version": self.router_version,
            "segmenter_version": self.segmenter_version,
            "text": self.text,
            "routed_span_count": len(self.routes),
            "known_count": len(self.known()),
            "unknown_count": len(self.unknown()),
            "need_counts": self.need_counts(),
            "routes": [route.to_dict() for route in self.routes],
        }


def route_segmentation(segmentation: SurfaceSegmentation, deck: TokenDeck) -> AcquisitionReport:
    """Route every lookup span against the deck without mutating anything.

    Only lookup spans are routed. Whitespace, punctuation, and symbol spans remain fully
    described by the segmentation and are referenced by ``span_index``.
    """

    routes = [
        _route_span(span, segmentation, deck)
        for span in segmentation.spans
        if span.is_lookup_candidate
    ]
    return AcquisitionReport(
        router_version=ROUTER_VERSION,
        segmenter_version=segmentation.segmenter_version,
        text=segmentation.text,
        routes=tuple(routes),
    )


def acquire_route(
    deck: TokenDeck,
    route: SpanRoute,
    *,
    evidence_id: str,
    origin: TokenOrigin = "observed",
    context_id: str | None = None,
) -> TokenCard:
    """Commit one routed span to the deck as a stable token identity.

    This is the only path from observation to identity, and it must be called explicitly.
    No sense is created: deciding what a token can mean belongs to TD-5, not to
    acquisition. External dictionary/parser/LLM assistance may later propose senses with
    their own provenance, and a proposal still will not be truth.
    """

    return deck.observe(
        route.surface,
        evidence_id=evidence_id,
        origin=origin,
        context_id=context_id,
    )


def _route_span(
    span: SurfaceSpan,
    segmentation: SurfaceSegmentation,
    deck: TokenDeck,
) -> SpanRoute:
    normalized = span.normalized or normalize_surface(span.text)
    evidence: list[RouteEvidence] = []

    card = deck.resolve_surface(span.text)
    if card is not None:
        evidence.append(
            RouteEvidence(
                signal="known_form",
                detail=f"{normalized!r} resolves to {card.token_id} with {len(card.senses)} sense(s)",
            )
        )
        return SpanRoute(
            span_index=span.index,
            start=span.start,
            end=span.end,
            surface=span.text,
            normalized=normalized,
            status="known",
            acquisition_need="none",
            token_id=card.token_id,
            known_sense_ids=tuple(sorted(card.senses)),
            evidence=tuple(evidence),
        )

    evidence.append(RouteEvidence(signal="unknown_form", detail=f"{normalized!r} is not in the deck"))
    evidence.append(RouteEvidence(signal="surface_category", detail=span.category))

    has_digits = span.category in {"numeric", "alphanumeric"}
    if has_digits:
        evidence.append(
            RouteEvidence(signal="contains_digits", detail=f"category {span.category}")
        )

    variant_of = _known_part(span, deck)
    if variant_of is not None:
        part, part_card = variant_of
        evidence.append(
            RouteEvidence(
                signal="contains_known_part",
                detail=f"mark-delimited part {part!r} resolves to {part_card.token_id}",
            )
        )
    elif span.internal_marks:
        evidence.append(
            RouteEvidence(
                signal="mark_delimited_structure",
                detail=(
                    "contains internal mark(s) "
                    f"{''.join(mark.char for mark in span.internal_marks)!r} and no known part"
                ),
            )
        )

    capitalised = span.text != span.text.lower()
    all_capitals = capitalised and len(span.text) > 1 and span.text == span.text.upper()
    sentence_initial = _is_sentence_initial(span, segmentation)
    if capitalised:
        evidence.append(
            RouteEvidence(
                signal="capitalised",
                detail="sentence-initial position" if sentence_initial else "interior position",
            )
        )
        if sentence_initial:
            evidence.append(
                RouteEvidence(
                    signal="uninformative_capital",
                    detail="sentence-initial capitalisation carries no name evidence",
                )
            )
        if all_capitals:
            evidence.append(
                RouteEvidence(
                    signal="all_capitals",
                    detail="all-capital form; acronym, emphasis, and name are not distinguished",
                )
            )

    return SpanRoute(
        span_index=span.index,
        start=span.start,
        end=span.end,
        surface=span.text,
        normalized=normalized,
        status="unknown",
        acquisition_need=_acquisition_need(
            span,
            has_digits=has_digits,
            has_known_part=variant_of is not None,
            capitalised=capitalised,
            all_capitals=all_capitals,
            sentence_initial=sentence_initial,
        ),
        evidence=tuple(evidence),
    )


def _acquisition_need(
    span: SurfaceSpan,
    *,
    has_digits: bool,
    has_known_part: bool,
    capitalised: bool,
    all_capitals: bool,
    sentence_initial: bool,
) -> AcquisitionNeed:
    """Choose one proposed need. Every observed signal is recorded regardless.

    The router abstains wherever the available orthographic evidence does not isolate a
    single class. Abstaining is cheap; a wrong confident class would propagate into
    identity.
    """

    if has_digits:
        return "number_symbol_or_code"
    if has_known_part:
        return "variant_candidate"
    if span.internal_marks:
        # Mark-delimited structure with no known part: not an ordinary dictionary word,
        # and nothing observable says what it is instead.
        return "unresolved"
    if capitalised and not sentence_initial and not all_capitals:
        # Names and entities must not be treated as dictionary words by default.
        return "likely_name_or_entity"
    if capitalised:
        # Sentence-initial or all-capital: the capital carries no isolating evidence.
        return "unresolved"
    if span.category == "alpha":
        return "ordinary_unknown_word"
    return "unresolved"


def _known_part(span: SurfaceSpan, deck: TokenDeck) -> tuple[str, TokenCard] | None:
    """Find a mark-delimited part of an unknown span that the deck already knows.

    This reports containment, which is observable. It asserts no lemma, stem, or
    inflection relationship: ``Daisy's`` containing a known ``Daisy`` is evidence that the
    form is worth examining as a variant, not a claim that it is a possessive.
    """

    if not span.internal_marks:
        return None

    for part in _mark_delimited_parts(span):
        card = deck.resolve_surface(part)
        if card is not None:
            return part, card
    return None


def _mark_delimited_parts(span: SurfaceSpan) -> list[str]:
    """Split a span at its observed internal marks: ``Daisy's`` -> ``Daisy``, ``s``."""

    parts: list[str] = []
    cursor = 0
    for mark in span.internal_marks:
        relative = mark.offset - span.start
        part = span.text[cursor:relative]
        if part:
            parts.append(part)
        cursor = relative + len(mark.char)
    tail = span.text[cursor:]
    if tail:
        parts.append(tail)
    return parts


def _is_sentence_initial(span: SurfaceSpan, segmentation: SurfaceSegmentation) -> bool:
    """Whether only whitespace and non-terminal punctuation precede this span.

    Opening quotes and brackets are skipped, so the first word inside a quotation is
    treated as sentence-initial and therefore as orthographically uninformative.
    """

    for previous in reversed(segmentation.spans[: span.index]):
        if previous.category == "whitespace":
            continue
        if previous.is_lookup_candidate:
            return False
        if any(character in SENTENCE_FINAL_MARKS for character in previous.text):
            return True
        continue
    return True


__all__ = [
    "ROUTER_VERSION",
    "SENTENCE_FINAL_MARKS",
    "AcquisitionNeed",
    "AcquisitionReport",
    "RouteEvidence",
    "RouteStatus",
    "SpanRoute",
    "acquire_route",
    "route_segmentation",
]
