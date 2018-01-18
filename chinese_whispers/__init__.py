from collections import defaultdict
from math import log2
from random import shuffle


def chinese_whispers(G, weighting="top", iterations=20):
    """ Performs clustering of nodes in a NetworkX graph G
    using the 'weighting' method. Three weighing schemas are available: 
    'top' relies on the original weights; 'nolog' normalizes an edge weight 
    by the degree of the related node; 'log' normalizes an edge weight by the 
    logariphm of the output degree. """

    for i, node in enumerate(G):
        G.node[node]['label'] = i + 1

    for i in range(iterations):
        changes = False

        nodes = list(G)
        shuffle(nodes)

        for node in nodes:
            previous = G.node[node]['label']
            if G[node]:
                G.node[node]['label'] = get_new_node_label(G, node, weighting)
            
            changes = changes or previous != G.node[node]['label']

        if not changes:
            break

    return G


def get_new_node_label(G, node, weighting="top"):
    """ Updates label of the node based on the local neighborhood of the node.  """
   
    labels = defaultdict(float)
    for neighbor in G[node]:
        
        if weighting == "nolog": normalizer = log2(G.degree(neighbor) + 1.0)
        elif weighting == "log": normalizer = G.degree(neighbor) + 1.0
        else: normalizer = 1.0
       
        if "weight" in G[node][neighbor]:
             neighbor_impact = G[node][neighbor]["weight"] / normalizer 
        else:
            neighbor_impact = 1.0

        labels[G.node[neighbor]["label"]] += neighbor_impact

    top_label = max(labels.items(), key=lambda key_value: key_value[1])[0]
    
    return top_label


def aggregate_clusters(G):
    """ Takes as input the labeled graph and outputs a dictionary with the keys
    being cluster IDs and the values being sets of cluster elements. """

    clusters = defaultdict(set)

    for node in G:
        clusters[G.node[node]['label']].add(node)

    return clusters
