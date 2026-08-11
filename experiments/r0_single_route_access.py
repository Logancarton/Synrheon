"""R0-SR1: deterministic single-route partial-cue access baseline.

This assay validates the retrieval instrument before any latent multi-route learning.
It intentionally supplies one oracle route index at a time and must not be described as
support for learned relationship channels.

The retriever never receives target identity. Experiment labels are used only after
retrieval for scoring.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Literal, Sequence
import argparse
import json
import random

EXPERIMENT_ID = "r0-single-route-access-v1"
MEMORY_COUNT = 128
FIELD_SIZE = 32
ROUTE_GROUP_SIZES = (8, 16, 32, 64)
ROUTE_COUNT = len(ROUTE_GROUP_SIZES)

ProbeCondition = Literal["full", "partial", "noisy", "missing", "wrong_route"]


@dataclass(frozen=True, slots=True)
class RouteBinding:
    """One memory's opaque binding inside one isolated generator route."""

    anchor_concept_id: str
    detail_concept_id: str

    def concept_ids(self) -> frozenset[str]:
        return frozenset((self.anchor_concept_id, self.detail_concept_id))


@dataclass(frozen=True, slots=True)
class MemoryRecord:
    """One opaque memory with one binding per hidden generator route slot."""

    memory_id: str
    bindings: tuple[RouteBinding, ...]

    def binding(self, route_index: int) -> RouteBinding:
        try:
            return self.bindings[route_index]
        except IndexError as exc:
            raise IndexError(f"Unknown route index: {route_index}") from exc


@dataclass(frozen=True, slots=True)
class SingleRouteWorld:
    """Deterministic family-A mechanism world used only by R0-SR1."""

    seed: int
    memories: tuple[MemoryRecord, ...]
    route_group_sizes: tuple[int, ...]

    @property
    def by_id(self) -> dict[str, MemoryRecord]:
        return {memory.memory_id: memory for memory in self.memories}

    @property
    def route_count(self) -> int:
        return len(self.route_group_sizes)


@dataclass(frozen=True, slots=True)
class RetrievalCue:
    """Model-visible cue. It deliberately contains no target identity."""

    concept_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class LabeledProbe:
    """Experiment wrapper that keeps target truth outside the retriever input."""

    probe_id: str
    route_index: int
    condition: ProbeCondition
    cue: RetrievalCue
    target_memory_id: str


@dataclass(frozen=True, slots=True)
class ScoredMemory:
    memory_id: str
    score: float


@dataclass(frozen=True, slots=True)
class ProbeOutcome:
    probe_id: str
    route_index: int
    condition: ProbeCondition
    target_memory_id: str
    target_rank: int | None
    hit_at_field: bool
    top1: bool
    field_size: int

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class RouteMetrics:
    route_index: int
    route_group_size: int
    probe_count_per_condition: int
    full_top1: float
    full_hit_at_32: float
    partial_hit_at_32: float
    noisy_hit_at_32: float
    missing_hit_at_32: float
    wrong_route_hit_at_32: float
    expected_partial_hit_at_32: float
    expected_missing_hit_at_32: float
    expected_wrong_route_hit_at_32: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class SingleRouteRetriever:
    """Simple isolated-route scorer frozen by the R0-SR1 preregistration.

    The route index is an oracle isolation variable for this baseline only. The scorer
    uses only stored route bindings and cue concepts. It has no API for target labels.
    """

    def __init__(self, world: SingleRouteWorld) -> None:
        self.world = world
        self._bindings: tuple[dict[str, frozenset[str]], ...] = tuple(
            {
                memory.memory_id: memory.binding(route_index).concept_ids()
                for memory in world.memories
            }
            for route_index in range(world.route_count)
        )

    def rank(
        self,
        cue: RetrievalCue,
        *,
        route_index: int,
        field_size: int = FIELD_SIZE,
    ) -> tuple[ScoredMemory, ...]:
        """Return a fixed-size field using only one route's bindings."""

        if not 0 <= route_index < self.world.route_count:
            raise IndexError(f"Unknown route index: {route_index}")
        if field_size <= 0:
            raise ValueError("Field size must be positive.")
        if field_size > len(self.world.memories):
            raise ValueError("Field size cannot exceed memory count.")

        cue_set = frozenset(cue.concept_ids)
        denominator = len(cue_set)
        ranked: list[ScoredMemory] = []
        for memory_id, binding in self._bindings[route_index].items():
            overlap = len(cue_set & binding)
            score = overlap / denominator if denominator else 0.0
            ranked.append(ScoredMemory(memory_id=memory_id, score=score))

        ranked.sort(key=lambda item: (-item.score, item.memory_id))
        return tuple(ranked[:field_size])


def make_family_a_world(
    *,
    seed: int = 1701,
    memory_count: int = MEMORY_COUNT,
    route_group_sizes: Sequence[int] = ROUTE_GROUP_SIZES,
) -> SingleRouteWorld:
    """Create opaque route partitions with controlled ambiguity.

    This is deliberately one generator family. Changing ``seed`` does not constitute a
    structural transfer family.
    """

    group_sizes = tuple(int(value) for value in route_group_sizes)
    if memory_count <= 0:
        raise ValueError("Memory count must be positive.")
    if not group_sizes:
        raise ValueError("At least one route group size is required.")
    for group_size in group_sizes:
        if group_size <= 0 or group_size > memory_count:
            raise ValueError("Route group sizes must be within memory count.")
        if memory_count % group_size != 0:
            raise ValueError("Each route group size must divide memory count exactly.")

    memory_ids = tuple(_opaque("memory", seed, index) for index in range(memory_count))
    per_memory: list[list[RouteBinding | None]] = [
        [None for _ in group_sizes] for _ in range(memory_count)
    ]

    for route_index, group_size in enumerate(group_sizes):
        permutation = list(range(memory_count))
        route_rng = random.Random(_route_seed(seed, route_index))
        route_rng.shuffle(permutation)

        for position, memory_index in enumerate(permutation):
            group_index = position // group_size
            anchor = _opaque("concept", seed, route_index, "anchor", group_index)
            detail = _opaque("concept", seed, route_index, "detail", memory_index)
            per_memory[memory_index][route_index] = RouteBinding(
                anchor_concept_id=anchor,
                detail_concept_id=detail,
            )

    memories: list[MemoryRecord] = []
    for memory_index, memory_id in enumerate(memory_ids):
        raw_bindings = per_memory[memory_index]
        if any(binding is None for binding in raw_bindings):
            raise RuntimeError("World construction left an incomplete route binding.")
        bindings = tuple(binding for binding in raw_bindings if binding is not None)
        memories.append(MemoryRecord(memory_id=memory_id, bindings=bindings))

    return SingleRouteWorld(
        seed=seed,
        memories=tuple(memories),
        route_group_sizes=group_sizes,
    )


def make_probe(
    world: SingleRouteWorld,
    memory: MemoryRecord,
    *,
    route_index: int,
    condition: ProbeCondition,
) -> LabeledProbe:
    """Build one labeled experiment probe while keeping truth outside the cue."""

    if not 0 <= route_index < world.route_count:
        raise IndexError(f"Unknown route index: {route_index}")

    binding = memory.binding(route_index)
    if condition == "full":
        concepts = (binding.anchor_concept_id, binding.detail_concept_id)
    elif condition == "partial":
        concepts = (binding.anchor_concept_id,)
    elif condition == "noisy":
        foreign = _foreign_detail(world, memory, route_index)
        concepts = (binding.anchor_concept_id, foreign)
    elif condition == "missing":
        concepts = (_opaque("missing", world.seed, route_index, memory.memory_id),)
    elif condition == "wrong_route":
        other_route = (route_index + 1) % world.route_count
        other = memory.binding(other_route)
        concepts = (other.anchor_concept_id, other.detail_concept_id)
    else:
        raise ValueError(f"Unknown probe condition: {condition}")

    probe_id = _opaque("probe", world.seed, route_index, condition, memory.memory_id)
    return LabeledProbe(
        probe_id=probe_id,
        route_index=route_index,
        condition=condition,
        cue=RetrievalCue(concept_ids=concepts),
        target_memory_id=memory.memory_id,
    )


def score_probe(
    retriever: SingleRouteRetriever,
    probe: LabeledProbe,
    *,
    field_size: int = FIELD_SIZE,
) -> ProbeOutcome:
    """Score target identity only after route retrieval is complete."""

    field = retriever.rank(
        probe.cue,
        route_index=probe.route_index,
        field_size=field_size,
    )
    target_rank: int | None = None
    for index, candidate in enumerate(field, start=1):
        if candidate.memory_id == probe.target_memory_id:
            target_rank = index
            break
    return ProbeOutcome(
        probe_id=probe.probe_id,
        route_index=probe.route_index,
        condition=probe.condition,
        target_memory_id=probe.target_memory_id,
        target_rank=target_rank,
        hit_at_field=target_rank is not None,
        top1=target_rank == 1,
        field_size=len(field),
    )


def run_single_route_assay(
    *,
    seed: int = 1701,
    field_size: int = FIELD_SIZE,
) -> dict[str, object]:
    """Run the frozen family-A single-route integrity assay."""

    world = make_family_a_world(seed=seed)
    retriever = SingleRouteRetriever(world)
    conditions: tuple[ProbeCondition, ...] = (
        "full",
        "partial",
        "noisy",
        "missing",
        "wrong_route",
    )

    route_metrics: list[RouteMetrics] = []
    all_outcomes: list[ProbeOutcome] = []
    for route_index, group_size in enumerate(world.route_group_sizes):
        outcomes_by_condition: dict[ProbeCondition, list[ProbeOutcome]] = {
            condition: [] for condition in conditions
        }
        for memory in world.memories:
            for condition in conditions:
                probe = make_probe(
                    world,
                    memory,
                    route_index=route_index,
                    condition=condition,
                )
                outcome = score_probe(retriever, probe, field_size=field_size)
                outcomes_by_condition[condition].append(outcome)
                all_outcomes.append(outcome)

        expected_partial = min(1.0, field_size / group_size)
        expected_chance = field_size / len(world.memories)
        route_metrics.append(
            RouteMetrics(
                route_index=route_index,
                route_group_size=group_size,
                probe_count_per_condition=len(world.memories),
                full_top1=_rate(outcomes_by_condition["full"], "top1"),
                full_hit_at_32=_rate(outcomes_by_condition["full"], "hit_at_field"),
                partial_hit_at_32=_rate(outcomes_by_condition["partial"], "hit_at_field"),
                noisy_hit_at_32=_rate(outcomes_by_condition["noisy"], "hit_at_field"),
                missing_hit_at_32=_rate(outcomes_by_condition["missing"], "hit_at_field"),
                wrong_route_hit_at_32=_rate(
                    outcomes_by_condition["wrong_route"], "hit_at_field"
                ),
                expected_partial_hit_at_32=expected_partial,
                expected_missing_hit_at_32=expected_chance,
                expected_wrong_route_hit_at_32=expected_chance,
            )
        )

    valid = _instrument_valid(route_metrics, all_outcomes, field_size=field_size)
    return {
        "experiment": EXPERIMENT_ID,
        "evidence_level": "synthetic mechanism integrity; not multi-route evidence",
        "generator_family": "A",
        "seed": seed,
        "memory_count": len(world.memories),
        "field_size": field_size,
        "route_group_sizes": list(world.route_group_sizes),
        "route_metrics": [metrics.to_dict() for metrics in route_metrics],
        "verdict": "SINGLE_ROUTE_INSTRUMENT_VALID" if valid else "INSTRUMENT_INVALID",
        "outcomes": [outcome.to_dict() for outcome in all_outcomes],
    }


def _foreign_detail(
    world: SingleRouteWorld,
    target: MemoryRecord,
    route_index: int,
) -> str:
    target_anchor = target.binding(route_index).anchor_concept_id
    for candidate in sorted(world.memories, key=lambda item: item.memory_id):
        binding = candidate.binding(route_index)
        if binding.anchor_concept_id != target_anchor:
            return binding.detail_concept_id
    raise RuntimeError("No foreign route group exists for noisy cue construction.")


def _rate(outcomes: Sequence[ProbeOutcome], attribute: Literal["top1", "hit_at_field"]) -> float:
    if not outcomes:
        return 0.0
    return sum(1.0 if bool(getattr(outcome, attribute)) else 0.0 for outcome in outcomes) / len(
        outcomes
    )


def _instrument_valid(
    metrics: Sequence[RouteMetrics],
    outcomes: Sequence[ProbeOutcome],
    *,
    field_size: int,
    tolerance: float = 1e-12,
) -> bool:
    for item in metrics:
        if abs(item.full_top1 - 1.0) > tolerance:
            return False
        if abs(item.full_hit_at_32 - 1.0) > tolerance:
            return False
        if abs(item.partial_hit_at_32 - item.expected_partial_hit_at_32) > tolerance:
            return False
        if abs(item.missing_hit_at_32 - item.expected_missing_hit_at_32) > tolerance:
            return False
        if abs(item.wrong_route_hit_at_32 - item.expected_wrong_route_hit_at_32) > tolerance:
            return False
    return all(outcome.field_size == field_size for outcome in outcomes)


def _route_seed(seed: int, route_index: int) -> int:
    digest = sha256(f"route-seed\0{seed}\0{route_index}".encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big")


def _opaque(kind: str, *parts: object) -> str:
    payload = "\0".join((kind, *(str(part) for part in parts)))
    digest = sha256(payload.encode("utf-8")).hexdigest()[:20]
    prefix = "m" if kind == "memory" else "x"
    return f"{prefix}:{digest}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run R0-SR1 single-route access integrity assay")
    parser.add_argument("--seed", type=int, default=1701)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    payload = run_single_route_assay(seed=args.seed)
    if args.summary_only:
        payload = {key: value for key, value in payload.items() if key != "outcomes"}
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
