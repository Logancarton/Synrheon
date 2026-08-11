"""Corrected reporting wrapper for the deterministic R0 exact-match baseline.

This module does not alter the v1 world, scorer, or baseline outputs. It corrects the
classification and explicitly exposes the deterministic zero-support tie behavior that
was previously described too loosely as random retrieval.
"""

from __future__ import annotations

from hashlib import sha256
import argparse
import json

from experiments.r0_exact_match_envelope import run_exact_match_envelope
from experiments.r0_single_route_access import (
    FIELD_SIZE,
    RetrievalCue,
    SingleRouteRetriever,
    make_family_a_world,
)

REPORT_ID = "r0-exact-match-envelope-v2"


def run_corrected_exact_match_report(*, seed: int = 1701) -> dict[str, object]:
    """Return a corrected specification/integrity report without changing v1 mechanics."""

    legacy = run_exact_match_envelope(seed=seed)
    world = make_family_a_world(seed=seed)
    retriever = SingleRouteRetriever(world)

    zero_support = []
    zero_support_valid = True
    for route_index in range(world.route_count):
        returned_fields: list[tuple[str, ...]] = []
        target_hits = 0

        for memory in world.memories:
            cue = RetrievalCue(
                concept_ids=(
                    f"zero-support:{seed}:{route_index}:{memory.memory_id}",
                )
            )
            field = retriever.rank(
                cue,
                route_index=route_index,
                field_size=FIELD_SIZE,
            )
            field_ids = tuple(item.memory_id for item in field)
            returned_fields.append(field_ids)
            if memory.memory_id in field_ids:
                target_hits += 1

        unique_fields = {field_ids for field_ids in returned_fields}
        expected_prefix = tuple(
            sorted(memory.memory_id for memory in world.memories)[:FIELD_SIZE]
        )
        only_field = next(iter(unique_fields)) if len(unique_fields) == 1 else tuple()
        query_invariant = len(unique_fields) == 1
        equals_memory_id_prefix = query_invariant and only_field == expected_prefix
        aggregate_hit = target_hits / len(world.memories)
        expected_aggregate = FIELD_SIZE / len(world.memories)

        valid = (
            query_invariant
            and equals_memory_id_prefix
            and abs(aggregate_hit - expected_aggregate) <= 1e-12
        )
        zero_support_valid = zero_support_valid and valid

        zero_support.append(
            {
                "route_index": route_index,
                "baseline_kind": "ZERO_SUPPORT_DETERMINISTIC_PREFIX",
                "all_candidate_scores_tied": True,
                "tie_break": "memory_id_ascending",
                "query_invariant_field": query_invariant,
                "unique_returned_fields": len(unique_fields),
                "equals_first_sorted_memory_ids": equals_memory_id_prefix,
                "field_size": FIELD_SIZE,
                "memory_count": len(world.memories),
                "aggregate_hit_at_32": aggregate_hit,
                "aggregate_hit_explanation": (
                    "field_size / memory_count because every zero-support query returns "
                    "the same deterministic memory-id prefix"
                ),
                "field_fingerprint": _field_fingerprint(only_field),
            }
        )

    corrected_metrics = []
    for metric in legacy["route_metrics"]:
        item = dict(metric)
        item["near_id_zero_support_prefix_hit_at_32"] = item.pop("near_id_hit_at_32")
        item["alias_zero_support_prefix_hit_at_32"] = item.pop("alias_hit_at_32")
        item["metric_class"] = "DERIVED_SPECIFICATION_CHECK"
        corrected_metrics.append(item)

    legacy_valid = legacy["verdict"] == "EXACT_MATCH_ENVELOPE_VALID"
    integrity_valid = legacy_valid and zero_support_valid

    return {
        "report": REPORT_ID,
        "legacy_artifact": legacy["experiment"],
        "amendment": "docs/R0_EXACT_MATCH_ENVELOPE_AMENDMENT_1.md",
        "artifact_class": "SPECIFICATION",
        "evidence_level": "implementation/specification integrity only",
        "scientific_finding": "NONE",
        "mechanism_changed_from_v1": False,
        "generator_family": legacy["generator_family"],
        "seed": seed,
        "memory_count": legacy["memory_count"],
        "field_sizes": legacy["field_sizes"],
        "route_group_sizes": legacy["route_group_sizes"],
        "unbound_noise_counts": legacy["unbound_noise_counts"],
        "field_sweep": legacy["field_sweep"],
        "route_metrics": corrected_metrics,
        "zero_support_baseline": zero_support,
        "interpretation": {
            "field_sweep": "closed-form consequence of fixed overlap scorer and group sizes",
            "detail_only": "closed-form consequence of unique exact detail construction",
            "unbound_noise": "algebraic invariance; unbound concepts match no candidate",
            "same_group_conflict": "arithmetic consequence: competitor has more exact overlap",
            "near_id_and_alias": (
                "zero exact support; aggregate 0.25 is deterministic prefix coverage, "
                "not random sampling"
            ),
        },
        "verdict": (
            "SPECIFICATION_INTEGRITY_VALID"
            if integrity_valid
            else "SPECIFICATION_INTEGRITY_INVALID"
        ),
    }


def _field_fingerprint(memory_ids: tuple[str, ...]) -> str:
    payload = "\0".join(memory_ids).encode("utf-8")
    return sha256(payload).hexdigest()[:16]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run corrected R0 exact-match specification report"
    )
    parser.add_argument("--seed", type=int, default=1701)
    args = parser.parse_args()
    print(json.dumps(run_corrected_exact_match_report(seed=args.seed), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
