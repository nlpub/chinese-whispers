"""
This is an implementation of the Chinese Whispers clustering algorithm.
"""

import random
from collections import defaultdict
from math import log2
from operator import itemgetter
from typing import TypeVar, Callable, Sequence, Union, Dict, DefaultDict, Optional, Set, cast, ItemsView, TypedDict

from networkx.classes import Graph
from networkx.utils import create_py_random_state

T = TypeVar('T')


class WeightDict(TypedDict):
    """A dictionary-like class that stores weights for nodes.

    Attributes:
        weight: The weight value associated with a key.
    """
    weight: float


# noinspection PyPep8Naming
def top_weighting(G: 'Graph[T]', node: T, neighbor: T) -> float:
    """
    Return the weight of an edge between two nodes.

    This function calculates the weight of an edge between two nodes in a graph.
    The weight is determined by the 'weight' attribute of the edge.
    If the 'weight' attribute is not present, a default weight of 1.0 is assumed.

    Parameters:
        G: The graph containing the edge.
        node: The source node of the edge.
        neighbor: The target node of the edge.

    Returns:
        The weight of the edge.
    """
    return cast(WeightDict, G[node][neighbor]).get('weight', 1.)


# noinspection PyPep8Naming
def linear_weighting(G: 'Graph[T]', node: T, neighbor: T) -> float:
    """
    Calculates the weight of an edge between two nodes in a graph using linear weighting,
    which is the edge weight divided by the degree of the destination node.
    If the 'weight' attribute is not present, a default weight of 1.0 is assumed.

    Parameters:
        G: The graph that contains the nodes and edges.
        node: The source node of the edge.
        neighbor: The destination node of the edge.

    Returns:
        The weight of the edge.
    """
    return cast(WeightDict, G[node][neighbor]).get('weight', 1.) / G.degree[neighbor]


# noinspection PyPep8Naming
def log_weighting(G: 'Graph[T]', node: T, neighbor: T) -> float:
    """
    Calculates the weight of an edge between two nodes in a graph using logarithm weighting,
    which is the edge weight divided by the logarithm of the degree of the destination node.
    If the 'weight' attribute is not present, a default weight of 1.0 is assumed.

    Parameters:
        G: The graph that contains the nodes and edges.
        node: The source node of the edge.
        neighbor: The destination node of the edge.

    Returns:
        The weight of the edge.
    """
    return cast(WeightDict, G[node][neighbor]).get('weight', 1.) / log2(G.degree[neighbor] + 1)


"""Shortcuts for the node weighting functions."""
WEIGHTING: Dict[str, Callable[['Graph[T]', T, T], float]] = {
    'top': top_weighting,
    'lin': linear_weighting,
    'log': log_weighting
}


def resolve_weighting(
        weighting: Union[str, Callable[['Graph[T]', T, T], float]]
) -> Callable[['Graph[T]', T, T], float]:
    """
    Resolve the weighting function.

    Parameters:
        weighting: The weighing method to use.
            It can be either a string specifying one of the three available schemas ('top', 'lin', 'log'),
            or a custom weighting function. Defaults to 'top'.

    Returns:
        The weighting function.
    """
    if isinstance(weighting, str):
        return WEIGHTING[weighting]
    else:
        return weighting


# noinspection PyPep8Naming
def chinese_whispers(
        G: 'Graph[T]',
        weighting: Union[str, Callable[['Graph[T]', T, T], float]] = 'top',
        iterations: int = 20,
        seed: Optional[int] = None,
        label_key: str = 'label'
) -> 'Graph[T]':
    """
    Perform clustering of nodes in a graph using the 'weighting' method.

    Parameters:
        G: The input graph.
        weighting: The weighing method to use.
            It can be either a string specifying one of the three available schemas ('top', 'lin', 'log'),
            or a custom weighting function. Defaults to 'top'.
        iterations: The maximum number of iterations to perform. Defaults to 20.
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
    weighting_func = resolve_weighting(weighting)

    rng = create_py_random_state(seed)

    for i, node in enumerate(G):
        G.nodes[node][label_key] = i + 1

    nodes = list(G)

    for i in range(iterations):
        changes = False

        rng.shuffle(nodes)

        for node in nodes:
            previous = G.nodes[node][label_key]

            if G[node]:
                scores = score(G, node, weighting_func, label_key)
                G.nodes[node][label_key] = random_argmax(scores.items(), choice=rng.choice)

            changes = changes or previous != G.nodes[node][label_key]

        if not changes:
            break

    return G


# noinspection PyPep8Naming
def score(
        G: 'Graph[T]',
        node: T,
        weighting_func: Callable[['Graph[T]', T, T], float],
        label_key: str
) -> DefaultDict[int, float]:
    """
    Compute label scores in the given node neighborhood.

    Parameters:
        G: The input graph.
        node: The node in the graph.
        weighting_func: A function to calculate the weight between two nodes.
        label_key: The key to access the label value for each node in the graph.

    Returns:
        A dictionary with label scores as values.
    """
    scores: DefaultDict[int, float] = defaultdict(float)

    if node not in G:
        return scores

    for neighbor in G[node]:
        scores[G.nodes[neighbor][label_key]] += weighting_func(G, node, neighbor)

    return scores


def random_argmax(
        items: ItemsView[T, float],
        choice: Callable[[Sequence[T]], T] = random.choice
) -> Optional[int]:
    """
    An argmax function that breaks the ties randomly.

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

    return cast('Optional[int]', choice(keys))


# noinspection PyPep8Naming
def aggregate_clusters(
        G: 'Graph[T]',
        label_key: str = 'label'
) -> Dict[int, Set[T]]:
    """
    Produce a dictionary with the keys being cluster IDs and the values being sets of cluster elements.

    Parameters:
        G: The graph object containing the clusters.
        label_key: The attribute key used to identify the clusters. Defaults to 'label'.

    Returns:
        A dictionary where the keys represent cluster IDs and the values are sets of cluster elements.
    """

    clusters: Dict[int, Set[T]] = {}

    for node in G:
        label = G.nodes[node][label_key]

        if label not in clusters:
            clusters[label] = {node}
        else:
            clusters[label].add(node)

    return clusters
