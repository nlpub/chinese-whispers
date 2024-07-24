"""An implementation of the Chinese Whispers clustering algorithm."""

from __future__ import annotations

import math
import random
from collections import defaultdict
from math import log2
from operator import itemgetter
from typing import TYPE_CHECKING, Literal, TypedDict, cast

from networkx.utils import create_py_random_state

if TYPE_CHECKING:
    from collections.abc import Callable, Collection, Sequence
    from typing import TypeVar

    from networkx.classes import Graph

    T = TypeVar("T")


class WeightDict(TypedDict):
    """
    A dictionary-like class that stores weights for nodes.

    Attributes:
        weight: The weight value associated with a key.

    """

    weight: float


def top_weighting(G: Graph[T], node: T, neighbor: T) -> float:
    """
    Return the weight of an edge between two nodes.

    This function calculates the weight of an edge between two nodes in a graph.
    The weight is determined by the 'weight' attribute of the edge.
    If the 'weight' attribute is not present, a default weight of 1.0 is assumed.

    Args:
        G: The graph containing the edge.
        node: The source node of the edge.
        neighbor: The target node of the edge.

    Returns:
        The weight of the edge.

    """
    return cast(WeightDict, G[node][neighbor]).get("weight", 1.)


def linear_weighting(G: Graph[T], node: T, neighbor: T) -> float:
    """
    Calculate the edge weight using the linear weighting schema.

    This function calculates the weight of an edge between two nodes in a graph using linear weighting,
    which is the edge weight divided by the degree of the destination node.
    If the 'weight' attribute is not present, a default weight of 1.0 is assumed.

    Args:
        G: The graph that contains the nodes and edges.
        node: The source node of the edge.
        neighbor: The destination node of the edge.

    Returns:
        The weight of the edge.

    """
    return cast(WeightDict, G[node][neighbor]).get("weight", 1.) / G.degree[neighbor]


def log_weighting(G: Graph[T], node: T, neighbor: T) -> float:
    """
    Calculate the edge weight using the logarithm weighting schema.

    This function calculates the weight of an edge between two nodes in a graph using logarithm weighting,
    which is the edge weight divided by the logarithm of the degree of the destination node.
    If the 'weight' attribute is not present, a default weight of 1.0 is assumed.

    Args:
        G: The graph that contains the nodes and edges.
        node: The source node of the edge.
        neighbor: The destination node of the edge.

    Returns:
        The weight of the edge.

    """
    return cast(WeightDict, G[node][neighbor]).get("weight", 1.) / log2(G.degree[neighbor] + 1)


"""Shortcuts for the node weighting functions."""
WEIGHTING: dict[str, Callable[[Graph[T], T, T], float]] = {
    "top": top_weighting,
    "lin": linear_weighting,
    "log": log_weighting,
}


def resolve_weighting(
        weighting: str | Callable[[Graph[T], T, T], float],
) -> Callable[[Graph[T], T, T], float]:
    """
    Resolve the weighting function.

    Args:
        weighting: The weighing method to use.
            It can be either a string specifying one of the three available schemas ('top', 'lin', 'log'),
            or a custom weighting function. Defaults to 'top'.

    Returns:
        The weighting function.

    """
    if isinstance(weighting, str):
        return WEIGHTING[weighting]

    return weighting


def chinese_whispers(
        G: Graph[T],
        weighting: Literal["top", "lin", "log"] | Callable[[Graph[T], T, T], float] = "top",
        iterations: int = 20,
        ignore: set[T] | None = None,
        seed: int | None = None,
        label_key: str = "label",
) -> Graph[T]:
    """
    Perform clustering of nodes in a graph using the 'weighting' method.

    Args:
        G: The input graph.
        weighting: The weighing method to use.
            It can be either a string specifying one of the three available schemas ('top', 'lin', 'log'),
            or a custom weighting function. Defaults to 'top'.
        iterations: The maximum number of iterations to perform. Defaults to 20.
        ignore: The set of nodes to ignore. Defaults to an empty set.
        seed: The random seed to use. Defaults to None.
        label_key: The key to store the cluster labels in the graph nodes. Defaults to 'label'.

    Returns:
        The input graph with cluster labels assigned to nodes.

    Three weighing schemas are available:

    - `top`: Just use the edge weights from the input graph.
    - `lin`: Normalize an edge weight by the degree of the related node.
    - `log`: Normalize an edge weight by the logarithm of the related node degree.

    It is possible to specify the maximum number of iterations as well as the random seed to use.

    """
    if ignore is None:
        ignore = set()

    weighting_func = resolve_weighting(weighting)

    rng = create_py_random_state(seed)

    nodes: list[T] = []

    for node in G:
        G.nodes[node].pop(label_key, None)

        if node not in ignore:
            nodes.append(node)

            G.nodes[node][label_key] = len(nodes)

    for _ in range(iterations):
        changes = False

        rng.shuffle(nodes)

        for node in nodes:
            previous = G.nodes[node][label_key]

            if G[node]:
                scores = score(G, node, weighting_func, ignore, label_key)

                G.nodes[node][label_key] = random_argmax(scores.items(), choice=rng.choice)

            changes = changes or previous != G.nodes[node][label_key]

        if not changes:
            break

    return G


def score(
        G: Graph[T],
        node: T,
        weighting_func: Callable[[Graph[T], T, T], float],
        ignore: set[T],
        label_key: str,
) -> defaultdict[int, float]:
    """
    Compute label scores in the given node neighborhood.

    Args:
        G: The input graph.
        node: The node in the graph.
        weighting_func: A function to calculate the weight between two nodes.
        ignore: The set of nodes to ignore.
        label_key: The key to access the label value for each node in the graph.

    Returns:
        A dictionary with label scores as values.

    """
    scores: defaultdict[int, float] = defaultdict(float)

    if node not in G or node in ignore:
        return scores

    for neighbor in G[node]:
        if neighbor not in ignore:
            scores[G.nodes[neighbor][label_key]] += weighting_func(G, node, neighbor)

    if not scores:
        scores[G.nodes[node][label_key]] = math.inf

    return scores


def random_argmax(
        items: Collection[tuple[T, float]],
        choice: Callable[[Sequence[T]], T] = random.choice,
) -> int | None:
    """
    Break the ties randomly.

    This is an argmax function that breaks the ties randomly.

    Args:
        items: A sequence of items with their corresponding weights.
        choice: A callable function that takes in a sequence of items and returns one of them.

    Returns:
        An optional integer representing the index of the maximum item, if exists.

    """
    if not items:
        # https://github.com/python/mypy/issues/1003
        return None

    _, maximum = max(items, key=itemgetter(1))

    keys = [k for k, v in items if v == maximum]

    return cast("int | None", choice(keys))


def aggregate_clusters(
        G: Graph[T],
        label_key: str = "label",
) -> dict[int, set[T]]:
    """
    Produce a dictionary with the keys being cluster IDs and the values being sets of cluster elements.

    Args:
        G: The graph object containing the clusters.
        label_key: The attribute key used to identify the clusters. Defaults to 'label'.

    Returns:
        A dictionary where the keys represent cluster IDs and the values are sets of cluster elements.

    """
    clusters: dict[int, set[T]] = {}

    for node in G:
        label = G.nodes[node].get(label_key)

        if label is not None:
            if label not in clusters:
                clusters[label] = {node}
            else:
                clusters[label].add(node)

    return clusters
