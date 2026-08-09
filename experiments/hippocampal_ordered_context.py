"""HCT-2 ordered conditional context-settling falsification assay.

This is a non-production synthetic experiment. HCT-2 follows HCT-1 without
modifying HCT-1's frozen experiment or held-out results.

Question:
    When context channels are hierarchically aliased, can a learned order of
    reversible sparse context stages preserve behavior while requiring fewer
    context-feature evaluations than a strong simultaneous generic-soft control?

The final held-out split is intentionally distinct from training/development.
The --quick flag uses development seeds, never final seeds.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import itertools
import json
import math
import random
from statistics import mean
from typing import Iterable

EXPERIMENT_ID = "hippocampal-ordered-conditional-context-v1"
HYPOTHESIS_ID = "HCT-2"

WORLD_TYPES = (
    "clear_hierarchy",
    "alias_conflict",
    "misleading_deep",
    "unresolved_branch",
    "context_reversal",
)

CONDITIONS = (
    "no_taper",
    "hard_topk",
    "generic_soft",
    "fixed_order_sparse",
    "learned_order_sparse",
    "learned_order_no_resistance",
    "learned_order_no_recurrence",
)

LEVEL_SIZES = (8, 7, 6, 5)

# Anonymous observed context channels do not appear in semantic-depth order.
CHANNEL_TO_DEPTH = (2, 0, 3, 1)
DEPTH_TO_CHANNEL = {
    depth: channel for channel, depth in enumerate(CHANNEL_TO_DEPTH)
}

DEFAULT_CANDIDATE_COUNT = 512
DEFAULT_RECURRENCE_WIDTH = 16
DEFAULT_RECURRENCE_CYCLES = 8
SPARSE_STAGE_CYCLES = 2
GENERIC_CYCLES = 8
SPARSE_RELATIVE_GATE = 0.25

TRAIN_SEEDS = range(70000, 70500)
DEVELOPMENT_SEEDS = range(71000, 71150)
FINAL_SEEDS = range(72000, 72300)
QUICK_DEVELOPMENT_SEEDS = range(71000, 71050)

# Frozen before any HCT-2 final split is run.
GATE = {
    "learned_good_behavior_min": 0.90,
    "learned_final_survival_min": 0.95,
    "unresolved_commit_rate_max": 0.20,
    "reversal_suppression_cases_min": 10,
    "learned_reactivation_min": 0.80,
    "hard_reactivation_disadvantage_min": 0.30,
    "recurrent_cost_fraction_max": 0.10,
    "renaming_retention_min": 0.97,
    "generic_behavior_advantage_max": 0.03,
    "context_eval_fraction_vs_generic_max": 0.50,
    "learned_order_efficiency_advantage_min": 0.03,
}


@dataclass(frozen=True, slots=True)
class Candidate:
    name: str
    semantic_path: tuple[int, ...]
    context_tokens: tuple[int, ...]
    evidence: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class ContextWorld:
    seed: int
    world_type: str
    candidates: tuple[Candidate, ...]
    excitation: tuple[tuple[int, int, float], ...]
    inhibition: tuple[tuple[int, int, float], ...]
    correct_index: int
    initial_cue: tuple[int, ...]
    late_cue: tuple[int, ...] | None


@dataclass(frozen=True, slots=True)
class LearnedParameters:
    """Identity-free training result retained for held-out inference."""

    evidence_resistance: tuple[float, ...]
    context_gains: tuple[float, ...]
    context_order: tuple[int, ...]

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
class TaperResult:
    activation: tuple[float, ...]
    active_counts: tuple[int, ...]
    context_feature_evaluations: int


@dataclass(frozen=True, slots=True)
class ConditionResult:
    correct: bool
    committed: bool
    good_behavior: bool
    correct_entered_recurrence: bool
    recurrent_candidate_cycles: int
    context_feature_evaluations: int
    post_taper_active_proxy: int
    initial_reversal_suppressed: bool | None
    reversal_reactivated: bool | None


@dataclass(frozen=True, slots=True)
class ConditionSummary:
    episodes: int
    correct_rate: float
    commit_rate: float
    good_behavior_rate: float
    correct_entered_recurrence_rate: float
    mean_recurrent_candidate_cycles: float
    mean_context_feature_evaluations: float
    mean_post_taper_active_proxy: float
    reversal_suppression_cases: int
    reversal_reactivation_rate: float | None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _clamp(value: float, lower: float = 0.0, upper: float = 1.6) -> float:
    return min(upper, max(lower, value))


def _normalize(values: list[float]) -> list[float]:
    total = sum(values)
    if total <= 0.0:
        return [1.0 / len(values) for _ in values]
    return [value / total for value in values]


def _stable_prefix_seed(prefix: tuple[int, ...], size: int) -> int:
    value = 2_166_136_261
    for item in prefix:
        value ^= (item + 1) * 16_777_619
        value = (value * 16_777_619) & 0xFFFFFFFF
    return value + size * 104_729


def _prefix_permutation(prefix: tuple[int, ...], size: int) -> tuple[int, ...]:
    rng = random.Random(_stable_prefix_seed(prefix, size))
    values = list(range(size))
    rng.shuffle(values)
    return tuple(values)


def _encode_child(prefix: tuple[int, ...], child: int, size: int) -> int:
    return _prefix_permutation(prefix, size)[child]


def _depth_tokens(path: tuple[int, ...]) -> tuple[int, ...]:
    values = [path[0]]
    for depth in range(1, len(path)):
        values.append(
            _encode_child(path[:depth], path[depth], LEVEL_SIZES[depth])
        )
    return tuple(values)


def _channel_tokens(path: tuple[int, ...]) -> tuple[int, ...]:
    depth_tokens = _depth_tokens(path)
    return tuple(depth_tokens[depth] for depth in CHANNEL_TO_DEPTH)


def _opaque_names(seed: int, count: int, rename_seed: int | None) -> list[str]:
    rng = random.Random(
        seed + 2_700_001 if rename_seed is None else rename_seed
    )
    tokens = rng.sample(range(100_000, 999_999), count)
    return [f"h{token}" for token in tokens]


def _random_path(rng: random.Random) -> tuple[int, ...]:
    return tuple(rng.randrange(size) for size in LEVEL_SIZES)


def _alias_pool(
    true_path: tuple[int, ...],
    true_tokens: tuple[int, ...],
) -> list[tuple[int, ...]]:
    """Find wrong-root paths whose deeper raw context tokens alias the true path."""

    root_depth = 0
    root_channel = DEPTH_TO_CHANNEL[root_depth]
    scored: list[tuple[int, tuple[int, ...]]] = []

    for wrong_root in range(LEVEL_SIZES[0]):
        if wrong_root == true_path[0]:
            continue
        for tail in itertools.product(
            range(LEVEL_SIZES[1]),
            range(LEVEL_SIZES[2]),
            range(LEVEL_SIZES[3]),
        ):
            path = (wrong_root, *tail)
            tokens = _channel_tokens(path)
            deep_matches = sum(
                1
                for channel, depth in enumerate(CHANNEL_TO_DEPTH)
                if depth > 0 and tokens[channel] == true_tokens[channel]
            )
            root_matches = tokens[root_channel] == true_tokens[root_channel]
            if root_matches:
                continue
            scored.append((deep_matches, path))

    scored.sort(key=lambda item: (-item[0], item[1]))
    return [path for _, path in scored]


def _build_relations(
    world_type: str,
    *,
    correct: int,
    allies: tuple[int, int],
    alias_indices: tuple[int, ...],
    rival: int | None,
) -> tuple[tuple[tuple[int, int, float], ...], tuple[tuple[int, int, float], ...]]:
    excitation: list[tuple[int, int, float]] = []
    inhibition: list[tuple[int, int, float]] = []

    coherent = {correct, *allies}
    if rival is not None:
        coherent.add(rival)

    for source in coherent:
        for target in coherent:
            if source == target:
                excitation.append((source, target, 0.04))
                continue
            weight = 0.44
            if target == correct and world_type != "unresolved_branch":
                weight += 0.07
            excitation.append((source, target, weight))

    for member in coherent:
        for alias in alias_indices[:7]:
            inhibition.append((member, alias, 0.24))
            inhibition.append((alias, member, 0.24))

    return tuple(excitation), tuple(inhibition)


def generate_world(
    seed: int,
    *,
    candidate_count: int = DEFAULT_CANDIDATE_COUNT,
    rename_seed: int | None = None,
) -> ContextWorld:
    if candidate_count < 96:
        raise ValueError("candidate_count must be at least 96")

    rng = random.Random(seed)
    world_type = WORLD_TYPES[seed % len(WORLD_TYPES)]
    true_path = _random_path(rng)
    true_tokens = _channel_tokens(true_path)

    paths: list[tuple[int, ...]] = [true_path, true_path, true_path]
    aliases = _alias_pool(true_path, true_tokens)
    alias_paths = aliases[:32]
    if world_type == "context_reversal":
        reversal_path = alias_paths[0]
        alias_paths = [reversal_path] * 20 + alias_paths[1:13]
    alias_start = len(paths)
    paths.extend(alias_paths)
    alias_indices = tuple(range(alias_start, alias_start + len(alias_paths)))

    rival: int | None = None
    if world_type == "unresolved_branch":
        rival = len(paths)
        paths.append(true_path)

    seen = set(paths)
    while len(paths) < candidate_count:
        path = _random_path(rng)
        if path in seen:
            continue
        seen.add(path)
        paths.append(path)

    names = _opaque_names(seed, candidate_count, rename_seed)
    root_channel = DEPTH_TO_CHANNEL[0]
    deepest_channel = DEPTH_TO_CHANNEL[3]
    candidates: list[Candidate] = []

    for index, path in enumerate(paths):
        tokens = _channel_tokens(path)
        matches = [
            1.0 if tokens[channel] == true_tokens[channel] else 0.0
            for channel in range(4)
        ]

        evidence: list[float] = []
        for channel, depth in enumerate(CHANNEL_TO_DEPTH):
            value = (
                0.18
                + 0.42 * matches[channel]
                + rng.uniform(-0.06, 0.06)
            )
            if depth >= 2:
                value += 0.10 * matches[channel]
            evidence.append(value)

        if index == 0:
            evidence[root_channel] += 0.10
            evidence = [value + 0.03 for value in evidence]
        elif index in (1, 2):
            evidence[root_channel] += 0.04
        elif index in alias_indices:
            alias_bonus = 0.10
            if world_type == "alias_conflict":
                alias_bonus = 0.18
            elif world_type == "misleading_deep":
                alias_bonus = 0.22
            elif world_type == "context_reversal":
                alias_bonus = 0.30

            for channel, depth in enumerate(CHANNEL_TO_DEPTH):
                if depth > 0:
                    evidence[channel] += alias_bonus
            if world_type == "misleading_deep":
                evidence[deepest_channel] += 0.20

        candidates.append(
            Candidate(
                name=names[index],
                semantic_path=path,
                context_tokens=tokens,
                evidence=tuple(_clamp(value) for value in evidence),
            )
        )

    if rival is not None:
        correct_evidence = candidates[0].evidence
        candidates[rival] = Candidate(
            name=names[rival],
            semantic_path=true_path,
            context_tokens=true_tokens,
            evidence=tuple(
                _clamp(value + rng.uniform(-0.004, 0.004))
                for value in correct_evidence
            ),
        )

    excitation, inhibition = _build_relations(
        world_type,
        correct=0,
        allies=(1, 2),
        alias_indices=alias_indices,
        rival=rival,
    )

    if world_type == "context_reversal":
        reversal_path = alias_paths[0]
        initial_cue = _channel_tokens(reversal_path)
        late_cue = true_tokens
    else:
        initial_cue = true_tokens
        late_cue = None

    return ContextWorld(
        seed=seed,
        world_type=world_type,
        candidates=tuple(candidates),
        excitation=excitation,
        inhibition=inhibition,
        correct_index=0,
        initial_cue=initial_cue,
        late_cue=late_cue,
    )


def _context_match(
    candidate: Candidate,
    channel: int,
    cue: tuple[int, ...],
) -> float:
    return 1.0 if candidate.context_tokens[channel] == cue[channel] else 0.0


def learn_parameters(
    training_seeds: Iterable[int] = TRAIN_SEEDS,
) -> LearnedParameters:
    resistance = [1.0, 1.0, 1.0, 1.0]
    utility_sums = [0.0, 0.0, 0.0, 0.0]
    episodes = 0

    for seed in training_seeds:
        world = generate_world(seed)
        episodes += 1
        final_cue = world.late_cue or world.initial_cue

        for channel in range(4):
            correct_support = world.candidates[world.correct_index].evidence[channel]
            strongest_wrong = max(
                candidate.evidence[channel]
                for index, candidate in enumerate(world.candidates)
                if index != world.correct_index
            )
            resistance[channel] = _clamp(
                resistance[channel]
                + 0.025 * (strongest_wrong - correct_support),
                0.25,
                3.0,
            )

            matches = [
                _context_match(candidate, channel, final_cue)
                for candidate in world.candidates
            ]
            utility_sums[channel] += (
                matches[world.correct_index] - mean(matches)
            )

    if episodes == 0:
        raise ValueError("at least one training world is required")

    utility = [value / episodes for value in utility_sums]
    average_utility = mean(utility)
    if average_utility <= 0.0:
        raise ValueError("training did not produce positive context utility")

    gains = tuple(value / average_utility for value in utility)
    order = tuple(
        sorted(range(4), key=lambda channel: utility[channel], reverse=True)
    )

    return LearnedParameters(
        evidence_resistance=tuple(resistance),
        context_gains=gains,
        context_order=order,
    )


def _front_end_base(world: ContextWorld) -> list[float]:
    values = [mean(candidate.evidence) for candidate in world.candidates]
    maximum = max(values)
    return _normalize(
        [math.exp((value - maximum) / 0.24) for value in values]
    )


def _choose_sparse_active(
    activation: list[float],
    *,
    minimum: int,
) -> set[int]:
    maximum = max(activation)
    eligible = {
        index
        for index, value in enumerate(activation)
        if value >= maximum * SPARSE_RELATIVE_GATE
    }
    if len(eligible) >= minimum:
        return eligible
    return set(
        sorted(
            range(len(activation)),
            key=lambda index: activation[index],
            reverse=True,
        )[:minimum]
    )


def sparse_context_cascade(
    world: ContextWorld,
    parameters: LearnedParameters,
    cue: tuple[int, ...],
    *,
    order: tuple[int, ...] | None = None,
) -> TaperResult:
    """Run reversible sparse stages; dormant candidates are preserved, not deleted."""

    stage_order = parameters.context_order if order is None else order
    activation = _front_end_base(world)
    active = set(range(len(activation)))
    evaluations = 0
    active_counts: list[int] = []

    for channel in stage_order:
        for _ in range(SPARSE_STAGE_CYCLES):
            raw = list(activation)
            for index in active:
                evaluations += 1
                raw[index] = (
                    activation[index] ** 0.90
                ) * math.exp(
                    parameters.context_gains[channel]
                    * _context_match(
                        world.candidates[index],
                        channel,
                        cue,
                    )
                    / 0.62
                )
            activation = _normalize(raw)

        active = _choose_sparse_active(
            activation,
            minimum=DEFAULT_RECURRENCE_WIDTH,
        )
        active_counts.append(len(active))

    return TaperResult(
        activation=tuple(activation),
        active_counts=tuple(active_counts),
        context_feature_evaluations=evaluations,
    )


def generic_soft_taper(
    world: ContextWorld,
    parameters: LearnedParameters,
    cue: tuple[int, ...],
) -> TaperResult:
    """Strong simultaneous control using all learned context gains every cycle."""

    activation = _front_end_base(world)
    evaluations = 0
    gain_total = sum(parameters.context_gains)

    for _ in range(GENERIC_CYCLES):
        previous = activation
        raw: list[float] = []

        for index, candidate in enumerate(world.candidates):
            score = 0.0
            for channel in range(4):
                evaluations += 1
                score += (
                    parameters.context_gains[channel]
                    * _context_match(candidate, channel, cue)
                )
            score /= gain_total
            raw.append(
                (previous[index] ** 0.90)
                * math.exp(score / 0.62)
            )

        activation = _normalize(raw)
        if sum(
            abs(new - old)
            for new, old in zip(activation, previous)
        ) < 0.004:
            break

    maximum = max(activation)
    active_proxy = sum(
        1
        for value in activation
        if value >= maximum * SPARSE_RELATIVE_GATE
    )

    return TaperResult(
        activation=tuple(activation),
        active_counts=(active_proxy,),
        context_feature_evaluations=evaluations,
    )


def _conductance(
    resistance: tuple[float, ...],
) -> tuple[float, ...]:
    inverse = [1.0 / value for value in resistance]
    average = mean(inverse)
    return tuple(value / average for value in inverse)


def _relation_maps(
    world: ContextWorld,
) -> tuple[dict[tuple[int, int], float], dict[tuple[int, int], float]]:
    excitation = {
        (source, target): weight
        for source, target, weight in world.excitation
    }
    inhibition = {
        (source, target): weight
        for source, target, weight in world.inhibition
    }
    return excitation, inhibition


def recurrent_solve(
    world: ContextWorld,
    activation: list[float] | tuple[float, ...],
    parameters: LearnedParameters,
    *,
    width: int,
    cycles: int = DEFAULT_RECURRENCE_CYCLES,
    resistance_override: tuple[float, ...] | None = None,
) -> SolveResult:
    """Identical relation-field solver; never consults world.correct_index."""

    if not 2 <= width <= len(activation):
        raise ValueError("invalid recurrence width")

    selected = tuple(
        sorted(
            range(len(activation)),
            key=lambda index: activation[index],
            reverse=True,
        )[:width]
    )
    maximum = max(activation[index] for index in selected) or 1.0
    state = {
        index: activation[index] / maximum
        for index in selected
    }

    resistance = (
        parameters.evidence_resistance
        if resistance_override is None
        else resistance_override
    )
    conductance = _conductance(resistance)
    evidence = {
        index: mean(
            value * gain
            for value, gain in zip(
                world.candidates[index].evidence,
                conductance,
            )
        )
        for index in selected
    }

    excitation, inhibition = _relation_maps(world)
    relation_sources = {
        source
        for source, _, _ in (*world.excitation, *world.inhibition)
        if source in selected
    }

    stability = 1.0
    for _ in range(cycles):
        raw: dict[int, float] = {}

        for index in selected:
            excite = sum(
                excitation.get((source, index), 0.0) * state[source]
                for source in relation_sources
            )
            inhibit = sum(
                inhibition.get((source, index), 0.0) * state[source]
                for source in relation_sources
            )
            raw[index] = max(
                0.0,
                0.28 * state[index]
                + 0.72 * excite
                - 0.65 * inhibit
                + 0.34 * evidence[index]
                + 0.12 * (activation[index] / maximum),
            )

        raw_maximum = max(raw.values()) or 1.0
        next_state = {
            index: value / raw_maximum
            for index, value in raw.items()
        }
        stability = sum(
            abs(next_state[index] - state[index])
            for index in selected
        )
        state = next_state

    ranked = sorted(
        selected,
        key=lambda index: state[index],
        reverse=True,
    )
    gap = state[ranked[0]] - state[ranked[1]]
    committed = gap >= 0.03 and stability <= 0.03

    return SolveResult(
        winner_index=ranked[0],
        confidence_gap=gap,
        stability_delta=stability,
        selected=selected,
        committed=committed,
    )


def static_solve(
    activation: list[float] | tuple[float, ...],
    *,
    width: int,
) -> SolveResult:
    selected = tuple(
        sorted(
            range(len(activation)),
            key=lambda index: activation[index],
            reverse=True,
        )[:width]
    )
    maximum = activation[selected[0]] or 1.0
    ranked = sorted(
        selected,
        key=lambda index: activation[index],
        reverse=True,
    )
    gap = (
        activation[ranked[0]] - activation[ranked[1]]
    ) / maximum
    return SolveResult(
        winner_index=ranked[0],
        confidence_gap=gap,
        stability_delta=0.0,
        selected=selected,
        committed=gap >= 0.08,
    )


def _good_behavior(
    world: ContextWorld,
    result: SolveResult,
) -> bool:
    if world.world_type == "unresolved_branch":
        return not result.committed
    return (
        result.committed
        and result.winner_index == world.correct_index
    )


def _active_proxy(
    activation: list[float] | tuple[float, ...],
) -> int:
    maximum = max(activation)
    return sum(
        1
        for value in activation
        if value >= maximum * SPARSE_RELATIVE_GATE
    )


def _run_taper(
    world: ContextWorld,
    parameters: LearnedParameters,
    condition: str,
    cue: tuple[int, ...],
) -> TaperResult:
    if condition == "generic_soft":
        return generic_soft_taper(world, parameters, cue)

    if condition in (
        "learned_order_sparse",
        "learned_order_no_resistance",
        "learned_order_no_recurrence",
    ):
        return sparse_context_cascade(world, parameters, cue)

    if condition == "fixed_order_sparse":
        return sparse_context_cascade(
            world,
            parameters,
            cue,
            order=(0, 1, 2, 3),
        )

    raise ValueError(f"condition has no taper helper: {condition}")


def _solve_for_condition(
    world: ContextWorld,
    activation: tuple[float, ...] | list[float],
    parameters: LearnedParameters,
    condition: str,
    *,
    width: int,
) -> SolveResult:
    if condition == "learned_order_no_recurrence":
        return static_solve(activation, width=width)

    resistance_override = (
        (1.0, 1.0, 1.0, 1.0)
        if condition == "learned_order_no_resistance"
        else None
    )
    return recurrent_solve(
        world,
        activation,
        parameters,
        width=width,
        resistance_override=resistance_override,
    )


def run_condition(
    world: ContextWorld,
    parameters: LearnedParameters,
    condition: str,
) -> ConditionResult:
    context_evaluations = 0
    initial_suppressed: bool | None = None
    reactivated: bool | None = None

    if condition == "no_taper":
        activation = tuple(_front_end_base(world))
        initial = recurrent_solve(
            world,
            activation,
            parameters,
            width=len(activation),
        )
        final = initial
        recurrent_cost = (
            len(activation) * DEFAULT_RECURRENCE_CYCLES
        )
        post_taper_active = len(activation)

    elif condition == "hard_topk":
        base = _front_end_base(world)
        gain_total = sum(parameters.context_gains)
        global_scores: list[float] = []
        for index, candidate in enumerate(world.candidates):
            context_score = 0.0
            for channel in range(4):
                context_evaluations += 1
                context_score += (
                    parameters.context_gains[channel]
                    * _context_match(
                        candidate,
                        channel,
                        world.initial_cue,
                    )
                )
            context_score /= gain_total
            global_scores.append(
                math.log(base[index] + 1e-12)
                + 2.4 * context_score
            )

        keep = tuple(
            sorted(
                range(len(global_scores)),
                key=lambda index: global_scores[index],
                reverse=True,
            )[:DEFAULT_RECURRENCE_WIDTH]
        )
        score_maximum = max(global_scores[index] for index in keep)
        exponentials = {
            index: math.exp(
                (global_scores[index] - score_maximum) / 0.62
            )
            for index in keep
        }
        denominator = sum(exponentials.values())
        activation = [0.0 for _ in world.candidates]
        for index, value in exponentials.items():
            activation[index] = value / denominator

        initial = recurrent_solve(
            world,
            activation,
            parameters,
            width=DEFAULT_RECURRENCE_WIDTH,
        )
        final = initial

        if world.late_cue is not None:
            initial_suppressed = world.correct_index not in keep
            # The hard condition may rescore only the candidates it retained.
            rescored: list[tuple[int, float]] = []
            gain_total = sum(parameters.context_gains)
            for index in keep:
                score = 0.0
                for channel in range(4):
                    context_evaluations += 1
                    score += (
                        parameters.context_gains[channel]
                        * _context_match(
                            world.candidates[index],
                            channel,
                            world.late_cue,
                        )
                    )
                rescored.append((index, score / gain_total))

            maximum_score = max(score for _, score in rescored)
            activation = [0.0 for _ in world.candidates]
            exponentials = {
                index: math.exp((score - maximum_score) / 0.62)
                for index, score in rescored
            }
            total = sum(exponentials.values())
            for index, value in exponentials.items():
                activation[index] = value / total

            final = recurrent_solve(
                world,
                activation,
                parameters,
                width=DEFAULT_RECURRENCE_WIDTH,
            )
            if initial_suppressed:
                reactivated = False

        recurrent_cost = (
            DEFAULT_RECURRENCE_WIDTH
            * DEFAULT_RECURRENCE_CYCLES
        )
        post_taper_active = DEFAULT_RECURRENCE_WIDTH

    else:
        taper = _run_taper(
            world,
            parameters,
            condition,
            world.initial_cue,
        )
        context_evaluations += taper.context_feature_evaluations
        activation = taper.activation
        initial = _solve_for_condition(
            world,
            activation,
            parameters,
            condition,
            width=DEFAULT_RECURRENCE_WIDTH,
        )
        final = initial

        if world.late_cue is not None:
            initial_suppressed = (
                world.correct_index not in initial.selected
            )
            reopened = _run_taper(
                world,
                parameters,
                condition,
                world.late_cue,
            )
            context_evaluations += (
                reopened.context_feature_evaluations
            )
            activation = reopened.activation
            final = _solve_for_condition(
                world,
                activation,
                parameters,
                condition,
                width=DEFAULT_RECURRENCE_WIDTH,
            )

            if initial_suppressed:
                reactivated = (
                    world.correct_index in final.selected
                    and final.winner_index == world.correct_index
                )

        recurrent_cost = (
            0
            if condition == "learned_order_no_recurrence"
            else (
                DEFAULT_RECURRENCE_WIDTH
                * DEFAULT_RECURRENCE_CYCLES
            )
        )
        post_taper_active = _active_proxy(activation)

    correct = final.winner_index == world.correct_index
    return ConditionResult(
        correct=correct,
        committed=final.committed,
        good_behavior=_good_behavior(world, final),
        correct_entered_recurrence=(
            world.correct_index in final.selected
        ),
        recurrent_candidate_cycles=recurrent_cost,
        context_feature_evaluations=context_evaluations,
        post_taper_active_proxy=post_taper_active,
        initial_reversal_suppressed=initial_suppressed,
        reversal_reactivated=reactivated,
    )


def _summarize(rows: list[ConditionResult]) -> ConditionSummary:
    suppression_rows = [
        row
        for row in rows
        if row.initial_reversal_suppressed is True
    ]
    reactivation_rows = [
        row
        for row in suppression_rows
        if row.reversal_reactivated is not None
    ]

    return ConditionSummary(
        episodes=len(rows),
        correct_rate=mean(
            1.0 if row.correct else 0.0
            for row in rows
        ),
        commit_rate=mean(
            1.0 if row.committed else 0.0
            for row in rows
        ),
        good_behavior_rate=mean(
            1.0 if row.good_behavior else 0.0
            for row in rows
        ),
        correct_entered_recurrence_rate=mean(
            1.0 if row.correct_entered_recurrence else 0.0
            for row in rows
        ),
        mean_recurrent_candidate_cycles=mean(
            row.recurrent_candidate_cycles
            for row in rows
        ),
        mean_context_feature_evaluations=mean(
            row.context_feature_evaluations
            for row in rows
        ),
        mean_post_taper_active_proxy=mean(
            row.post_taper_active_proxy
            for row in rows
        ),
        reversal_suppression_cases=len(suppression_rows),
        reversal_reactivation_rate=(
            mean(
                1.0 if row.reversal_reactivated else 0.0
                for row in reactivation_rows
            )
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
    rows_by_type: dict[
        str, dict[str, list[ConditionResult]]
    ] = {
        condition: {
            world_type: []
            for world_type in WORLD_TYPES
        }
        for condition in CONDITIONS
    }

    for seed in seeds:
        world = generate_world(
            seed,
            candidate_count=candidate_count,
            rename_seed=(
                seed + rename_offset
                if rename_offset is not None
                else None
            ),
        )
        for condition in CONDITIONS:
            result = run_condition(
                world,
                parameters,
                condition,
            )
            rows_by_condition[condition].append(result)
            rows_by_type[condition][world.world_type].append(
                result
            )

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


def _metric(
    bundle: dict[str, object],
    condition: str,
    metric: str,
) -> float:
    conditions = bundle["conditions"]
    assert isinstance(conditions, dict)
    summary = conditions[condition]
    assert isinstance(summary, dict)
    value = summary[metric]
    if not isinstance(value, (int, float)):
        raise TypeError(
            f"metric {condition}.{metric} is unavailable"
        )
    return float(value)


def _optional_metric(
    bundle: dict[str, object],
    condition: str,
    metric: str,
) -> float | None:
    conditions = bundle["conditions"]
    assert isinstance(conditions, dict)
    summary = conditions[condition]
    assert isinstance(summary, dict)
    value = summary[metric]
    if value is None:
        return None
    if not isinstance(value, (int, float)):
        raise TypeError(
            f"metric {condition}.{metric} is invalid"
        )
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
        raise TypeError(
            f"metric {condition}.{world_type}.{metric} "
            "is unavailable"
        )
    return float(value)


def verdict(
    held_out: dict[str, object],
    renamed: dict[str, object],
    parameters: LearnedParameters,
) -> tuple[str, dict[str, bool | float | None | list[int]]]:
    learned_good = _metric(
        held_out,
        "learned_order_sparse",
        "good_behavior_rate",
    )
    learned_survival = _metric(
        held_out,
        "learned_order_sparse",
        "correct_entered_recurrence_rate",
    )
    unresolved_commit = _type_metric(
        held_out,
        "learned_order_sparse",
        "unresolved_branch",
        "commit_rate",
    )
    suppression_cases = _metric(
        held_out,
        "learned_order_sparse",
        "reversal_suppression_cases",
    )
    learned_reactivation = _optional_metric(
        held_out,
        "learned_order_sparse",
        "reversal_reactivation_rate",
    )
    hard_reactivation = _optional_metric(
        held_out,
        "hard_topk",
        "reversal_reactivation_rate",
    )

    learned_recurrent_cost = _metric(
        held_out,
        "learned_order_sparse",
        "mean_recurrent_candidate_cycles",
    )
    no_taper_recurrent_cost = _metric(
        held_out,
        "no_taper",
        "mean_recurrent_candidate_cycles",
    )
    recurrent_fraction = (
        learned_recurrent_cost / no_taper_recurrent_cost
    )

    generic_good = _metric(
        held_out,
        "generic_soft",
        "good_behavior_rate",
    )
    generic_advantage = generic_good - learned_good

    learned_context_evals = _metric(
        held_out,
        "learned_order_sparse",
        "mean_context_feature_evaluations",
    )
    generic_context_evals = _metric(
        held_out,
        "generic_soft",
        "mean_context_feature_evaluations",
    )
    context_eval_fraction = (
        learned_context_evals / generic_context_evals
        if generic_context_evals > 0.0
        else float("inf")
    )

    fixed_context_evals = _metric(
        held_out,
        "fixed_order_sparse",
        "mean_context_feature_evaluations",
    )
    order_efficiency_advantage = (
        (fixed_context_evals - learned_context_evals)
        / fixed_context_evals
        if fixed_context_evals > 0.0
        else 0.0
    )

    renamed_good = _metric(
        renamed,
        "learned_order_sparse",
        "good_behavior_rate",
    )
    renaming_retention = (
        renamed_good / learned_good
        if learned_good > 0.0
        else 0.0
    )

    learned_reactivation_value = (
        learned_reactivation
        if learned_reactivation is not None
        else 0.0
    )
    hard_reactivation_value = (
        hard_reactivation
        if hard_reactivation is not None
        else 0.0
    )
    reversal_exercised = (
        suppression_cases
        >= GATE["reversal_suppression_cases_min"]
        and learned_reactivation is not None
        and hard_reactivation is not None
    )

    learned_order_depths = [
        CHANNEL_TO_DEPTH[channel]
        for channel in parameters.context_order
    ]
    learned_hierarchical_order = (
        learned_order_depths == [0, 1, 2, 3]
    )

    checks: dict[
        str, bool | float | None | list[int]
    ] = {
        "learned_good_behavior": learned_good,
        "learned_good_behavior_pass": (
            learned_good
            >= GATE["learned_good_behavior_min"]
        ),
        "learned_final_survival": learned_survival,
        "learned_final_survival_pass": (
            learned_survival
            >= GATE["learned_final_survival_min"]
        ),
        "unresolved_commit_rate": unresolved_commit,
        "unresolved_commit_rate_pass": (
            unresolved_commit
            <= GATE["unresolved_commit_rate_max"]
        ),
        "reversal_suppression_cases": suppression_cases,
        "reversal_exercised_pass": reversal_exercised,
        "learned_reactivation": learned_reactivation,
        "learned_reactivation_pass": (
            reversal_exercised
            and learned_reactivation_value
            >= GATE["learned_reactivation_min"]
        ),
        "hard_reactivation": hard_reactivation,
        "hard_reactivation_disadvantage": (
            learned_reactivation_value
            - hard_reactivation_value
        ),
        "hard_reactivation_disadvantage_pass": (
            reversal_exercised
            and (
                learned_reactivation_value
                - hard_reactivation_value
            )
            >= GATE[
                "hard_reactivation_disadvantage_min"
            ]
        ),
        "recurrent_cost_fraction": recurrent_fraction,
        "recurrent_cost_fraction_pass": (
            recurrent_fraction
            <= GATE["recurrent_cost_fraction_max"]
        ),
        "renaming_retention": renaming_retention,
        "renaming_retention_pass": (
            renaming_retention
            >= GATE["renaming_retention_min"]
        ),
        "generic_behavior_advantage": generic_advantage,
        "generic_behavior_advantage_pass": (
            generic_advantage
            <= GATE["generic_behavior_advantage_max"]
        ),
        "context_eval_fraction_vs_generic": (
            context_eval_fraction
        ),
        "context_eval_fraction_vs_generic_pass": (
            context_eval_fraction
            <= GATE[
                "context_eval_fraction_vs_generic_max"
            ]
        ),
        "learned_order_efficiency_advantage": (
            order_efficiency_advantage
        ),
        "learned_order_efficiency_advantage_pass": (
            order_efficiency_advantage
            >= GATE[
                "learned_order_efficiency_advantage_min"
            ]
        ),
        "learned_order_depths": learned_order_depths,
        "learned_hierarchical_order_pass": (
            learned_hierarchical_order
        ),
    }

    if not reversal_exercised:
        return (
            "INCONCLUSIVE: HCT-2 did not exercise enough "
            "reversible-suppression cases.",
            checks,
        )

    pass_flags = [
        value
        for key, value in checks.items()
        if key.endswith("_pass") and isinstance(value, bool)
    ]
    if all(pass_flags):
        return (
            "REINFORCED: HCT-2 v1 passed every frozen "
            "ordered-context criterion.",
            checks,
        )

    failed = [
        key
        for key, value in checks.items()
        if key.endswith("_pass") and value is False
    ]
    return (
        "DISCOUNTED: HCT-2 v1 failed frozen criteria: "
        + ", ".join(failed),
        checks,
    )


def _seeds_for_split(split: str) -> range:
    if split == "quick":
        return QUICK_DEVELOPMENT_SEEDS
    if split == "development":
        return DEVELOPMENT_SEEDS
    if split == "final":
        return FINAL_SEEDS
    raise ValueError(f"unknown split: {split}")


def run_assay(*, split: str = "final") -> dict[str, object]:
    parameters = learn_parameters(TRAIN_SEEDS)
    seeds = _seeds_for_split(split)

    held_out = evaluate(
        seeds,
        parameters=parameters,
    )
    renamed = evaluate(
        seeds,
        parameters=parameters,
        rename_offset=2_300_000,
    )
    decision, checks = verdict(
        held_out,
        renamed,
        parameters,
    )

    return {
        "experiment": EXPERIMENT_ID,
        "hypothesis": HYPOTHESIS_ID,
        "split": split,
        "question": (
            "Do learned ordered reversible sparse context stages "
            "preserve behavior while reducing context evaluation "
            "cost in hierarchically aliased worlds better than "
            "simultaneous generic soft weighting or fixed-order "
            "sparse settling?"
        ),
        "candidate_count": DEFAULT_CANDIDATE_COUNT,
        "recurrence_width": DEFAULT_RECURRENCE_WIDTH,
        "training_seed_range": [
            TRAIN_SEEDS.start,
            TRAIN_SEEDS.stop - 1,
        ],
        "development_seed_range": [
            DEVELOPMENT_SEEDS.start,
            DEVELOPMENT_SEEDS.stop - 1,
        ],
        "evaluation_seed_range": [
            seeds.start,
            seeds.stop - 1,
        ],
        "final_seed_range_reserved": [
            FINAL_SEEDS.start,
            FINAL_SEEDS.stop - 1,
        ],
        "learned_parameters": parameters.to_dict(),
        "learned_order_depths": [
            CHANNEL_TO_DEPTH[channel]
            for channel in parameters.context_order
        ],
        "frozen_gate": dict(GATE),
        "held_out": held_out,
        "renamed_candidates": renamed,
        "checks": checks,
        "verdict": decision,
        "cost_note": (
            "Context-feature evaluations and recurrent candidate-"
            "cycles are reported separately. HCT-2 does not claim "
            "wall-clock superiority without an explicit calibrated "
            "cost model."
        ),
        "ablation_note": (
            "No-resistance and no-recurrence conditions are "
            "reported as mechanistic ablations. They are not forced "
            "to fail by the frozen primary gate."
        ),
        "scientific_boundary": (
            "Controlled synthetic evidence only. HCT-2 does not "
            "establish biological hippocampal equivalence, natural-"
            "language benefit, learned semantic representations, "
            "general intelligence, or production integration."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--quick",
        action="store_true",
        help=(
            "Use 50 development worlds. This never touches the "
            "reserved final split."
        ),
    )
    group.add_argument(
        "--development",
        action="store_true",
        help="Use the full development split.",
    )
    args = parser.parse_args()

    if args.quick:
        split = "quick"
    elif args.development:
        split = "development"
    else:
        split = "final"

    print(json.dumps(run_assay(split=split), indent=2))


if __name__ == "__main__":
    main()
