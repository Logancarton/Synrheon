"""Thin Synrheon runtime / integration owner.

Stage 0B responsibilities:
- own one live organism session
- receive distinct external and internal stimuli
- sequence one-step / continue / pause control
- expose observable state and trace

The runtime does not interpret language or own memory, retrieval, learning,
abstraction, or problem-solving cognition.
"""

from __future__ import annotations

from threading import Event, RLock, Thread
from time import sleep

from synrheon.core import OrganismState, StimulusKind, StimulusRecord, TraceEvent


class SynrheonRuntime:
    """Sequence the Stage 0B organism without pretending to implement cognition."""

    def __init__(self, cycle_interval_seconds: float = 0.75) -> None:
        self._state = OrganismState()
        self._lock = RLock()
        self._stop_event = Event()
        self._cycle_interval_seconds = cycle_interval_seconds
        self._worker = Thread(target=self._continue_loop, name="synrheon-runtime", daemon=True)
        self._worker.start()

    def start(self) -> dict[str, object]:
        """Start a fresh session in paused mode."""
        with self._lock:
            self._state.begin_session()
            self._trace("session_started", "Synrheon session started in paused mode.")
            return self._state.snapshot()

    def pause(self) -> dict[str, object]:
        """Pause future automatic cycles while preserving current state."""
        with self._lock:
            self._require_started()
            self._state.status = "paused"
            self._trace("paused", "Automatic cognitive cycles paused.")
            return self._state.snapshot()

    def continue_thinking(self) -> dict[str, object]:
        """Allow the harness to advance repeated observable cycles."""
        with self._lock:
            self._require_started()
            self._state.status = "running"
            self._trace("continued", "Automatic cognitive cycles enabled.")
            return self._state.snapshot()

    def think_one_step(self) -> dict[str, object]:
        """Advance exactly one observable cycle without inventing cognition."""
        with self._lock:
            self._require_started()
            if self._state.status == "running":
                raise RuntimeError("Pause Synrheon before requesting exactly one step.")
            self._advance_cycle("manual")
            return self._state.snapshot()

    def send_external_stimulus(self, text: str) -> dict[str, object]:
        """Record a user-facing chat stimulus as external input."""
        return self._record_stimulus("external", text)

    def inject_internal_thought(self, text: str) -> dict[str, object]:
        """Record an explicitly injected internal stimulus on a distinct channel."""
        return self._record_stimulus("internal", text)

    def snapshot(self) -> dict[str, object]:
        """Return the current detached observable state."""
        with self._lock:
            return self._state.snapshot()

    def close(self) -> None:
        """Stop the background harness thread."""
        self._stop_event.set()
        self._worker.join(timeout=1.5)

    def _record_stimulus(self, kind: StimulusKind, text: str) -> dict[str, object]:
        cleaned = text.strip()
        if not cleaned:
            raise ValueError("Stimulus text cannot be empty.")

        with self._lock:
            self._require_started()
            sequence = self._state.next_event_sequence()
            self._state.stimuli.append(StimulusRecord(sequence=sequence, kind=kind, text=cleaned))
            label = "chat_stimulus_received" if kind == "external" else "thought_injected"
            detail = (
                "External chat stimulus reached the runtime."
                if kind == "external"
                else "Internal thought injection reached the runtime."
            )
            self._state.trace.append(TraceEvent(sequence=sequence, event=label, detail=detail))
            return self._state.snapshot()

    def _advance_cycle(self, source: str) -> None:
        self._state.cycle += 1
        self._trace(
            "cycle_advanced",
            f"Observable Stage 0B cycle {self._state.cycle} advanced by {source} control.",
        )

    def _trace(self, event: str, detail: str) -> None:
        sequence = self._state.next_event_sequence()
        self._state.trace.append(TraceEvent(sequence=sequence, event=event, detail=detail))

    def _require_started(self) -> None:
        if self._state.status == "off" or self._state.session_id is None:
            raise RuntimeError("Start Synrheon before using organism controls.")

    def _continue_loop(self) -> None:
        while not self._stop_event.is_set():
            sleep(self._cycle_interval_seconds)
            with self._lock:
                if self._state.status == "running":
                    self._advance_cycle("continue")


def main() -> None:
    """Start the Stage 0B development application."""
    from synrheon.interfaces import run_development_server

    runtime = SynrheonRuntime()
    try:
        run_development_server(runtime)
    finally:
        runtime.close()
