import numpy as np
import networkx as nx
from matplotlib import pyplot as plt

N = 20

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

    def createTrafficMatrix(self,min,max,N):
        T_matrix = np.zeros((N,N))
        for u in range(N):
            for v in range(N):
                if u != v:
                    p = np.random.uniform(0,1)
                    if p<=0.1:
                        flow = np.random.uniform(min*10,max*10)
                    else:
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
        return fmax






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

