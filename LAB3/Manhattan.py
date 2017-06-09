import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

G = nx.DiGraph()
N = 16
nodes = range(N)

for i in nodes:
    if i == 0:
        G.add_edges_from([(i, i+3),(i,i+1),(i, i+4),(i, i+12)])

    elif i == 3:
        G.add_edges_from([(i,i-3),(i,i-1),(i, i+4),(i, i+12)])

    elif i == 15:
        G.add_edges_from([(i,i-4),(i,i-1),(i,i-3),(i,i-12)])

    elif i == 12:
        G.add_edges_from([(i,i-4),(i,i+1),(i,i+3),(i,i-12)])

    elif i == 7 or i == 11:
        G.add_edges_from([(i,i+4),(i,i-4),(i,i-1),(i,i-3)])

    elif i == 4 or i == 8:
        G.add_edges_from([(i,i+3),(i,i+1),(i, i+4),(i, i-4)])

    elif i > 0 and i < 3:
        G.add_edges_from([(i,i-1),(i,i+1),(i, i+4),(i, i+12)])

    elif (i > 4 and i < 7) or (i > 8 and i < 11):
        G.add_edges_from([(i,i+1),(i,i-1),(i, i+4),(i,i-4)])

    elif i > 12 and i < 15:
        G.add_edges_from([(i,i+1),(i, i-1),(i, i-4),(i, i-12)])

# T_matrix = np.zeros((N, N))
#
# for u in nodes:
#     for v in nodes:
#         if u != v:
#             if (u,v)> 4 and (u,v) < 7 or (u,v) > 8 and (u,v) < 11:
#                 flow = np.random.uniform(1.0, 1.5)
#             else:
#                 flow = np.random.uniform(0.5, 1.5)
#             G.add_edges_from([(u, v)], weight=flow, capacity=np.random.randint(8, 12))
#             T_matrix[u, v] = flow

# np.set_printoptions(precision=3)
# print T_matrix

nx.draw_networkx(G, arrows=True, with_labels=True)
plt.show()