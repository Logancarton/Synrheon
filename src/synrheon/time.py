"""Computational time owner for ordered organism experience."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""
    return datetime.now(UTC).isoformat()


@dataclass(slots=True, frozen=True)
class TemporalCoordinate:
    """One meaningful event's position in the current episode."""

    sequence: int
    occurred_at: str
    episode_id: str
    elapsed_seconds: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(slots=True)
class ComputationalTime:
    """Own monotonic experience sequence and episode-relative time."""

    episode_id: str | None = None
    episode_started_at: str | None = None
    experience_sequence: int = 0
    last_event_at: str | None = None

    def begin_episode(self, episode_id: str) -> None:
        now = datetime.now(UTC)
        self.episode_id = episode_id
        self.episode_started_at = now.isoformat()
        self.experience_sequence = 0
        self.last_event_at = None

    def next_coordinate(self) -> TemporalCoordinate:
        if self.episode_id is None or self.episode_started_at is None:
            raise RuntimeError("Start a Synrheon episode before recording experience.")

        now = datetime.now(UTC)
        started = datetime.fromisoformat(self.episode_started_at)
        self.experience_sequence += 1
        self.last_event_at = now.isoformat()
        return TemporalCoordinate(
            sequence=self.experience_sequence,
            occurred_at=self.last_event_at,
            episode_id=self.episode_id,
            elapsed_seconds=max(0.0, (now - started).total_seconds()),
        )

    def snapshot(self) -> dict[str, object]:
        return {
            "episode_id": self.episode_id,
            "episode_started_at": self.episode_started_at,
            "experience_sequence": self.experience_sequence,
            "last_event_at": self.last_event_at,
        }
