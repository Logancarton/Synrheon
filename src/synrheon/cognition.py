"""Trainable cognitive-policy primitives for the first E011 assay.

The policy only consumes explicit, already-revealed cognitive state. It does not
know the experiment's hidden graph, goal location, solver path, seed, or correct
next action. Python may enumerate valid operation/target candidates; the learned
policy chooses among them.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
import random
from typing import Literal, Sequence

CognitiveOperation = Literal["EXPAND", "STOP"]


@dataclass(frozen=True, slots=True)
class RevealedNode:
    """Policy-visible facts about one currently revealed candidate region."""

    handle: str
    depth: int
    expanded: bool
    reveal_order: int
    frontier: bool
    is_goal: bool = False


@dataclass(frozen=True, slots=True)
class CognitiveAction:
    """One bounded operation plus the target chosen by the policy."""

    operation: CognitiveOperation
    target: str | None = None

    def __post_init__(self) -> None:
        if self.operation == "EXPAND" and not self.target:
            raise ValueError("EXPAND requires a target.")
        if self.operation == "STOP" and self.target is not None:
            raise ValueError("STOP does not accept a target.")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class CognitiveState:
    """The explicit policy-visible state for one bounded cognitive checkpoint."""

    checkpoint_index: int
    remaining_budget: int
    hard_budget: int
    nodes: tuple[RevealedNode, ...]
    revealed_edges: tuple[tuple[str, str], ...]
    previous_action: CognitiveAction | None = None

    def __post_init__(self) -> None:
        if self.checkpoint_index < 0:
            raise ValueError("Checkpoint index cannot be negative.")
        if self.hard_budget <= 0:
            raise ValueError("Hard budget must be positive.")
        if not 0 <= self.remaining_budget <= self.hard_budget:
            raise ValueError("Remaining budget must be within the hard budget.")
        handles = [node.handle for node in self.nodes]
        if len(handles) != len(set(handles)):
            raise ValueError("Revealed node handles must be unique.")
        known = set(handles)
        for source, target in self.revealed_edges:
            if source not in known or target not in known:
                raise ValueError("Revealed edges may reference revealed nodes only.")

    @property
    def goal_revealed(self) -> bool:
        return any(node.is_goal for node in self.nodes)

    def node(self, handle: str) -> RevealedNode:
        for item in self.nodes:
            if item.handle == handle:
                return item
        raise KeyError(f"Unknown revealed node: {handle}")

    def to_dict(self) -> dict[str, object]:
        return {
            "checkpoint_index": self.checkpoint_index,
            "remaining_budget": self.remaining_budget,
            "hard_budget": self.hard_budget,
            "nodes": [asdict(node) for node in self.nodes],
            "revealed_edges": [list(edge) for edge in self.revealed_edges],
            "previous_action": self.previous_action.to_dict() if self.previous_action else None,
        }


FEATURE_NAMES: tuple[str, ...] = (
    "bias",
    "is_stop",
    "goal_revealed_for_stop",
    "target_depth",
    "target_recency",
    "frontier_fraction",
    "remaining_budget_fraction",
    "checkpoint_fraction",
    "previous_was_expand",
)


@dataclass(frozen=True, slots=True)
class CandidateEvaluation:
    """One candidate paired with policy-visible features and probability."""

    action: CognitiveAction
    features: tuple[float, ...]
    score: float
    probability: float


class LinearCognitivePolicy:
    """Small trainable softmax policy over operation + target candidates.

    Node identities are deliberately excluded from the feature vector. The first
    assay can therefore learn preferences over visible cognitive structure without
    acquiring a stable embedding for a world-specific opaque handle.
    """

    architecture_id = "e011a-linear-softmax-v1"

    def __init__(self, *, seed: int, weights: Sequence[float] | None = None) -> None:
        if weights is None:
            rng = random.Random(seed)
            self.weights = [rng.uniform(-0.02, 0.02) for _ in FEATURE_NAMES]
        else:
            if len(weights) != len(FEATURE_NAMES):
                raise ValueError("Unexpected policy weight count.")
            self.weights = [float(value) for value in weights]
        self.initialization_seed = seed

    def valid_actions(self, state: CognitiveState) -> tuple[CognitiveAction, ...]:
        """Enumerate valid actions without ranking or selecting a target."""

        expand = [
            CognitiveAction("EXPAND", node.handle)
            for node in sorted(state.nodes, key=lambda item: item.reveal_order)
            if node.frontier and not node.expanded
        ]
        return tuple([*expand, CognitiveAction("STOP")])

    def feature_vector(self, state: CognitiveState, action: CognitiveAction) -> tuple[float, ...]:
        frontier = [node for node in state.nodes if node.frontier and not node.expanded]
        newest_order = max((node.reveal_order for node in state.nodes), default=0)
        target_depth = 0.0
        target_recency = 0.0
        if action.operation == "EXPAND":
            target = state.node(action.target or "")
            if target.expanded or not target.frontier:
                raise ValueError("EXPAND target must be an unexpanded frontier node.")
            target_depth = min(target.depth, state.hard_budget) / state.hard_budget
            if newest_order > 0:
                target_recency = target.reveal_order / newest_order
            else:
                target_recency = 1.0

        return (
            1.0,
            1.0 if action.operation == "STOP" else 0.0,
            1.0 if action.operation == "STOP" and state.goal_revealed else 0.0,
            target_depth,
            target_recency,
            len(frontier) / max(1, len(state.nodes)),
            state.remaining_budget / state.hard_budget,
            state.checkpoint_index / state.hard_budget,
            1.0 if state.previous_action and state.previous_action.operation == "EXPAND" else 0.0,
        )

    def evaluate(
        self,
        state: CognitiveState,
        actions: Sequence[CognitiveAction] | None = None,
        *,
        temperature: float = 1.0,
    ) -> tuple[CandidateEvaluation, ...]:
        candidates = tuple(actions or self.valid_actions(state))
        if not candidates:
            raise ValueError("At least one cognitive action is required.")
        if temperature <= 0:
            raise ValueError("Temperature must be positive.")

        features = [self.feature_vector(state, action) for action in candidates]
        scores = [sum(weight * value for weight, value in zip(self.weights, row)) for row in features]
        scaled = [score / temperature for score in scores]
        maximum = max(scaled)
        exponentials = [math.exp(value - maximum) for value in scaled]
        denominator = sum(exponentials)
        probabilities = [value / denominator for value in exponentials]
        return tuple(
            CandidateEvaluation(action, row, score, probability)
            for action, row, score, probability in zip(candidates, features, scores, probabilities)
        )

    def choose(
        self,
        state: CognitiveState,
        *,
        rng: random.Random,
        greedy: bool = False,
        temperature: float = 1.0,
    ) -> tuple[CognitiveAction, tuple[CandidateEvaluation, ...], int]:
        evaluations = self.evaluate(state, temperature=temperature)
        if greedy:
            selected_index = max(
                range(len(evaluations)),
                key=lambda index: (evaluations[index].score, -index),
            )
        else:
            needle = rng.random()
            cumulative = 0.0
            selected_index = len(evaluations) - 1
            for index, item in enumerate(evaluations):
                cumulative += item.probability
                if needle <= cumulative:
                    selected_index = index
                    break
        return evaluations[selected_index].action, evaluations, selected_index

    def parameter_checksum(self) -> str:
        payload = json.dumps(self.weights, separators=(",", ":"), sort_keys=False).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    def to_dict(self) -> dict[str, object]:
        return {
            "architecture_id": self.architecture_id,
            "initialization_seed": self.initialization_seed,
            "feature_names": list(FEATURE_NAMES),
            "weights": list(self.weights),
            "parameter_checksum": self.parameter_checksum(),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "LinearCognitivePolicy":
        architecture_id = payload.get("architecture_id")
        if architecture_id != cls.architecture_id:
            raise ValueError(f"Unsupported policy architecture: {architecture_id}")
        raw_seed = payload.get("initialization_seed")
        raw_weights = payload.get("weights")
        if not isinstance(raw_seed, int) or not isinstance(raw_weights, list):
            raise ValueError("Malformed policy payload.")
        return cls(seed=raw_seed, weights=[float(value) for value in raw_weights])
