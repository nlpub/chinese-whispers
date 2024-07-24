#!/usr/bin/env python3

"""A command-line interface for Chinese Whispers."""

import argparse

import networkx as nx

from chinese_whispers import WEIGHTING, aggregate_clusters, chinese_whispers
from chinese_whispers import __version__ as version


def main() -> None:
    """Entry point for the Chinese Whispers command-line interface."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--weighting", choices=WEIGHTING.keys(), default="lin")
    parser.add_argument("--delimiter", default="\t")
    parser.add_argument("--iterations", type=int, default=20)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--version", action="version", version="Chinese Whispers v" + version)
    parser.add_argument("edges", type=argparse.FileType("r", encoding="UTF-8"))
    args = parser.parse_args()

    lines = (line.rstrip() for line in args.edges)

    G = nx.parse_edgelist(  # type: ignore[call-overload]
        lines,
        delimiter=args.delimiter,
        comments="\n",
        data=(("weight", float),),
    )

    chinese_whispers(G, args.weighting, args.iterations, args.seed)

    for label, elements in aggregate_clusters(G).items():
        elements_str = ", ".join(elements)

        print("\t".join((str(label), str(len(elements)), elements_str)))  # noqa: T201


if __name__ == "__main__":
    main()
