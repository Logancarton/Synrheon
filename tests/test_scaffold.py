"""Stage 0B regression plus Stage 1 substrate/experience-thread tests."""

from __future__ import annotations

import json
from threading import Thread
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

from synrheon.core import CognitiveSubstrate, Concept, WorldRelation
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


def test_open_ended_self_relations_are_data_not_fixed_dimensions() -> None:
    substrate = CognitiveSubstrate()
    substrate.add_concept(Concept("daisy", "Daisy"))
    substrate.add_concept(Concept("dog", "dog"))
    substrate.add_world_relation(
        WorldRelation("daisy", "IS_A", "dog", origin="injected", confidence=1.0)
    )

    injected = substrate.set_injected_self_relation(
        concept_id="daisy",
        relation_type="protective_of",
        strength=0.7,
        confidence=0.9,
    )
    substrate.set_activation("daisy", 1.0)

    snapshot = substrate.snapshot()
    self_relation = snapshot["self_relations"][0]
    assert injected.relation_type == "protective_of"
    assert self_relation["injected"][0]["relation_type"] == "protective_of"
    assert self_relation["injected"][0]["strength"] == 0.7
    assert self_relation["injected"][0]["origin"] == "injected"
    assert self_relation["learned"] == []
    assert snapshot["world_relations"][0]["relation"] == "IS_A"
    assert snapshot["activation"] == {"daisy": 1.0}


def test_self_learning_updates_arbitrary_relation_without_rewriting_injected_or_world_state() -> None:
    substrate = CognitiveSubstrate()
    substrate.add_concept(Concept("daisy", "Daisy"))
    substrate.add_concept(Concept("dog", "dog"))
    substrate.add_world_relation(
        WorldRelation("daisy", "IS_A", "dog", origin="injected", confidence=1.0)
    )
    substrate.set_injected_self_relation(
        concept_id="daisy",
        relation_type="protective_of",
        strength=0.7,
        confidence=0.9,
    )
    before_world = substrate.snapshot()["world_relations"]
    before_injected = substrate.snapshot()["self_relations"][0]["injected"]

    learned = substrate.learn_self_relation(
        concept_id="daisy",
        relation_type="protective_of",
        observed_strength=1.0,
        trust=0.8,
        learning_rate=0.5,
        evidence_event_id="experience-1",
    )

    assert learned.strength == pytest.approx(0.4)
    assert learned.confidence == pytest.approx(0.4)
    assert learned.origin == "learned"
    assert learned.evidence_event_ids == ["experience-1"]

    snapshot = substrate.snapshot()
    assert snapshot["world_relations"] == before_world
    assert snapshot["self_relations"][0]["injected"] == before_injected
    assert snapshot["self_relations"][0]["learned"][0]["relation_type"] == "protective_of"


def test_arbitrary_relation_types_and_invalid_values() -> None:
    substrate = CognitiveSubstrate()
    substrate.add_concept(Concept("daisy", "Daisy"))

    substrate.set_injected_self_relation(
        concept_id="daisy",
        relation_type="expects_help_from",
        strength=0.2,
        confidence=0.8,
    )
    substrate.learn_self_relation(
        concept_id="daisy",
        relation_type="reminds_me_of_home",
        observed_strength=0.9,
        trust=0.5,
        learning_rate=0.5,
        evidence_event_id="experience-2",
    )

    self_relation = substrate.snapshot()["self_relations"][0]
    types = {
        relation["relation_type"]
        for group in (self_relation["injected"], self_relation["learned"])
        for relation in group
    }
    assert types == {"expects_help_from", "reminds_me_of_home"}

    with pytest.raises(ValueError):
        substrate.set_injected_self_relation(
            concept_id="daisy",
            relation_type="   ",
            strength=0.2,
            confidence=0.8,
        )
    with pytest.raises(ValueError):
        substrate.set_injected_self_relation(
            concept_id="daisy",
            relation_type="anything",
            strength=1.2,
            confidence=0.8,
        )


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


def test_http_boundary_accepts_unseen_self_relation_type() -> None:
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
        related = post(
            "/api/self-relation",
            {
                "concept_id": "daisy",
                "relation_type": "protective_of",
                "strength": 0.7,
                "confidence": 0.9,
            },
        )
        chatted = post("/api/stimulus", {"text": "Daisy"})
        thought = post("/api/thought", {"text": "Daisy may expect a walk"})
        stepped = post("/api/step")

        injected = related["state"]["cognitive_substrate"]["self_relations"][0]["injected"][0]
        assert injected["relation_type"] == "protective_of"
        assert injected["origin"] == "injected"
        assert chatted["state"]["experience_thread"]["events"][-1]["origin"] == "observed"
        assert thought["state"]["experience_thread"]["events"][-1]["origin"] == "injected"
        assert stepped["state"]["cycle"] == 1

        with urlopen(f"{base}/", timeout=2) as response:  # noqa: S310
            html = response.read().decode("utf-8")
        assert "Internal Thought" in html
        assert "Knowledge" in html
        assert "Inject Self Relation" in html
        assert "selfRelationType" in html

        bad_request = Request(
            f"{base}/api/self-relation",
            data=json.dumps(
                {"concept_id": "daisy", "relation_type": "", "strength": 0.7}
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
