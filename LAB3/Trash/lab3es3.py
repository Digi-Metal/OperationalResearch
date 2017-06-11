import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import time
import calendar
import fnss
import scipy.optimize

N = 40
DELTA = 2


def findMaxCardinality(G):
    max = 0
    max_index = -1
    for i in range(N):
        if len(G.edge[i]) > max:
            max = len(G.edge[i])
            max_index = i

    return max_index


def findMaxInCardinality(G):
    max = 0
    max_index = -1
    for i in range(N):
        if G.in_degree(i) > max:
            max = G.in_degree(i)
            max_index = i

    return max_index


def findMaxEdge(G, Node):
    # print Node,'excluding',excluding
    # print Node,G.edge[Node]
    max = 0
    max_index = -1
    for j in G.edge[Node]:
        if G.edge[Node][j]['weight'] > max:
            max = G.edge[Node][j]['weight']
            max_index = j
    return max_index


def findMinEdgeDest(G, Node, excluding):
    # print Node,'excluding',excluding
    # print Node,G.edge[Node]
    min = 500
    min_index = -1
    for j in range(N):
        if G.has_edge(j, Node):
            if G.edge[j][Node]['weight'] < min and j not in excluding:
                min = G.edge[j][Node]['weight']
                min_index = j
    return min_index


def findMinEdgeForAll(G, N, excluding):
    min_vect = []
    for i in range(N):
        min = 500
        min_index = 0
        for j in G.edge[i]:
            if G.edge[i][j]['weight'] < min and j not in excluding:
                min = G.edge[i][j]['weight']
                min_index = j
        min_vect.append(min_index)

    return min_vect


def vectorMaxFromTraffic(Matrix, N):
    max_vect = []
    for i in range(N):
        for j in range(N):
            max_vect.append(np.argmax(Matrix[j]))
    return max_vect


def findMaxIndexMatrixAndRemove(matrix, N):
    max = np.max(matrix)
    for i in range(N):
        if np.amax(matrix[i]) == max:
            index = np.argmax(matrix[i])
            matrix[i][index] = 0
            break
    for j in range(N):
        return (i, index)


def findMaxIndexMatrixOnlyMatch(matrix, N, s_u, d_u):
    max = 0
    indexes = (0, 0)
    for s in range(N):
        for d in range(N):
            if s_u[s] == 1 and d_u[d] == 1:
                if matrix[s][d] > max:
                    max = matrix[s][d]
                    indexes = (s, d)
    matrix[indexes[0]][indexes[1]] = -1
    return indexes


if __name__ == '__main__':

    mean_vector_f = []
    for x in range(5):

        # costruisco anello
        delta_in = np.ones(N) * DELTA
        delta_out = np.ones(N) * DELTA

        matchable_s = np.ones(N)
        matchable_d = np.ones(N)

        G = nx.DiGraph()

        T_matrix = np.zeros((N, N))
        weight = np.inf * np.ones((N, N))

        for u in range(N):
            for v in range(N):
                if u != v:
                    p = np.random.uniform(0,1)
                    if p<=0.1:
                        flow = np.random.uniform(5.0,15.0)
                    else:
                        flow = np.random.uniform(0.5, 1.5)
                    T_matrix[u, v] = flow

        tsd_tmp = T_matrix.copy()
        flagNodes = np.zeros(N)
        flowNodes = []

        indexes = findMaxIndexMatrixAndRemove(tsd_tmp, N)
        G.add_edges_from([indexes], weight=tsd_tmp[indexes[0]][indexes[1]])
        weight[indexes[0]][indexes[1]] = T_matrix[indexes[0]][indexes[1]]
        flagNodes[indexes[0]] = 1
        flagNodes[indexes[1]] = 1
        flowNodes.append(indexes[0])
        flowNodes.append(indexes[1])
        s = indexes[1]
        for i in range(N - 1):
            for j in range(N):
                flagNodes[s] = 1
                d = np.argmax(tsd_tmp[s])  # this is the next node index

                if flagNodes[d] == 0:
                    G.add_edges_from([(s, d)], weight=tsd_tmp[s][d])
                    weight[s][d] = T_matrix[s][d]
                    flowNodes.append(d)
                    tsd_tmp[s, d] = 0
                    flagNodes[d] = 1
                    s = d
                    break
                else:
                    tsd_tmp[s, d] = 0

        G.add_edges_from([(s, indexes[0])], weight=tsd_tmp[s][indexes[0]])
        weight[s, indexes[0]] = T_matrix[s, indexes[0]]
        tsd_tmp[s, indexes[0]] = 0

        print flowNodes

        # nx.draw_networkx(G, arrows=True, with_labels=True)

        print nx.shortest_path(G)

        shortest_path = nx.shortest_path(G)

        # the weight of a logical link is given by nhop*tsd
        for i in range(N):
            for j in range(N):
                weight[i][j] = (len(shortest_path[i][j]) - 1) * T_matrix[i][j]

        # add for each arc on the path the tsd
        for i in range(N):
            for j in range(N):
                if len(nx.shortest_path(G, i, j)) > 2:
                    edges = nx.shortest_path(G, i, j)
                    for k in range(1, len(edges) - 1):
                        G.edge[edges[k - 1]][edges[k]]['weight'] += T_matrix[i][j]
        attempt = 0
        weight_tmp = weight.copy()
        enter = calendar.timegm(time.gmtime())
        while (sum(list(G.in_degree(range(N)).values())) < N * DELTA or sum(list(G.out_degree(range(N)).values())) < N * DELTA) and (calendar.timegm(time.gmtime())-enter)<30:

            (s, d) = findMaxIndexMatrixOnlyMatch(weight_tmp, N, matchable_s, matchable_d)

            if G.in_degree(d) < DELTA and G.out_degree(s) < DELTA:
                if not G.has_edge(s, d):
                    edges = nx.shortest_path(G, s, d)
                    for k in range(1, len(edges) - 1):
                        G.edge[edges[k - 1]][edges[k]]['weight'] -= T_matrix[s][d]
                    G.add_edges_from([(s, d)], weight=T_matrix[s][d])
                    weight[s][d] = T_matrix[s][d]
            else:
                if G.out_degree(s)<DELTA and sum(matchable_d)<2:
                    if matchable_d[s]==1:
                        break
                    if G.in_degree(np.argmax(matchable_d)) >= DELTA:
                        break


                if G.in_degree(d) >= DELTA:
                    matchable_d[d] = 0
                if G.out_degree(s) >= DELTA:
                    matchable_s[s] = 0

                if calendar.timegm(time.gmtime())-enter > 30:
                    break

        print enter, calendar.timegm(time.gmtime()),calendar.timegm(time.gmtime()) -enter
        #print matchable_d
        #print matchable_s
        #   nx.draw_networkx(G,with_labels=True)

        fmax = 0
        (s_f, d_f) = (0, 0)

        for s in G.edge:
            for d in G.edge[s]:
                if G.edge[s][d]['weight'] > fmax:
                    fmax = G.edge[s][d]['weight']
                    (s_f, d_f) = (s, d)

        mean_vector_f.append(fmax)
        # print fmax
        # print (s_f,d_f)
        # print len(G.edges())
        #
        # for e in G.nodes():
        #     print e,G.in_degree(e),G.out_degree(e)
        print 'Fine', x


        # plt.show()

    print np.mean(mean_vector_f)
    plt.stem(mean_vector_f)
    plt.show()
