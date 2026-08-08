"""Scaffold integrity plus Stage 0B connected-organism tests."""

from __future__ import annotations

import json
from threading import Thread
from urllib.request import Request, urlopen

import pytest

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


def test_http_boundary_reaches_the_real_runtime() -> None:
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
        started = post("/api/start")
        assert started["state"]["status"] == "paused"

        chatted = post("/api/stimulus", {"text": "external"})
        thought = post("/api/thought", {"text": "internal"})
        stepped = post("/api/step")

        assert chatted["state"]["stimuli"][-1]["kind"] == "external"
        assert thought["state"]["stimuli"][-1]["kind"] == "internal"
        assert stepped["state"]["cycle"] == 1

        with urlopen(f"{base}/", timeout=2) as response:  # noqa: S310
            html = response.read().decode("utf-8")
        assert "Internal Thought" in html
        assert "Start Synrheon" in html
    finally:
        server.shutdown()
        server.server_close()
        runtime.close()
        thread.join(timeout=2)
