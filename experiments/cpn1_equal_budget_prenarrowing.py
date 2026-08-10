"""CPN-1: equal-budget contextual pre-narrowing on SciFact development.

Implements exactly:

    docs/CPN1_PREREGISTRATION.md      frozen at afea37c
    docs/CPN1_1_AMENDMENT.md          frozen pre-result clarifications

Question: does spending the one affordable broad feature pass under partial context, using
that pass to create a reversible active ceiling, and then spending the remaining channel
computation under full context, improve retrieval quality relative to the same frozen
channel schedule performed entirely under full context?

A negative result means contextual pre-narrowing is not a required Ground 0 mechanism under
this task and compute model. It does **not** close the general multi-stage / iterative
settling question.

Result-bearing execution on external data requires an explicit ``evidence_run=True``. It is
off by default so a development outcome cannot be produced accidentally.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from statistics import mean
from typing import Iterable, Sequence
import argparse
import json

from experiments.external_retrieval_cascade import (
    CANDIDATE_DEPTH,
    DORMANT_FLOOR,
    RECURRENCE_WIDTH,
    TAPER_RELATIVE_GATE,
    TAPER_STAGE_CYCLES,
    TAPER_TEMPERATURE,
    BM25Index,
    ChannelBank,
    Dataset,
    FeatureMeter,
    LearnedParameters,
    Query,
    _initial_activation,
    _normalize,
    _ranked,
    _reopen_cue,
    build_environment,
    learn_parameters,
    load_beir_dataset,
    ndcg_at_k,
    paired_bootstrap,
    queries_for_split,
    split_of,
)

import math

CPN1_ID = "cpn-1-equal-budget-contextual-prenarrowing-v1"

#: Frozen decision constants, carried unchanged from MT-1 v1.
MATERIAL_DELTA = 0.010
MIN_TRANSITION_QUERIES = 30
EXPECTED_SCIFACT_DEVELOPMENT_QUERIES = 93

CONDITIONS = ("A0", "A1", "T", "C_carry", "C_reversed", "C_hard")
PRIMARY_COMPARISON = ("T", "A1")
SECONDARY_COMPARISONS = (
    ("T", "C_carry"),
    ("T", "C_hard"),
    ("T", "C_reversed"),
    ("A1", "A0"),
)


@dataclass(slots=True)
class StageTrace:
    """Observable record of one settling stage."""

    channels: tuple[int, ...]
    cue_used: bool
    cycles_completed: int
    channels_completed: int
    truncated: bool
    update_region_sizes: tuple[int, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(slots=True)
class ConditionResult:
    """One condition's complete trajectory for one query."""

    condition: str
    ranking: list[str]
    activation: dict[str, float]
    update_ceiling: tuple[str, ...]
    evaluations: int
    requests: int
    per_channel: tuple[int, ...]
    nanoseconds: int
    activation_updates: int
    normalization_ops: int
    stages: list[StageTrace] = field(default_factory=list)
    truncated: bool = False
    removed_candidates: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "condition": self.condition,
            "ranking_depth": len(self.ranking),
            "field_size": len(self.activation),
            "update_ceiling_size": len(self.update_ceiling),
            "evaluations": self.evaluations,
            "requests": self.requests,
            "per_channel": list(self.per_channel),
            "nanoseconds": self.nanoseconds,
            "activation_updates": self.activation_updates,
            "normalization_ops": self.normalization_ops,
            "truncated": self.truncated,
            "removed_candidate_count": len(self.removed_candidates),
            "stages": [stage.to_dict() for stage in self.stages],
        }


@dataclass(slots=True)
class Trajectory:
    """A condition's mutable state plus its own isolated feature meter.

    Cache isolation is structural: each trajectory constructs its own ``FeatureMeter`` and
    tracks its own evaluated keys. Nothing but the scalar budget ever crosses a condition
    boundary (CPN-1.1 clarification 4).
    """

    meter: FeatureMeter
    activation: dict[str, float]
    update_region: set[str]
    evaluated_keys: set[tuple[str, int, tuple[str, ...]]] = field(default_factory=set)
    activation_updates: int = 0
    normalization_ops: int = 0
    stages: list[StageTrace] = field(default_factory=list)
    truncated: bool = False


def new_trajectory(bank: ChannelBank, activation: dict[str, float]) -> Trajectory:
    """Start a condition with a private, empty feature cache."""

    return Trajectory(
        meter=FeatureMeter(bank),
        activation=dict(activation),
        update_region=set(activation),
    )


def _context(query: Query, cue: tuple[str, ...] | None) -> tuple[str, ...]:
    return tuple(query.tokens if cue is None else cue)


def run_stage(
    trajectory: Trajectory,
    query: Query,
    parameters: LearnedParameters,
    *,
    channels: Sequence[int],
    cue: tuple[str, ...] | None,
    ceiling: Iterable[str] | None = None,
    budget: int | None = None,
    minimum_active: int = RECURRENCE_WIDTH,
) -> StageTrace:
    """Run one settling stage over the complete activation field.

    Mirrors the frozen taper dynamics exactly. Two behaviours are specified by CPN-1.1:

    * ``ceiling`` is an **update** ceiling, never a deletion boundary. Candidates outside it
      stay in ``trajectory.activation``, receive no feature update, and remain rankable.
    * ``budget`` stops the stage **before** any cycle whose cache misses would exceed it.
      There is no partial cycle and no overdraft.
    """

    cap = set(ceiling) if ceiling is not None else None
    if cap is not None:
        trajectory.update_region &= cap

    context = _context(query, cue)
    trace = StageTrace(
        channels=tuple(channels),
        cue_used=cue is not None,
        cycles_completed=0,
        channels_completed=0,
        truncated=False,
    )
    sizes: list[int] = []

    for channel in channels:
        gain = parameters.channel_gains[channel]
        for _ in range(TAPER_STAGE_CYCLES):
            misses = sum(
                1
                for doc_id in trajectory.update_region
                if (doc_id, channel, context) not in trajectory.evaluated_keys
            )
            if budget is not None and trajectory.meter.evaluations + misses > budget:
                trace.truncated = True
                trajectory.truncated = True
                trace.update_region_sizes = tuple(sizes)
                trajectory.stages.append(trace)
                return trace

            updated = dict(trajectory.activation)
            for doc_id in trajectory.update_region:
                value = trajectory.meter.value(query, doc_id, channel, cue=cue)
                trajectory.evaluated_keys.add((doc_id, channel, context))
                updated[doc_id] = (
                    max(trajectory.activation[doc_id], DORMANT_FLOOR) ** 0.90
                    * math.exp(gain * value / TAPER_TEMPERATURE)
                )
            trajectory.activation_updates += len(trajectory.update_region)
            trajectory.activation = _normalize(updated)
            trajectory.normalization_ops += len(trajectory.activation)
            trace.cycles_completed += 1

        peak = max(trajectory.activation.values()) if trajectory.activation else 0.0
        eligible = {
            doc_id
            for doc_id, value in trajectory.activation.items()
            if value >= peak * TAPER_RELATIVE_GATE
        }
        if cap is not None:
            eligible &= cap
        if len(eligible) < minimum_active:
            pool = [
                doc_id
                for doc_id, _ in _ranked(trajectory.activation)
                if cap is None or doc_id in cap
            ]
            eligible = set(pool[:minimum_active])
        trajectory.update_region = eligible
        trace.channels_completed += 1
        sizes.append(len(eligible))

    trace.update_region_sizes = tuple(sizes)
    trajectory.stages.append(trace)
    return trace


def _finish(
    condition: str,
    trajectory: Trajectory,
    *,
    ceiling: Iterable[str],
    removed: Iterable[str] = (),
) -> ConditionResult:
    return ConditionResult(
        condition=condition,
        ranking=[doc_id for doc_id, _ in _ranked(trajectory.activation)],
        activation=dict(trajectory.activation),
        update_ceiling=tuple(sorted(ceiling)),
        evaluations=trajectory.meter.evaluations,
        requests=trajectory.meter.requests,
        per_channel=tuple(trajectory.meter.per_channel),
        nanoseconds=trajectory.meter.nanoseconds,
        activation_updates=trajectory.activation_updates,
        normalization_ops=trajectory.normalization_ops,
        stages=list(trajectory.stages),
        truncated=trajectory.truncated,
        removed_candidates=tuple(sorted(removed)),
    )


def run_a1(
    query: Query,
    bank: ChannelBank,
    parameters: LearnedParameters,
    full_query_prior: dict[str, float],
) -> ConditionResult:
    """Full-context baseline. Its natural evaluation cost defines B(q)."""

    trajectory = new_trajectory(bank, full_query_prior)
    run_stage(trajectory, query, parameters, channels=parameters.channel_order, cue=None)
    return _finish("A1", trajectory, ceiling=trajectory.update_region)


def run_prenarrowed(
    condition: str,
    query: Query,
    bank: ChannelBank,
    parameters: LearnedParameters,
    full_query_prior: dict[str, float],
    cue: tuple[str, ...],
    budget: int,
    *,
    stage1_cue: tuple[str, ...] | None,
    stage2_cue: tuple[str, ...] | None,
    carry: bool = False,
    hard_prune: bool = False,
) -> ConditionResult:
    """Shared two-stage trajectory for T, C-carry, C-reversed, and C-hard.

    The conditions differ only in which stage sees the partial cue, whether the transition
    resets or carries activation, and whether the transition suppresses or removes.
    """

    order = parameters.channel_order
    trajectory = new_trajectory(bank, full_query_prior)
    run_stage(
        trajectory, query, parameters,
        channels=order[:1], cue=stage1_cue, budget=budget,
    )
    stage1_active = set(trajectory.update_region)

    if hard_prune:
        survivors = [
            doc_id
            for doc_id, _ in _ranked(trajectory.activation)[:RECURRENCE_WIDTH]
        ]
        removed = set(trajectory.activation) - set(survivors)
        # Destructive: removed identities leave the result-bearing field entirely.
        trajectory.activation = _normalize({d: full_query_prior[d] for d in survivors})
        trajectory.update_region = set(survivors)
        run_stage(
            trajectory, query, parameters,
            channels=order[1:], cue=stage2_cue, ceiling=set(survivors), budget=budget,
            minimum_active=min(RECURRENCE_WIDTH, len(survivors)),
        )
        return _finish(condition, trajectory, ceiling=survivors, removed=removed)

    if not carry:
        # Reset ranking activation; every candidate identity stays represented.
        trajectory.activation = dict(full_query_prior)
    trajectory.update_region = set(stage1_active)
    run_stage(
        trajectory, query, parameters,
        channels=order[1:], cue=stage2_cue, ceiling=stage1_active, budget=budget,
    )
    return _finish(condition, trajectory, ceiling=stage1_active)


@dataclass(frozen=True, slots=True)
class CPN1QueryOutcome:
    query_id: str
    transition_evaluable: bool
    budget: int
    ndcg: dict[str, float]
    conditions: dict[str, dict[str, object]]
    budget_respected: bool

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def run_query(
    dataset: Dataset,
    index: BM25Index,
    bank: ChannelBank,
    parameters: LearnedParameters,
    query: Query,
    *,
    score: bool,
) -> CPN1QueryOutcome:
    """Run every condition for one query.

    ``score`` gates nDCG computation. It is False unless a result-bearing run was explicitly
    requested, so a development outcome cannot be produced by accident.
    """

    judged = dataset.qrels.get(query.query_id, {}) if score else {}
    candidates = index.top_candidates(query.tokens, CANDIDATE_DEPTH)
    field_ids = [doc_id for doc_id, _ in candidates]

    ndcg = {condition: 0.0 for condition in CONDITIONS}
    results: dict[str, ConditionResult] = {}

    if not candidates:
        return CPN1QueryOutcome(
            query_id=query.query_id, transition_evaluable=False, budget=0,
            ndcg=ndcg, conditions={}, budget_respected=True,
        )

    full_query_prior = _initial_activation(candidates)

    if score:
        ndcg["A0"] = ndcg_at_k(field_ids, judged, 10)

    a1 = run_a1(query, bank, parameters, full_query_prior)
    results["A1"] = a1
    budget = a1.evaluations
    if score:
        ndcg["A1"] = ndcg_at_k(a1.ranking, judged, 10)

    cue = _reopen_cue(query)
    if cue is None:
        return CPN1QueryOutcome(
            query_id=query.query_id, transition_evaluable=False, budget=budget,
            ndcg=ndcg, conditions={k: v.to_dict() for k, v in results.items()},
            budget_respected=True,
        )

    plans = {
        "T": dict(stage1_cue=cue, stage2_cue=None),
        "C_carry": dict(stage1_cue=cue, stage2_cue=None, carry=True),
        "C_reversed": dict(stage1_cue=None, stage2_cue=cue),
        "C_hard": dict(stage1_cue=cue, stage2_cue=None, hard_prune=True),
    }
    for condition, plan in plans.items():
        result = run_prenarrowed(
            condition, query, bank, parameters, full_query_prior, cue, budget, **plan
        )
        results[condition] = result
        if score:
            ndcg[condition] = ndcg_at_k(result.ranking, judged, 10)

    respected = all(
        result.evaluations <= budget for name, result in results.items() if name != "A0"
    )
    return CPN1QueryOutcome(
        query_id=query.query_id,
        transition_evaluable=True,
        budget=budget,
        ndcg=ndcg,
        conditions={name: result.to_dict() for name, result in results.items()},
        budget_respected=respected,
    )


def classify_cpn1(
    *,
    transition_queries: int,
    delta: float,
    ci_low: float,
    budget_control_ok: bool,
) -> str:
    """Apply only the frozen CPN-1 interpretation categories."""

    if not budget_control_ok:
        return "INVALID_BUDGET_CONTROL"
    if transition_queries < MIN_TRANSITION_QUERIES:
        return "INCONCLUSIVE"
    if delta <= 0.0 or ci_low <= 0.0:
        return "CONTEXTUAL_PRENARROWING_NOT_SUPPORTED"
    if delta >= MATERIAL_DELTA:
        return "CONTEXTUAL_PRENARROWING_SUPPORTED"
    return "CONTEXTUAL_PRENARROWING_IMMATERIAL"


def _paired(rows: Sequence[CPN1QueryOutcome], left: str, right: str) -> dict[str, float]:
    return paired_bootstrap(
        [row.ndcg[left] for row in rows],
        [row.ndcg[right] for row in rows],
    )


def run_cpn1(dataset: Dataset, *, evidence_run: bool = False) -> dict[str, object]:
    """Run CPN-1 on the development split.

    ``evidence_run`` must be explicitly True to score external data. Synthetic runs are
    always mechanism checks and are never evidence.
    """

    if not dataset.synthetic and not evidence_run:
        raise RuntimeError(
            "CPN-1 result-bearing execution requires evidence_run=True (CLI: --run-evidence). "
            "Refusing to compute a SciFact development ranking or nDCG outcome by accident."
        )
    if not dataset.synthetic and dataset.name.lower() != "scifact":
        raise ValueError("CPN-1 is frozen for the SciFact development dataset only.")

    index, bank = build_environment(dataset)
    development = queries_for_split(dataset, "development")
    if not development:
        raise ValueError("development split is empty")
    if not dataset.synthetic and len(development) != EXPECTED_SCIFACT_DEVELOPMENT_QUERIES:
        raise ValueError(
            "Frozen CPN-1 expects exactly 93 SciFact development queries; "
            f"received {len(development)}."
        )
    stray = [q.query_id for q in development if split_of(q.query_id) != "development"]
    if stray:
        raise RuntimeError(f"Reserved final-split queries reached CPN-1: {stray[:5]}")

    parameters = learn_parameters(dataset, bank, index, development=development)
    rows = [
        run_query(dataset, index, bank, parameters, query, score=True)
        for query in development
    ]
    transition_rows = [row for row in rows if row.transition_evaluable]

    budget_control_ok = all(row.budget_respected for row in rows)

    primary = (
        _paired(transition_rows, *PRIMARY_COMPARISON)
        if transition_rows
        else {"delta": 0.0, "ci_low": 0.0, "ci_high": 0.0, "p_greater": 0.0}
    )
    secondary = {
        f"{left}_minus_{right}": _paired(transition_rows, left, right)
        for left, right in SECONDARY_COMPARISONS
    } if transition_rows else {}

    classification = classify_cpn1(
        transition_queries=len(transition_rows),
        delta=primary["delta"],
        ci_low=primary["ci_low"],
        budget_control_ok=budget_control_ok,
    )

    def condition_stat(name: str, key: str) -> float:
        values = [
            row.conditions[name][key]
            for row in transition_rows
            if name in row.conditions
        ]
        return round(mean(values), 3) if values else 0.0

    compute = {
        name: {
            "mean_evaluations": condition_stat(name, "evaluations"),
            "max_evaluations": max(
                (row.conditions[name]["evaluations"] for row in transition_rows
                 if name in row.conditions), default=0
            ),
            "mean_requests": condition_stat(name, "requests"),
            "mean_activation_updates": condition_stat(name, "activation_updates"),
            "mean_normalization_ops": condition_stat(name, "normalization_ops"),
            "mean_nanoseconds": condition_stat(name, "nanoseconds"),
            "truncation_rate": round(
                mean(
                    1.0 if row.conditions[name]["truncated"] else 0.0
                    for row in transition_rows if name in row.conditions
                ), 4
            ) if transition_rows else 0.0,
        }
        for name in CONDITIONS[1:]
    }

    return {
        "experiment": CPN1_ID,
        "preregistration": "docs/CPN1_PREREGISTRATION.md",
        "amendment": "docs/CPN1_1_AMENDMENT.md",
        "dataset": dataset.name,
        "synthetic": dataset.synthetic,
        "split": "development",
        "development_queries": len(development),
        "transition_evaluable_queries": len(transition_rows),
        "minimum_transition_queries": MIN_TRANSITION_QUERIES,
        "material_delta": MATERIAL_DELTA,
        "parameters": parameters.to_dict(),
        "mean_budget": round(mean(row.budget for row in transition_rows), 3)
        if transition_rows else 0.0,
        "all_development_ndcg10": {
            name: round(mean(row.ndcg[name] for row in rows), 6) for name in ("A0", "A1")
        },
        "paired_transition_ndcg10": {
            name: round(mean(row.ndcg[name] for row in transition_rows), 6)
            for name in CONDITIONS
        } if transition_rows else {},
        "primary_effect": {
            "comparison": f"{PRIMARY_COMPARISON[0]}_minus_{PRIMARY_COMPARISON[1]}",
            **primary,
        },
        "secondary_effects": secondary,
        "secondary_note": (
            "Secondary comparisons are mechanistic evidence only. None may change, veto, "
            "promote, or replace the primary T-A1 classification (CPN-1.1 clarification 3)."
        ),
        "paired_compute": compute,
        "budget_control_ok": budget_control_ok,
        "classification": classification,
        "verdict": (
            f"NOT EVIDENCE: synthetic mechanism check; classification={classification}."
            if dataset.synthetic
            else classification
        ),
        "per_query": [row.to_dict() for row in rows],
        "scope_note": (
            "Development-only equal-budget contextual pre-narrowing test. No recurrence, no "
            "Token Deck input, no final split, no overdraft, and no post-hoc threshold "
            "changes are permitted. A negative result does not close the general "
            "multi-stage / iterative-settling question."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="CPN-1 equal-budget contextual pre-narrowing")
    parser.add_argument("--data", help="Unzipped BEIR SciFact dataset directory")
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Run a synthetic mechanism check; output is explicitly not evidence.",
    )
    parser.add_argument(
        "--run-evidence",
        action="store_true",
        help="Explicitly authorise a result-bearing run on external data.",
    )
    args = parser.parse_args()

    if args.smoke:
        from experiments.ext2_diagnostics import make_hard_corpus

        dataset = make_hard_corpus(seed=31, clusters=30, queries=140, informative_features=True)
    elif args.data:
        dataset = load_beir_dataset(args.data)
    else:
        parser.error("provide --data <SciFact folder> or --smoke")

    print(json.dumps(run_cpn1(dataset, evidence_run=args.run_evidence), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
