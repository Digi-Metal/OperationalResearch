from topology import Topology
from green import GreenNetwork
from matplotlib import pyplot as plt
import networkx as nx
N = 10

if __name__ == '__main__':
    gn = GreenNetwork(N,percentage_inactive=0.3,capacity=3,node_power = 2,link_power = 4,alpha=1)
    tsd = gn.createTrafficMatrix(0.5,1.5,N)

    G = nx.DiGraph()
    G = gn.createRandomTopology(N,tsd)
    gn.routing(G,tsd,N)

    for n in G.node:
        gn.setNodePower(G,n)

    print gn.getPower(G)

    G_copy = nx.DiGraph()
    G_copy = G.copy()
    nx.draw_networkx(G_copy,block=False)
    transient = gn.getTransient()
    for n in range(N):
        node = gn.getNodeMinimumPower(G_copy)[0]
        adj = G_copy.edges(node)
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

        nx.draw_networkx(G_copy)
       # plt.show()

    print gn.getPower(G_copy)