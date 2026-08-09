"""Scientific integrity/regression tests for EXT-1."""
from __future__ import annotations

import sys
import pytest
import experiments.external_retrieval_cascade as experiment_module
from experiments.external_retrieval_cascade import (
    CANDIDATE_DEPTH,
    CHANNEL_COUNT,
    CONDITIONS,
    CONTEXTS_PER_QUERY,
    GATE,
    PUBLISHED_BM25_NDCG10,
    RECURRENCE_WIDTH,
    BM25Index,
    ChannelBank,
    Dataset,
    FeatureMeter,
    build_environment,
    build_relations,
    evaluate,
    hard_taper,
    learn_parameters,
    make_document,
    make_smoke_dataset,
    ndcg_at_k,
    paired_bootstrap,
    queries_for_split,
    recall_at_k,
    run_assay,
    run_condition,
    soft_taper,
    split_of,
    summarize,
    verdict,
)

@pytest.fixture(scope="module")
def environment():
    dataset = make_smoke_dataset()
    index, bank = build_environment(dataset)
    development = queries_for_split(dataset, "development")
    parameters = learn_parameters(dataset, bank, index, development=development)
    return dataset, index, bank, parameters


def test_final_split_is_disjoint_and_stable() -> None:
    dataset = make_smoke_dataset()
    development = {q.query_id for q in queries_for_split(dataset, "development")}
    final = {q.query_id for q in queries_for_split(dataset, "final")}
    assert development and final
    assert development.isdisjoint(final)
    assert development | final == {q.query_id for q in dataset.queries}
    assert split_of("q0001") == split_of("q0001")


def test_environment_calibration_uses_development_queries_only(monkeypatch) -> None:
    dataset = make_smoke_dataset()
    development = {q.query_id for q in queries_for_split(dataset, "development")}
    final = {q.query_id for q in queries_for_split(dataset, "final")}
    seen: list[str] = []
    original = ChannelBank.calibrate
    def watched(self, sample):
        sample = tuple(sample)
        seen.extend(q.query_id for q in sample)
        return original(self, sample)
    monkeypatch.setattr(ChannelBank, "calibrate", watched)
    build_environment(dataset)
    assert seen
    assert set(seen) <= development
    assert not (set(seen) & final)


def test_ranking_ties_break_on_identifier_only(environment) -> None:
    dataset, index, bank, _ = environment
    query = queries_for_split(dataset, "final")[0]
    candidates = index.top_candidates(query.tokens, CANDIDATE_DEPTH)
    tied = {doc_id: 0.5 for doc_id, _ in candidates}
    ranked = experiment_module._ranked(tied)
    assert [doc_id for doc_id, _ in ranked] == sorted(tied)
    assert experiment_module._ranked(dict(reversed(list(tied.items())))) == ranked


def test_relations_are_answer_free_symmetric_and_self_free(environment) -> None:
    dataset, index, _, _ = environment
    survivors = [doc.doc_id for doc in dataset.documents[:24]]
    original = build_relations(dataset.by_id, survivors, index)
    poisoned = Dataset(dataset.name, dataset.synthetic, dataset.documents, dataset.queries,
                       {query_id: {} for query_id in dataset.qrels})
    assert build_relations(poisoned.by_id, survivors, index) == original
    assert all(left != right for left, right in original)
    for (left, right), weight in original.items():
        assert original[(right, left)] == weight


def test_learning_never_reads_final_qrels(environment) -> None:
    dataset, index, bank, _ = environment
    development = queries_for_split(dataset, "development")
    final_ids = {q.query_id for q in queries_for_split(dataset, "final")}
    touched: list[str] = []
    original_qrels = dataset.qrels
    class Watcher(dict):
        def get(self, key, default=None):
            touched.append(key)
            return original_qrels.get(key, default)
    watched = Dataset(dataset.name, dataset.synthetic, dataset.documents, dataset.queries,
                      Watcher(original_qrels))
    learn_parameters(watched, bank, index, development=development)
    assert not (set(touched) & final_ids)


def test_feature_meter_memoizes_invariants_and_uses_deterministic_key(environment) -> None:
    dataset, _, bank, _ = environment
    query = queries_for_split(dataset, "final")[0]
    doc_id = dataset.documents[0].doc_id
    meter = FeatureMeter(bank)
    first = meter.value(query, doc_id, 0)
    for _ in range(20):
        assert meter.value(query, doc_id, 0) == first
    assert meter.requests == 21
    assert meter.evaluations == 1
    assert next(iter(meter._cache)) == (doc_id, 0, query.tokens)


def test_cost_is_measured_and_full_rerank_is_not_handicapped(environment) -> None:
    dataset, index, bank, parameters = environment
    query = queries_for_split(dataset, "final")[0]
    full = run_condition(dataset, index, bank, parameters, query, "full_rerank")
    learned = run_condition(dataset, index, bank, parameters, query, "learned_order_taper")
    bm25 = run_condition(dataset, index, bank, parameters, query, "bm25_only")
    assert bm25.evaluations == 0
    assert full.evaluations > 0 and full.nanoseconds > 0
    assert learned.evaluations > 0 and learned.nanoseconds > 0
    assert full.evaluations <= CONTEXTS_PER_QUERY * CANDIDATE_DEPTH * CHANNEL_COUNT


def test_control_and_cascade_face_same_information_arrival(environment) -> None:
    dataset, index, bank, parameters = environment
    for query in queries_for_split(dataset, "final")[:6]:
        cue = experiment_module._reopen_cue(query)
        if cue is None:
            continue
        control = run_condition(dataset, index, bank, parameters, query, "full_rerank")
        cascade = run_condition(dataset, index, bank, parameters, query, "learned_order_taper")
        assert control.evaluations > CANDIDATE_DEPTH * CHANNEL_COUNT
        assert cascade.evaluations > 0


def test_soft_taper_is_reversible_while_hard_taper_deletes(environment) -> None:
    dataset, index, bank, parameters = environment
    query = queries_for_split(dataset, "final")[0]
    candidates = index.top_candidates(query.tokens, CANDIDATE_DEPTH)
    soft = soft_taper(query, candidates, parameters, FeatureMeter(bank))
    hard = hard_taper(query, candidates, parameters, FeatureMeter(bank))
    assert set(soft.activation) == {doc_id for doc_id, _ in candidates}
    assert soft.dormant
    assert all(soft.activation[doc_id] > 0.0 for doc_id in soft.dormant)
    assert len(soft.active) >= RECURRENCE_WIDTH
    assert len(hard.activation) == RECURRENCE_WIDTH
    assert hard.dormant == ()


def test_reopening_resumes_dormant_state_not_full_restart(environment) -> None:
    dataset, index, bank, parameters = environment
    query = queries_for_split(dataset, "final")[0]
    candidates = index.top_candidates(query.tokens, CANDIDATE_DEPTH)
    first = soft_taper(query, candidates, parameters, FeatureMeter(bank))
    resumed = soft_taper(query, candidates, parameters, FeatureMeter(bank), prior=first.activation)
    fresh = soft_taper(query, candidates, parameters, FeatureMeter(bank))
    assert resumed.activation != fresh.activation
    assert set(resumed.activation) == set(first.activation)


def test_reopening_probe_is_relevance_free(environment) -> None:
    dataset, _, _, _ = environment
    query = queries_for_split(dataset, "final")[0]
    cue = experiment_module._reopen_cue(query)
    assert cue == query.tokens[:len(query.tokens)//2]


def test_recurrence_ablation_changes_only_downstream_stage(environment) -> None:
    dataset, index, bank, parameters = environment
    queries = queries_for_split(dataset, "final")[:12]
    with_rec = [run_condition(dataset, index, bank, parameters, q, "learned_order_taper") for q in queries]
    without = [run_condition(dataset, index, bank, parameters, q, "learned_order_no_recurrence") for q in queries]
    assert [row.evaluations for row in with_rec] == [row.evaluations for row in without]


def test_metrics_and_bootstrap_are_sane() -> None:
    judged = {"a": 1, "b": 1}
    assert ndcg_at_k(["a", "b", "c"], judged, 10) == pytest.approx(1.0)
    assert 0.0 < ndcg_at_k(["c", "a", "b"], judged, 10) < 1.0
    assert recall_at_k(["a", "x"], judged, 100) == pytest.approx(0.5)
    interval = paired_bootstrap([0.5] * 40, [0.5] * 40)
    assert interval["ci_low"] <= 0.0 <= interval["ci_high"]


def test_gate_and_external_anchors_are_frozen() -> None:
    assert GATE == {
        "local_bm25_vs_published_min_ratio": 0.90,
        "learned_ndcg_vs_bm25_min_delta": 0.0,
        "learned_ndcg_vs_full_rerank_min_delta": -0.01,
        "learned_cost_fraction_vs_full_rerank_max": 0.50,
        "learned_vs_fixed_order_cost_advantage_min": 0.03,
        "reopen_recovery_advantage_vs_hard_min": 0.10,
        "reopen_probe_cases_min": 30,
        "abstention_precision_gain_min": 0.05,
        "empty_field_abstain_rate_min": 0.50,
    }
    assert PUBLISHED_BM25_NDCG10["scifact"] == 0.665
    assert PUBLISHED_BM25_NDCG10["nfcorpus"] == 0.325


def test_synthetic_corpus_can_never_be_evidence(environment) -> None:
    dataset, index, bank, parameters = environment
    queries = queries_for_split(dataset, "final")
    results = evaluate(dataset, index, bank, parameters, queries)
    summaries = {name: summarize(rows) for name, rows in results.items()}
    decision, checks = verdict(dataset, results, summaries)
    assert decision.startswith("NOT EVIDENCE")
    assert set(checks["claim_status"]) == {"C1", "C2", "C3"}


def test_unknown_external_dataset_cannot_pass_anchor(environment) -> None:
    dataset, index, bank, parameters = environment
    queries = queries_for_split(dataset, "final")
    results = evaluate(dataset, index, bank, parameters, queries)
    summaries = {name: summarize(rows) for name, rows in results.items()}
    external = Dataset("unanchored-external", False, dataset.documents, dataset.queries, dataset.qrels)
    _, checks = verdict(external, results, summaries)
    assert checks["local_bm25_vs_published_pass"] is False
    assert checks["claim_status"]["C1"] == "DISCOUNTED"


def test_c2_and_c3_report_uncertainty_intervals(environment) -> None:
    dataset, index, bank, parameters = environment
    queries = queries_for_split(dataset, "final")
    results = evaluate(dataset, index, bank, parameters, queries)
    summaries = {name: summarize(rows) for name, rows in results.items()}
    external = Dataset("scifact", False, dataset.documents, dataset.queries, dataset.qrels)
    _, checks = verdict(external, results, summaries)
    for key in ("reopen_recovery_bootstrap", "abstention_precision_gain_bootstrap"):
        interval = checks[key]
        assert set(interval) >= {"delta", "ci_low", "ci_high"}
        assert interval["ci_low"] <= interval["ci_high"]
    if checks["reopen_cases"] < GATE["reopen_probe_cases_min"]:
        assert checks["claim_status"]["C2"] == "INCONCLUSIVE"


def test_partial_final_runs_are_forbidden() -> None:
    with pytest.raises(ValueError, match="partial final runs are forbidden"):
        run_assay(dataset=make_smoke_dataset(), split="final", limit=5)


def test_cli_limit_requires_development(monkeypatch) -> None:
    monkeypatch.setattr(sys, "argv", ["ext1", "--smoke", "--limit", "5"])
    with pytest.raises(SystemExit):
        experiment_module.main()


def test_every_condition_is_reported(environment) -> None:
    dataset, index, bank, parameters = environment
    queries = queries_for_split(dataset, "final")[:6]
    results = evaluate(dataset, index, bank, parameters, queries)
    assert set(results) == set(CONDITIONS)
    assert all(len(rows) == len(queries) for rows in results.values())


def test_learned_parameters_contain_no_candidate_identity(environment) -> None:
    _, _, _, parameters = environment
    assert len(parameters.channel_gains) == CHANNEL_COUNT
    assert sorted(parameters.channel_order) == list(range(CHANNEL_COUNT))
    assert all(cost > 0.0 for cost in parameters.channel_unit_cost_ns)
    assert set(parameters.to_dict()) == {"channel_gains", "channel_unit_cost_ns", "channel_order", "commit_margin"}


def test_bm25_known_ranking() -> None:
    docs = [
        make_document("d0", "cardiac arrest", "myocardial infarction outcomes in adults"),
        make_document("d1", "plant biology", "photosynthesis in maize under drought"),
        make_document("d2", "cardiac imaging", "myocardial perfusion imaging protocols"),
    ]
    ranked = BM25Index(docs).top_candidates(("myocardial", "infarction"), 3)
    assert ranked[0][0] == "d0"
    assert {doc_id for doc_id, _ in ranked[:2]} == {"d0", "d2"}
