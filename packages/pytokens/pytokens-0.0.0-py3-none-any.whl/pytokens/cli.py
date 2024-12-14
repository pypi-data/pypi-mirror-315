"""CLI interface for pytokens."""
from __future__ import annotations

import argparse

from pytokens import greet


class CLIArgs:
    name: str


def cli(argv: list[str] | None = None) -> int:
    """CLI interface."""
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    args = parser.parse_args(argv, namespace=CLIArgs)

    print(greet(args.name))
    return 0
