import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from topology import Topology


if __name__ == '__main__':

    N = 16
    nodes = range(N)
    np.random.seed(5)
    t = Topology()


    T_matrix = t.createTrafficMatrix(0.5,1.5,N)
    G = t.createManhattanFullDuplex(N)



    remaining_node = 4*np.ones(N)
    rem = 4*np.ones(N)
    taken = 4*np.zeros(N)
    tk = 4*np.zeros(N)
    tsd_copy = T_matrix.copy()

    for n in nodes:

        if n == 0:
            i,j = t.findMaxAndRemove(tsd_copy,N)
            G.node[0]['node'] = i
            G.node[1]['node'] = j
            G.edge[0][1]['weight'] = T_matrix[i][j]
            G.edge[1][0]['weight'] = T_matrix[j][i]
            remaining_node[i]-=1
            remaining_node[j] -=1
            taken[i] = 1
            taken[j] = 1

            #todo elimina
            tk[0] = 1
            rem[0] -= 1
            rem[1] -= 1
            tk[1] = 1
            #todo finqua
            for s,d in G.edges(0):
                if (s,d) != (0,1):
                    argmax,max = t.findMaxForRowAndRemove(tsd_copy,i)
                    G.node[d]['node'] = argmax
                    G.edge[s][d]['weight'] = T_matrix[i][argmax]
                    G.edge[d][s]['weight'] = T_matrix[argmax][i]
                    remaining_node[i] -= 1
                    remaining_node[argmax] -= 1
                    taken[argmax] = 1
                    tk[d] = 1
                    rem[s] -= 1
                    rem[d] -= 1
        else:
            for s, d in G.edges(n):

                if len(G.edge[s][d])== 0 and rem[s]>0:

                        avail = rem[s]

                        while avail == rem[s]:

                            if tk[d] == 1 and tk[s]== 1 and len(G.edge[s][d]) == 0:
                                G.edge[s][d]['weight'] = T_matrix[G.node[s]['node']][G.node[d]['node']]
                                G.edge[d][s]['weight'] = T_matrix[G.node[d]['node']][G.node[s]['node']]
                                rem[s] -= 1
                                rem[d] -= 1
                                break

                            argmax,max = t.findMaxForRowAndRemove(tsd_copy,G.node[n]['node'])
                            #if remaining_node[argmax] > 0 and taken[argmax]== 0:
                            if (rem[d] > 0 and tk[d] == 0 and taken[argmax] == 0):
                                G.node[d]['node'] = argmax
                                G.edge[s][d]['weight'] = T_matrix[G.node[n]['node']][argmax]
                                G.edge[d][s]['weight'] = T_matrix[argmax][G.node[n]['node']]
                                remaining_node[G.node[n]['node']] -= 1
                                remaining_node[argmax] -= 1
                                taken[argmax] = 1
                                rem[s] -= 1
                                rem[d] -= 1
                                tk[d] = 1

    for j in range(4):
        print G.node[4*j+0]['node'], G.node[4*j+1]['node'], G.node[4*j+2]['node'], G.node[4*j+3]['node']


    t.routingManahttan(G,T_matrix,N)

    f_max =  t.fmax(G)

    print f_max


    nx.draw_networkx(G, arrows=True, with_labels=True)

    plt.title('fmax = ' + str(f_max[0]))
    plt.show()
