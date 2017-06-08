import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

class Topology(object, nx.Graph):

    N = 5
    delta = 3
    nodes = range(N)
    np.random.seed(5)
    G = nx.Graph()

    edges = G.edges_iter()
    for u, v in list(edges):
        if G.has_edge(u, v) & G.has_edge(v, u):
            G.remove_edge(u, v)

    T_matrix = np.zeros((N, N))
    tot_edges = N
    edge_list = []

    for s in nodes:
        tot_edges -= 1
        if tot_edges > 0:
            flow = np.random.uniform(0.5, 1.5)
            G.add_edges_from([(s, s+1)], weight=flow)
            T_matrix[s, s+1] = flow
            edge_list.append([(s, s+1)])
        else:
            break

    np.set_printoptions(precision=3)
    print T_matrix
    print edge_list

    nx.draw_networkx(G, arrows=True, with_labels=True)
    plt.show()