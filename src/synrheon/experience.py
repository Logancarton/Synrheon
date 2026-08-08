"""Autobiographical experience owner.

Meaningful external and internal events become an ordered thread with provenance and
explicit before/after links. This is current-episode experience, not durable memory.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal
from uuid import uuid4

from synrheon.time import TemporalCoordinate

ExperienceKind = Literal["external", "internal"]
ExperienceOrigin = Literal["observed", "injected"]


@dataclass(slots=True)
class ExperienceEvent:
    """One event in the organism's ordered autobiographical thread."""

    event_id: str
    kind: ExperienceKind
    origin: ExperienceOrigin
    text: str
    time: TemporalCoordinate
    previous_event_id: str | None = None
    next_event_id: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "event_id": self.event_id,
            "kind": self.kind,
            "origin": self.origin,
            "text": self.text,
            "time": self.time.to_dict(),
            "previous_event_id": self.previous_event_id,
            "next_event_id": self.next_event_id,
        }


@dataclass(slots=True)
class ExperienceThread:
    """One current-episode memory thread with explicit sequence links."""

    episode_id: str | None = None
    events: list[ExperienceEvent] = field(default_factory=list)

    def begin_episode(self, episode_id: str) -> None:
        self.episode_id = episode_id
        self.events.clear()

    def append(
        self,
        *,
        kind: ExperienceKind,
        origin: ExperienceOrigin,
        text: str,
        coordinate: TemporalCoordinate,
    ) -> ExperienceEvent:
        if self.episode_id is None or coordinate.episode_id != self.episode_id:
            raise RuntimeError("Experience coordinate does not belong to the active episode.")

        previous = self.events[-1] if self.events else None
        event = ExperienceEvent(
            event_id=str(uuid4()),
            kind=kind,
            origin=origin,
            text=text,
            time=coordinate,
            previous_event_id=previous.event_id if previous else None,
        )
        if previous is not None:
            previous.next_event_id = event.event_id
        self.events.append(event)
        return event

    def snapshot(self) -> dict[str, object]:
        return {
            "episode_id": self.episode_id,
            "events": [event.to_dict() for event in self.events],
        }
