import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
import Queue

color = {}
color['router'] = 'red'
color['access'] = 'blue'
color['central'] = 'green'
color['disabled'] = 'black'

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
        self.color_map = ["" for x in range(self.nodes+2)]
        np.random.seed(8)


    def getCapacity(self):
        return self.capacity

    def anyPeer(self,G,node):
        for s,d in G.edges(node):
            if G.node[s]['type'] == G.node[d]['type']:
                return True
        return False

    def getColorMap(self):
        return self.color_map

    def createTrafficMatrix(self,min,max,N):
        T_matrix = np.zeros((N,N))
        number_inactive = N*self.inactive
        for u in range(N):
            p = np.random.uniform(0, 1)

            if p<=self.inactive:
                self.transient.put(u)
                self.transient_v.append(u)
                self.setInactive(u,T_matrix,N)
                number_inactive -= 1
            else:
                if number_inactive!=0 and (N-u) == number_inactive:
                    self.setInactive(u,T_matrix,N)
                    self.transient_v.append(u)
                    number_inactive-=1

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

    def createTopology(self,N):

        G = nx.Graph()

        central_node = self.nodes
        central_node2 = self.nodes + + 1
        G.add_edge(central_node,central_node2,weight=0)
        G.add_node(central_node,type = 'central',enabled = True)
        G.add_node(central_node2,type = 'central',enabled = True)
        self.color_map[central_node] = color['central']
        self.color_map[central_node2] = color['central']


        for i in range(len(self.transient_v)):
            G.add_node(self.transient_v[i],type = 'router',enabled = True)
            self.color_map[self.transient_v[i]] = color['router']
            self.linked[self.transient_v[i]] = 1

            if (i%2==0):
                G.add_edge(self.transient_v[i],self.transient_v[i+1],weight=0)


            G.add_edge(central_node,self.transient_v[i],weight=0)
            G.add_edge(central_node2,self.transient_v[i],weight=0)

        nextRouter = 0

        for dev in range(self.nodes):
            if self.linked[dev] == 0:
                G.add_node(dev,type='access',enabled = True)
                self.color_map[dev] = color['access']
                G.add_edge(self.transient_v[nextRouter%len(self.transient_v)],dev,weight=0)
                G.add_edge(self.transient_v[(nextRouter+1) % len(self.transient_v)], dev,weight=0)
                nextRouter += 1
                self.linked[dev] = 1

        return G





    def createRandomTopology(self,N,tsd):
        delta = np.random.randint(4,N/2)
        degree = [delta for i in xrange(N)]
        G = nx.directed_havel_hakimi_graph(degree,degree)

        for s,d in G.edges():
            G.edge[s][d]['weight'] = tsd[s][d]


        #nx.draw_networkx(G)
        #plt.show()
        return G

    def cleanTheGraphForRouting(self,G,tsd):
        for (s,d) in G.edges():
            if G.node[s]['type'] == 'access' and G.node[d]['type']=='access':
                G.edge[s][d]['weight'] = tsd[s][d]
            if G.node[s]['type'] == 'central' or G.node[s]['type'] == 'router' or G.node[d]['type'] == 'central' or G.node[d]['type'] == 'router':
                G.edge[s][d]['weight'] = 0

    def getTransient(self):
        return self.transient_v


    def disable_node(self,G,n):
        G.node[n]['enabled'] = False
        self.color_map[n] = color['disabled']


    def routing(self,G,tsd,N):
        for s in G.nodes():
            for d in G.nodes():
                if G.node[s]['type'] == 'access' and G.node[d]['type']=='access' and not G.has_edge(s,d) and s!=d:
                    try:
                        paths = list(nx.all_simple_paths(G,s,d))
                        paths.sort(lambda x, y: cmp(len(x), len(y)))
                        #print(paths[1:10])
                        for path in paths:
                            right_path = True
                            for node in path:
                                if not G.node[node]['enabled']:
                                    right_path = False
                            if right_path == True:
                                edges = path
                                break
                        if right_path == False:
                            return right_path

                    except nx.NetworkXNoPath:
                        return False

                    for e in range(len(edges)-1):
                        G.edge[edges[e]][edges[e+1]]['weight'] += tsd[s][d]
        return True



    def setNodePower(self,G,n):
        total_flow = 0
        if G.node[n]['type'] == 'router':
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
        for node in G.nodes():
            if G.node[node]['type'] == 'router':
                power += G.node[node]['power']

        for s,d in G.edges():
            power += G.edge[s][d]['weight']*self.alpha+self.link_power
        return power

    def getPower2(self,G):
        power = 0
        for node in G.nodes():
            if G.node[node]['type'] == 'router' and G.node[node]['enabled'] == True:
                power += G.node[node]['power']

        for s,d in G.edges():
            if G.node[s]['enabled'] == True and G.node[d]['enabled'] == True:
                power += G.edge[s][d]['weight']*self.alpha+self.link_power
        return power