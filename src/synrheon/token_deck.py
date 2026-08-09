"""Stable lexical/sense representation for Synrheon's Token Deck.

The Token Deck owns representational identity and provenance, not language truth.
Its central separation is:

    surface form != token identity != sense != concept/entity

The first slice deliberately does not segment raw text, infer morphology, choose a
correct sense, query an LLM, or mutate world knowledge. It provides the cognitive
physics needed for those skills to be learned/tested later.

Sense activation is context-conditional and reversible. A weak sense remains present
unless the sense inventory itself is explicitly changed.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from hashlib import sha256
import math
from typing import Literal, Mapping
import unicodedata

TokenOrigin = Literal["observed", "injected", "dictionary", "llm", "learned"]


@dataclass(frozen=True, slots=True)
class TokenEvidence:
    """Provenance for one observed/injected/acquired use of a token form."""

    evidence_id: str
    origin: TokenOrigin
    surface_form: str
    context_id: str | None = None

    def __post_init__(self) -> None:
        if not self.evidence_id.strip():
            raise ValueError("Token evidence ID is required.")
        if not self.surface_form.strip():
            raise ValueError("Token evidence surface form is required.")
        if self.context_id is not None and not self.context_id.strip():
            raise ValueError("Context ID must be non-empty when supplied.")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(slots=True)
class SenseRecord:
    """One possible meaning/use of a token card.

    ``sense_type`` is intentionally open-ended. The architecture does not impose a
    permanent noun/verb/entity/etc. ontology. ``concept_id`` is an optional bridge to
    world identity and is never substituted for the token or sense ID.
    """

    sense_id: str
    sense_key: str
    label: str
    sense_type: str
    origin: TokenOrigin
    concept_id: str | None = None
    evidence_ids: list[str] = field(default_factory=list)
    usage_count: int = 0

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class SenseContextCheckpoint:
    """Reversible context-conditioned activation over a complete sense inventory."""

    sequence: int
    context_id: str
    activation: dict[str, float]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(slots=True)
class TokenCard:
    """Stable token identity with forms, senses, provenance, and current sense state."""

    token_id: str
    canonical_form: str
    normalized_form: str
    surface_forms: set[str] = field(default_factory=set)
    morphology_by_form: dict[str, dict[str, str]] = field(default_factory=dict)
    evidence: list[TokenEvidence] = field(default_factory=list)
    senses: dict[str, SenseRecord] = field(default_factory=dict)
    sense_activation: dict[str, float] = field(default_factory=dict)
    current_context_id: str | None = None
    context_checkpoints: list[SenseContextCheckpoint] = field(default_factory=list)
    usage_count: int = 0

    def to_dict(self) -> dict[str, object]:
        return {
            "token_id": self.token_id,
            "canonical_form": self.canonical_form,
            "normalized_form": self.normalized_form,
            "surface_forms": sorted(self.surface_forms),
            "morphology_by_form": {
                form: dict(sorted(metadata.items()))
                for form, metadata in sorted(self.morphology_by_form.items())
            },
            "evidence": [item.to_dict() for item in self.evidence],
            "senses": [self.senses[key].to_dict() for key in sorted(self.senses)],
            "sense_activation": dict(self.sense_activation),
            "current_context_id": self.current_context_id,
            "context_checkpoints": [item.to_dict() for item in self.context_checkpoints],
            "usage_count": self.usage_count,
        }


@dataclass(slots=True)
class TokenDeck:
    """Registry of stable token cards and reversible candidate senses.

    This object deliberately provides storage/invariants rather than a tokenizer or
    disambiguation policy. Callers may explicitly register forms/senses and supply
    context-conditioned support only from visible evidence.
    """

    cards: dict[str, TokenCard] = field(default_factory=dict)
    form_index: dict[str, str] = field(default_factory=dict)

    def observe(
        self,
        surface_form: str,
        *,
        evidence_id: str,
        origin: TokenOrigin = "observed",
        context_id: str | None = None,
        morphology: Mapping[str, str] | None = None,
    ) -> TokenCard:
        """Observe a surface form, creating or reusing one stable token card."""

        surface = _clean_surface(surface_form)
        normalized = normalize_surface(surface)
        token_id = self.form_index.get(normalized)
        if token_id is None:
            token_id = _token_id_for(normalized)
            existing = self.cards.get(token_id)
            if existing is not None and existing.normalized_form != normalized:
                raise RuntimeError("Stable token ID collision detected.")
            card = TokenCard(
                token_id=token_id,
                canonical_form=surface,
                normalized_form=normalized,
            )
            self.cards[token_id] = card
            self.form_index[normalized] = token_id
        else:
            card = self.cards[token_id]

        self._record_form(
            card,
            surface,
            evidence_id=evidence_id,
            origin=origin,
            context_id=context_id,
            morphology=morphology,
        )
        return card

    def add_alias(
        self,
        token_id: str,
        surface_form: str,
        *,
        evidence_id: str,
        origin: TokenOrigin = "injected",
        context_id: str | None = None,
        morphology: Mapping[str, str] | None = None,
    ) -> TokenCard:
        """Explicitly register another surface/morphological form for a token card."""

        card = self.require_card(token_id)
        surface = _clean_surface(surface_form)
        normalized = normalize_surface(surface)
        existing = self.form_index.get(normalized)
        if existing is not None and existing != token_id:
            raise ValueError(
                f"Surface form {surface!r} is already registered to another token: {existing}"
            )
        self.form_index[normalized] = token_id
        self._record_form(
            card,
            surface,
            evidence_id=evidence_id,
            origin=origin,
            context_id=context_id,
            morphology=morphology,
        )
        return card

    def add_sense(
        self,
        token_id: str,
        *,
        sense_key: str,
        label: str,
        sense_type: str,
        origin: TokenOrigin = "injected",
        concept_id: str | None = None,
        evidence_id: str | None = None,
    ) -> SenseRecord:
        """Add one explicit candidate sense without selecting it as truth."""

        card = self.require_card(token_id)
        cleaned_key = _clean_identifier(sense_key, "Sense key").casefold()
        cleaned_label = _clean_identifier(label, "Sense label")
        cleaned_type = _clean_identifier(sense_type, "Sense type")
        cleaned_concept = concept_id.strip() if concept_id is not None else None
        if cleaned_concept == "":
            raise ValueError("Concept ID must be non-empty when supplied.")

        sense_id = _sense_id_for(token_id, cleaned_key)
        existing = card.senses.get(sense_id)
        if existing is not None:
            if (
                existing.sense_key != cleaned_key
                or existing.label != cleaned_label
                or existing.sense_type != cleaned_type
                or existing.concept_id != cleaned_concept
            ):
                raise ValueError(
                    "Existing sense identity cannot be silently redefined; create a new sense key."
                )
            if evidence_id is not None:
                _append_unique(existing.evidence_ids, _clean_identifier(evidence_id, "Evidence ID"))
            return existing

        record = SenseRecord(
            sense_id=sense_id,
            sense_key=cleaned_key,
            label=cleaned_label,
            sense_type=cleaned_type,
            origin=origin,
            concept_id=cleaned_concept,
        )
        if evidence_id is not None:
            record.evidence_ids.append(_clean_identifier(evidence_id, "Evidence ID"))
        card.senses[sense_id] = record

        # A newly discovered alternative invalidates any settled distribution over the
        # previously incomplete inventory. Reopen neutrally rather than assigning the
        # new sense permanent zero support.
        self._reopen_sense_inventory(card)
        return record

    def set_context_activation(
        self,
        token_id: str,
        *,
        context_id: str,
        support: Mapping[str, float],
    ) -> SenseContextCheckpoint:
        """Install reversible support over every currently known sense.

        The complete sense key set is required so a caller cannot silently delete an
        alternative by omitting it from an update.
        """

        card = self.require_card(token_id)
        context = _clean_identifier(context_id, "Context ID")
        if not card.senses:
            raise ValueError("Cannot settle sense activation before senses exist.")
        expected = set(card.senses)
        supplied = set(support)
        if supplied != expected:
            missing = sorted(expected - supplied)
            extra = sorted(supplied - expected)
            raise ValueError(
                "Context activation must preserve the complete sense inventory; "
                f"missing={missing}, extra={extra}."
            )

        card.sense_activation = _normalize_support(support)
        card.current_context_id = context
        checkpoint = SenseContextCheckpoint(
            sequence=len(card.context_checkpoints) + 1,
            context_id=context,
            activation=dict(card.sense_activation),
        )
        card.context_checkpoints.append(checkpoint)
        return checkpoint

    def reopen_senses(self, token_id: str) -> None:
        """Return all known senses to neutral support without deleting history."""

        self._reopen_sense_inventory(self.require_card(token_id))

    def restore_context(self, token_id: str, sequence: int) -> SenseContextCheckpoint:
        """Restore an earlier context state when its sense inventory still matches."""

        card = self.require_card(token_id)
        for checkpoint in card.context_checkpoints:
            if checkpoint.sequence != sequence:
                continue
            if set(checkpoint.activation) != set(card.senses):
                raise ValueError(
                    "Cannot exactly restore a checkpoint created before the current sense inventory."
                )
            card.sense_activation = dict(checkpoint.activation)
            card.current_context_id = checkpoint.context_id
            return checkpoint
        raise KeyError(f"Unknown sense checkpoint sequence: {sequence}")

    def ranked_senses(self, token_id: str) -> list[tuple[SenseRecord, float]]:
        """Return all senses ranked by current activation; no sense is omitted."""

        card = self.require_card(token_id)
        return [
            (card.senses[sense_id], value)
            for sense_id, value in sorted(
                card.sense_activation.items(),
                key=lambda item: (-item[1], item[0]),
            )
        ]

    def resolve_surface(self, surface_form: str) -> TokenCard | None:
        normalized = normalize_surface(_clean_surface(surface_form))
        token_id = self.form_index.get(normalized)
        return self.cards.get(token_id) if token_id is not None else None

    def require_card(self, token_id: str) -> TokenCard:
        try:
            return self.cards[token_id]
        except KeyError as exc:
            raise KeyError(f"Unknown token card: {token_id}") from exc

    def snapshot(self) -> dict[str, object]:
        return {
            "card_count": len(self.cards),
            "form_count": len(self.form_index),
            "cards": [self.cards[key].to_dict() for key in sorted(self.cards)],
        }

    def _record_form(
        self,
        card: TokenCard,
        surface: str,
        *,
        evidence_id: str,
        origin: TokenOrigin,
        context_id: str | None,
        morphology: Mapping[str, str] | None,
    ) -> None:
        evidence = TokenEvidence(
            evidence_id=_clean_identifier(evidence_id, "Token evidence ID"),
            origin=origin,
            surface_form=surface,
            context_id=context_id.strip() if context_id is not None else None,
        )
        card.surface_forms.add(surface)
        if morphology is not None:
            card.morphology_by_form[surface] = {
                _clean_identifier(str(key), "Morphology key"): _clean_identifier(
                    str(value), "Morphology value"
                )
                for key, value in morphology.items()
            }
        duplicate = any(
            item.evidence_id == evidence.evidence_id
            and item.origin == evidence.origin
            and item.surface_form == evidence.surface_form
            and item.context_id == evidence.context_id
            for item in card.evidence
        )
        if not duplicate:
            card.evidence.append(evidence)
            card.usage_count += 1

    @staticmethod
    def _reopen_sense_inventory(card: TokenCard) -> None:
        if not card.senses:
            card.sense_activation = {}
        else:
            neutral = 1.0 / len(card.senses)
            card.sense_activation = {sense_id: neutral for sense_id in card.senses}
        card.current_context_id = None


def normalize_surface(surface_form: str) -> str:
    """Minimal stable form normalization; this is not linguistic lemmatization."""

    return unicodedata.normalize("NFKC", surface_form).strip().casefold()


def _token_id_for(normalized_form: str) -> str:
    digest = sha256(normalized_form.encode("utf-8")).hexdigest()[:16]
    return f"tok:{digest}"


def _sense_id_for(token_id: str, sense_key: str) -> str:
    digest = sha256(f"{token_id}\0{sense_key}".encode("utf-8")).hexdigest()[:16]
    return f"sense:{digest}"


def _normalize_support(values: Mapping[str, float]) -> dict[str, float]:
    cleaned: dict[str, float] = {}
    for key, raw in values.items():
        value = float(raw)
        if not math.isfinite(value) or value < 0.0:
            raise ValueError("Sense support must be finite and non-negative.")
        cleaned[key] = value
    total = sum(cleaned.values())
    if total <= 0.0:
        neutral = 1.0 / len(cleaned)
        return {key: neutral for key in cleaned}
    return {key: value / total for key, value in cleaned.items()}


def _clean_surface(value: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("Surface form is required.")
    return cleaned


def _clean_identifier(value: str, label: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{label} is required.")
    return cleaned


def _append_unique(values: list[str], value: str) -> None:
    if value not in values:
        values.append(value)


__all__ = [
    "SenseContextCheckpoint",
    "SenseRecord",
    "TokenCard",
    "TokenDeck",
    "TokenEvidence",
    "TokenOrigin",
    "normalize_surface",
]
