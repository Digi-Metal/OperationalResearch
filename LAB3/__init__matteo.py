import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import fnss
import scipy.optimize

N = 5
DELTA = 2

def capacities(G):
    return nx.get_edge_attributes(G, 'capacity')

def weights(G):
    return nx.get_edge_attributes(G, 'weight')


def findMinEdge(G,N):
    min_vect = []
    for i in range(N):
        min = 500
        min_index = 0
        for j in G.edge[i]:
            if G.edge[i][j]['weight']<min:
                min = G.edge[i][j]['weight']
                min_index = j
        min_vect.append(min_index)

    return min_vect



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

    toDelete = {}
    nodes = range(N)
    T_matrix = np.zeros((N, N))
    for u in nodes:
        for v in nodes:
            if u != v:
                flow = np.random.uniform(0.5, 1.5)
                G.add_edges_from([(u, v)], weight=flow, status='DELETABLE')
                T_matrix[u, v] = flow


    print T_matrix
    findMinEdge(G,N)
    #x = nx.shortest_path(G,0,minimum[0])


#RIMUOVO ARCHI
    #COME STOPPING CONDITION VADO A CONTROLLARE IL DELTA IN E OUT
    #PER CONTROLLARE FACCIO SOMMA DEI DIVERSI DELTA E CONTROLLO CHE SIA N*DELTA

    while sum(list(G.degree(range(N)).values())) != 2*N*DELTA:
        minimum = findMinEdge(G, N)
        for i in range(N):
            if G.in_degree(minimum[i]) > DELTA and G.out_degree(i)>DELTA and G.get_edge_data(i,minimum[i])['status'] == 'DELETABLE':
                toDelete[(i,minimum[i])] = {'weight': G.get_edge_data(i,minimum[i])['weight']}
                G.remove_edge(i,minimum[i])
                if len(nx.shortest_path(G,i,minimum[i]))==0:
                    G.add_edge(i,minimum[i],weight=toDelete[(i,minimum[i])]['weight'],status = 'UNDELETABLE')
                else:
                    edges = nx.shortest_path(G, i, minimum[i])
                    for j in range(1, len(edges)):
                        G.edge[edges[j - 1]][edges[j]]['weight'] += toDelete[(i, minimum[i])]['weight']
                    del toDelete[(i, minimum[i])]

        print G.edges()
        nx.draw_networkx(G, arrows=True, with_labels=True)


        plt.show()



 #nx.directed_havel_hakimi_graph(degree,degree)
#nx.gnm_random_graph(N,number_edges)