"""E012-style learned-resistance assay for hippocampal sparse settling.

This remains non-production experiment code. The experiment asks a stricter question
than ``hippocampal_settling``: can pathway resistance be learned from outcomes, frozen,
and then improve recurrent settling on unseen candidate identities?

The learner never memorizes candidate names. It learns resistance for anonymous
evidence channels. Low resistance means evidence on that channel flows more easily
through the recurrent settling operator; high resistance suppresses historically
misleading evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
import argparse
import json
import random
from statistics import mean

from experiments.hippocampal_settling import Candidate, SettlingResult, settle

EXPERIMENT_ID = "hippocampal-learned-resistance-v1"
CHANNEL_COUNT = 4
TRAIN_SEEDS = range(1000, 1400)
FINAL_SEEDS = range(10000, 11000)


@dataclass(frozen=True, slots=True)
class LearningEpisode:
    """One anonymous candidate field plus an outcome revealed after the decision."""

    seed: int
    names: tuple[str, ...]
    initial_activations: tuple[float, ...]
    supports: tuple[tuple[float, ...], ...]
    correct_index: int

    @property
    def correct_name(self) -> str:
        return self.names[self.correct_index]


@dataclass(frozen=True, slots=True)
class AssaySummary:
    episodes: int
    accuracy: float
    mean_confidence_gap: float
    settled_rate: float

    def to_dict(self) -> dict[str, object]:
        return {
            "episodes": self.episodes,
            "accuracy": self.accuracy,
            "mean_confidence_gap": self.mean_confidence_gap,
            "settled_rate": self.settled_rate,
        }


class ChannelResistanceLearner:
    """Learn evidence-channel resistance from successful versus failed alternatives.

    For each channel j after an outcome is known:

        delta_R_j = learning_rate * (strongest_wrong_support_j - correct_support_j)
        R_j <- clamp(R_j + delta_R_j)

    Therefore a channel repeatedly stronger in wrong candidates acquires resistance,
    while a channel repeatedly stronger in the successful candidate becomes easier to
    traverse. The candidate identities are never parameters.
    """

    def __init__(
        self,
        *,
        channel_count: int = CHANNEL_COUNT,
        learning_rate: float = 0.03,
        minimum_resistance: float = 0.25,
        maximum_resistance: float = 3.0,
    ) -> None:
        if channel_count < 1:
            raise ValueError("channel_count must be positive")
        self.resistances = [1.0] * channel_count
        self.learning_rate = learning_rate
        self.minimum_resistance = minimum_resistance
        self.maximum_resistance = maximum_resistance
        self.updates = 0

    def observe_outcome(self, episode: LearningEpisode) -> None:
        correct = episode.supports[episode.correct_index]
        wrong = [
            support
            for index, support in enumerate(episode.supports)
            if index != episode.correct_index
        ]
        for channel in range(len(self.resistances)):
            strongest_wrong = max(support[channel] for support in wrong)
            delta = self.learning_rate * (strongest_wrong - correct[channel])
            self.resistances[channel] = min(
                self.maximum_resistance,
                max(self.minimum_resistance, self.resistances[channel] + delta),
            )
        self.updates += 1

    def frozen(self) -> tuple[float, ...]:
        return tuple(self.resistances)


def generate_episode(seed: int, *, rename_seed: int | None = None) -> LearningEpisode:
    """Generate a deterministic anonymous field with one misleading evidence channel.

    Channel 0 is deliberately seductive: wrong candidates tend to score highly on it.
    Channels 1-3 are weaker individually but jointly reliable. The correct candidate is
    not the strongest first-pass activation, so immediate maximum activation is a poor
    strategy.
    """

    rng = random.Random(seed)
    count = 3
    correct = rng.randrange(count)
    misleading_wrong = (correct + 1) % count
    name_rng = random.Random(seed + 500_003 if rename_seed is None else rename_seed)
    opaque = [f"c{index:02d}" for index in range(count)]
    name_rng.shuffle(opaque)
    names = tuple(f"{token}_{name_rng.randrange(1000, 9999)}" for token in opaque)

    supports: list[tuple[float, ...]] = []
    initial: list[float] = []
    for index in range(count):
        if index == correct:
            support = (
                rng.uniform(0.25, 0.45),
                rng.uniform(0.58, 0.78),
                rng.uniform(0.58, 0.78),
                rng.uniform(0.58, 0.78),
            )
            activation = rng.uniform(0.42, 0.56)
        elif index == misleading_wrong:
            support = (
                rng.uniform(0.92, 1.00),
                rng.uniform(0.40, 0.58),
                rng.uniform(0.38, 0.56),
                rng.uniform(0.40, 0.58),
            )
            activation = rng.uniform(0.70, 0.88)
        else:
            support = (
                rng.uniform(0.68, 0.90),
                rng.uniform(0.25, 0.48),
                rng.uniform(0.25, 0.48),
                rng.uniform(0.25, 0.48),
            )
            activation = rng.uniform(0.55, 0.72)
        supports.append(support)
        initial.append(activation)

    return LearningEpisode(
        seed=seed,
        names=names,
        initial_activations=tuple(initial),
        supports=tuple(supports),
        correct_index=correct,
    )


def _conductance_weights(resistances: tuple[float, ...]) -> tuple[float, ...]:
    if any(value <= 0.0 for value in resistances):
        raise ValueError("resistances must be positive")
    conductances = [1.0 / value for value in resistances]
    average = mean(conductances)
    return tuple(value / average for value in conductances)


def candidates_from_episode(
    episode: LearningEpisode,
    resistances: tuple[float, ...],
) -> tuple[Candidate, ...]:
    """Apply frozen learned resistance without exposing the episode outcome."""

    weights = _conductance_weights(resistances)
    return tuple(
        Candidate(
            name=episode.names[index],
            initial_activation=episode.initial_activations[index],
            support=tuple(value * weight for value, weight in zip(support, weights)),
            resistance=1.0,
        )
        for index, support in enumerate(episode.supports)
    )


def infer(episode: LearningEpisode, resistances: tuple[float, ...]) -> SettlingResult:
    return settle(
        candidates_from_episode(episode, resistances),
        cycles=6,
        sparsity_schedule=(3, 3, 3, 2, 2, 2),
        settle_gap=0.10,
    )


def train_resistance(
    seeds: range = TRAIN_SEEDS,
) -> ChannelResistanceLearner:
    learner = ChannelResistanceLearner()
    for seed in seeds:
        learner.observe_outcome(generate_episode(seed))
    return learner


def evaluate(
    seeds: range,
    resistances: tuple[float, ...],
    *,
    rename_offset: int | None = None,
) -> AssaySummary:
    results: list[tuple[bool, SettlingResult]] = []
    for seed in seeds:
        episode = generate_episode(
            seed,
            rename_seed=(seed + rename_offset) if rename_offset is not None else None,
        )
        result = infer(episode, resistances)
        results.append((result.winner == episode.correct_name, result))
    return AssaySummary(
        episodes=len(results),
        accuracy=mean(1.0 if correct else 0.0 for correct, _ in results),
        mean_confidence_gap=mean(result.confidence_gap for _, result in results),
        settled_rate=mean(1.0 if result.settled else 0.0 for _, result in results),
    )


def run_assay(*, quick: bool = False) -> dict[str, object]:
    train_seeds = range(1000, 1120) if quick else TRAIN_SEEDS
    final_seeds = range(10000, 10200) if quick else FINAL_SEEDS

    learner = train_resistance(train_seeds)
    frozen = learner.frozen()
    equal = (1.0,) * CHANNEL_COUNT

    baseline = evaluate(final_seeds, equal)
    trained = evaluate(final_seeds, frozen)
    renamed = evaluate(final_seeds, frozen, rename_offset=700_000)

    return {
        "experiment": EXPERIMENT_ID,
        "question": (
            "Can outcome-driven resistance learning improve recurrent sparse settling "
            "on unseen anonymous candidate identities after learning is frozen?"
        ),
        "training": {
            "episodes": len(train_seeds),
            "updates": learner.updates,
            "learned_channel_resistance": list(frozen),
            "interpretation": {
                "channel_0": "historically misleading; should become high resistance",
                "channels_1_3": "jointly reliable; should become low resistance",
            },
        },
        "held_out_unseen": {
            "equal_resistance_baseline": baseline.to_dict(),
            "learned_resistance": trained.to_dict(),
            "renamed_candidates": renamed.to_dict(),
            "accuracy_gain": trained.accuracy - baseline.accuracy,
            "renaming_retention": (
                renamed.accuracy / trained.accuracy if trained.accuracy > 0.0 else 0.0
            ),
        },
        "scientific_boundary": (
            "This demonstrates learned structural resistance transfer in a synthetic "
            "world family. It does not yet demonstrate language grounding, autonomous "
            "discriminator generation, or production cognition integration."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run_assay(quick=args.quick), indent=2))


if __name__ == "__main__":
    main()
