from collections import defaultdict
from math import log2
from random import shuffle


def label_weighting(G, node):
    return max(G.node[neighbor]['label'] for neighbor in G[node])


def top_weighting(G, node):
    return G.node[max(G[node], key=lambda neighbor: G[node][neighbor]['weight'])]['label']


def log_weighting(G, node):
    def weight(neighbor):
        return G[node][neighbor]['weight'] / log2(G.degree(neighbor) + 1)

    return G.node[max(G[node], key=weight)]['label']


def nolog_weighting(G, node):
    def weight(neighbor):
        return G[node][neighbor]['weight'] / G.degree(neighbor)

    return G.node[max(G[node], key=weight)]['label']


WEIGHTING = {
    'label': label_weighting,
    'top': top_weighting,
    'log': log_weighting,
    'nolog': nolog_weighting
}


def chinese_whispers(G, weighting, iterations=20):
    for i, node in enumerate(G):
        G.node[node]['label'] = i + 1

    for i in range(iterations):
        changes = False

        nodes = list(G)
        shuffle(nodes)

        for node in nodes:
            previous = G.node[node]['label']

            if G[node]:
                G.node[node]['label'] = weighting(G, node)

            changes = changes or previous != G.node[node]['label']

        if not changes:
            break

    return G


def aggregate_clusters(G):
    clusters = defaultdict(set)

    for node in G:
        clusters[G.node[node]['label']].add(node)

    return clusters
