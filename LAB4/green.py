import networkx as nx
import numpy as np
import Queue

color = {}
color['router'] = 'red'
color['access'] = 'blue'
color['central'] = 'green'
color['disabled'] = 'gray'

class GreenNetwork():

    def __init__(self,nodes,percentage_inactive,capacity,accessP,routerP,centralP,linkP,alpha):
        self.nodes = nodes
        self.inactive = percentage_inactive
        self.capacity = capacity
        self.node_power = accessP

        self.power = {}
        self.power['access'] = accessP
        self.power['router'] = routerP
        self.power['link'] = linkP
        self.power['central'] = centralP

        self.alpha = alpha
        self.link_power = linkP
        self.transient = Queue.Queue()
        self.transient_v = []
        self.linked = np.zeros(self.nodes+2)
        self.color_map = ["" for x in range(self.nodes+2)]

        self.right_path = 1
        self.edges = []

        np.random.seed(4)


    def getCapacity(self):
        return self.capacity

    def anyPeer(self,G,node):
        for s,d in G.edges(node):
            if G.node[s]['type'] == G.node[d]['type'] and G.node[d]['enabled'] == True:
                return True
        return False

    def justTheCentral(self,G,n):
        for s,d in G.edges(n):
            if G.node[d]['type'] == 'access':
                return False
        return True

    def getPowerPerType(self,G):
        powerPertType = {}
        powerPertType['router'] = 0
        powerPertType['access'] = 0
        powerPertType['central'] = 0
        powerPertType['link'] = {}
        powerPertType['link']['dr'] = 0
        powerPertType['link']['rr'] = 0
        powerPertType['link']['cc'] = 0
        powerPertType['link']['rc'] = 0

        for n in G.nodes():
            powerPertType[G.node[n]['type']]+=G.node[n]['power']*self.alpha + self.power[G.node[n]['type']]

        for s,d in G.edges():
            if G.node[s]['type'] == 'access' and G.node[d]['type'] == 'router':
                if G.node[d]['enabled'] == True:
                    powerPertType['link']['dr'] += G.edge[s][d]['weight']*self.alpha+self.power['link']
                else:
                    powerPertType['link']['dr'] += self.power['link']
            if G.node[s]['type'] == 'router' and G.node[d]['type'] == 'central':
                if G.node[d]['enabled'] == True and G.node[s]['enabled'] == True:
                    powerPertType['link']['rc'] += G.edge[s][d]['weight']*self.alpha+2*self.power['link']
                else:
                    powerPertType['link']['rc'] += 2*self.power['link']

            if G.node[s]['type'] == 'router' and G.node[d]['type'] == 'router':
                if G.node[d]['enabled'] == True and G.node[s]['enabled'] == True:
                    powerPertType['link']['rr'] += G.edge[s][d]['weight']*self.alpha+2*self.power['link']
                else:
                    powerPertType['link']['rr'] += 2*self.power['link']


            if G.node[s]['type'] == 'central' and G.node[d]['type'] == 'central':
                if G.node[s]['enabled'] == True and G.node[d]['enabled'] == True:
                    powerPertType['link']['cc'] += G.edge[s][d]['weight'] * self.alpha+4*self.power['link']
                else:
                    powerPertType['link']['cc'] += 4*self.power['link']

        return powerPertType

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

        #todo sei qua
        self.transient_v.append(central_node2)
        self.transient_v.append(central_node)
        self.linked[self.nodes] = 1
        self.linked[self.nodes+1] = 1

        for i in range(len(self.transient_v)-2):
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
                G.add_edge(self.transient_v[nextRouter%(len(self.transient_v)-2)],dev,weight=0)
                G.add_edge(self.transient_v[(nextRouter+1) % (len(self.transient_v)-2)], dev,weight=0)
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
        G.node[n]['power'] = 0

        self.color_map[n] = color['disabled']


    def routing(self,G,tsd,N):
        for s in G.nodes():
            for d in G.nodes():
                if G.node[s]['type'] == 'access' and G.node[d]['type']=='access' and not G.has_edge(s,d) and s!=d:
                    try:
                        paths = list(nx.all_simple_paths(G,s,d))
                        paths.sort(lambda x, y: cmp(len(x), len(y)))
                        self.right_path = 1
                        self.edges = []
                        for path in paths:
                            self.right_path = 1
                            for node in path:
                                if not G.node[node]['enabled']:
                                    self.right_path = 0
                            if self.right_path == 1:
                                self.edges = path
                                break
                        if self.right_path == 0:
                            return False
                        for e in range(len(self.edges) - 1):
                            G.edge[self.edges[e]][self.edges[e + 1]]['weight'] += tsd[s][d]
                    except nx.NetworkXNoPath, UnboundLocalError:
                        print 'Error'
                        return False


        return True



    def setNodePower(self,G,n):
        total_flow = 0

        if G.node[n]['enabled'] == False:
            G.node[n]['power'] = 0
            return

        if G.node[n]['type'] == 'router' or G.node[n]['type'] == 'central':
            for s,d in G.edges(n):
                total_flow += G.edge[s][d]['weight']

            total_flow = total_flow*self.alpha
            total_flow += self.power[G.node[n]['type']]
            G.node[n]['power'] = total_flow

        else:

            G.node[n]['power'] = self.alpha*self.power[G.node[n]['type']]
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
            if G.node[node]['enabled'] == True:
                power += G.node[node]['power']

        for s,d in G.edges():
            if G.node[s]['type'] == 'access' and G.node[d]['type'] == 'router':
                if G.node[d]['enabled'] == True:
                    power += G.edge[s][d]['weight']*self.alpha+self.power['link']
                else:
                    power += 0
            if G.node[s]['type'] == 'router' and G.node[d]['type'] == 'central':
                if G.node[d]['enabled'] == True and G.node[s]['enabled'] == True:
                    power += G.edge[s][d]['weight']*self.alpha+2*self.power['link']
                else:
                    power += 0

            if G.node[s]['type'] == 'router' and G.node[d]['type'] == 'router':
                if G.node[d]['enabled'] == True and G.node[s]['enabled'] == True:
                    power += G.edge[s][d]['weight']*self.alpha+2*self.power['link']
                else:
                    power += 0


            if G.node[s]['type'] == 'central' and G.node[d]['type'] == 'central':
                if G.node[s]['enabled'] == True and G.node[d]['enabled'] == True:
                    power += G.edge[s][d]['weight'] * self.alpha+4*self.power['link']
                else:
                    power += 0


        return power


    def getPower2(self,G):
        power = 0
        for node in G.nodes():
            if G.node[node]['enabled'] == True:
                power += G.node[node]['power']

        for s,d in G.edges():
            if G.node[s]['type'] == 'access' and G.node[d]['type'] == 'router':
                if G.node[d]['enabled'] == True:
                    power += G.edge[s][d]['weight']*self.alpha+self.power['link']
                else:
                    power += self.power['link']
            if G.node[s]['type'] == 'router' and G.node[d]['type'] == 'central':
                if G.node[d]['enabled'] == True and G.node[s]['enabled'] == True:
                    power += G.edge[s][d]['weight']*self.alpha+2*self.power['link']
                else:
                    power += 2*self.power['link']

            if G.node[s]['type'] == 'router' and G.node[d]['type'] == 'router':
                if G.node[d]['enabled'] == True and G.node[s]['enabled'] == True:
                    power += G.edge[s][d]['weight']*self.alpha+2*self.power['link']
                else:
                    power += 2*self.power['link']


            if G.node[s]['type'] == 'central' and G.node[d]['type'] == 'central':
                if G.node[s]['enabled'] == True and G.node[d]['enabled'] == True:
                    power += G.edge[s][d]['weight'] * self.alpha+4*self.power['link']
                else:
                    power += 4*self.power['link']


        return power

    def notUtilized(self,G,n):
        if G.node[n]['power'] < self.power[G.node[n]['type']]:
            return True
        return False
