from __future__ import annotations

import pytest

import math
from experiments.ext2_diagnostics import (
    anchored_taper, d1_prior_retention, d3_residual_signal,
    d5_oracle_ceiling, make_hard_corpus, spearman,
)
from experiments.external_retrieval_cascade import (
    FeatureMeter, build_environment, learn_parameters, queries_for_split, soft_taper,
)

pytestmark = pytest.mark.scientific


def env(informative=True):
    dataset = make_hard_corpus(seed=23, clusters=24, queries=120, informative_features=informative)
    index, bank = build_environment(dataset)
    dev = queries_for_split(dataset, "development")
    params = learn_parameters(dataset, bank, index, development=dev)
    return dataset, index, bank, params, dev


def test_spearman_ties_are_average_ranked():
    assert math.isclose(spearman([1, 1, 2], [1, 1, 2]), 1.0)
    assert math.isclose(spearman([1, 1, 2], [2, 2, 1]), -1.0)


def test_gamma_zero_exactly_reproduces_ext1_soft_taper():
    dataset, index, bank, params, dev = env()
    q = dev[0]
    candidates = index.top_candidates(q.tokens, 100)
    expected = soft_taper(q, candidates, params, FeatureMeter(bank)).activation
    actual = anchored_taper(q, candidates, params, FeatureMeter(bank), gamma=0.0)
    assert actual.keys() == expected.keys()
    for doc_id in actual:
        assert math.isclose(actual[doc_id], expected[doc_id], rel_tol=1e-12, abs_tol=1e-15)


def test_d1_is_coefficients_not_information_share():
    p = d1_prior_retention().payload
    assert p["ext1_retained_initial_log_coefficient"] == 0.4305
    assert p["coefficient_ratio_updates_to_retained_initial"] == 13.23
    assert p["proposed_anchor_space"] == "activation"


def test_d3_finds_known_proximity_signal_on_bm25_errors():
    dataset, index, bank, params, dev = env(True)
    p = d3_residual_signal(dataset, index, bank, params, dev).payload
    assert p["bm25_error_pairs"] > 0
    assert p["mean_channel_delta_on_bm25_errors"][2] > 0
    assert p["channel_win_rate_on_bm25_errors"][2] > 0.5
    assert p["degenerate_no_channel_adds_signal"] is False


def test_d5_is_corpus_dependent_and_oracle_is_upper_bound():
    dataset, index, _, _, dev = env()
    p = d5_oracle_ceiling(dataset, index, dev)
    assert p.corpus_dependent is True
    assert p.payload["oracle_ndcg10"] >= p.payload["bm25_ndcg10"]
