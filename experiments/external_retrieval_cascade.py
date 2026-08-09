"""EXT-1: Ground 0 against external retrieval baselines.

This confirmatory assay moves Synrheon outside the self-authored HCT world family.
Relevance comes from BEIR qrels and is never an inference input. Candidate relations
come from document/document overlap only. Every condition uses an isolated cached
FeatureMeter. Feature work is counted and timed. Development/final assignment is a
stable hash of query id, and partial final runs are forbidden.

The three claims are evaluated independently:
C1 staged narrowing at lower measured feature cost,
C2 reversible recovery after under-specified context,
C3 evidence-gated abstention versus forced commitment.

Synthetic smoke data can exercise code paths but can never return an evidence verdict.
"""
from __future__ import annotations
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from statistics import mean
from typing import Callable, Iterable, Sequence
import argparse
import csv
import hashlib
import json
import math
import random
import re
import time
EXPERIMENT_ID = 'external-retrieval-cascade-v1'
HYPOTHESIS_ID = 'EXT-1'
PUBLISHED_BM25_NDCG10 = {'scifact': 0.665, 'nfcorpus': 0.325, 'scidocs': 0.158, 'arguana': 0.315}
BM25_K1 = 0.9
BM25_B = 0.4
CHANNEL_NAMES = ('lexical_core', 'rare_term_coverage', 'proximity_window', 'char_ngram_semantic')
CHANNEL_COUNT = len(CHANNEL_NAMES)
CANDIDATE_DEPTH = 100
RECURRENCE_WIDTH = 16
RECURRENCE_CYCLES = 6
TAPER_STAGE_CYCLES = 2
TAPER_RELATIVE_GATE = 0.25
TAPER_TEMPERATURE = 0.62
DORMANT_FLOOR = 1e-09
GENERIC_CYCLES = 8
CONTEXTS_PER_QUERY = 2
BOOTSTRAP_RESAMPLES = 1000
BOOTSTRAP_SEED = 90210
CONDITIONS = ('bm25_only', 'full_rerank', 'hard_cascade', 'fixed_order_taper', 'learned_order_taper', 'learned_order_no_recurrence', 'learned_order_no_reopen')
GATE = {'local_bm25_vs_published_min_ratio': 0.9, 'learned_ndcg_vs_bm25_min_delta': 0.0, 'learned_ndcg_vs_full_rerank_min_delta': -0.01, 'learned_cost_fraction_vs_full_rerank_max': 0.5, 'learned_vs_fixed_order_cost_advantage_min': 0.03, 'reopen_recovery_advantage_vs_hard_min': 0.1, 'reopen_probe_cases_min': 30, 'abstention_precision_gain_min': 0.05, 'empty_field_abstain_rate_min': 0.5}
_TOKEN = re.compile('[a-z0-9]+')
_STOPWORDS = frozenset('a an and are as at be by for from has have in is it its of on or that the to was were will with we this these those than then there their they'.split())

def tokenize(text: str) -> tuple[str, ...]:
    return tuple(token for token in _TOKEN.findall(text.lower()) if token not in _STOPWORDS and len(token) > 1)

@dataclass(frozen=True, slots=True)
class Document:
    doc_id: str
    text: str
    tokens: tuple[str, ...]
    token_set: frozenset[str]
    positions: dict[str, tuple[int, ...]]
    char_grams: frozenset[str]

@dataclass(frozen=True, slots=True)
class Query:
    query_id: str
    text: str
    tokens: tuple[str, ...]

@dataclass(frozen=True, slots=True)
class Dataset:
    name: str
    synthetic: bool
    documents: tuple[Document, ...]
    queries: tuple[Query, ...]
    qrels: dict[str, dict[str, int]]
    @property
    def by_id(self) -> dict[str, Document]:
        return {document.doc_id: document for document in self.documents}

def _char_grams(text: str, size: int = 5) -> frozenset[str]:
    cleaned = ' '.join(_TOKEN.findall(text.lower()))
    if len(cleaned) < size:
        return frozenset({cleaned}) if cleaned else frozenset()
    return frozenset(cleaned[index:index + size] for index in range(len(cleaned) - size + 1))

def _positions(tokens: Sequence[str]) -> dict[str, tuple[int, ...]]:
    found: dict[str, list[int]] = defaultdict(list)
    for index, token in enumerate(tokens):
        found[token].append(index)
    return {token: tuple(values) for token, values in found.items()}

def make_document(doc_id: str, title: str, body: str) -> Document:
    text = f'{title} {body}'.strip()
    tokens = tokenize(text)
    return Document(doc_id, text, tokens, frozenset(tokens), _positions(tokens), _char_grams(text))

def load_beir_dataset(folder: str | Path, *, split: str = 'test') -> Dataset:
    root = Path(folder)
    corpus_path = root / 'corpus.jsonl'
    queries_path = root / 'queries.jsonl'
    qrels_path = root / 'qrels' / f'{split}.tsv'
    for path in (corpus_path, queries_path, qrels_path):
        if not path.exists():
            raise FileNotFoundError(f'{path} not found; expected a BEIR-format directory')
    qrels: dict[str, dict[str, int]] = defaultdict(dict)
    with qrels_path.open(encoding='utf-8') as handle:
        reader = csv.reader(handle, delimiter='\t')
        header = next(reader, None)
        if header and header[0].strip().lower() not in {'query-id', 'query_id'}:
            handle.seek(0)
            reader = csv.reader(handle, delimiter='\t')
        for row in reader:
            if len(row) < 3:
                continue
            try:
                value = int(float(row[2]))
            except ValueError:
                continue
            if value > 0:
                qrels[row[0]][row[1]] = value
    documents: list[Document] = []
    with corpus_path.open(encoding='utf-8') as handle:
        for line in handle:
            if line.strip():
                payload = json.loads(line)
                documents.append(make_document(str(payload['_id']), payload.get('title', ''), payload.get('text', '')))
    queries: list[Query] = []
    with queries_path.open(encoding='utf-8') as handle:
        for line in handle:
            if not line.strip():
                continue
            payload = json.loads(line)
            query_id = str(payload['_id'])
            if query_id in qrels:
                text = payload.get('text', '')
                queries.append(Query(query_id, text, tokenize(text)))
    if not queries:
        raise ValueError('no queries had judgments for this split')
    return Dataset(root.name, False, tuple(documents), tuple(sorted(queries, key=lambda item: item.query_id)), dict(qrels))

def make_smoke_dataset(*, seed: int = 5, documents: int = 240, queries: int = 60) -> Dataset:
    rng = random.Random(seed)
    common = [f'common{index:02d}' for index in range(10)]
    rare = [f'rare{index:03d}' for index in range(240)]
    corpus: list[Document] = []
    clusters: list[list[str]] = []
    for cluster_index in range(documents // 4):
        shared_common = rng.sample(common, 4)
        shared_rare = rng.sample(rare, 7)
        members: list[str] = []
        for member in range(4):
            unique = rng.sample(rare, 2)
            doc_id = f'd{cluster_index:04d}_{member}'
            body = ' '.join(shared_common + shared_rare + unique + rng.sample(rare, 6))
            corpus.append(make_document(doc_id, f'title {shared_common[0]}', body))
            members.append(doc_id)
        clusters.append(members)
    by_id = {document.doc_id: document for document in corpus}
    query_list: list[Query] = []
    qrels: dict[str, dict[str, int]] = {}
    for index in range(queries):
        members = clusters[rng.randrange(len(clusters))]
        target = by_id[members[rng.randrange(len(members))]]
        siblings = {token for member in members if member != target.doc_id for token in by_id[member].token_set}
        generic = [token for token in target.tokens if token.startswith('common')][:2]
        distinguishing = [token for token in target.tokens if token.startswith('rare') and token not in siblings][:2]
        shared_rare = [token for token in target.tokens if token.startswith('rare') and token in siblings][:1]
        text = ' '.join(generic + shared_rare + distinguishing)
        query_id = f'q{index:04d}'
        query_list.append(Query(query_id, text, tokenize(text)))
        qrels[query_id] = {target.doc_id: 1}
    return Dataset('smoke', True, tuple(corpus), tuple(query_list), qrels)

def split_of(query_id: str, *, development_fraction: float = 0.30) -> str:
    digest = hashlib.sha256(query_id.encode('utf-8')).digest()
    bucket = int.from_bytes(digest[:4], 'big') / 0xFFFFFFFF
    return 'development' if bucket < development_fraction else 'final'

def queries_for_split(dataset: Dataset, split: str, *, limit: int | None = None) -> tuple[Query, ...]:
    if split == 'all':
        selected = list(dataset.queries)
    elif split in {'development', 'final'}:
        selected = [query for query in dataset.queries if split_of(query.query_id) == split]
    else:
        raise ValueError(f'unknown split: {split}')
    if limit is not None:
        selected = selected[:limit]
    return tuple(selected)

class BM25Index:
    def __init__(self, documents: Sequence[Document], *, k1: float = BM25_K1, b: float = BM25_B) -> None:
        if not documents:
            raise ValueError('at least one document is required')
        self.documents = tuple(documents)
        self.k1 = k1
        self.b = b
        self.lengths = {document.doc_id: len(document.tokens) for document in documents}
        self.average_length = mean(self.lengths.values()) or 1.0
        postings: dict[str, list[tuple[str, int]]] = defaultdict(list)
        for document in documents:
            counts: dict[str, int] = defaultdict(int)
            for token in document.tokens:
                counts[token] += 1
            for token, count in counts.items():
                postings[token].append((document.doc_id, count))
        self.postings = {token: tuple(items) for token, items in postings.items()}
        total = len(documents)
        self.idf = {token: math.log(1.0 + (total - len(items) + 0.5) / (len(items) + 0.5)) for token, items in self.postings.items()}
    def score(self, tokens: Sequence[str]) -> dict[str, float]:
        scores: dict[str, float] = defaultdict(float)
        for token in tokens:
            items = self.postings.get(token)
            if not items:
                continue
            idf = self.idf[token]
            for doc_id, frequency in items:
                length = self.lengths[doc_id]
                denominator = frequency + self.k1 * (1.0 - self.b + self.b * length / self.average_length)
                scores[doc_id] += idf * frequency * (self.k1 + 1.0) / denominator
        return dict(scores)
    def top_candidates(self, tokens: Sequence[str], depth: int) -> tuple[tuple[str, float], ...]:
        return tuple(sorted(self.score(tokens).items(), key=lambda item: (-item[1], item[0]))[:depth])

@dataclass
class FeatureMeter:
    index: 'ChannelBank'
    evaluations: int = 0
    requests: int = 0
    nanoseconds: int = 0
    per_channel: list[int] = field(default_factory=lambda: [0] * CHANNEL_COUNT)
    _cache: dict[tuple[str, int, tuple[str, ...]], float] = field(default_factory=dict)
    def value(self, query: Query, doc_id: str, channel: int, *, cue: tuple[str, ...] | None = None) -> float:
        tokens = query.tokens if cue is None else cue
        key = (doc_id, channel, tuple(tokens))
        self.requests += 1
        cached = self._cache.get(key)
        if cached is not None:
            return cached
        started = time.perf_counter_ns()
        computed = self.index.compute(tokens, doc_id, channel)
        self.nanoseconds += time.perf_counter_ns() - started
        self.evaluations += 1
        self.per_channel[channel] += 1
        self._cache[key] = computed
        return computed

class ChannelBank:
    def __init__(self, index: BM25Index, documents: dict[str, Document]) -> None:
        self.index = index
        self.documents = documents
        self._max_bm25 = 1.0
    def calibrate(self, sample: Iterable[Query]) -> None:
        peaks = []
        for query in sample:
            scores = self.index.score(query.tokens)
            if scores:
                peaks.append(max(scores.values()))
        self._max_bm25 = max(peaks) if peaks else 1.0
    def compute(self, tokens: tuple[str, ...], doc_id: str, channel: int) -> float:
        document = self.documents[doc_id]
        if channel == 0:
            length = self.index.lengths[doc_id]
            counts: dict[str, int] = defaultdict(int)
            for token in document.tokens:
                counts[token] += 1
            total = 0.0
            for token in tokens:
                frequency = counts.get(token, 0)
                if frequency:
                    idf = self.index.idf.get(token, 0.0)
                    denominator = frequency + BM25_K1 * (1.0 - BM25_B + BM25_B * length / self.index.average_length)
                    total += idf * frequency * (BM25_K1 + 1.0) / denominator
            return min(1.0, total / self._max_bm25) if self._max_bm25 > 0 else 0.0
        if channel == 1:
            rare = [token for token in tokens if self.index.idf.get(token, 0.0) >= 3.0]
            return sum(1 for token in rare if token in document.token_set) / len(rare) if rare else 0.0
        if channel == 2:
            present = [token for token in dict.fromkeys(tokens) if token in document.positions]
            if len(present) < 2:
                return 0.0
            best = math.inf
            for left_index in range(len(present) - 1):
                for right_index in range(left_index + 1, len(present)):
                    for position in document.positions[present[left_index]]:
                        for other in document.positions[present[right_index]]:
                            best = min(best, abs(position - other))
            return 0.0 if best is math.inf else 1.0 / (1.0 + math.log1p(best))
        if channel == 3:
            query_grams = _char_grams(' '.join(tokens))
            if not query_grams or not document.char_grams:
                return 0.0
            return len(query_grams & document.char_grams) / math.sqrt(len(query_grams) * len(document.char_grams))
        raise ValueError(f'unknown channel: {channel}')

@dataclass(frozen=True, slots=True)
class LearnedParameters:
    channel_gains: tuple[float, ...]
    channel_unit_cost_ns: tuple[float, ...]
    channel_order: tuple[int, ...]
    commit_margin: float
    def to_dict(self) -> dict[str, object]:
        return asdict(self)

def learn_parameters(dataset: Dataset, bank: ChannelBank, index: BM25Index, *, development: Sequence[Query]) -> LearnedParameters:
    if not development:
        raise ValueError('development split is empty')
    relevant_totals = [0.0] * CHANNEL_COUNT
    relevant_counts = [0] * CHANNEL_COUNT
    field_totals = [0.0] * CHANNEL_COUNT
    field_counts = [0] * CHANNEL_COUNT
    cost_totals = [0] * CHANNEL_COUNT
    cost_counts = [0] * CHANNEL_COUNT
    for query in development:
        candidates = index.top_candidates(query.tokens, CANDIDATE_DEPTH)
        judged = dataset.qrels.get(query.query_id, {})
        for doc_id, _ in candidates:
            for channel in range(CHANNEL_COUNT):
                started = time.perf_counter_ns()
                value = bank.compute(query.tokens, doc_id, channel)
                cost_totals[channel] += time.perf_counter_ns() - started
                cost_counts[channel] += 1
                field_totals[channel] += value
                field_counts[channel] += 1
                if judged.get(doc_id, 0) > 0:
                    relevant_totals[channel] += value
                    relevant_counts[channel] += 1
    utility = []
    for channel in range(CHANNEL_COUNT):
        field_mean = field_totals[channel] / max(1, field_counts[channel])
        relevant_mean = relevant_totals[channel] / relevant_counts[channel] if relevant_counts[channel] else field_mean
        utility.append(max(0.0, relevant_mean - field_mean))
    unit_cost = tuple(cost_totals[channel] / max(1, cost_counts[channel]) for channel in range(CHANNEL_COUNT))
    average_utility = mean(utility)
    if average_utility <= 0.0:
        raise ValueError('development split produced no positive channel utility')
    gains = tuple(value / average_utility for value in utility)
    efficiency = [utility[channel] / max(1.0, unit_cost[channel]) for channel in range(CHANNEL_COUNT)]
    order = tuple(sorted(range(CHANNEL_COUNT), key=lambda c: (-efficiency[c], c)))
    margin = _select_commit_margin(dataset, bank, index, development, gains, order)
    return LearnedParameters(gains, unit_cost, order, margin)

def _select_commit_margin(dataset: Dataset, bank: ChannelBank, index: BM25Index, development: Sequence[Query], gains: tuple[float, ...], order: tuple[int, ...]) -> float:
    provisional = LearnedParameters(gains, (1.0,) * CHANNEL_COUNT, order, 0.0)
    records: list[tuple[float, bool]] = []
    for query in development:
        candidates = index.top_candidates(query.tokens, CANDIDATE_DEPTH)
        if not candidates:
            continue
        taper = soft_taper(query, candidates, provisional, FeatureMeter(bank), order=order)
        ranked = _ranked(taper.activation)
        if len(ranked) < 2:
            continue
        records.append((ranked[0][1] - ranked[1][1], dataset.qrels.get(query.query_id, {}).get(ranked[0][0], 0) > 0))
    if not records:
        return 0.0
    best_margin, best_score = 0.0, -1.0
    for threshold in [value / 200.0 for value in range(41)]:
        committed = [correct for margin, correct in records if margin >= threshold]
        if not committed:
            continue
        precision = mean(1.0 if correct else 0.0 for correct in committed)
        coverage = len(committed) / len(records)
        score = 2 * precision * coverage / (precision + coverage) if precision + coverage else 0.0
        if score > best_score:
            best_margin, best_score = threshold, score
    return best_margin

@dataclass(frozen=True, slots=True)
class TaperResult:
    activation: dict[str, float]
    active: tuple[str, ...]
    dormant: tuple[str, ...]
    stage_active_counts: tuple[int, ...]

def _ranked(activation: dict[str, float]) -> list[tuple[str, float]]:
    return sorted(activation.items(), key=lambda item: (-item[1], item[0]))

def _normalize(values: dict[str, float]) -> dict[str, float]:
    total = sum(values.values())
    if total <= 0.0:
        uniform = 1.0 / max(1, len(values))
        return {key: uniform for key in values}
    return {key: value / total for key, value in values.items()}

def _initial_activation(candidates: Sequence[tuple[str, float]]) -> dict[str, float]:
    if not candidates:
        return {}
    peak = max(score for _, score in candidates)
    return _normalize({doc_id: math.exp((score - peak) / max(1e-9, 0.24 * abs(peak) or 1.0)) for doc_id, score in candidates})

def soft_taper(query: Query, candidates: Sequence[tuple[str, float]], parameters: LearnedParameters, meter: FeatureMeter, *, order: Sequence[int] | None = None, prior: dict[str, float] | None = None, cue: tuple[str, ...] | None = None, minimum_active: int = RECURRENCE_WIDTH) -> TaperResult:
    stage_order = tuple(parameters.channel_order if order is None else order)
    activation = dict(prior) if prior else _initial_activation(candidates)
    for doc_id, _ in candidates:
        activation.setdefault(doc_id, 0.0)
    active = {doc_id for doc_id, _ in candidates}
    counts = []
    for channel in stage_order:
        gain = parameters.channel_gains[channel]
        for _ in range(TAPER_STAGE_CYCLES):
            updated = dict(activation)
            for doc_id in active:
                value = meter.value(query, doc_id, channel, cue=cue)
                updated[doc_id] = max(activation[doc_id], DORMANT_FLOOR) ** 0.90 * math.exp(gain * value / TAPER_TEMPERATURE)
            activation = _normalize(updated)
        peak = max(activation.values()) if activation else 0.0
        eligible = {doc_id for doc_id, value in activation.items() if value >= peak * TAPER_RELATIVE_GATE}
        if len(eligible) < minimum_active:
            eligible = {doc_id for doc_id, _ in _ranked(activation)[:minimum_active]}
        active = eligible
        counts.append(len(active))
    return TaperResult(activation, tuple(sorted(active)), tuple(sorted(set(activation) - active)), tuple(counts))

def hard_taper(query: Query, candidates: Sequence[tuple[str, float]], parameters: LearnedParameters, meter: FeatureMeter, *, cue: tuple[str, ...] | None = None, prior: dict[str, float] | None = None, keep: int = RECURRENCE_WIDTH) -> TaperResult:
    activation = dict(prior) if prior else _initial_activation(candidates)
    total_gain = sum(parameters.channel_gains) or 1.0
    scores = {}
    for doc_id, _ in candidates:
        combined = sum(parameters.channel_gains[channel] * meter.value(query, doc_id, channel, cue=cue) for channel in range(CHANNEL_COUNT))
        scores[doc_id] = math.log(activation[doc_id] + 1e-12) + 2.4 * combined / total_gain
    kept = [doc_id for doc_id, _ in sorted(scores.items(), key=lambda item: (-item[1], item[0]))[:keep]]
    peak = max(scores[doc_id] for doc_id in kept)
    retained = _normalize({doc_id: math.exp((scores[doc_id] - peak) / TAPER_TEMPERATURE) for doc_id in kept})
    return TaperResult(retained, tuple(sorted(kept)), (), (len(kept),))

def build_relations(documents: dict[str, Document], survivors: Sequence[str], index: BM25Index) -> dict[tuple[str, str], float]:
    profiles = {doc_id: {token for token in documents[doc_id].token_set if index.idf.get(token, 0.0) >= 3.0} for doc_id in survivors}
    relations = {}
    for left in survivors:
        for right in survivors:
            if left >= right:
                continue
            first, second = profiles[left], profiles[right]
            if not first or not second:
                continue
            overlap = len(first & second) / math.sqrt(len(first) * len(second))
            if overlap > 0.0:
                relations[left, right] = overlap
                relations[right, left] = overlap
    return relations

def recurrent_solve(activation: dict[str, float], survivors: Sequence[str], relations: dict[tuple[str, str], float], *, cycles: int = RECURRENCE_CYCLES, persistence: float = 0.30, excitation_gain: float = 0.55, inhibition_gain: float = 0.45, evidence_gain: float = 0.40) -> dict[str, float]:
    peak = max((activation[doc_id] for doc_id in survivors), default=0.0) or 1.0
    state = {doc_id: activation[doc_id] / peak for doc_id in survivors}
    evidence = dict(state)
    mean_affinity = mean(relations.values()) if relations else 0.0
    for _ in range(cycles):
        updated = {}
        for doc_id in survivors:
            excite = inhibit = 0.0
            for other in survivors:
                if other == doc_id:
                    continue
                affinity = relations.get((other, doc_id), 0.0)
                if affinity >= mean_affinity:
                    excite += affinity * state[other]
                else:
                    inhibit += (mean_affinity - affinity) * state[other]
            updated[doc_id] = max(0.0, persistence * state[doc_id] + excitation_gain * excite - inhibition_gain * inhibit + evidence_gain * evidence[doc_id])
        top = max(updated.values()) or 1.0
        state = {doc_id: value / top for doc_id, value in updated.items()}
    return state

def ndcg_at_k(ranking: Sequence[str], judged: dict[str, int], k: int = 10) -> float:
    gains = [judged.get(doc_id, 0) for doc_id in ranking[:k]]
    dcg = sum(gain / math.log2(position + 2) for position, gain in enumerate(gains))
    ideal = sorted(judged.values(), reverse=True)[:k]
    idcg = sum(gain / math.log2(position + 2) for position, gain in enumerate(ideal))
    return dcg / idcg if idcg > 0 else 0.0

def recall_at_k(ranking: Sequence[str], judged: dict[str, int], k: int = 100) -> float:
    return sum(1 for doc_id in ranking[:k] if judged.get(doc_id, 0) > 0) / len(judged) if judged else 0.0

@dataclass(frozen=True, slots=True)
class QueryOutcome:
    query_id: str
    ndcg10: float
    recall100: float
    committed: bool
    top_correct: bool
    field_contains_relevant: bool
    evaluations: int
    nanoseconds: int
    reopen_probed: bool
    reopen_initially_missing: bool
    reopen_recovered: bool

def _reopen_cue(query: Query) -> tuple[str, ...] | None:
    return query.tokens[:len(query.tokens) // 2] if len(query.tokens) >= 4 else None

def _cue_prior(query: Query, field_ids: Sequence[str], meter: FeatureMeter, cue: tuple[str, ...]) -> dict[str, float]:
    scores = {doc_id: meter.value(query, doc_id, 0, cue=cue) for doc_id in field_ids}
    peak = max(scores.values(), default=0.0)
    return _normalize({doc_id: math.exp((value - peak) / TAPER_TEMPERATURE) for doc_id, value in scores.items()})

def run_condition(dataset: Dataset, index: BM25Index, bank: ChannelBank, parameters: LearnedParameters, query: Query, condition: str) -> QueryOutcome:
    judged = dataset.qrels.get(query.query_id, {})
    meter = FeatureMeter(bank)
    candidates = index.top_candidates(query.tokens, CANDIDATE_DEPTH)
    field_ids = [doc_id for doc_id, _ in candidates]
    field_has_relevant = any(judged.get(doc_id, 0) > 0 for doc_id in field_ids)
    if not candidates:
        return QueryOutcome(query.query_id, 0.0, 0.0, False, False, False, 0, 0, False, False, False)
    reopen_cue = _reopen_cue(query)
    probes_reopen = reopen_cue is not None and condition in {'hard_cascade', 'fixed_order_taper', 'learned_order_taper', 'learned_order_no_recurrence', 'learned_order_no_reopen'}
    initially_missing = recovered = False
    if condition == 'bm25_only':
        ranking = field_ids
        margin_source = _initial_activation(candidates)
    elif condition == 'full_rerank':
        total_gain = sum(parameters.channel_gains) or 1.0
        def rerank(start: dict[str, float], cue: tuple[str, ...] | None) -> dict[str, float]:
            activation = dict(start)
            for _ in range(GENERIC_CYCLES):
                previous = dict(activation)
                updated = {}
                for doc_id in field_ids:
                    combined = sum(parameters.channel_gains[channel] * meter.value(query, doc_id, channel, cue=cue) for channel in range(CHANNEL_COUNT))
                    updated[doc_id] = max(previous[doc_id], DORMANT_FLOOR) ** 0.90 * math.exp(combined / total_gain / TAPER_TEMPERATURE)
                activation = _normalize(updated)
                if sum(abs(activation[doc_id] - previous[doc_id]) for doc_id in field_ids) < 0.004:
                    break
            return activation
        if reopen_cue is not None:
            activation = rerank(rerank(_cue_prior(query, field_ids, meter, reopen_cue), reopen_cue), None)
        else:
            activation = rerank(_initial_activation(candidates), None)
        margin_source = activation
        ranking = [doc_id for doc_id, _ in _ranked(activation)]
    elif condition == 'hard_cascade':
        cue = reopen_cue if probes_reopen else None
        prior = _cue_prior(query, field_ids, meter, cue) if cue else None
        taper = hard_taper(query, candidates, parameters, meter, cue=cue, prior=prior)
        survivors = list(taper.active)
        activation = dict(taper.activation)
        if probes_reopen:
            initially_missing = not any(judged.get(doc_id, 0) > 0 for doc_id in survivors)
            total_gain = sum(parameters.channel_gains) or 1.0
            rescored = {doc_id: sum(parameters.channel_gains[channel] * meter.value(query, doc_id, channel) for channel in range(CHANNEL_COUNT)) / total_gain for doc_id in survivors}
            activation = _normalize({doc_id: math.exp(value / TAPER_TEMPERATURE) for doc_id, value in rescored.items()})
        state = recurrent_solve(activation, survivors, build_relations(dataset.by_id, survivors, index))
        margin_source = state
        ordered = [doc_id for doc_id, _ in _ranked(state)]
        ranking = ordered + [doc_id for doc_id in field_ids if doc_id not in set(ordered)]
        if probes_reopen and initially_missing:
            recovered = any(judged.get(doc_id, 0) > 0 for doc_id in ranking[:10])
    else:
        order = (0, 1, 2, 3) if condition == 'fixed_order_taper' else parameters.channel_order
        if probes_reopen:
            taper = soft_taper(query, candidates, parameters, meter, order=order, prior=_cue_prior(query, field_ids, meter, reopen_cue), cue=reopen_cue)
            provisional = [doc_id for doc_id, _ in _ranked(taper.activation)[:RECURRENCE_WIDTH]]
            initially_missing = not any(judged.get(doc_id, 0) > 0 for doc_id in provisional)
            if condition != 'learned_order_no_reopen':
                taper = soft_taper(query, candidates, parameters, meter, order=order, prior=taper.activation)
        else:
            taper = soft_taper(query, candidates, parameters, meter, order=order)
        survivors = [doc_id for doc_id, _ in _ranked(taper.activation)[:RECURRENCE_WIDTH]]
        state = {doc_id: taper.activation[doc_id] for doc_id in survivors} if condition == 'learned_order_no_recurrence' else recurrent_solve(taper.activation, survivors, build_relations(dataset.by_id, survivors, index))
        margin_source = state
        ordered = [doc_id for doc_id, _ in _ranked(state)]
        ranking = ordered + [doc_id for doc_id, _ in _ranked(taper.activation) if doc_id not in set(ordered)]
        if probes_reopen and initially_missing:
            recovered = any(judged.get(doc_id, 0) > 0 for doc_id in ranking[:10])
    ranked_margin = _ranked(margin_source)
    margin = ranked_margin[0][1] - ranked_margin[1][1] if len(ranked_margin) > 1 else 0.0
    return QueryOutcome(query.query_id, ndcg_at_k(ranking, judged, 10), recall_at_k(ranking, judged, 100), margin >= parameters.commit_margin, bool(ranking) and judged.get(ranking[0], 0) > 0, field_has_relevant, meter.evaluations, meter.nanoseconds, probes_reopen, initially_missing, recovered)

@dataclass(frozen=True, slots=True)
class ConditionSummary:
    queries: int
    ndcg10: float
    recall100: float
    commit_rate: float
    committed_precision: float
    forced_precision: float
    empty_field_abstain_rate: float
    mean_evaluations: float
    mean_microseconds: float
    reopen_cases: int
    reopen_recovery_rate: float | None
    def to_dict(self) -> dict[str, object]:
        return asdict(self)

def summarize(rows: Sequence[QueryOutcome]) -> ConditionSummary:
    committed = [row for row in rows if row.committed]
    empty_field = [row for row in rows if not row.field_contains_relevant]
    missing = [row for row in rows if row.reopen_probed and row.reopen_initially_missing]
    return ConditionSummary(len(rows), mean(row.ndcg10 for row in rows) if rows else 0.0, mean(row.recall100 for row in rows) if rows else 0.0, mean(1.0 if row.committed else 0.0 for row in rows) if rows else 0.0, mean(1.0 if row.top_correct else 0.0 for row in committed) if committed else 0.0, mean(1.0 if row.top_correct else 0.0 for row in rows) if rows else 0.0, mean(0.0 if row.committed else 1.0 for row in empty_field) if empty_field else 0.0, mean(row.evaluations for row in rows) if rows else 0.0, mean(row.nanoseconds / 1000.0 for row in rows) if rows else 0.0, len(missing), mean(1.0 if row.reopen_recovered else 0.0 for row in missing) if missing else None)

def paired_bootstrap(left: Sequence[float], right: Sequence[float], *, resamples: int = BOOTSTRAP_RESAMPLES, seed: int = BOOTSTRAP_SEED) -> dict[str, float]:
    if len(left) != len(right):
        raise ValueError('paired bootstrap requires equal-length samples')
    if not left:
        return {'delta': 0.0, 'ci_low': 0.0, 'ci_high': 0.0, 'p_greater': 0.0}
    differences = [a - b for a, b in zip(left, right)]
    rng = random.Random(seed)
    draws = [mean(differences[rng.randrange(len(differences))] for _ in differences) for _ in range(resamples)]
    draws.sort()
    return {'delta': mean(differences), 'ci_low': draws[int(0.025 * resamples)], 'ci_high': draws[min(resamples - 1, int(0.975 * resamples))], 'p_greater': mean(1.0 if value > 0.0 else 0.0 for value in draws)}

def evaluate(dataset: Dataset, index: BM25Index, bank: ChannelBank, parameters: LearnedParameters, queries: Sequence[Query], *, conditions: Sequence[str] = CONDITIONS) -> dict[str, list[QueryOutcome]]:
    results = {condition: [] for condition in conditions}
    for query in queries:
        for condition in conditions:
            results[condition].append(run_condition(dataset, index, bank, parameters, query, condition))
    return results

def _bootstrap_statistic(rows: Sequence[QueryOutcome], statistic: Callable[[Sequence[QueryOutcome]], float], *, resamples: int = BOOTSTRAP_RESAMPLES, seed: int = BOOTSTRAP_SEED) -> dict[str, float]:
    if not rows:
        return {'delta': 0.0, 'ci_low': 0.0, 'ci_high': 0.0}
    rng = random.Random(seed)
    draws = [statistic([rows[rng.randrange(len(rows))] for _ in rows]) for _ in range(resamples)]
    draws.sort()
    return {'delta': statistic(rows), 'ci_low': draws[int(0.025 * resamples)], 'ci_high': draws[min(resamples - 1, int(0.975 * resamples))]}

def _abstention_gain(rows: Sequence[QueryOutcome]) -> float:
    if not rows:
        return 0.0
    committed = [row for row in rows if row.committed]
    committed_precision = mean(1.0 if row.top_correct else 0.0 for row in committed) if committed else 0.0
    return committed_precision - mean(1.0 if row.top_correct else 0.0 for row in rows)

def verdict(dataset: Dataset, results: dict[str, list[QueryOutcome]], summaries: dict[str, ConditionSummary]) -> tuple[str, dict[str, object]]:
    learned, bm25, full, fixed = summaries['learned_order_taper'], summaries['bm25_only'], summaries['full_rerank'], summaries['fixed_order_taper']
    published = PUBLISHED_BM25_NDCG10.get(dataset.name.lower())
    bm25_ratio = bm25.ndcg10 / published if published else None
    versus_bm25 = paired_bootstrap([row.ndcg10 for row in results['learned_order_taper']], [row.ndcg10 for row in results['bm25_only']])
    versus_full = paired_bootstrap([row.ndcg10 for row in results['learned_order_taper']], [row.ndcg10 for row in results['full_rerank']])
    cost_versus_full = paired_bootstrap([float(row.evaluations) for row in results['learned_order_taper']], [float(row.evaluations) for row in results['full_rerank']])
    cost_versus_fixed = paired_bootstrap([float(row.evaluations) for row in results['fixed_order_taper']], [float(row.evaluations) for row in results['learned_order_taper']])
    time_versus_full = paired_bootstrap([float(row.nanoseconds) for row in results['learned_order_taper']], [float(row.nanoseconds) for row in results['full_rerank']])
    cost_fraction = learned.mean_evaluations / full.mean_evaluations if full.mean_evaluations else 1.0
    order_advantage = (fixed.mean_evaluations - learned.mean_evaluations) / fixed.mean_evaluations if fixed.mean_evaluations else 0.0
    learned_by_id = {row.query_id: row for row in results['learned_order_taper']}
    hard_by_id = {row.query_id: row for row in results['hard_cascade']}
    common_reopen_ids = sorted(query_id for query_id in learned_by_id.keys() & hard_by_id.keys() if learned_by_id[query_id].reopen_probed and hard_by_id[query_id].reopen_probed and learned_by_id[query_id].reopen_initially_missing and hard_by_id[query_id].reopen_initially_missing)
    reopen_delta = paired_bootstrap([1.0 if learned_by_id[q].reopen_recovered else 0.0 for q in common_reopen_ids], [1.0 if hard_by_id[q].reopen_recovered else 0.0 for q in common_reopen_ids])
    recovery_advantage = reopen_delta['delta'] if common_reopen_ids else None
    abstention_bootstrap = _bootstrap_statistic(results['learned_order_taper'], _abstention_gain, seed=BOOTSTRAP_SEED + 1)
    abstention_gain = abstention_bootstrap['delta']
    checks: dict[str, object] = {
        'local_bm25_ndcg10': bm25.ndcg10,
        'published_bm25_ndcg10': published,
        'local_bm25_vs_published_ratio': bm25_ratio,
        'local_bm25_vs_published_pass': bm25_ratio is not None and bm25_ratio >= GATE['local_bm25_vs_published_min_ratio'],
        'learned_vs_bm25_ndcg': versus_bm25,
        'learned_vs_bm25_pass': versus_bm25['delta'] >= GATE['learned_ndcg_vs_bm25_min_delta'] and versus_bm25['ci_low'] > 0.0,
        'learned_vs_full_rerank_ndcg': versus_full,
        'learned_vs_full_rerank_pass': versus_full['ci_low'] >= GATE['learned_ndcg_vs_full_rerank_min_delta'],
        'cost_fraction_vs_full_rerank': cost_fraction,
        'cost_vs_full_bootstrap': cost_versus_full,
        'time_vs_full_bootstrap': time_versus_full,
        'cost_fraction_vs_full_rerank_pass': cost_fraction <= GATE['learned_cost_fraction_vs_full_rerank_max'] and cost_versus_full['ci_high'] < 0.0,
        'learned_vs_fixed_order_cost_advantage': order_advantage,
        'learned_vs_fixed_order_cost_bootstrap': cost_versus_fixed,
        'learned_vs_fixed_order_pass': order_advantage >= GATE['learned_vs_fixed_order_cost_advantage_min'] and cost_versus_fixed['ci_low'] > 0.0,
        'reopen_cases': len(common_reopen_ids),
        'reopen_case_query_ids': common_reopen_ids,
        'reopen_exercised_pass': len(common_reopen_ids) >= GATE['reopen_probe_cases_min'],
        'reopen_recovery_bootstrap': reopen_delta,
        'reopen_recovery_advantage': recovery_advantage,
        'reopen_recovery_pass': len(common_reopen_ids) >= GATE['reopen_probe_cases_min'] and recovery_advantage is not None and recovery_advantage >= GATE['reopen_recovery_advantage_vs_hard_min'] and reopen_delta['ci_low'] > 0.0,
        'committed_precision': learned.committed_precision,
        'forced_precision': learned.forced_precision,
        'abstention_precision_gain': abstention_gain,
        'abstention_precision_gain_bootstrap': abstention_bootstrap,
        'abstention_precision_gain_pass': abstention_gain >= GATE['abstention_precision_gain_min'] and abstention_bootstrap['ci_low'] > 0.0,
        'empty_field_abstain_rate': learned.empty_field_abstain_rate,
        'empty_field_abstain_pass': learned.empty_field_abstain_rate >= GATE['empty_field_abstain_rate_min'],
    }
    c1_keys = ('local_bm25_vs_published_pass', 'learned_vs_bm25_pass', 'learned_vs_full_rerank_pass', 'cost_fraction_vs_full_rerank_pass', 'learned_vs_fixed_order_pass')
    c3_keys = ('abstention_precision_gain_pass', 'empty_field_abstain_pass')
    c1 = 'REINFORCED' if all(checks[key] is True for key in c1_keys) else 'DISCOUNTED'
    c2 = 'INCONCLUSIVE' if checks['reopen_exercised_pass'] is not True else ('REINFORCED' if checks['reopen_recovery_pass'] is True else 'DISCOUNTED')
    c3 = 'REINFORCED' if all(checks[key] is True for key in c3_keys) else 'DISCOUNTED'
    checks['claim_status'] = {'C1': c1, 'C2': c2, 'C3': c3}
    if dataset.synthetic:
        return ('NOT EVIDENCE: synthetic smoke corpus; external evidence is required.', checks)
    if 'DISCOUNTED' in (c1, c2, c3):
        return (f'DISCOUNTED: C1={c1}, C2={c2}, C3={c3}.', checks)
    if 'INCONCLUSIVE' in (c1, c2, c3):
        return (f'INCONCLUSIVE: C1={c1}, C2={c2}, C3={c3}.', checks)
    return ('REINFORCED: all three independently frozen EXT-1 claims passed on the external benchmark.', checks)

def build_environment(dataset: Dataset) -> tuple[BM25Index, ChannelBank]:
    index = BM25Index(dataset.documents)
    bank = ChannelBank(index, dataset.by_id)
    calibration = queries_for_split(dataset, 'development')
    if not calibration:
        raise ValueError('development split is empty')
    bank.calibrate(calibration[:min(50, len(calibration))])
    return index, bank

def run_assay(*, dataset: Dataset | None = None, data_path: str | Path | None = None, split: str = 'final', limit: int | None = None) -> dict[str, object]:
    if dataset is None:
        if data_path is None:
            raise ValueError('provide either dataset or data_path')
        dataset = load_beir_dataset(data_path)
    if split == 'final' and limit is not None:
        raise ValueError('limit is development-only; partial final runs are forbidden')
    index, bank = build_environment(dataset)
    development = queries_for_split(dataset, 'development')
    parameters = learn_parameters(dataset, bank, index, development=development)
    evaluation_queries = queries_for_split(dataset, split, limit=limit)
    if not evaluation_queries:
        raise ValueError(f'split {split} is empty')
    results = evaluate(dataset, index, bank, parameters, evaluation_queries)
    summaries = {condition: summarize(rows) for condition, rows in results.items()}
    decision, checks = verdict(dataset, results, summaries)
    return {'experiment': EXPERIMENT_ID, 'hypothesis': HYPOTHESIS_ID, 'dataset': dataset.name, 'synthetic': dataset.synthetic, 'split': split, 'question': 'Does reversible ordered tapering with recurrent deliberation earn its cost on a public benchmark against published baselines?', 'corpus_size': len(dataset.documents), 'development_queries': len(development), 'evaluation_queries': len(evaluation_queries), 'candidate_depth': CANDIDATE_DEPTH, 'channels': list(CHANNEL_NAMES), 'learned_parameters': parameters.to_dict(), 'learned_channel_names': [CHANNEL_NAMES[c] for c in parameters.channel_order], 'frozen_gate': dict(GATE), 'conditions': {name: summary.to_dict() for name, summary in summaries.items()}, 'checks': checks, 'verdict': decision, 'cost_note': 'Feature evaluations are cache misses under a per-condition cache; nanoseconds are measured around those misses.', 'scientific_boundary': 'EXT-1 is one external retrieval benchmark with four hand-designed feature channels; it does not establish biological equivalence, learned representations, general reasoning, dense-retrieval superiority, or production readiness.'}

def main() -> None:
    parser = argparse.ArgumentParser(description='EXT-1 external retrieval cascade assay')
    parser.add_argument('--data')
    parser.add_argument('--smoke', action='store_true')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--development', action='store_true')
    group.add_argument('--limit', type=int)
    args = parser.parse_args()
    if args.limit is not None and not args.development:
        parser.error('--limit is development-only; partial final runs are forbidden')
    if args.smoke:
        report = run_assay(dataset=make_smoke_dataset(), split='development' if args.development else 'final', limit=args.limit)
    elif args.data:
        report = run_assay(data_path=args.data, split='development' if args.development else 'final', limit=args.limit)
    else:
        parser.error('provide --data <path> or --smoke')
        return
    print(json.dumps(report, indent=2, default=str))

if __name__ == '__main__':
    main()
