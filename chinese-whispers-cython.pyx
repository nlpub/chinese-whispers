import numpy as np
cimport numpy as np
import networkx as nx
from datetime import datetime
import scipy
cimport cython
from cython.parallel import prange, threadid
from libc.stdlib cimport malloc, free
from collections import Counter
from matplotlib import pyplot as plt

DTYPE=np.intc

@cython.boundscheck(False)
cdef void label_this_node(int[:] arr_all_labels, int[:,:] arr_edges, int[:] arr_cum, int[:] arr_shuff, int c) nogil:
    
    cdef int new_label, n, j, count, i, beginning, end, lenght, cum_index

    cum_index = arr_shuff[c]
    if cum_index == 0:
        beginning = 0
    else:
        beginning = arr_cum[cum_index - 1]
    end = arr_cum[cum_index]
    lenght = end - beginning

    cdef int *arr_to_process = <int *>malloc((lenght) * sizeof(int))
    cdef int *freq = <int *>malloc((lenght) * sizeof(int))
    cdef int node_id = arr_edges[beginning, 0] 

    for i in range(lenght):
        n = arr_edges[beginning + i, 1]
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

    cdef int max_i = 0
    cdef int maxi = freq[0]
    for i in range(lenght):
        if freq[i] > maxi:
            maxi = freq[i]
            max_i = i 
    new_label = arr_to_process[max_i]
    free(arr_to_process)
    free(freq)

    with gil:
        arr_all_labels[node_id] = new_label
        #print('f')


def update_labels(all_labels_v, edges_v, cum_no_neighbors_v):
    
    cdef int l = len(cum_no_neighbors_v) 
    order = np.arange(l, dtype=DTYPE)
    shuffled = np.copy(order)
    np.random.shuffle(shuffled)

    cdef int [:] shuffled_v = shuffled
    cdef int c
    
    for c in prange(l, nogil=True, schedule='dynamic', num_threads=1): 

        label_this_node(all_labels_v, edges_v, cum_no_neighbors_v, shuffled_v, c)


def corri(G, n, draw=False):

    start=datetime.now()

    M = nx.to_scipy_sparse_matrix(G,dtype=DTYPE,format='lil')
    edges = np.asarray(M.nonzero(), dtype=DTYPE).T 
    cdef int nodes = M.shape[0]

    no_neighbors = np.fromiter((scipy.sparse.lil_matrix.count_nonzero(M[i]) for i in range(nodes)), dtype=DTYPE, count=nodes)
    no_neighbors = no_neighbors[no_neighbors != 0]

    cum_no_neighbors = np.cumsum(no_neighbors, dtype=DTYPE)
    M=0

    cdef int i
    all_labels = np.fromiter((i for i in range(1, nodes+1)), dtype=DTYPE, count=nodes)

    cdef int [:] all_labels_v = all_labels
    cdef int [:,:] edges_v = edges
    cdef int [:] cum_no_neighbors_v = cum_no_neighbors

    print('finished preparations, updating labels')
    print(datetime.now()-start)

    for it in range(n):
        print('iter %i' %it)
        update_labels(all_labels_v, edges_v, cum_no_neighbors_v)

    print(datetime.now()-start)

    most_10 = Counter(all_labels).most_common(10)
    print(most_10)

    for node in G:
        if G[node]:
            G.node[node]['label'] = all_labels[node]

    if draw: draw_graph(G, all_labels)


def draw_graph(G, all_labels):
    most_5 = Counter(all_labels).most_common(4)
    red = []
    green = []
    yellow = []
    white = []
    blue = []
    for n, l in enumerate(all_labels):
        if l == most_5[0][0]: blue.append(n)
        elif l == most_5[1][0]: red.append(n)
        elif l == most_5[2][0]: green.append(n)
        elif l == most_5[3][0]: yellow.append(n)
        else: white.append(n)
    pos=nx.spring_layout(G)
    nx.draw(G, pos, with_labels=False, node_size=1, width=1)
    nx.draw_networkx_nodes(G, pos, nodelist=white, node_color='#cbccc1')
    nx.draw_networkx_nodes(G, pos, nodelist=red, node_color='r')
    nx.draw_networkx_nodes(G, pos, nodelist=blue, node_color='b')
    nx.draw_networkx_nodes(G, pos, nodelist=yellow, node_color='#cfe014')
    nx.draw_networkx_nodes(G, pos, nodelist=green, node_color='g')

    plt.show()