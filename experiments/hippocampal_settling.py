"""Experimental recurrent sparse-settling assay.

This module tests a hippocampal-inspired computational hypothesis without changing
production cognition. Input only opens a broad candidate field. Recurrent cycles
then combine learned support, pathway resistance, consensus, contradiction pressure,
and progressively tighter sparsity until the field settles or remains ambiguous.

The experiment is intentionally transparent: every cycle is serializable for the UI.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import math
from typing import Iterable


@dataclass(frozen=True, slots=True)
class Candidate:
    name: str
    initial_activation: float
    support: tuple[float, ...]
    resistance: float
    contradiction: float = 0.0


@dataclass(frozen=True, slots=True)
class CycleState:
    cycle: int
    keep_k: int
    activations: dict[str, float]
    consensus: dict[str, int]
    raw_scores: dict[str, float]


@dataclass(frozen=True, slots=True)
class SettlingResult:
    winner: str | None
    settled: bool
    confidence_gap: float
    cycles: tuple[CycleState, ...]
    explanation: str

    def to_dict(self) -> dict[str, object]:
        return {
            "winner": self.winner,
            "settled": self.settled,
            "confidence_gap": self.confidence_gap,
            "cycles": [asdict(cycle) for cycle in self.cycles],
            "explanation": self.explanation,
        }


@dataclass(frozen=True, slots=True)
class TruthProbe:
    proposition: str
    true_support: float
    always_true_support: float
    false_possible_support: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ScenarioResult:
    scenario: str
    stimulus: tuple[str, ...]
    first_pass_winner: str
    settling: SettlingResult
    truth_probe: TruthProbe
    clarification_needed: bool
    clarification_question: str | None
    clarification_answer: str | None
    refined_settling: SettlingResult | None

    def to_dict(self) -> dict[str, object]:
        return {
            "scenario": self.scenario,
            "stimulus": list(self.stimulus),
            "first_pass_winner": self.first_pass_winner,
            "settling": self.settling.to_dict(),
            "truth_probe": self.truth_probe.to_dict(),
            "clarification_needed": self.clarification_needed,
            "clarification_question": self.clarification_question,
            "clarification_answer": self.clarification_answer,
            "refined_settling": self.refined_settling.to_dict() if self.refined_settling else None,
        }


def _normalize(values: dict[str, float]) -> dict[str, float]:
    if not values:
        return {}
    maximum = max(values.values())
    if maximum <= 0.0:
        return {name: 0.0 for name in values}
    return {name: value / maximum for name, value in values.items()}


def _consensus_count(candidate: Candidate, threshold: float = 0.45) -> int:
    return sum(1 for value in candidate.support if value >= threshold)


def settle(
    candidates: Iterable[Candidate],
    *,
    cycles: int = 6,
    alpha: float = 0.25,
    beta: float = 0.55,
    gamma: float = 0.20,
    consensus_weight: float = 0.12,
    contradiction_weight: float = 0.55,
    sparsity_schedule: tuple[int, ...] | None = None,
    settle_gap: float = 0.22,
) -> SettlingResult:
    """Run recurrent sparse settling over a broad candidate field.

    Core update:

        recurrent_i = (sum_j support_ij * anchor_j / resistance_i)
        raw_i = alpha * previous_i + beta * recurrent_i + gamma * initial_i
        raw_i *= 1 + consensus_weight * consensus_i
        raw_i -= contradiction_weight * contradiction_i

    The active field is then normalized and progressively Top-K sparsified.
    """

    items = tuple(candidates)
    if len(items) < 2:
        raise ValueError("At least two candidates are required.")
    if any(item.resistance <= 0.0 for item in items):
        raise ValueError("Candidate resistance must be positive.")

    if sparsity_schedule is None:
        broad = len(items)
        sparsity_schedule = tuple(max(2, broad - step) for step in range(cycles))
    if not sparsity_schedule:
        raise ValueError("Sparsity schedule cannot be empty.")

    activations = _normalize({item.name: item.initial_activation for item in items})
    states: list[CycleState] = []

    # Fixed evidence anchors represent the broad input dimensions. They are not answers.
    anchor_count = max(len(item.support) for item in items)
    anchors = [1.0] * anchor_count

    for cycle_index in range(cycles):
        consensus: dict[str, int] = {}
        raw: dict[str, float] = {}

        for item in items:
            support_sum = sum(
                item.support[index] * anchors[index]
                for index in range(len(item.support))
            )
            recurrent = support_sum / item.resistance
            count = _consensus_count(item)
            score = (
                alpha * activations.get(item.name, 0.0)
                + beta * recurrent
                + gamma * item.initial_activation
            )
            score *= 1.0 + consensus_weight * count
            score -= contradiction_weight * item.contradiction
            consensus[item.name] = count
            raw[item.name] = max(0.0, score)

        normalized = _normalize(raw)
        keep_k = min(len(items), sparsity_schedule[min(cycle_index, len(sparsity_schedule) - 1)])
        ranked = sorted(normalized.items(), key=lambda pair: pair[1], reverse=True)
        survivors = {name for name, _ in ranked[:keep_k]}
        activations = {
            name: (value if name in survivors else 0.0)
            for name, value in normalized.items()
        }
        states.append(
            CycleState(
                cycle=cycle_index + 1,
                keep_k=keep_k,
                activations=dict(activations),
                consensus=consensus,
                raw_scores=raw,
            )
        )

    final_ranked = sorted(activations.items(), key=lambda pair: pair[1], reverse=True)
    winner, best = final_ranked[0]
    second = final_ranked[1][1]
    gap = best - second
    settled = best > 0.0 and gap >= settle_gap
    explanation = (
        f"Settled on {winner}: final normalized activation={best:.3f}, "
        f"runner-up={second:.3f}, gap={gap:.3f}."
        if settled
        else f"Field remains ambiguous: best={best:.3f}, runner-up={second:.3f}, gap={gap:.3f}."
    )
    return SettlingResult(
        winner=winner if settled else None,
        settled=settled,
        confidence_gap=gap,
        cycles=tuple(states),
        explanation=explanation,
    )


def daisy_leash_scenario(*, ambiguous: bool = False) -> ScenarioResult:
    """Run the transparent Logan/Daisy/leash completion scenario.

    The first-pass winner is intentionally Vet. The recurrent field should allow Park
    to win when broad contextual support and lower learned resistance agree.
    """

    stimulus = ("Logan", "Daisy", "leash", "?", "happy")
    if ambiguous:
        candidates = (
            Candidate("Park", 0.58, (0.82, 0.78, 0.88, 0.70), 0.82),
            Candidate("Vet", 0.62, (0.80, 0.83, 0.42, 0.28), 0.88),
            Candidate("Neighborhood", 0.55, (0.68, 0.58, 0.81, 0.72), 0.86),
        )
        gap = 0.28
    else:
        candidates = (
            Candidate("Park", 0.58, (0.90, 0.86, 0.96, 0.88), 0.65),
            Candidate("Vet", 0.62, (0.84, 0.90, 0.35, 0.18), 0.95),
            Candidate("Neighborhood", 0.55, (0.72, 0.55, 0.82, 0.76), 1.05),
        )
        gap = 0.22

    first_pass = max(candidates, key=lambda item: item.initial_activation).name
    first = settle(candidates, settle_gap=gap, sparsity_schedule=(3, 3, 3, 2, 2, 2))

    truth = TruthProbe(
        proposition="Logan + Daisy + leash predicts park",
        true_support=31 / 42,
        always_true_support=0.0,
        false_possible_support=11 / 42,
    )

    needs_clarification = ambiguous or not first.settled
    question = "Did Daisy get into the car?" if needs_clarification else None
    answer = "Yes" if needs_clarification else None
    refined: SettlingResult | None = None

    if needs_clarification:
        refined_candidates = (
            Candidate("Park", 0.52, (0.68, 0.72, 0.54, 0.48, 0.35), 0.88),
            Candidate("Vet", 0.70, (0.86, 0.91, 0.44, 0.30, 0.98), 0.62),
            Candidate("Neighborhood", 0.18, (0.52, 0.46, 0.69, 0.60, 0.08), 1.08),
            Candidate("Other", 0.31, (0.35, 0.40, 0.30, 0.22, 0.42), 1.15),
        )
        refined = settle(
            refined_candidates,
            settle_gap=0.22,
            sparsity_schedule=(4, 4, 3, 3, 2, 2),
        )

    return ScenarioResult(
        scenario="Daisy leash completion",
        stimulus=stimulus,
        first_pass_winner=first_pass,
        settling=first,
        truth_probe=truth,
        clarification_needed=needs_clarification,
        clarification_question=question,
        clarification_answer=answer,
        refined_settling=refined,
    )


def run_demo() -> dict[str, object]:
    clear = daisy_leash_scenario(ambiguous=False)
    ambiguous = daisy_leash_scenario(ambiguous=True)
    return {
        "experiment": "hippocampal-sparse-settling-v1",
        "hypothesis": (
            "A broad input field followed by recurrent consensus, learned resistance, "
            "contradiction pressure, and progressive sparsity can outperform one-pass "
            "maximum activation and can recursively request discriminating evidence."
        ),
        "clear": clear.to_dict(),
        "ambiguous": ambiguous.to_dict(),
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run_demo(), indent=2))
