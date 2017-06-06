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
                G.add_edges_from([(u, v)], weight=np.random.uniform(1.0, 4.0), status='DELETABLE')
                T_matrix[u, v] = np.random.uniform(0.5, 1.5)

    print T_matrix
    nx.draw_networkx(G, arrows=True, with_labels=True)
    plt.show()

    #todo general LTD constraints

    #todo Obj function

