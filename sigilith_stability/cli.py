"""Command-line interface for the Sigilith Stability Engine."""

import argparse
import json
import sys

from .report import generate_report


def main(argv=None) -> None:
    """Entry point for the CLI."""
    parser = argparse.ArgumentParser(
        prog="sigilith-stability",
        description="Sigilith Stability Engine — structural drift detector for symbolic strings.",
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="-",
        help="Input file path, or '-' to read from stdin (default: stdin).",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="-",
        help="Output file path, or '-' to write to stdout (default: stdout).",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indentation level (default: 2).",
    )

    args = parser.parse_args(argv)

    if args.input == "-":
        text = sys.stdin.read()
    else:
        with open(args.input, encoding="utf-8") as fh:
            text = fh.read()

    lines = text.splitlines()
    report = generate_report(lines)
    output = json.dumps(report, indent=args.indent)

    if args.output == "-":
        print(output)
    else:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(output)
            fh.write("\n")
