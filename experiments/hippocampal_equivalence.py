"""Falsification assay for learned-resistance recurrent sparse settling.

This experiment asks whether the current recurrent operator contributes anything beyond
one exact first-cycle weighted pass using the same learned resistances and the same
visible information.

A positive result for recurrence is NOT assumed. If the one-pass rule and recurrent
settling agree almost perfectly, the correct conclusion is that recurrence has not yet
been shown necessary in this world family.
"""

from __future__ import annotations

from dataclasses import dataclass
import argparse
import json
from statistics import mean

from experiments.hippocampal_learning import (
    CHANNEL_COUNT,
    FINAL_SEEDS,
    TRAIN_SEEDS,
    LearningEpisode,
    candidates_from_episode,
    generate_episode,
    train_resistance,
)
from experiments.hippocampal_settling import Candidate, settle

EXPERIMENT_ID = "hippocampal-one-pass-equivalence-v1"


@dataclass(frozen=True, slots=True)
class Decision:
    winner: str
    confidence_gap: float


@dataclass(frozen=True, slots=True)
class ComparisonSummary:
    episodes: int
    one_pass_accuracy: float
    recurrent_progressive_accuracy: float
    recurrent_fixed_k_accuracy: float
    one_pass_recurrent_agreement: float
    recurrent_advantage: float
    progressive_advantage_over_fixed: float
    mean_one_pass_gap: float
    mean_recurrent_gap: float

    def to_dict(self) -> dict[str, object]:
        return {
            "episodes": self.episodes,
            "one_pass_accuracy": self.one_pass_accuracy,
            "recurrent_progressive_accuracy": self.recurrent_progressive_accuracy,
            "recurrent_fixed_k_accuracy": self.recurrent_fixed_k_accuracy,
            "one_pass_recurrent_agreement": self.one_pass_recurrent_agreement,
            "recurrent_advantage": self.recurrent_advantage,
            "progressive_advantage_over_fixed": self.progressive_advantage_over_fixed,
            "mean_one_pass_gap": self.mean_one_pass_gap,
            "mean_recurrent_gap": self.mean_recurrent_gap,
        }


def _normalize(values: dict[str, float]) -> dict[str, float]:
    maximum = max(values.values())
    if maximum <= 0.0:
        return {name: 0.0 for name in values}
    return {name: value / maximum for name, value in values.items()}


def _consensus_count(candidate: Candidate, threshold: float = 0.45) -> int:
    return sum(1 for value in candidate.support if value >= threshold)


def exact_one_pass(
    candidates: tuple[Candidate, ...],
    *,
    alpha: float = 0.25,
    beta: float = 0.55,
    gamma: float = 0.20,
    consensus_weight: float = 0.12,
    contradiction_weight: float = 0.55,
) -> Decision:
    """Replicate cycle 1 of ``settle`` exactly, but stop before recurrence.

    This is the strongest simple control because it receives the same candidate field,
    learned conductance-weighted supports, initial activation, consensus rule, and
    contradiction penalty. The only thing removed is repeated state evolution and the
    multi-cycle sparsity schedule.
    """

    initial = _normalize({item.name: item.initial_activation for item in candidates})
    raw: dict[str, float] = {}
    for item in candidates:
        recurrent_support = sum(item.support) / item.resistance
        score = (
            alpha * initial[item.name]
            + beta * recurrent_support
            + gamma * item.initial_activation
        )
        score *= 1.0 + consensus_weight * _consensus_count(item)
        score -= contradiction_weight * item.contradiction
        raw[item.name] = max(0.0, score)

    normalized = _normalize(raw)
    ranked = sorted(normalized.items(), key=lambda pair: pair[1], reverse=True)
    winner, best = ranked[0]
    second = ranked[1][1]
    return Decision(winner=winner, confidence_gap=best - second)


def compare_episode(
    episode: LearningEpisode,
    resistances: tuple[float, ...],
) -> tuple[Decision, Decision, Decision]:
    candidates = candidates_from_episode(episode, resistances)
    one_pass = exact_one_pass(candidates)

    progressive_result = settle(
        candidates,
        cycles=6,
        sparsity_schedule=(3, 3, 3, 2, 2, 2),
        settle_gap=0.0,
    )
    fixed_result = settle(
        candidates,
        cycles=6,
        sparsity_schedule=(3, 3, 3, 3, 3, 3),
        settle_gap=0.0,
    )

    progressive = Decision(
        winner=progressive_result.winner or max(
            progressive_result.cycles[-1].activations,
            key=progressive_result.cycles[-1].activations.get,
        ),
        confidence_gap=progressive_result.confidence_gap,
    )
    fixed = Decision(
        winner=fixed_result.winner or max(
            fixed_result.cycles[-1].activations,
            key=fixed_result.cycles[-1].activations.get,
        ),
        confidence_gap=fixed_result.confidence_gap,
    )
    return one_pass, progressive, fixed


def evaluate_equivalence(
    seeds: range,
    resistances: tuple[float, ...],
    *,
    rename_offset: int | None = None,
) -> ComparisonSummary:
    records: list[tuple[bool, bool, bool, bool, float, float]] = []
    for seed in seeds:
        episode = generate_episode(
            seed,
            rename_seed=(seed + rename_offset) if rename_offset is not None else None,
        )
        one_pass, progressive, fixed = compare_episode(episode, resistances)
        records.append(
            (
                one_pass.winner == episode.correct_name,
                progressive.winner == episode.correct_name,
                fixed.winner == episode.correct_name,
                one_pass.winner == progressive.winner,
                one_pass.confidence_gap,
                progressive.confidence_gap,
            )
        )

    one_accuracy = mean(1.0 if row[0] else 0.0 for row in records)
    recurrent_accuracy = mean(1.0 if row[1] else 0.0 for row in records)
    fixed_accuracy = mean(1.0 if row[2] else 0.0 for row in records)
    return ComparisonSummary(
        episodes=len(records),
        one_pass_accuracy=one_accuracy,
        recurrent_progressive_accuracy=recurrent_accuracy,
        recurrent_fixed_k_accuracy=fixed_accuracy,
        one_pass_recurrent_agreement=mean(1.0 if row[3] else 0.0 for row in records),
        recurrent_advantage=recurrent_accuracy - one_accuracy,
        progressive_advantage_over_fixed=recurrent_accuracy - fixed_accuracy,
        mean_one_pass_gap=mean(row[4] for row in records),
        mean_recurrent_gap=mean(row[5] for row in records),
    )


def interpret(summary: ComparisonSummary) -> str:
    """Return a conservative verdict without assuming the desired outcome."""

    if summary.one_pass_recurrent_agreement >= 0.98 and abs(summary.recurrent_advantage) < 0.01:
        return (
            "CURRENT RECURRENCE NOT YET NECESSARY: the exact one-pass control and the "
            "six-cycle recurrent operator make essentially the same decisions in this "
            "world family. Learned resistance is useful, but recurrence has not yet "
            "shown independent computational value."
        )
    if summary.recurrent_advantage >= 0.03:
        return (
            "EVIDENCE FOR RECURRENT VALUE: repeated settling improves held-out accuracy "
            "by at least three percentage points over the exact one-pass control using "
            "the same learned resistance and visible evidence."
        )
    return (
        "MIXED RESULT: one-pass and recurrent inference differ, but the present effect "
        "is too small or inconsistent to establish recurrence as a necessary component."
    )


def run_assay(*, quick: bool = False) -> dict[str, object]:
    train_seeds = range(1000, 1120) if quick else TRAIN_SEEDS
    final_seeds = range(10000, 10200) if quick else FINAL_SEEDS

    learner = train_resistance(train_seeds)
    frozen = learner.frozen()
    comparison = evaluate_equivalence(final_seeds, frozen)
    renamed = evaluate_equivalence(final_seeds, frozen, rename_offset=900_000)

    return {
        "experiment": EXPERIMENT_ID,
        "question": (
            "Does six-cycle recurrent progressive sparse settling outperform an exact "
            "one-pass control when both use the same learned resistances and evidence?"
        ),
        "learned_channel_resistance": list(frozen),
        "held_out": comparison.to_dict(),
        "renamed_candidates": renamed.to_dict(),
        "verdict": interpret(comparison),
        "scientific_boundary": (
            "This assay isolates recurrence within the current synthetic world family. "
            "It does not test dynamic evidence arrival, state-dependent support, learned "
            "candidate-to-candidate recurrence, or cross-family structural transfer."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run_assay(quick=args.quick), indent=2))


if __name__ == "__main__":
    main()
