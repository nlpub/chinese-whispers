#!/usr/bin/env python3

import unittest

from random import Random
from chinese_whispers import chinese_whispers, aggregate_clusters, random_argmax
import networkx as nx


class TestRandomArgMax(unittest.TestCase):
    EMPTY = []
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

        self.assertIn(1, clusters.keys())
        self.assertIn(34, clusters.keys())

        self.assertEqual(clusters[1], {0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 16, 17, 19, 21})
        self.assertEqual(clusters[34], {32, 33, 8, 9, 14, 15, 18, 20, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31})


if __name__ == '__main__':
    unittest.main()
