import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
import Queue

class GreenNetwork():

    def __init__(self,nodes,percentage_inactive,capacity,node_power,link_power,alpha):
        self.nodes = nodes
        self.inactive = percentage_inactive
        self.capacity = capacity
        self.node_power = node_power
        self.alpha = alpha
        self.link_power = link_power
        self.transient = Queue.Queue()
        self.transient_v = []
        self.linked = np.zeros(self.nodes)
        self.color_map = ["" for x in range(self.nodes)]
        np.random.seed(8)


    def getCapacity(self):
        return self.capacity

    def createTrafficMatrix(self,min,max,N):
        T_matrix = np.zeros((N,N))
        number_inactive = N*self.inactive
        for u in range(N):
            p = np.random.uniform(0, 1)

            if p<self.inactive:
                self.transient.put(u)
                self.transient_v.append(u)
                self.setInactive(u,T_matrix,N)
                number_inactive -= 1
            else:
                if number_inactive!=0 and (N-u) == number_inactive:
                    self.setInactive(u,T_matrix,N)

                else:
                    for v in range(N):
                            if u != v:
                                flow = np.random.uniform(min, max)
                                T_matrix[u, v] = flow

        return T_matrix


    def setInactive(self,node,matrix,N):
        for i in range(N):
            matrix[node][i] = 0
            matrix[i][node] = 0

    def createTopology(self,tsd):

        G = nx.Graph()

        for router in self.transient_v:
            G.add_node(router)
            self.color_map[router] = 'blue'
            self.linked[router] = 1

        while sum(self.linked) != self.nodes:
            for router in self.transient_v:
                dev = np.random.randint(1,self.nodes)
                if self.linked[dev] == 0:
                    G.add_node(dev)
                    self.color_map[dev] = 'red'
        return G





    def createRandomTopology(self,N,tsd):
        delta = np.random.randint(4,N/2)
        print delta
        degree = [delta for i in xrange(N)]
        G = nx.directed_havel_hakimi_graph(degree,degree)

        for s,d in G.edges():
            G.edge[s][d]['weight'] = tsd[s][d]


        #nx.draw_networkx(G)
        #plt.show()
        return G

    def cleanTheGraphForRouting(self,G,tsd):
        for (s,d) in G.edges():
            G.edge[s][d]['weight'] = tsd[s][d]

    def getTransient(self):
        return self.transient

    def routing(self,G,tsd,N):
        for s in G.node:
            for d in G.node:
                if not G.has_edge(s,d) and s!=d:
                    try:
                        edges = nx.shortest_path(G,s,d)
                    except nx.NetworkXNoPath:
                        return False

                    for e in range(len(edges)-1):
                        G.edge[edges[e]][edges[e+1]]['weight'] += tsd[s][d]
                    return True



    def setNodePower(self,G,n):
        total_flow = 0

        for s,d in G.edges(n):
            total_flow += G.edge[s][d]['weight']

        total_flow += self.alpha*self.node_power
        G.node[n]['power'] = total_flow

        return total_flow

    def getNodeMinimumPower(self,G):
        min = np.inf
        argmin = -1
        for n in G.node:
            if G.node[n]['power']<min:
                argmin = n
                min = G.node[n]['power']

        return argmin,min

    def getPower(self,G):
        power = 0
        for node in G.node:
            power += G.node[node]['power']
        return power
