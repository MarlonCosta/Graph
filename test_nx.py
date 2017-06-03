import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_edges_from(['J' 'C', 'C' 'E', 'C' 'E', 'C' 'P', 'C' 'P', 'C' 'M', 'C' 'T', 'M' 'T', 'T' 'Z'])
d = nx.degree(G)

pos = nx.spring_layout(G)

nx.draw_networkx_labels(G, pos)
nx.draw(G, pos, nodelist=d.keys(), node_size=[v * 500 for v in d.values()])

plt.show()  # display
