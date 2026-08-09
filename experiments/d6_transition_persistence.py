"""D6: isolate partial -> full context transition persistence on SciFact development.

This module implements the frozen protocol in ``docs/D6_PREREGISTRATION.md``.
It has no final-split option, invokes no recurrence, and treats synthetic runs as
mechanism smoke tests only.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from statistics import mean
from typing import Sequence
import argparse
import json
import math

from synrheon.contextual_search import ReversibleCandidateField

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

D6_ID = "d6-transition-persistence-v1"
MIN_TRANSITION_QUERIES = 30
EXPECTED_SCIFACT_DEVELOPMENT_QUERIES = 93
CONDITIONS = ("A_bm25", "B_full_soft", "C_carry", "D_reset", "E_residual")


@dataclass(frozen=True, slots=True)
class D6QueryOutcome:
    query_id: str
    transition_evaluable: bool
    ndcg: dict[str, float]
    feature_evaluations: dict[str, int]
    feature_nanoseconds: dict[str, int]
    reset_state_max_abs_diff: float | None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def residual_taper(
    query: Query,
    candidates: Sequence[tuple[str, float]],
    parameters: LearnedParameters,
    meter: FeatureMeter,
    *,
    prior: dict[str, float],
    partial_cue: tuple[str, ...],
) -> TaperResult:
    """Stage-two taper using only full-minus-partial feature residuals.

    This is the exact D6-E operationalization. It preserves the existing taper
    dynamics and changes only the feature term. Negative residual evidence is kept.
    """

    activation = dict(prior)
    for doc_id, _ in candidates:
        activation.setdefault(doc_id, 0.0)
    active = {doc_id for doc_id, _ in candidates}
    counts: list[int] = []

    for channel in parameters.channel_order:
        gain = parameters.channel_gains[channel]
        for _ in range(TAPER_STAGE_CYCLES):
            updated = dict(activation)
            for doc_id in active:
                full_value = meter.value(query, doc_id, channel)
                partial_value = meter.value(query, doc_id, channel, cue=partial_cue)
                residual_value = full_value - partial_value
                updated[doc_id] = (
                    max(activation[doc_id], DORMANT_FLOOR) ** 0.90
                    * math.exp(gain * residual_value / TAPER_TEMPERATURE)
                )
            activation = _normalize(updated)

        peak = max(activation.values()) if activation else 0.0
        eligible = {
            doc_id
            for doc_id, value in activation.items()
            if value >= peak * TAPER_RELATIVE_GATE
        }
        if len(eligible) < RECURRENCE_WIDTH:
            eligible = {
                doc_id for doc_id, _ in _ranked(activation)[:RECURRENCE_WIDTH]
            }
        active = eligible
        counts.append(len(active))

    return TaperResult(
        activation=activation,
        active=tuple(sorted(active)),
        dormant=tuple(sorted(set(activation) - active)),
        stage_active_counts=tuple(counts),
    )


def _rank_ndcg(activation: dict[str, float], judged: dict[str, int]) -> float:
    return ndcg_at_k([doc_id for doc_id, _ in _ranked(activation)], judged, 10)


def _field_from_candidates(candidates: Sequence[tuple[str, float]]) -> ReversibleCandidateField:
    return ReversibleCandidateField(_initial_activation(candidates))


def _run_partial_stage(
    query: Query,
    candidates: Sequence[tuple[str, float]],
    parameters: LearnedParameters,
    meter: FeatureMeter,
    cue: tuple[str, ...],
) -> tuple[ReversibleCandidateField, TaperResult]:
    field = _field_from_candidates(candidates)
    field.record_checkpoint(context_id="full-query-retrieval-prior", transition="reset")
    partial = soft_taper(
        query,
        candidates,
        parameters,
        meter,
        prior=_cue_prior(query, [doc_id for doc_id, _ in candidates], meter, cue),
        cue=cue,
    )
    field.replace_activation(
        partial.activation,
        context_id="partial-context-settled",
        transition="carry",
        active_ids=partial.active,
    )
    return field, partial


def run_query(
    dataset: Dataset,
    index: BM25Index,
    bank: ChannelBank,
    parameters: LearnedParameters,
    query: Query,
) -> D6QueryOutcome:
    judged = dataset.qrels.get(query.query_id, {})
    candidates = index.top_candidates(query.tokens, CANDIDATE_DEPTH)
    field_ids = [doc_id for doc_id, _ in candidates]
    if not candidates:
        return D6QueryOutcome(
            query_id=query.query_id,
            transition_evaluable=False,
            ndcg={condition: 0.0 for condition in CONDITIONS},
            feature_evaluations={condition: 0 for condition in CONDITIONS},
            feature_nanoseconds={condition: 0 for condition in CONDITIONS},
            reset_state_max_abs_diff=None,
        )

    ndcg: dict[str, float] = {}
    evaluations = {condition: 0 for condition in CONDITIONS}
    nanoseconds = {condition: 0 for condition in CONDITIONS}

    ndcg["A_bm25"] = ndcg_at_k(field_ids, judged, 10)

    meter_b = FeatureMeter(bank)
    taper_b = soft_taper(query, candidates, parameters, meter_b)
    ndcg["B_full_soft"] = _rank_ndcg(taper_b.activation, judged)
    evaluations["B_full_soft"] = meter_b.evaluations
    nanoseconds["B_full_soft"] = meter_b.nanoseconds

    cue = _reopen_cue(query)
    if cue is None:
        ndcg.update({"C_carry": 0.0, "D_reset": 0.0, "E_residual": 0.0})
        return D6QueryOutcome(
            query_id=query.query_id,
            transition_evaluable=False,
            ndcg=ndcg,
            feature_evaluations=evaluations,
            feature_nanoseconds=nanoseconds,
            reset_state_max_abs_diff=None,
        )

    meter_c = FeatureMeter(bank)
    field_c, _ = _run_partial_stage(query, candidates, parameters, meter_c, cue)
    taper_c = soft_taper(
        query,
        candidates,
        parameters,
        meter_c,
        prior=field_c.prior_for("carry"),
    )
    field_c.replace_activation(
        taper_c.activation,
        context_id="full-context-carried",
        transition="carry",
        active_ids=taper_c.active,
    )
    ndcg["C_carry"] = _rank_ndcg(field_c.activation, judged)
    evaluations["C_carry"] = meter_c.evaluations
    nanoseconds["C_carry"] = meter_c.nanoseconds

    meter_d = FeatureMeter(bank)
    field_d, _ = _run_partial_stage(query, candidates, parameters, meter_d, cue)
    reset_prior = field_d.prior_for("reset")
    taper_d = soft_taper(query, candidates, parameters, meter_d, prior=reset_prior)
    field_d.replace_activation(
        taper_d.activation,
        context_id="full-context-reset",
        transition="reset",
        active_ids=taper_d.active,
    )
    ndcg["D_reset"] = _rank_ndcg(field_d.activation, judged)
    evaluations["D_reset"] = meter_d.evaluations
    nanoseconds["D_reset"] = meter_d.nanoseconds

    reset_diff = max(
        abs(taper_b.activation[doc_id] - field_d.activation[doc_id])
        for doc_id in taper_b.activation
    )

    meter_e = FeatureMeter(bank)
    field_e, _ = _run_partial_stage(query, candidates, parameters, meter_e, cue)
    taper_e = residual_taper(
        query,
        candidates,
        parameters,
        meter_e,
        prior=field_e.prior_for("residual"),
        partial_cue=cue,
    )
    field_e.replace_activation(
        taper_e.activation,
        context_id="full-context-residual",
        transition="residual",
        active_ids=taper_e.active,
    )
    ndcg["E_residual"] = _rank_ndcg(field_e.activation, judged)
    evaluations["E_residual"] = meter_e.evaluations
    nanoseconds["E_residual"] = meter_e.nanoseconds

    return D6QueryOutcome(
        query_id=query.query_id,
        transition_evaluable=True,
        ndcg=ndcg,
        feature_evaluations=evaluations,
        feature_nanoseconds=nanoseconds,
        reset_state_max_abs_diff=reset_diff,
    )


def _paired(rows: Sequence[D6QueryOutcome], left: str, right: str) -> dict[str, float]:
    return paired_bootstrap(
        [row.ndcg[left] for row in rows],
        [row.ndcg[right] for row in rows],
    )


def classify_d6(
    *,
    transition_queries: int,
    damage: float,
    reset_effect: dict[str, float],
    reset_recovery_fraction: float | None,
    reset_integrity_ok: bool,
) -> str:
    """Apply only the frozen D6 interpretation categories."""

    if not reset_integrity_ok:
        return "INVALID_RESET_CONTROL"
    if damage <= 0.0:
        return "DAMAGE_NOT_REPRODUCED"
    if transition_queries < MIN_TRANSITION_QUERIES:
        return "INCONCLUSIVE"
    if reset_recovery_fraction is None:
        return "INCONCLUSIVE"
    if reset_recovery_fraction < 0.25:
        return "PERSISTENCE_INSUFFICIENT"
    if reset_recovery_fraction < 0.50:
        return "PARTIAL_SUPPORT"
    if reset_effect["delta"] > 0.0 and reset_effect["ci_low"] > 0.0:
        return "MAJOR_PERSISTENCE_CONTRIBUTION_SUPPORTED"
    return "INCONCLUSIVE"


def run_d6(dataset: Dataset) -> dict[str, object]:
    """Run D6 on development only; non-SciFact external datasets are rejected."""

    if not dataset.synthetic and dataset.name.lower() != "scifact":
        raise ValueError("D6 is frozen for the SciFact development dataset only.")

    index, bank = build_environment(dataset)
    development = queries_for_split(dataset, "development")
    if not development:
        raise ValueError("development split is empty")
    if not dataset.synthetic and len(development) != EXPECTED_SCIFACT_DEVELOPMENT_QUERIES:
        raise ValueError(
            "Frozen D6 expects exactly 93 SciFact development queries; "
            f"received {len(development)}."
        )

    parameters = learn_parameters(dataset, bank, index, development=development)
    rows = [run_query(dataset, index, bank, parameters, query) for query in development]
    transition_rows = [row for row in rows if row.transition_evaluable]

    all_dev_means = {
        condition: round(mean(row.ndcg[condition] for row in rows), 6)
        for condition in ("A_bm25", "B_full_soft")
    }
    paired_means = {
        condition: round(mean(row.ndcg[condition] for row in transition_rows), 6)
        if transition_rows
        else 0.0
        for condition in CONDITIONS
    }

    b_minus_c = _paired(transition_rows, "B_full_soft", "C_carry")
    d_minus_c = _paired(transition_rows, "D_reset", "C_carry")
    e_minus_c = _paired(transition_rows, "E_residual", "C_carry")
    e_minus_b = _paired(transition_rows, "E_residual", "B_full_soft")

    damage = b_minus_c["delta"]
    reset_fraction = (
        d_minus_c["delta"] / damage if damage > 0.0 else None
    )
    max_reset_diff = max(
        (row.reset_state_max_abs_diff or 0.0) for row in transition_rows
    ) if transition_rows else 0.0
    reset_integrity_ok = max_reset_diff <= 1e-12

    classification = classify_d6(
        transition_queries=len(transition_rows),
        damage=damage,
        reset_effect=d_minus_c,
        reset_recovery_fraction=reset_fraction,
        reset_integrity_ok=reset_integrity_ok,
    )

    paired_cost = {
        condition: {
            "mean_feature_evaluations": round(
                mean(row.feature_evaluations[condition] for row in transition_rows), 3
            ) if transition_rows else 0.0,
            "mean_feature_microseconds": round(
                mean(row.feature_nanoseconds[condition] / 1000.0 for row in transition_rows), 3
            ) if transition_rows else 0.0,
        }
        for condition in CONDITIONS
    }

    if dataset.synthetic:
        verdict = f"NOT EVIDENCE: synthetic mechanism check; diagnostic classification={classification}."
    else:
        verdict = classification

    return {
        "diagnostic": D6_ID,
        "dataset": dataset.name,
        "synthetic": dataset.synthetic,
        "split": "development",
        "development_queries": len(development),
        "transition_evaluable_queries": len(transition_rows),
        "minimum_transition_queries": MIN_TRANSITION_QUERIES,
        "parameters": parameters.to_dict(),
        "all_development_ndcg10": all_dev_means,
        "paired_transition_ndcg10": paired_means,
        "paired_effects": {
            "B_minus_C": b_minus_c,
            "D_minus_C": d_minus_c,
            "E_minus_C": e_minus_c,
            "E_minus_B": e_minus_b,
        },
        "delta_damage": damage,
        "reset_recovery_fraction": reset_fraction,
        "reset_control_max_abs_activation_diff_vs_B": max_reset_diff,
        "reset_control_integrity_ok": reset_integrity_ok,
        "paired_compute": paired_cost,
        "classification": classification,
        "verdict": verdict,
        "per_query": [row.to_dict() for row in rows],
        "scope_note": (
            "Development-only transition isolation. No recurrence, no final split, "
            "and no post-hoc threshold changes are permitted."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="D6 transition persistence diagnostic")
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

    print(json.dumps(run_d6(dataset), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
