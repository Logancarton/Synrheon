from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
import random
from statistics import mean

from experiments.hippocampal_stateful_recurrence import StatefulWorld, one_pass, recurrent

EXPERIMENT_ID = "hippocampal-confidence-gated-sparsity-v2"
WORLD_TYPES = (
    "easy_clear",
    "delayed_clear",
    "persistent_close",
    "misleading_early",
    "unresolved_close",
)


@dataclass(frozen=True, slots=True)
class AdaptiveTrace:
    cycle: int
    keep_k: int
    gap: float
    stability_delta: float
    leader: str
    leader_correct: bool
    pruned: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class AdaptiveResult:
    winner: str
    confidence_gap: float
    traces: tuple[AdaptiveTrace, ...]
    first_prune_cycle: int | None
    prune_leader_correct: bool | None
    winner_reversed_after_prune: bool
    active_state_cost: int


@dataclass(frozen=True, slots=True)
class Summary:
    episodes: int
    accuracy: float
    mean_confidence_gap: float
    prune_rate: float
    correct_prune_rate: float
    false_prune_rate: float
    mean_first_prune_cycle: float
    never_pruned_rate: float
    winner_reversal_after_prune_rate: float
    mean_active_state_fraction: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _normalize(values: list[float]) -> list[float]:
    maximum = max(values)
    return [0.0 for _ in values] if maximum <= 0.0 else [value / maximum for value in values]


def _gap(values: list[float]) -> float:
    ranked = sorted(values, reverse=True)
    return ranked[0] - ranked[1]


def _delta(a: list[float], b: list[float]) -> float:
    return sum(abs(x - y) for x, y in zip(a, b))


def _opaque_names(seed: int, count: int, rename_seed: int | None) -> tuple[str, ...]:
    rng = random.Random(seed + 910_003 if rename_seed is None else rename_seed)
    labels = [f"m{index}_{rng.randrange(1000, 9999)}" for index in range(count)]
    rng.shuffle(labels)
    return tuple(labels)


def generate_mixed_world(seed: int, *, rename_seed: int | None = None) -> tuple[str, StatefulWorld]:
    """Generate one of five regimes that exercise the gating rule differently.

    The world family deliberately includes cases where pruning should happen, should
    wait, or should never happen. Candidate names are opaque and can be independently
    renamed without changing structure.
    """

    rng = random.Random(seed)
    world_type = WORLD_TYPES[seed % len(WORLD_TYPES)]
    n = 4
    correct = rng.randrange(3)
    lure = 3
    names = _opaque_names(seed, n, rename_seed)

    excitation = [[0.0 for _ in range(n)] for _ in range(n)]
    inhibition = [[0.0 for _ in range(n)] for _ in range(n)]

    if world_type == "easy_clear":
        initial = [rng.uniform(0.38, 0.48) for _ in range(n)]
        initial[correct] = rng.uniform(0.82, 0.90)
        excitation[correct][correct] = rng.uniform(0.36, 0.46)
        for idx in range(n):
            if idx != correct:
                inhibition[correct][idx] = rng.uniform(0.18, 0.26)

    elif world_type == "delayed_clear":
        initial = [rng.uniform(0.50, 0.58) for _ in range(3)] + [rng.uniform(0.72, 0.80)]
        initial[correct] += rng.uniform(0.04, 0.07)
        for source in range(3):
            for target in range(3):
                if source != target:
                    excitation[source][target] = rng.uniform(0.42, 0.54)
        for source in range(3):
            if source != correct:
                excitation[source][correct] += rng.uniform(0.10, 0.14)
        for idx in range(3):
            inhibition[idx][lure] = rng.uniform(0.34, 0.44)
            inhibition[lure][idx] = rng.uniform(0.24, 0.34)

    elif world_type == "persistent_close":
        rival = (correct + 1) % 3
        initial = [rng.uniform(0.52, 0.58) for _ in range(n)]
        initial[correct] = rng.uniform(0.60, 0.64)
        initial[rival] = rng.uniform(0.59, 0.63)
        for source in range(3):
            for target in range(3):
                if source != target:
                    excitation[source][target] = rng.uniform(0.34, 0.42)
        excitation[rival][correct] += rng.uniform(0.025, 0.045)
        excitation[correct][rival] += rng.uniform(0.015, 0.030)
        inhibition[correct][lure] = rng.uniform(0.18, 0.24)
        inhibition[rival][lure] = rng.uniform(0.18, 0.24)

    elif world_type == "misleading_early":
        initial = [rng.uniform(0.46, 0.54) for _ in range(3)] + [rng.uniform(0.86, 0.94)]
        initial[correct] += rng.uniform(0.03, 0.05)
        for source in range(3):
            for target in range(3):
                if source != target:
                    excitation[source][target] = rng.uniform(0.52, 0.64)
        for source in range(3):
            if source != correct:
                excitation[source][correct] += rng.uniform(0.08, 0.12)
        excitation[lure][lure] = rng.uniform(0.08, 0.14)
        for idx in range(3):
            inhibition[idx][lure] = rng.uniform(0.44, 0.56)
            inhibition[lure][idx] = rng.uniform(0.28, 0.38)

    else:  # unresolved_close
        rival = (correct + 1) % 3
        initial = [rng.uniform(0.50, 0.56) for _ in range(n)]
        initial[correct] = rng.uniform(0.61, 0.64)
        initial[rival] = rng.uniform(0.60, 0.635)
        for source in (correct, rival):
            excitation[source][correct] = rng.uniform(0.22, 0.28)
            excitation[source][rival] = rng.uniform(0.22, 0.28)
        # Tiny structural edge makes a final answer scoreable while intentionally
        # keeping the top pair close enough that a prudent gate should stay open.
        excitation[rival][correct] += rng.uniform(0.008, 0.016)
        for idx in range(n):
            if idx not in (correct, rival):
                inhibition[correct][idx] = rng.uniform(0.12, 0.18)
                inhibition[rival][idx] = rng.uniform(0.12, 0.18)

    return world_type, StatefulWorld(
        seed=seed,
        names=names,
        initial=tuple(initial),
        excitation=tuple(tuple(row) for row in excitation),
        inhibition=tuple(tuple(row) for row in inhibition),
        correct_index=correct,
    )


def adaptive_recurrent(
    world: StatefulWorld,
    *,
    cycles: int = 8,
    clear_gap: float = 0.15,
    stable_delta: float = 0.12,
    minimum_open_cycles: int = 2,
    collapsed_k: int = 2,
) -> AdaptiveResult:
    """Keep the field broad until the leader is both clear and dynamically stable."""

    a = _normalize(list(world.initial))
    n = len(a)
    keep_k = n
    first_prune: int | None = None
    prune_leader_correct: bool | None = None
    prune_leader_index: int | None = None
    traces: list[AdaptiveTrace] = []
    active_cost = n  # initial field

    for step in range(1, cycles + 1):
        raw: list[float] = []
        for i in range(n):
            excite = sum(world.excitation[j][i] * a[j] for j in range(n))
            inhibit = sum(world.inhibition[j][i] * a[j] for j in range(n))
            raw.append(max(0.0, 0.28 * a[i] + 0.78 * excite - 0.72 * inhibit + 0.22 * world.initial[i]))

        next_a = _normalize(raw)
        gap = _gap(next_a)
        stability = _delta(next_a, a)  # compare to the immediately prior recurrent state
        ranked = sorted(range(n), key=lambda idx: next_a[idx], reverse=True)
        leader = ranked[0]

        if first_prune is None and step >= minimum_open_cycles and gap >= clear_gap and stability <= stable_delta:
            keep_k = min(collapsed_k, n)
            first_prune = step
            prune_leader_index = leader
            prune_leader_correct = leader == world.correct_index

        survivors = set(ranked[:keep_k])
        pruned = tuple(world.names[idx] for idx in ranked[keep_k:])
        next_a = [value if idx in survivors else 0.0 for idx, value in enumerate(next_a)]
        active_cost += keep_k
        traces.append(
            AdaptiveTrace(
                cycle=step,
                keep_k=keep_k,
                gap=gap,
                stability_delta=stability,
                leader=world.names[leader],
                leader_correct=leader == world.correct_index,
                pruned=pruned,
            )
        )
        a = next_a

    ranked = sorted(range(n), key=lambda idx: a[idx], reverse=True)
    winner_index = ranked[0]
    return AdaptiveResult(
        winner=world.names[winner_index],
        confidence_gap=a[ranked[0]] - a[ranked[1]],
        traces=tuple(traces),
        first_prune_cycle=first_prune,
        prune_leader_correct=prune_leader_correct,
        winner_reversed_after_prune=(prune_leader_index is not None and winner_index != prune_leader_index),
        active_state_cost=active_cost,
    )


def _adaptive_summary(rows: list[tuple[bool, AdaptiveResult]], *, n: int = 4, cycles: int = 8) -> Summary:
    pruned = [result for _, result in rows if result.first_prune_cycle is not None]
    correct_prunes = [result for result in pruned if result.prune_leader_correct]
    false_prunes = [result for result in pruned if result.prune_leader_correct is False]
    full_cost = n * (cycles + 1)
    return Summary(
        episodes=len(rows),
        accuracy=mean(1.0 if ok else 0.0 for ok, _ in rows),
        mean_confidence_gap=mean(result.confidence_gap for _, result in rows),
        prune_rate=len(pruned) / len(rows),
        correct_prune_rate=len(correct_prunes) / len(rows),
        false_prune_rate=len(false_prunes) / len(rows),
        mean_first_prune_cycle=mean(result.first_prune_cycle for result in pruned) if pruned else 0.0,
        never_pruned_rate=1.0 - (len(pruned) / len(rows)),
        winner_reversal_after_prune_rate=(
            mean(1.0 if result.winner_reversed_after_prune else 0.0 for result in pruned) if pruned else 0.0
        ),
        mean_active_state_fraction=mean(result.active_state_cost / full_cost for _, result in rows),
    )


def _simple_summary(rows: list[tuple[bool, float]], *, active_fraction: float) -> Summary:
    return Summary(
        episodes=len(rows),
        accuracy=mean(1.0 if ok else 0.0 for ok, _ in rows),
        mean_confidence_gap=mean(gap for _, gap in rows),
        prune_rate=0.0,
        correct_prune_rate=0.0,
        false_prune_rate=0.0,
        mean_first_prune_cycle=0.0,
        never_pruned_rate=1.0,
        winner_reversal_after_prune_rate=0.0,
        mean_active_state_fraction=active_fraction,
    )


def evaluate(seeds: range, rename_offset: int | None = None) -> dict[str, object]:
    adaptive_rows: list[tuple[bool, AdaptiveResult]] = []
    fixed_rows: list[tuple[bool, float]] = []
    clock_rows: list[tuple[bool, float]] = []
    one_rows: list[tuple[bool, float]] = []
    by_type_rows: dict[str, list[tuple[bool, AdaptiveResult]]] = {kind: [] for kind in WORLD_TYPES}

    for seed in seeds:
        world_type, world = generate_mixed_world(
            seed,
            rename_seed=(seed + rename_offset) if rename_offset is not None else None,
        )
        adaptive = adaptive_recurrent(world)
        fixed = recurrent(world, progressive_sparsity=False)
        clock = recurrent(world, progressive_sparsity=True)
        first = one_pass(world)

        adaptive_ok = adaptive.winner == world.correct_name
        adaptive_rows.append((adaptive_ok, adaptive))
        by_type_rows[world_type].append((adaptive_ok, adaptive))
        fixed_rows.append((fixed.winner == world.correct_name, fixed.confidence_gap))
        clock_rows.append((clock.winner == world.correct_name, clock.confidence_gap))
        one_rows.append((first.winner == world.correct_name, first.confidence_gap))

    adaptive_summary = _adaptive_summary(adaptive_rows)
    fixed_summary = _simple_summary(fixed_rows, active_fraction=1.0)
    clock_summary = _simple_summary(clock_rows, active_fraction=(4 + 4 + 4 + 3 + 3 + 3 + 2 + 2 + 2) / 36)
    one_summary = _simple_summary(one_rows, active_fraction=4 / 36)

    return {
        "one_pass": one_summary,
        "clock_progressive": clock_summary,
        "fixed_width": fixed_summary,
        "confidence_gated": adaptive_summary,
        "by_world_type": {kind: _adaptive_summary(rows) for kind, rows in by_type_rows.items()},
        "active_state_savings_vs_fixed": 1.0 - adaptive_summary.mean_active_state_fraction,
    }


def verdict(bundle: dict[str, object]) -> str:
    adaptive = bundle["confidence_gated"]
    fixed = bundle["fixed_width"]
    by_type = bundle["by_world_type"]
    assert isinstance(adaptive, Summary) and isinstance(fixed, Summary) and isinstance(by_type, dict)

    easy = by_type["easy_clear"]
    delayed = by_type["delayed_clear"]
    close = by_type["persistent_close"]
    misleading = by_type["misleading_early"]
    unresolved = by_type["unresolved_close"]
    assert all(isinstance(item, Summary) for item in (easy, delayed, close, misleading, unresolved))

    # Inconclusive checks come first: do not call the theory reinforced if the
    # mechanism never actually exercises both pruning and non-pruning behavior.
    if adaptive.prune_rate < 0.20 or adaptive.prune_rate > 0.80:
        return "INCONCLUSIVE: the mixed assay did not exercise both prune and keep-open behavior sufficiently."
    if easy.prune_rate < 0.60:
        return "INCONCLUSIVE: clear worlds rarely triggered the zoom-in gate."
    if unresolved.never_pruned_rate < 0.60:
        return "DISCOUNTED: genuinely close worlds were collapsed too often."
    if misleading.false_prune_rate > 0.10:
        return "DISCOUNTED: the gate too often committed to misleading early leaders."
    if adaptive.accuracy < fixed.accuracy - 0.05:
        return "DISCOUNTED: adaptive pruning materially reduced recurrent accuracy."
    if adaptive.false_prune_rate <= 0.05 and adaptive.accuracy >= fixed.accuracy - 0.03 and bundle["active_state_savings_vs_fixed"] >= 0.10:
        return "REINFORCED: confidence/stability gating selectively prunes clear fields, preserves close calls, and reduces active-state cost without material accuracy loss."
    return "MIXED RESULT"


def _serialize(bundle: dict[str, object]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in bundle.items():
        if isinstance(value, Summary):
            result[key] = value.to_dict()
        elif isinstance(value, dict):
            result[key] = {subkey: subvalue.to_dict() if isinstance(subvalue, Summary) else subvalue for subkey, subvalue in value.items()}
        else:
            result[key] = value
    return result


def run_assay(*, quick: bool = False) -> dict[str, object]:
    seeds = range(30000, 30500) if quick else range(30000, 32500)
    held = evaluate(seeds)
    renamed = evaluate(seeds, 1_200_000)
    return {
        "experiment": EXPERIMENT_ID,
        "question": (
            "Can a confidence-and-stability gate learn when to keep recurrent alternatives alive and when to collapse the field, "
            "while preserving accuracy and reducing active-state computation across mixed difficulty regimes?"
        ),
        "gating_rule": {
            "minimum_open_cycles": 2,
            "clear_gap": 0.15,
            "stable_l1_delta": 0.12,
            "collapsed_k": 2,
        },
        "world_types": list(WORLD_TYPES),
        "held_out": _serialize(held),
        "renamed_candidates": _serialize(renamed),
        "verdict": verdict(held),
        "scientific_boundary": (
            "This remains a synthetic mixed-family gating assay. It tests selective commitment dynamics, not language grounding, "
            "learned representations, biological equivalence, or optimality against all conventional baselines."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run_assay(quick=args.quick), indent=2))


if __name__ == "__main__":
    main()
