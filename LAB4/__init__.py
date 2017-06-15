from topology import Topology
from green import GreenNetwork
from matplotlib import pyplot as plt
from operator import itemgetter
import scipy
import operator

import networkx as nx
import Queue

#N = 10


color = {}
color['router'] = 'red'
color['access'] = 'blue'
color['central'] = 'green'

if __name__ == '__main__':

    for N in [10]:
        for perc in [0.2]:
            for capacity in [40]:
                print '-----------------'
                print 'Nodes = ',N,' R = ', perc*100, '% C = ',capacity

                gn = GreenNetwork(N,percentage_inactive=perc,capacity=capacity,accessP= 2,linkP=4, routerP=1,centralP=10,alpha=0.5)
                tsd = gn.createTrafficMatrix(0.5,1.5,N)
                G = gn.createTopology(tsd)
                color_map = gn.getColorMap()


                nx.draw_networkx(G,node_color = color_map)
                plt.show(block = False)


                gn.routing(G,tsd,N)

                for n in G.nodes():
                    gn.setNodePower(G,n)

                print 'Initial topology',gn.getPower2(G)

                G_copy = G.copy()
                transient = gn.getTransient()


                transient_dict = {}

                for t in transient:
                    transient_dict[t] = {'power':G.node[t]['power']}
                transient_dict = (sorted(transient_dict.items(), key=itemgetter(1)))

                for i in range(len(transient)):
                    node = transient_dict[i][0]
                    adj = G_copy.edges(node)
                    node_type = G_copy.node[node]['type']
                    if gn.anyPeer(G_copy,node) :#and gn.notUtilized(G_copy,node) == True :
                        #print 'Trying to remove', node
                        power_node = G_copy.node[node]['power']
                        gn.disable_node(G_copy,node)
                        gn.cleanTheGraphForRouting(G=G_copy,tsd=tsd)
                        thereisapath = gn.routing(G=G_copy,tsd=tsd,N=N)
                        good = True
                        for s,d in G_copy.edges():
                            if G_copy.edge[s][d]['weight'] > gn.getCapacity():
                                good = False
                                break

                        #if good and thereisapath:
                            #print 'Node',node,'was removed'

                        if good == False:
                            #print 'The system goes over the capacity in the edge',s,d,G_copy.edge[s][d]['weight']
                            G_copy.add_node(node,type=node_type,enabled=True)
                            color_map[node] = color[node_type]
                            for s,d in adj:
                                G_copy.add_edge(s,d)
                            gn.cleanTheGraphForRouting(G=G_copy,tsd=tsd)
                            gn.routing(G=G_copy,tsd=tsd,N=N)
                            gn.setNodePower(G_copy,node)


                        if not thereisapath:
                            #print 'Removing the node',node,'the system is disconnected'
                            G_copy.add_node(node,type=node_type,enabled=True)
                            color_map[node] = color[node_type]
                            for s,d in adj:
                                G_copy.add_edge(s,d)
                            gn.cleanTheGraphForRouting(G=G_copy,tsd=tsd)
                            route = gn.routing(G=G_copy,tsd=tsd,N=N)
                            while not route:
                                for s in G_copy.nodes():
                                    for d in G_copy.nodes():
                                        if not G_copy.has_edge(s,d) and s!=d:
                                            G_copy.add_edge(s,d)
                                gn.cleanTheGraphForRouting(G=G_copy,tsd=tsd)
                                route = gn.routing(G=G_copy, tsd=tsd, N=N)
                                gn.setNodePower(G_copy, node)

                        for n in G_copy.nodes():
                            gn.setNodePower(G_copy, n)

                new_color_map = gn.getColorMap()

                plt.figure()
                title = 'After having disabled nodes | N = '+str(N)+ ' router ='+str(perc*100)+'%' # | Power = ' + str(gn.getPower2(G_copy))

                plt.title(title)
                nx.draw_networkx(G_copy, node_color=new_color_map)
                plt.show(block=False)

                print 'After removing nodes',gn.getPower2(G_copy)

                for n in G_copy.nodes():
                    gn.setNodePower(G_copy,n)
                    #print n,G_copy.node[n]['power']

                #trying to remove edges

                for n in G_copy.nodes():
                    routers = {}
                    edges_r = []

                    if G_copy.node[n]['enabled'] == False:
                        for s,d in G_copy.edges(n):
                            if G_copy.node[d]['type'] == 'access':
                                G_copy.remove_edge(s,d)
                                gn.cleanTheGraphForRouting(G_copy,tsd)
                                gn.routing(G_copy,tsd,N)

                    if G_copy.node[n]['type'] == 'access':
                        neighb = G_copy.edges(n)
                        for s,neigh in neighb:
                            if G_copy.node[neigh]['enabled'] == False:
                                G_copy.remove_edge(s,neigh)
                                gn.cleanTheGraphForRouting(G_copy,tsd)
                                gn.routing(G_copy,tsd,N)


                        #     if G_copy.node[neigh]['type'] == 'router':
                        #         routers[neigh] = G_copy.edge[n][neigh]
                        #
                        #
                        #
                        # if len(routers) > 1:
                        #     routers.__delitem__(max(routers.keys()))
                        #     for router in routers:
                        #         G_copy.remove_edge(n,router)
                        #         gn.cleanTheGraphForRouting(G_copy,tsd)
                        #         thereisapath = gn.routing(G_copy,tsd,N)
                        #         if thereisapath == False:
                        #             G_copy.add_edges_from([(n,router)],weight = routers[router]['weight'])
                        #


                for node in G_copy.nodes():
                    gn.setNodePower(G_copy,node)

                print 'After removing edges',gn.getPower2(G_copy)


                print 'Initial nodes', G.nodes()
                print 'Final node', G_copy.nodes()
                print 'Initial edges', len(G.edges())
                print 'Final edges', len(G_copy.edges())

                plt.figure()
                title = 'After removal of the edges | N = '+str(N)+ ' R ='+str(perc*100)+'% | Power = ' + str(gn.getPower2(G_copy))
                plt.title(title)
                nx.draw_networkx(G_copy,node_color = new_color_map)
                plt.show()