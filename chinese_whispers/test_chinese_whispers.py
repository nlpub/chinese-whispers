#!/usr/bin/env python3

from __future__ import annotations

import unittest
from random import Random
from typing import ClassVar

import networkx as nx
from networkx.utils import edges_equal

from .chinese_whispers import aggregate_clusters, chinese_whispers, random_argmax


class TestRandomArgMax(unittest.TestCase):  # noqa: D101
    EMPTY: ClassVar[set[tuple[int, int]]] = set()
    ITEMS: ClassVar[set[tuple[int, int]]] = set({1: 3, 2: 1, 3: 2, 4: 3}.items())

    def test_empty(self) -> None:  # noqa: D102
        self.assertIsNone(random_argmax(self.EMPTY))

    def test_items(self) -> None:  # noqa: D102
        self.assertEqual(4, random_argmax(self.ITEMS, Random(0).choice))
        self.assertEqual(1, random_argmax(self.ITEMS, Random(1).choice))
        self.assertEqual(1, random_argmax(self.ITEMS, Random(2).choice))


class TestChineseWhispers(unittest.TestCase):  # noqa: D101
    SEED = 1337

    G = nx.karate_club_graph()
    custom_label_key = "cluster_id"

    def setUp(self) -> None:  # noqa: D102
        # networkx/networkx#5285
        for _, _, data in self.G.edges(data=True):
            data.clear()

        self.H = chinese_whispers(self.G.copy(), seed=self.SEED)
        self.H_with_label_key = chinese_whispers(self.G.copy(), seed=self.SEED, label_key=self.custom_label_key)

    def test_return(self) -> None:  # noqa: D102
        self.assertTrue(edges_equal(self.G.edges, self.H.edges))  # type: ignore[no-untyped-call]

    def test_labels(self) -> None:  # noqa: D102
        self.assertEqual(34, len(self.H.nodes))

        self.assertEqual(list(self.G), list(self.H))

        for node in self.H:
            self.assertIsNotNone(self.H.nodes[node]["label"])

    def test_labels_with_custom_key(self) -> None:  # noqa: D102
        for node in self.H_with_label_key:
            self.assertIsNotNone(self.H_with_label_key.nodes[node][self.custom_label_key])

    def test_aggregation(self) -> None:  # noqa: D102
        clusters = aggregate_clusters(self.H)

        self.assertEqual(2, len(clusters))

        index = {node: cluster_id for cluster_id, cluster in clusters.items() for node in cluster}

        self.assertEqual(34, len(index))
        self.assertTrue(index[0] != index[33])

    def test_aggregation_with_label_key(self) -> None:  # noqa: D102
        clusters = aggregate_clusters(self.H_with_label_key, label_key=self.custom_label_key)

        self.assertEqual(2, len(clusters))

        index = {node: cluster_id for cluster_id, cluster in clusters.items() for node in cluster}

        self.assertEqual(34, len(index))
        self.assertTrue(index[0] != index[33])


if __name__ == "__main__":
    unittest.main()
