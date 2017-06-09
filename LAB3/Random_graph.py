import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

class Topology(object, nx.Graph):

    N = 20
    delta = 4
    nodes = range(N)
    np.random.seed(5)
    degree = [delta for i in xrange(N)]
    G = nx.directed_havel_hakimi_graph(degree, degree)
    G = nx.DiGraph(G)

    bb = nx.edge_betweenness_centrality(G, normalized=False)
    nx. set_edge_attributes(G, 'weight', bb)
    nx.set_edge_attributes(G, 'capacity', bb)

    # edges = G.edges_iter()
    # new_edge_list = []

    # for u, v in list(edges):
    #     if G.has_edge(u, v) & G.has_edge(v, u):
    #         G.remove_edge(v, u)
    #         new_edge_list.append([u, v])

    T_matrix = np.zeros((N, N))
    tot_edges = G.number_of_edges()

    for s in nodes:
        for d in nodes:
            if s != d:
                flow = np.random.uniform(0.5, 1.5)
                T_matrix[s, d] = flow
                if G.has_edge(s, d):
                    G.edge[s][d]['weight']=flow
                    G.edge[s][d]['capacity'] = np.random.randint(8, 12)

    edge_list = []

    for i in range(N):
        for j in range(N):
            if len(nx.shortest_path(G, i, j)) > 2:
                edges = nx.shortest_path(G, i, j)
                for k in range(1, len(edges) - 1):
                    G.edge[edges[k - 1]][edges[k]]['weight'] += T_matrix[i][j]
                    paths = nx.shortest_simple_paths(G, source=i, target=j)
                    edge_list.append({i: list(paths)})

    fmax = 0
    (s_f, d_f) = (0, 0)

    for s in G.edge:
        for d in G.edge[s]:
            if G.edge[s][d]['weight'] > fmax:
                fmax = G.edge[s][d]['weight']
                (s_f, d_f) = (s, d)

    flow_value = nx.maximum_flow_value(G, 0, N-1)

    np.set_printoptions(precision=3)
    print T_matrix
    print edge_list
    print 'max flow value', flow_value, 'and total flow', fmax, 'on', (s_f, d_f)
    print edge_list
    # print new_edge_list

    nx.draw_networkx(G, arrows=True, with_labels=True)
    plt.show()