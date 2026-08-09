"""EXT-2 development diagnostics for the EXT-1 failure.

This module diagnoses mechanisms only. It never evaluates a reserved final split.
D1 is arithmetic; D2-D5 are corpus-dependent and must be interpreted on development.
"""
from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Sequence
import argparse
import json
import math
import random

from experiments.external_retrieval_cascade import (
    BM25Index,
    CANDIDATE_DEPTH,
    CHANNEL_COUNT,
    CHANNEL_NAMES,
    DORMANT_FLOOR,
    RECURRENCE_WIDTH,
    TAPER_RELATIVE_GATE,
    TAPER_STAGE_CYCLES,
    TAPER_TEMPERATURE,
    ChannelBank,
    Dataset,
    FeatureMeter,
    LearnedParameters,
    Query,
    _initial_activation,
    _normalize,
    _ranked,
    build_environment,
    build_relations,
    learn_parameters,
    make_document,
    ndcg_at_k,
    queries_for_split,
)

DIAGNOSTIC_ID = "ext2-diagnostics-v2"
GAMMA_GRID = (0.0, 0.25, 0.5, 1.0, 2.0, 4.0)


@dataclass(frozen=True, slots=True)
class Probe:
    name: str
    corpus_dependent: bool
    payload: dict[str, object]


def make_hard_corpus(*, seed: int = 11, clusters: int = 90, queries: int = 300,
                     informative_features: bool = True) -> Dataset:
    """Synthetic mechanism demo only; never evidence for EXT-1/EXT-2."""
    rng = random.Random(seed)
    common = [f"common{i:02d}" for i in range(14)]
    rare = [f"rare{i:04d}" for i in range(1400)]
    documents = []
    phrases: dict[str, tuple[str, ...]] = {}
    groups: list[list[str]] = []
    for cluster in range(clusters):
        shared_common = rng.sample(common, 5)
        shared_rare = rng.sample(rare, 15)
        members = []
        for member in range(5):
            phrase = tuple(shared_rare[member * 3:member * 3 + 3])
            tail = [t for t in shared_rare if t not in phrase] + rng.sample(rare, rng.randrange(10, 26))
            rng.shuffle(tail)
            doc_id = f"d{cluster:03d}_{member}"
            documents.append(make_document(doc_id, f"title {shared_common[0]}", " ".join(shared_common + list(phrase) + tail)))
            phrases[doc_id] = phrase
            members.append(doc_id)
        groups.append(members)

    by_id = {d.doc_id: d for d in documents}
    qlist: list[Query] = []
    qrels: dict[str, dict[str, int]] = {}
    for i in range(queries):
        members = groups[rng.randrange(len(groups))]
        target = members[rng.randrange(len(members))]
        generic = [t for t in by_id[target].tokens if t.startswith("common")][:2]
        if informative_features:
            tokens = tuple(generic + list(phrases[target]))
        else:
            decoy = next(m for m in members if m != target)
            marker = f"marker{i:04d}"
            d = by_id[target]
            by_id[target] = make_document(target, "", f"{d.text} {marker}")
            tokens = tuple(generic + list(phrases[decoy]) + [marker])
        qid = f"q{i:04d}"
        qlist.append(Query(qid, " ".join(tokens), tokens))
        qrels[qid] = {target: 1}

    documents = [by_id[d.doc_id] for d in documents]
    name = "hard-smoke-informative" if informative_features else "hard-smoke-noisy"
    return Dataset(name, True, tuple(documents), tuple(qlist), qrels)


def anchored_taper(query: Query, candidates: Sequence[tuple[str, float]],
                   parameters: LearnedParameters, meter: FeatureMeter, *, gamma: float,
                   order: Sequence[int] | None = None,
                   gains: Sequence[float] | None = None) -> dict[str, float]:
    """EXT-1 soft taper plus gamma*initial activation in activation space.

    gamma=0 reproduces EXT-1. The prior term is added to every candidate each cycle,
    while expensive feature evaluation remains limited to the active set.
    """
    stage_order = tuple(parameters.channel_order if order is None else order)
    channel_gains = tuple(parameters.channel_gains if gains is None else gains)
    prior = _initial_activation(candidates)
    activation = dict(prior)
    active = {doc_id for doc_id, _ in candidates}
    for channel in stage_order:
        gain = channel_gains[channel]
        for _ in range(TAPER_STAGE_CYCLES):
            updated = dict(activation)
            for doc_id in active:
                value = meter.value(query, doc_id, channel)
                base = max(activation[doc_id], DORMANT_FLOOR)
                updated[doc_id] = math.exp(0.90 * math.log(base) + gain * value / TAPER_TEMPERATURE)
            if gamma:
                for doc_id, prior_value in prior.items():
                    updated[doc_id] = updated.get(doc_id, 0.0) + gamma * prior_value
            activation = _normalize(updated)
        peak = max(activation.values()) if activation else 0.0
        eligible = {doc_id for doc_id, value in activation.items()
                    if value >= peak * TAPER_RELATIVE_GATE}
        if len(eligible) < RECURRENCE_WIDTH:
            eligible = {doc_id for doc_id, _ in _ranked(activation)[:RECURRENCE_WIDTH]}
        active = eligible
    return activation


def spearman(left: Sequence[float], right: Sequence[float]) -> float:
    """Spearman correlation with average ranks for ties."""
    def ranks(values: Sequence[float]) -> list[float]:
        ordered = sorted(range(len(values)), key=lambda i: values[i])
        out = [0.0] * len(values)
        pos = 0
        while pos < len(ordered):
            end = pos + 1
            value = values[ordered[pos]]
            while end < len(ordered) and values[ordered[end]] == value:
                end += 1
            avg = (pos + end - 1) / 2.0
            for j in range(pos, end):
                out[ordered[j]] = avg
            pos = end
        return out
    a, b = ranks(left), ranks(right)
    if len(a) < 2:
        return 0.0
    ma, mb = mean(a), mean(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    den = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))
    return num / den if den else 0.0


def d1_prior_retention() -> Probe:
    decay = 0.90
    cycles = CHANNEL_COUNT * TAPER_STAGE_CYCLES
    retained = decay ** cycles
    accumulated = sum(decay ** k for k in range(cycles))
    return Probe("D1_prior_retention", False, {
        "cycles": cycles,
        "ext1_retained_initial_log_coefficient": round(retained, 4),
        "accumulated_per_cycle_update_coefficient": round(accumulated, 4),
        "coefficient_ratio_updates_to_retained_initial": round(accumulated / retained, 2),
        "proposed_anchor_space": "activation",
        "gamma_grid": list(GAMMA_GRID),
        "interpretation": "Coefficient ratio only; not an information-share estimate.",
    })


def d2_gamma_sweep(dataset: Dataset, index: BM25Index, bank: ChannelBank,
                   parameters: LearnedParameters, queries: Sequence[Query]) -> Probe:
    bm25 = []
    for q in queries:
        candidates = index.top_candidates(q.tokens, CANDIDATE_DEPTH)
        bm25.append(ndcg_at_k([d for d, _ in candidates], dataset.qrels[q.query_id], 10))
    rows = []
    for gamma in GAMMA_GRID:
        scores, agreements = [], []
        for q in queries:
            candidates = index.top_candidates(q.tokens, CANDIDATE_DEPTH)
            if len(candidates) < 2:
                continue
            activation = anchored_taper(q, candidates, parameters, FeatureMeter(bank), gamma=gamma)
            ranking = [d for d, _ in _ranked(activation)]
            scores.append(ndcg_at_k(ranking, dataset.qrels[q.query_id], 10))
            bscore = dict(candidates)
            agreements.append(spearman([activation[d] for d, _ in candidates],
                                       [bscore[d] for d, _ in candidates]))
        rows.append({"gamma": gamma, "ndcg10": round(mean(scores), 4),
                     "spearman_vs_bm25": round(mean(agreements), 4),
                     "delta_vs_bm25": round(mean(scores) - mean(bm25), 4)})
    best = max(rows, key=lambda row: row["ndcg10"])
    return Probe("D2_gamma_sweep", True, {
        "bm25_ndcg10": round(mean(bm25), 4), "rows": rows,
        "best_gamma": best["gamma"], "best_ndcg10": best["ndcg10"],
    })


def d3_residual_signal(dataset: Dataset, index: BM25Index, bank: ChannelBank,
                       parameters: LearnedParameters, queries: Sequence[Query]) -> Probe:
    deltas: list[list[float]] = [[] for _ in range(CHANNEL_COUNT)]
    error_pairs = 0
    for q in queries:
        candidates = index.top_candidates(q.tokens, CANDIDATE_DEPTH)
        judged = dataset.qrels[q.query_id]
        rank = {doc_id: i for i, (doc_id, _) in enumerate(candidates)}
        relevant = [d for d, _ in candidates if judged.get(d, 0) > 0]
        nonrelevant = [d for d, _ in candidates if judged.get(d, 0) <= 0]
        for rel in relevant:
            rel_values = [bank.compute(q.tokens, rel, c) for c in range(CHANNEL_COUNT)]
            for other in nonrelevant:
                if rank[other] >= rank[rel]:
                    continue
                error_pairs += 1
                for c in range(CHANNEL_COUNT):
                    deltas[c].append(rel_values[c] - bank.compute(q.tokens, other, c))
    means = [mean(v) if v else 0.0 for v in deltas]
    wins = [sum(x > 0 for x in v) / len(v) if v else 0.0 for v in deltas]
    positive = [max(0.0, x) for x in means]
    scale = mean(x for x in positive if x > 0) if any(positive) else 0.0
    gains = [x / scale for x in positive] if scale else [0.0] * CHANNEL_COUNT
    return Probe("D3_residual_signal", True, {
        "bm25_error_pairs": error_pairs,
        "channel_names": list(CHANNEL_NAMES),
        "mean_channel_delta_on_bm25_errors": [round(x, 5) for x in means],
        "channel_win_rate_on_bm25_errors": [round(x, 4) for x in wins],
        "candidate_residual_gains": [round(x, 3) for x in gains],
        "marginal_gains_for_reference": [round(x, 3) for x in parameters.channel_gains],
        "no_bm25_error_pairs": error_pairs == 0,
        "degenerate_no_channel_adds_signal": error_pairs > 0 and not any(x > 0 for x in means),
    })


def d4_connectivity(dataset: Dataset, index: BM25Index, bank: ChannelBank,
                    parameters: LearnedParameters, queries: Sequence[Query], *, gamma: float) -> Probe:
    relevant_scores, other_scores = [], []
    cases = 0
    for q in queries:
        candidates = index.top_candidates(q.tokens, CANDIDATE_DEPTH)
        if len(candidates) < 2:
            continue
        activation = anchored_taper(q, candidates, parameters, FeatureMeter(bank), gamma=gamma)
        survivors = [d for d, _ in _ranked(activation)[:RECURRENCE_WIDTH]]
        judged = dataset.qrels[q.query_id]
        if not any(judged.get(d, 0) > 0 for d in survivors):
            continue
        relations = build_relations(dataset.by_id, survivors, index)
        centrality = {d: mean(relations.get((d, o), 0.0) for o in survivors if o != d)
                      for d in survivors}
        cases += 1
        for d in survivors:
            (relevant_scores if judged.get(d, 0) > 0 else other_scores).append(centrality[d])
    rmean = mean(relevant_scores) if relevant_scores else 0.0
    omean = mean(other_scores) if other_scores else 0.0
    diff = rmean - omean
    return Probe("D4_connectivity", True, {
        "cases": cases, "mean_centrality_relevant": round(rmean, 5),
        "mean_centrality_other": round(omean, 5), "difference": round(diff, 5),
        "implication": "relevance aligns with centrality" if diff > 0 else "centrality points away from relevance",
    })


def d5_oracle_ceiling(dataset: Dataset, index: BM25Index, queries: Sequence[Query]) -> Probe:
    bm25, oracle = [], []
    for q in queries:
        candidates = index.top_candidates(q.tokens, CANDIDATE_DEPTH)
        judged = dataset.qrels[q.query_id]
        field = [d for d, _ in candidates]
        bm25.append(ndcg_at_k(field, judged, 10))
        perfect = sorted(field, key=lambda d: -judged.get(d, 0))
        oracle.append(ndcg_at_k(perfect, judged, 10))
    b, o = mean(bm25), mean(oracle)
    return Probe("D5_oracle_ceiling", True, {
        "bm25_ndcg10": round(b, 4), "oracle_ndcg10": round(o, 4),
        "headroom": round(o - b, 4), "bm25_share_of_ceiling": round(b / o, 4) if o else 0.0,
    })


def run_diagnostics(dataset: Dataset) -> dict[str, object]:
    index, bank = build_environment(dataset)
    development = queries_for_split(dataset, "development")
    if not development:
        raise ValueError("development split is empty")
    parameters = learn_parameters(dataset, bank, index, development=development)
    d1 = d1_prior_retention()
    d5 = d5_oracle_ceiling(dataset, index, development)
    d2 = d2_gamma_sweep(dataset, index, bank, parameters, development)
    gamma = float(d2.payload["best_gamma"])
    d3 = d3_residual_signal(dataset, index, bank, parameters, development)
    d4 = d4_connectivity(dataset, index, bank, parameters, development, gamma=gamma)
    probes = [d1, d2, d3, d4, d5]
    return {
        "diagnostic": DIAGNOSTIC_ID,
        "dataset": dataset.name,
        "synthetic": dataset.synthetic,
        "split": "development",
        "development_queries": len(development),
        "probes": {p.name: {"corpus_dependent": p.corpus_dependent, **p.payload} for p in probes},
        "scope_note": "D1 is corpus-independent. D2-D5 are development-only corpus diagnostics; synthetic runs are mechanism demos, never evidence.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="EXT-2 development diagnostics")
    parser.add_argument("--data", help="Unzipped BEIR dataset directory")
    parser.add_argument("--hard-smoke", choices=["informative", "noisy"])
    args = parser.parse_args()
    if args.hard_smoke:
        dataset = make_hard_corpus(informative_features=args.hard_smoke == "informative")
    elif args.data:
        from experiments.external_retrieval_cascade import load_beir_dataset
        dataset = load_beir_dataset(args.data)
    else:
        parser.error("provide --data <path> or --hard-smoke")
        return
    print(json.dumps(run_diagnostics(dataset), indent=2, default=str))


if __name__ == "__main__":
    main()
