"""Ground 0 cognition contracts.

This module owns the production-facing cognitive-cycle boundary for Synrheon:

    broad candidate field
        -> learned routing / ordered reversible tapering
        -> serious-candidate field
        -> state-dependent recurrent deliberation
        -> evidence assessment
        -> commit / abstain / seek evidence / reopen

The HCT synthetic generators and hidden scorers do not belong here. Ground 0 is not
live-integrated yet; these checkpoint types define an observable production contract
for the next integration work.

The E011-A policy primitives are re-exported temporarily for compatibility with the
frozen historical experiment. Their implementation now lives in ``synrheon.policy``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

from synrheon.policy import (
    CandidateEvaluation,
    CognitiveAction,
    CognitiveOperation,
    CognitiveState,
    FEATURE_NAMES,
    LinearCognitivePolicy,
    RevealedNode,
)

CognitivePhase = Literal[
    "broad_field",
    "routing",
    "tapering",
    "recurrent_deliberation",
    "evidence_assessment",
    "complete",
]

CognitiveDisposition = Literal[
    "continue",
    "commit",
    "abstain",
    "seek_evidence",
    "reopen",
]


@dataclass(frozen=True, slots=True)
class Ground0Checkpoint:
    """Observable boundary between major Ground 0 cognitive phases.

    The checkpoint records process state only. It does not decide which candidates
    are correct and does not contain hidden experiment truth.
    """

    phase: CognitivePhase
    broad_candidate_count: int
    serious_candidate_count: int
    recurrent_cycle: int = 0
    disposition: CognitiveDisposition = "continue"

    def __post_init__(self) -> None:
        if self.broad_candidate_count < 0:
            raise ValueError("Broad candidate count cannot be negative.")
        if self.serious_candidate_count < 0:
            raise ValueError("Serious candidate count cannot be negative.")
        if self.serious_candidate_count > self.broad_candidate_count:
            raise ValueError("Serious candidate count cannot exceed the broad field.")
        if self.recurrent_cycle < 0:
            raise ValueError("Recurrent cycle cannot be negative.")
        if self.phase != "recurrent_deliberation" and self.recurrent_cycle != 0:
            raise ValueError("Only recurrent-deliberation checkpoints may have a recurrent cycle.")
        if self.phase == "complete" and self.disposition == "continue":
            raise ValueError("A complete checkpoint requires a terminal disposition.")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


__all__ = [
    "CandidateEvaluation",
    "CognitiveAction",
    "CognitiveDisposition",
    "CognitiveOperation",
    "CognitivePhase",
    "CognitiveState",
    "FEATURE_NAMES",
    "Ground0Checkpoint",
    "LinearCognitivePolicy",
    "RevealedNode",
]
