import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

class Topology(object, nx.Graph):

    N = 5
    delta = 3
    nodes = range(N)
    np.random.seed(5)
    G = nx.DiGraph()

    edges = G.edges_iter()
    for u, v in list(edges):
        if G.has_edge(u, v) & G.has_edge(v, u):
            G.remove_edge(u, v)

    T_matrix = np.zeros((N, N))
    tot_edges = N
    edge_list = []
    tot_flow = 0

    for s in nodes:
        tot_edges -= 1
        if tot_edges > 0:
            flow = np.random.uniform(0.5, 1.5)
            G.add_edges_from([(s, s+1)], weight=flow, capacity=np.random.randint(8, 12))
            T_matrix[s, s+1] = flow
            edge_list.append([(s, s+1)])
            tot_flow += flow
        else:
            G.add_edges_from([(s, 0)], weight=flow, capacity=np.random.randint(8, 12))
            break

    flow_value = nx.maximum_flow_value(G, 0, N-1)

    np.set_printoptions(precision=3)
    print T_matrix
    print edge_list
    print 'max flow value', flow_value, 'and total flow', tot_flow

    nx.draw_networkx(G, arrows=True, with_labels=True)
    plt.show()