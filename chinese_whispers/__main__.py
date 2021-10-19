#!/usr/bin/env python3

import argparse

import networkx as nx

from chinese_whispers import __version__ as version, chinese_whispers, aggregate_clusters, WEIGHTING


def main() -> None:
    """Entry point for the Chinese Whispers command-line interface."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--weighting', choices=WEIGHTING.keys(), default='lin')
    parser.add_argument('--delimiter', default='\t')
    parser.add_argument('--iterations', type=int, default=20)
    parser.add_argument('--seed', type=int, default=None)
    parser.add_argument('--version', action='version', version='Chinese Whispers v' + version)
    parser.add_argument('edges', type=argparse.FileType('r', encoding='UTF-8'))
    args = parser.parse_args()

    lines = (line.rstrip() for line in args.edges)

    # noinspection PyPep8Naming
    G = nx.parse_edgelist(lines, delimiter=args.delimiter, comments='\n', data=[('weight', float)])

    chinese_whispers(G, args.weighting, args.iterations, args.seed)

    for label, elements in aggregate_clusters(G).items():
        elements_str = ', '.join(elements)

        print('\t'.join((str(label), str(len(elements)), elements_str)))


if __name__ == '__main__':
    main()
