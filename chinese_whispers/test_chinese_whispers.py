#!/usr/bin/env python3

from __future__ import annotations

from random import Random
from typing import TYPE_CHECKING, cast

import networkx as nx
import pytest
from networkx.utils import edges_equal

from .chinese_whispers import aggregate_clusters, chinese_whispers, random_argmax

if TYPE_CHECKING:
    from collections.abc import Collection


@pytest.fixture()
def empty_collection() -> Collection[tuple[int, int]]:
    return set()


@pytest.fixture()
def items_collection() -> Collection[tuple[int, int]]:
    return {1: 3, 2: 1, 3: 2, 4: 3}.items()


def test_random_argmax_empty(empty_collection: Collection[tuple[int, int]]) -> None:
    assert random_argmax(empty_collection) is None


def test_random_argmax_items(items_collection: Collection[tuple[int, int]]) -> None:
    assert random_argmax(items_collection, Random(0).choice) == 4
    assert random_argmax(items_collection, Random(1).choice) == 1
    assert random_argmax(items_collection, Random(2).choice) == 1


@pytest.fixture()
def graph() -> nx.Graph[int]:
    graph = nx.karate_club_graph()

    for _, _, data in graph.edges(data=True):
        data.clear()

    return cast("nx.Graph[int]", graph)


@pytest.fixture()
def clustered_graph(graph: nx.Graph[int]) -> nx.Graph[int]:
    return chinese_whispers(graph, seed=0)


CUSTOM_KEY = "cluster_id"


@pytest.fixture()
def clustered_graph_custom_key(graph: nx.Graph[int]) -> nx.Graph[int]:
    return chinese_whispers(graph, seed=0, label_key=CUSTOM_KEY)


def test_return(graph: nx.Graph[int], clustered_graph: nx.Graph[int]) -> None:
    assert edges_equal(graph.edges, clustered_graph.edges)  # type: ignore[no-untyped-call]


def test_labels(graph: nx.Graph[int], clustered_graph: nx.Graph[int]) -> None:
    assert len(clustered_graph.nodes) == 34

    assert list(graph) == list(clustered_graph)

    for node in clustered_graph:
        assert clustered_graph.nodes[node].get("label") is not None


def test_labels_custom_key(clustered_graph_custom_key: nx.Graph[int]) -> None:
    for node in clustered_graph_custom_key:
        assert clustered_graph_custom_key.nodes[node][CUSTOM_KEY] is not None


def test_ignore_all(graph: nx.Graph[int]) -> None:
    graph_ignored = chinese_whispers(graph, ignore=set(graph), seed=0)

    assert not aggregate_clusters(graph_ignored)


def test_ignore_nothing(graph: nx.Graph[int], clustered_graph_custom_key: nx.Graph[int]) -> None:
    graph_ignored = chinese_whispers(graph, ignore=set(), seed=0)

    assert aggregate_clusters(graph_ignored) == aggregate_clusters(clustered_graph_custom_key)


def test_ignore_one(graph: nx.Graph[int]) -> None:
    ignore = {0}

    graph_ignored = chinese_whispers(graph, ignore=ignore, seed=0)

    nodes = set.union(*aggregate_clusters(graph_ignored).values())

    assert set(graph) - nodes == ignore


def test_aggregation(clustered_graph: nx.Graph[int]) -> None:
    clusters = aggregate_clusters(clustered_graph)

    assert len(clusters) == 2

    index = {node: cluster_id for cluster_id, cluster in clusters.items() for node in cluster}

    assert len(index) == 34
    assert index[0] != index[33]


def test_aggregation_with_label_key(clustered_graph_custom_key: nx.Graph[int]) -> None:
    clusters = aggregate_clusters(clustered_graph_custom_key, label_key=CUSTOM_KEY)

    assert len(clusters) == 2

    index = {node: cluster_id for cluster_id, cluster in clusters.items() for node in cluster}

    assert len(index) == 34
    assert index[0] != index[33]
