"""An implementation of the Chinese Whispers clustering algorithm."""

from __future__ import annotations

import math
import random
from collections import defaultdict
from enum import Enum
from math import log2
from operator import itemgetter
from typing import TYPE_CHECKING, Literal, Protocol, TypedDict, TypeVar, cast, overload

from networkx.utils import create_py_random_state

if TYPE_CHECKING:
    from collections.abc import Callable, Collection, Container, Sequence

    from networkx.classes import Graph

T = TypeVar("T")


class UnknownWeightingError(ValueError):
    """Exception raised when an unknown weighting schema is encountered."""

    def __init__(self, weighting: object) -> None:
        """Initialize the exception with the unknown weighting."""
        super().__init__(f"Unknown weighting: {weighting}")


class WeightDict(TypedDict):
    """
    A dictionary-like class that stores weights for nodes.

    Attributes:
        weight: The weight value associated with a key.

    """

    weight: float


def top_weighting(graph: Graph[T], node: T, neighbor: T) -> float:
    """
    Return the weight of an edge between two nodes.

    This function calculates the weight of an edge between two nodes in a graph.
    The weight is determined by the 'weight' attribute of the edge.
    If the 'weight' attribute is not present, a default weight of 1.0 is assumed.

    Args:
        graph: The graph containing the edge.
        node: The source node of the edge.
        neighbor: The target node of the edge.

    Returns:
        The weight of the edge.

    """
    return cast("WeightDict", graph[node][neighbor]).get("weight", 1.0)


def linear_weighting(graph: Graph[T], node: T, neighbor: T) -> float:
    """
    Calculate the edge weight using the linear weighting schema.

    This function calculates the weight of an edge between two nodes in a graph using linear weighting,
    which is the edge weight divided by the degree of the destination node.
    If the 'weight' attribute is not present, a default weight of 1.0 is assumed.

    Args:
        graph: The graph that contains the nodes and edges.
        node: The source node of the edge.
        neighbor: The destination node of the edge.

    Returns:
        The weight of the edge.

    """
    return cast("WeightDict", graph[node][neighbor]).get("weight", 1.0) / graph.degree[neighbor]


def log_weighting(graph: Graph[T], node: T, neighbor: T) -> float:
    """
    Calculate the edge weight using the logarithm weighting schema.

    This function calculates the weight of an edge between two nodes in a graph using logarithm weighting,
    which is the edge weight divided by the logarithm of the degree of the destination node.
    If the 'weight' attribute is not present, a default weight of 1.0 is assumed.

    Args:
        graph: The graph that contains the nodes and edges.
        node: The source node of the edge.
        neighbor: The destination node of the edge.

    Returns:
        The weight of the edge.

    """
    return cast("WeightDict", graph[node][neighbor]).get("weight", 1.0) / log2(graph.degree[neighbor] + 1)


class WeightingFunc(Protocol[T]):
    """Callable protocol for edge weighting functions."""

    def __call__(self, graph: Graph[T], u: T, v: T) -> float:
        """Calculate the weight of an edge between two nodes in a graph."""
        ...


class Weighting(Enum):
    """Available weighting schemas."""

    TOP = "top"
    LINEAR = "linear"
    LOGARITHMIC = "logarithmic"

    def __call__(self, graph: Graph[T], u: T, v: T) -> float:
        """Resolve to the corresponding weighting function and call it."""
        if self is Weighting.TOP:
            return top_weighting(graph, u, v)
        if self is Weighting.LINEAR:
            return linear_weighting(graph, u, v)
        if self is Weighting.LOGARITHMIC:
            return log_weighting(graph, u, v)

        raise UnknownWeightingError(self)


@overload
def resolve_weighting(weighting: Literal["top", "linear", "logarithmic", "log"]) -> WeightingFunc[T]: ...


@overload
def resolve_weighting(weighting: Weighting) -> WeightingFunc[T]: ...


@overload
def resolve_weighting(weighting: WeightingFunc[T]) -> WeightingFunc[T]: ...


@overload
def resolve_weighting(weighting: str) -> WeightingFunc[T]: ...


def resolve_weighting(weighting: str | Weighting | WeightingFunc[T]) -> WeightingFunc[T]:
    """
    Resolve the weighting function.

    Args:
        weighting: The weighing method to use.
            It can be either a string specifying one of the available schemas ('top', 'linear', 'logarithmic'),
            an instance of the Weighting enum, or a custom weighting function. Defaults to 'top'.

    Returns:
        The weighting function.

    """
    if isinstance(weighting, Weighting):
        return weighting

    if isinstance(weighting, str):
        try:
            return Weighting(weighting.lower())
        except ValueError:
            if weighting.lower() == "log":
                return Weighting.LOGARITHMIC
            raise UnknownWeightingError(weighting) from None

    return weighting


def chinese_whispers(
    graph: Graph[T],
    weighting: Literal["top", "linear", "logarithmic", "log"] | Weighting | WeightingFunc[T] | None = None,
    iterations: int = 20,
    ignore: Container[T] | None = None,
    seed: int | None = None,
    label_key: str = "label",
) -> Graph[T]:
    """
    Perform clustering of nodes in a graph using the 'weighting' method.

    Args:
        graph: The input graph.
        weighting: The weighing method to use.
            It can be either a string specifying one of the available schemas ('top', 'linear', 'logarithmic', 'log'),
            an instance of the Weighting Enum, or a custom weighting function. Defaults to Weighting.TOP.
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

    weighting_func: WeightingFunc[T] = resolve_weighting(weighting or "top")

    rng = create_py_random_state(seed)

    nodes: list[T] = []

    for node in graph:
        graph.nodes[node].pop(label_key, None)

        if node not in ignore:
            nodes.append(node)

            graph.nodes[node][label_key] = len(nodes)

    for _ in range(iterations):
        changes = False

        rng.shuffle(nodes)

        for node in nodes:
            previous = graph.nodes[node][label_key]

            if graph[node]:
                scores = score(graph, node, weighting_func, ignore, label_key)

                graph.nodes[node][label_key] = random_argmax(scores.items(), choice=rng.choice)

            changes = changes or previous != graph.nodes[node][label_key]

        if not changes:
            break

    return graph


def score(
    graph: Graph[T],
    node: T,
    weighting_func: WeightingFunc[T],
    ignore: Container[T],
    label_key: str,
) -> defaultdict[int, float]:
    """
    Compute label scores in the given node neighborhood.

    Args:
        graph: The input graph.
        node: The node in the graph.
        weighting_func: A function to calculate the weight between two nodes.
        ignore: The set of nodes to ignore.
        label_key: The key to access the label value for each node in the graph.

    Returns:
        A dictionary with label scores as values.

    """
    scores: defaultdict[int, float] = defaultdict(float)

    if node not in graph or node in ignore:
        return scores

    for neighbor in graph[node]:
        if neighbor not in ignore:
            scores[graph.nodes[neighbor][label_key]] += weighting_func(graph, node, neighbor)

    if not scores:
        scores[graph.nodes[node][label_key]] = math.inf

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
    graph: Graph[T],
    label_key: str = "label",
) -> dict[int, set[T]]:
    """
    Produce a dictionary with the keys being cluster IDs and the values being sets of cluster elements.

    Args:
        graph: The graph object containing the clusters.
        label_key: The attribute key used to identify the clusters. Defaults to 'label'.

    Returns:
        A dictionary where the keys represent cluster IDs and the values are sets of cluster elements.

    """
    clusters: dict[int, set[T]] = {}

    for node in graph:
        label = graph.nodes[node].get(label_key)

        if label is not None:
            if label not in clusters:
                clusters[label] = {node}
            else:
                clusters[label].add(node)

    return clusters
