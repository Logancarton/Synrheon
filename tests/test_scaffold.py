"""Stage 0B regression plus current substrate, experience, and Ground 0 contracts."""

from __future__ import annotations

import json
from threading import Thread
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

from synrheon.cognition import Ground0Checkpoint
from synrheon.dev_server import create_development_server
from synrheon.runtime import SynrheonRuntime
from synrheon.state import CognitiveSubstrate, Concept, WorldRelation


def test_scaffold_imports() -> None:
    import synrheon
    import synrheon.cognition
    import synrheon.dev_server
    import synrheon.experience
    import synrheon.policy
    import synrheon.policy_learning
    import synrheon.runtime
    import synrheon.state
    import synrheon.temporal

    assert synrheon.__version__ == "0.0.1"


def test_ground0_checkpoint_is_explicit_and_bounded() -> None:
    checkpoint = Ground0Checkpoint(
        phase="recurrent_deliberation",
        broad_candidate_count=512,
        serious_candidate_count=16,
        recurrent_cycle=2,
        disposition="continue",
    )
    assert checkpoint.to_dict()["serious_candidate_count"] == 16

    with pytest.raises(ValueError):
        Ground0Checkpoint(
            phase="tapering",
            broad_candidate_count=12,
            serious_candidate_count=13,
        )


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
        assert "cognitive_frames" not in state
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


def test_open_ended_organism_relations_remain_data_not_fixed_dimensions() -> None:
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
    assert self_relation["learned"] == []
    assert snapshot["world_relations"][0]["relation"] == "IS_A"
    assert snapshot["activation"] == {"daisy": 1.0}


def test_self_learning_storage_update_preserves_injected_and_world_state() -> None:
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
    assert substrate.snapshot()["world_relations"] == before_world
    assert substrate.snapshot()["self_relations"][0]["injected"] == before_injected


def test_chat_does_not_apply_a_hand_written_cognitive_policy() -> None:
    runtime = SynrheonRuntime(cycle_interval_seconds=10.0)
    try:
        runtime.start()
        runtime.define_concept("daisy", "Daisy")
        runtime.define_concept("dog", "dog")
        runtime.define_world_relation("daisy", "IS_A", "dog")
        runtime.define_self_relation("dog", "personally_relevant_to_self", 0.9, 0.9)
        before = runtime.snapshot()["cognitive_substrate"]

        state = runtime.send_external_stimulus("Daisy")

        assert state["experience_thread"]["events"][-1]["text"] == "Daisy"
        assert state["experience_thread"]["events"][-1]["origin"] == "observed"
        assert state["cognitive_substrate"] == before
        assert "cognitive_frames" not in state
        assert not any(event["event"] == "cognition_activated" for event in state["trace"])
    finally:
        runtime.close()


def test_runtime_controls_require_start_and_reject_empty_input() -> None:
    runtime = SynrheonRuntime(cycle_interval_seconds=10.0)
    try:
        with pytest.raises(RuntimeError):
            runtime.think_one_step()

        runtime.start()
        before = runtime.snapshot()
        with pytest.raises(ValueError):
            runtime.send_external_stimulus("   ")
        assert runtime.snapshot() == before
    finally:
        runtime.close()


def test_http_boundary_preserves_ui_and_process_without_heuristic_cognition() -> None:
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
        post(
            "/api/world-relation",
            {
                "source_concept_id": "daisy",
                "relation": "IS_A",
                "target_concept_id": "dog",
                "confidence": 1.0,
            },
        )
        related = post(
            "/api/self-relation",
            {
                "concept_id": "dog",
                "relation_type": "protective_of",
                "strength": 0.7,
                "confidence": 0.9,
            },
        )
        chatted = post("/api/stimulus", {"text": "Daisy"})
        thought = post("/api/thought", {"text": "Inspect the current state"})

        assert related["state"]["cognitive_substrate"]["self_relations"][0]["injected"][0]["relation_type"] == "protective_of"
        assert chatted["state"]["experience_thread"]["events"][-1]["origin"] == "observed"
        assert thought["state"]["experience_thread"]["events"][-1]["origin"] == "injected"
        assert "cognitive_frames" not in chatted["state"]
        assert chatted["state"]["cognitive_substrate"]["activation"] == {}

        with urlopen(f"{base}/", timeout=2) as response:  # noqa: S310
            html = response.read().decode("utf-8")
        assert "Synrheon Chat" in html
        assert "Internal Thought" in html
        assert "Knowledge" in html
        assert "Inject Self Relation" in html

        bad_request = Request(
            f"{base}/api/self-relation",
            data=json.dumps(
                {"concept_id": "dog", "relation_type": "", "strength": 0.7}
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
