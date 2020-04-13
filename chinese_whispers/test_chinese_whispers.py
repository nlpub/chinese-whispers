#!/usr/bin/env python3

import sys
import unittest
from random import Random

if sys.version_info[:2] >= (3, 5):
    from typing import Tuple, Sequence

import networkx as nx

from .chinese_whispers import chinese_whispers, aggregate_clusters, random_argmax


class TestRandomArgMax(unittest.TestCase):
    EMPTY = []  # type: Sequence[Tuple[int, int]]
    ITEMS = [(1, 3), (2, 1), (3, 2), (4, 3)]

    def test_empty(self):
        self.assertIsNone(random_argmax(self.EMPTY))

    def test_items(self):
        self.assertEqual(4, random_argmax(self.ITEMS, Random(0).choice))
        self.assertEqual(1, random_argmax(self.ITEMS, Random(1).choice))
        self.assertEqual(1, random_argmax(self.ITEMS, Random(2).choice))


class TestChineseWhispers(unittest.TestCase):
    SEED = 1337

    G = nx.karate_club_graph()

    def setUp(self):
        self.H = chinese_whispers(self.G, seed=self.SEED)

    def test_return(self):
        self.assertEqual(self.G, self.H)

    def test_labels(self):
        self.assertEqual(34, len(self.H.nodes))

        self.assertEqual(self.G.nodes, self.H.nodes)

        for node in self.H:
            self.assertIsNotNone(self.H.nodes[node]['label'])

    def test_aggregation(self):
        clusters = aggregate_clusters(self.H)

        self.assertEqual(2, len(clusters))

        index = {node: cluster_id for cluster_id, cluster in clusters.items() for node in cluster}

        self.assertEqual(34, len(index))
        self.assertTrue(index[0] != index[33])


if __name__ == '__main__':
    unittest.main()
