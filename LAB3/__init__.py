import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

class Topology(object, nx.Graph):

    G = nx.DiGraph()

    N = 5
    nodes = range(N)
    T_matrix = np.zeros((N, N))
    flow_value = np.zeros((N, N))
    for u in nodes:
        for v in nodes:
            if u != v:
                flow = np.random.uniform(0.5, 1.5)
                G.add_edges_from([(u, v)], weight=flow , capacity=np.random.randint(8, 12))
                T_matrix[u, v] = flow

    delta_in = list(G.in_degree(range(N)).values())
    delta_out = list(G.out_degree(range(N)).values())

    mincostFlow = nx.max_flow_min_cost(G, 0, N - 1)
    mincost = nx.cost_of_flow(G, mincostFlow)
    count = mincostFlow.values()

    minimum = list(np.where(T_matrix > 0, T_matrix, T_matrix.max()).min(1))
    index = list(np.where(T_matrix > 0, T_matrix, T_matrix.max()).argmin(axis=1))


    for n, nbrs in G.adjacency_iter():
        for nbr, eattr in nbrs.items():
            data = eattr['weight']
            cap = eattr['capacity']
            print('(%d, %d, %.3f, %.2f)' % (n, nbr, data, cap))


    np.set_printoptions(precision=3)
    print T_matrix

    print delta_in
    print delta_out
    print minimum
    print index

    print count


    nx.draw_networkx(G, arrows=True, with_labels=True)
    plt.show()

    #todo general LTD constraints

    #todo Obj function

