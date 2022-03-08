import random
from collections import defaultdict
from math import log2
from operator import itemgetter
from random import Random
from typing import Any, Callable, Sequence, Tuple, ItemsView, Union, Dict, DefaultDict, Optional, Set, cast

from networkx.classes import Graph
from networkx.utils import create_py_random_state


# noinspection PyPep8Naming
def top_weighting(G: Graph, node: Any, neighbor: Any) -> float:
    """A weight is the edge weight."""
    return cast(float, G[node][neighbor].get('weight', 1.))


# noinspection PyPep8Naming
def linear_weighting(G: Graph, node: Any, neighbor: Any) -> float:
    """A weight is the edge weight divided to the node degree."""
    return cast(float, G[node][neighbor].get('weight', 1.)) / cast(float, G.degree[neighbor])


# noinspection PyPep8Naming
def log_weighting(G: Graph, node: Any, neighbor: Any) -> float:
    """A weight is the edge weight divided to the log2 of node degree."""
    return cast(float, G[node][neighbor].get('weight', 1.)) / log2(G.degree[neighbor] + 1)


"""Shortcuts for the node weighting functions."""
WEIGHTING: Dict[str, Callable[[Graph, Any, Any], float]] = {
    'top': top_weighting,
    'lin': linear_weighting,
    'log': log_weighting
}


# noinspection PyPep8Naming
def chinese_whispers(G: Graph, weighting: Union[str, Callable[[Graph, Any, Any], float]] = 'top', iterations: int = 20,
                     seed: Optional[int] = None, label_key: str = 'label') -> Graph:
    """Perform clustering of nodes in a graph G using the 'weighting' method.

    Three weighing schemas are available:

    top
      Just use the edge weights from the input graph.

    lin
      Normalize an edge weight by the degree of the related node.

    log
      Normalize an edge weight by the logarithm of the related node degree.

    It is possible to specify the maximum number of iterations as well as the random seed to use."""

    weighting_func = WEIGHTING[weighting] if isinstance(weighting, str) else weighting

    rng: Random = create_py_random_state(seed)

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
def score(G: Graph, node: Any, weighting_func: Callable[[Graph, Any, Any], float],
          label_key: str) -> DefaultDict[int, float]:
    """Compute label scores in the given node neighborhood."""

    scores: DefaultDict[int, float] = defaultdict(float)

    if node not in G:
        return scores

    for neighbor in G[node]:
        scores[G.nodes[neighbor][label_key]] += weighting_func(G, node, neighbor)

    return scores


def random_argmax(items: Union[Sequence[Tuple[Any, float]], ItemsView[Any, float]],
                  choice: Callable[[Sequence[Any]], Any] = random.choice) -> Optional[int]:
    """An argmax function that breaks the ties randomly."""
    if not items:
        # https://github.com/python/mypy/issues/1003
        return None

    _, maximum = max(items, key=itemgetter(1))

    keys = [k for k, v in items if v == maximum]

    return cast('Optional[int]', choice(keys))


# noinspection PyPep8Naming
def aggregate_clusters(G: Graph, label_key: str = 'label') -> Dict[int, Set[Any]]:
    """Produce a dictionary with the keys being cluster IDs and the values being sets of cluster elements."""

    clusters: Dict[int, Set[Any]] = {}

    for node in G:
        label = G.nodes[node][label_key]

        if label not in clusters:
            clusters[label] = {node}
        else:
            clusters[label].add(node)

    return clusters
