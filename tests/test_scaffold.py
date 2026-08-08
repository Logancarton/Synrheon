"""Stage 0B regression plus Stage 1 substrate/experience-thread tests."""

from __future__ import annotations

import json
from threading import Thread
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

from synrheon.core import CognitiveSubstrate, Concept, SelfRelationVector
from synrheon.interfaces import create_development_server
from synrheon.runtime import SynrheonRuntime


def test_scaffold_imports() -> None:
    import synrheon
    import synrheon.abstraction
    import synrheon.autonomy
    import synrheon.cognition
    import synrheon.consolidation
    import synrheon.core
    import synrheon.experience
    import synrheon.interfaces
    import synrheon.learning
    import synrheon.memory
    import synrheon.problem_solving
    import synrheon.retrieval
    import synrheon.runtime
    import synrheon.scratchpad
    import synrheon.time

    assert synrheon.__version__ == "0.0.1"


def test_runtime_records_ordered_experience_with_distinct_provenance() -> None:
    runtime = SynrheonRuntime(cycle_interval_seconds=10.0)
    try:
        runtime.start()
        runtime.send_external_stimulus("Daisy came to the door")
        state = runtime.inject_internal_thought("Consider whether Daisy expects a walk")

        events = state["experience_thread"]["events"]
        assert [event["origin"] for event in events] == ["observed", "injected"]
        assert [event["time"]["sequence"] for event in events] == [1, 2]
        assert events[0]["next_event_id"] == events[1]["event_id"]
        assert events[1]["previous_event_id"] == events[0]["event_id"]
        assert state["stimuli"][0]["experience_event_id"] == events[0]["event_id"]
        assert state["stimuli"][1]["experience_event_id"] == events[1]["event_id"]
        assert state["time"]["experience_sequence"] == 2
    finally:
        runtime.close()


def test_runtime_start_step_and_distinct_input_channels() -> None:
    runtime = SynrheonRuntime(cycle_interval_seconds=10.0)
    try:
        started = runtime.start()
        assert started["status"] == "paused"
        assert started["cycle"] == 0
        assert started["session_id"]

        external = runtime.send_external_stimulus("Hello Synrheon")
        internal = runtime.inject_internal_thought("Inspect the unresolved state")
        stepped = runtime.think_one_step()

        assert [item["kind"] for item in internal["stimuli"]] == ["external", "internal"]
        assert external["stimuli"][0]["text"] == "Hello Synrheon"
        assert internal["stimuli"][1]["text"] == "Inspect the unresolved state"
        assert stepped["cycle"] == 1
        assert any(event["event"] == "cycle_advanced" for event in stepped["trace"])
    finally:
        runtime.close()


def test_substrate_keeps_world_self_and_activation_separate() -> None:
    substrate = CognitiveSubstrate()
    substrate.add_concept(Concept("daisy", "Daisy"))
    substrate.add_concept(Concept("dog", "dog"))

    from synrheon.core import WorldRelation

    substrate.add_world_relation(
        WorldRelation("daisy", "IS_A", "dog", origin="injected", confidence=1.0)
    )
    substrate.set_injected_self_relation(
        concept_id="daisy",
        dimension="social",
        value=0.8,
        confidence=0.9,
    )
    substrate.set_activation("daisy", 1.0)

    snapshot = substrate.snapshot()
    assert snapshot["world_relations"][0]["origin"] == "injected"
    assert snapshot["self_relations"][0]["origin"] == "injected"
    assert snapshot["self_relations"][0]["vector"]["social"] == 0.8
    assert snapshot["activation"] == {"daisy": 1.0}
    assert snapshot["concepts"][0]["world_vector"] == []


def test_self_learning_updates_explicit_vector_without_rewriting_world_knowledge() -> None:
    substrate = CognitiveSubstrate()
    substrate.add_concept(Concept("daisy", "Daisy"))
    substrate.add_concept(Concept("dog", "dog"))

    from synrheon.core import WorldRelation

    substrate.add_world_relation(
        WorldRelation("daisy", "IS_A", "dog", origin="injected", confidence=1.0)
    )
    before_world = substrate.snapshot()["world_relations"]

    learned = substrate.learn_self_relation(
        concept_id="daisy",
        observation=SelfRelationVector(experience=1.0, social=0.8, prediction=0.6),
        trust=0.8,
        learning_rate=0.5,
        evidence_event_id="experience-1",
    )

    assert learned.origin == "learned"
    assert learned.vector.experience == pytest.approx(0.4)
    assert learned.vector.social == pytest.approx(0.32)
    assert learned.vector.prediction == pytest.approx(0.24)
    assert learned.confidence == pytest.approx(0.4)
    assert learned.evidence_event_ids == ["experience-1"]
    assert substrate.snapshot()["world_relations"] == before_world


def test_runtime_controls_require_start_and_reject_empty_input() -> None:
    runtime = SynrheonRuntime(cycle_interval_seconds=10.0)
    try:
        with pytest.raises(RuntimeError):
            runtime.think_one_step()

        runtime.start()
        before = runtime.snapshot()
        with pytest.raises(ValueError):
            runtime.send_external_stimulus("   ")
        after = runtime.snapshot()

        assert after == before
    finally:
        runtime.close()


def test_http_boundary_reaches_runtime_thread_and_substrate() -> None:
    runtime = SynrheonRuntime(cycle_interval_seconds=10.0)
    server = create_development_server(runtime, port=0)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address[:2]
    base = f"http://{host}:{port}"

    def post(path: str, payload: dict[str, object] | None = None) -> dict[str, object]:
        body = json.dumps(payload or {}).encode("utf-8")
        request = Request(
            f"{base}{path}",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=2) as response:  # noqa: S310
            return json.loads(response.read().decode("utf-8"))

    try:
        post("/api/start")
        post("/api/concept", {"concept_id": "daisy", "label": "Daisy"})
        post("/api/concept", {"concept_id": "dog", "label": "dog"})
        related = post(
            "/api/world-relation",
            {
                "source_concept_id": "daisy",
                "relation": "IS_A",
                "target_concept_id": "dog",
                "confidence": 1.0,
            },
        )
        self_related = post(
            "/api/self-relation",
            {"concept_id": "daisy", "dimension": "social", "value": 0.9, "confidence": 0.8},
        )
        chatted = post("/api/stimulus", {"text": "Daisy"})
        thought = post("/api/thought", {"text": "Daisy may expect a walk"})
        stepped = post("/api/step")

        assert related["state"]["cognitive_substrate"]["world_relations"][0]["origin"] == "injected"
        assert self_related["state"]["cognitive_substrate"]["self_relations"][0]["vector"]["social"] == 0.9
        assert chatted["state"]["experience_thread"]["events"][-1]["origin"] == "observed"
        assert thought["state"]["experience_thread"]["events"][-1]["origin"] == "injected"
        assert stepped["state"]["cycle"] == 1

        with urlopen(f"{base}/", timeout=2) as response:  # noqa: S310
            html = response.read().decode("utf-8")
        assert "Internal Thought" in html
        assert "Knowledge" in html
        assert "Inject Self Relation" in html

        bad_request = Request(
            f"{base}/api/world-relation",
            data=json.dumps(
                {
                    "source_concept_id": "unknown",
                    "relation": "IS_A",
                    "target_concept_id": "dog",
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with pytest.raises(HTTPError) as exc_info:
            urlopen(bad_request, timeout=2)  # noqa: S310
        assert exc_info.value.code == 400
    finally:
        server.shutdown()
        server.server_close()
        runtime.close()
        thread.join(timeout=2)
