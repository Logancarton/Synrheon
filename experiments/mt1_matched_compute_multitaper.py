"""MT-1 v1: matched-compute multi-taper falsification — **UNEXECUTED / DESIGN-INVALID**.

.. warning::

   This implementation is preserved as design evidence and **must not be run for
   evidence**. A pre-result implementation audit found that the treatment condition
   cannot satisfy the experiment's own matched-compute admissibility rule:

   ```text
   frozen admissibility rule     E(M3) <= 1.10 * E(M1)
   measured engineering cost     E(M3) ~= 2.285 * E(M1)
   ```

   `MULTI_STAGE_SUPPORTED` was therefore structurally unreachable. See
   ``docs/MT1_DESIGN_AUDIT.md``. The replacement design is
   ``docs/CPN1_PREREGISTRATION.md``.

   No SciFact development nDCG result was ever computed or inspected under this design,
   so the development split remains available to the replacement experiment. To keep it
   that way, :func:`run_mt1` refuses non-synthetic datasets.

This module implements the frozen protocol in ``docs/MT1_PREREGISTRATION.md`` exactly.
That preregistration is retained unedited as frozen historical design evidence; it was
not amended to rescue the treatment.

It has no final-split option, invokes no recurrence, uses no Token Deck output, and treats
synthetic runs as mechanism smoke tests only.

Central question:

    After controlling the known transition-state persistence pathology, does more than one
    soft contextual settling stage materially outperform one good soft settling stage
    under matched computation?

D6 established that blind carry is harmful but did not hold compute constant: its staged
conditions spent roughly twice the per-query feature budget of its single-stage condition.
MT-1 closes exactly that gap by giving every condition the same nominal eight
channel-cycle update sweeps and gating any supportive reading on measured feature cost.

Thresholds here are frozen. Do not adjust them after observing a result.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from statistics import mean
from typing import Sequence
import argparse
import json
import math

from experiments.external_retrieval_cascade import (
    CANDIDATE_DEPTH,
    DORMANT_FLOOR,
    RECURRENCE_WIDTH,
    TAPER_RELATIVE_GATE,
    TAPER_TEMPERATURE,
    BM25Index,
    ChannelBank,
    Dataset,
    FeatureMeter,
    LearnedParameters,
    Query,
    TaperResult,
    _cue_prior,
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
    soft_taper,
)

MT1_ID = "mt1-matched-compute-multitaper-v1"

#: Frozen nominal budget: every condition receives eight channel-cycle update sweeps.
NOMINAL_SWEEPS = 8
SINGLE_STAGE_CYCLES = 2
MULTI_STAGE_CYCLES = 1

#: Frozen decision constants.
MATERIAL_DELTA = 0.010
COMPUTE_TOLERANCE = 1.10
MIN_TRANSITION_QUERIES = 30
EXPECTED_SCIFACT_DEVELOPMENT_QUERIES = 93

CONDITIONS = (
    "M0_bm25_anchor",
    "M1_single_full_soft",
    "M2_multi_naive_carry",
    "M3_multi_reset_narrowed",
    "M4_multi_full_reset",
    "M5_reversed_order",
    "M6_hard_staged_prune",
)

#: The primary comparison and the secondary comparisons, frozen in this order.
PRIMARY_COMPARISON = ("M3_multi_reset_narrowed", "M1_single_full_soft")
SECONDARY_COMPARISONS = (
    ("M3_multi_reset_narrowed", "M2_multi_naive_carry"),
    ("M3_multi_reset_narrowed", "M4_multi_full_reset"),
    ("M3_multi_reset_narrowed", "M5_reversed_order"),
    ("M3_multi_reset_narrowed", "M6_hard_staged_prune"),
    ("M1_single_full_soft", "M0_bm25_anchor"),
)


@dataclass(frozen=True, slots=True)
class MT1QueryOutcome:
    query_id: str
    transition_evaluable: bool
    ndcg: dict[str, float]
    feature_evaluations: dict[str, int]
    feature_nanoseconds: dict[str, int]
    single_stage_equivalence_max_abs_diff: float | None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def soft_stage(
    query: Query,
    candidates: Sequence[tuple[str, float]],
    parameters: LearnedParameters,
    meter: FeatureMeter,
    *,
    prior: dict[str, float],
    cue: tuple[str, ...] | None,
    cycles_per_channel: int,
    active_ceiling: Sequence[str] | None = None,
    minimum_active: int = RECURRENCE_WIDTH,
) -> TaperResult:
    """One soft settling stage.

    Mirrors ``soft_taper`` exactly except for two frozen MT-1 additions:

    * ``cycles_per_channel`` replaces the fixed ``TAPER_STAGE_CYCLES`` so a two-stage
      condition can split the same eight-sweep budget across its stages;
    * ``active_ceiling`` restricts the stage to an already-narrowed candidate set, which
      is what lets an earlier stage contribute compute narrowing without contributing
      ranking state.

    Stage dynamics, decay, temperature, channel gains, gate, and dormant floor are
    unchanged.
    """

    activation = dict(prior)
    for doc_id, _ in candidates:
        activation.setdefault(doc_id, 0.0)

    ceiling = set(active_ceiling) if active_ceiling is not None else None
    active = set(ceiling) if ceiling is not None else {doc_id for doc_id, _ in candidates}
    counts: list[int] = []

    for channel in parameters.channel_order:
        gain = parameters.channel_gains[channel]
        for _ in range(cycles_per_channel):
            updated = dict(activation)
            for doc_id in active:
                value = meter.value(query, doc_id, channel, cue=cue)
                updated[doc_id] = (
                    max(activation[doc_id], DORMANT_FLOOR) ** 0.90
                    * math.exp(gain * value / TAPER_TEMPERATURE)
                )
            activation = _normalize(updated)

        peak = max(activation.values()) if activation else 0.0
        eligible = {
            doc_id
            for doc_id, value in activation.items()
            if value >= peak * TAPER_RELATIVE_GATE
        }
        if ceiling is not None:
            # The retained narrowing is a ceiling: a later stage may narrow further but
            # never re-expand past what the earlier stage left active.
            eligible &= ceiling
        if len(eligible) < minimum_active:
            pool = [
                doc_id
                for doc_id, _ in _ranked(activation)
                if ceiling is None or doc_id in ceiling
            ]
            eligible = set(pool[:minimum_active])
        active = eligible
        counts.append(len(active))

    return TaperResult(
        activation=activation,
        active=tuple(sorted(active)),
        dormant=tuple(sorted(set(activation) - active)),
        stage_active_counts=tuple(counts),
    )


def _restricted_prior(prior: dict[str, float], survivors: Sequence[str]) -> dict[str, float]:
    return _normalize({doc_id: prior[doc_id] for doc_id in survivors})


def _ranking_from(activation: dict[str, float]) -> list[str]:
    return [doc_id for doc_id, _ in _ranked(activation)]


def _hard_pruned_ranking(
    survivor_activation: dict[str, float],
    field_ids: Sequence[str],
) -> list[str]:
    """Survivors ranked by activation, then removed candidates in retrieval order.

    Hard pruning removes rather than damps, so pruned candidates cannot be recovered by
    later evidence. They keep only their original retrieval order beneath the survivors.
    """

    survivors = _ranking_from(survivor_activation)
    kept = set(survivors)
    return survivors + [doc_id for doc_id in field_ids if doc_id not in kept]


def run_query(
    dataset: Dataset,
    index: BM25Index,
    bank: ChannelBank,
    parameters: LearnedParameters,
    query: Query,
) -> MT1QueryOutcome:
    judged = dataset.qrels.get(query.query_id, {})
    candidates = index.top_candidates(query.tokens, CANDIDATE_DEPTH)
    field_ids = [doc_id for doc_id, _ in candidates]

    ndcg = {condition: 0.0 for condition in CONDITIONS}
    evaluations = {condition: 0 for condition in CONDITIONS}
    nanoseconds = {condition: 0 for condition in CONDITIONS}

    if not candidates:
        return MT1QueryOutcome(
            query_id=query.query_id,
            transition_evaluable=False,
            ndcg=ndcg,
            feature_evaluations=evaluations,
            feature_nanoseconds=nanoseconds,
            single_stage_equivalence_max_abs_diff=None,
        )

    retrieval_prior = _initial_activation(candidates)

    # --- M0: retrieval anchor, no taper -------------------------------------------
    ndcg["M0_bm25_anchor"] = ndcg_at_k(field_ids, judged, 10)

    # --- M1: single full-context soft settling (primary baseline) -------------------
    meter_1 = FeatureMeter(bank)
    stage_1 = soft_stage(
        query,
        candidates,
        parameters,
        meter_1,
        prior=dict(retrieval_prior),
        cue=None,
        cycles_per_channel=SINGLE_STAGE_CYCLES,
    )
    ndcg["M1_single_full_soft"] = ndcg_at_k(_ranking_from(stage_1.activation), judged, 10)
    evaluations["M1_single_full_soft"] = meter_1.evaluations
    nanoseconds["M1_single_full_soft"] = meter_1.nanoseconds

    # Integrity: M1 must reproduce the frozen single-stage taper (D6 condition B).
    reference_meter = FeatureMeter(bank)
    reference = soft_taper(query, candidates, parameters, reference_meter)
    equivalence_diff = max(
        abs(stage_1.activation[doc_id] - reference.activation[doc_id])
        for doc_id in reference.activation
    )

    cue = _reopen_cue(query)
    if cue is None:
        return MT1QueryOutcome(
            query_id=query.query_id,
            transition_evaluable=False,
            ndcg=ndcg,
            feature_evaluations=evaluations,
            feature_nanoseconds=nanoseconds,
            single_stage_equivalence_max_abs_diff=equivalence_diff,
        )

    def partial_stage(meter: FeatureMeter) -> TaperResult:
        return soft_stage(
            query,
            candidates,
            parameters,
            meter,
            prior=_cue_prior(query, field_ids, meter, cue),
            cue=cue,
            cycles_per_channel=MULTI_STAGE_CYCLES,
        )

    # --- M2: multi-soft with naive carry (pathology control) ------------------------
    meter_2 = FeatureMeter(bank)
    first_2 = partial_stage(meter_2)
    second_2 = soft_stage(
        query,
        candidates,
        parameters,
        meter_2,
        prior=dict(first_2.activation),
        cue=None,
        cycles_per_channel=MULTI_STAGE_CYCLES,
    )
    ndcg["M2_multi_naive_carry"] = ndcg_at_k(_ranking_from(second_2.activation), judged, 10)
    evaluations["M2_multi_naive_carry"] = meter_2.evaluations
    nanoseconds["M2_multi_naive_carry"] = meter_2.nanoseconds

    # --- M3: reset activation, retain narrowing (primary treatment) -----------------
    meter_3 = FeatureMeter(bank)
    first_3 = partial_stage(meter_3)
    second_3 = soft_stage(
        query,
        candidates,
        parameters,
        meter_3,
        prior=dict(retrieval_prior),
        cue=None,
        cycles_per_channel=MULTI_STAGE_CYCLES,
        active_ceiling=first_3.active,
    )
    ndcg["M3_multi_reset_narrowed"] = ndcg_at_k(_ranking_from(second_3.activation), judged, 10)
    evaluations["M3_multi_reset_narrowed"] = meter_3.evaluations
    nanoseconds["M3_multi_reset_narrowed"] = meter_3.nanoseconds

    # --- M4: full reset (wasted-stage sanity control) -------------------------------
    meter_4 = FeatureMeter(bank)
    partial_stage(meter_4)
    second_4 = soft_stage(
        query,
        candidates,
        parameters,
        meter_4,
        prior=dict(retrieval_prior),
        cue=None,
        cycles_per_channel=MULTI_STAGE_CYCLES,
    )
    ndcg["M4_multi_full_reset"] = ndcg_at_k(_ranking_from(second_4.activation), judged, 10)
    evaluations["M4_multi_full_reset"] = meter_4.evaluations
    nanoseconds["M4_multi_full_reset"] = meter_4.nanoseconds

    # --- M5: reversed stage order (order control) -----------------------------------
    meter_5 = FeatureMeter(bank)
    first_5 = soft_stage(
        query,
        candidates,
        parameters,
        meter_5,
        prior=dict(retrieval_prior),
        cue=None,
        cycles_per_channel=MULTI_STAGE_CYCLES,
    )
    second_5 = soft_stage(
        query,
        candidates,
        parameters,
        meter_5,
        prior=_cue_prior(query, field_ids, meter_5, cue),
        cue=cue,
        cycles_per_channel=MULTI_STAGE_CYCLES,
        active_ceiling=first_5.active,
    )
    ndcg["M5_reversed_order"] = ndcg_at_k(_ranking_from(second_5.activation), judged, 10)
    evaluations["M5_reversed_order"] = meter_5.evaluations
    nanoseconds["M5_reversed_order"] = meter_5.nanoseconds

    # --- M6: matched-compute hard staged pruning (reversibility control) ------------
    meter_6 = FeatureMeter(bank)
    first_6 = partial_stage(meter_6)
    survivors = [
        doc_id for doc_id, _ in _ranked(first_6.activation)[:RECURRENCE_WIDTH]
    ]
    survivor_candidates = [(doc_id, score) for doc_id, score in candidates if doc_id in set(survivors)]
    second_6 = soft_stage(
        query,
        survivor_candidates,
        parameters,
        meter_6,
        prior=_restricted_prior(retrieval_prior, survivors),
        cue=None,
        cycles_per_channel=MULTI_STAGE_CYCLES,
        minimum_active=min(RECURRENCE_WIDTH, len(survivors)),
    )
    ndcg["M6_hard_staged_prune"] = ndcg_at_k(
        _hard_pruned_ranking(second_6.activation, field_ids), judged, 10
    )
    evaluations["M6_hard_staged_prune"] = meter_6.evaluations
    nanoseconds["M6_hard_staged_prune"] = meter_6.nanoseconds

    return MT1QueryOutcome(
        query_id=query.query_id,
        transition_evaluable=True,
        ndcg=ndcg,
        feature_evaluations=evaluations,
        feature_nanoseconds=nanoseconds,
        single_stage_equivalence_max_abs_diff=equivalence_diff,
    )


def classify_mt1(
    *,
    transition_queries: int,
    delta: float,
    ci_low: float,
    compute_ratio: float,
    single_stage_equivalence_ok: bool,
) -> str:
    """Apply only the frozen MT-1 interpretation categories."""

    if not single_stage_equivalence_ok:
        return "INVALID_SINGLE_STAGE_CONTROL"
    if transition_queries < MIN_TRANSITION_QUERIES:
        return "INCONCLUSIVE"
    # A loss is a loss regardless of budget: extra compute cannot excuse it.
    if delta <= 0.0 or ci_low <= 0.0:
        return "MULTI_STAGE_NOT_SUPPORTED"
    if compute_ratio > COMPUTE_TOLERANCE:
        return "COMPUTE_UNMATCHED"
    if delta >= MATERIAL_DELTA:
        return "MULTI_STAGE_SUPPORTED"
    return "MULTI_STAGE_IMMATERIAL"


def _paired(rows: Sequence[MT1QueryOutcome], left: str, right: str) -> dict[str, float]:
    return paired_bootstrap(
        [row.ndcg[left] for row in rows],
        [row.ndcg[right] for row in rows],
    )


def run_mt1(dataset: Dataset) -> dict[str, object]:
    """Run MT-1 on development only; non-SciFact external datasets are rejected."""

    if not dataset.synthetic:
        raise RuntimeError(
            "MT-1 v1 is UNEXECUTED / DESIGN-INVALID and must not produce a development "
            "result. Its treatment condition cannot satisfy its own matched-compute rule "
            "(E(M3) ~= 2.285 * E(M1) against a 1.10 tolerance), so MULTI_STAGE_SUPPORTED "
            "is structurally unreachable. See docs/MT1_DESIGN_AUDIT.md; the replacement "
            "design is docs/CPN1_PREREGISTRATION.md."
        )

    index, bank = build_environment(dataset)
    development = queries_for_split(dataset, "development")
    if not development:
        raise ValueError("development split is empty")
    if not dataset.synthetic and len(development) != EXPECTED_SCIFACT_DEVELOPMENT_QUERIES:
        raise ValueError(
            "Frozen MT-1 expects exactly 93 SciFact development queries; "
            f"received {len(development)}."
        )

    parameters = learn_parameters(dataset, bank, index, development=development)
    rows = [run_query(dataset, index, bank, parameters, query) for query in development]
    transition_rows = [row for row in rows if row.transition_evaluable]

    all_development = {
        condition: round(mean(row.ndcg[condition] for row in rows), 6)
        for condition in ("M0_bm25_anchor", "M1_single_full_soft")
    }
    paired_means = {
        condition: round(mean(row.ndcg[condition] for row in transition_rows), 6)
        if transition_rows
        else 0.0
        for condition in CONDITIONS
    }

    primary = _paired(transition_rows, *PRIMARY_COMPARISON) if transition_rows else {
        "delta": 0.0, "ci_low": 0.0, "ci_high": 0.0, "p_greater": 0.0
    }
    secondary = {
        f"{left}_minus_{right}": _paired(transition_rows, left, right)
        for left, right in SECONDARY_COMPARISONS
    } if transition_rows else {}

    compute = {
        condition: {
            "mean_feature_evaluations": round(
                mean(row.feature_evaluations[condition] for row in transition_rows), 3
            )
            if transition_rows
            else 0.0,
            "mean_feature_microseconds": round(
                mean(row.feature_nanoseconds[condition] / 1000.0 for row in transition_rows), 3
            )
            if transition_rows
            else 0.0,
        }
        for condition in CONDITIONS
    }

    baseline_cost = compute["M1_single_full_soft"]["mean_feature_evaluations"]
    treatment_cost = compute["M3_multi_reset_narrowed"]["mean_feature_evaluations"]
    compute_ratio = treatment_cost / baseline_cost if baseline_cost > 0.0 else math.inf

    equivalence_values = [
        row.single_stage_equivalence_max_abs_diff
        for row in rows
        if row.single_stage_equivalence_max_abs_diff is not None
    ]
    max_equivalence_diff = max(equivalence_values) if equivalence_values else 0.0
    equivalence_ok = max_equivalence_diff <= 1e-12

    classification = classify_mt1(
        transition_queries=len(transition_rows),
        delta=primary["delta"],
        ci_low=primary["ci_low"],
        compute_ratio=compute_ratio,
        single_stage_equivalence_ok=equivalence_ok,
    )

    if dataset.synthetic:
        verdict = f"NOT EVIDENCE: synthetic mechanism check; classification={classification}."
    else:
        verdict = classification

    return {
        "experiment": MT1_ID,
        "dataset": dataset.name,
        "synthetic": dataset.synthetic,
        "split": "development",
        "development_queries": len(development),
        "transition_evaluable_queries": len(transition_rows),
        "minimum_transition_queries": MIN_TRANSITION_QUERIES,
        "nominal_sweeps_per_condition": NOMINAL_SWEEPS,
        "parameters": parameters.to_dict(),
        "all_development_ndcg10": all_development,
        "paired_transition_ndcg10": paired_means,
        "primary_effect": {
            "comparison": f"{PRIMARY_COMPARISON[0]}_minus_{PRIMARY_COMPARISON[1]}",
            **primary,
        },
        "secondary_effects": secondary,
        "paired_compute": compute,
        "compute_ratio_M3_over_M1": round(compute_ratio, 6),
        "compute_tolerance": COMPUTE_TOLERANCE,
        "material_delta": MATERIAL_DELTA,
        "single_stage_equivalence_max_abs_diff": max_equivalence_diff,
        "single_stage_equivalence_ok": equivalence_ok,
        "classification": classification,
        "verdict": verdict,
        "per_query": [row.to_dict() for row in rows],
        "scope_note": (
            "Development-only matched-compute stage-necessity test. No recurrence, no "
            "Token Deck input, no final split, and no post-hoc threshold changes are "
            "permitted."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="MT-1 matched-compute multi-taper falsification")
    parser.add_argument("--data", help="Unzipped BEIR SciFact dataset directory")
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Run a synthetic mechanism check; output is explicitly not evidence.",
    )
    args = parser.parse_args()

    if args.smoke:
        from experiments.ext2_diagnostics import make_hard_corpus

        dataset = make_hard_corpus(seed=31, clusters=30, queries=140, informative_features=True)
    elif args.data:
        dataset = load_beir_dataset(args.data)
    else:
        parser.error("provide --data <SciFact folder> or --smoke")

    print(json.dumps(run_mt1(dataset), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
