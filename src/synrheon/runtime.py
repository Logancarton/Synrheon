"""Thin Synrheon runtime / integration owner.

Runtime sequences owners and routes commands. It does not own semantic interpretation,
memory, learning, retrieval, abstraction, or problem-solving cognition.
"""

from __future__ import annotations

from pathlib import Path
from threading import Event, RLock, Thread
from time import sleep
from typing import Sequence

from synrheon.acquisition_routing import AcquisitionNeed, acquire_route, route_segmentation
from synrheon.policy_learning import load_recorded_learning_metrics
from synrheon.state import Concept, OrganismState, StimulusKind, StimulusRecord, TraceEvent, WorldRelation
from synrheon.surface_segmentation import segment_surface
from synrheon.temporal import utc_now

_E011A_EVIDENCE_FILE = Path(__file__).resolve().parents[2] / "data" / "e011a_v1_evidence.json"


class SynrheonRuntime:
    """Sequence the live organism while keeping cognition in its owners."""

    def __init__(self, cycle_interval_seconds: float = 0.75) -> None:
        self._state = OrganismState()
        self._state.learning_metrics = load_recorded_learning_metrics(_E011A_EVIDENCE_FILE)
        self._lock = RLock()
        self._stop_event = Event()
        self._cycle_interval_seconds = cycle_interval_seconds
        self._worker = Thread(target=self._continue_loop, name="synrheon-runtime", daemon=True)
        self._worker.start()

    def start(self) -> dict[str, object]:
        with self._lock:
            self._state.begin_session()
            self._trace("session_started", "Synrheon session started in paused mode.")
            return self._state.snapshot()

    def pause(self) -> dict[str, object]:
        with self._lock:
            self._require_started()
            self._state.status = "paused"
            self._trace("paused", "Automatic cognitive cycles paused.")
            return self._state.snapshot()

    def continue_thinking(self) -> dict[str, object]:
        with self._lock:
            self._require_started()
            self._state.status = "running"
            self._trace("continued", "Automatic cognitive cycles enabled.")
            return self._state.snapshot()

    def think_one_step(self) -> dict[str, object]:
        with self._lock:
            self._require_started()
            if self._state.status == "running":
                raise RuntimeError("Pause Synrheon before requesting exactly one step.")
            self._advance_cycle("manual")
            return self._state.snapshot()

    def send_external_stimulus(self, text: str) -> dict[str, object]:
        return self._record_stimulus("external", text)

    def inject_internal_thought(self, text: str) -> dict[str, object]:
        return self._record_stimulus("internal", text)

    def define_concept(self, concept_id: str, label: str) -> dict[str, object]:
        """Route explicit developer knowledge injection to the substrate owner."""
        with self._lock:
            self._require_started()
            concept = Concept(concept_id=concept_id.strip(), label=label.strip())
            self._state.substrate.add_concept(concept)
            self._trace("concept_injected", f"Injected concept {concept.concept_id}: {concept.label}.")
            return self._state.snapshot()

    def define_world_relation(
        self,
        source_concept_id: str,
        relation: str,
        target_concept_id: str,
        confidence: float = 1.0,
    ) -> dict[str, object]:
        """Route explicit world knowledge without treating it as self-learned."""
        with self._lock:
            self._require_started()
            world_relation = WorldRelation(
                source_concept_id=source_concept_id.strip(),
                relation=relation.strip(),
                target_concept_id=target_concept_id.strip(),
                origin="injected",
                confidence=confidence,
            )
            self._state.substrate.add_world_relation(world_relation)
            self._trace(
                "world_relation_injected",
                f"{world_relation.source_concept_id} {world_relation.relation} "
                f"{world_relation.target_concept_id}.",
            )
            return self._state.snapshot()

    def define_self_relation(
        self,
        concept_id: str,
        relation_type: str,
        strength: float,
        confidence: float = 1.0,
    ) -> dict[str, object]:
        """Route arbitrary injected organism-relative scaffolding to the substrate."""
        with self._lock:
            self._require_started()
            relation = self._state.substrate.set_injected_self_relation(
                concept_id=concept_id.strip(),
                relation_type=relation_type,
                strength=strength,
                confidence=confidence,
            )
            self._trace(
                "self_relation_injected",
                f"self {relation.relation_type} {concept_id.strip()} = {relation.strength:.3f}.",
            )
            return self._state.snapshot()

    def inspect_segmentation(self, text: str) -> dict[str, object]:
        """Segment text for inspection without recording a stimulus or mutating state.

        This is the stimulus-testing entry point for TD-3. It observes surface
        structure only; it creates no token card, sense, or concept.
        """
        return segment_surface(text).to_dict()

    def inspect_acquisition(self, text: str) -> dict[str, object]:
        """Route text against the live deck without recording or acquiring anything.

        This is the stimulus-testing entry point for TD-4. Routing is read-only:
        acquisition is a separate explicit decision.
        """
        with self._lock:
            return route_segmentation(
                segment_surface(text), self._state.substrate.token_deck
            ).to_dict()

    def acquire_from_text(
        self,
        text: str,
        *,
        needs: Sequence[AcquisitionNeed] | None = None,
    ) -> dict[str, object]:
        """Explicitly admit routed unknown forms from text into the Token Deck.

        This is the deliberate developer decision that TD-4 routing deliberately withholds.
        Nothing on the stimulus path calls it. ``needs`` optionally restricts which
        acquisition classes are admitted, so `unresolved` forms can be left alone.

        Identity only: no sense is created, because deciding what a token can mean is a
        TD-5 question.
        """

        cleaned = text.strip()
        if not cleaned:
            raise ValueError("Acquisition text cannot be empty.")

        with self._lock:
            self._require_started()
            deck = self._state.substrate.token_deck
            report = route_segmentation(segment_surface(cleaned), deck)
            admitted = [
                route
                for route in report.unknown()
                if needs is None or route.acquisition_need in set(needs)
            ]

            coordinate = self._state.computational_time.next_coordinate()
            acquired: list[str] = []
            for route in admitted:
                card = acquire_route(
                    deck,
                    route,
                    evidence_id=f"acquisition-{coordinate.sequence}-{route.span_index}",
                    origin="observed",
                    context_id=self._state.session_id,
                )
                acquired.append(f"{route.surface}={route.acquisition_need}->{card.token_id}")

            self._trace(
                "tokens_acquired",
                f"Explicitly acquired {len(acquired)} of {len(report.unknown())} unknown "
                f"form(s) with no senses: {', '.join(acquired) if acquired else 'none'}.",
            )
            return self._state.snapshot()

    def snapshot(self) -> dict[str, object]:
        with self._lock:
            return self._state.snapshot()

    def close(self) -> None:
        self._stop_event.set()
        self._worker.join(timeout=1.5)

    def _record_stimulus(self, kind: StimulusKind, text: str) -> dict[str, object]:
        cleaned = text.strip()
        if not cleaned:
            raise ValueError("Stimulus text cannot be empty.")

        with self._lock:
            self._require_started()
            coordinate = self._state.computational_time.next_coordinate()
            origin = "observed" if kind == "external" else "injected"
            experience_event = self._state.experience.append(
                kind=kind,
                origin=origin,
                text=cleaned,
                coordinate=coordinate,
            )

            segmentation = segment_surface(cleaned)
            acquisition = route_segmentation(segmentation, self._state.substrate.token_deck)
            sequence = self._state.next_event_sequence()
            self._state.stimuli.append(
                StimulusRecord(
                    sequence=sequence,
                    kind=kind,
                    text=cleaned,
                    created_at=coordinate.occurred_at,
                    experience_event_id=experience_event.event_id,
                    segmentation=segmentation,
                    acquisition=acquisition,
                )
            )
            label = "chat_stimulus_received" if kind == "external" else "thought_injected"
            detail = (
                f"External chat stimulus became observed experience #{coordinate.sequence}."
                if kind == "external"
                else f"Internal injection became injected experience #{coordinate.sequence}."
            )
            self._state.trace.append(
                TraceEvent(
                    sequence=sequence,
                    event=label,
                    detail=detail,
                    created_at=coordinate.occurred_at,
                )
            )
            self._trace(
                "surface_segmented",
                f"{segmentation.segmenter_version} observed {len(segmentation.spans)} spans "
                f"({len(segmentation.lookup_spans())} lookup candidates) in stimulus "
                f"#{sequence}; no sense or concept was assigned.",
            )
            self._trace(
                "acquisition_routed",
                f"{acquisition.router_version} routed {len(acquisition.routes)} lookup spans: "
                f"{len(acquisition.known())} known, {len(acquisition.unknown())} unknown "
                f"{acquisition.need_counts()}; no token card was created.",
            )
            return self._state.snapshot()

    def _advance_cycle(self, source: str) -> None:
        self._state.cycle += 1
        self._trace(
            "cycle_advanced",
            f"Observable cycle {self._state.cycle} advanced by {source} control.",
        )

    def _trace(self, event: str, detail: str) -> None:
        sequence = self._state.next_event_sequence()
        self._state.trace.append(
            TraceEvent(sequence=sequence, event=event, detail=detail, created_at=utc_now())
        )

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
    """Start the connected development application."""
    from synrheon.dev_server import run_development_server

    runtime = SynrheonRuntime()
    try:
        run_development_server(runtime)
    finally:
        runtime.close()
