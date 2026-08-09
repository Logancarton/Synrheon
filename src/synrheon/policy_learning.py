"""Outcome-driven updates for the retained E011-A cognitive policy."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Sequence

from synrheon.policy import CandidateEvaluation, LinearCognitivePolicy


@dataclass(frozen=True, slots=True)
class PolicyDecisionTrace:
    """Learning-relevant evidence for one policy decision."""

    candidates: tuple[CandidateEvaluation, ...]
    selected_index: int


class ReinforceLearner:
    """Small REINFORCE updater that only consumes outcomes, not hidden world truth."""

    def __init__(
        self,
        policy: LinearCognitivePolicy,
        *,
        learning_rate: float = 0.035,
        gamma: float = 0.97,
        baseline_rate: float = 0.04,
        gradient_clip: float = 2.0,
    ) -> None:
        if learning_rate <= 0:
            raise ValueError("Learning rate must be positive.")
        if not 0 < gamma <= 1:
            raise ValueError("Gamma must be in (0, 1].")
        if not 0 < baseline_rate <= 1:
            raise ValueError("Baseline rate must be in (0, 1].")
        if gradient_clip <= 0:
            raise ValueError("Gradient clip must be positive.")
        self.policy = policy
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.baseline_rate = baseline_rate
        self.gradient_clip = gradient_clip
        self.running_baseline = 0.0
        self.episodes_seen = 0

    def update_episode(
        self,
        decisions: Sequence[PolicyDecisionTrace],
        rewards: Sequence[float],
    ) -> None:
        if len(decisions) != len(rewards):
            raise ValueError("Decision and reward counts must match.")
        if not decisions:
            return

        returns = [0.0 for _ in rewards]
        running = 0.0
        for index in range(len(rewards) - 1, -1, -1):
            running = float(rewards[index]) + self.gamma * running
            returns[index] = running

        episode_mean = sum(returns) / len(returns)
        baseline_before = self.running_baseline
        if self.episodes_seen == 0:
            self.running_baseline = episode_mean
        else:
            self.running_baseline += self.baseline_rate * (episode_mean - self.running_baseline)
        self.episodes_seen += 1

        for decision, discounted_return in zip(decisions, returns):
            advantage = discounted_return - baseline_before
            chosen = decision.candidates[decision.selected_index]
            expected = [0.0 for _ in self.policy.weights]
            for candidate in decision.candidates:
                for feature_index, value in enumerate(candidate.features):
                    expected[feature_index] += candidate.probability * value

            for feature_index, selected_value in enumerate(chosen.features):
                gradient = advantage * (selected_value - expected[feature_index])
                gradient = max(-self.gradient_clip, min(self.gradient_clip, gradient))
                self.policy.weights[feature_index] += self.learning_rate * gradient


def load_recorded_learning_metrics(path: Path) -> dict[str, object]:
    """Load recorded experiment evidence without importing a hidden experiment harness."""

    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(payload, dict):
        return {}
    metrics = payload.get("learning_metrics")
    if not isinstance(metrics, dict):
        return {}
    return dict(metrics)
