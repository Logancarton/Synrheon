"""Stochastic multi-trial recurrent consensus assay.

This experiment tests a stronger version of the Synrheon settling hypothesis:

1. Do not trust one recurrent trajectory as final confidence.
2. Rerun the same relational field under small controlled uncertainty perturbations.
3. Accumulate empirical winner frequencies.
4. Commit only after the leading winner has a sufficiently large population gap.
5. Preserve the strongest losing hypotheses for later counterfactual analysis.

The test is deliberately falsifiable. A repeated-trial system is not considered useful
merely because it runs more compute. It must preserve accuracy on resolvable worlds,
avoid false commitment on genuinely unresolved worlds, and exercise both early stopping
and continued sampling.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
import math
import random
from statistics import mean

from experiments.hippocampal_confidence_gated import WORLD_TYPES, generate_mixed_world
from experiments.hippocampal_stateful_recurrence import StatefulWorld, recurrent

EXPERIMENT_ID = "hippocampal-stochastic-consensus-v1"
RESOLVABLE_TYPES = ("easy_clear", "delayed_clear", "persistent_close", "misleading_early")


@dataclass(frozen=True, slots=True)
class TrialOutcome:
    trial: int
    winner: str
    confidence_gap: float


@dataclass(frozen=True, slots=True)
class ConsensusResult:
    committed: bool
    winner: str | None
    trials_used: int
    winner_share: float
    runner_up_share: float
    population_gap: float
    win_shares: dict[str, float]
    retained_alternatives: tuple[tuple[str, float], ...]
    outcomes: tuple[TrialOutcome, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "committed": self.committed,
            "winner": self.winner,
            "trials_used": self.trials_used,
            "winner_share": self.winner_share,
            "runner_up_share": self.runner_up_share,
            "population_gap": self.population_gap,
            "win_shares": dict(self.win_shares),
            "retained_alternatives": [list(item) for item in self.retained_alternatives],
            "outcomes": [asdict(item) for item in self.outcomes],
        }


@dataclass(frozen=True, slots=True)
class Summary:
    episodes: int
    committed_rate: float
    committed_accuracy: float
    overall_correct_or_abstain_rate: float
    mean_trials: float
    early_stop_rate: float
    max_trial_rate: float
    mean_population_gap: float
    mean_retained_alternatives: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _clamp(value: float, lower: float = 0.0, upper: float = 1.25) -> float:
    return min(upper, max(lower, value))


def perturb_world(world: StatefulWorld, *, seed: int, noise_scale: float = 0.045) -> StatefulWorld:
    """Create one plausible trajectory by perturbing uncertain evidence slightly.

    Candidate identity and the hidden correct index never change. Perturbations affect
    initial activation and relational strengths only. This is analogous to sampling
    within uncertainty rather than asking the deterministic system the same question
    repeatedly.
    """

    rng = random.Random(seed)
    initial = tuple(_clamp(value + rng.gauss(0.0, noise_scale)) for value in world.initial)

    excitation_rows: list[tuple[float, ...]] = []
    inhibition_rows: list[tuple[float, ...]] = []
    relation_noise = noise_scale * 0.55
    for excitation_row, inhibition_row in zip(world.excitation, world.inhibition):
        excitation_rows.append(
            tuple(
                _clamp(value + rng.gauss(0.0, relation_noise)) if value > 0.0 else 0.0
                for value in excitation_row
            )
        )
        inhibition_rows.append(
            tuple(
                _clamp(value + rng.gauss(0.0, relation_noise)) if value > 0.0 else 0.0
                for value in inhibition_row
            )
        )

    return StatefulWorld(
        seed=world.seed,
        names=world.names,
        initial=initial,
        excitation=tuple(excitation_rows),
        inhibition=tuple(inhibition_rows),
        correct_index=world.correct_index,
    )


def _shares(counts: dict[str, int], trials: int) -> dict[str, float]:
    return {name: count / trials for name, count in counts.items()}


def _ranked_shares(shares: dict[str, float]) -> list[tuple[str, float]]:
    return sorted(shares.items(), key=lambda item: (-item[1], item[0]))


def _retained_alternatives(
    ranked: list[tuple[str, float]],
    *,
    relative_floor: float = 0.20,
) -> tuple[tuple[str, float], ...]:
    """Retain meaningful losing hypotheses for later analysis.

    A loser is retained when its empirical win share is at least 20% of the winning
    share. The runner-up is always retained when one exists so every commitment keeps
    at least one explicit counterfactual.
    """

    if len(ranked) < 2:
        return ()
    winner_share = ranked[0][1]
    kept = [item for item in ranked[1:] if item[1] >= winner_share * relative_floor]
    if not kept:
        kept = [ranked[1]]
    return tuple(kept)


def consensus_trials(
    world: StatefulWorld,
    *,
    trial_seed: int,
    minimum_trials: int = 9,
    maximum_trials: int = 51,
    check_every: int = 3,
    commit_gap: float = 0.34,
    minimum_winner_share: float = 0.58,
    noise_scale: float = 0.045,
) -> ConsensusResult:
    """Repeat recurrent settling until a population-level winner is decisive.

    Stopping rule after minimum_trials:

        winner_share >= minimum_winner_share
        and
        winner_share - runner_up_share >= commit_gap

    If the population never separates enough, return committed=False at maximum_trials.
    """

    if minimum_trials < 3 or maximum_trials < minimum_trials:
        raise ValueError("invalid trial budget")
    if check_every < 1:
        raise ValueError("check_every must be positive")

    counts = {name: 0 for name in world.names}
    outcomes: list[TrialOutcome] = []
    rng = random.Random(trial_seed)
    committed = False

    for trial in range(1, maximum_trials + 1):
        sampled = perturb_world(world, seed=rng.randrange(1, 2_147_483_647), noise_scale=noise_scale)
        result = recurrent(sampled, progressive_sparsity=False)
        counts[result.winner] += 1
        outcomes.append(TrialOutcome(trial, result.winner, result.confidence_gap))

        if trial < minimum_trials or trial % check_every != 0:
            continue

        ranked = _ranked_shares(_shares(counts, trial))
        lead_share = ranked[0][1]
        second_share = ranked[1][1]
        if lead_share >= minimum_winner_share and lead_share - second_share >= commit_gap:
            committed = True
            break

    trials_used = len(outcomes)
    shares = _shares(counts, trials_used)
    ranked = _ranked_shares(shares)
    winner_name = ranked[0][0] if committed else None
    winner_share = ranked[0][1]
    runner_up_share = ranked[1][1]
    return ConsensusResult(
        committed=committed,
        winner=winner_name,
        trials_used=trials_used,
        winner_share=winner_share,
        runner_up_share=runner_up_share,
        population_gap=winner_share - runner_up_share,
        win_shares=shares,
        retained_alternatives=_retained_alternatives(ranked),
        outcomes=tuple(outcomes),
    )


def _summary(rows: list[tuple[bool, bool, ConsensusResult]], *, unresolved: bool) -> Summary:
    committed = [row for row in rows if row[1]]
    committed_correct = [row for row in committed if row[0]]
    if unresolved:
        good_behavior = [row for row in rows if not row[1]]
    else:
        good_behavior = [row for row in rows if row[0] and row[1]]

    return Summary(
        episodes=len(rows),
        committed_rate=mean(1.0 if committed_flag else 0.0 for _, committed_flag, _ in rows),
        committed_accuracy=(len(committed_correct) / len(committed)) if committed else 0.0,
        overall_correct_or_abstain_rate=len(good_behavior) / len(rows),
        mean_trials=mean(result.trials_used for _, _, result in rows),
        early_stop_rate=mean(1.0 if result.trials_used < 51 else 0.0 for _, _, result in rows),
        max_trial_rate=mean(1.0 if result.trials_used == 51 else 0.0 for _, _, result in rows),
        mean_population_gap=mean(result.population_gap for _, _, result in rows),
        mean_retained_alternatives=mean(len(result.retained_alternatives) for _, _, result in rows),
    )


def evaluate(seeds: range, *, rename_offset: int | None = None) -> dict[str, object]:
    by_type_rows: dict[str, list[tuple[bool, bool, ConsensusResult]]] = {kind: [] for kind in WORLD_TYPES}
    deterministic_correct: dict[str, list[bool]] = {kind: [] for kind in WORLD_TYPES}

    for seed in seeds:
        world_type, world = generate_mixed_world(
            seed,
            rename_seed=(seed + rename_offset) if rename_offset is not None else None,
        )
        deterministic = recurrent(world, progressive_sparsity=False)
        deterministic_correct[world_type].append(deterministic.winner == world.correct_name)

        result = consensus_trials(world, trial_seed=seed * 17 + 11)
        correct = result.committed and result.winner == world.correct_name
        by_type_rows[world_type].append((correct, result.committed, result))

    by_type = {
        kind: _summary(rows, unresolved=(kind == "unresolved_close"))
        for kind, rows in by_type_rows.items()
    }

    resolvable_rows = [
        row
        for kind in RESOLVABLE_TYPES
        for row in by_type_rows[kind]
    ]
    unresolved_rows = by_type_rows["unresolved_close"]
    resolvable = _summary(resolvable_rows, unresolved=False)
    unresolved = _summary(unresolved_rows, unresolved=True)

    deterministic_resolvable_accuracy = mean(
        1.0 if ok else 0.0
        for kind in RESOLVABLE_TYPES
        for ok in deterministic_correct[kind]
    )
    deterministic_unresolved_accuracy = mean(
        1.0 if ok else 0.0 for ok in deterministic_correct["unresolved_close"]
    )

    return {
        "resolvable": resolvable,
        "unresolved_close": unresolved,
        "by_world_type": by_type,
        "deterministic_fixed_recurrent": {
            "resolvable_accuracy": deterministic_resolvable_accuracy,
            "unresolved_close_forced_accuracy": deterministic_unresolved_accuracy,
        },
    }


def verdict(bundle: dict[str, object]) -> str:
    resolvable = bundle["resolvable"]
    unresolved = bundle["unresolved_close"]
    by_type = bundle["by_world_type"]
    baseline = bundle["deterministic_fixed_recurrent"]
    assert isinstance(resolvable, Summary)
    assert isinstance(unresolved, Summary)
    assert isinstance(by_type, dict)
    assert isinstance(baseline, dict)

    easy = by_type["easy_clear"]
    misleading = by_type["misleading_early"]
    assert isinstance(easy, Summary) and isinstance(misleading, Summary)

    # First establish that the sampling mechanism actually exercises both outcomes.
    if resolvable.early_stop_rate < 0.25:
        return "INCONCLUSIVE: resolvable worlds rarely reached an early population consensus."
    if unresolved.max_trial_rate < 0.50:
        return "DISCOUNTED: genuinely unresolved worlds too often produced a false population consensus."

    # Core falsification criteria.
    baseline_accuracy = float(baseline["resolvable_accuracy"])
    if resolvable.committed_accuracy < baseline_accuracy - 0.05:
        return "DISCOUNTED: repeated consensus reduced accuracy on resolvable worlds."
    if resolvable.committed_rate < 0.65:
        return "DISCOUNTED: the consensus rule abstained too often on resolvable worlds."
    if unresolved.committed_rate > 0.35:
        return "DISCOUNTED: the consensus rule overcommitted on unresolved close calls."
    if misleading.committed_accuracy < 0.85:
        return "DISCOUNTED: repeated trials did not reliably overcome misleading early evidence."
    if resolvable.mean_retained_alternatives < 1.0:
        return "DISCOUNTED: the system failed to retain explicit losing counterfactuals."

    return "REINFORCED: repeated stochastic recurrence forms stable population consensus, preserves counterfactual losers, and abstains when the population remains split."


def serialize(bundle: dict[str, object]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in bundle.items():
        if isinstance(value, Summary):
            result[key] = value.to_dict()
        elif isinstance(value, dict):
            result[key] = {
                subkey: (subvalue.to_dict() if isinstance(subvalue, Summary) else subvalue)
                for subkey, subvalue in value.items()
            }
        else:
            result[key] = value
    return result


def run_assay(*, quick: bool = False) -> dict[str, object]:
    seeds = range(40000, 40250) if quick else range(40000, 41250)
    held = evaluate(seeds)
    renamed = evaluate(seeds, rename_offset=1_300_000)
    return {
        "experiment": EXPERIMENT_ID,
        "question": (
            "Can repeated perturbed recurrent trials accumulate a reliable population "
            "winner, stop when the winner separates, preserve strong losing hypotheses, "
            "and remain unresolved when no stable winner exists?"
        ),
        "decision_rule": {
            "minimum_trials": 9,
            "maximum_trials": 51,
            "check_every": 3,
            "minimum_winner_share": 0.58,
            "commit_gap": 0.34,
            "counterfactual_relative_floor": 0.20,
        },
        "held_out": serialize(held),
        "renamed_candidates": serialize(renamed),
        "verdict": verdict(held),
        "scientific_boundary": (
            "This tests stochastic consensus only in the current synthetic mixed relational "
            "family. It does not establish optimal thresholds, biological equivalence, or "
            "benefit in learned language representations."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run_assay(quick=args), indent=2))


if __name__ == "__main__":
    main()
