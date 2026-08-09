from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
from statistics import mean

from experiments.hippocampal_stateful_recurrence import StatefulWorld, generate_world, one_pass, recurrent

EXPERIMENT_ID = "hippocampal-confidence-gated-sparsity-v1"

@dataclass(frozen=True, slots=True)
class AdaptiveTrace:
    cycle: int
    keep_k: int
    gap: float
    stability_delta: float
    pruned: tuple[str, ...]

@dataclass(frozen=True, slots=True)
class AdaptiveResult:
    winner: str
    confidence_gap: float
    traces: tuple[AdaptiveTrace, ...]
    first_prune_cycle: int | None

@dataclass(frozen=True, slots=True)
class Summary:
    episodes: int
    accuracy: float
    mean_confidence_gap: float
    mean_first_prune_cycle: float
    never_pruned_rate: float
    def to_dict(self) -> dict[str, object]:
        return asdict(self)

def _normalize(values: list[float]) -> list[float]:
    m = max(values)
    return [0.0 for _ in values] if m <= 0.0 else [v / m for v in values]

def _gap(values: list[float]) -> float:
    ranked = sorted(values, reverse=True)
    return ranked[0] - ranked[1]

def _delta(a: list[float], b: list[float]) -> float:
    return sum(abs(x-y) for x,y in zip(a,b))

def adaptive_recurrent(
    world: StatefulWorld,
    *,
    cycles: int = 8,
    clear_gap: float = 0.18,
    stable_delta: float = 0.10,
    minimum_open_cycles: int = 3,
    collapsed_k: int = 2,
) -> AdaptiveResult:
    a = _normalize(list(world.initial))
    previous = list(a)
    n = len(a)
    keep_k = n
    first_prune: int | None = None
    traces: list[AdaptiveTrace] = []

    for step in range(1, cycles + 1):
        raw: list[float] = []
        for i in range(n):
            excite = sum(world.excitation[j][i] * a[j] for j in range(n))
            inhibit = sum(world.inhibition[j][i] * a[j] for j in range(n))
            raw.append(max(0.0, 0.28*a[i] + 0.78*excite - 0.72*inhibit + 0.22*world.initial[i]))
        next_a = _normalize(raw)
        gap = _gap(next_a)
        stability = _delta(next_a, previous)
        if first_prune is None and step >= minimum_open_cycles and gap >= clear_gap and stability <= stable_delta:
            keep_k = min(collapsed_k, n)
            first_prune = step
        ranked = sorted(range(n), key=lambda idx: next_a[idx], reverse=True)
        survivors = set(ranked[:keep_k])
        pruned = tuple(world.names[idx] for idx in ranked[keep_k:])
        next_a = [v if idx in survivors else 0.0 for idx,v in enumerate(next_a)]
        traces.append(AdaptiveTrace(step, keep_k, gap, stability, pruned))
        previous = list(a)
        a = next_a

    ranked = sorted(range(n), key=lambda idx: a[idx], reverse=True)
    return AdaptiveResult(world.names[ranked[0]], a[ranked[0]]-a[ranked[1]], tuple(traces), first_prune)

def _summary(seeds: range, mode: str, rename_offset: int | None = None) -> Summary:
    rows: list[tuple[bool,float,int|None]] = []
    for seed in seeds:
        world = generate_world(seed, rename_seed=(seed+rename_offset) if rename_offset is not None else None)
        if mode == "adaptive":
            result = adaptive_recurrent(world)
            rows.append((result.winner == world.correct_name, result.confidence_gap, result.first_prune_cycle))
        elif mode == "fixed":
            result = recurrent(world, progressive_sparsity=False)
            rows.append((result.winner == world.correct_name, result.confidence_gap, None))
        elif mode == "progressive":
            result = recurrent(world, progressive_sparsity=True)
            rows.append((result.winner == world.correct_name, result.confidence_gap, None))
        else:
            result = one_pass(world)
            rows.append((result.winner == world.correct_name, result.confidence_gap, None))
    prune = [p for _,_,p in rows if p is not None]
    return Summary(len(rows), mean(1.0 if ok else 0.0 for ok,_,_ in rows), mean(g for _,g,_ in rows), mean(prune) if prune else 0.0, mean(1.0 if p is None else 0.0 for _,_,p in rows))

def evaluate(seeds: range, rename_offset: int | None = None) -> dict[str, Summary]:
    return {
        "one_pass": _summary(seeds, "one", rename_offset),
        "clock_progressive": _summary(seeds, "progressive", rename_offset),
        "fixed_width": _summary(seeds, "fixed", rename_offset),
        "confidence_gated": _summary(seeds, "adaptive", rename_offset),
    }

def verdict(bundle: dict[str, Summary]) -> str:
    a, f, p = bundle["confidence_gated"], bundle["fixed_width"], bundle["clock_progressive"]
    if a.accuracy >= 0.90 and a.accuracy >= f.accuracy - 0.05 and a.accuracy >= p.accuracy + 0.40:
        return "REINFORCED: adaptive gating preserves recurrent accuracy while avoiding premature pruning."
    if a.accuracy <= f.accuracy - 0.20:
        return "DISCOUNTED: adaptive collapse still removes useful states too early."
    if a.never_pruned_rate >= 0.95:
        return "INCONCLUSIVE: gating almost never activates and behaves like fixed width."
    return "MIXED RESULT"

def run_assay(*, quick: bool = False) -> dict[str, object]:
    seeds = range(20000,20200) if quick else range(20000,21000)
    held = evaluate(seeds)
    renamed = evaluate(seeds, 900000)
    return {
        "experiment": EXPERIMENT_ID,
        "question": "Does pruning only after a leader is clear and stable preserve recurrent performance better than clock-driven sparsity?",
        "gating_rule": {"minimum_open_cycles":3,"clear_gap":0.18,"stable_l1_delta":0.10,"collapsed_k":2},
        "held_out": {k:v.to_dict() for k,v in held.items()},
        "renamed_candidates": {k:v.to_dict() for k,v in renamed.items()},
        "verdict": verdict(held),
        "scientific_boundary": "This tests adaptive pruning only inside the current synthetic relational family."
    }

def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--quick", action="store_true"); args = parser.parse_args()
    print(json.dumps(run_assay(quick=args.quick), indent=2))

if __name__ == "__main__":
    main()
