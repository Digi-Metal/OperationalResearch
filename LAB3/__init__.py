import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

class BaseTopology(object):

    def capacities(self):
        return nx.get_edge_attributes(self, 'capacity')

    def weights(self):
        return nx.get_edge_attributes(self, 'weight')

class Topology(object, nx.Graph, BaseTopology):
    def __init__(self, data=None, name="", **kwargs):
        super(Topology, self).__init__(data=data, name=name, **kwargs)

    G = nx.DiGraph()

    N = 5
    nodes = range(N)
    T_matrix = np.zeros((N, N))
    for u in nodes:
        for v in nodes:
            if u != v:
                flow = np.random.uniform(0.5, 1.5)
                G.add_edges_from([(u, v)], weight=flow , status='DELETABLE')
                T_matrix[u, v] = flow
                delta_in = list(G.in_degree(range(N)).values())
                delta_out = list(G.out_degree(range(N)).values())

    minimum = list(np.where(T_matrix > 0, T_matrix, T_matrix.max()).min(1))

    for n, nbrs in G.adjacency_iter():
        for nbr, eattr in nbrs.items():
            data = eattr['weight']
            print('(%d, %d, %.3f)' % (n, nbr, data))

    print delta_in
    print delta_out
    print T_matrix
    print minimum

    nx.draw_networkx(G, arrows=True, with_labels=True)
    plt.show()

    #todo general LTD constraints

    #todo Obj function

