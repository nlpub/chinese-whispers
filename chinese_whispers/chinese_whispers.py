import random
import sys
from collections import defaultdict
from math import log2
from operator import itemgetter

if sys.version_info[:2] >= (3, 5):
    from typing import Any, Callable, Sequence, Tuple, ItemsView, Union, Dict, Optional, Set

from networkx.classes import Graph


def top_weighting(G, node, neighbor):
    # type: (Graph, Any, Any) -> float
    """A weight is the edge weight."""
    return G[node][neighbor].get('weight', 1.)


def lin_weighting(G, node, neighbor):
    # type: (Graph, Any, Any) -> float
    """A weight is the edge weight divided to the node degree."""
    return G[node][neighbor].get('weight', 1.) / G.degree[neighbor]


def log_weighting(G, node, neighbor):
    # type: (Graph, Any, Any) -> float
    """A weight is the edge weight divided to the log2 of node degree."""
    return G[node][neighbor].get('weight', 1.) / log2(G.degree[neighbor] + 1)


"""Shortcuts for the node weighting functions."""
WEIGHTING = {
    'top': top_weighting,
    'lin': lin_weighting,
    'log': log_weighting
}  # type: Dict[str, Callable[[Graph, Any, Any], float]]


def chinese_whispers(G, weighting='top', iterations=20, seed=None):
    # type: (Graph, Union[str, Callable[[Graph, Any, Any], float]], int, Optional[int]) -> Graph
    """Perform clustering of nodes in a graph G using the 'weighting' method.

    Three weighing schemas are available:

    top
      Just use the edge weights from the input graph.

    lin
      Normalize an edge weight by the degree of the related node.

    log
      Normalize an edge weight by the logarithm of the related node degree.

    It is possible to specify the maximum number of iterations as well as the random seed to use."""

    if isinstance(weighting, str):
        weighting_func = WEIGHTING[weighting]
    else:
        weighting_func = weighting

    if seed:
        rng = random.Random(seed)
        shuffle_func = rng.shuffle
        choice_func = rng.choice
    else:
        shuffle_func = random.shuffle
        choice_func = random.choice

    for i, node in enumerate(G):
        G.nodes[node]['label'] = i + 1

    nodes = list(G)

    for i in range(iterations):
        changes = False

        shuffle_func(nodes)

        for node in nodes:
            previous = G.nodes[node]['label']

            if G[node]:
                scores = score(G, node, weighting_func)
                G.nodes[node]['label'] = random_argmax(scores.items(), choice_func=choice_func)

            changes = changes or previous != G.nodes[node]['label']

        if not changes:
            break

    return G


def score(G, node, weighting_func):
    # type: (Graph, Any, Callable[[Graph, Any, Any], float]) -> Dict[int, float]
    """Compute label scores in the given node neighborhood."""

    scores = defaultdict(float)  # type: Dict[int, float]

    if node not in G:
        return scores

    for neighbor in G[node]:
        scores[G.nodes[neighbor]['label']] += weighting_func(G, node, neighbor)

    return scores


def random_argmax(items, choice_func=random.choice):
    # type: (Union[Sequence[Tuple[Any, float]], ItemsView[Any, float]], Callable[[Sequence[Any]], Any]) -> Optional[int]
    """An argmax function that breaks the ties randomly."""
    if not items:
        # https://github.com/python/mypy/issues/1003
        return None

    _, maximum = max(items, key=itemgetter(1))

    keys = [k for k, v in items if v == maximum]

    return choice_func(keys)


def aggregate_clusters(G):
    # type: (Graph) -> Dict[int, Set[Any]]
    """Produce a dictionary with the keys being cluster IDs and the values being sets of cluster elements."""

    clusters = {}  # type: Dict[int, Set[Any]]

    for node in G:
        label = G.nodes[node]['label']

        if label not in clusters:
            clusters[label] = {node}
        else:
            clusters[label].add(node)

    return clusters
