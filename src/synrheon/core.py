"""Core cognitive substrate and observable organism state.

Stage 1 separates generic world knowledge, open-ended organism-relative relations,
current activation, and observable cognitive transition evidence.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Literal
from uuid import uuid4

from synrheon.experience import ExperienceThread
from synrheon.time import ComputationalTime

RunStatus = Literal["off", "paused", "running"]
StimulusKind = Literal["external", "internal"]
RelationOrigin = Literal["injected", "observed", "inferred", "learned"]
OrganismRelationOrigin = Literal["injected", "learned"]
CognitiveFrameStatus = Literal["activated", "unmatched"]
ActivationContributionKind = Literal["seed", "retained", "world", "organism"]


@dataclass(slots=True)
class StimulusRecord:
    """One external chat stimulus or explicitly injected internal thought."""

    sequence: int
    kind: StimulusKind
    text: str
    created_at: str
    experience_event_id: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(slots=True)
class TraceEvent:
    """One observable runtime event, not hidden reasoning."""

    sequence: int
    event: str
    detail: str
    created_at: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(slots=True)
class Concept:
    """One stable concept identity with optional generic/world vector data."""

    concept_id: str
    label: str
    world_vector: list[float] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(slots=True)
class WorldRelation:
    """A relationship about the world, preserving its provenance."""

    source_concept_id: str
    relation: str
    target_concept_id: str
    origin: RelationOrigin = "injected"
    confidence: float = 1.0
    evidence_event_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(slots=True)
class OrganismRelation:
    """One open-ended relationship between Synrheon and a concept.

    The relation type is data. Production code does not define a closed ontology of
    allowed meanings such as social, trust, preference, or prediction.
    """

    relation_type: str
    strength: float
    confidence: float
    origin: OrganismRelationOrigin
    evidence_event_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(slots=True)
class SelfRelation:
    """Open-ended injected and self-learned relations for one concept."""

    concept_id: str
    injected_relations: dict[str, OrganismRelation] = field(default_factory=dict)
    learned_relations: dict[str, OrganismRelation] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {
            "concept_id": self.concept_id,
            "injected": [
                self.injected_relations[key].to_dict()
                for key in sorted(self.injected_relations)
            ],
            "learned": [
                self.learned_relations[key].to_dict()
                for key in sorted(self.learned_relations)
            ],
        }


@dataclass(slots=True)
class ActivationContribution:
    """Observable evidence for one activation contribution, not hidden reasoning."""

    round_index: int
    kind: ActivationContributionKind
    target_concept_id: str
    amount: float
    source_concept_id: str | None = None
    relation: str | None = None
    origin: str | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(slots=True)
class CognitiveFrame:
    """One inspectable cognitive activation result produced from one experience."""

    experience_event_id: str
    stimulus_text: str
    status: CognitiveFrameStatus
    matched_concept_ids: list[str]
    active_concepts: dict[str, float]
    contributions: list[ActivationContribution] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "experience_event_id": self.experience_event_id,
            "stimulus_text": self.stimulus_text,
            "status": self.status,
            "matched_concept_ids": list(self.matched_concept_ids),
            "active_concepts": dict(self.active_concepts),
            "contributions": [item.to_dict() for item in self.contributions],
        }


@dataclass(slots=True)
class ActivationState:
    """Current concept activation, kept separate from stored knowledge."""

    values: dict[str, float] = field(default_factory=dict)

    def replace(self, values: dict[str, float]) -> None:
        self.values = dict(values)

    def top_k(self, count: int) -> list[tuple[str, float]]:
        if count < 1:
            return []
        return sorted(self.values.items(), key=lambda item: (-item[1], item[0]))[:count]

    def to_dict(self) -> dict[str, float]:
        return dict(self.values)


@dataclass(slots=True)
class CognitiveSubstrate:
    """Stage 1 boundary for world/self knowledge and current activation."""

    concepts: dict[str, Concept] = field(default_factory=dict)
    world_relations: list[WorldRelation] = field(default_factory=list)
    self_relations: dict[str, SelfRelation] = field(default_factory=dict)
    activation: ActivationState = field(default_factory=ActivationState)

    def add_concept(self, concept: Concept) -> None:
        if not concept.concept_id.strip() or not concept.label.strip():
            raise ValueError("Concept ID and label are required.")
        if concept.concept_id in self.concepts:
            raise ValueError(f"Concept already exists: {concept.concept_id}")
        self.concepts[concept.concept_id] = concept

    def add_world_relation(self, relation: WorldRelation) -> None:
        self._require_concept(relation.source_concept_id)
        self._require_concept(relation.target_concept_id)
        if not relation.relation.strip():
            raise ValueError("World relation type is required.")
        _validate_unit_interval(relation.confidence, "Confidence")
        self.world_relations.append(relation)

    def set_injected_self_relation(
        self,
        *,
        concept_id: str,
        relation_type: str,
        strength: float,
        confidence: float,
    ) -> OrganismRelation:
        """Set only injected organism-relative state for an arbitrary relation type."""

        self._require_concept(concept_id)
        relation_type = _require_relation_type(relation_type)
        _validate_unit_interval(strength, "Relation strength")
        _validate_unit_interval(confidence, "Confidence")

        container = self.self_relations.setdefault(concept_id, SelfRelation(concept_id=concept_id))
        relation = OrganismRelation(
            relation_type=relation_type,
            strength=strength,
            confidence=confidence,
            origin="injected",
        )
        container.injected_relations[relation_type] = relation
        return relation

    def learn_self_relation(
        self,
        *,
        concept_id: str,
        relation_type: str,
        observed_strength: float,
        trust: float,
        learning_rate: float,
        evidence_event_id: str,
    ) -> OrganismRelation:
        """Update only a self-learned arbitrary relation from trusted evidence.

        learned_new = learned_old + (learning_rate * trust) *
            (observed_strength - learned_old)

        Injected organism-relative state is never rewritten by this operation.
        """

        self._require_concept(concept_id)
        relation_type = _require_relation_type(relation_type)
        _validate_unit_interval(observed_strength, "Observed relation strength")
        _validate_unit_interval(trust, "Trust")
        _validate_unit_interval(learning_rate, "Learning rate")
        if not evidence_event_id.strip():
            raise ValueError("Evidence event ID is required.")

        container = self.self_relations.setdefault(concept_id, SelfRelation(concept_id=concept_id))
        previous = container.learned_relations.get(relation_type)
        old_strength = previous.strength if previous is not None else 0.0
        old_confidence = previous.confidence if previous is not None else 0.0
        evidence_ids = list(previous.evidence_event_ids) if previous is not None else []

        effective_rate = learning_rate * trust
        new_strength = old_strength + effective_rate * (observed_strength - old_strength)
        new_confidence = old_confidence + effective_rate * (1.0 - old_confidence)
        if evidence_event_id not in evidence_ids:
            evidence_ids.append(evidence_event_id)

        learned = OrganismRelation(
            relation_type=relation_type,
            strength=new_strength,
            confidence=new_confidence,
            origin="learned",
            evidence_event_ids=evidence_ids,
        )
        container.learned_relations[relation_type] = learned
        return learned

    def set_activation(self, concept_id: str, value: float) -> None:
        self._require_concept(concept_id)
        _validate_unit_interval(value, "Activation")
        self.activation.values[concept_id] = value

    def _require_concept(self, concept_id: str) -> None:
        if concept_id not in self.concepts:
            raise KeyError(f"Unknown concept: {concept_id}")

    def snapshot(self) -> dict[str, object]:
        return {
            "concepts": [concept.to_dict() for concept in self.concepts.values()],
            "world_relations": [relation.to_dict() for relation in self.world_relations],
            "self_relations": [relation.to_dict() for relation in self.self_relations.values()],
            "activation": self.activation.to_dict(),
        }


@dataclass(slots=True)
class OrganismState:
    """Live state shared by the verified harness and emerging cognitive owners."""

    session_id: str | None = None
    status: RunStatus = "off"
    cycle: int = 0
    event_sequence: int = 0
    stimuli: list[StimulusRecord] = field(default_factory=list)
    trace: list[TraceEvent] = field(default_factory=list)
    cognitive_frames: list[CognitiveFrame] = field(default_factory=list)
    computational_time: ComputationalTime = field(default_factory=ComputationalTime)
    experience: ExperienceThread = field(default_factory=ExperienceThread)
    substrate: CognitiveSubstrate = field(default_factory=CognitiveSubstrate)

    def begin_session(self) -> None:
        self.session_id = str(uuid4())
        self.status = "paused"
        self.cycle = 0
        self.event_sequence = 0
        self.stimuli.clear()
        self.trace.clear()
        self.cognitive_frames.clear()
        self.computational_time.begin_episode(self.session_id)
        self.experience.begin_episode(self.session_id)
        self.substrate.activation.values.clear()

    def next_event_sequence(self) -> int:
        self.event_sequence += 1
        return self.event_sequence

    def snapshot(self) -> dict[str, object]:
        return {
            "session_id": self.session_id,
            "status": self.status,
            "cycle": self.cycle,
            "event_sequence": self.event_sequence,
            "stimuli": [stimulus.to_dict() for stimulus in self.stimuli],
            "trace": [event.to_dict() for event in self.trace],
            "cognitive_frames": [frame.to_dict() for frame in self.cognitive_frames],
            "time": self.computational_time.snapshot(),
            "experience_thread": self.experience.snapshot(),
            "cognitive_substrate": self.substrate.snapshot(),
        }


def _require_relation_type(relation_type: str) -> str:
    cleaned = relation_type.strip()
    if not cleaned:
        raise ValueError("Organism relation type is required.")
    return cleaned


def _validate_unit_interval(value: float, label: str) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{label} must be between 0 and 1.")
