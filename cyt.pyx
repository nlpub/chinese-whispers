#cython: boundscheck=False

import sys
import numpy as np
cimport numpy as np
import networkx as nx
from datetime import datetime
import scipy
cimport cython
from cython.parallel import prange
from libc.stdlib cimport malloc, free
from collections import Counter
from matplotlib import pyplot as plt

INT = np.intc
FLOAT = np.float32

cdef void label_this_node_unweighted(
    int arr_all_labels[], 
    const int arr_edges_o[],
    const int arr_edges_d[], 
    const int arr_cum[], 
    const int arr_shuff[], 
    int c) nogil:
    
    cdef int node_id, max_i, maxi, new_label, n, j, count, i, beginning, end, lenght, cum_index
    cum_index = arr_shuff[c]
    if cum_index == 0:
        beginning = 0
    else:
        beginning = arr_cum[cum_index - 1]
    end = arr_cum[cum_index]
    lenght = end - beginning
    node_id = arr_edges_o[beginning] 

    cdef int *arr_to_process = <int *>malloc(lenght * sizeof(int))
    cdef int *freq = <int *>malloc(lenght * sizeof(int))
    if not arr_to_process or not freq:
        with gil:
            raise MemoryError()

    try:
        for i in range(lenght):
            n = arr_edges_d[beginning + i]
            arr_to_process[i] = arr_all_labels[n]

        for i in range(lenght):
            freq[i] = -1

        for i in range(lenght):
            count = 1;
            for j in range(i + 1, lenght):    
                if arr_to_process[i] == arr_to_process[j]:      
                    count += 1
                    freq[j] = 0
            if freq[i] != 0:
                freq[i] = count

        max_i = 0
        maxi = freq[0]
        for i in range(lenght):
            if freq[i] > maxi:
                maxi = freq[i]
                max_i = i 
        new_label = arr_to_process[max_i]

        with gil:
            arr_all_labels[node_id] = new_label

    finally:
        free(arr_to_process)
        free(freq)

cdef void label_this_node_weighted(
    int arr_all_labels[], 
    const int arr_edges_o[],
    const int arr_edges_d[], 
    const int arr_cum[], 
    const int arr_shuff[], 
    const float arr_all_weights[],
    int c) nogil:
    
    cdef int node_id, max_i, new_label, n, j, i, beginning, end, lenght, cum_index
    cdef float maxi, count

    cum_index = arr_shuff[c]
    if cum_index == 0:
        beginning = 0
    else:
        beginning = arr_cum[cum_index - 1]
    end = arr_cum[cum_index]
    lenght = end - beginning
    node_id = arr_edges_o[beginning] 

    cdef int *arr_to_process = <int *>malloc(lenght * sizeof(int))
    cdef float *freq = <float *>malloc(lenght * sizeof(float))
    cdef float *weights = <float *>malloc(lenght * sizeof(float))
    if not arr_to_process or not freq or not weights:
        with gil:
            raise MemoryError()

    try:
        for i in range(lenght):
            n = arr_edges_d[beginning + i]
            arr_to_process[i] = arr_all_labels[n]
            weights[i] = arr_all_weights[beginning + i]

        for i in range(lenght):
            freq[i] = -1

        for i in range(lenght):
            count = weights[i];
            for j in range(i + 1, lenght):    
                if arr_to_process[i] == arr_to_process[j]:      
                    count += weights[j]
                    freq[j] = 0
            if freq[i] != 0:
                freq[i] = count

        max_i = 0
        maxi = freq[0]
        for i in range(lenght):
            if freq[i] > maxi:
                maxi = freq[i]
                max_i = i 
        new_label = arr_to_process[max_i]

        with gil:
            arr_all_labels[node_id] = new_label

    finally:
        free(arr_to_process)
        free(freq)
        free(weights)


def update_labels(
    int[::1] all_labels_v, 
    int[::1] edges_ov, 
    int[::1] edges_dv, 
    int[::1] cum_no_neighbors_v,
    float[::1] weights_v,
    int threads):
    
    cdef int l = len(cum_no_neighbors_v) 
    order = np.arange(l, dtype=INT)
    shuffled = np.copy(order)
    np.random.shuffle(shuffled)

    cdef const int [::1] shuffled_v = shuffled.copy()
    cdef int c
    
    if weights_v.size == 1:
        for c in prange(l, nogil=True, schedule='static', num_threads=threads): 

            label_this_node_unweighted(
                &all_labels_v[0], 
                &edges_ov[0], 
                &edges_dv[0], 
                &cum_no_neighbors_v[0], 
                &shuffled_v[0],
                c)
    else:
        for c in prange(l, nogil=True, schedule='static', num_threads=threads): 

            label_this_node_weighted(
                &all_labels_v[0], 
                &edges_ov[0], 
                &edges_dv[0], 
                &cum_no_neighbors_v[0], 
                &shuffled_v[0],
                &weights_v[0],
                c)

def chinese_whispers(G, it=20, weighted=False, threads=1):

    start=datetime.now()

    M = nx.to_scipy_sparse_matrix(G,dtype=FLOAT,format='lil')
    cdef int nodes = M.shape[0]

    edges = np.asarray(M.nonzero(), dtype=INT, order='C')
    edges_o = edges[0] #the origin of the edges
    edges_d = edges[1] #the destination of the edge
    cdef const int [::1] edges_ov = edges_o
    cdef const int [::1] edges_dv = edges_d
    
    # a graph with edges: (node1-node2, node1-node3) is represented as such:
    # edges_o = [node1, node1, node2, node3]
    # edges_d = [node2, node3, node1, node1]
    # weights = [weight_1_2, weight_1_3, weight_2_1, weight_3_1], where weight_1_2 = weight_2_1, and weight_1_3 = weight_3_1
    #
    # the labels array is a 1d array where the node id is the array index, and the label is the int value at that index
    # 

    if weighted:
        weights = M[(edges_o,edges_d)]
        weights = weights.toarray(order='C')[0]
    else:
        weights = np.asarray([0], dtype=FLOAT)
    cdef const float [::1] weights_v = weights

    edges=0
    M=0

    cum_no_neighbors = np.where(edges_o[:-1] != edges_o[1:])[0] + 1 
    cum_no_neighbors = np.append(cum_no_neighbors, len(edges_o))
    cum_no_neighbors = np.ascontiguousarray(cum_no_neighbors, dtype=INT)

    cdef int i
    all_labels = np.arange(1, nodes+1, dtype=INT)
    all_labels = np.ascontiguousarray(all_labels, dtype=INT)
    
    cdef int [::1] all_labels_v = all_labels
    cdef const int [::1] cum_no_neighbors_v = cum_no_neighbors

    sys.stderr.write('finished preparations, updating labels..\n')
    sys.stderr.write(datetime.now()-start)

    for iteration in range(it):
        update_labels(all_labels_v, edges_ov, edges_dv, cum_no_neighbors_v, weights_v, threads)

    sys.stderr.write(datetime.now()-start)

    most_10 = Counter(all_labels).most_common(10)
    sys.stderr.write('The 10 labels with the most nodes are: (label:count)\n')
    sys.stderr.write(most_10)

    for node in G:
        if G[node]:
            G.node[node]['label'] = all_labels[node]


