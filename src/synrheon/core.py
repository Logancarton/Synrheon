"""Core cognitive substrate and observable organism state.

Stage 1 separates generic world knowledge, organism-relative knowledge, and
current activation so later sparse activation can weight them differently.
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

SELF_RELATION_DIMENSIONS = (
    "ownership",
    "experience",
    "social",
    "goal",
    "history",
    "knowledge",
    "trust",
    "prediction",
    "consequence",
    "preference",
    "uncertainty",
)


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
class SelfRelationVector:
    """Organism-relative dimensions used later to gate sparse activation."""

    ownership: float = 0.0
    experience: float = 0.0
    social: float = 0.0
    goal: float = 0.0
    history: float = 0.0
    knowledge: float = 0.0
    trust: float = 0.0
    prediction: float = 0.0
    consequence: float = 0.0
    preference: float = 0.0
    uncertainty: float = 0.0

    def to_list(self) -> list[float]:
        return [getattr(self, name) for name in SELF_RELATION_DIMENSIONS]

    def to_dict(self) -> dict[str, float]:
        return asdict(self)

    def with_dimension(self, dimension: str, value: float) -> SelfRelationVector:
        if dimension not in SELF_RELATION_DIMENSIONS:
            raise ValueError(f"Unknown self-relation dimension: {dimension}")
        _validate_unit_interval(value, "Self-relation value")
        values = self.to_dict()
        values[dimension] = value
        return SelfRelationVector(**values)


@dataclass(slots=True)
class SelfRelation:
    """How one concept relates to Synrheon, separate from generic world truth."""

    concept_id: str
    vector: SelfRelationVector = field(default_factory=SelfRelationVector)
    origin: RelationOrigin = "injected"
    confidence: float = 0.0
    evidence_event_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "concept_id": self.concept_id,
            "vector": self.vector.to_dict(),
            "origin": self.origin,
            "confidence": self.confidence,
            "evidence_event_ids": list(self.evidence_event_ids),
        }


@dataclass(slots=True)
class ActivationState:
    """Current concept activation, kept separate from stored knowledge."""

    values: dict[str, float] = field(default_factory=dict)

    def top_k(self, count: int) -> list[tuple[str, float]]:
        if count < 1:
            return []
        return sorted(self.values.items(), key=lambda item: (-item[1], item[0]))[:count]

    def to_dict(self) -> dict[str, float]:
        return dict(self.values)


@dataclass(slots=True)
class CognitiveSubstrate:
    """Stage 1 representation boundary for world/self knowledge and activation."""

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
        dimension: str,
        value: float,
        confidence: float,
    ) -> SelfRelation:
        """Inject organism-relative scaffolding without calling it learned."""

        self._require_concept(concept_id)
        _validate_unit_interval(confidence, "Confidence")
        current = self.self_relations.get(concept_id, SelfRelation(concept_id=concept_id))
        relation = SelfRelation(
            concept_id=concept_id,
            vector=current.vector.with_dimension(dimension, value),
            origin="injected",
            confidence=confidence,
            evidence_event_ids=list(current.evidence_event_ids),
        )
        self.self_relations[concept_id] = relation
        return relation

    def learn_self_relation(
        self,
        *,
        concept_id: str,
        observation: SelfRelationVector,
        trust: float,
        learning_rate: float,
        evidence_event_id: str,
    ) -> SelfRelation:
        """Update a distinct self vector using confidence-weighted online learning.

        s_new = s_old + (learning_rate * trust) * (observation - s_old)

        The explicit vector and evidence lineage remain outside neural weights.
        """

        self._require_concept(concept_id)
        _validate_unit_interval(trust, "Trust")
        _validate_unit_interval(learning_rate, "Learning rate")
        if not evidence_event_id.strip():
            raise ValueError("Evidence event ID is required.")

        current = self.self_relations.get(concept_id, SelfRelation(concept_id=concept_id))
        effective_rate = learning_rate * trust
        old_values = current.vector.to_dict()
        observed_values = observation.to_dict()
        updated_values = {
            name: old_values[name] + effective_rate * (observed_values[name] - old_values[name])
            for name in SELF_RELATION_DIMENSIONS
        }
        confidence = current.confidence + effective_rate * (1.0 - current.confidence)
        evidence_ids = list(current.evidence_event_ids)
        if evidence_event_id not in evidence_ids:
            evidence_ids.append(evidence_event_id)

        learned = SelfRelation(
            concept_id=concept_id,
            vector=SelfRelationVector(**updated_values),
            origin="learned",
            confidence=confidence,
            evidence_event_ids=evidence_ids,
        )
        self.self_relations[concept_id] = learned
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
            "time": self.computational_time.snapshot(),
            "experience_thread": self.experience.snapshot(),
            "cognitive_substrate": self.substrate.snapshot(),
        }


def _validate_unit_interval(value: float, label: str) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{label} must be between 0 and 1.")
