"""Current-state to next-state cognitive activation owner.

This first live cognitive mechanism deliberately stays small:
- map text to already-known concepts using generic lexical cue matching
- spread activation through directed world relations
- let open-ended organism relations increase salience only for already-reached concepts
- apply decay, competition, and bounded Top-K selection
- return observable activation evidence without exposing hidden chain-of-thought

It is not semantic language understanding, retrieval, response generation, or autonomy.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import re

from synrheon.core import (
    ActivationContribution,
    CognitiveFrame,
    CognitiveSubstrate,
    OrganismRelation,
)

_TOKEN_RE = re.compile(r"[a-z0-9]+")


@dataclass(slots=True, frozen=True)
class ActivationConfig:
    """General sparse-activation mechanics, independent of stimulus meaning."""

    seed_strength: float = 1.0
    decay: float = 0.30
    spread_gain: float = 0.62
    organism_gain: float = 0.35
    inhibition_fraction: float = 0.10
    activation_floor: float = 0.05
    top_k: int = 5
    rounds: int = 3


DEFAULT_ACTIVATION_CONFIG = ActivationConfig()


def activate_from_text(
    substrate: CognitiveSubstrate,
    *,
    text: str,
    experience_event_id: str,
    config: ActivationConfig = DEFAULT_ACTIVATION_CONFIG,
) -> CognitiveFrame:
    """Transform one textual experience into a sparse active concept region.

    The lexical matcher is a temporary bootstrap: it can only cue concepts that have
    already been explicitly created, and it matches normalized concept IDs/labels.
    No concept name or domain example is special-cased in production code.
    """

    tokens = _tokens(text)
    matched = sorted(
        concept.concept_id
        for concept in substrate.concepts.values()
        if _concept_matches(tokens, concept.concept_id, concept.label)
    )

    if not matched:
        substrate.activation.replace({})
        return CognitiveFrame(
            experience_event_id=experience_event_id,
            stimulus_text=text,
            status="unmatched",
            matched_concept_ids=[],
            active_concepts={},
        )

    current = {concept_id: config.seed_strength for concept_id in matched}
    contributions: list[ActivationContribution] = [
        ActivationContribution(
            round_index=0,
            kind="seed",
            target_concept_id=concept_id,
            amount=config.seed_strength,
        )
        for concept_id in matched
    ]
    outgoing = _outgoing_relations(substrate)

    for round_index in range(1, config.rounds + 1):
        scores: dict[str, float] = defaultdict(float)

        for concept_id, activation in current.items():
            retained = activation * config.decay
            if retained > 0.0:
                scores[concept_id] += retained
                contributions.append(
                    ActivationContribution(
                        round_index=round_index,
                        kind="retained",
                        source_concept_id=concept_id,
                        target_concept_id=concept_id,
                        amount=retained,
                    )
                )

        for source_id, source_activation in current.items():
            relations = outgoing.get(source_id, ())
            if not relations:
                continue
            normalizer = max(1.0, sum(relation.confidence for relation in relations))
            for relation in relations:
                amount = (
                    source_activation
                    * config.spread_gain
                    * (relation.confidence / normalizer)
                )
                if amount <= 0.0:
                    continue
                scores[relation.target_concept_id] += amount
                contributions.append(
                    ActivationContribution(
                        round_index=round_index,
                        kind="world",
                        source_concept_id=source_id,
                        relation=relation.relation,
                        target_concept_id=relation.target_concept_id,
                        amount=amount,
                        origin=relation.origin,
                    )
                )

        for concept_id in matched:
            scores[concept_id] = max(scores.get(concept_id, 0.0), config.seed_strength)

        _apply_organism_salience(
            substrate,
            scores,
            contributions,
            round_index=round_index,
            gain=config.organism_gain,
        )

        current = _select_sparse_winners(scores, config)
        if not current:
            break

    substrate.activation.replace(current)
    return CognitiveFrame(
        experience_event_id=experience_event_id,
        stimulus_text=text,
        status="activated",
        matched_concept_ids=matched,
        active_concepts=current,
        contributions=contributions,
    )


def _tokens(text: str) -> tuple[str, ...]:
    return tuple(_TOKEN_RE.findall(text.casefold()))


def _concept_matches(
    stimulus_tokens: tuple[str, ...],
    concept_id: str,
    label: str,
) -> bool:
    for cue in {_tokens(concept_id.replace("_", " ")), _tokens(label)}:
        if cue and _contains_phrase(stimulus_tokens, cue):
            return True
    return False


def _contains_phrase(tokens: tuple[str, ...], phrase: tuple[str, ...]) -> bool:
    if len(phrase) > len(tokens):
        return False
    width = len(phrase)
    return any(tokens[index : index + width] == phrase for index in range(len(tokens) - width + 1))


def _outgoing_relations(substrate: CognitiveSubstrate) -> dict[str, tuple[object, ...]]:
    grouped: dict[str, list[object]] = defaultdict(list)
    for relation in substrate.world_relations:
        grouped[relation.source_concept_id].append(relation)
    return {source: tuple(relations) for source, relations in grouped.items()}


def _apply_organism_salience(
    substrate: CognitiveSubstrate,
    scores: dict[str, float],
    contributions: list[ActivationContribution],
    *,
    round_index: int,
    gain: float,
) -> None:
    """Amplify already-reached concepts using arbitrary organism relations.

    Relation names are not interpreted here. Each relation contributes only its stored
    strength × confidence, preserving an open relation space while avoiding global
    activation of unrelated concepts.
    """

    for concept_id, base_score in list(scores.items()):
        container = substrate.self_relations.get(concept_id)
        if container is None or base_score <= 0.0:
            continue

        relations = tuple(container.injected_relations.values()) + tuple(
            container.learned_relations.values()
        )
        weighted = [
            (relation, relation.strength * relation.confidence)
            for relation in relations
            if relation.strength > 0.0 and relation.confidence > 0.0
        ]
        total_weight = sum(weight for _, weight in weighted)
        if total_weight <= 0.0:
            continue

        salience = min(1.0, total_weight)
        total_bonus = base_score * gain * salience
        scores[concept_id] += total_bonus

        for relation, weight in weighted:
            contributions.append(
                ActivationContribution(
                    round_index=round_index,
                    kind="organism",
                    source_concept_id="self",
                    relation=relation.relation_type,
                    target_concept_id=concept_id,
                    amount=total_bonus * (weight / total_weight),
                    origin=relation.origin,
                )
            )


def _select_sparse_winners(
    scores: dict[str, float],
    config: ActivationConfig,
) -> dict[str, float]:
    if not scores:
        return {}

    clipped = {concept_id: min(1.0, max(0.0, score)) for concept_id, score in scores.items()}
    strongest = max(clipped.values(), default=0.0)
    threshold = max(config.activation_floor, strongest * config.inhibition_fraction)
    ranked = sorted(
        (
            (concept_id, value)
            for concept_id, value in clipped.items()
            if value >= threshold
        ),
        key=lambda item: (-item[1], item[0]),
    )[: config.top_k]
    return dict(ranked)
