"""Production-facing reversible candidate-field mechanics for Ground 0.

This module intentionally implements only cognitive physics that can be shared by
experiments and the future live organism. It does not decide which context matters,
which candidate is correct, or whether an answer should be committed.

The core invariant is:

    suppressed != deleted

Every transition retains a complete activation vector and can be checkpointed,
restored, or reopened. Experimental truth, qrels, hidden target identity, and
hand-written semantic routing do not belong here.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Iterable, Literal, Mapping

TransitionMode = Literal["carry", "reset", "residual"]


@dataclass(frozen=True, slots=True)
class ContextCheckpoint:
    """One reversible observation of a candidate field after contextual processing."""

    sequence: int
    context_id: str
    transition: TransitionMode
    activation: dict[str, float]
    active: tuple[str, ...]
    dormant: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(slots=True)
class ReversibleCandidateField:
    """Complete candidate state with soft suppression and reversible checkpoints.

    ``retrieval_prior`` is the full broad-field prior from the owner that produced the
    candidate field. ``activation`` may change as context arrives, but the candidate
    key set may not silently shrink. ``active`` controls where expensive downstream
    computation is currently allowed; dormant candidates retain their activation.

    The class deliberately does not implement a taper equation. Experiments and later
    learned cognitive policies supply candidate updates while this owner enforces
    reversibility and transition provenance.
    """

    retrieval_prior: dict[str, float]
    activation: dict[str, float] = field(init=False)
    active: set[str] = field(init=False)
    checkpoints: list[ContextCheckpoint] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.retrieval_prior:
            raise ValueError("A candidate field requires at least one candidate.")
        normalized = _normalize_activation(self.retrieval_prior)
        self.retrieval_prior = normalized
        self.activation = dict(normalized)
        self.active = set(normalized)

    @property
    def candidate_ids(self) -> tuple[str, ...]:
        return tuple(sorted(self.retrieval_prior))

    @property
    def dormant(self) -> set[str]:
        return set(self.retrieval_prior) - self.active

    def prior_for(self, mode: TransitionMode) -> dict[str, float]:
        """Return the state from which a new context stage should begin.

        ``carry`` reuses the current settled activation.
        ``reset`` restores the original broad-field retrieval prior.
        ``residual`` retains the current activation while requiring the caller to
        supply only incremental/context-residual evidence in its update equation.

        Residual evidence is intentionally not computed here because its meaning is a
        scientific/learned policy question rather than a storage invariant.
        """

        _validate_transition(mode)
        if mode == "reset":
            return dict(self.retrieval_prior)
        return dict(self.activation)

    def replace_activation(
        self,
        values: Mapping[str, float],
        *,
        context_id: str,
        transition: TransitionMode,
        active_ids: Iterable[str] | None = None,
        checkpoint: bool = True,
    ) -> ContextCheckpoint | None:
        """Install a complete soft state without allowing silent hard deletion."""

        _validate_transition(transition)
        context_id = context_id.strip()
        if not context_id:
            raise ValueError("Context ID is required.")
        expected = set(self.retrieval_prior)
        supplied = set(values)
        if supplied != expected:
            missing = sorted(expected - supplied)
            extra = sorted(supplied - expected)
            raise ValueError(
                "Candidate activation must preserve the complete broad field; "
                f"missing={missing}, extra={extra}."
            )

        self.activation = _normalize_activation(values)
        if active_ids is not None:
            self.set_active(active_ids)
        if checkpoint:
            return self.record_checkpoint(context_id=context_id, transition=transition)
        return None

    def set_active(self, candidate_ids: Iterable[str]) -> None:
        """Choose the expensive-compute region without deleting dormant candidates."""

        selected = set(candidate_ids)
        unknown = selected - set(self.retrieval_prior)
        if unknown:
            raise KeyError(f"Unknown candidates cannot be activated: {sorted(unknown)}")
        if not selected:
            raise ValueError("At least one candidate must remain active.")
        self.active = selected

    def reactivate(self, candidate_ids: Iterable[str]) -> None:
        """Reopen dormant candidates while retaining their previously stored support."""

        requested = set(candidate_ids)
        unknown = requested - set(self.retrieval_prior)
        if unknown:
            raise KeyError(f"Unknown candidates cannot be reactivated: {sorted(unknown)}")
        self.active.update(requested)

    def reopen_all(self) -> None:
        self.active = set(self.retrieval_prior)

    def reset_to_retrieval_prior(self) -> None:
        """Restore broad activation and eligibility without changing candidate identity."""

        self.activation = dict(self.retrieval_prior)
        self.active = set(self.retrieval_prior)

    def record_checkpoint(
        self,
        *,
        context_id: str,
        transition: TransitionMode,
    ) -> ContextCheckpoint:
        _validate_transition(transition)
        cleaned = context_id.strip()
        if not cleaned:
            raise ValueError("Context ID is required.")
        checkpoint = ContextCheckpoint(
            sequence=len(self.checkpoints) + 1,
            context_id=cleaned,
            transition=transition,
            activation=dict(self.activation),
            active=tuple(sorted(self.active)),
            dormant=tuple(sorted(self.dormant)),
        )
        self.checkpoints.append(checkpoint)
        return checkpoint

    def restore(self, sequence: int) -> ContextCheckpoint:
        """Restore one previously checkpointed complete state."""

        for checkpoint in self.checkpoints:
            if checkpoint.sequence == sequence:
                self.activation = dict(checkpoint.activation)
                self.active = set(checkpoint.active)
                return checkpoint
        raise KeyError(f"Unknown checkpoint sequence: {sequence}")

    def ranked(self, *, include_dormant: bool = True) -> list[tuple[str, float]]:
        allowed = set(self.retrieval_prior) if include_dormant else self.active
        return sorted(
            ((candidate_id, self.activation[candidate_id]) for candidate_id in allowed),
            key=lambda item: (-item[1], item[0]),
        )

    def snapshot(self) -> dict[str, object]:
        return {
            "candidate_count": len(self.retrieval_prior),
            "active_count": len(self.active),
            "dormant_count": len(self.dormant),
            "retrieval_prior": dict(self.retrieval_prior),
            "activation": dict(self.activation),
            "active": sorted(self.active),
            "dormant": sorted(self.dormant),
            "checkpoints": [checkpoint.to_dict() for checkpoint in self.checkpoints],
        }


def _normalize_activation(values: Mapping[str, float]) -> dict[str, float]:
    cleaned: dict[str, float] = {}
    for candidate_id, value in values.items():
        candidate = str(candidate_id).strip()
        if not candidate:
            raise ValueError("Candidate ID cannot be empty.")
        numeric = float(value)
        if numeric < 0.0:
            raise ValueError("Candidate activation cannot be negative.")
        cleaned[candidate] = numeric
    total = sum(cleaned.values())
    if total <= 0.0:
        uniform = 1.0 / len(cleaned)
        return {candidate_id: uniform for candidate_id in cleaned}
    return {candidate_id: value / total for candidate_id, value in cleaned.items()}


def _validate_transition(mode: str) -> None:
    if mode not in {"carry", "reset", "residual"}:
        raise ValueError(f"Unknown context transition mode: {mode}")


__all__ = ["ContextCheckpoint", "ReversibleCandidateField", "TransitionMode"]
