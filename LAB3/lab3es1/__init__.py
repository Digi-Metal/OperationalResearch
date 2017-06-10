import networkx as nx
import numpy as np
import calendar
import time
from topology import Topology
from matplotlib import pyplot as plt

N = 20
DELTA = 4

if __name__ == '__main__':
    f_max_vector = []
    for i in range(5):
        t = Topology()
        #creo la matrice
        T_matrix = t.createTrafficMatrix(0.5,1.5,N)

        #creo il ring andando a scegliere gli archi con maggior traffico
        tsd_tmp = T_matrix.copy()
        G,flow_ring = t.createRing(tsd_tmp,N)
        print flow_ring
        #nx.draw_networkx(G)
        #plt.show()
        paths = {}
        t.printEdgesAndWeight(G)
        #routing dell'anello in modo da caricare i diversi flussi
        #provato e funzionante
        t.routing(G,T_matrix,paths)

        t.printEdgesAndWeight(G)
        tsd_tmp = T_matrix.copy()
        enter = calendar.timegm(time.gmtime())
        while (sum(list(G.in_degree(range(N)).values())) < N * DELTA or sum(list(G.out_degree(range(N)).values())) < N * DELTA) and calendar.timegm(time.gmtime())-enter<10:
            (s,d) = t.findMaxAndRemove(tsd_tmp,N)
            if not G.has_edge(s,d):
                if G.in_degree(d) < DELTA and G.out_degree(s)<DELTA:
                    # print s,d,T_matrix[s][d]
                    # print paths[s][d]
                    t.addEdgeAndRemoveFromOthers(G,s,d,paths,T_matrix)
                    t.printEdgesAndWeight(G)
                    # print '-/-/-/-/-/-/-/-/'
                    t.cleanTheGraphForRouting(G,T_matrix)
                    # t.printEdgesAndWeight(G)
                    # print '-0-0-0-0-0-0-0'
                    t.routing(G,T_matrix,paths)
                    # t.printEdgesAndWeight(G)
                    # print '-*-*-*-*--*-*'

        #nx.draw_networkx(G)
        #plt.show()

        f_max_vector.append(t.fmax(G))

    plt.stem(f_max_vector)
    str = str(N) + ' nodes with delta ' + str(DELTA) + ' AVG: ' + str(np.mean(f_max_vector))
    plt.title(str)
    plt.show()
    print np.mean(f_max_vector)


