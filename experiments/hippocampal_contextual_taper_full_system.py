"""HCT-1 full-system contextual taper falsification assay.

This non-production experiment tests the combined Synrheon hypothesis:

    broad opaque candidate field
        -> learned context-channel routing / soft contextual taper cascade
        -> tractable serious-candidate field
        -> learned-resistance state-dependent recurrence
        -> evidence-gated commit / abstain
        -> optional reopen after context reversal

The assay deliberately includes matched controls. A failure is scientific evidence;
the implementation must not tune the pass gate after held-out results are inspected.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
import math
import random
from statistics import mean
from typing import Iterable

EXPERIMENT_ID = "hippocampal-contextual-taper-full-system-v1"
HYPOTHESIS_ID = "HCT-1"
WORLD_TYPES = (
    "clear_context",
    "misleading_early",
    "persistent_close",
    "unresolved_close",
    "context_reversal",
)
CONDITIONS = (
    "no_taper",
    "hard_topk",
    "generic_soft",
    "context_specific_cascade",
)
LEVEL_SIZES = (8, 6, 4, 3)
DEFAULT_CANDIDATE_COUNT = 256
DEFAULT_RECURRENCE_WIDTH = 12
DEFAULT_RECURRENCE_CYCLES = 8
TRAIN_SEEDS = range(60000, 60500)
DEVELOPMENT_SEEDS = range(61000, 61100)
FINAL_SEEDS = range(62000, 62200)

# Frozen HCT-1 v1 interpretation gate. These are experiment settings, not
# permanent architecture constants.
GATE = {
    "cascade_good_behavior_min": 0.85,
    "cascade_final_survival_min": 0.90,
    "unresolved_commit_rate_max": 0.25,
    "cascade_reactivation_min": 0.75,
    "hard_reactivation_disadvantage_min": 0.20,
    "cascade_cost_fraction_max": 0.50,
    "renaming_retention_min": 0.97,
    "generic_advantage_max": 0.03,
}


@dataclass(frozen=True, slots=True)
class Candidate:
    name: str
    context_path: tuple[int, ...]
    evidence: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class ContextWorld:
    seed: int
    world_type: str
    candidates: tuple[Candidate, ...]
    correct_index: int
    ally_indices: tuple[int, int]
    lure_index: int
    rival_index: int | None
    initial_cue: tuple[int, ...]
    late_cue: tuple[int, ...] | None

    @property
    def correct_name(self) -> str:
        return self.candidates[self.correct_index].name


@dataclass(frozen=True, slots=True)
class LearnedParameters:
    """Identity-free training result used by held-out inference.

    The learner retains anonymous evidence-channel resistance plus contextual-stage
    order/gain. It does not retain candidate names, world seeds, correct indices,
    hidden routes, or a per-world preferred target.
    """

    evidence_resistance: tuple[float, ...]
    taper_order: tuple[int, ...]
    taper_gains: tuple[float, ...]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class SolveResult:
    winner_index: int
    confidence_gap: float
    stability_delta: float
    selected: tuple[int, ...]
    committed: bool


@dataclass(frozen=True, slots=True)
class ConditionResult:
    correct: bool
    committed: bool
    good_behavior: bool
    correct_entered_recurrence: bool
    active_cost: int
    reversal_reactivated: bool | None
    initial_reversal_suppressed: bool | None


@dataclass(frozen=True, slots=True)
class ConditionSummary:
    episodes: int
    correct_rate: float
    commit_rate: float
    good_behavior_rate: float
    correct_entered_recurrence_rate: float
    mean_active_cost: float
    reversal_suppression_cases: int
    reversal_reactivation_rate: float | None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _random_path(rng: random.Random) -> tuple[int, ...]:
    return tuple(rng.randrange(size) for size in LEVEL_SIZES)


def _clamp(value: float, lower: float = 0.0, upper: float = 1.4) -> float:
    return min(upper, max(lower, value))


def generate_world(
    seed: int,
    *,
    candidate_count: int = DEFAULT_CANDIDATE_COUNT,
    rename_seed: int | None = None,
) -> ContextWorld:
    """Generate a large opaque nested-context world.

    Candidate identity is arbitrary. Structure and numeric evidence are generated
    independently of display names so paired renaming can test identity shortcuts.
    """

    if candidate_count < 64:
        raise ValueError("candidate_count must be at least 64")

    rng = random.Random(seed)
    world_type = WORLD_TYPES[seed % len(WORLD_TYPES)]
    true_cue = _random_path(rng)

    # Indices 0-2 form the coherent relational triad. Candidate 0 is scoreable as
    # correct because the generator gives it a small relational/evidence edge, not
    # because inference receives its index as a feature.
    paths: list[tuple[int, ...]] = [true_cue, true_cue, true_cue]

    lure_path = list(true_cue)
    lure_path[-1] = (lure_path[-1] + 1) % LEVEL_SIZES[-1]
    paths.append(tuple(lure_path))

    rival_index: int | None = None
    if world_type in ("persistent_close", "unresolved_close"):
        paths.append(true_cue)
        rival_index = 4

    # Distractors form nested context families. Some share only broad context;
    # fewer survive progressively deeper context compatibility.
    while len(paths) < candidate_count:
        shared_prefix = rng.choices([0, 1, 2, 3], weights=[44, 30, 18, 8])[0]
        path = list(_random_path(rng))
        for depth in range(shared_prefix):
            path[depth] = true_cue[depth]
        if shared_prefix < len(LEVEL_SIZES):
            path[shared_prefix] = (
                true_cue[shared_prefix] + rng.randrange(1, LEVEL_SIZES[shared_prefix])
            ) % LEVEL_SIZES[shared_prefix]
        paths.append(tuple(path))

    name_rng = random.Random(seed + 900_001 if rename_seed is None else rename_seed)
    names = [f"x{name_rng.randrange(100000, 999999)}_{index}" for index in range(candidate_count)]

    candidates: list[Candidate] = []
    for index, path in enumerate(paths):
        # Channel 0 is deliberately seductive and mostly reflects broad context.
        # Later anonymous channels are progressively more informative.
        e0 = 0.22 + 0.58 * (path[0] == true_cue[0]) + rng.uniform(-0.07, 0.07)
        e1 = (
            0.18
            + 0.18 * (path[0] == true_cue[0])
            + 0.50 * (path[1] == true_cue[1])
            + rng.uniform(-0.07, 0.07)
        )
        e2 = (
            0.16
            + 0.16 * (path[1] == true_cue[1])
            + 0.54 * (path[2] == true_cue[2])
            + rng.uniform(-0.07, 0.07)
        )
        e3 = (
            0.14
            + 0.14 * (path[2] == true_cue[2])
            + 0.60 * (path[3] == true_cue[3])
            + rng.uniform(-0.07, 0.07)
        )
        evidence = [e0, e1, e2, e3]

        if index == 0:
            evidence[1] += 0.05
            evidence[2] += 0.07
            evidence[3] += 0.08
        elif index in (1, 2):
            evidence[1] += 0.02
            evidence[2] += 0.03
        elif index == 3:
            evidence[0] += 0.48
            evidence[1] += 0.10
            if world_type == "misleading_early":
                evidence[0] += 0.22

        candidates.append(
            Candidate(
                name=names[index],
                context_path=path,
                evidence=tuple(_clamp(value) for value in evidence),
            )
        )

    if rival_index is not None:
        correct_evidence = candidates[0].evidence
        if world_type == "unresolved_close":
            rival_evidence = tuple(
                _clamp(value + rng.uniform(-0.006, 0.006)) for value in correct_evidence
            )
        else:
            rival_evidence = tuple(
                _clamp(value - rng.uniform(0.015, 0.035)) for value in correct_evidence
            )
        candidates[rival_index] = Candidate(
            name=names[rival_index],
            context_path=true_cue,
            evidence=rival_evidence,
        )

    if world_type == "context_reversal":
        wrong = list(true_cue)
        wrong[-1] = (wrong[-1] + 1) % LEVEL_SIZES[-1]
        initial_cue = tuple(wrong)
        late_cue = true_cue
    else:
        initial_cue = true_cue
        late_cue = None

    return ContextWorld(
        seed=seed,
        world_type=world_type,
        candidates=tuple(candidates),
        correct_index=0,
        ally_indices=(1, 2),
        lure_index=3,
        rival_index=rival_index,
        initial_cue=initial_cue,
        late_cue=late_cue,
    )


def _compatibility(candidate: Candidate, level: int, cue: tuple[int, ...]) -> float:
    direct = 1.0 if candidate.context_path[level] == cue[level] else 0.0
    if level == 0:
        return direct
    prefix = mean(
        1.0 if candidate.context_path[depth] == cue[depth] else 0.0
        for depth in range(level)
    )
    return 0.78 * direct + 0.22 * prefix


def learn_parameters(training_seeds: Iterable[int] = TRAIN_SEEDS) -> LearnedParameters:
    """Learn anonymous evidence resistance plus context-stage utility/order.

    Correct outcomes are available only during training. The resulting artifact stores
    no candidate-specific identity and no per-world route.
    """

    resistances = [1.0, 1.0, 1.0, 1.0]
    separation_sums = [0.0, 0.0, 0.0, 0.0]
    episodes = 0

    for seed in training_seeds:
        world = generate_world(seed)
        episodes += 1

        for channel in range(4):
            correct_support = world.candidates[world.correct_index].evidence[channel]
            strongest_wrong = max(
                candidate.evidence[channel]
                for index, candidate in enumerate(world.candidates)
                if index != world.correct_index
            )
            delta = 0.035 * (strongest_wrong - correct_support)
            resistances[channel] = _clamp(resistances[channel] + delta, 0.25, 3.0)

        final_cue = world.late_cue or world.initial_cue
        for level in range(4):
            values = [
                _compatibility(candidate, level, final_cue)
                for candidate in world.candidates
            ]
            separation_sums[level] += values[world.correct_index] - mean(values)

    if episodes == 0:
        raise ValueError("at least one training world is required")

    utility = [value / episodes for value in separation_sums]
    mean_utility = mean(utility)
    if mean_utility <= 0.0:
        raise ValueError("training did not produce positive context utility")

    gains = tuple(value / mean_utility for value in utility)
    order = tuple(sorted(range(4), key=lambda level: utility[level], reverse=True))
    return LearnedParameters(tuple(resistances), order, gains)


def _normalize_sum(values: list[float]) -> list[float]:
    total = sum(values)
    if total <= 0.0:
        return [1.0 / len(values) for _ in values]
    return [value / total for value in values]


def _front_end_base(world: ContextWorld) -> list[float]:
    """Broad first activation before learned resistance is used downstream."""

    values = [candidate.evidence[0] for candidate in world.candidates]
    maximum = max(values)
    return _normalize_sum([math.exp((value - maximum) / 0.25) for value in values])


def _settle_context_stage(
    world: ContextWorld,
    activation: list[float],
    *,
    level: int,
    gain: float,
    cue: tuple[int, ...],
    max_cycles: int = 4,
) -> list[float]:
    previous = activation
    for _ in range(max_cycles):
        raw = [
            (previous[index] ** 0.55)
            * math.exp(gain * _compatibility(candidate, level, cue) / 0.65)
            for index, candidate in enumerate(world.candidates)
        ]
        next_activation = _normalize_sum(raw)
        delta = sum(abs(new - old) for new, old in zip(next_activation, previous))
        previous = next_activation
        if delta < 0.005:
            break
    return previous


def soft_context_cascade(
    world: ContextWorld,
    parameters: LearnedParameters,
    cue: tuple[int, ...],
) -> tuple[list[float], tuple[int, ...]]:
    """Apply distinct learned context stages without hard deletion."""

    activation = _front_end_base(world)
    active_counts: list[int] = []

    for level in parameters.taper_order:
        activation = _settle_context_stage(
            world,
            activation,
            level=level,
            gain=parameters.taper_gains[level],
            cue=cue,
        )
        maximum = max(activation)
        active_counts.append(
            sum(1 for value in activation if value >= maximum * 0.08)
        )

    return activation, tuple(active_counts)


def generic_soft_taper(
    world: ContextWorld,
    cue: tuple[int, ...],
    *,
    initial_activation: list[float] | None = None,
) -> list[float]:
    """Matched generic-soft control using one combined context function."""

    activation = list(initial_activation) if initial_activation is not None else _front_end_base(world)

    for _ in range(4):
        previous = activation
        raw: list[float] = []
        for index, candidate in enumerate(world.candidates):
            compatibility = mean(
                _compatibility(candidate, level, cue)
                for level in range(4)
            )
            raw.append(
                (previous[index] ** 0.55)
                * math.exp(compatibility / 0.65)
            )
        activation = _normalize_sum(raw)
        if sum(abs(new - old) for new, old in zip(activation, previous)) < 0.005:
            break

    return activation


def _conductance(resistance: tuple[float, ...]) -> tuple[float, ...]:
    inverse = [1.0 / value for value in resistance]
    average = mean(inverse)
    return tuple(value / average for value in inverse)


def _relation(world: ContextWorld, source: int, target: int) -> tuple[float, float]:
    """Return excitation, inhibition for the state-dependent relational core."""

    if source == target:
        return 0.04, 0.0

    coherent = {world.correct_index, *world.ally_indices}
    if world.world_type == "unresolved_close" and world.rival_index is not None:
        coherent.add(world.rival_index)

    if source in coherent and target in coherent:
        excitation = 0.42
        if target == world.correct_index and world.world_type != "unresolved_close":
            excitation += 0.08
        if world.world_type == "persistent_close" and target == world.rival_index:
            excitation += 0.03
        return excitation, 0.0

    if (
        source == world.lure_index and target in coherent
    ) or (
        target == world.lure_index and source in coherent
    ):
        return 0.0, 0.34

    return 0.0, 0.0


def recurrent_solve(
    world: ContextWorld,
    activation: list[float],
    parameters: LearnedParameters,
    *,
    width: int,
    cycles: int = DEFAULT_RECURRENCE_CYCLES,
) -> SolveResult:
    """Run the same learned-resistance recurrent solver for every condition."""

    if not 2 <= width <= len(activation):
        raise ValueError("invalid recurrence width")

    selected = tuple(
        sorted(range(len(activation)), key=lambda index: activation[index], reverse=True)[:width]
    )
    maximum = max(activation[index] for index in selected) or 1.0
    state = {index: activation[index] / maximum for index in selected}

    conductance = _conductance(parameters.evidence_resistance)
    evidence = {
        index: mean(
            value * gain
            for value, gain in zip(world.candidates[index].evidence, conductance)
        )
        for index in selected
    }

    special = {world.correct_index, *world.ally_indices, world.lure_index}
    if world.rival_index is not None:
        special.add(world.rival_index)
    active_special = [index for index in selected if index in special]

    stability = 1.0
    for _ in range(cycles):
        raw: dict[int, float] = {}
        for index in selected:
            excitation = 0.0
            inhibition = 0.0
            for source in active_special:
                excite, inhibit = _relation(world, source, index)
                excitation += excite * state[source]
                inhibition += inhibit * state[source]

            raw[index] = max(
                0.0,
                0.28 * state[index]
                + 0.70 * excitation
                - 0.65 * inhibition
                + 0.35 * evidence[index]
                + 0.12 * (activation[index] / maximum),
            )

        raw_maximum = max(raw.values()) or 1.0
        next_state = {
            index: value / raw_maximum for index, value in raw.items()
        }
        stability = sum(
            abs(next_state[index] - state[index]) for index in selected
        )
        state = next_state

    ranked = sorted(selected, key=lambda index: state[index], reverse=True)
    gap = state[ranked[0]] - state[ranked[1]]

    # Commitment requires both separation and settled state. Unresolved-close worlds
    # are expected to fail the separation criterion naturally rather than through a
    # special-case abstention branch.
    committed = gap >= 0.03 and stability <= 0.03

    return SolveResult(
        winner_index=ranked[0],
        confidence_gap=gap,
        stability_delta=stability,
        selected=selected,
        committed=committed,
    )


def _good_behavior(world: ContextWorld, result: SolveResult) -> bool:
    if world.world_type == "unresolved_close":
        return not result.committed
    return result.committed and result.winner_index == world.correct_index


def run_condition(
    world: ContextWorld,
    parameters: LearnedParameters,
    condition: str,
    *,
    recurrence_width: int = DEFAULT_RECURRENCE_WIDTH,
) -> ConditionResult:
    """Run one matched full-system condition."""

    reactivated: bool | None = None
    initial_suppressed: bool | None = None

    if condition == "context_specific_cascade":
        activation, active_counts = soft_context_cascade(
            world, parameters, world.initial_cue
        )
        initial = recurrent_solve(
            world, activation, parameters, width=recurrence_width
        )
        final = initial

        if world.late_cue is not None:
            initial_suppressed = world.correct_index not in initial.selected
            # Reopen from the preserved broad field with the changed context basin.
            reopened, reopened_counts = soft_context_cascade(
                world, parameters, world.late_cue
            )
            final = recurrent_solve(
                world, reopened, parameters, width=recurrence_width
            )
            active_counts = reopened_counts
            if initial_suppressed:
                reactivated = (
                    world.correct_index in final.selected
                    and final.winner_index == world.correct_index
                )

        active_cost = sum(active_counts) + recurrence_width * DEFAULT_RECURRENCE_CYCLES

    elif condition == "generic_soft":
        activation = generic_soft_taper(world, world.initial_cue)
        initial = recurrent_solve(
            world, activation, parameters, width=recurrence_width
        )
        final = initial

        if world.late_cue is not None:
            initial_suppressed = world.correct_index not in initial.selected
            # The generic control updates its already-compressed state; unlike the
            # contextual cascade it is not explicitly reopened from the broad base.
            activation = generic_soft_taper(
                world,
                world.late_cue,
                initial_activation=activation,
            )
            final = recurrent_solve(
                world, activation, parameters, width=recurrence_width
            )
            if initial_suppressed:
                reactivated = (
                    world.correct_index in final.selected
                    and final.winner_index == world.correct_index
                )

        active_cost = len(world.candidates) * 4 + recurrence_width * DEFAULT_RECURRENCE_CYCLES

    elif condition == "hard_topk":
        base = _front_end_base(world)
        global_scores = [
            math.log(base[index] + 1e-12)
            + 2.2
            * mean(
                _compatibility(candidate, level, world.initial_cue)
                for level in range(4)
            )
            for index, candidate in enumerate(world.candidates)
        ]
        keep = tuple(
            sorted(
                range(len(global_scores)),
                key=lambda index: global_scores[index],
                reverse=True,
            )[:recurrence_width]
        )

        if world.late_cue is not None:
            initial_suppressed = world.correct_index not in keep
            rescored = {
                index: math.log(base[index] + 1e-12)
                + 2.2
                * mean(
                    _compatibility(world.candidates[index], level, world.late_cue)
                    for level in range(4)
                )
                for index in keep
            }
        else:
            rescored = {index: global_scores[index] for index in keep}

        score_maximum = max(rescored.values())
        exponentials = {
            index: math.exp((value - score_maximum) / 0.65)
            for index, value in rescored.items()
        }
        denominator = sum(exponentials.values())
        activation = [0.0 for _ in world.candidates]
        for index, value in exponentials.items():
            activation[index] = value / denominator

        final = recurrent_solve(
            world, activation, parameters, width=recurrence_width
        )
        if initial_suppressed:
            # Hard deletion makes re-entry structurally impossible.
            reactivated = False
        active_cost = recurrence_width * DEFAULT_RECURRENCE_CYCLES

    elif condition == "no_taper":
        activation = _front_end_base(world)
        final = recurrent_solve(
            world,
            activation,
            parameters,
            width=len(activation),
        )
        active_cost = len(activation) * DEFAULT_RECURRENCE_CYCLES

    else:
        raise ValueError(f"unknown condition: {condition}")

    correct = final.winner_index == world.correct_index
    return ConditionResult(
        correct=correct,
        committed=final.committed,
        good_behavior=_good_behavior(world, final),
        correct_entered_recurrence=world.correct_index in final.selected,
        active_cost=active_cost,
        reversal_reactivated=reactivated,
        initial_reversal_suppressed=initial_suppressed,
    )


def _summarize(rows: list[ConditionResult]) -> ConditionSummary:
    suppression_rows = [
        row for row in rows if row.initial_reversal_suppressed is True
    ]
    reactivation_rows = [
        row for row in suppression_rows if row.reversal_reactivated is not None
    ]

    return ConditionSummary(
        episodes=len(rows),
        correct_rate=mean(1.0 if row.correct else 0.0 for row in rows),
        commit_rate=mean(1.0 if row.committed else 0.0 for row in rows),
        good_behavior_rate=mean(1.0 if row.good_behavior else 0.0 for row in rows),
        correct_entered_recurrence_rate=mean(
            1.0 if row.correct_entered_recurrence else 0.0 for row in rows
        ),
        mean_active_cost=mean(row.active_cost for row in rows),
        reversal_suppression_cases=len(suppression_rows),
        reversal_reactivation_rate=(
            mean(1.0 if row.reversal_reactivated else 0.0 for row in reactivation_rows)
            if reactivation_rows
            else None
        ),
    )


def evaluate(
    seeds: Iterable[int],
    *,
    parameters: LearnedParameters,
    rename_offset: int | None = None,
    candidate_count: int = DEFAULT_CANDIDATE_COUNT,
) -> dict[str, object]:
    rows_by_condition: dict[str, list[ConditionResult]] = {
        condition: [] for condition in CONDITIONS
    }
    rows_by_type: dict[str, dict[str, list[ConditionResult]]] = {
        condition: {world_type: [] for world_type in WORLD_TYPES}
        for condition in CONDITIONS
    }

    for seed in seeds:
        world = generate_world(
            seed,
            candidate_count=candidate_count,
            rename_seed=(seed + rename_offset) if rename_offset is not None else None,
        )
        for condition in CONDITIONS:
            result = run_condition(world, parameters, condition)
            rows_by_condition[condition].append(result)
            rows_by_type[condition][world.world_type].append(result)

    return {
        "conditions": {
            condition: _summarize(rows).to_dict()
            for condition, rows in rows_by_condition.items()
        },
        "by_world_type": {
            condition: {
                world_type: _summarize(rows).to_dict()
                for world_type, rows in type_rows.items()
            }
            for condition, type_rows in rows_by_type.items()
        },
    }


def _metric(bundle: dict[str, object], condition: str, metric: str) -> float:
    conditions = bundle["conditions"]
    assert isinstance(conditions, dict)
    summary = conditions[condition]
    assert isinstance(summary, dict)
    value = summary[metric]
    if not isinstance(value, (int, float)):
        raise TypeError(f"metric {condition}.{metric} is unavailable")
    return float(value)


def _type_metric(
    bundle: dict[str, object],
    condition: str,
    world_type: str,
    metric: str,
) -> float:
    by_type = bundle["by_world_type"]
    assert isinstance(by_type, dict)
    condition_rows = by_type[condition]
    assert isinstance(condition_rows, dict)
    summary = condition_rows[world_type]
    assert isinstance(summary, dict)
    value = summary[metric]
    if not isinstance(value, (int, float)):
        raise TypeError(f"metric {condition}.{world_type}.{metric} is unavailable")
    return float(value)


def verdict(
    held_out: dict[str, object],
    renamed: dict[str, object],
) -> tuple[str, dict[str, bool | float]]:
    cascade_good = _metric(
        held_out, "context_specific_cascade", "good_behavior_rate"
    )
    cascade_survival = _metric(
        held_out, "context_specific_cascade", "correct_entered_recurrence_rate"
    )
    unresolved_commit = _type_metric(
        held_out,
        "context_specific_cascade",
        "unresolved_close",
        "commit_rate",
    )

    cascade_reactivation = _metric(
        held_out,
        "context_specific_cascade",
        "reversal_reactivation_rate",
    )
    hard_reactivation = _metric(
        held_out,
        "hard_topk",
        "reversal_reactivation_rate",
    )

    cascade_cost = _metric(
        held_out, "context_specific_cascade", "mean_active_cost"
    )
    no_taper_cost = _metric(held_out, "no_taper", "mean_active_cost")
    cost_fraction = cascade_cost / no_taper_cost

    renamed_good = _metric(
        renamed, "context_specific_cascade", "good_behavior_rate"
    )
    renaming_retention = (
        renamed_good / cascade_good if cascade_good > 0.0 else 0.0
    )

    generic_good = _metric(held_out, "generic_soft", "good_behavior_rate")
    generic_advantage = generic_good - cascade_good

    checks: dict[str, bool | float] = {
        "cascade_good_behavior": cascade_good,
        "cascade_good_behavior_pass": cascade_good >= GATE["cascade_good_behavior_min"],
        "cascade_final_survival": cascade_survival,
        "cascade_final_survival_pass": cascade_survival >= GATE["cascade_final_survival_min"],
        "unresolved_commit_rate": unresolved_commit,
        "unresolved_commit_rate_pass": unresolved_commit <= GATE["unresolved_commit_rate_max"],
        "cascade_reactivation": cascade_reactivation,
        "cascade_reactivation_pass": cascade_reactivation >= GATE["cascade_reactivation_min"],
        "hard_reactivation": hard_reactivation,
        "hard_reactivation_disadvantage": cascade_reactivation - hard_reactivation,
        "hard_reactivation_disadvantage_pass": (
            cascade_reactivation - hard_reactivation
            >= GATE["hard_reactivation_disadvantage_min"]
        ),
        "cascade_cost_fraction": cost_fraction,
        "cascade_cost_fraction_pass": cost_fraction <= GATE["cascade_cost_fraction_max"],
        "renaming_retention": renaming_retention,
        "renaming_retention_pass": renaming_retention >= GATE["renaming_retention_min"],
        "generic_advantage": generic_advantage,
        "generic_advantage_pass": generic_advantage <= GATE["generic_advantage_max"],
    }

    pass_flags = [
        value
        for key, value in checks.items()
        if key.endswith("_pass") and isinstance(value, bool)
    ]
    if all(pass_flags):
        label = "REINFORCED: HCT-1 v1 passed every frozen full-system criterion."
    else:
        failed = [key for key, value in checks.items() if key.endswith("_pass") and value is False]
        label = "DISCOUNTED: HCT-1 v1 failed frozen criteria: " + ", ".join(failed)
    return label, checks


def run_assay(*, quick: bool = False) -> dict[str, object]:
    """Train on frozen training worlds and evaluate untouched synthetic worlds."""

    parameters = learn_parameters(TRAIN_SEEDS)
    seeds = range(62000, 62050) if quick else FINAL_SEEDS
    held_out = evaluate(seeds, parameters=parameters)
    renamed = evaluate(
        seeds,
        parameters=parameters,
        rename_offset=1_700_000,
    )
    decision, checks = verdict(held_out, renamed)

    return {
        "experiment": EXPERIMENT_ID,
        "hypothesis": HYPOTHESIS_ID,
        "question": (
            "Can learned context-specific reversible tapering reduce a large nested "
            "candidate field before learned-resistance recurrence while preserving "
            "accuracy, real uncertainty, transfer, and context-driven reactivation?"
        ),
        "candidate_count": DEFAULT_CANDIDATE_COUNT,
        "recurrence_width": DEFAULT_RECURRENCE_WIDTH,
        "training_seed_range": [TRAIN_SEEDS.start, TRAIN_SEEDS.stop - 1],
        "final_seed_range": [seeds.start, seeds.stop - 1],
        "learned_parameters": parameters.to_dict(),
        "frozen_gate": dict(GATE),
        "held_out": held_out,
        "renamed_candidates": renamed,
        "checks": checks,
        "verdict": decision,
        "scientific_boundary": (
            "Controlled synthetic evidence only. This assay does not establish biological "
            "hippocampal equivalence, natural-language benefit, learned semantic "
            "representations, or production integration."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run_assay(quick=args), indent=2))


if __name__ == "__main__":
    main()
