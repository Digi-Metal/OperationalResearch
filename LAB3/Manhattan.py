import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

class Routing(object, nx.Graph):

    G = nx.DiGraph()
    N = 16
    nodes = range(N)
    np.random.seed(6)

    bb = nx.edge_betweenness_centrality(G, normalized=False)
    nx.set_edge_attributes(G, 'weight', bb)
    nx.set_edge_attributes(G, 'capacity', bb)

    T_matrix = np.zeros((N, N))

    for u in nodes:
        for v in nodes:
            if u != v:
                if (u > 4 and v > 4 and u < 7 and v < 7) or (u > 8 and v > 8 and u < 11 and v < 11) or (u == 5 and v == 9) or (u==9 and v == 5) or (u == 6 and v== 10) or (u==10 and v ==6):
                    flow_high = np.random.uniform(10, 15)
                    T_matrix[u, v] = flow_high
                else:
                    flow_low = np.random.uniform(0.5, 1.5)
                    T_matrix[u, v] = flow_low

    for i in nodes:
        if i == 0:
            G.add_edges_from([(i, i + 3), (i, i + 1), (i, i + 4), (i, i + 12)])

        elif i == 3:
            G.add_edges_from([(i, i - 3), (i, i - 1), (i, i + 4), (i, i + 12)])

        elif i == 15:
            G.add_edges_from([(i, i - 4), (i, i - 1), (i, i - 3), (i, i - 12)])

        elif i == 12:
            G.add_edges_from([(i, i - 4), (i, i + 1), (i, i + 3), (i, i - 12)])

        elif i == 7 or i == 11:
            G.add_edges_from([(i, i + 4), (i, i - 4), (i, i - 1), (i, i - 3)])

        elif i == 4 or i == 8:
            G.add_edges_from([(i, i + 3), (i, i + 1), (i, i + 4), (i, i - 4)])

        elif i > 0 and i < 3:
            G.add_edges_from([(i, i - 1), (i, i + 1), (i, i + 4), (i, i + 12)])

        elif (i > 4 and i < 7) or (i > 8 and i < 11):
            G.add_edges_from([(i, i + 1), (i, i - 1), (i, i + 4), (i, i - 4)])

        elif i > 12 and i < 15:
            G.add_edges_from([(i, i + 1), (i, i - 1), (i, i - 4), (i, i - 12)])

        else:
            break

    nx.draw_networkx(G, arrows=True, with_labels=True)
    plt.show()

    for s in range(N):
        for d in range(N):
            if G.has_edge(s, d):
                G.edge[s][d]['weight'] = T_matrix[s][d]
                G.edge[s][d]['capacity'] = np.random.randint(8, 12)

    f_value = 0
    (p, a) = (0, 0)
    for i in range(N):
        for j in range(N):
            if len(nx.shortest_path(G, i, j)) > 2:
                edges = nx.shortest_path(G, i, j, weight='weight')
                for k in range(len(edges) - 1):
                    G.edge[edges[k]][edges[k + 1]]['weight'] += T_matrix[i][j]
                if i != j:
                    flow_value = nx.maximum_flow_value(G, i, j)
                    if flow_value > f_value:
                        f_value = flow_value
                        (p, a) = (i, j)

    fmax = 0
    (s_f, d_f) = (0, 0)

    for s in G.edge:
        for d in G.edge[s]:
            if G.edge[s][d]['weight'] > fmax:
                fmax = G.edge[s][d]['weight']
                (s_f, d_f) = (s, d)

    tot_edges = G.number_of_edges()

    np.set_printoptions(precision=3,  linewidth=150)
    print T_matrix
    print tot_edges
    print 'max flow value on capacity', flow_value, 'on', (p, a), 'and max flow on weight', fmax, 'on', (s_f, d_f)