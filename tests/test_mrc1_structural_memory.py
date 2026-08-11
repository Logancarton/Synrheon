from __future__ import annotations

import pytest

from experiments.mrc1_structural_memory import (
    MemoryRecord,
    StructuralMemoryIndex,
    _generate_growth_records,
    _probe_cues,
    _rank_of,
    _record_digest,
    run_benchmark,
)

pytestmark = pytest.mark.scientific


def _tiny_index() -> StructuralMemoryIndex:
    index = StructuralMemoryIndex()
    rows = (
        MemoryRecord("m-z", ("a", "b", "c", "d", "e", "f"), "p-z", 0),
        MemoryRecord("m-a", ("a", "b", "c", "x", "y", "z"), "p-a", 1),
        MemoryRecord("m-q", ("a", "b", "u", "v", "w", "x"), "p-q", 2),
        MemoryRecord("m-r", ("a", "t", "u", "v", "w", "x"), "p-r", 3),
    )
    for row in rows:
        index.insert(row)
    return index


def test_insert_preserves_existing_record_serialization() -> None:
    index = StructuralMemoryIndex()
    old = (
        MemoryRecord("m1", ("a", "b", "c", "d", "e", "f"), "source-1", 0),
        MemoryRecord("m2", ("g", "h", "i", "j", "k", "l"), "source-2", 1),
    )
    for record in old:
        index.insert(record)
    before = _record_digest(index.records.values())

    index.insert(
        MemoryRecord("m3", ("a", "g", "m", "n", "o", "p"), "source-3", 2)
    )
    after_old = _record_digest(index.records[memory_id] for memory_id in ("m1", "m2"))

    assert before == after_old


def test_delete_removes_record_and_posting_memberships_only() -> None:
    index = _tiny_index()
    unrelated_before = index.records["m-z"]
    removed = index.delete("m-q")

    assert removed.memory_id == "m-q"
    assert "m-q" not in index.records
    assert all("m-q" not in posting for posting in index.postings.values())
    assert index.records["m-z"] == unrelated_before
    assert index.provenance("m-z") == "p-z"


def test_selectivity_first_and_reverse_return_same_ranking() -> None:
    index = _tiny_index()
    cue = ("a", "b", "c")
    selective = index.retrieve(cue, order="selectivity_first")
    reverse = index.retrieve(cue, order="reverse_selectivity")

    assert selective.ranked_ids == reverse.ranked_ids == ("m-a", "m-z")
    selective_work = (
        selective.posting_entries_read
        + selective.candidate_score_updates
        + selective.intersection_membership_checks
    )
    reverse_work = (
        reverse.posting_entries_read
        + reverse.candidate_score_updates
        + reverse.intersection_membership_checks
    )
    assert selective_work <= reverse_work


def test_posting_route_target_rank_matches_full_scan_for_exact_partial_cue() -> None:
    index = _tiny_index()
    cue = ("a", "b", "c")
    routed = index.retrieve(cue)
    full = index.full_scan(cue)

    assert _rank_of("m-z", routed.ranked_ids) == _rank_of("m-z", full.ranked_ids)
    assert _rank_of("m-a", routed.ranked_ids) == _rank_of("m-a", full.ranked_ids)


def test_growth_generator_keeps_probe_identity_and_cues_fixed() -> None:
    records = _generate_growth_records(seed=81001, regime="selective", checkpoints=(1000, 3000))
    cues = _probe_cues(records)

    assert len(records) == 3000
    assert len(cues) == 100
    first = records[0]
    assert cues[first.memory_id] == first.concepts[:3]


def test_quick_benchmark_reports_both_regimes_without_claiming_ann_superiority() -> None:
    report = run_benchmark(seeds=(81001,))

    assert report["artifact_class"] == "SYNTHETIC_SYSTEMS_BENCHMARK"
    assert set(report["aggregate"]) == {"selective", "crowded"}
    assert report["interpretation_boundary"]["no_ann_superiority_claim"] is True
    assert report["interpretation_boundary"]["no_rag_superiority_claim"] is True
    assert report["integrity"]["all_deletion_checks_pass"] is True
    assert report["integrity"]["all_routed_vs_full_scan_rank_spotchecks_pass"] is True
    assert report["integrity"]["all_selectivity_order_controls_pass"] is True
