import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import fnss
import scipy.optimize




def capacities(G):
    return nx.get_edge_attributes(G, 'capacity')

def weights(G):
    return nx.get_edge_attributes(G, 'weight')



def findMinNotDiagR(matrix,N):
    vector_min = []
    for i in range(N):
        min = np.argmax(matrix[i])
        for j in range(N):
            if i!=j:
                if matrix[i,j]<matrix[i,min]:
                    min = j
        vector_min.append(min)
    return vector_min

def findMinNotDiagC(matrix,N):
    vector_min = []
    for i in range(N):
        min = np.argmax(matrix[i])
        for j in range(N):
            if i!=j:
                if matrix[i,j]<matrix[i,min]:
                    min = j
        vector_min.append(min)

    return vector_min

if __name__ == '__main__':

    G = nx.DiGraph()

    N = 5
    nodes = range(N)
    T_matrix = np.zeros((N, N))
    for u in nodes:
        for v in nodes:
            if u != v:
                flow = np.random.uniform(0.5, 1.5)
                G.add_edges_from([(u, v)], weight=flow, status='DELETABLE')
                T_matrix[u, v] = flow


    print T_matrix
    minimum = findMinNotDiagR(T_matrix,N)
    #x = nx.shortest_path(G,0,minimum[0])

    print G.edges()
    for i in range(N):
        G.remove_edge(i,minimum[i])

    print (G.edge)

    for i in range(N):
        edges = nx.shortest_path(G,i,minimum[i])
        for j in range(1,len(edges)):
            G.edge[i][j]['weight'] += T_matrix[i,minimum[i]]



    nx.draw_networkx(G, arrows=True, with_labels=True)

    plt.show()


