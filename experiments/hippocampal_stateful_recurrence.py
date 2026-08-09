"""State-dependent recurrent settling assay.

This non-production experiment asks whether recurrence becomes independently useful
when candidate activations alter the evidence landscape on later cycles.

Unlike the earlier static-anchor assay, each candidate can excite compatible
candidates and inhibit incompatible candidates. Therefore the state at cycle t
changes the evidence received at cycle t+1.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import argparse
import json
import random
from statistics import mean

EXPERIMENT_ID = "hippocampal-stateful-recurrence-v1"


@dataclass(frozen=True, slots=True)
class StatefulWorld:
    seed: int
    names: tuple[str, ...]
    initial: tuple[float, ...]
    excitation: tuple[tuple[float, ...], ...]
    inhibition: tuple[tuple[float, ...], ...]
    correct_index: int

    @property
    def correct_name(self) -> str:
        return self.names[self.correct_index]


@dataclass(frozen=True, slots=True)
class Cycle:
    cycle: int
    activations: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class InferenceResult:
    winner: str
    confidence_gap: float
    cycles: tuple[Cycle, ...]


@dataclass(frozen=True, slots=True)
class Summary:
    episodes: int
    accuracy: float
    mean_confidence_gap: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _normalize(values: list[float]) -> list[float]:
    maximum = max(values)
    if maximum <= 0.0:
        return [0.0 for _ in values]
    return [value / maximum for value in values]


def generate_world(seed: int, *, rename_seed: int | None = None) -> StatefulWorld:
    """Generate an unseen relational field where a coherent triad must beat a lure.

    Candidates 0-2 form a mutually supportive triad. Candidate 3 is a lure with the
    strongest initial activation but conflicts with two members of the triad.
    The correct answer is one member of the triad, selected by a small initial edge.

    A one-pass scorer sees the lure as strongest because recurrent support has not yet
    had time to circulate through the triad. Multi-cycle recurrence should amplify the
    coherent triad and suppress the incompatible lure.
    """

    rng = random.Random(seed)
    count = 4
    correct = rng.randrange(3)
    lure = 3

    name_rng = random.Random(seed + 800_003 if rename_seed is None else rename_seed)
    names_list = [f"q{index}_{name_rng.randrange(1000, 9999)}" for index in range(count)]
    name_rng.shuffle(names_list)
    # Preserve index identity after shuffling names only; labels remain opaque.
    names = tuple(names_list)

    initial = [rng.uniform(0.48, 0.58) for _ in range(3)] + [rng.uniform(0.76, 0.88)]
    initial[correct] += rng.uniform(0.05, 0.09)

    excitation = [[0.0 for _ in range(count)] for _ in range(count)]
    inhibition = [[0.0 for _ in range(count)] for _ in range(count)]

    # Coherent triad: moderate recurrent excitation circulates among 0,1,2.
    for source in range(3):
        for target in range(3):
            if source != target:
                excitation[source][target] = rng.uniform(0.46, 0.62)

    # Slightly stronger support into the designated correct member.
    for source in range(3):
        if source != correct:
            excitation[source][correct] += rng.uniform(0.07, 0.11)

    # Lure weakly excites itself and one triad member, but conflicts with two others.
    excitation[lure][lure] = rng.uniform(0.10, 0.18)
    weak_friend = (correct + 1) % 3
    excitation[lure][weak_friend] = rng.uniform(0.10, 0.18)
    excitation[weak_friend][lure] = rng.uniform(0.08, 0.16)

    conflicted = [idx for idx in range(3) if idx != weak_friend]
    for idx in conflicted:
        inhibition[idx][lure] = rng.uniform(0.42, 0.58)
        inhibition[lure][idx] = rng.uniform(0.42, 0.58)

    return StatefulWorld(
        seed=seed,
        names=names,
        initial=tuple(initial),
        excitation=tuple(tuple(row) for row in excitation),
        inhibition=tuple(tuple(row) for row in inhibition),
        correct_index=correct,
    )


def one_pass(world: StatefulWorld) -> InferenceResult:
    """Matched control: choose from initial evidence only, before feedback circulates."""
    activations = _normalize(list(world.initial))
    ranked = sorted(range(len(activations)), key=lambda i: activations[i], reverse=True)
    winner = ranked[0]
    gap = activations[ranked[0]] - activations[ranked[1]]
    return InferenceResult(world.names[winner], gap, (Cycle(0, tuple(activations)),))


def recurrent(
    world: StatefulWorld,
    *,
    cycles: int = 8,
    persistence: float = 0.28,
    excitation_gain: float = 0.78,
    inhibition_gain: float = 0.72,
    input_gain: float = 0.22,
    progressive_sparsity: bool = True,
) -> InferenceResult:
    """Run state-dependent recurrence.

    u_i(t+1) = p*a_i(t)
               + e*sum_j excitation[j][i]*a_j(t)
               - h*sum_j inhibition[j][i]*a_j(t)
               + g*initial_i

    The critical property is that a_j(t) changes every cycle, so later evidence differs
    from earlier evidence. Optional progressive sparsity contracts the active field.
    """

    a = _normalize(list(world.initial))
    history: list[Cycle] = [Cycle(0, tuple(a))]
    n = len(a)

    for step in range(1, cycles + 1):
        raw: list[float] = []
        for i in range(n):
            excite = sum(world.excitation[j][i] * a[j] for j in range(n))
            inhibit = sum(world.inhibition[j][i] * a[j] for j in range(n))
            value = (
                persistence * a[i]
                + excitation_gain * excite
                - inhibition_gain * inhibit
                + input_gain * world.initial[i]
            )
            raw.append(max(0.0, value))

        a = _normalize(raw)

        if progressive_sparsity:
            keep_k = 4 if step <= 2 else (3 if step <= 5 else 2)
            ranked = sorted(range(n), key=lambda idx: a[idx], reverse=True)
            survivors = set(ranked[:keep_k])
            a = [value if idx in survivors else 0.0 for idx, value in enumerate(a)]

        history.append(Cycle(step, tuple(a)))

    ranked = sorted(range(n), key=lambda i: a[i], reverse=True)
    winner = ranked[0]
    gap = a[ranked[0]] - a[ranked[1]]
    return InferenceResult(world.names[winner], gap, tuple(history))


def evaluate(seeds: range, *, rename_offset: int | None = None) -> dict[str, Summary | float]:
    one: list[tuple[bool, InferenceResult]] = []
    rec: list[tuple[bool, InferenceResult]] = []
    fixed: list[tuple[bool, InferenceResult]] = []

    for seed in seeds:
        world = generate_world(
            seed,
            rename_seed=(seed + rename_offset) if rename_offset is not None else None,
        )
        one_result = one_pass(world)
        rec_result = recurrent(world, progressive_sparsity=True)
        fixed_result = recurrent(world, progressive_sparsity=False)
        one.append((one_result.winner == world.correct_name, one_result))
        rec.append((rec_result.winner == world.correct_name, rec_result))
        fixed.append((fixed_result.winner == world.correct_name, fixed_result))

    def summarize(items: list[tuple[bool, InferenceResult]]) -> Summary:
        return Summary(
            episodes=len(items),
            accuracy=mean(1.0 if ok else 0.0 for ok, _ in items),
            mean_confidence_gap=mean(result.confidence_gap for _, result in items),
        )

    one_s = summarize(one)
    rec_s = summarize(rec)
    fixed_s = summarize(fixed)
    agreement = mean(
        1.0 if one_result.winner == rec_result.winner else 0.0
        for (_, one_result), (_, rec_result) in zip(one, rec)
    )
    return {
        "one_pass": one_s,
        "recurrent_progressive": rec_s,
        "recurrent_fixed": fixed_s,
        "one_pass_recurrent_agreement": agreement,
        "recurrent_advantage": rec_s.accuracy - one_s.accuracy,
        "progressive_advantage_over_fixed": rec_s.accuracy - fixed_s.accuracy,
    }


def run_assay(*, quick: bool = False) -> dict[str, object]:
    seeds = range(20000, 20200) if quick else range(20000, 21000)
    held = evaluate(seeds)
    renamed = evaluate(seeds, rename_offset=900_000)

    one = held["one_pass"]
    rec = held["recurrent_progressive"]
    assert isinstance(one, Summary) and isinstance(rec, Summary)
    advantage = rec.accuracy - one.accuracy

    if advantage >= 0.25 and rec.accuracy >= 0.80:
        verdict = "EVIDENCE FOR STATE-DEPENDENT RECURRENT VALUE"
    elif advantage < 0.05:
        verdict = "STATE-DEPENDENT RECURRENCE NOT YET SUPPORTED"
    else:
        verdict = "MIXED RESULT"

    def serialize(bundle: dict[str, Summary | float]) -> dict[str, object]:
        return {
            key: (value.to_dict() if isinstance(value, Summary) else value)
            for key, value in bundle.items()
        }

    return {
        "experiment": EXPERIMENT_ID,
        "question": (
            "Can state-dependent excitation/inhibition make recurrent settling solve "
            "unseen relational fields that a matched one-pass initial scorer cannot?"
        ),
        "held_out": serialize(held),
        "renamed_candidates": serialize(renamed),
        "verdict": verdict,
        "scientific_boundary": (
            "The generator is synthetic and explicitly contains recurrent relational "
            "structure. A positive result would show that multi-cycle state evolution "
            "adds value in this family, not that the mechanism is generally optimal."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run_assay(quick=args), indent=2))


if __name__ == "__main__":
    main()
