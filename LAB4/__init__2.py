from topology import Topology
from green import GreenNetwork
from matplotlib import pyplot as plt
import scipy
import networkx as nx
import Queue
N = 20

if __name__ == '__main__':
    gn = GreenNetwork(N,percentage_inactive=0.5,capacity=100,node_power = 2,link_power = 4,alpha=0.5)
    tsd = gn.createTrafficMatrix(0.5,1.5,N)
    print tsd
    G = gn.createTopology(tsd)
    color_map = gn.getColorMap()


    nx.draw_networkx(G,node_color = color_map)
    plt.show(block = False)


    gn.routing(G,tsd,N)

    for n in G.node:
        gn.setNodePower(G,n)

    print gn.getPower(G)

    G_copy = G.copy()
    transient = gn.getTransient()
    for i in range(len(transient)-1):
        node = transient[i]
        adj = G_copy.edges(node)
        if gn.anyPeer(G_copy,node):
            G_copy.remove_node(node)
            gn.cleanTheGraphForRouting(G=G_copy,tsd=tsd)
            thereisapath = gn.routing(G=G_copy,tsd=tsd,N=N)
            good = True
            for s,d in G_copy.edges():
                if G.edge[s][d]['weight'] > gn.getCapacity():
                    good = False
                    break

            if good and thereisapath:
                print 'Node',node,'was removed'

            if good == False:
                print 'The system goes over the capacity in the edge',s,d,G_copy.edge[s][d]['weight']
                G_copy.add_node(node)
                for s,d in adj:
                    G_copy.add_edge(s,d)
                gn.cleanTheGraphForRouting(G=G_copy,tsd=tsd)
                gn.routing(G=G_copy,tsd=tsd,N=N)


            if not thereisapath:
                print 'Removing the node',node,'the system is disconnected'
                G_copy.add_node(node)
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


            for n in G_copy.nodes():
                gn.setNodePower(G_copy, n)


    new_color_map = []

    for node in G_copy.nodes():
        if G_copy.node[node]['type'] == 'access':
            new_color_map.append('grey')
        if G_copy.node[node]['type'] == 'router':
            new_color_map.append('red')
        if G_copy.node[node]['type'] == 'central':
            new_color_map.append('green')


    print gn.getPower(G_copy)

    plt.figure()
    nx.draw_networkx(G_copy,node_color = new_color_map)
    plt.show()