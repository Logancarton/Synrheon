"""Minimal observable state for the Synrheon organism.

Stage 0B intentionally keeps this state mechanically simple. It gives the runtime a
real state object to own and expose without pretending that cognition exists yet.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Literal
from uuid import uuid4


RunStatus = Literal["off", "paused", "running"]
StimulusKind = Literal["external", "internal"]


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp for observable runtime events."""
    return datetime.now(UTC).isoformat()


@dataclass(slots=True)
class StimulusRecord:
    """One external chat stimulus or explicitly injected internal thought."""

    sequence: int
    kind: StimulusKind
    text: str
    created_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-safe representation for the observation surface."""
        return asdict(self)


@dataclass(slots=True)
class TraceEvent:
    """One observable runtime event.

    Trace events explain what the harness did. They are not hidden reasoning and do
    not claim that Synrheon performed cognition.
    """

    sequence: int
    event: str
    detail: str
    created_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-safe representation for the observation surface."""
        return asdict(self)


@dataclass(slots=True)
class OrganismState:
    """Smallest persistent state needed by the Stage 0B running organism."""

    session_id: str | None = None
    status: RunStatus = "off"
    cycle: int = 0
    event_sequence: int = 0
    stimuli: list[StimulusRecord] = field(default_factory=list)
    trace: list[TraceEvent] = field(default_factory=list)

    def begin_session(self) -> None:
        """Create a fresh live session and place it in paused mode."""
        self.session_id = str(uuid4())
        self.status = "paused"
        self.cycle = 0
        self.event_sequence = 0
        self.stimuli.clear()
        self.trace.clear()

    def next_event_sequence(self) -> int:
        """Return the next monotonically increasing observable event number."""
        self.event_sequence += 1
        return self.event_sequence

    def snapshot(self) -> dict[str, object]:
        """Return a detached JSON-safe snapshot for the UI/API."""
        return {
            "session_id": self.session_id,
            "status": self.status,
            "cycle": self.cycle,
            "event_sequence": self.event_sequence,
            "stimuli": [stimulus.to_dict() for stimulus in self.stimuli],
            "trace": [event.to_dict() for event in self.trace],
        }
