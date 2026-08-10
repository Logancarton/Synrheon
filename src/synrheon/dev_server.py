"""Development HTTP/API boundary for the observable Synrheon organism.

This module translates browser requests into runtime commands and serves the local
UI. It does not interpret stimuli, choose cognitive routes, or own cognitive state.
"""

from __future__ import annotations

import json
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from synrheon.runtime import SynrheonRuntime


_UI_FILE = Path(__file__).resolve().parents[2] / "ui" / "index.html"


class DevelopmentRequestHandler(BaseHTTPRequestHandler):
    """Serve the UI and translate API requests into runtime calls."""

    runtime: SynrheonRuntime

    def do_GET(self) -> None:  # noqa: N802
        if self.path in {"/", "/index.html"}:
            self._send_html()
            return
        if self.path == "/api/state":
            self._send_json(HTTPStatus.OK, {"ok": True, "state": self.runtime.snapshot()})
            return
        if self.path == "/health":
            self._send_json(HTTPStatus.OK, {"ok": True, "service": "synrheon"})
            return
        self._send_json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "Not found."})

    def do_POST(self) -> None:  # noqa: N802
        try:
            payload = self._read_json()
            if self.path == "/api/segment":
                # Inspection only: returns the TD-3 observation without recording a
                # stimulus, so it has no state to send back.
                self._send_json(
                    HTTPStatus.OK,
                    {
                        "ok": True,
                        "segmentation": self.runtime.inspect_segmentation(
                            self._required_text(payload)
                        ),
                    },
                )
                return
            if self.path == "/api/acquisition":
                # Inspection only: TD-4 routing is read-only and acquires nothing.
                self._send_json(
                    HTTPStatus.OK,
                    {
                        "ok": True,
                        "acquisition": self.runtime.inspect_acquisition(
                            self._required_text(payload)
                        ),
                    },
                )
                return
            if self.path == "/api/start":
                state = self.runtime.start()
            elif self.path == "/api/pause":
                state = self.runtime.pause()
            elif self.path == "/api/continue":
                state = self.runtime.continue_thinking()
            elif self.path == "/api/step":
                state = self.runtime.think_one_step()
            elif self.path == "/api/stimulus":
                state = self.runtime.send_external_stimulus(self._required_text(payload))
            elif self.path == "/api/thought":
                state = self.runtime.inject_internal_thought(self._required_text(payload))
            elif self.path == "/api/acquire":
                state = self.runtime.acquire_from_text(
                    self._required_text(payload),
                    needs=self._optional_needs(payload),
                )
            elif self.path == "/api/concept":
                state = self.runtime.define_concept(
                    self._required_string(payload, "concept_id"),
                    self._required_string(payload, "label"),
                )
            elif self.path == "/api/world-relation":
                state = self.runtime.define_world_relation(
                    self._required_string(payload, "source_concept_id"),
                    self._required_string(payload, "relation"),
                    self._required_string(payload, "target_concept_id"),
                    self._optional_number(payload, "confidence", 1.0),
                )
            elif self.path == "/api/self-relation":
                state = self.runtime.define_self_relation(
                    self._required_string(payload, "concept_id"),
                    self._required_string(payload, "relation_type"),
                    self._required_number(payload, "strength"),
                    self._optional_number(payload, "confidence", 1.0),
                )
            else:
                self._send_json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "Not found."})
                return
        except (KeyError, ValueError, RuntimeError) as exc:
            self._send_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": str(exc)})
            return

        self._send_json(HTTPStatus.OK, {"ok": True, "state": state})

    def log_message(self, format: str, *args: Any) -> None:
        return

    def _read_json(self) -> dict[str, object]:
        length = int(self.headers.get("Content-Length", "0"))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Request body must be valid JSON.") from exc
        if not isinstance(payload, dict):
            raise ValueError("Request body must be a JSON object.")
        return payload

    @staticmethod
    def _required_text(payload: dict[str, object]) -> str:
        return DevelopmentRequestHandler._required_string(payload, "text")

    @staticmethod
    def _required_string(payload: dict[str, object], field: str) -> str:
        value = payload.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"A non-empty {field} field is required.")
        return value

    @staticmethod
    def _optional_needs(payload: dict[str, object]) -> list[str] | None:
        value = payload.get("needs")
        if value is None:
            return None
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            raise ValueError("The needs field must be a list of acquisition need names.")
        return value

    @staticmethod
    def _required_number(payload: dict[str, object], field: str) -> float:
        value = payload.get(field)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"A numeric {field} field is required.")
        return float(value)

    @staticmethod
    def _optional_number(payload: dict[str, object], field: str, default: float) -> float:
        if field not in payload:
            return default
        return DevelopmentRequestHandler._required_number(payload, field)

    def _send_html(self) -> None:
        if not _UI_FILE.exists():
            self._send_json(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"ok": False, "error": "Development UI file is missing."},
            )
            return
        body = _UI_FILE.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status: HTTPStatus, payload: dict[str, object]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def create_development_server(
    runtime: SynrheonRuntime,
    host: str = "127.0.0.1",
    port: int = 8765,
) -> ThreadingHTTPServer:
    """Create the HTTP transport around an existing runtime."""
    handler = type(
        "SynrheonDevelopmentRequestHandler",
        (DevelopmentRequestHandler,),
        {"runtime": runtime},
    )
    return ThreadingHTTPServer((host, port), handler)


def run_development_server(
    runtime: SynrheonRuntime,
    host: str = "127.0.0.1",
    port: int = 8765,
    *,
    open_browser: bool = True,
) -> None:
    """Serve the connected development UI until the user stops the process."""
    server = create_development_server(runtime, host, port)
    actual_host, actual_port = server.server_address[:2]
    url = f"http://{actual_host}:{actual_port}"
    print(f"Synrheon development organism: {url}")
    print("Press Ctrl+C to stop.")

    if open_browser:
        webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
