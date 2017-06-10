import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import fnss
import scipy.optimize

N = 5
DELTA = 1

def capacities(G):
    return nx.get_edge_attributes(G, 'capacity')

def weights(G):
    return nx.get_edge_attributes(G, 'weight')


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





def findMinEdge(G,Node,excluding):
    #print Node,'excluding',excluding
    #print Node,G.edge[Node]
    min = 500
    min_index = -1
    for j in G.edge[Node]:
        if G.edge[Node][j]['weight'] < min and j not in excluding:
            min = G.edge[Node][j]['weight']
            min_index = j
    return min_index


def findMinEdgeDest(G,Node,excluding):
    #print Node,'excluding',excluding
    #print Node,G.edge[Node]
    min = 500
    min_index = -1
    for j in range(N):
        if G.has_edge(j,Node):
            if G.edge[j][Node]['weight'] < min and j not in excluding:
                min = G.edge[j][Node]['weight']
                min_index = j
    return min_index

def findMinEdgeForAll(G,N,excluding):
    min_vect = []
    for i in range(N):
        min = 500
        min_index = 0
        for j in G.edge[i]:
            if G.edge[i][j]['weight']<min and j not in excluding:
                min = G.edge[i][j]['weight']
                min_index = j
        min_vect.append(min_index)

    return min_vect


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
    print findMaxCardinality(G)
    #x = nx.shortest_path(G,0,minimum[0])


#RIMUOVO ARCHI
    #COME STOPPING CONDITION VADO A CONTROLLARE IL DELTA IN E OUT
    #PER CONTROLLARE FACCIO SOMMA DEI DIVERSI DELTA E CONTROLLO CHE SIA N*DELTA
    excluding = []
    while sum(list(G.in_degree(range(N)).values())) > N*DELTA or sum(list(G.out_degree(range(N)).values())) > N*DELTA:
        print sum(list(G.in_degree(range(N)).values()))
        print sum(list(G.out_degree(range(N)).values()))
        finded = False
        while not finded:
            counter = 0
            while counter < 10:
                i = findMaxCardinality(G)
                minimum = findMinEdge(G, i, excluding)
                #vado ad estarre ogni volta il nodo con la massima cardinalita in uscita
                #in questo modo bilancio la rimozione per non trovarmi nella situazione di non saper
                #piu cosa cancellare per non disconnettere la matrice
                #for i in range(N):
                if minimum >= 0 and G.out_degree(i)>DELTA and G.get_edge_data(i,minimum)['status'] == 'DELETABLE':
                    if G.in_degree(minimum) > DELTA:
                        toDelete[(i,minimum)] = {'weight': G.get_edge_data(i,minimum)['weight']}
                        G.remove_edge(i,minimum)
                        try:
                            if len(nx.shortest_path(G, i, minimum)) == 0:
                                G.add_edge(i, minimum, weight=toDelete[(i, minimum)]['weight'], status='UNDELETABLE')
                            else:
                                edges = nx.shortest_path(G, i, minimum)
                                for j in range(1, len(edges)):
                                    G.edge[edges[j - 1]][edges[j]]['weight'] += toDelete[(i, minimum)]['weight']
                                del toDelete[(i, minimum)]
                        except nx.NetworkXNoPath:
                            print ('Aggiunto in quanto disconnettevo')
                            G.add_edge(i, minimum, weight=toDelete[(i, minimum)]['weight'], status='UNDELETABLE')
                        finded = True
                        counter = 11
                    #il nodo con il minimo flusso ha gia raggiunto il minimo numero di archi in entrata
                    #quindi vado a scegliere un altro nodo da cui togliere un arco
                    else:
                        excluding.append(minimum)
                        G.edge[i][minimum]['status'] = 'UNDELETABLE'
                        counter += 1
            #stessa cosa ma al contrario
            counter = 0
            while counter < 10:
                excluding = []
                i = findMaxInCardinality(G)
                minimum = findMinEdgeDest(G, i, excluding)
                if minimum >= 0 and G.in_degree(i) > DELTA and G.get_edge_data(minimum,i)[
                    'status'] == 'DELETABLE':
                    if G.out_degree(minimum) > DELTA:
                        toDelete[(minimum,i)] = {'weight': G.get_edge_data(minimum,i)['weight']}
                        G.remove_edge(minimum,i)
                        try:
                            if len(nx.shortest_path(G,minimum,i)) == 0:
                                G.add_edge(minimum,i, weight=toDelete[(minimum,i)]['weight'],
                                           status='UNDELETABLE')
                            else:
                                edges = nx.shortest_path(G,minimum,i)
                                for j in range(1, len(edges)):
                                    G.edge[edges[j - 1]][edges[j]]['weight'] += toDelete[(minimum,i)][
                                        'weight']
                                del toDelete[(minimum,i)]
                        except nx.NetworkXNoPath:
                            print ('Aggiunto in quanto disconnettevo')
                            G.add_edge(minimum,i, weight=toDelete[(minimum,i)]['weight'],
                                       status='UNDELETABLE')
                        finded = True
                        counter = 11
                    # il nodo con il minimo flusso ha gia raggiunto il minimo numero di archi in entrata
                    # quindi vado a scegliere un altro nodo da cui togliere un arco
                    else:
                        excluding.append(minimum)
                        G.edge[minimum][i]['status'] = 'UNDELETABLE'
                        counter += 1
#if counter > 10 and finded is False:

        print G.edges()
    nx.draw_networkx(G, arrows=True, with_labels=True)


    plt.show()
