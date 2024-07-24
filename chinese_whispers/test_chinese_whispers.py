#!/usr/bin/env python3

from __future__ import annotations

import unittest
from random import Random
from typing import ClassVar

import networkx as nx
from networkx.utils import edges_equal

from .chinese_whispers import aggregate_clusters, chinese_whispers, random_argmax


class TestRandomArgMax(unittest.TestCase):
    EMPTY: ClassVar[set[tuple[int, int]]] = set()
    ITEMS: ClassVar[set[tuple[int, int]]] = set({1: 3, 2: 1, 3: 2, 4: 3}.items())

    def test_empty(self) -> None:
        assert random_argmax(self.EMPTY) is None

    def test_items(self) -> None:
        assert random_argmax(self.ITEMS, Random(0).choice) == 4
        assert random_argmax(self.ITEMS, Random(1).choice) == 1
        assert random_argmax(self.ITEMS, Random(2).choice) == 1


class TestChineseWhispers(unittest.TestCase):
    SEED = 1337

    G = nx.karate_club_graph()
    custom_label_key = "cluster_id"

    def setUp(self) -> None:
        # networkx/networkx#5285
        for _, _, data in self.G.edges(data=True):
            data.clear()

        self.H = chinese_whispers(self.G.copy(), seed=self.SEED)
        self.H_with_label_key = chinese_whispers(self.G.copy(), seed=self.SEED, label_key=self.custom_label_key)

    def test_return(self) -> None:
        assert edges_equal(self.G.edges, self.H.edges)  # type: ignore[no-untyped-call]

    def test_labels(self) -> None:
        assert len(self.H.nodes) == 34

        assert list(self.G) == list(self.H)

        for node in self.H:
            assert self.H.nodes[node].get("label") is not None

    def test_labels_with_custom_key(self) -> None:
        for node in self.H_with_label_key:
            assert self.H_with_label_key.nodes[node][self.custom_label_key] is not None

    def test_ignore_all(self) -> None:
        H_ignore = chinese_whispers(self.G.copy(), ignore=set(self.G), seed=self.SEED)

        assert not aggregate_clusters(H_ignore)

    def test_ignore_nothing(self) -> None:
        H_ignore = chinese_whispers(self.G.copy(), ignore=set(), seed=self.SEED)

        assert aggregate_clusters(H_ignore) == aggregate_clusters(self.H)

    def test_ignore_one(self) -> None:
        ignore = {0}

        H_ignore = chinese_whispers(self.G.copy(), ignore=ignore, seed=self.SEED)

        nodes = set.union(*aggregate_clusters(H_ignore).values())

        assert set(self.G) - nodes == ignore

    def test_aggregation(self) -> None:
        clusters = aggregate_clusters(self.H)

        assert len(clusters) == 2

        index = {node: cluster_id for cluster_id, cluster in clusters.items() for node in cluster}

        assert len(index) == 34
        assert index[0] != index[33]

    def test_aggregation_with_label_key(self) -> None:
        clusters = aggregate_clusters(self.H_with_label_key, label_key=self.custom_label_key)

        assert len(clusters) == 2

        index = {node: cluster_id for cluster_id, cluster in clusters.items() for node in cluster}

        assert len(index) == 34
        assert index[0] != index[33]


if __name__ == "__main__":
    unittest.main()
