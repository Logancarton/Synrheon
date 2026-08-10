"""Developer entry point for the Synrheon scaffold.

With no arguments this starts the observable development organism. The ``segment`` and
``route`` subcommands are stimulus-testing shortcuts: they print the exact TD-3 surface
observation and the TD-4 acquisition routing for one string without starting a session or
touching organism state.

``route`` runs against a fresh empty deck, so every lookup span is unknown. To route
against the live deck, use ``POST /api/acquisition`` or send a stimulus and read
``state.stimuli[].acquisition``.
"""

from __future__ import annotations

import argparse
import json
import sys


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="synrheon", description="Synrheon developer entry point")
    subcommands = parser.add_subparsers(dest="command")

    for name, help_text in (
        ("segment", "Print the TD-3 surface segmentation of one stimulus as JSON."),
        ("route", "Print the TD-4 acquisition routing of one stimulus against an empty deck."),
    ):
        subcommand = subcommands.add_parser(name, help=help_text)
        subcommand.add_argument(
            "text",
            nargs="?",
            help="Stimulus text; omit to read the stimulus from stdin.",
        )

    arguments = parser.parse_args(sys.argv[1:] if argv is None else argv)

    if arguments.command in {"segment", "route"}:
        from synrheon.surface_segmentation import segment_surface

        text = arguments.text if arguments.text is not None else sys.stdin.read()
        segmentation = segment_surface(text)
        if arguments.command == "segment":
            payload = segmentation.to_dict()
        else:
            from synrheon.acquisition_routing import route_segmentation
            from synrheon.token_deck import TokenDeck

            payload = route_segmentation(segmentation, TokenDeck()).to_dict()
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    from synrheon.runtime import main as run_development_organism

    run_development_organism()


if __name__ == "__main__":
    main()
