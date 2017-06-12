import numpy as np
import networkx as nx
from matplotlib import pyplot as plt

class Topology():
    def __init__(self):
        np.random.seed(5)

    def createRing(self,T_matrix,N):
        flow_nodes = []
        used = np.zeros(N)
        (s,d)= self.findMaxMatrix(T_matrix,N)
        G = nx.DiGraph()
        G.add_edges_from([(s,d)],weight=T_matrix[s,d])
        first = s
        flow_nodes.append(s)
        used[s] = 1
        used[d] = 1
        T_matrix[s][d] = -1
        T_matrix[d][s] = -1
        for i in range(N-2):
            s = d
            flow_nodes.append(s)
            max = 0
            for j in range(N):
                if used[j] == 0 and T_matrix[s][j]>max:
                    max = T_matrix[i][j]
                    d = j
            G.add_edges_from([(s,d)],weight = T_matrix[s][d])
            T_matrix[s][d] = -1
            T_matrix[d][s] = -1
            used[s] = 1
            used[d] = 1
        flow_nodes.append(d)
        G.add_edges_from([(d,first)],weight=T_matrix[d][first])
        return G,flow_nodes

    def createManhattanTopology(self,N):

        G = nx.Graph()

        for i in range(N):
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
        return G

    def createManhattanFullDuplex(self,N):

        G = nx.DiGraph()

        for node in range(N):
            if node == 0:
                nextNodes = [1, 3, 4, 12]
                for element in nextNodes:
                    G.add_edge(node, element)
            elif node == 1:
                nextNodes = [0, 2, 5, 13]
                for element in nextNodes:
                    G.add_edge(node, element)
            elif node == 2:
                nextNodes = [1, 3, 6, 14]
                for element in nextNodes:
                    G.add_edge(node, element)
            elif node == 3:
                nextNodes = [0, 2, 7, 15]
                for element in nextNodes:
                    G.add_edge(node, element)
            elif node == 4:
                nextNodes = [0, 5, 7, 8]
                for element in nextNodes:
                    G.add_edge(node, element)
            elif node == 5:
                nextNodes = [1, 4, 6, 9]
                for element in nextNodes:
                    G.add_edge(node, element)
            elif node == 6:
                nextNodes = [2, 5, 7, 10]
                for element in nextNodes:
                    G.add_edge(node, element)
            elif node == 7:
                nextNodes = [3, 4, 6, 11]
                for element in nextNodes:
                    G.add_edge(node, element)
            elif node == 8:
                nextNodes = [4, 9, 11, 12]
                for element in nextNodes:
                    G.add_edge(node, element)
            elif node == 9:
                nextNodes = [5, 8, 10, 13]
                for element in nextNodes:
                    G.add_edge(node, element)
            elif node == 10:
                nextNodes = [6, 9, 11, 14]
                for element in nextNodes:
                    G.add_edge(node, element)
            elif node == 11:
                nextNodes = [7, 8, 10, 15]
                for element in nextNodes:
                    G.add_edge(node, element)
            elif node == 12:
                nextNodes = [0, 8, 13, 15]
                for element in nextNodes:
                    G.add_edge(node, element)
            elif node == 13:
                nextNodes = [1, 9, 12, 14]
                for element in nextNodes:
                    G.add_edge(node, element)
            elif node == 14:
                nextNodes = [2, 10, 13, 15]
                for element in nextNodes:
                    G.add_edge(node, element)
            elif node == 15:
                nextNodes = [3, 11, 12, 14]
                for element in nextNodes:
                    G.add_edge(node, element)
        return G

    def createTrafficMatrix(self,min,max,N):
        T_matrix = np.zeros((N,N))
        for u in range(N):
            for v in range(N):
                if u != v:
                    flow = np.random.uniform(min, max)
                    T_matrix[u, v] = flow
        return T_matrix

    def routing(self,G,tsd,paths,N):
        for s in range(N):
            paths[s] = {}
            for d in range(N):
                if not G.has_edge(s,d) and s!=d:
                    edges = nx.shortest_path(G,s,d)
                    paths[s][d] = edges
                    for e in range(len(edges)-1):
                        G.edge[edges[e]][edges[e+1]]['weight'] += tsd[s][d]

                elif G.has_edge(s,d) and s!=d:
                    paths[s][d] = [s,d]

    def routingManahttan(self,G,tsd,N):
        for s in range(N):
            for d in range(N):
                if not G.has_edge(s,d) and s!=d:
                    edges = nx.shortest_path(G,s,d,weight='weight')
                    for e in range(len(edges)-1):
                        G.edge[edges[e]][edges[e+1]]['weight'] += tsd[G.node[s]['node']][G.node[d]['node']]

    def cleanTheGraphForRouting(self,G,tsd):
        for (s,d) in G.edges():
            G.edge[s][d]['weight'] = tsd[s][d]

    def printEdgesAndWeight(self,G):
        for (s,d) in G.edges():
            print s,d,G.get_edge_data(s,d)

    def addEdgeAndRemoveFromOthers(self,G,s,d,paths,tsd):
        edges = paths[s][d]
        for e in range(len(edges) - 1):
            G.edge[edges[e]][edges[e + 1]]['weight'] -= tsd[s][d]
        G.add_edges_from([(s,d)],weight=tsd[s][d])

    def fmax(self,G):
        fmax = 0
        (s_f,d_f) = (0,0)

        for s in G.edge:
            for d in G.edge[s]:
                if G.edge[s][d]['weight'] > fmax:
                    fmax = G.edge[s][d]['weight']
                    (s_f,d_f) = (s,d)
        return fmax,s_f,d_f

    def findMaxMatrix(self,T_matrix,N):
        max = 0
        (s,d) = (0,0)
        for i in range(N):
            for j in range(N):
                if T_matrix[i][j]>max:
                    (s,d) = (i,j)
                    max = T_matrix[i][j]

        return (s,d)

    def findMaxAndRemove(self,matrix,N):
        max = 0
        (s,d) = (0,0)
        for i in range(N):
            for j in range(N):
                if matrix[i][j]>max:
                    (s,d) = (i,j)
                    max = matrix[i][j]

        matrix[s][d] = 0
        return (s,d)

    def findMaxForRowAndRemove(self,matrix,row):
        argmax = np.argmax(matrix[row])
        max = matrix[row][argmax]
        matrix[row][argmax] = 0
        return argmax,max

    def swapNodes(self,G,n1,n2):
        x = G.node[n1]['node']
        G.node[n1]['node'] = G.node[n2]['node']
        G.node[n2]['node'] = x

    def cleanAndReRouteManh(self,G,tsd,N):

        #'cleaning' the graph
        for s,d in G.edges():
            G.edge[s][d]['weight'] = 0

        for s in range(N):
            for d in range(N):
                if s!=d:
                    if G.has_edge(s,d):# and s!=d:
                        G.edge[s][d]['weight'] = tsd[G.node[s]['node']][G.node[d]['node']]

                    else:
                    #if not G.has_edge(s,d):# and s!=d:
                        edges = nx.shortest_path(G,s,d,weight='weight')
                        for e in range(len(edges)-1):
                            #G.edge[edges[e]][edges[e+1]]['weight'] += tsd[s][d]
                            G.edge[edges[e]][edges[e+1]]['weight'] += tsd[G.node[s]['node']][G.node[d]['node']]

    def printManahttan(self,G):
        for j in range(4):
            print G.node[4 * j + 0]['node'], G.node[4 * j + 1]['node'], G.node[4 * j + 2]['node'], G.node[4 * j + 3]['node']


    def simulatedAnnealing(self,tsd,G,N):
        G_first = G.copy()
        # Simultaed annealing
        n1 = np.random.randint(0, N - 1)
        n2 = np.random.randint(0, N - 1)
        while n1 == n2:
            n2 = np.random.randint(0, N-1)

        self.swapNodes(G_first, n1, n2)
        #self.printManahttan(G_first)
        self.cleanAndReRouteManh(G_first, tsd, N)

        return self.fmax(G_first)[0],G_first
